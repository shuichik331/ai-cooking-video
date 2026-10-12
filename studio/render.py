"""FFmpeg assembly and ffprobe verification of the final 9:16 video.

Each scene clip is trimmed to its storyboard duration, normalized (size, fps, pixel
format, audio) and concatenated in storyboard order. The output is then probed and
checked against the storyboard before anything reports success.
"""
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from .project import REPO_ROOT, load_json, resolve_asset

VIDEO_SETTINGS = REPO_ROOT / "config" / "video-settings.json"
FIT_FILTERS = {
    "pad": "scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2",
    "crop": "scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}",
}


class RenderError(Exception):
    pass


def require_ffmpeg():
    missing = [tool for tool in ("ffmpeg", "ffprobe") if not shutil.which(tool)]
    if missing:
        raise RenderError(f"not installed: {', '.join(missing)}")


def probe(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
        check=True, capture_output=True, text=True,
    ).stdout
    data = json.loads(out)
    video = next((s for s in data["streams"] if s["codec_type"] == "video"), None)
    audio = next((s for s in data["streams"] if s["codec_type"] == "audio"), None)
    return {"duration": float(data["format"].get("duration", 0)), "video": video, "audio": audio}


def _fps(stream):
    num, den = stream["r_frame_rate"].split("/")
    return float(num) / float(den or 1)


def collect_clips(project, use_manifest=False, allow_unapproved=False):
    """[(scene, clip_path, trim_in)] in storyboard order, or raise listing every problem."""
    problems, clips = [], []
    scene_status = project.status.get("scenes", {})
    manifest = (project.manifest or {}).get("scenes", {})
    for scene in project.scenes:
        sid = scene["id"]
        entry = scene_status.get(sid, {})
        path = manifest.get(sid) if use_manifest else entry.get("asset_path")
        if not path:
            problems.append(f"{sid}: no clip path")
            continue
        path = resolve_asset(path)
        if not path.is_file():
            problems.append(f"{sid}: file not found {path}")
            continue
        if not allow_unapproved and not entry.get("approved"):
            problems.append(f"{sid}: not approved")
            continue
        clips.append((scene, path, entry.get("trim_in_seconds")))
    if problems:
        raise RenderError("cannot render:\n  " + "\n  ".join(problems))
    return clips


def _trim_in(source_duration, use_seconds, anchor, explicit):
    if explicit is not None:
        start = float(explicit)
    elif anchor == "center":
        start = (source_duration - use_seconds) / 2
    else:
        start = 0.0
    if start < 0 or start + use_seconds > source_duration + 1e-3:
        raise RenderError(f"trim window {start:.2f}+{use_seconds}s exceeds clip length {source_duration:.2f}s")
    return start


def _concat_input(listfile, files):
    listfile.write_text("".join(f"file '{Path(f).as_posix()}'\n" for f in files), encoding="utf-8")
    return ["-f", "concat", "-safe", "0", "-i", str(listfile)]


def render(project, output, fit="pad", trim_anchor="start", audio=True,
           use_manifest=False, allow_unapproved=False, settings=None, keep_temp=False):
    require_ffmpeg()
    if fit not in FIT_FILTERS:
        raise RenderError(f"unknown fit {fit!r}")
    settings = settings or load_json(VIDEO_SETTINGS)
    w, h, fps = settings["width"], settings["height"], settings["fps"]
    clips = collect_clips(project, use_manifest, allow_unapproved)
    vf = FIT_FILTERS[fit].format(w=w, h=h) + f",fps={fps},setsar=1,format=yuv420p"
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)

    tmp = Path(tempfile.mkdtemp(prefix="render-"))
    try:
        video_segments, audio_segments = [], []
        for idx, (scene, path, explicit_in) in enumerate(clips):
            use = scene["end_seconds"] - scene["start_seconds"]
            info = probe(path)
            start = _trim_in(info["duration"], use, trim_anchor, explicit_in)
            stem = tmp / f"{idx:03d}_{scene['id']}"
            # Exact frame count per scene keeps the cut points on the storyboard timeline.
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{start:.3f}", "-i", str(path),
                            "-map", "0:v:0", "-vf", vf, "-frames:v", str(round(use * fps)),
                            "-c:v", settings["video_codec"], "-preset", "medium", "-crf", "18", "-an",
                            f"{stem}.mp4"], check=True)
            video_segments.append(f"{stem}.mp4")
            if audio:
                # PCM segments concatenate sample-exactly; AAC is encoded once at the end.
                src = ["-ss", f"{start:.3f}", "-i", str(path), "-map", "0:a:0"] if info["audio"] else \
                      ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
                subprocess.run(["ffmpeg", "-v", "error", "-y", *src,
                                "-af", f"aresample=48000,apad,atrim=0:{use}", "-ac", "2", "-t", f"{use}",
                                "-c:a", "pcm_s16le", f"{stem}.wav"], check=True)
                audio_segments.append(f"{stem}.wav")
        cmd = ["ffmpeg", "-v", "error", "-y", *_concat_input(tmp / "video.txt", video_segments)]
        if audio:
            cmd += [*_concat_input(tmp / "audio.txt", audio_segments), "-map", "0:v", "-map", "1:a",
                    "-c:a", settings["audio_codec"], "-b:a", "192k", "-shortest"]
        cmd += ["-c:v", "copy", "-movflags", "+faststart", str(output)]
        subprocess.run(cmd, check=True)
    finally:
        if not keep_temp:
            shutil.rmtree(tmp, ignore_errors=True)
    return verify(output, project, settings, expect_audio=audio)


def verify(path, project=None, settings=None, expect_audio=None, tolerance=0.15):
    """Probe a rendered file and compare it with the delivery spec and storyboard."""
    require_ffmpeg()
    settings = settings or load_json(VIDEO_SETTINGS)
    path = Path(path)
    if not path.is_file():
        return {"path": str(path), "verified": False, "problems": ["file not found"]}
    info = probe(path)
    problems = []
    v = info["video"]
    if v is None:
        problems.append("no video stream")
    else:
        if (v["width"], v["height"]) != (settings["width"], settings["height"]):
            problems.append(f"size {v['width']}x{v['height']} != {settings['width']}x{settings['height']}")
        if abs(_fps(v) - settings["fps"]) > 0.01:
            problems.append(f"fps {_fps(v):.3f} != {settings['fps']}")
        if v.get("codec_name") != "h264":
            problems.append(f"video codec {v.get('codec_name')} != h264")
        if v.get("pix_fmt") != "yuv420p":
            problems.append(f"pixel format {v.get('pix_fmt')} != yuv420p")
    if expect_audio is True and info["audio"] is None:
        problems.append("no audio stream")
    if expect_audio is True and info["audio"] and info["audio"].get("codec_name") != "aac":
        problems.append(f"audio codec {info['audio'].get('codec_name')} != aac")
    expected = project.storyboard.get("duration_seconds") if project else None
    if expected is not None and abs(info["duration"] - expected) > tolerance:
        problems.append(f"duration {info['duration']:.3f}s != storyboard {expected}s (±{tolerance})")
    return {
        "path": str(path),
        "verified": not problems,
        "problems": problems,
        "duration_seconds": round(info["duration"], 3),
        "width": v and v["width"],
        "height": v and v["height"],
        "fps": v and round(_fps(v), 3),
        "audio": bool(info["audio"]),
    }
