"""Measure storyboard panel picture boxes from page structure.

Each row of panels has a paper header band (number + time) and a paper caption band;
frame lines inside the header band come in triples per panel: left edge, number-box
separator, right edge. The picture is between the header and caption bands. Boxes are
[left, top, right, bottom], inset past the frame lines. Results are checked visually.
"""
import numpy as np
from PIL import Image


def _runs(mask, min_len):
    runs, start = [], None
    for i, v in enumerate(list(mask) + [False]):
        if v and start is None:
            start = i
        elif not v and start is not None:
            if i - start >= min_len:
                runs.append((start, i - 1))
            start = None
    return runs


def _lines(dark, y0, y1):
    cf = dark[y0:y1 + 1, :].mean(0)
    return [int((a + b) / 2) for a, b in _runs(cf > 0.85, 1)]


def detect(path, expected, inset=3):
    im = np.asarray(Image.open(path).convert("RGB")).astype(int)
    H, W, _ = im.shape
    mn, mx = im.min(2), im.max(2)
    paper = (mn > 200) & (mx - mn < 40)
    dark = im.sum(2) < 400
    runs = [r for r in _runs(paper[:, 30:-30].mean(1) > 0.55, 8) if r[0] > 120]
    headers = [r for r in runs if 30 <= r[1] - r[0] <= 45]
    captions = [r for r in runs if r[1] - r[0] > 45]
    rows = []
    for h in headers:
        cap = next((c for c in captions if c[0] > h[1] + 100), None)
        if cap:
            rows.append((h, cap))
    # A row whose header tabs are short (not a full-width paper band): find it from the
    # caption that has no header, and read lines from the tab rows just above the picture.
    used = {c for _, c in rows}
    for cap in captions:
        if cap in used or cap[0] < 300:
            continue
        prev_gap = max((r for r in runs if r[1] < cap[0] and r[1] - r[0] < 25), key=lambda r: r[1], default=None)
        if prev_gap:
            rows.append(((prev_gap[1] + 4, prev_gap[1] + 42), cap, "tab"))
    boxes = []
    for row in sorted(rows):
        (h0, h1), (c0, c1) = row[0], row[1]
        if len(row) == 3:
            # short header tabs: panel edges come from the caption band (only frame lines
            # there); keep the triple shape by inserting a dummy separator per panel.
            edges = _lines(dark, c0 + 3, c1 - 3)
            xs = []
            for k in range(0, len(edges) - 1, 2):
                xs += [edges[k], edges[k] + 1, edges[k + 1]]
        else:
            xs = _lines(dark, h0, h1)
        # triples: left, separator, right
        i = 0
        while i + 2 < len(xs):
            left, right = xs[i], xs[i + 2]
            if right - left < 150:
                i += 1
                continue
            top, bottom = h1 + 1, c0
            # skip only the frame line itself (a few rows), never into the picture
            for _ in range(5):
                if dark[top, left + 8:right - 8].mean() > 0.6:
                    top += 1
            for _ in range(5):
                if dark[bottom - 1, left + 8:right - 8].mean() > 0.6:
                    bottom -= 1
            boxes.append([left + 2 + inset, top + inset, right - 1 - inset, bottom - inset])
            i += 3
    if len(boxes) != expected:
        raise ValueError(f"{path}: found {len(boxes)} panels, expected {expected}")
    return boxes
