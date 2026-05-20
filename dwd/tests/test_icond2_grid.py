"""Tests for the IconD2GridModule polling state machine.

These tests stub the network listings and the eccodes/numpy decode path so
they run without libeccodes installed and without contacting opendata.dwd.de.
The goal is to verify:
  - module metadata (name, default_enabled, default_poll_interval),
  - filename discovery picks the newest run per parameter,
  - state checkpointing prevents re-emission across polls,
  - the emitted event shape matches the IconD2 contract.
"""

from __future__ import annotations

import sys
import types
from typing import Any, Dict, List
from unittest.mock import MagicMock, patch

import pytest

from dwd.modules.icond2_grid import IconD2GridModule
from dwd.util.http_client import DirEntry
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# Stub HTTP client
# ---------------------------------------------------------------------------

class FakeHttp:
    def __init__(self):
        self.base_url = "https://opendata.dwd.de"
        self.dirs: Dict[str, List[str]] = {}
        self.downloads: Dict[str, bytes] = {}
        self.download_calls: List[str] = []

    def list_directory(self, path: str) -> List[DirEntry]:
        names = self.dirs.get(path, [])
        ts = datetime(2026, 1, 1, tzinfo=timezone.utc)
        return [DirEntry(name=n, modified=ts, size_str="123K") for n in names]

    def download_bytes(self, path: str):
        self.download_calls.append(path)
        return self.downloads.get(path, b"fake-grib-bytes")


# ---------------------------------------------------------------------------
# Build a module with a stubbed _build_event so we don't need eccodes.
# ---------------------------------------------------------------------------

def _make_module(http, parameters=("t_2m",), max_files=12):
    mod = IconD2GridModule(http, parameters=list(parameters),
                           max_files_per_poll=max_files)

    def fake_build_event(run_id, param, lead):
        from datetime import timedelta
        run_dt = datetime.strptime(run_id, "%Y%m%d%H").replace(tzinfo=timezone.utc)
        valid = run_dt + timedelta(hours=lead)
        return {
            "run_id": run_id,
            "run_time": run_dt.isoformat().replace("+00:00", "Z"),
            "parameter": param,
            "unit": "degC",
            "lead_hour": int(lead),
            "valid_time": valid.isoformat().replace("+00:00", "Z"),
            "produced_at": "2026-01-01T00:05:00Z",
            "source_url": (
                f"https://opendata.dwd.de/weather/nwp/icon-d2/grib/"
                f"{run_dt.strftime('%H')}/{param}/"
                f"icon-d2_germany_icosahedral_single-level_"
                f"{run_id}_{lead:03d}_2d_{param}.grib2.bz2"
            ),
            "resolution_deg": 0.1,
            "bbox_min_lon": -4.0, "bbox_min_lat": 43.0,
            "bbox_max_lon": 20.5, "bbox_max_lat": 58.2,
            "lats": [50.0], "lons": [10.0], "values": [5.5],
        }

    mod._build_event = fake_build_event  # type: ignore[assignment]
    return mod


def _file(run_id: str, lead: int, param: str) -> str:
    return (f"icon-d2_germany_icosahedral_single-level_"
            f"{run_id}_{lead:03d}_2d_{param}.grib2.bz2")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_module_metadata():
    mod = IconD2GridModule(FakeHttp())
    assert mod.name == "icond2_grid"
    assert mod.default_enabled is False
    assert mod.default_poll_interval == 600


def test_unsupported_parameter_rejected():
    with pytest.raises(ValueError):
        IconD2GridModule(FakeHttp(), parameters=["not_a_real_param"])


def test_emits_each_lead_once_then_checkpoints():
    http = FakeHttp()
    # The 00Z run directory has two lead hours available.
    http.dirs["weather/nwp/icon-d2/grib/00/t_2m/"] = [
        _file("2026010100", 0, "t_2m"),
        _file("2026010100", 1, "t_2m"),
    ]
    mod = _make_module(http)

    state: Dict[str, Any] = {}
    events = mod.poll(state)
    assert [e["data"]["lead_hour"] for e in events] == [0, 1]
    assert all(e["type"] == "icond2_grid" for e in events)

    # Second poll over unchanged listing: nothing new.
    events2 = mod.poll(state)
    assert events2 == []

    # State carries the emitted lead hours under the run_id.
    assert state["last_emitted"]["2026010100"]["t_2m"] == [0, 1]


def test_picks_newest_run_across_directories():
    http = FakeHttp()
    # Older run published earlier in the day.
    http.dirs["weather/nwp/icon-d2/grib/00/t_2m/"] = [
        _file("2026010100", 0, "t_2m"),
    ]
    # Newer run in a later directory should win.
    http.dirs["weather/nwp/icon-d2/grib/12/t_2m/"] = [
        _file("2026010112", 0, "t_2m"),
    ]
    mod = _make_module(http)
    events = mod.poll({})
    assert len(events) == 1
    assert events[0]["data"]["run_id"] == "2026010112"


def test_max_files_per_poll_caps_emissions():
    http = FakeHttp()
    http.dirs["weather/nwp/icon-d2/grib/00/t_2m/"] = [
        _file("2026010100", h, "t_2m") for h in range(0, 5)
    ]
    mod = _make_module(http, max_files=2)
    events = mod.poll({})
    assert len(events) == 2


def test_event_payload_fields_match_contract():
    http = FakeHttp()
    http.dirs["weather/nwp/icon-d2/grib/00/t_2m/"] = [
        _file("2026010100", 0, "t_2m"),
    ]
    mod = _make_module(http)
    events = mod.poll({})
    data = events[0]["data"]
    # Required fields per xreg DE.DWD.IconD2.jstruct.Grid.
    required = {
        "run_id", "run_time", "parameter", "unit", "lead_hour",
        "valid_time", "produced_at", "source_url", "resolution_deg",
        "bbox_min_lon", "bbox_min_lat", "bbox_max_lon", "bbox_max_lat",
        "lats", "lons", "values",
    }
    assert required.issubset(data.keys())
    # Key/subject components must be the literal field values.
    assert data["run_id"] == "2026010100"
    assert data["parameter"] == "t_2m"
    assert data["lead_hour"] == 0
