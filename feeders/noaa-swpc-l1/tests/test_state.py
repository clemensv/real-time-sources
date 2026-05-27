from __future__ import annotations

import json

import pytest

from noaa_swpc_l1_core import load_state, save_state


@pytest.mark.unit
def test_load_save_state_roundtrip(tmp_path):
    state_file = tmp_path / "state.json"
    payload = {"last_time_tag": "2025-01-02T03:04:05.123000+00:00"}

    save_state(str(state_file), payload)

    assert load_state(str(state_file)) == payload
    assert json.loads(state_file.read_text(encoding="utf-8")) == payload


@pytest.mark.unit
def test_load_state_missing_or_empty_path_returns_empty(tmp_path):
    assert load_state("") == {}
    assert load_state(str(tmp_path / "missing.json")) == {}


@pytest.mark.unit
def test_save_state_empty_path_is_noop():
    save_state("", {"last_time_tag": "ignored"})
