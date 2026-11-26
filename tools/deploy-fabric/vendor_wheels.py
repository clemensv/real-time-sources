"""Verify source-local shared wheels and copy them into a notebook bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]


def vendored_wheels(source: Path) -> list[Path]:
    manifest_path = source / "vendor" / "core-wheel.json"
    if not manifest_path.exists():
        return []
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    filename = manifest["wheel"]
    if Path(filename).name != filename or not filename.endswith(".whl"):
        raise ValueError(f"Invalid vendor wheel filename: {manifest_path}")
    wheel = manifest_path.parent / filename
    if not wheel.is_file() or hashlib.sha256(wheel.read_bytes()).hexdigest() != manifest["wheel_sha256"]:
        raise ValueError(f"Missing or modified vendor wheel: {wheel}")
    if sorted(manifest_path.parent.glob("*.whl")) != [wheel]:
        raise ValueError(f"Unexpected stale wheels in {manifest_path.parent}")
    builder = (ROOT / manifest["builder"]).resolve()
    if not builder.is_relative_to(ROOT) or not builder.is_file():
        raise ValueError(f"Vendor wheel builder is unavailable: {builder}")
    subprocess.run([sys.executable, str(builder), "--check"], cwd=ROOT, check=True)
    return [wheel]


def copy_vendor_wheels(source: Path, destination: Path) -> list[Path]:
    wheels = vendored_wheels(source)
    destination.mkdir(parents=True, exist_ok=True)
    copied = []
    for wheel in wheels:
        target = destination / wheel.name
        if target.resolve() != wheel.resolve():
            shutil.copyfile(wheel, target)
        copied.append(target)
    return copied


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Source directory, e.g. feeders/usgs-iv")
    parser.add_argument("destination", type=Path, help="Wheel bundle output directory")
    args = parser.parse_args()
    for wheel in copy_vendor_wheels(args.source.resolve(), args.destination.resolve()):
        print(f"Included verified shared wheel: {wheel.name}")


if __name__ == "__main__":
    main()
