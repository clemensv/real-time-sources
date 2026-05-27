#!/usr/bin/env python3
"""Inject (or refresh) a per-source hero header block in every source's
README.md and CONTAINER.md, bounded by <!-- source-hero:begin/end --> sentinels.

The hero block mirrors the pegelonline gold standard:
  - large flag + country
  - source title + name
  - tagline (upstream, API docs, cadence, scope)
  - transport pills (Kafka / MQTT / AMQP)
  - destination chips (Azure templates, Fabric, Docker images)
  - build badge link
  - one-line summary
  - shortcut buttons (Deploy / Notebook / docker pull / EVENTS / KQL / Fabric Map)

Run from repo root:
  python tools/docs/generate_source_heroes.py
"""
from __future__ import annotations
import json
import re
from pathlib import Path

# Reuse maps from the catalog generator
from generate_root_catalog import (
    FLAG, FLAG_BY_ID, parse_xreg, derive_region, derive_scope,
    ROOT, CATALOG, UPSTREAM, REPO, PORTAL,
)

BEGIN = "<!-- source-hero:begin -->"
END = "<!-- source-hero:end -->"


def big_flag(cc: str, region: str) -> str:
    cc = (cc or "un").lower()
    return (
        f'<img src="https://flagcdn.com/64x48/{cc}.png" '
        f'alt="{region or cc.upper()}" width="64" height="48">'
    )


def transport_pills_big(transports: set) -> str:
    """Three named pills (Kafka/MQTT/AMQP) — full word, not letter."""
    out = []
    for name, color in (("Kafka", "231f20"), ("MQTT", "660066"), ("AMQP", "1a4a78")):
        if name in transports:
            out.append(
                f'<img align="middle" alt="{name}" '
                f'src="https://img.shields.io/badge/-{name}-{color}?style=flat-square">'
            )
    return " ".join(out)


def dest_chips(entry: dict) -> str:
    """Big destination chips: Azure templates count, Fabric (Notebook+ACI / ACI), Docker images."""
    sid = entry["id"]
    src_dir = ROOT / sid
    az_templates = len(list(src_dir.glob("azure-template*.json"))) if src_dir.exists() else 0
    dockerfiles = len(list(src_dir.glob("Dockerfile*"))) if src_dir.exists() else 0
    has_notebook = entry.get("notebook", False)
    fabric_label = "Notebook_%2B_ACI" if has_notebook else "ACI"
    chips = []
    if az_templates:
        chips.append(
            f'<img align="middle" '
            f'src="https://img.shields.io/badge/Azure-{az_templates}_templates-0078d4?style=flat-square">'
        )
    chips.append(
        f'<img align="middle" '
        f'src="https://img.shields.io/badge/Fabric-{fabric_label}-117865?style=flat-square">'
    )
    if dockerfiles:
        chips.append(
            f'<img align="middle" '
            f'src="https://img.shields.io/badge/Docker-{dockerfiles}_image{"s" if dockerfiles > 1 else ""}-2496ed?style=flat-square">'
        )
    return " ".join(chips)


def shortcut_buttons(entry: dict, upstream: dict) -> str:
    sid = entry["id"]
    src_dir = ROOT / sid
    parts = [
        f'[🚀 **Deploy to Azure**]({PORTAL}#{sid})',
    ]
    if entry.get("notebook"):
        parts.append(f'[📓 **Fabric Notebook**]({PORTAL}#{sid}/fabric-notebook)')
    parts.append('[🐳 **docker pull**](CONTAINER.md)')
    parts.append('[📑 **Event schemas**](EVENTS.md)')
    if (src_dir / "kql").exists():
        kql_files = list((src_dir / "kql").glob("*.kql"))
        if kql_files:
            parts.append(f'[🗄️ **KQL schema**](kql/{kql_files[0].name})')
    if (src_dir / "fabric" / "README.md").exists():
        parts.append('[🗺️ **Fabric Map**](fabric/README.md)')
    up_entry = upstream.get(sid) or {}
    if up_entry.get("homepage"):
        parts.append(f'[↗ **Upstream**]({up_entry["homepage"]})')
    return " &nbsp;·&nbsp;\n".join(parts)


def tagline(entry: dict, upstream: dict, xreg_info: dict) -> str:
    sid = entry["id"]
    desc = entry.get("desc", "")
    scope = derive_scope(desc)
    bits = []
    if scope:
        bits.append(scope)
    transports = " · ".join(
        t for t in ("Kafka", "MQTT", "AMQP") if t in xreg_info.get("transports", set())
    )
    if transports:
        bits.append(transports)
    up_entry = upstream.get(sid) or {}
    if up_entry.get("homepage"):
        bits.append(f'<a href="{up_entry["homepage"]}">upstream</a>')
    if up_entry.get("api_docs"):
        bits.append(f'<a href="{up_entry["api_docs"]}">API docs</a>')
    return " · ".join(bits)


def render_hero(entry: dict, upstream: dict, xreg_info: dict) -> str:
    sid = entry["id"]
    name = entry["name"]
    desc = entry.get("desc", "")
    cc, region = derive_region(desc, sid)
    flag_html = big_flag(cc, region)
    region_label = region or "Worldwide"

    transports_pill = transport_pills_big(xreg_info.get("transports", {"Kafka"}))
    chips = dest_chips(entry)
    buttons = shortcut_buttons(entry, upstream)
    tline = tagline(entry, upstream, xreg_info)

    summary = entry.get("desc", name)

    build_badge = (
        f'<a href="https://github.com/{REPO}/actions/workflows/build_containers.yml">'
        f'<img align="middle" alt="build" '
        f'src="https://github.com/{REPO}/actions/workflows/build_containers.yml/badge.svg"></a>'
    )

    return (
        f'{BEGIN}\n'
        f'<table width="100%"><tr>\n'
        f'<td width="80" valign="middle" align="center">\n'
        f'{flag_html}<br>\n'
        f'<sub><b>{region_label}</b></sub>\n'
        f'</td>\n'
        f'<td valign="middle">\n\n'
        f'# {name}\n\n'
        f'<sub>{tline}</sub>\n\n'
        f'{transports_pill}\n&nbsp;\n{chips}\n&nbsp;\n{build_badge}\n\n'
        f'> {summary}\n\n'
        f'{buttons}\n\n'
        f'</td></tr></table>\n'
        f'{END}\n'
    )


def upsert_hero(path: Path, hero_block: str) -> tuple[bool, str]:
    """Inject or replace hero block in the given markdown file.

    If sentinels already exist, replace between them.
    Otherwise insert at the top (before the first heading or as the first lines).
    Returns (changed, action).
    """
    if not path.exists():
        return (False, "skip (file missing)")
    text = path.read_text(encoding="utf-8")
    if BEGIN in text and END in text:
        pat = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n?", re.DOTALL)
        new = pat.sub(hero_block, text, count=1)
        action = "replaced"
    else:
        # Strip a leading shields-badge line + the first H1 if present, to avoid duplicate titles
        stripped = text
        # Drop leading "[![Build...]( ... )]( ... )" badge line + blank
        stripped = re.sub(r"^\[!\[[^\]]*\]\([^)]*\)\]\([^)]*\)\s*\n+", "", stripped, count=1)
        # Drop leading top-level "# Title" line + blank that immediately follows
        stripped = re.sub(r"^# [^\n]*\n+", "", stripped, count=1)
        new = hero_block + "\n" + stripped
        action = "inserted"
    if new == text:
        return (False, "no-op")
    path.write_text(new, encoding="utf-8")
    return (True, action)


def main() -> int:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    upstream = {}
    if UPSTREAM.exists():
        try:
            upstream = json.loads(UPSTREAM.read_text(encoding="utf-8"))
        except Exception:
            pass
    total = 0
    actions = {"replaced": 0, "inserted": 0, "no-op": 0, "skip (file missing)": 0}
    for entry in catalog:
        sid = entry["id"]
        src_dir = ROOT / sid
        if not src_dir.exists():
            continue
        xreg_info = parse_xreg(src_dir)
        hero = render_hero(entry, upstream, xreg_info)
        for fname in ("README.md", "CONTAINER.md"):
            changed, action = upsert_hero(src_dir / fname, hero)
            actions[action] = actions.get(action, 0) + 1
            if changed:
                total += 1
    print(f"Updated {total} files. Breakdown:")
    for a, n in actions.items():
        print(f"  {a}: {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
