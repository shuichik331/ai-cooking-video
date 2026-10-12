"""Crop storyboard panels out of page images (FFmpeg only, no extra dependencies).

The grid geometry comes from projects/<id>/panel-layout.json and must be confirmed by
looking at the real pages; nothing here guesses it. Example:

{
  "pages": {
    "storyboard-pages/page-01.png": {
      "grid": {"rows": 7, "cols": 2},
      "area": {"left": 0.03, "top": 0.06, "right": 0.97, "bottom": 0.98},
      "panel_inset": {"left": 0.02, "top": 0.02, "right": 0.02, "bottom": 0.18}
    }
  }
}

area: the region holding the grid, as fractions of the page.
panel_inset: fractions of each cell to drop (borders, caption/timecode bars).
Panels are read left-to-right, top-to-bottom and matched to pages.json scene_ids in order.
"""
import subprocess
from pathlib import Path

from .project import REPO_ROOT, load_json
from .render import probe

LAYOUT_FILE = "panel-layout.json"
CROP_DIR = REPO_ROOT / "media"


class PanelError(Exception):
    pass


def load_layout(project):
    path = project.root / LAYOUT_FILE
    if not path.is_file():
        raise PanelError(f"{path} missing: confirm the panel grid from the real page images first")
    return load_json(path)


def panel_boxes(width, height, spec, count):
    rows, cols = spec["grid"]["rows"], spec["grid"]["cols"]
    if rows * cols < count:
        raise PanelError(f"grid {rows}x{cols} has fewer cells than {count} scenes")
    area = {"left": 0, "top": 0, "right": 1, "bottom": 1, **spec.get("area", {})}
    inset = {"left": 0, "top": 0, "right": 0, "bottom": 0, **spec.get("panel_inset", {})}
    cell_w = (area["right"] - area["left"]) * width / cols
    cell_h = (area["bottom"] - area["top"]) * height / rows
    boxes = []
    for i in range(count):
        r, c = divmod(i, cols)
        x0 = area["left"] * width + c * cell_w + inset["left"] * cell_w
        y0 = area["top"] * height + r * cell_h + inset["top"] * cell_h
        w = cell_w * (1 - inset["left"] - inset["right"])
        h = cell_h * (1 - inset["top"] - inset["bottom"])
        if w < 16 or h < 16:
            raise PanelError("panel inset leaves an empty crop")
        # Even sizes keep downstream encoders happy.
        boxes.append(tuple(int(v) // 2 * 2 for v in (x0, y0, w, h)))
    return boxes


def crop_panels(project, out_dir=None, scene_ids=None):
    """Write <out_dir>/<scene>.png for each panel; returns {scene_id: path}."""
    layout = load_layout(project)
    out_dir = Path(out_dir or CROP_DIR / project.id / "panels")
    out_dir.mkdir(parents=True, exist_ok=True)
    written = {}
    for page in (project.pages or {}).get("pages", []):
        image = project.root / page["file"]
        if not image.is_file():
            raise PanelError(f"{page['file']} not found")
        spec = layout["pages"].get(page["file"])
        if spec is None:
            raise PanelError(f"{LAYOUT_FILE} has no entry for {page['file']}")
        video = probe(image)["video"]
        boxes = panel_boxes(video["width"], video["height"], spec, len(page["scene_ids"]))
        for sid, (x, y, w, h) in zip(page["scene_ids"], boxes):
            if scene_ids and sid not in scene_ids:
                continue
            dest = out_dir / f"{sid}.png"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(image),
                            "-vf", f"crop={w}:{h}:{x}:{y}", "-frames:v", "1", str(dest)], check=True)
            written[sid] = dest
    return written


def contact_sheet(crops, dest, cols=7):
    """Tile crops into one image for a quick human check of the crop/scene mapping."""
    files = list(crops.values())
    if not files:
        raise PanelError("no crops")
    inputs = []
    for f in files:
        inputs += ["-i", str(f)]
    scaled = "".join(f"[{i}:v]scale=240:240:force_original_aspect_ratio=decrease,pad=240:240:(ow-iw)/2:(oh-ih)/2:color=white[p{i}];" for i in range(len(files)))
    layout = "|".join(f"{(i % cols) * 240}_{(i // cols) * 240}" for i in range(len(files)))
    stack = "".join(f"[p{i}]" for i in range(len(files)))
    filt = scaled + (f"{stack}xstack=inputs={len(files)}:layout={layout}:fill=white" if len(files) > 1 else "[p0]null")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", filt, "-frames:v", "1", str(dest)],
                   check=True)
    return Path(dest)
