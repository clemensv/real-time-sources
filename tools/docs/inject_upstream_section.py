#!/usr/bin/env python3
"""Inject a standard "## Upstream" section into every source's README.md
and CONTAINER.md.

Reads upstream_links.json (sibling file). For each source dir with both
README.md and CONTAINER.md:
  - If an existing "## Upstream" section is present, replace it.
  - Otherwise insert it AFTER the H1 + the immediately following lead
    paragraph (so the section sits at the top of the doc but below the
    title and the one-line intro). If no lead paragraph is found, insert
    immediately after the H1.

The section format is:

    ## Upstream

    - Home: <a href> (humanised host or hand-curated label)
    - API docs: <a href>  (omitted if api_docs missing)

The section is bracketed with HTML comment markers so re-runs are
idempotent.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
LINKS_PATH = Path(__file__).resolve().parent / "upstream_links.json"

BEGIN = "<!-- upstream-links:begin -->"
END = "<!-- upstream-links:end -->"
SECTION_RE = re.compile(
    re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n*",
    re.DOTALL,
)


def render_section(homepage: str | None, api_docs: str | None) -> str:
    if not homepage and not api_docs:
        return ""
    lines = [BEGIN, "## Upstream", ""]
    if homepage:
        host = urlparse(homepage).hostname or homepage
        lines.append(f"- Home page: <{homepage}>")
    if api_docs:
        lines.append(f"- API / data documentation: <{api_docs}>")
    lines += ["", END, ""]
    return "\n".join(lines)


def inject(text: str, section: str) -> tuple[str, bool]:
    """Return (new_text, changed)."""
    if not section:
        return text, False
    # Remove any existing block first.
    if BEGIN in text:
        new_text = SECTION_RE.sub("", text, count=1)
    else:
        new_text = text
    # Find the H1 line (first '# ' at start of file area).
    lines = new_text.splitlines(keepends=True)
    insert_at = 0
    # Skip leading blank lines / HTML comments.
    while insert_at < len(lines) and (lines[insert_at].strip() == ""
                                       or lines[insert_at].lstrip().startswith("<!--")):
        insert_at += 1
    if insert_at < len(lines) and lines[insert_at].startswith("# "):
        # Skip the H1 itself.
        insert_at += 1
        # Skip blank lines after H1.
        while insert_at < len(lines) and lines[insert_at].strip() == "":
            insert_at += 1
        # Skip a single lead paragraph (until next blank line).
        while insert_at < len(lines) and lines[insert_at].strip() != "":
            insert_at += 1
        # Skip blank separator.
        while insert_at < len(lines) and lines[insert_at].strip() == "":
            insert_at += 1
    head = "".join(lines[:insert_at])
    tail = "".join(lines[insert_at:])
    # Ensure exactly one blank line above the inserted section.
    if head and not head.endswith("\n"):
        head += "\n"
    if head and not head.endswith("\n\n"):
        head += "\n"
    # Ensure exactly one blank line between the section end and the tail.
    if tail and not tail.startswith("\n"):
        tail = "\n" + tail
    new_text = head + section + tail
    return new_text, new_text != text


def main():
    links = json.loads(LINKS_PATH.read_text(encoding="utf-8"))
    links = {k: v for k, v in links.items() if not k.startswith("_")}
    touched = []
    skipped = []
    for src_id, info in sorted(links.items()):
        d = ROOT / src_id
        if not d.is_dir():
            skipped.append((src_id, "no source dir"))
            continue
        hp = info.get("homepage")
        api = info.get("api_docs")
        section = render_section(hp, api)
        if not section:
            skipped.append((src_id, "no urls"))
            continue
        for fname in ("README.md", "CONTAINER.md"):
            f = d / fname
            if not f.exists():
                continue
            txt = f.read_text(encoding="utf-8")
            new_txt, changed = inject(txt, section)
            if changed:
                f.write_text(new_txt, encoding="utf-8")
                touched.append(str(f.relative_to(ROOT)))
    print(f"Updated {len(touched)} files")
    for t in touched:
        print(f"  {t}")
    if skipped:
        print(f"\nSkipped {len(skipped)} sources:")
        for s, r in skipped:
            print(f"  {s} ({r})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
