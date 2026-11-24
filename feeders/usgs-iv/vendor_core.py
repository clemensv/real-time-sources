"""Build/check the shared pure-Python USGS core wheel for isolated source contexts.

Run with Python 3.11+ from any working directory. No package installation or
network access is needed. The authoritative core remains under usgs-waterdata.
"""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import io
import json
from pathlib import Path
import tomllib
import zipfile


ROOT = Path(__file__).resolve().parents[2]
CORE = ROOT / "feeders" / "usgs-waterdata" / "usgs_waterdata_core"
DESTINATIONS = [ROOT / "feeders" / source / "vendor" for source in ("usgs-iv", "usgs-nwis-wq")]


def source_bytes(path: Path) -> bytes:
    # Canonical CRLF preserves the reviewed wheel across Git autocrlf checkouts.
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")


def build() -> tuple[str, bytes, dict[str, object]]:
    source_files = {
        str(path.relative_to(CORE)).replace("\\", "/"): source_bytes(path)
        for path in sorted((CORE / "usgs_waterdata_core").rglob("*.py"))
    }
    source_files["pyproject.toml"] = source_bytes(CORE / "pyproject.toml")
    hashes = {name: hashlib.sha256(data).hexdigest() for name, data in source_files.items()}
    source_hash = hashlib.sha256(
        json.dumps(hashes, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    version = f"0.1.0+{source_hash[:12]}"
    name = "usgs_waterdata_core"
    dist = f"{name}-{version}.dist-info"
    project = tomllib.loads(source_files["pyproject.toml"].decode("utf-8"))["project"]
    metadata = [
        "Metadata-Version: 2.3", f"Name: {project['name']}", f"Version: {version}",
        f"Summary: {project['description']}", f"Requires-Python: {project['requires-python']}",
        *(f"Requires-Dist: {dependency}" for dependency in project["dependencies"]), "", "",
    ]
    contents = {key: value for key, value in source_files.items() if key != "pyproject.toml"}
    contents[f"{dist}/METADATA"] = "\n".join(metadata).encode("utf-8")
    contents[f"{dist}/WHEEL"] = b"Wheel-Version: 1.0\nGenerator: usgs-vendor-core\nRoot-Is-Purelib: true\nTag: py3-none-any\n"
    scripts = project.get("scripts", {})
    contents[f"{dist}/entry_points.txt"] = (
        "[console_scripts]\n" + "".join(f"{key} = {value}\n" for key, value in sorted(scripts.items()))
    ).encode("utf-8")
    rows = []
    for path, data in sorted(contents.items()):
        digest = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b"=").decode("ascii")
        rows.append((path, f"sha256={digest}", str(len(data))))
    rows.append((f"{dist}/RECORD", "", ""))
    record = io.StringIO(newline="")
    csv.writer(record, lineterminator="\n").writerows(rows)
    contents[f"{dist}/RECORD"] = record.getvalue().encode("utf-8")
    stream = io.BytesIO()
    # Stored entries avoid zlib-version-dependent compressed bytes.
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_STORED) as archive:
        for path, data in sorted(contents.items()):
            info = zipfile.ZipInfo(path, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    wheel = stream.getvalue()
    filename = f"{name}-{version}-py3-none-any.whl"
    manifest: dict[str, object] = {
        "authoritative_source": "feeders/usgs-waterdata/usgs_waterdata_core",
        "builder": "feeders/usgs-iv/vendor_core.py",
        "source_sha256": source_hash,
        "files": hashes,
        "wheel": filename,
        "wheel_sha256": hashlib.sha256(wheel).hexdigest(),
    }
    return filename, wheel, manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if either vendored wheel differs from the authoritative core")
    args = parser.parse_args()
    filename, wheel, manifest = build()
    manifest_bytes = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")
    for directory in DESTINATIONS:
        if args.check:
            path = directory / filename
            if (
                not path.exists() or path.read_bytes() != wheel
                or not (directory / "core-wheel.json").exists()
                or (directory / "core-wheel.json").read_bytes().replace(b"\r\n", b"\n") != manifest_bytes
                or len(list(directory.glob("*.whl"))) != 1
            ):
                raise SystemExit(f"Stale USGS core vendor wheel: {directory}; run python feeders\\usgs-iv\\vendor_core.py")
        else:
            directory.mkdir(parents=True, exist_ok=True)
            for old in directory.glob("usgs_waterdata_core-*.whl"):
                old.unlink()
            (directory / filename).write_bytes(wheel)
            (directory / "core-wheel.json").write_bytes(manifest_bytes)
    print(f"{'Verified' if args.check else 'Built'} {filename}: {manifest['wheel_sha256']}")


if __name__ == "__main__":
    main()
