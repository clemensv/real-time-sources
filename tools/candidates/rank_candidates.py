#!/usr/bin/env python3
"""Generate the definitive ranked implementation checklist for qualifying
real-time-source candidates.

Reads every per-source note under tools/candidates/<domain>/*.md (skipping
INDEX.md and the _research-rounds/ logs), extracts the fitness score and
metadata, filters to the QUALIFIED pool, ranks them with a transparent,
reproducible key, and writes:

  tools/candidates/IMPLEMENTATION-RANKING.md   (human checklist, committed)
  tools/candidates/_implementation-ranking.tsv (machine-readable, committed)

Re-run after adding/scoring notes:  python tools/candidates/rank_candidates.py

Qualification bar (established earlier in this repo's candidate sweeps):
  * a note must carry a fitness score of N/18, and
  * score >= 10/18, and
  * not carry an explicit SKIP / defer / reject verdict.

Ranking key (descending priority), documented in the output header:
  1. effort tier  -- config quick-wins on an existing GENERALIZED feeder
     (gtfs/siri, gbfs-bikeshare, fdsn-seismology) before new builds
  2. fitness score (N/18) descending
  3. pattern-reuse leverage  -- reuses a protocol family already in the repo
  4. domain (clusters related builds so they can be batched)
  5. title (alphabetical, for a deterministic order)

Also emits a "Generalization strategy" section: which protocol families
already have a config-driven feeder (new sources = config adds) and which
candidate clusters justify generalizing one feeder instead of N bespoke
builds -- the "generalize the feeder, don't fork it" rule.
"""
from __future__ import annotations
import os
import re
import glob
import csv
import datetime

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.abspath(os.path.join(BASE, "..", ".."))
MD_OUT = os.path.join(BASE, "IMPLEMENTATION-RANKING.md")
TSV_OUT = os.path.join(BASE, "_implementation-ranking.tsv")

# ----------------------------------------------------------------------------
# Effort classification. The repo already ships GENERALIZED, config-driven
# feeders for a handful of standardized protocol families: adding a new source
# in one of those families is a CONFIG entry (append a feed URL / node to a
# list), NOT a new-feeder build. Verified by inspecting each feeder's core:
#   gtfs / siri      -> multi-agency GTFS-RT & multi-endpoint SIRI transit
#   gbfs-bikeshare   -> GBFS_FEEDS auto-discovery URL list (multi-system)
#   fdsn-seismology  -> federated FDSN datacenter/node list (multi-network)
# Keyed by the pattern-reuse family label (see REUSE_PATTERNS below). This is
# the "generalize the feeder, don't fork it" rule: when sources differ only by
# configuration, one config-driven feeder serves the whole family.
GENERALIZED_FEEDER = {
    "GTFS-RT/SIRI (transit)": ["gtfs", "siri"],
    "GBFS (micromobility)": ["gbfs-bikeshare"],
    "FDSN/QuakeML (seismology)": ["fdsn-seismology"],
}
GENERALIZED_DIRS = {d for ds in GENERALIZED_FEEDER.values() for d in ds}
GENERIC_CONFIG_CAT = {"bikeshare-gbfs"}
CONFIG_TRANSIT_HINTS = ["gtfs-rt", "gtfs", "siri", "mqtt vehicle"]


def classify_kind(cat: str, slug: str, title: str, text: str,
                  reuse_label: str) -> str:
    # A source whose protocol family already has a generalized feeder in the
    # repo is a config add, not a build.
    if reuse_label in GENERALIZED_FEEDER:
        return "config"
    if cat in GENERIC_CONFIG_CAT:
        return "config"
    t = (title + " " + slug + " " + text[:400]).lower()
    if cat in ("transit", "ferry") and any(k in t for k in CONFIG_TRANSIT_HINTS):
        return "config"
    return "new"


# ----------------------------------------------------------------------------
# pattern-reuse leverage: a new build that speaks a protocol family the repo
# already implements is cheaper than a greenfield protocol. Detect the family
# from the note text; first match wins for the label, any match sets the flag.
REUSE_PATTERNS = [
    ("FDSN/QuakeML (seismology)", re.compile(r"\bFDSN\b|QuakeML|fdsnws", re.I)),
    ("KiWIS/KISTERS (hydrology)", re.compile(r"KiWIS|KISTERS|WISKI", re.I)),
    ("GBFS (micromobility)", re.compile(r"\bGBFS\b", re.I)),
    ("GTFS-RT/SIRI (transit)", re.compile(r"\bGTFS\b|\bSIRI\b", re.I)),
    ("CAP alerts", re.compile(r"Common Alerting Protocol|\bCAP\b(?!TCHA)", re.I)),
    ("ERDDAP/THREDDS (ocean grid)", re.compile(r"ERDDAP|THREDDS", re.I)),
    ("DATEX II (road traffic)", re.compile(r"DATEX", re.I)),
    ("ArcGIS FeatureServer (poller)", re.compile(r"FeatureServer|ArcGIS", re.I)),
    ("OpenAQ (air quality)", re.compile(r"OpenAQ", re.I)),
    ("OGC SensorThings/SOS", re.compile(r"SensorThings|\bSOS\b|Sensor Observation", re.I)),
    ("GeoJSON REST (poller)", re.compile(r"GeoJSON", re.I)),
]


def reuse_leverage(text: str):
    for label, rx in REUSE_PATTERNS:
        if rx.search(text):
            return 1, label
    return 0, ""


def detect_existing_families(repo: str):
    """Map each pattern-reuse family -> sorted list of existing feeder dirs
    whose README references that protocol. Reproducible companion to the
    candidate reuse tags: used to surface generalization opportunities (many
    bespoke feeders re-implementing one standardized protocol) and bespoke
    feeders that duplicate an already-generalized feeder and should be folded
    into it as a config."""
    fam: dict[str, list[str]] = {}
    fdir = os.path.join(repo, "feeders")
    if not os.path.isdir(fdir):
        return fam
    for d in sorted(os.listdir(fdir)):
        readme = os.path.join(fdir, d, "README.md")
        if not os.path.isfile(readme):
            continue
        text = open(readme, encoding="utf-8", errors="replace").read()
        for label, rx in REUSE_PATTERNS:
            if rx.search(text):
                fam.setdefault(label, []).append(d)
    return fam


# ----------------------------------------------------------------------------
SKIP_VERDICT = re.compile(
    r"\*\*(?:Verdict|Recommendation|Decision)\*\*\s*[:\-]?\s*(.+)", re.I)

# Curated commercial/paid vendors that slip past the **SKIP** verdict text but
# are disqualified by the find-real-time-sources policy (paid commercial license
# or per-query billing). Matched against the note TITLE only (not body, to avoid
# false hits from comparison mentions) so they never surface as buildable
# generalized-feeder cluster members. Finer per-source keep/drop still happens
# during each source's upstream audit at build time.
COMMERCIAL_SKIP = re.compile(
    r"\bTomTom\b|\bHERE\s+(?:Traffic|Maps|Technologies|Location|Routing|API)\b",
    re.I)


def is_skip(text: str, title: str = "") -> bool:
    if re.search(r"\*\*SKIP\*\*", text, re.I) or "\u23ed" in text:
        return True
    if title and COMMERCIAL_SKIP.search(title):
        return True
    m = SKIP_VERDICT.search(text)
    if m and re.search(r"\bskip\b|\bdefer\b|\breject\b|\u274c", m.group(1), re.I):
        return True
    return False


FIELD_RX = {
    "region": re.compile(r"^\s*[-*]?\s*\*\*(?:Country/Region|Region|Country)\*\*\s*[:\-]\s*(.+?)\s*$", re.I | re.M),
    "protocol": re.compile(r"^\s*[-*]?\s*\*\*Protocol\*\*\s*[:\-]\s*(.+?)\s*$", re.I | re.M),
    "freshness": re.compile(r"^\s*[-*]?\s*\*\*(?:Update Frequency|Freshness|Cadence|Latency)\*\*\s*[:\-]\s*(.+?)\s*$", re.I | re.M),
    "auth": re.compile(r"^\s*[-*]?\s*\*\*Auth\*\*\s*[:\-]\s*(.+?)\s*$", re.I | re.M),
}
SCORE_ACTUAL = re.compile(r"\*\*Actual\b[^\n]*?(\d+)\s*/\s*18", re.I)
SCORE_EXPLICIT = re.compile(r"\*\*Score\*\*\s*[:\-]?\s*(\d+)\s*/\s*18", re.I)
SCORE_TOTAL = re.compile(r"\*\*Total\b[^\n]*?(\d+)\s*/\s*18", re.I)
TITLE_RX = re.compile(r"^#\s+(.+?)\s*$", re.M)


def field(rx, text, default=""):
    m = rx.search(text)
    if not m:
        return default
    val = m.group(1).strip()
    # strip stray markdown emphasis / backticks for the compact row
    val = re.sub(r"`([^`]*)`", r"\1", val)
    return val.replace("|", "/").strip()


def parse_note(path: str):
    cat = os.path.basename(os.path.dirname(path))
    slug = os.path.basename(path)[:-3]
    text = open(path, encoding="utf-8", errors="replace").read()
    mt = TITLE_RX.search(text)
    title = mt.group(1).strip() if mt else slug
    # score precedence: penalized **Actual** > **Score** > table **Total**.
    # A note MUST carry one of these STRUCTURED scores to qualify. The bare
    # "N/18" fallback is deliberately NOT used: every legitimate scored note
    # uses one of the three above, whereas a stray "N/18" only ever comes
    # from CONDITIONAL prose ("if NCM publishes an API this would be 17/18"),
    # a "TBD/provisional" note, or an inventory cross-link — none of which is
    # a verified, buildable source. Notes without a structured score are
    # treated as unscored and excluded.
    score = None
    score_src = ""
    for rx, src in ((SCORE_ACTUAL, "actual"), (SCORE_EXPLICIT, "explicit"),
                    (SCORE_TOTAL, "total")):
        m = rx.search(text)
        if m:
            score = int(m.group(1))
            score_src = src
            break
    rel = os.path.relpath(path, REPO).replace("\\", "/")
    reuse, reuse_label = reuse_leverage(text)
    return {
        "domain": cat,
        "slug": slug,
        "title": re.sub(r"\s*\u2014.*$", "", title).strip() or title,  # short title before em-dash
        "full_title": title,
        "score": score,
        "score_src": score_src,
        "kind": classify_kind(cat, slug, title, text, reuse_label),
        "skip": is_skip(text, title),
        "region": field(FIELD_RX["region"], text),
        "protocol": field(FIELD_RX["protocol"], text),
        "freshness": field(FIELD_RX["freshness"], text),
        "auth": field(FIELD_RX["auth"], text),
        "reuse": reuse,
        "reuse_label": reuse_label,
        "path": rel,
    }


def main():
    rows = []
    for path in glob.glob(os.path.join(BASE, "**", "*.md"), recursive=True):
        name = os.path.basename(path)
        if name == "INDEX.md" or "_research-rounds" in path.replace("\\", "/"):
            continue
        if name == "IMPLEMENTATION-RANKING.md":
            continue
        rows.append(parse_note(path))

    qualified = [r for r in rows
                 if r["score"] is not None and r["score"] >= 10 and not r["skip"]]

    # ranking key
    def sort_key(r):
        return (
            0 if r["kind"] == "config" else 1,   # configs first
            -r["score"],                          # higher fitness first
            -r["reuse"],                          # known-pattern reuse first
            r["domain"],                          # cluster related builds
            r["title"].lower(),
        )

    qualified.sort(key=sort_key)
    for i, r in enumerate(qualified, 1):
        r["rank"] = i

    # ---- write TSV (machine-readable) ----
    with open(TSV_OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["rank", "kind", "score", "domain", "title", "region",
                    "protocol", "freshness", "auth", "reuse_pattern",
                    "score_src", "path"])
        for r in qualified:
            w.writerow([r["rank"], r["kind"], r["score"], r["domain"],
                        r["full_title"], r["region"], r["protocol"],
                        r["freshness"], r["auth"], r["reuse_label"],
                        r["score_src"], r["path"]])

    # ---- build markdown ----
    configs = [r for r in qualified if r["kind"] == "config"]
    builds = [r for r in qualified if r["kind"] == "new"]

    def band(rs, lo, hi):
        return [r for r in rs if lo <= r["score"] <= hi]

    w1 = band(builds, 15, 18)
    w2 = band(builds, 12, 14)
    w3 = band(builds, 10, 11)

    # domain distribution among qualified
    from collections import Counter
    dom_counts = Counter(r["domain"] for r in qualified)

    # generalization analysis: which protocol families already have a
    # config-driven feeder (new sources = config adds) and which families have
    # a candidate cluster / bespoke duplication big enough to justify building
    # one generalized feeder instead of N bespoke ones.
    existing_fam = detect_existing_families(REPO)
    cand_fam = Counter(r["reuse_label"] for r in qualified if r["reuse_label"])
    GENERALIZE_MIN_CAND = 6
    GEOJSON_LABEL = "GeoJSON REST (poller)"  # a format, not a single-feeder protocol
    gen_opps = []
    for _label, _rx in REUSE_PATTERNS:
        if _label in GENERALIZED_FEEDER or _label == GEOJSON_LABEL:
            continue
        _existing = existing_fam.get(_label, [])
        _ncand = cand_fam.get(_label, 0)
        if _ncand >= GENERALIZE_MIN_CAND or len(_existing) >= 2:
            gen_opps.append((_label, _existing, _ncand))
    gen_opps.sort(key=lambda o: (-(o[2] + len(o[1])), o[0]))

    today = datetime.date.today().isoformat()

    def row_line(r):
        bits = []
        if r["region"]:
            bits.append(r["region"])
        if r["protocol"]:
            bits.append(r["protocol"])
        if r["freshness"]:
            bits.append(r["freshness"])
        meta = " · ".join(bits)
        reuse = f" · ♻ {r['reuse_label']}" if r["reuse_label"] else ""
        meta_part = f" — {meta}" if meta else ""
        return (f"- [ ] **{r['rank']}.** {r['full_title']} "
                f"`{r['score']}/18` `{r['domain']}`{meta_part}{reuse} "
                f"· [`note`]({os.path.relpath(r['path'], 'tools/candidates').replace(os.sep,'/')})")

    out = []
    A = out.append
    A("# Real-Time Sources — Definitive Implementation Ranking\n")
    A("> **Generated** by `tools/candidates/rank_candidates.py` on "
      f"{today}. Re-run after scoring or adding candidate notes; do not "
      "hand-edit (edits are overwritten). Tick a box when the feeder ships.\n")
    A("This is the single ordered backlog for building out the qualifying "
      "candidate feeders catalogued under `tools/candidates/`. Work it "
      "top-to-bottom. Within each wave, rows are in strict priority order "
      "(highest fitness score first); same-domain items naturally cluster "
      "inside a score band so related builds can be batched — use the "
      "domain table and the `♻` reuse tags to pick a batch (e.g. all FDSN "
      "seismology or all GBFS configs in one sprint).\n")

    # methodology
    A("## How this ranking is built\n")
    A("**Qualification bar** — a note qualifies only if it carries a fitness "
      "score of `N/18`, scores **≥ 10/18**, and has **no** explicit "
      "SKIP / defer / reject verdict. Web-only/PDF-only, key-gated, "
      "batch-cadence, and duplicate sources were already scored down or "
      "skip-flagged in the per-domain sweeps and are excluded here.\n")
    A("**Ranking key** (descending priority):\n")
    A("1. **Effort tier** — *config quick-wins* (just append a feed/node entry "
      "to an existing **generalized** bridge: GTFS-RT/SIRI transit "
      "(`gtfs`,`siri`), GBFS micromobility (`gbfs-bikeshare`), FDSN seismology "
      "(`fdsn-seismology`)) rank above *new-feeder builds*, because they ship "
      "in hours not days. See the **Generalization strategy** section below.\n"
      "2. **Fitness score** (`N/18`) descending — the per-note score already "
      "weighs freshness, openness, endpoint stability, payload structure, "
      "stable identifiers, volume and additivity.\n"
      "3. **Pattern reuse** (`♻`) — a new build that speaks a protocol family "
      "the repo already implements (FDSN, KiWIS, CAP, ERDDAP, DATEX II, "
      "ArcGIS, OpenAQ, SensorThings, GBFS, GTFS) is cheaper and sorts ahead "
      "of a greenfield protocol at the same score.\n"
      "4. **Domain** then **title** — clusters related work and makes the "
      "order deterministic.\n")
    A("> The fitness score is the backbone but is **not** the whole story: "
      "before pulling the next item, sanity-check *additivity* (does it open "
      "a new region/domain or merely duplicate existing coverage?) and "
      "*effort* (greenfield protocol vs. reuse). The `♻` flag and the "
      "wave/cluster layout surface both at a glance.\n")

    # dashboard
    A("## Backlog at a glance\n")
    A(f"- **Qualifying feeders:** {len(qualified)}\n"
      f"- **Quick-win configs (Wave 0):** {len(configs)}\n"
      f"- **Flagship new builds 15–18/18 (Wave 1):** {len(w1)}\n"
      f"- **Solid new builds 12–14/18 (Wave 2):** {len(w2)}\n"
      f"- **Marginal new builds 10–11/18 (Wave 3):** {len(w3)}\n"
      f"- **Pattern-reuse builds (`♻`):** {sum(1 for r in builds if r['reuse'])}\n")
    A("**Qualifying feeders by domain:**\n")
    A("| Domain | Count |  | Domain | Count |")
    A("|---|---:|---|---|---:|")
    doms = sorted(dom_counts.items(), key=lambda kv: (-kv[1], kv[0]))
    half = (len(doms) + 1) // 2
    left, right = doms[:half], doms[half:]
    for i in range(half):
        ld, lc = left[i]
        if i < len(right):
            rd, rc = right[i]
            A(f"| `{ld}` | {lc} |  | `{rd}` | {rc} |")
        else:
            A(f"| `{ld}` | {lc} |  |  |  |")
    A("")

    # generalization strategy
    A("## Generalization strategy — one config-driven feeder, not many\n")
    A("Several protocol families are standardized enough that **one** "
      "config-driven feeder serves every source in the family: you append a "
      "feed URL or node to a list instead of building a new feeder. This is "
      "the `gtfs` / `siri` / `gbfs-bikeshare` / `fdsn-seismology` model — "
      "**generalize the feeder, don't fork it**. When sources differ only by "
      "configuration, prefer extending a generalized feeder over a bespoke "
      "build.\n")
    A("**Already generalized — new sources in these families are Wave-0 "
      "config adds, not builds:**\n")
    A("| Family | Generalized feeder | Config candidates | Existing bespoke feeders to fold in |")
    A("|---|---|---:|---|")
    for _label, _feeders in GENERALIZED_FEEDER.items():
        _ncand = cand_fam.get(_label, 0)
        _bespoke = [f for f in existing_fam.get(_label, [])
                    if f not in GENERALIZED_DIRS]
        _bes = ", ".join("`" + b + "`" for b in _bespoke) if _bespoke else "—"
        A(f"| {_label} | `{' / '.join(_feeders)}` | {_ncand} | {_bes} |")
    A("")
    if gen_opps:
        A("**Generalization opportunities — build one config-driven feeder to "
          "cover the whole cluster instead of N bespoke feeders:**\n")
        A("| Family | Qualified candidates | Existing bespoke feeders | Action |")
        A("|---|---:|---|---|")
        for _label, _existing, _ncand in gen_opps:
            _ex = ", ".join("`" + e + "`" for e in _existing
                            if e not in GENERALIZED_DIRS) or "—"
            _short = _label.split(" (")[0]
            A(f"| {_label} | {_ncand} | {_ex} | Generalize one `{_short}` feeder, then config |")
        A("")
    _geojson_n = cand_fam.get(GEOJSON_LABEL, 0)
    if _geojson_n:
        A(f"> The {_geojson_n} `GeoJSON REST` candidates are **not** one feeder "
          "— GeoJSON is a payload format, not a protocol — but they share a "
          "*poll → parse FeatureCollection → key by feature id* skeleton; "
          "reuse a common poller template rather than copying boilerplate.\n")

    def section(title, blurb, items):
        A(f"## {title}  ({len(items)})\n")
        if blurb:
            A(blurb + "\n")
        for r in items:
            A(row_line(r))
        A("")

    section("Wave 0 — Quick-win configs",
            "Existing **generalized** feeders (`gtfs`/`siri` transit, "
            "`gbfs-bikeshare`, `fdsn-seismology`) just need a feed/node entry "
            "— no new code. Highest ROI; ship these first. See the "
            "Generalization strategy table above for the family→feeder map.",
            configs)
    section("Wave 1 — Flagship new builds (15–18/18)",
            "Strongest greenfield candidates. Clean open APIs, fresh data, "
            "stable identifiers.", w1)
    section("Wave 2 — Solid new builds (12–14/18)",
            "Solid candidates; some carry a minor caveat (auth key, coarser "
            "cadence, or partial coverage).", w2)
    section("Wave 3 — Marginal new builds (10–11/18)",
            "Qualify but with real trade-offs; build when the higher waves "
            "are exhausted or when a strategic gap makes one worth pulling "
            "forward.", w3)

    A("---\n")
    A(f"_Machine-readable companion: `_implementation-ranking.tsv` "
      f"({len(qualified)} rows)._\n")

    with open(MD_OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(out))

    # console summary
    print(f"notes scanned: {len(rows)}")
    print(f"qualified:     {len(qualified)}")
    print(f"  configs (Wave0): {len(configs)}")
    print(f"  W1 15-18: {len(w1)}   W2 12-14: {len(w2)}   W3 10-11: {len(w3)}")
    print(f"  reuse builds:    {sum(1 for r in builds if r['reuse'])}")
    by_src = Counter(r["score_src"] for r in qualified)
    print(f"  score sources: {dict(by_src)}")
    print(f"wrote {os.path.relpath(MD_OUT, REPO)}")
    print(f"wrote {os.path.relpath(TSV_OUT, REPO)}")


if __name__ == "__main__":
    main()
