"""Post-process wheels to strip absolute file:// path dependency suffixes
that pip wheel bakes in for poetry/setuptools path-deps.

Reads <wheel>, rewrites the METADATA file so any line like
    Requires-Dist: foo @ file:///abs/path
becomes
    Requires-Dist: foo
and writes <wheel> in-place.
"""
from __future__ import annotations

import argparse
import io
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

_RE = re.compile(
    r"^(Requires-Dist:\s*[A-Za-z0-9_.\-]+(?:\s*\[[^\]]+\])?)\s*@\s*file://\S+\s*(?:\r?\n[ \t]+\S+\s*)*$",
    re.MULTILINE,
)


def _strip(metadata: str) -> str:
    return _RE.sub(r"\1", metadata)


def patch(wheel_path: Path) -> bool:
    changed = False
    fd, tmp_str = tempfile.mkstemp(suffix=".whl")
    import os
    os.close(fd)
    tmp = Path(tmp_str)
    try:
        with zipfile.ZipFile(wheel_path, "r") as zin, zipfile.ZipFile(
            tmp, "w", zipfile.ZIP_DEFLATED
        ) as zout:
            for info in zin.infolist():
                data = zin.read(info.filename)
                if info.filename.endswith(".dist-info/METADATA"):
                    text = data.decode("utf-8")
                    new_text = _strip(text)
                    if new_text != text:
                        changed = True
                        data = new_text.encode("utf-8")
                zout.writestr(info, data)
        if changed:
            shutil.move(str(tmp), str(wheel_path))
        else:
            tmp.unlink(missing_ok=True)
    except Exception:
        tmp.unlink(missing_ok=True)
        raise
    return changed


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("wheels", nargs="+", type=Path)
    args = p.parse_args(argv)
    for w in args.wheels:
        if not w.is_file():
            print(f"skip (not a file): {w}", file=sys.stderr)
            continue
        changed = patch(w)
        print(f"{'patched' if changed else 'unchanged'}: {w.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
