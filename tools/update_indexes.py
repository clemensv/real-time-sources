"""Append a 'Round 2026-05' section to each touched INDEX.md, or create a
fresh INDEX.md if the topic folder is new.

This script scans tools/candidates/<topic>/ for files whose basename starts
with any of the round prefixes (gulf countries + satellite agencies). For
each such file it pulls the H1 title and the Score line, then writes a
table row into the INDEX.

Idempotent: if an "## Round 2026-05" heading already exists it is replaced.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "tools" / "candidates"
ROUND_HEADER = "## Round 2026-05 — Gulf + Satellite EO sweep"
PREFIXES = (
    "kw-", "ae-", "om-", "sa-", "bh-", "qa-", "iq-",
    "nasa-", "esa-", "noaasat-", "eumetsat-",
    "jaxa-", "isro-", "kari-", "cnsa-", "tasa-",
    "spaceother-",
)

H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.M)
SCORE_RE = re.compile(r"\*\*Score\*\*[: ]*\s*\*?\*?(\d+\s*/\s*18)", re.I)
SCORE_ALT_RE = re.compile(r"Score[: ]\s*\*?\*?(\d+\s*/\s*18)", re.I)
VERDICT_RE = re.compile(
    r"\*\*Verdict\*\*[: ]*\s*\**\s*([✅⚠️⏭️❌][^\n*]+?)(?:\*\*|$)",
    re.M,
)
VERDICT_ALT_RE = re.compile(
    r"(✅\s*\*?\*?Build|⚠️\s*\*?\*?Maybe|⏭️\s*\*?\*?Reference|❌\s*\*?\*?Skip)",
    re.I,
)


def extract(file: Path) -> tuple[str, str, str]:
    text = file.read_text(encoding="utf-8", errors="replace")
    h1 = H1_RE.search(text)
    title = h1.group(1).strip() if h1 else file.stem
    title = re.sub(r"\s+", " ", title)
    score_m = SCORE_RE.search(text) or SCORE_ALT_RE.search(text)
    score = score_m.group(1).replace(" ", "") if score_m else "?/18"
    v_m = VERDICT_RE.search(text)
    if v_m:
        verdict = v_m.group(1).strip().rstrip("*").strip()
    else:
        v_m2 = VERDICT_ALT_RE.search(text)
        verdict = v_m2.group(1) if v_m2 else "—"
    verdict = re.sub(r"\s+", " ", verdict)[:80]
    return title, score, verdict


def build_section(files: list[Path]) -> str:
    lines = [
        ROUND_HEADER,
        "",
        "Added in May 2026 by the Gulf (KW/AE/OM/SA/BH/QA/IQ) and satellite-EO "
        "(NASA/ESA/NOAA/EUMETSAT/JAXA/ISRO/KARI/CNSA/Other) research fleets.",
        "",
        "| Candidate | File | Score | Verdict |",
        "|---|---|---|---|",
    ]
    for f in sorted(files, key=lambda p: p.name):
        title, score, verdict = extract(f)
        # Escape pipes in title/verdict
        title = title.replace("|", "\\|")
        verdict = verdict.replace("|", "\\|")
        lines.append(f"| {title} | [{f.name}]({f.name}) | {score} | {verdict} |")
    lines.append("")
    return "\n".join(lines)


def folder_friendly_name(folder: str) -> str:
    return folder.replace("-", " ").title()


touched_summary: list[tuple[str, int]] = []

for topic_dir in sorted(ROOT.iterdir()):
    if not topic_dir.is_dir() or topic_dir.name.startswith("_"):
        continue
    new_files = [
        f for f in topic_dir.iterdir()
        if f.is_file()
        and f.suffix == ".md"
        and f.name != "INDEX.md"
        and any(f.name.startswith(p) for p in PREFIXES)
    ]
    if not new_files:
        continue
    section = build_section(new_files)
    index = topic_dir / "INDEX.md"
    if index.exists():
        text = index.read_text(encoding="utf-8")
        # Strip an existing round-2026-05 section, if any
        text = re.sub(
            r"\n*## Round 2026-05[^\n]*\n.*?(?=\n## |\Z)",
            "",
            text,
            flags=re.S,
        )
        text = text.rstrip() + "\n\n" + section + "\n"
        index.write_text(text, encoding="utf-8")
    else:
        # Brand new topic folder — create a minimal INDEX.md
        header = f"# {folder_friendly_name(topic_dir.name)} — Candidate Sources\n\n"
        index.write_text(header + section + "\n", encoding="utf-8")
    touched_summary.append((topic_dir.name, len(new_files)))

print(f"Updated INDEX.md in {len(touched_summary)} topic folders:")
for name, n in touched_summary:
    print(f"  {name:30s} +{n}")
print(f"\nTotal new candidate files indexed: {sum(n for _, n in touched_summary)}")
