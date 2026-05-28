"""Render a 1200x630 Open Graph social card for a single feeder source.

Designed for crawler-friendly preview cards on the gh-pages portal share
shells (``share/<sid>/index.html``). One PNG per source.

Layout (1200x630):

    +-----------------------------------------------------------+
    |  [flag]  CATEGORY ·  REGION                    [K M A]   |
    |                                                            |
    |   <Source Name>            (Inter Bold ~76pt)              |
    |   <description>            (Inter Regular ~32pt)           |
    |                                                            |
    |   keyed by {...}  ·  N event types                         |
    |                                                            |
    |   ----------------------------------------------------     |
    |   real-time-sources · Apache Kafka · MQTT · AMQP           |
    +-----------------------------------------------------------+

Usage::

    from tools.ghpages.render_og_card import render_card
    render_card(entry, out_path="share/bafu-hydro/og.png", flag_dir=...)
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys
import urllib.request
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont

# ── Paths ────────────────────────────────────────────────────────────────────
HERE = Path(__file__).resolve().parent
FONTS_DIR = HERE / "fonts"
FONT_REGULAR = FONTS_DIR / "Inter-Regular.ttf"
FONT_SEMIBOLD = FONTS_DIR / "Inter-SemiBold.ttf"
FONT_BOLD = FONTS_DIR / "Inter-Bold.ttf"

CARD_W, CARD_H = 1200, 630
PAD_X, PAD_Y = 72, 64

# ── Palette (RGB) ────────────────────────────────────────────────────────────
# Aligned with root README colour palette in tools/docs/generate_root_catalog.py.
C_KAFKA = (35, 31, 32)       # 231f20 — Apache Kafka brand black
C_MQTT  = (102, 0, 102)      # 660066 — MQTT brand purple
C_AMQP  = (26, 74, 120)      # 1a4a78 — AMQP blue
C_AZURE = (0, 120, 212)      # 0078d4 — Azure blue
C_FAB   = (17, 120, 101)     # 117865 — Fabric teal

# Category accent (background top-band). Falls back to a neutral slate.
CATEGORY_ACCENT: Dict[str, Tuple[int, int, int]] = {
    "Hydrology":                              (35, 92, 142),     # deep blue
    "Weather":                                (94, 109, 138),    # steel
    "Air Quality":                            (90, 120, 88),     # mossy green
    "Disaster Alerts and Civil Protection":   (170, 60, 50),     # warning red
    "Disasters":                              (170, 60, 50),
    "Radiation":                              (160, 120, 30),    # caution amber
    "Maritime":                               (28, 80, 110),     # navy
    "Aviation":                               (60, 90, 130),     # sky-navy
    "Transport":                              (180, 110, 30),    # signal orange
    "Railway":                                (90, 60, 100),     # purple-grey
    "Nightlife":                              (110, 50, 130),    # violet
    "Energy":                                 (200, 150, 30),    # electric gold
    "Energy and Infrastructure":              (200, 150, 30),
    "Social":                                 (90, 100, 130),    # cool slate
    "Public Events":                          (140, 90, 50),     # warm earth
    "Science":                                (60, 110, 130),    # teal
}

# Category emoji is too font-dependent; we use unicode glyphs that work in Inter.
CATEGORY_GLYPH: Dict[str, str] = {
    "Hydrology":                              "≈",  # waves
    "Weather":                                "☁",
    "Air Quality":                            "✦",
    "Disaster Alerts and Civil Protection":   "▲",
    "Disasters":                              "▲",
    "Radiation":                              "⚛",
    "Maritime":                               "⚓",
    "Aviation":                               "✈",
    "Transport":                              "⇄",
    "Railway":                                "▤",
    "Nightlife":                              "♪",
    "Energy":                                 "⚡",
    "Energy and Infrastructure":              "⚡",
    "Social":                                 "✉",
    "Public Events":                          "★",
    "Science":                                "◎",
}

# Background base (dark canvas) and surface tones.
BG_DARK = (15, 20, 28)
SURFACE = (24, 30, 42)
TEXT_PRIMARY = (245, 247, 250)
TEXT_SECONDARY = (175, 185, 200)
TEXT_MUTED = (130, 142, 160)
RULE = (50, 60, 75)


# ── Font cache ───────────────────────────────────────────────────────────────
_font_cache: Dict[Tuple[str, int], ImageFont.FreeTypeFont] = {}


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    """Return a (cached) Inter font at the given size."""
    key = (str(path), size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(str(path), size=size)
    return _font_cache[key]


# ── Flag loader (flagcdn.com PNG, with on-disk cache) ────────────────────────
def _ensure_flag(cc: str, cache_dir: Path) -> Optional[Path]:
    """Return path to a 1280x960 PNG of the requested country flag.

    Downloads from flagcdn.com once and caches under ``cache_dir``. Returns
    ``None`` if the download fails (renderer just skips the flag in that case).
    """
    cc = (cc or "").lower()
    if not cc:
        return None
    cache_dir.mkdir(parents=True, exist_ok=True)
    dest = cache_dir / f"{cc}.png"
    if dest.exists():
        return dest
    # flagcdn 1280px PNGs render crisply when scaled down to ~80–120px tall.
    url = f"https://flagcdn.com/w1280/{cc}.png"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            dest.write_bytes(resp.read())
        return dest
    except Exception as e:  # pragma: no cover — network best-effort
        print(f"  warn: flag {cc} download failed: {e}", file=sys.stderr)
        return None


# ── Drawing helpers ──────────────────────────────────────────────────────────
def _gradient_band(img: Image.Image, accent: Tuple[int, int, int]) -> None:
    """Paint a vertical gradient from the category accent (top) into the dark
    canvas tone (bottom). Subtle — keeps the card legible without screaming."""
    base = Image.new("RGB", (CARD_W, CARD_H), BG_DARK)
    overlay = Image.new("RGBA", (CARD_W, CARD_H), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    ar, ag, ab = accent
    # Fade alpha from ~110 at the top to 0 by ~60% of card height.
    for y in range(CARD_H):
        t = max(0.0, 1.0 - (y / (CARD_H * 0.55)))
        a = int(110 * (t ** 1.4))
        if a <= 0:
            break
        odraw.line([(0, y), (CARD_W, y)], fill=(ar, ag, ab, a))
    base.paste(overlay, (0, 0), overlay)
    img.paste(base, (0, 0))


def _draw_text(draw: ImageDraw.ImageDraw, xy: Tuple[int, int], text: str,
               fnt: ImageFont.FreeTypeFont, fill: Tuple[int, int, int]) -> Tuple[int, int]:
    """Draw text and return its (width, height)."""
    draw.text(xy, text, font=fnt, fill=fill)
    bbox = draw.textbbox(xy, text, font=fnt)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def _wrap(text: str, fnt: ImageFont.FreeTypeFont, max_w: int,
          draw: ImageDraw.ImageDraw) -> List[str]:
    """Greedy word-wrap to fit ``max_w`` pixels."""
    words = text.split()
    lines: List[str] = []
    cur = ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def _pill(draw: ImageDraw.ImageDraw, x: int, y: int, label: str,
          bg: Tuple[int, int, int], on: bool = True) -> int:
    """Render a square-ish transport pill (K / M / A). Returns x of right edge."""
    fnt = font(FONT_BOLD, 30)
    pad_x = 18
    pad_y = 8
    tw = int(draw.textlength(label, font=fnt))
    th = 32
    w = tw + pad_x * 2
    h = th + pad_y * 2
    fill = bg if on else (50, 55, 65)
    text_fill = (245, 247, 250) if on else (90, 100, 115)
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=fill)
    # Center text inside the pill.
    tx = x + (w - tw) // 2
    ty = y + (h - th) // 2 - 4
    draw.text((tx, ty), label, font=fnt, fill=text_fill)
    return x + w


# ── Region extraction ────────────────────────────────────────────────────────
def _region_from_desc(desc: str) -> str:
    """Pull a leading region marker from a description like
    ``"Switzerland — ~300 stations, FOEN"``. Returns ``""`` if absent."""
    if not desc:
        return ""
    # Split on em-dash, en-dash, or " - ".
    for sep in ("—", "–", " - "):
        if sep in desc:
            head = desc.split(sep, 1)[0].strip()
            if 0 < len(head) <= 40 and not head.endswith("."):
                return head
    return ""


def _scope_from_desc(desc: str) -> str:
    """Everything after the region marker. Falls back to the full desc."""
    if not desc:
        return ""
    for sep in ("—", "–", " - "):
        if sep in desc:
            return desc.split(sep, 1)[1].strip()
    return desc.strip()


# ── Public API ───────────────────────────────────────────────────────────────
def render_card(
    entry: Dict[str, Any],
    out_path: Path,
    *,
    flag_cache_dir: Path,
    flag_cc: str = "",
    region_override: str = "",
) -> Path:
    """Render the OG card for one catalog entry and write a PNG to ``out_path``."""
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    name = entry.get("name", entry.get("id", ""))
    desc = entry.get("desc", "")
    cat = entry.get("cat", "")
    has_kafka = True
    has_mqtt = bool(entry.get("mqtt"))
    has_amqp = bool(entry.get("amqp"))
    has_fab = bool(entry.get("notebook")) or bool(entry.get("kql"))

    region = region_override or _region_from_desc(desc)
    scope = _scope_from_desc(desc)

    accent = CATEGORY_ACCENT.get(cat, (60, 80, 110))

    img = Image.new("RGB", (CARD_W, CARD_H), BG_DARK)
    _gradient_band(img, accent)
    draw = ImageDraw.Draw(img, "RGBA")

    # ── Top row: flag + category/region (left) | transport pills (right) ────
    top_y = PAD_Y
    cursor_x = PAD_X

    # Flag (left edge).
    flag_path = _ensure_flag(flag_cc, flag_cache_dir) if flag_cc else None
    if flag_path and flag_path.exists():
        try:
            flag = Image.open(flag_path).convert("RGBA")
            target_h = 56
            ratio = target_h / flag.height
            target_w = max(1, int(flag.width * ratio))
            flag = flag.resize((target_w, target_h), Image.LANCZOS)
            # Soft rounded border around the flag.
            border = Image.new("RGBA", (target_w + 4, target_h + 4), (0, 0, 0, 0))
            bdraw = ImageDraw.Draw(border)
            bdraw.rounded_rectangle(
                [0, 0, target_w + 3, target_h + 3], radius=8,
                fill=(0, 0, 0, 0), outline=(255, 255, 255, 90), width=2,
            )
            img.paste(flag, (cursor_x + 2, top_y + 2), flag)
            img.paste(border, (cursor_x, top_y), border)
            cursor_x += target_w + 24
        except Exception as e:  # pragma: no cover
            print(f"  warn: flag render failed: {e}", file=sys.stderr)

    # Category + region (centered vertically against the flag).
    cat_fnt = font(FONT_SEMIBOLD, 28)
    cat_label = (cat or "Real-Time Source").upper()
    if region and region.lower() not in (cat or "").lower():
        cat_label += f"   ·   {region}"
    _draw_text(draw, (cursor_x, top_y + 12), cat_label, cat_fnt, TEXT_SECONDARY)

    # Transport pills right-aligned at the top.
    pills_y = top_y
    pill_x = CARD_W - PAD_X
    # Render right-to-left so the pill order is K M A on screen.
    pills: List[Tuple[str, Tuple[int, int, int], bool]] = [
        ("K", C_KAFKA, has_kafka),
        ("M", C_MQTT,  has_mqtt),
        ("A", C_AMQP,  has_amqp),
    ]
    # Compute total width first.
    fnt = font(FONT_BOLD, 30)
    widths = []
    for label, _, _ in pills:
        tw = int(draw.textlength(label, font=fnt))
        widths.append(tw + 18 * 2)
    total_w = sum(widths) + (len(pills) - 1) * 12
    px = CARD_W - PAD_X - total_w
    for (label, bg, on), w in zip(pills, widths):
        _pill(draw, px, pills_y, label, bg, on)
        px += w + 12

    # ── Title ───────────────────────────────────────────────────────────────
    title_top = top_y + 96
    # Auto-shrink the title to fit one line when possible.
    title_size = 88
    title_fnt = font(FONT_BOLD, title_size)
    while title_size > 56 and draw.textlength(name, font=title_fnt) > CARD_W - 2 * PAD_X:
        title_size -= 6
        title_fnt = font(FONT_BOLD, title_size)
    title_lines = _wrap(name, title_fnt, CARD_W - 2 * PAD_X, draw)[:2]
    y = title_top
    for line in title_lines:
        _draw_text(draw, (PAD_X, y), line, title_fnt, TEXT_PRIMARY)
        y += int(title_size * 1.05)

    # ── Scope / description (2 lines max) ───────────────────────────────────
    if scope:
        desc_fnt = font(FONT_REGULAR, 36)
        desc_lines = _wrap(scope, desc_fnt, CARD_W - 2 * PAD_X, draw)[:2]
        y += 18
        for line in desc_lines:
            _draw_text(draw, (PAD_X, y), line, desc_fnt, TEXT_SECONDARY)
            y += 48

    # ── Footer rule + attribution ───────────────────────────────────────────
    rule_y = CARD_H - PAD_Y - 64
    draw.line([(PAD_X, rule_y), (CARD_W - PAD_X, rule_y)], fill=RULE, width=2)

    foot_fnt = font(FONT_SEMIBOLD, 26)
    foot_left = "real-time-sources"
    _draw_text(draw, (PAD_X, rule_y + 22), foot_left, foot_fnt, TEXT_PRIMARY)

    foot_meta_parts: List[str] = []
    foot_meta_parts.append("Kafka" + ("" if not has_kafka else ""))
    if has_mqtt:
        foot_meta_parts.append("MQTT 5.0")
    if has_amqp:
        foot_meta_parts.append("AMQP 1.0")
    if has_fab:
        foot_meta_parts.append("Fabric")
    foot_meta = "  ·  ".join(foot_meta_parts)

    meta_fnt = font(FONT_REGULAR, 24)
    meta_w = draw.textlength(foot_meta, font=meta_fnt)
    _draw_text(draw, (CARD_W - PAD_X - int(meta_w), rule_y + 24),
               foot_meta, meta_fnt, TEXT_MUTED)

    img.save(out_path, format="PNG", optimize=True)
    return out_path


# ── CLI ──────────────────────────────────────────────────────────────────────
def _main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--catalog", default="catalog.json")
    p.add_argument("--out-dir", required=True, help="Output directory (one PNG per source)")
    p.add_argument("--flag-cache", default=".cache/flags")
    p.add_argument("--only", action="append", default=[],
                   help="Render only these source IDs (repeatable). Default: all.")
    p.add_argument("--flag-map", default=None,
                   help="Optional JSON file mapping source-id -> ISO alpha-2 cc.")
    args = p.parse_args()

    catalog = json.loads(Path(args.catalog).read_text(encoding="utf-8"))
    out_dir = Path(args.out_dir)
    flag_cache = Path(args.flag_cache)

    flag_map: Dict[str, str] = {}
    if args.flag_map and Path(args.flag_map).exists():
        flag_map = json.loads(Path(args.flag_map).read_text(encoding="utf-8"))

    filt = set(args.only)
    rendered = 0
    for entry in catalog:
        sid = entry["id"]
        if filt and sid not in filt:
            continue
        cc = flag_map.get(sid, "")
        out = out_dir / sid / "og.png"
        render_card(entry, out, flag_cache_dir=flag_cache, flag_cc=cc)
        rendered += 1
        print(f"  [ok] {sid:38} -> {out}")
    print(f"Rendered {rendered} card(s).")
    return 0


if __name__ == "__main__":
    sys.exit(_main())
