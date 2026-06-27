#!/usr/bin/env python3
"""P3 mojibake / encoding lint.

Detects the CP1252 round-trip corruption and raw-CP1252 bytes that have
repeatedly damaged generated catalog and documentation files:

* incident ``25e33ecd2`` -- the root-README generator wrote double-encoded
  ``Ã``/``â€`` mojibake across 106 catalog fields;
* ``cap-alerts/EVENTS.md`` -- a raw CP1252 ``0x97`` em-dash byte (invalid UTF-8);
* ``king-county-marine/EVENTS.md`` -- eight ``Â°`` / ``Âµ`` / ``Â²`` sequences.

Files must be valid UTF-8, BOM-free, and free of the mojibake signatures below.

Usage::

    python tools/ci/lint_catalog_encoding.py                # root catalog.json + README.md
    python tools/ci/lint_catalog_encoding.py <file> [...]   # explicit files

Exit 1 on any finding.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

# High-precision signatures: a UTF-8 multibyte char decoded as CP1252 and then
# re-encoded as UTF-8 yields these stable 2-3 char sequences. They effectively
# never occur in correct text in this repo's languages, so false positives are
# negligible.
SIGNATURES = {
    "\u00c3\u00a9": "A-tilde e (mojibake for e-acute)",
    "\u00c3\u00a8": "A-tilde egrave",
    "\u00c3\u00bc": "A-tilde u-umlaut",
    "\u00c3\u00b6": "A-tilde o-umlaut",
    "\u00c3\u00a4": "A-tilde a-umlaut",
    "\u00c3\u009f": "A-tilde sharp-s",
    "\u00e2\u0080\u0099": "a-circ euro right-single-quote",
    "\u00e2\u0080\u009c": "a-circ euro left-double-quote",
    "\u00e2\u0080\u009d": "a-circ euro right-double-quote",
    "\u00e2\u0080\u0094": "a-circ euro em-dash",
    "\u00c2\u00b0": "A-circ degree",
    "\u00c2\u00b5": "A-circ micro",
    "\u00c2\u00b2": "A-circ squared",
}


def check(path: Path) -> list[str]:
    findings: list[str] = []
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        findings.append("UTF-8 BOM present")
        data = data[3:]
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        findings.append(f"not valid UTF-8 (raw CP1252 byte?): {exc}")
        return findings
    for sig, desc in SIGNATURES.items():
        n = text.count(sig)
        if n:
            disp = sig.encode("unicode_escape").decode("ascii")
            findings.append(f"mojibake {disp} ({desc}) x{n}")
    return findings


def main(argv: list[str]) -> int:
    files = [Path(a) for a in argv] if argv else [REPO / "catalog.json", REPO / "README.md"]
    bad = 0
    checked = 0
    for f in files:
        if not f.exists():
            continue
        checked += 1
        found = check(f)
        if found:
            bad += 1
            print(f"FAIL {f}:")
            for x in found:
                print(f"    - {x}")
    if bad:
        print(f"\n{bad} file(s) with encoding problems (of {checked} checked)")
        return 1
    print(f"OK: {checked} file(s) clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
