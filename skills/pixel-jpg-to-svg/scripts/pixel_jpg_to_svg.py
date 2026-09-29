#!/usr/bin/env python3
"""Reconstruct pixel-art JPG/PNG as a crisp SVG of merged rectangles."""

from __future__ import annotations

import argparse
import os
from collections import defaultdict

import numpy as np
from PIL import Image, ImageDraw


def load_rgb(path: str) -> np.ndarray:
    return np.array(Image.open(path).convert("RGB")).astype(np.float32)


def auto_bg(im: np.ndarray) -> np.ndarray:
    flat = im.reshape(-1, 3).astype(np.int32)
    # quantize slightly so JPEG noise does not explode unique counts
    key = (flat[:, 0] << 16) | (flat[:, 1] << 8) | flat[:, 2]
    vals, counts = np.unique(key, return_counts=True)
    k = vals[int(counts.argmax())]
    return np.array([(k >> 16) & 255, (k >> 8) & 255, k & 255], dtype=np.float32)


def grid_score(im: np.ndarray, bg: np.ndarray, period: int, ox: int, oy: int, bg_dist: float):
    h, w, _ = im.shape
    H = ((h - oy) // period) * period
    W = ((w - ox) // period) * period
    if H < period or W < period:
        return 1e9, 0
    crop = im[oy : oy + H, ox : ox + W]
    gh, gw = H // period, W // period
    cells = crop.reshape(gh, period, gw, period, 3).swapaxes(1, 2)
    flat = cells.reshape(gh, gw, period * period, 3)
    var = flat.var(axis=2).mean(axis=2)
    mean = flat.mean(axis=2)
    fg = np.linalg.norm(mean - bg, axis=2) > bg_dist
    if not fg.any():
        return 1e9, 0
    return float(var[fg].mean()), int(fg.sum())


def detect_grid(im: np.ndarray, bg: np.ndarray, bg_dist: float, periods: list[int]):
    best = (1e9, 20, 0, 0)
    for period in periods:
        local = []
        for ox in range(period):
            for oy in range(period):
                v, n = grid_score(im, bg, period, ox, oy, bg_dist)
                local.append((v, period, ox, oy, n))
        local.sort()
        if local and local[0][0] < best[0]:
            best = (local[0][0], local[0][1], local[0][2], local[0][3])
    return best[1], best[2], best[3], best[0]


def sample_grid(im: np.ndarray, period: int, ox: int, oy: int):
    h, w, _ = im.shape
    H = ((h - oy) // period) * period
    W = ((w - ox) // period) * period
    crop = im[oy : oy + H, ox : ox + W]
    gh, gw = H // period, W // period
    cells = crop.reshape(gh, period, gw, period, 3).swapaxes(1, 2)
    med = np.median(cells.reshape(gh, gw, period * period, 3), axis=2)
    return med


def cluster_colors(med: np.ndarray, fg_mask: np.ndarray, thresh: float):
    coords = list(zip(*np.where(fg_mask)))
    if not coords:
        raise SystemExit("No foreground cells. Relax --bg-dist or set --bg-rgb / --auto-bg.")
    cols = np.array([med[y, x] for y, x in coords])
    centers: list[list] = []
    assign = np.zeros(len(coords), dtype=int)
    for i, c in enumerate(cols):
        if not centers:
            centers.append([c.copy(), 1])
            assign[i] = 0
            continue
        means = np.array([ct[0] for ct in centers])
        d = np.linalg.norm(means - c, axis=1)
        j = int(d.argmin())
        if d[j] <= thresh:
            s, cnt = centers[j]
            centers[j][0] = (s * cnt + c) / (cnt + 1)
            centers[j][1] = cnt + 1
            assign[i] = j
        else:
            assign[i] = len(centers)
            centers.append([c.copy(), 1])
    palette = [tuple(int(x) for x in np.clip(np.round(ct[0]), 0, 255)) for ct in centers]
    gh, gw = med.shape[:2]
    idx_map = np.full((gh, gw), -1, dtype=int)
    for i, (y, x) in enumerate(coords):
        idx_map[y, x] = assign[i]
    return palette, idx_map


def merge_vertical(runs):
    runs = sorted(runs, key=lambda r: (r[0], r[1], r[2]))
    used = [False] * len(runs)
    out = []
    for i, r in enumerate(runs):
        if used[i]:
            continue
        x, y, w, h = r
        used[i] = True
        changed = True
        while changed:
            changed = False
            for j, r2 in enumerate(runs):
                if used[j]:
                    continue
                x2, y2, w2, h2 = r2
                if x2 == x and w2 == w and y2 == y + h:
                    h += h2
                    used[j] = True
                    changed = True
        out.append((x, y, w, h))
    return out


def collect_rects(idx_map: np.ndarray, pad: int):
    ys, xs = np.where(idx_map >= 0)
    y0 = max(0, int(ys.min()) - pad)
    x0 = max(0, int(xs.min()) - pad)
    y1 = min(idx_map.shape[0] - 1, int(ys.max()) + pad)
    x1 = min(idx_map.shape[1] - 1, int(xs.max()) + pad)
    runs_by_color = defaultdict(list)
    for y in range(y0, y1 + 1):
        x = x0
        while x <= x1:
            cid = int(idx_map[y, x])
            if cid < 0:
                x += 1
                continue
            x2 = x
            while x2 + 1 <= x1 and int(idx_map[y, x2 + 1]) == cid:
                x2 += 1
            runs_by_color[cid].append((x - x0, y - y0, x2 - x + 1, 1))
            x = x2 + 1
    for cid in list(runs_by_color):
        runs_by_color[cid] = merge_vertical(runs_by_color[cid])
    return runs_by_color, x1 - x0 + 1, y1 - y0 + 1


def hexcol(rgb) -> str:
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"


def write_svg(path: str, palette, runs_by_color, cw: int, ch: int, scale: int, label: str):
    order = sorted(
        runs_by_color.keys(),
        key=lambda i: 0.2126 * palette[i][0] + 0.7152 * palette[i][1] + 0.0722 * palette[i][2],
    )
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {cw} {ch}" '
            f'width="{cw * scale}" height="{ch * scale}" role="img" '
            f'aria-label="{label}">'
        ),
        "  <!-- Pixel-grid reconstruction. Background is transparent. -->",
        '  <g shape-rendering="crispEdges">',
    ]
    for cid in order:
        lines.append(f'    <g fill="{hexcol(palette[cid])}">')
        for x, y, rw, rh in sorted(runs_by_color[cid], key=lambda t: (t[1], t[0])):
            lines.append(f'      <rect x="{x}" y="{y}" width="{rw}" height="{rh}"/>')
        lines.append("    </g>")
    lines.append("  </g>")
    lines.append("</svg>")
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return order


def write_preview(path: str, palette, runs_by_color, order, cw: int, ch: int, scale: int):
    prev = Image.new("RGBA", (cw * scale, ch * scale), (0, 0, 0, 0))
    draw = ImageDraw.Draw(prev)
    for cid in order:
        rgb = palette[cid] + (255,)
        for x, y, rw, rh in runs_by_color[cid]:
            draw.rectangle(
                [x * scale, y * scale, (x + rw) * scale - 1, (y + rh) * scale - 1],
                fill=rgb,
            )
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    prev.save(path)
    return prev


def parse_args():
    p = argparse.ArgumentParser(description="Pixel-art JPG/PNG to SVG")
    p.add_argument("input")
    p.add_argument("--out-svg", default="logo.svg")
    p.add_argument("--out-preview", default="logo_preview.png")
    p.add_argument("--period", type=int, default=0, help="0 = auto detect")
    p.add_argument("--ox", type=int, default=-1)
    p.add_argument("--oy", type=int, default=-1)
    p.add_argument("--periods", default="16,20,24,32")
    p.add_argument("--thresh", type=float, default=14.0)
    p.add_argument("--bg-dist", type=float, default=22.0)
    p.add_argument("--bg-rgb", nargs=3, type=int, default=None)
    p.add_argument("--auto-bg", action="store_true")
    p.add_argument("--pad", type=int, default=2)
    p.add_argument("--preview-scale", type=int, default=24)
    p.add_argument("--svg-scale", type=int, default=20)
    p.add_argument("--label", default="Pixel art logo")
    p.add_argument("--transparent", action="store_true", default=True)
    return p.parse_args()


def main():
    args = parse_args()
    im = load_rgb(args.input)
    if args.auto_bg:
        bg = auto_bg(im)
    elif args.bg_rgb:
        bg = np.array(args.bg_rgb, dtype=np.float32)
    else:
        bg = np.array([15.0, 26.0, 44.0], dtype=np.float32)

    if args.period and args.ox >= 0 and args.oy >= 0:
        period, ox, oy = args.period, args.ox, args.oy
        score = grid_score(im, bg, period, ox, oy, args.bg_dist)[0]
    elif args.period:
        period = args.period
        best = (1e9, 0, 0)
        for ox in range(period):
            for oy in range(period):
                v, _ = grid_score(im, bg, period, ox, oy, args.bg_dist)
                if v < best[0]:
                    best = (v, ox, oy)
        ox, oy, score = best[1], best[2], best[0]
    else:
        periods = [int(x) for x in args.periods.split(",") if x.strip()]
        period, ox, oy, score = detect_grid(im, bg, args.bg_dist, periods)

    med = sample_grid(im, period, ox, oy)
    fg_mask = np.linalg.norm(med - bg, axis=2) > args.bg_dist
    palette, idx_map = cluster_colors(med, fg_mask, args.thresh)
    runs_by_color, cw, ch = collect_rects(idx_map, args.pad)
    order = write_svg(args.out_svg, palette, runs_by_color, cw, ch, args.svg_scale, args.label)
    write_preview(args.out_preview, palette, runs_by_color, order, cw, ch, args.preview_scale)

    nrect = sum(len(v) for v in runs_by_color.values())
    print(f"grid period={period} ox={ox} oy={oy} var={score:.2f}")
    print(f"canvas={cw}x{ch} colors={len(runs_by_color)} rects={nrect}")
    print(f"bg=({int(bg[0])},{int(bg[1])},{int(bg[2])}) thresh={args.thresh}")
    print(f"wrote {args.out_svg}")
    print(f"wrote {args.out_preview}")


if __name__ == "__main__":
    main()
