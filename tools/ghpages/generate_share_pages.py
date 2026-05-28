"""Generate per-source share-landing pages and OG cards for the gh-pages portal.

For every entry in ``catalog.json`` we emit, under the configured output dir::

    share/<sid>/index.html   — crawler-friendly HTML with full OG/Twitter meta
                                + JS + <meta refresh> hop to /#<sid>
    share/<sid>/og.png       — 1200x630 pre-rendered Open Graph image

This is the static infrastructure that backs the in-app **Share** button.
Crawlers (X, LinkedIn, Slack, Discord, FB, Mastodon, Bluesky, Teams) do not
execute JavaScript, so SPA-only OG tags don't work — these static shells are
required for rich link previews.

Usage::

    python tools/ghpages/generate_share_pages.py \
        --catalog catalog.json \
        --out-dir ghpages/share \
        --base-url https://clemensv.github.io/real-time-sources
"""

from __future__ import annotations

import argparse
import json
import sys
from html import escape as he
from pathlib import Path
from typing import Any, Dict, Optional

# Make the sibling renderer importable when run as a script.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_og_card import render_card  # noqa: E402

# Re-use the flag-resolution tables from the root catalog generator so all
# surfaces (root README, ghpages, share cards) agree on which flag to use.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "docs"))
from generate_root_catalog import FLAG, FLAG_BY_ID  # noqa: E402


TEMPLATE_PATH = Path(__file__).resolve().parent / "share_template.html"


def _resolve_flag_cc(entry: Dict[str, Any]) -> str:
    """Determine the ISO alpha-2 country code for a catalog entry.

    Order: per-id override → first token of ``desc`` matched against the
    ``FLAG`` table → empty string (renderer will simply skip the flag image).
    """
    sid = entry["id"]
    if sid in FLAG_BY_ID:
        return FLAG_BY_ID[sid]
    desc = entry.get("desc", "")
    # Region prefix is everything before the em/en-dash separator.
    for sep in ("—", "–", " - "):
        if sep in desc:
            head = desc.split(sep, 1)[0].strip()
            if head in FLAG:
                return FLAG[head]
            break
    return ""


def _short_desc(entry: Dict[str, Any]) -> str:
    """Build the OG/Twitter description string from the catalog entry."""
    name = entry.get("name", entry["id"])
    cat = entry.get("cat", "Real-time source")
    desc = entry.get("desc", "").strip()
    if desc:
        return f"{cat} — {desc}"
    return f"{cat} — real-time {name} data on Kafka, MQTT, AMQP and Microsoft Fabric."


def _json_ld(entry: Dict[str, Any], spa_url: str, og_url: str) -> str:
    """Emit a JSON-LD Dataset descriptor for richer SEO."""
    keywords = ["Apache Kafka", "real-time data"]
    if entry.get("mqtt"):
        keywords.append("MQTT 5.0")
    if entry.get("amqp"):
        keywords.append("AMQP 1.0")
    if entry.get("notebook") or entry.get("kql"):
        keywords.append("Microsoft Fabric")
    keywords.append(entry.get("cat", "real-time"))

    payload: Dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": entry.get("name", entry["id"]),
        "description": _short_desc(entry),
        "url": spa_url,
        "image": og_url,
        "isAccessibleForFree": True,
        "license": "https://www.apache.org/licenses/LICENSE-2.0",
        "keywords": ", ".join(keywords),
        "creator": {
            "@type": "Organization",
            "name": "real-time-sources",
            "url": "https://github.com/clemensv/real-time-sources",
        },
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def render_share_page(
    entry: Dict[str, Any],
    out_dir: Path,
    *,
    base_url: str,
    flag_cache_dir: Path,
    template: str,
    write_image: bool = True,
) -> None:
    """Write ``share/<sid>/index.html`` (and og.png) for one catalog entry."""
    sid = entry["id"]
    share_dir = out_dir / sid
    share_dir.mkdir(parents=True, exist_ok=True)

    if write_image:
        render_card(
            entry,
            share_dir / "og.png",
            flag_cache_dir=flag_cache_dir,
            flag_cc=_resolve_flag_cc(entry),
        )

    title = entry.get("name", sid)
    description = _short_desc(entry)
    spa_url = f"{base_url}/#{sid}"
    share_url = f"{base_url}/share/{sid}/"
    og_image_url = f"{share_url}og.png"

    html = (
        template
        .replace("{{TITLE}}", he(title))
        .replace("{{DESCRIPTION}}", he(description))
        .replace("{{SPA_URL}}", he(spa_url, quote=True))
        .replace("{{SPA_URL_JSON}}", json.dumps(spa_url))
        .replace("{{SHARE_URL}}", he(share_url, quote=True))
        .replace("{{OG_IMAGE_URL}}", he(og_image_url, quote=True))
        .replace("{{SPA_BASE}}", he(base_url, quote=True))
        .replace("{{JSON_LD}}", _json_ld(entry, spa_url, og_image_url))
    )
    (share_dir / "index.html").write_text(html, encoding="utf-8")


def _index_listing(catalog, base_url: str) -> str:
    """Emit a simple human-readable index at share/index.html (also handy for
    sanity checks). Crawlers don't need it — it's not the canonical URL."""
    rows = []
    for e in sorted(catalog, key=lambda x: x["id"]):
        sid = e["id"]
        rows.append(
            f'<li><a href="{he(sid, quote=True)}/">{he(e.get("name", sid))}</a> '
            f'— <span style="color:#8590a0">{he(e.get("desc",""))}</span></li>'
        )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Share pages — real-time-sources</title>
<meta name="robots" content="noindex">
<style>
  body {{ font: 15px/1.5 system-ui, sans-serif; max-width: 900px; margin: 40px auto; padding: 0 16px; color: #e5eaf0; background: #0f141c; }}
  h1 {{ font-size: 22px; }}
  a {{ color: #4aa3df; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  li {{ margin: 4px 0; }}
  .head {{ color: #afb9c8; margin-bottom: 24px; }}
</style></head>
<body>
<h1>Per-source share landing pages</h1>
<p class="head">{len(catalog)} sources. Each URL is the canonical share target for
  cards on X, LinkedIn, Slack, Discord, FB, Mastodon, Bluesky and Teams. Humans
  are redirected to <code>{he(base_url, quote=True)}/#&lt;source-id&gt;</code>.</p>
<ul>
{chr(10).join(rows)}
</ul>
</body></html>
"""


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--catalog", default="catalog.json")
    p.add_argument("--out-dir", required=True,
                   help="Output dir for per-source share pages, e.g. ghpages/share")
    p.add_argument("--base-url", default="https://clemensv.github.io/real-time-sources",
                   help="Site origin + base path (no trailing slash)")
    p.add_argument("--flag-cache", default=".cache/flags",
                   help="Where to cache flag PNGs downloaded from flagcdn.com")
    p.add_argument("--only", action="append", default=[],
                   help="Render only these source IDs (repeatable). Default: all.")
    p.add_argument("--skip-images", action="store_true",
                   help="Skip PNG regeneration (HTML only). Useful for fast iteration.")
    args = p.parse_args()

    catalog = json.loads(Path(args.catalog).read_text(encoding="utf-8"))
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    out_dir = Path(args.out_dir)
    flag_cache = Path(args.flag_cache)
    filt = set(args.only)

    n = 0
    for entry in catalog:
        if filt and entry["id"] not in filt:
            continue
        render_share_page(
            entry, out_dir,
            base_url=args.base_url.rstrip("/"),
            flag_cache_dir=flag_cache,
            template=template,
            write_image=not args.skip_images,
        )
        n += 1
        print(f"  [ok] {entry['id']}")

    # Write a simple index page (only when emitting the full set).
    if not filt:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(
            _index_listing(catalog, args.base_url.rstrip("/")), encoding="utf-8",
        )

    print(f"\nGenerated {n} share page(s) under {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
