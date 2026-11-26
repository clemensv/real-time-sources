"""Shared-core freshness, offline bundling and CI install ordering."""

import importlib.util
from pathlib import Path
import shutil
import sys

import pytest


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "feeders" / "usgs-iv"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_bundle_contains_identical_verified_core(tmp_path):
    helper = load("vendor_wheels", ROOT / "tools" / "deploy-fabric" / "vendor_wheels.py")
    wheels = helper.copy_vendor_wheels(SOURCE, tmp_path)
    assert len(wheels) == 1
    assert wheels[0].read_bytes() == (SOURCE / "vendor" / wheels[0].name).read_bytes()


def test_modified_vendor_wheel_fails_before_install(tmp_path):
    helper = load("vendor_wheels", ROOT / "tools" / "deploy-fabric" / "vendor_wheels.py")
    shutil.copytree(SOURCE / "vendor", tmp_path / "vendor")
    wheel = next((tmp_path / "vendor").glob("*.whl"))
    wheel.write_bytes(wheel.read_bytes() + b"modified")
    with pytest.raises(ValueError, match="modified vendor wheel"):
        helper.vendored_wheels(tmp_path)


def test_import_smoke_registers_core_before_local_resolution(monkeypatch):
    smoke = load("import_smoke", ROOT / "tools" / "ci" / "import_smoke.py")
    wheel = next((SOURCE / "vendor").glob("*.whl"))
    commands = []
    monkeypatch.setattr(smoke, "vendored_wheels", lambda source: [wheel])
    monkeypatch.setattr(smoke, "install_order", lambda source: [SOURCE])
    monkeypatch.setattr(smoke, "dockerfile_modules", lambda source: [])
    monkeypatch.setattr(smoke.compileall, "compile_dir", lambda *args, **kwargs: True)
    monkeypatch.setattr(smoke, "_run", lambda command: commands.append(command) or 0)
    assert smoke.main([str(SOURCE), "--install-only"]) == 0
    assert str(wheel) == commands[0][-1] and "--no-deps" in commands[0]
    assert "-e" in commands[1] and "--no-deps" in commands[1]
    assert str(wheel) == commands[2][-1] and "--no-deps" not in commands[2]
    assert "-e" in commands[3] and "--no-deps" not in commands[3]


def test_vendor_archive_is_identical_for_lf_checkout(monkeypatch):
    helper = load("vendor_core", SOURCE / "vendor_core.py")
    expected = helper.build()
    original = Path.read_bytes

    def lf_checkout(path):
        data = original(path)
        return data.replace(b"\r\n", b"\n") if path.is_relative_to(helper.CORE) else data

    monkeypatch.setattr(Path, "read_bytes", lf_checkout)
    assert helper.build() == expected


def test_vendor_check_accepts_crlf_manifest_without_changing_wheel(tmp_path, monkeypatch):
    helper = load("vendor_core", SOURCE / "vendor_core.py")
    shutil.copytree(SOURCE / "vendor", tmp_path / "vendor")
    manifest = tmp_path / "vendor" / "core-wheel.json"
    manifest.write_bytes(manifest.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
    monkeypatch.setattr(helper, "DESTINATIONS", [manifest.parent])
    monkeypatch.setattr(sys, "argv", ["vendor_core.py", "--check"])
    helper.main()
