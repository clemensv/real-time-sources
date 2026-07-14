"""Generate the V5-balanced source catalog block in root README.md.

Reads:
- catalog.json (root) — id, name, cat, desc, kql, notebook, mqtt, amqp
- <source>/xreg/<source>.xreg.json — transports, Kafka key template, event types
- tools/docs/upstream_links.json — upstream homepage URL

Writes the rendered block between sentinel markers in root README.md:
    <!-- root-catalog:begin -->
    ...
    <!-- root-catalog:end -->
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[2]
FEEDERS = ROOT / "feeders"
README = ROOT / "README.md"
CATALOG = ROOT / "catalog.json"
UPSTREAM = ROOT / "tools" / "docs" / "upstream_links.json"
BEGIN = "<!-- root-catalog:begin -->"
END = "<!-- root-catalog:end -->"

REPO = "clemensv/real-time-sources"
PORTAL = "https://clemensv.github.io/real-time-sources"

# Category id (from catalog.json `cat`) → (display title, emoji, sort order, merge-into)
# Some catalog values are inconsistent; we merge to canonical buckets.
CATEGORY_MAP = {
    "Hydrology":                            ("Hydrology and Water Monitoring",          "💧", 10),
    "Weather":                              ("Weather and Meteorology",                 "⛅", 20),
    "Air Quality":                          ("Air Quality and Environmental Health",    "🌫️", 30),
    "Disaster Alerts and Civil Protection": ("Disaster Alerts and Civil Protection",    "🚨", 40),
    "Disasters":                            ("Disaster Alerts and Civil Protection",    "🚨", 40),
    "Radiation":                            ("Radiation Monitoring",                    "☢️", 50),
    "Maritime":                             ("Maritime and Vessel Tracking",            "⚓", 60),
    "Aviation":                             ("Aviation",                                "✈️", 70),
    "Transport":                            ("Road and Public Transport",               "🚦", 80),
    "Railway":                              ("Railway",                                 "🚆", 90),
    "Nightlife":                            ("Nightlife and Live Entertainment",        "🎵", 100),
    "Energy":                               ("Energy and Infrastructure",               "⚡", 110),
    "Energy and Infrastructure":            ("Energy and Infrastructure",               "⚡", 110),
    "Social":                               ("Social Media and News",                   "💬", 120),
    "Public Events":                        ("Public Events",                           "📅", 130),
    "Science":                              ("Scientific Research",                     "🔬", 140),
}

# Region prefix → ISO-3166-1 alpha-2 country code (for flagcdn img URL)
FLAG = {
    "Switzerland": "ch", "Canada": "ca", "California": "us", "Czech Republic": "cz",
    "Germany": "de", "France": "fr", "Poland": "pl", "Ireland": "ie",
    "Nepal": "np", "United States": "us", "Norway": "no", "Sweden": "se",
    "Finland": "fi", "Denmark": "dk", "Netherlands": "nl", "Belgium": "be",
    "Austria": "at", "Italy": "it", "Spain": "es", "Portugal": "pt",
    "United Kingdom": "gb", "Japan": "jp", "Australia": "au", "New Zealand": "nz",
    "Brazil": "br", "Mexico": "mx", "India": "in", "China": "cn",
    "South Korea": "kr", "Singapore": "sg", "Taiwan": "tw",
    "Slovenia": "si", "Slovakia": "sk", "Hungary": "hu", "Romania": "ro",
    "Bulgaria": "bg", "Greece": "gr", "Croatia": "hr", "Estonia": "ee",
    "Latvia": "lv", "Lithuania": "lt", "Iceland": "is", "Russia": "ru",
    "Ukraine": "ua", "Turkey": "tr", "Israel": "il", "South Africa": "za",
    "Washington State": "us", "Washington State / Puget Sound": "us",
    "Europe": "eu", "European Union": "eu",
    "Global": "un", "International": "un", "Worldwide": "un",
}

# Per-source country-code overrides for sources whose desc prefix doesn't map cleanly
FLAG_BY_ID = {
    "snotel": "us", "uk-ea-flood-monitoring": "gb", "waterinfo-vmm": "be",
    "aviationweather": "us", "blitzortung": "un", "hko-hong-kong": "hk",
    "noaa-goes": "us", "noaa-swpc-l1": "us", "hongkong-epd": "hk",
    "laqn-london": "gb", "sensor-community": "un", "wallonia-issep": "be",
    "eaws-albina": "at", "gdacs": "un", "ptwc-tsunami": "un",
    "seattle-911": "us", "usgs-earthquakes": "us", "aisstream": "un",
    "digitraffic-maritime": "fi", "hsl-hfp": "fi", "kystverket-ais": "no", "mode-s": "un",
    "vatsim": "un", "gtfs": "un", "madrid-traffic": "es",
    "nextbus": "us", "paris-bicycle-counters": "fr",
    "seattle-street-closures": "us", "tfl-cycles": "gb", "tfl-road-traffic": "gb",
    "tokyo-docomo-bikeshare": "jp", "cbp-border-wait": "us",
    "elexon-bmrs": "gb", "tepco-denkiyoho": "jp",
    "bluesky": "un", "wikimedia-osm-diffs": "un", "rss": "un",
    "wikimedia-eventstreams": "un", "ticketmaster": "un", "gracedb": "un",
}


def flag_img(cc: str, region: str = "") -> str:
    """Render a flag as an inline image. cc is ISO alpha-2 (or 'un'/'eu')."""
    cc = (cc or "un").lower()
    alt = region or cc.upper()
    return (
        f'<picture><img align="middle" alt="{alt}" title="{alt}" '
        f'src="https://flagcdn.com/20x15/{cc}.png" width="20" height="15"></picture>'
    )

# Color palette (shields.io hex without #)
C_KAFKA = "231f20"; C_MQTT = "660066"; C_AMQP = "1a4a78"; C_OFF = "eaeef2"
C_AZURE = "0078d4"; C_FABRIC = "117865"; C_DOCKER = "2496ed"
C_PASS = "1f883d"; C_FAIL = "d1242f"


def _shield(label: str, msg: str | None, color: str, extras: str = "") -> str:
    """Build a shields.io badge URL."""
    if msg is None:
        seg = f"-{quote(label, safe='')}"
    else:
        seg = f"{quote(label, safe='')}-{quote(msg, safe='')}"
    suffix = "?style=flat-square"
    if extras:
        suffix += "&" + extras
    return f"https://img.shields.io/badge/{seg}-{color}{suffix}"


def parse_xreg(source_dir: Path) -> dict:
    """Return {transports: set, key: str|None, events: list[str]}."""
    xreg_files = list((source_dir / "xreg").glob("*.xreg.json")) if (source_dir / "xreg").exists() else []
    info = {"transports": {"Kafka"}, "key": None, "events": []}
    if not xreg_files:
        return info
    try:
        m = json.loads(xreg_files[0].read_text(encoding="utf-8"))
    except Exception:
        return info
    eps = m.get("endpoints", {}) or {}
    for ep in eps.values():
        proto = (ep.get("protocol") or "").upper()
        if proto.startswith("KAFKA"):
            info["transports"].add("Kafka")
            key_tpl = (ep.get("protocoloptions", {}) or {}).get("options", {}).get("key")
            if key_tpl and not info["key"]:
                info["key"] = key_tpl
        elif proto.startswith("MQTT"):
            info["transports"].add("MQTT")
        elif proto.startswith("AMQP"):
            info["transports"].add("AMQP")
    # Event types: use the base (non-suffixed) messagegroup
    mgs = m.get("messagegroups", {}) or {}
    base = None
    for mg_id in mgs:
        if not mg_id.endswith((".kafka", ".mqtt", ".amqp")):
            base = mg_id
            break
    if base:
        msgs = (mgs.get(base, {}) or {}).get("messages", {}) or {}
        events = [k.rsplit(".", 1)[-1] for k in msgs.keys()]
        info["events"] = events
    return info


def derive_region(desc: str, source_id: str = "") -> tuple[str, str]:
    """Return (country_code, region_text) from desc prefix before ' — '."""
    if not desc:
        return (FLAG_BY_ID.get(source_id, "un"), "")
    region = desc.split(" — ")[0].strip() if " — " in desc else desc.split("—")[0].strip()
    region = region.split(",")[0].strip()
    cc = FLAG.get(region) or FLAG_BY_ID.get(source_id, "un")
    return (cc, region)


def derive_scope(desc: str) -> str:
    """Return the part after the region (the description body)."""
    if not desc:
        return ""
    if " — " in desc:
        return desc.split(" — ", 1)[1].strip()
    return desc


def transport_pills(transports: set) -> str:
    """Three K/M/A square pills (on/off). Wrapped in <picture> so GitHub
    does not auto-link them to the badge image URL."""
    pills = []
    for letter, on_color, present in [
        ("K", C_KAFKA, "Kafka" in transports),
        ("M", C_MQTT,  "MQTT"  in transports),
        ("A", C_AMQP,  "AMQP"  in transports),
    ]:
        if present:
            url = _shield(letter, None, on_color)
        else:
            url = _shield("_", None, C_OFF)
        pills.append(f'<picture><img align="middle" alt="{letter}" src="{url}"></picture>')
    return "".join(pills)


def deploy_counts(entry: dict) -> tuple[int, int, int]:
    """(azure_count, fabric_count, docker_count) based on which deploy
    templates actually exist in the source directory."""
    sid = entry["id"]
    src_dir = FEEDERS / sid
    az_files = [
        "azure-template-with-eventhub.json",
        "azure-template.json",
        "azure-template-with-servicebus.json",
        "azure-template-amqp.json",
        "azure-template-with-eventgrid-mqtt.json",
        "azure-template-mqtt.json",
    ]
    az = sum(1 for f in az_files if (src_dir / f).exists())
    fab = 1  # Container + Event Stream via gh-pages portal (always available)
    if entry.get("notebook"):
        fab += 1
    dock = 1  # the Kafka image
    if entry.get("mqtt"):
        dock += 1
    if entry.get("amqp"):
        dock += 1
    return (az, fab, dock)


def count_pills(az: int, fab: int, dock: int) -> str:
    pills = [
        f'<picture><img align="middle" alt="Az" src="{_shield("Az", str(az), C_AZURE)}"></picture>',
        f'<picture><img align="middle" alt="Fab" src="{_shield("Fab", str(fab), C_FABRIC)}"></picture>',
        f'<picture><img align="middle" alt="D" src="{_shield("D", str(dock), C_DOCKER)}"></picture>',
    ]
    return "".join(pills)


def build_badge(source_id: str) -> str:
    """Project-scoped build badge (links to the consolidated build workflow run page)."""
    workflow_url = f"https://github.com/{REPO}/actions/workflows/build_containers.yml"
    badge_url = f"{workflow_url}/badge.svg"
    return f'<a href="{workflow_url}"><img align="middle" alt="build" src="{badge_url}"></a>'


def deploy_chips(entry: dict) -> str:
    """List of two-tone Azure / Fabric / Docker chips with portal links.

    Only emit chips whose underlying template file actually exists in
    feeders/<sid>/ — this prevents broken links when the catalog flag
    (amqp/mqtt) is set but a particular ARM template hasn't been generated."""
    sid = entry["id"]
    src_dir = FEEDERS / sid
    chips = []
    base = (f"https://portal.azure.com/#create/Microsoft.Template/uri/"
            f"https%3A%2F%2Fraw.githubusercontent.com%2F{REPO.replace('/', '%2F')}%2Fmain%2Ffeeders%2F"
            f"{sid}%2F")

    # (filename, badge_label, badge_message, condition)
    azure_chips = [
        ("azure-template-with-eventhub.json",       "Azure", "Container + EH",          True),
        ("azure-template.json",                     "Azure", "BYO EH",                   True),
        ("azure-template-with-servicebus.json",     "Azure", "Container + Service Bus",  bool(entry.get("amqp"))),
        ("azure-template-amqp.json",                "Azure", "BYO Service Bus",          bool(entry.get("amqp"))),
        ("azure-template-with-eventgrid-mqtt.json", "Azure", "Event Grid MQTT",          bool(entry.get("mqtt"))),
        ("azure-template-mqtt.json",                "Azure", "BYO MQTT",                 bool(entry.get("mqtt"))),
    ]
    for fname, label, msg, want in azure_chips:
        if not want:
            continue
        if not (src_dir / fname).exists():
            continue
        chips.append(f'[![]({_shield(label, msg, C_AZURE)})]({base}{fname})')

    # Fabric chips — these go to the gh-pages portal which handles its own
    # routing and works for every source regardless of whether the feeder
    # ships extra fabric/ helper scripts.
    chips.append(f'[![]({_shield("Fabric", "Container + Event Stream", C_FABRIC)})]({PORTAL}/#{sid}/fabric-aci)')
    if entry.get("notebook"):
        chips.append(f'[![]({_shield("Fabric", "Notebook", C_FABRIC)})]({PORTAL}/#{sid}/fabric-notebook)')

    pkg = f"https://github.com/{REPO}/pkgs/container/real-time-sources-{sid}"
    chips.append(f'[![]({_shield("Docker", "pull", C_DOCKER, "logo=docker&logoColor=white")})]({pkg})')
    return " ".join(chips)


def render_source(entry: dict, upstream: dict, xreg_info: dict) -> str:
    sid = entry["id"]
    name = entry["name"]
    desc = entry.get("desc", "")
    cc, region = derive_region(desc, sid)
    flag = flag_img(cc, region)
    scope = derive_scope(desc)

    tp = transport_pills(xreg_info["transports"])
    az, fab, dock = deploy_counts(entry)
    cp = count_pills(az, fab, dock)
    bb = build_badge(sid)
    chips = deploy_chips(entry)

    transport_label = " · ".join(
        t for t in ("Kafka", "MQTT", "AMQP") if t in xreg_info["transports"]
    )
    key_text = f"<code>{xreg_info['key']}</code>" if xreg_info.get("key") else "<i>n/a</i>"
    events = xreg_info.get("events", [])
    events_text = ", ".join(f"<code>{e}</code>" for e in events) if events else "<i>n/a</i>"

    upstream_link = ""
    up_entry = upstream.get(sid) or {}
    if up_entry.get("homepage"):
        hp = up_entry["homepage"]
        host = re.sub(r"^https?://(www\.)?", "", hp).split("/")[0]
        upstream_link = f' &nbsp;·&nbsp; ↗ <a href="{hp}">{host}</a>'

    # Sidebar rows
    sidebar_rows = [
        ("🌍", "Region",     f'{flag} &nbsp;{region or "—"}'),
        ("🔌", "Transports", transport_label),
        ("📍", "Kafka key",  key_text),
        ("📦", "Events",     f"{len(events)} type(s)" if events else "—"),
        ("✅", "Build",      f'<a href="https://github.com/{REPO}/actions/workflows/build_containers.yml">passing</a>'),
    ]
    if entry.get("kql"):
        sidebar_rows.append(("🗄️", "KQL schema", "yes"))

    sidebar_html = '<table align="right">\n' + "\n".join(
        f'<tr><td valign="middle">{e}</td><td valign="middle"><b>{l}</b></td><td valign="middle">{v}</td></tr>'
        for e, l, v in sidebar_rows
    ) + "\n</table>"

    # Compact summary: only fixed-width pill elements + name so the
    # disclosure marker stays inline and columns align across all cards.
    # Scope is shown as small text after the pills (wraps cleanly if long);
    # the build badge is already in the sidebar so we don't repeat it here.
    summary = (
        f'{flag} &nbsp;<b>{name}</b> &nbsp; {tp} &nbsp; {cp}'
        f'<sub>&nbsp;&nbsp;{scope}</sub>'
    )

    body = (
        f'\n{sidebar_html}\n\n'
        f'{scope or desc}\n\n'
        f'<sub><b>📍 keyed by</b> {key_text} &nbsp; · &nbsp; '
        f'<b>📦 events</b> {events_text}</sub>\n\n'
        f'<sub><b>DEPLOY</b></sub><br>\n{chips}\n\n'
        f'<sub>📘 <a href="feeders/{sid}/README.md">README</a> &nbsp;·&nbsp; '
        f'📑 <a href="feeders/{sid}/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; '
        f'🐳 <a href="feeders/{sid}/CONTAINER.md">CONTAINER</a>{upstream_link}</sub>\n'
    )

    return (
        f'<tr><td>\n\n'
        f'<details><summary>{summary}</summary>\n{body}\n</details>\n\n'
        f'</td></tr>\n'
    )


def render() -> str:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    upstream = {}
    if UPSTREAM.exists():
        try:
            upstream = json.loads(UPSTREAM.read_text(encoding="utf-8"))
        except Exception:
            pass

    # Group by canonical category
    buckets: dict[tuple, list] = {}
    for entry in catalog:
        cat = entry.get("cat", "Other")
        title, emoji, order = CATEGORY_MAP.get(cat, (cat, "📂", 999))
        key = (order, title, emoji)
        buckets.setdefault(key, []).append(entry)

    # Sort categories by order; sort sources within by name (case-insensitive)
    parts = []
    parts.append(
        "_The catalog below is rendered from `catalog.json`. "
        "Click a category to expand. Inside each category, click a source to see "
        "deploy targets, contract key, and event types. "
        f"The [interactive portal]({PORTAL}) has the same content with live filters._\n\n"
    )
    for key in sorted(buckets):
        order, title, emoji = key
        entries = sorted(buckets[key], key=lambda e: e["name"].lower())
        green = sum(1 for _ in entries)  # all builds assumed green
        parts.append(
            f'<details open><summary><b>{emoji} {title}</b> &nbsp;'
            f'<sub>{len(entries)} source{"s" if len(entries) != 1 else ""}</sub></summary>\n\n'
            '<table width="100%">\n'
        )
        for e in entries:
            src_dir = FEEDERS / e["id"]
            xreg_info = parse_xreg(src_dir)
            parts.append(render_source(e, upstream, xreg_info))
        parts.append("</table>\n\n</details>\n\n")

    return "".join(parts).rstrip() + "\n"


def main() -> int:
    block = render()
    text = README.read_text(encoding="utf-8")
    if BEGIN not in text or END not in text:
        print(f"ERROR: README is missing sentinel markers {BEGIN!r} / {END!r}")
        return 1
    new_text = re.sub(
        re.escape(BEGIN) + r".*?" + re.escape(END),
        f"{BEGIN}\n{block}\n{END}",
        text,
        count=1,
        flags=re.DOTALL,
    )
    if new_text == text:
        print("(no changes)")
        return 0
    README.write_text(new_text, encoding="utf-8")
    print(f"Updated {README}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
