#!/usr/bin/env python3
"""Production CLI. No command here calls a paid API.

  list [--all]                         projects with not_started / ready_for_generation
  validate [PROJECT...] [--record]     validate project files (and record result in status)
  sheet PROJECT                        write generation-sheet.json / .md (verbatim creative fields)
  status PROJECT --set STATUS          guarded overall status transition
  scene PROJECT SCENE STATUS [--asset] set a scene status (approve/reject after human review)
  discrepancy PROJECT SCENE ...        record a reference/JSON conflict and its decision
  plan PROJECT --resolution R          build generation requests; writes queue only with approval
  record-job PROJECT SCENE JOB_ID ...  record a submitted Higgsfield job
  register-clip PROJECT SCENE PATH     attach a generated/uploaded clip (probed, not approved)
  render PROJECT --output OUT          assemble approved clips with FFmpeg and verify
  verify VIDEO [--project P]           ffprobe check against delivery spec and storyboard
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from studio import higgsfield, render, scene_sheet, status  # noqa: E402
from studio.project import ACTIONABLE_STATUSES, PROJECTS_DIR, discover_projects, load_project, write_json  # noqa: E402
from studio.validate import validate_project  # noqa: E402


def _project(name):
    path = Path(name)
    root = path if path.is_dir() else PROJECTS_DIR / name
    if not (root / "storyboard.json").is_file():
        sys.exit(f"no project at {root}")
    return load_project(root)


def _save(project):
    write_json(project.status_path, project.status)


def cmd_list(args):
    projects = discover_projects(statuses=None if args.all else ACTIONABLE_STATUSES)
    if not projects:
        print("no matching projects")
    for p in projects:
        report = validate_project(p)
        print(f"{p.id:24} {p.status.get('overall_status', '?'):22} {len(p.scenes):3} scenes  {report.summary()}")


def cmd_validate(args):
    projects = [_project(n) for n in args.projects] or discover_projects()
    failed = False
    for p in projects:
        report = validate_project(p)
        print(report.summary())
        for issue in report.issues:
            if issue.severity != "warning" or args.verbose:
                print(f"  {issue}")
        if args.record:
            status.record_validation(p, report)
            _save(p)
        failed |= not report.ok
    sys.exit(1 if failed else 0)


def cmd_sheet(args):
    p = _project(args.project)
    report = validate_project(p)
    if not report.ok:
        sys.exit(f"validation errors; fix the creative files first:\n" + "\n".join(map(str, report.errors)))
    sheet = scene_sheet.build_sheet(p, report)
    write_json(p.root / "generation-sheet.json", sheet)
    (p.root / "generation-sheet.md").write_text(scene_sheet.render_markdown(sheet), encoding="utf-8")
    print(f"wrote {p.root / 'generation-sheet.json'} and .md ({sheet['scene_count']} scenes)")
    print("estimated credits:", scene_sheet.estimate_credits(sheet))


def cmd_status(args):
    p = _project(args.project)
    report = validate_project(p)
    try:
        status.set_overall(p, args.set, report)
    except status.StatusError as exc:
        sys.exit(str(exc))
    status.record_validation(p, report)
    _save(p)
    print(f"{p.id}: overall_status = {args.set}")


def cmd_scene(args):
    p = _project(args.project)
    try:
        status.set_scene(p, args.scene, args.status, asset_path=args.asset, note=args.note)
    except status.StatusError as exc:
        sys.exit(str(exc))
    _save(p)
    print(f"{p.id} {args.scene}: {args.status}")


def cmd_discrepancy(args):
    p = _project(args.project)
    status.record_discrepancy(p, args.scene, args.source, args.issue, args.resolution, args.decided_by)
    status.record_validation(p, validate_project(p))
    _save(p)
    print(f"recorded discrepancy for {args.scene}")


def cmd_plan(args):
    p = _project(args.project)
    report = validate_project(p)
    config = scene_sheet.load_generation_config()
    sheet = scene_sheet.build_sheet(p, report, config)
    requests = higgsfield.build_requests(p, sheet, config, args.resolution, args.audio, args.scenes)
    total = sum(r.estimated_credits or 0 for r in requests)
    print(f"{len(requests)} request(s), estimated {total} credits at {args.resolution} (observed prices; re-quote first)")
    try:
        approval = higgsfield.check_approval(p, requests)
    except higgsfield.ApprovalError as exc:
        print(f"NOT QUEUED: {exc}")
        return
    higgsfield.write_queue(p, requests, approval)
    print(f"queued in {p.root / higgsfield.QUEUE_FILE}")


def cmd_record_job(args):
    p = _project(args.project)
    higgsfield.record_job(p, args.scene, args.job_id, args.credits, args.resolution)
    _save(p)


def cmd_register_clip(args):
    p = _project(args.project)
    try:
        higgsfield.register_clip(p, args.scene, args.path)
    except status.StatusError as exc:
        sys.exit(str(exc))
    _save(p)
    print(f"{args.scene}: generated (awaiting human review)")


def cmd_render(args):
    p = _project(args.project)
    try:
        result = render.render(p, args.output, fit=args.fit, trim_anchor=args.trim_anchor, audio=not args.no_audio,
                               use_manifest=args.manifest, allow_unapproved=args.draft)
    except render.RenderError as exc:
        sys.exit(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.record and not args.draft:
        p.status["render"] = {**result, "rendered_at": status.now_iso(), "fit": args.fit, "trim_anchor": args.trim_anchor}
        _save(p)
    sys.exit(0 if result["verified"] else 1)


def cmd_verify(args):
    p = _project(args.project) if args.project else None
    result = render.verify(args.video, p, expect_audio=None if args.audio is None else args.audio == "yes")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["verified"] else 1)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("list"); s.add_argument("--all", action="store_true"); s.set_defaults(fn=cmd_list)
    s = sub.add_parser("validate"); s.add_argument("projects", nargs="*")
    s.add_argument("--record", action="store_true"); s.add_argument("-v", "--verbose", action="store_true")
    s.set_defaults(fn=cmd_validate)
    s = sub.add_parser("sheet"); s.add_argument("project"); s.set_defaults(fn=cmd_sheet)
    s = sub.add_parser("status"); s.add_argument("project")
    s.add_argument("--set", required=True, choices=status.OVERALL_STATUSES); s.set_defaults(fn=cmd_status)
    s = sub.add_parser("scene"); s.add_argument("project"); s.add_argument("scene")
    s.add_argument("status", choices=status.SCENE_STATUSES); s.add_argument("--asset"); s.add_argument("--note")
    s.set_defaults(fn=cmd_scene)
    s = sub.add_parser("discrepancy"); s.add_argument("project"); s.add_argument("scene")
    s.add_argument("--source", required=True); s.add_argument("--issue", required=True)
    s.add_argument("--resolution", required=True); s.add_argument("--decided-by", required=True)
    s.set_defaults(fn=cmd_discrepancy)
    s = sub.add_parser("plan"); s.add_argument("project"); s.add_argument("--resolution", required=True)
    s.add_argument("--audio", action="store_true"); s.add_argument("--scenes", nargs="*")
    s.set_defaults(fn=cmd_plan)
    s = sub.add_parser("record-job"); s.add_argument("project"); s.add_argument("scene"); s.add_argument("job_id")
    s.add_argument("--credits", type=float, required=True); s.add_argument("--resolution", required=True)
    s.set_defaults(fn=cmd_record_job)
    s = sub.add_parser("register-clip"); s.add_argument("project"); s.add_argument("scene"); s.add_argument("path")
    s.set_defaults(fn=cmd_register_clip)
    s = sub.add_parser("render"); s.add_argument("project"); s.add_argument("--output", required=True)
    s.add_argument("--fit", choices=list(render.FIT_FILTERS), default="pad")
    s.add_argument("--trim-anchor", choices=["start", "center"], default="start")
    s.add_argument("--no-audio", action="store_true")
    s.add_argument("--manifest", action="store_true", help="take clip paths from manifest.json")
    s.add_argument("--draft", action="store_true", help="allow unapproved clips (preview only, never recorded)")
    s.add_argument("--record", action="store_true"); s.set_defaults(fn=cmd_render)
    s = sub.add_parser("verify"); s.add_argument("video"); s.add_argument("--project")
    s.add_argument("--audio", choices=["yes", "no"]); s.set_defaults(fn=cmd_verify)

    args = ap.parse_args(argv)
    args.fn(args)


if __name__ == "__main__":
    main()
