"""
Convert pyproject.toml files from poetry-core to setuptools + setuptools-scm.

This script converts the build backend so that `pip wheel` automatically
derives the package version from git tags via setuptools-scm, eliminating
hardcoded 0.1.0 versions.

Conversion rules:
- build-system → setuptools + setuptools-scm
- [tool.poetry] metadata → [project] (PEP 621)
- version → dynamic = ["version"]
- poetry deps → PEP 621 dependencies (path deps dropped, python → requires-python)
- poetry scripts → [project.scripts]
- dev-dependencies → [project.optional-dependencies] dev
- Package discovery configured for src-layout or flat-layout
- [tool.setuptools_scm] added
"""

import sys
import re
import tomllib
import tomli_w
from pathlib import Path


def convert_poetry_version_spec(name: str, spec) -> str | None:
    """Convert a poetry dependency spec to PEP 621 format."""
    if isinstance(spec, dict):
        if "path" in spec:
            return None  # Drop path dependencies
        version = spec.get("version", "")
        extras = spec.get("extras", [])
        optional = spec.get("optional", False)
        if optional:
            return None
        extra_str = f"[{','.join(extras)}]" if extras else ""
        if version:
            return f"{name}{extra_str}{convert_version_constraint(version)}"
        return f"{name}{extra_str}"
    elif isinstance(spec, str):
        if spec == "*":
            return name
        return f"{name}{convert_version_constraint(spec)}"
    return name


def convert_version_constraint(spec: str) -> str:
    """Convert poetry version constraint to PEP 440."""
    if not spec:
        return ""
    # Handle comma-separated constraints
    parts = [s.strip() for s in spec.split(",")]
    converted = []
    for part in parts:
        converted.append(convert_single_constraint(part))
    return ",".join(converted)


def convert_single_constraint(part: str) -> str:
    """Convert a single poetry version constraint to PEP 440."""
    part = part.strip()
    if part.startswith("^"):
        # Caret: ^1.2.3 means >=1.2.3,<2.0.0 (major); ^0.2.3 means >=0.2.3,<0.3.0
        ver = part[1:]
        segments = ver.split(".")
        major = int(segments[0]) if segments else 0
        if major > 0:
            return f">={ver},<{major + 1}.0.0"
        elif len(segments) > 1:
            minor = int(segments[1])
            return f">={ver},<0.{minor + 1}.0"
        else:
            return f">={ver},<1.0.0"
    elif part.startswith("~"):
        # Tilde: ~1.2.3 means >=1.2.3,<1.3.0
        ver = part[1:]
        segments = ver.split(".")
        major = int(segments[0]) if segments else 0
        minor = int(segments[1]) if len(segments) > 1 else 0
        return f">={ver},<{major}.{minor + 1}.0"
    elif part.startswith(">=") or part.startswith("<=") or part.startswith("!=") or part.startswith("==") or part.startswith(">") or part.startswith("<"):
        return part
    else:
        return f"=={part}"


def detect_package_layout(pyproject_path: Path) -> dict:
    """Detect whether this is a src-layout or flat-layout package."""
    parent = pyproject_path.parent
    src_dir = parent / "src"
    if src_dir.is_dir():
        # src-layout (typical for generated producer packages)
        return {"where": ["src"]}
    else:
        return {}


def convert_pyproject(path: Path, dry_run: bool = False) -> bool:
    """Convert a single pyproject.toml from poetry to setuptools+scm. Returns True if changed."""
    with open(path, "rb") as f:
        data = tomllib.load(f)

    # Skip if already using setuptools
    build_sys = data.get("build-system", {})
    if "setuptools" in build_sys.get("build-backend", ""):
        return False

    # Must be a poetry-core project
    if "poetry" not in build_sys.get("build-backend", ""):
        return False

    poetry = data.get("tool", {}).get("poetry", {})
    if not poetry:
        return False

    # Build new pyproject structure
    new = {}

    # [build-system]
    new["build-system"] = {
        "requires": ["setuptools>=64", "setuptools-scm>=8"],
        "build-backend": "setuptools.build_meta",
    }

    # [project]
    project = {}
    project["name"] = poetry.get("name", path.parent.name)
    project["dynamic"] = ["version"]

    desc = poetry.get("description", "")
    if desc:
        project["description"] = desc

    authors = poetry.get("authors", [])
    if authors:
        pep621_authors = []
        for a in authors:
            match = re.match(r"^(.+?)\s*<(.+?)>\s*$", a)
            if match:
                pep621_authors.append({"name": match.group(1).strip(), "email": match.group(2)})
            else:
                pep621_authors.append({"name": a})
        project["authors"] = pep621_authors

    license_val = poetry.get("license", "")
    if license_val:
        project["license"] = license_val

    # requires-python
    deps = poetry.get("dependencies", {})
    python_req = deps.get("python", "")
    if python_req:
        project["requires-python"] = python_req

    # dependencies (skip python, skip path deps)
    pep621_deps = []
    for name, spec in deps.items():
        if name == "python":
            continue
        converted = convert_poetry_version_spec(name, spec)
        if converted:
            pep621_deps.append(converted)
    if pep621_deps:
        project["dependencies"] = sorted(pep621_deps)

    # scripts
    scripts = poetry.get("scripts", {})
    if scripts:
        project["scripts"] = scripts

    # optional-dependencies (dev)
    dev_deps = poetry.get("dev-dependencies", {})
    if dev_deps:
        dev_list = []
        for name, spec in dev_deps.items():
            converted = convert_poetry_version_spec(name, spec)
            if converted:
                dev_list.append(converted)
        if dev_list:
            project["optional-dependencies"] = {"dev": sorted(dev_list)}

    new["project"] = project

    # [tool.setuptools_scm]
    tool = {}

    # Compute relative path from pyproject.toml to repo root (where .git lives)
    # Walk up from the pyproject.toml until we find .git
    repo_root = path.parent
    while repo_root != repo_root.parent:
        if (repo_root / ".git").exists():
            break
        repo_root = repo_root.parent

    try:
        rel = path.parent.relative_to(repo_root)
        depth = len(rel.parts)
        root_rel = "/".join([".."] * depth) if depth > 0 else "."
    except ValueError:
        root_rel = "."

    tool["setuptools_scm"] = {
        "root": root_rel,
        "version_scheme": "post-release",
        "local_scheme": "no-local-version",
    }

    # [tool.setuptools.packages.find]
    layout = detect_package_layout(path)
    if layout:
        tool["setuptools"] = {"packages": {"find": layout}}
    else:
        # For flat layout, find Python packages (directories with __init__.py)
        # Exclude test directories
        pkg_dirs = [
            d.name for d in path.parent.iterdir()
            if d.is_dir()
            and (d / "__init__.py").exists()
            and not d.name.startswith(".")
            and d.name not in ("tests", "test", "testing")
        ]
        if pkg_dirs:
            tool["setuptools"] = {"packages": pkg_dirs}

    new["tool"] = tool

    if dry_run:
        print(f"Would convert: {path}")
        return True

    with open(path, "wb") as f:
        tomli_w.dump(new, f)
    return True


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Convert poetry pyproject.toml to setuptools+scm")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be changed")
    parser.add_argument("--path", type=str, help="Convert a single file")
    parser.add_argument("--feeders-dir", type=str, default="feeders", help="Root feeders directory")
    args = parser.parse_args()

    if args.path:
        p = Path(args.path)
        if convert_pyproject(p, args.dry_run):
            print(f"Converted: {p}")
        else:
            print(f"Skipped (already setuptools or not poetry): {p}")
        return

    feeders = Path(args.feeders_dir)
    if not feeders.is_dir():
        print(f"Error: {feeders} not found", file=sys.stderr)
        sys.exit(1)

    converted = 0
    skipped = 0
    errors = []
    for pyproj in sorted(feeders.rglob("pyproject.toml")):
        try:
            if convert_pyproject(pyproj, args.dry_run):
                converted += 1
            else:
                skipped += 1
        except Exception as e:
            errors.append((pyproj, str(e)))

    print(f"\nConverted: {converted}, Skipped: {skipped}, Errors: {len(errors)}")
    for p, e in errors:
        print(f"  ERROR {p}: {e}")


if __name__ == "__main__":
    main()
