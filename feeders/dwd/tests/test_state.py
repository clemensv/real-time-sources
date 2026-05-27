"""Tests for state management."""

import json
import os
import tempfile

from dwd.util.state import load_state, save_state


class TestState:
    def test_roundtrip(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            path = f.name
        try:
            data = {"station_obs_10min": {"air_temperature": {"44": "2026-04-01T08:50:00+00:00"}}}
            save_state(path, data)
            loaded = load_state(path)
            assert loaded == data
        finally:
            os.unlink(path)

    def test_load_missing(self):
        assert load_state("/nonexistent/path.json") == {}

    def test_load_corrupt(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("not json")
            path = f.name
        try:
            assert load_state(path) == {}
        finally:
            os.unlink(path)

    def test_save_creates_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "sub", "state.json")
            save_state(path, {"key": "value"})
            assert os.path.exists(path)
