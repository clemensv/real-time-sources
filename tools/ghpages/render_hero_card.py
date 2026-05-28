"""Render the top-level 1200x630 Open Graph hero card for the portal.

This is the social-preview image used by ``share/index.html`` (the portal
homepage), as opposed to the per-source cards rendered by
``render_og_card.py``.

Layout (1200x630):

    +------------------------------------------------------------+
    |   [compass]   real-time-sources                            |
    |                                                             |
    |     Real-Time Sources                  (Inter Bold ~96pt)  |
    |     for Apache Kafka, MQTT & AMQP      (Inter SemiBold)    |
    |                                                             |
    |     105 live feeders · 12 categories · global              |
    |                                                             |
    |     ----------------------------------------------------    |
    |     [K] [M] [A] [Fab] [D]   Azure Event Hubs · Fabric ...  |
    +------------------------------------------------------------+
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

from PIL import Image, ImageDraw

# Re-use renderer primitives from the per-source card module.
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import render_og_card as og  # noqa: E402

CARD_W, CARD_H = og.CARD_W, og.CARD_H
PAD_X, PAD_Y = og.PAD_X, og.PAD_Y

COMPASS_PNG = HERE / "assets" / "compass.png"


def _compass_image(size: int, color: Tuple[int, int, int]) -> Image.Image:
    """Load the pre-baked compass PNG and tint it with ``color``."""
    if not COMPASS_PNG.exists():
        raise FileNotFoundError(
            f"{COMPASS_PNG} missing - run tools/ghpages/bake_compass.py")
    src = Image.open(COMPASS_PNG).convert("RGBA")
    src = src.resize((size, size), Image.LANCZOS)
    # Re-tint: alpha from source, RGB from `color`.
    r, g, b = color
    out = Image.new("RGBA", (size, size), (r, g, b, 0))
    out.putalpha(src.getchannel("A"))
    return out


def render_hero(out_path: Path, *, n_sources: int, n_categories: int,
                accent: Tuple[int, int, int] = (35, 92, 142)) -> Path:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    img = Image.new("RGB", (CARD_W, CARD_H), og.BG_DARK)
    og._gradient_band(img, accent)
    draw = ImageDraw.Draw(img, "RGBA")

    # ── Brand mark (compass + wordmark) ────────────────────────────────────
    top_y = PAD_Y
    cursor_x = PAD_X

    compass_size = 56
    compass = _compass_image(compass_size, og.TEXT_PRIMARY)
    img.paste(compass, (cursor_x, top_y), compass)
    cursor_x += compass_size + 18

    brand_fnt = og.font(og.FONT_SEMIBOLD, 30)
    og._draw_text(draw, (cursor_x, top_y + 16), "real-time-sources",
                  brand_fnt, og.TEXT_PRIMARY)

    # ── Title ──────────────────────────────────────────────────────────────
    title_top = top_y + 110
    title = "Real-Time Sources"
    title_fnt = og.font(og.FONT_BOLD, 104)
    og._draw_text(draw, (PAD_X, title_top), title, title_fnt, og.TEXT_PRIMARY)

    # ── Subtitle ───────────────────────────────────────────────────────────
    sub_top = title_top + 130
    sub_fnt = og.font(og.FONT_SEMIBOLD, 36)
    og._draw_text(draw, (PAD_X, sub_top),
                  "for Apache Kafka, MQTT 5.0 & AMQP 1.0",
                  sub_fnt, og.TEXT_SECONDARY)

    # ── Stats line ─────────────────────────────────────────────────────────
    stats_top = sub_top + 60
    stats_fnt = og.font(og.FONT_REGULAR, 30)
    stats = (
        f"{n_sources} live feeders   ·   {n_categories} categories   "
        f"·   global coverage"
    )
    og._draw_text(draw, (PAD_X, stats_top), stats, stats_fnt, og.TEXT_MUTED)

    # ── Footer rule + transport pills (with Azure/Fabric attribution) ─────
    rule_y = CARD_H - PAD_Y - 80
    draw.line([(PAD_X, rule_y), (CARD_W - PAD_X, rule_y)],
              fill=og.RULE, width=2)

    # Pills (left): K / M / A / Fab / Az — all on.
    pill_y = rule_y + 22
    pills: List[Tuple[str, Tuple[int, int, int]]] = [
        ("K",   og.C_KAFKA),
        ("M",   og.C_MQTT),
        ("A",   og.C_AMQP),
        ("Fab", og.C_FAB),
        ("Az",  og.C_AZURE),
    ]
    pill_fnt = og.font(og.FONT_BOLD, 30)
    px = PAD_X
    pad_x_pill = 18
    pad_y_pill = 8
    th = 32
    for label, bg in pills:
        tw = int(draw.textlength(label, font=pill_fnt))
        w = tw + pad_x_pill * 2
        h = th + pad_y_pill * 2
        draw.rounded_rectangle([px, pill_y, px + w, pill_y + h],
                               radius=10, fill=bg)
        tx = px + (w - tw) // 2
        ty = pill_y + (h - th) // 2 - 4
        draw.text((tx, ty), label, font=pill_fnt, fill=og.TEXT_PRIMARY)
        px += w + 12
    pills_right_edge = px

    # Attribution (right) — shrink + ellipsize if it would collide with pills.
    meta_fnt = og.font(og.FONT_REGULAR, 24)
    meta = "Azure Event Hubs · Service Bus · Event Grid · Microsoft Fabric"
    avail = CARD_W - PAD_X - pills_right_edge - 24
    if draw.textlength(meta, font=meta_fnt) > avail:
        meta = "Azure Event Hubs · Fabric"
        if draw.textlength(meta, font=meta_fnt) > avail:
            meta = "Azure · Fabric"
    meta_w = draw.textlength(meta, font=meta_fnt)
    og._draw_text(
        draw,
        (CARD_W - PAD_X - int(meta_w), pill_y + (th + 2 * pad_y_pill - 24) // 2),
        meta, meta_fnt, og.TEXT_MUTED,
    )

    img.save(out_path, format="PNG", optimize=True)
    return out_path


def _main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--catalog", default="catalog.json")
    p.add_argument("--out", required=True,
                   help="Output PNG path (e.g. og.png at portal root)")
    args = p.parse_args()

    catalog = json.loads(Path(args.catalog).read_text(encoding="utf-8"))
    n_sources = len({e["id"] for e in catalog})
    n_categories = len({(e.get("cat") or "").strip()
                        for e in catalog if e.get("cat")})

    out = render_hero(Path(args.out),
                      n_sources=n_sources, n_categories=n_categories)
    print(f"  [ok] hero card -> {out} ({n_sources} sources, {n_categories} cats)")
    return 0


if __name__ == "__main__":
    sys.exit(_main())
