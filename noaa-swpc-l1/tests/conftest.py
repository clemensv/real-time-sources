from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import pytest

from noaa_swpc_l1_core import EXPECTED_COLUMNS, PropagatedSolarWindRow


@pytest.fixture
def upstream_payload() -> list[list[Any]]:
    return [
        EXPECTED_COLUMNS.copy(),
        [
            "2025-01-02 03:04:05.123",
            "410.5",
            "6.2",
            "123456",
            "-1.1",
            "2.2",
            None,
            "3.3",
            None,
            "",
            "not-a-number",
            "2025-01-02 03:44:05.123",
        ],
        [
            "2025-01-02 03:05:05.000",
            411,
            None,
            "123457",
            "-1.0",
            "2.0",
            "0.1",
            "3.0",
            None,
            None,
            None,
            "2025-01-02 03:45:05.000",
        ],
    ]


@pytest.fixture
def sample_row() -> PropagatedSolarWindRow:
    return PropagatedSolarWindRow(
        spacecraft="dscovr",
        time_tag=datetime(2025, 1, 2, 3, 4, 5, 123000, tzinfo=timezone.utc),
        propagated_time_tag=datetime(2025, 1, 2, 3, 44, 5, 123000, tzinfo=timezone.utc),
        speed=410.5,
        density=6.2,
        temperature=123456.0,
        bx=-1.1,
        by=2.2,
        bz=None,
        bt=3.3,
        vx=None,
        vy=None,
        vz=None,
    )


class FakeResponse:
    def __init__(self, payload: Any) -> None:
        self.payload = payload
        self.raise_for_status_called = False

    def raise_for_status(self) -> None:
        self.raise_for_status_called = True

    def json(self) -> Any:
        return self.payload


class FakeSession:
    def __init__(self, payload: Any) -> None:
        self.response = FakeResponse(payload)
        self.calls: list[tuple[str, float]] = []

    def get(self, url: str, timeout: float) -> FakeResponse:
        self.calls.append((url, timeout))
        return self.response


@pytest.fixture
def fake_session_factory():
    return FakeSession
