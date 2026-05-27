"""Test that --once causes the EURDEP bridge to exit after one polling cycle."""

import argparse
from unittest.mock import MagicMock, patch

from eurdep_radiation.eurdep_radiation import feed


SAMPLE_FEATURE = {
    "type": "Feature",
    "geometry": {"type": "Point", "coordinates": [16.39, 48.73]},
    "properties": {
        "id": "AT0001",
        "name": "Laa/Thaya",
        "site_status": 1,
        "site_status_text": "in Betrieb",
        "height_above_sea": 183,
        "analyzed_range_in_h": 1,
        "start_measure": "2026-04-08T19:00:00Z",
        "end_measure": "2026-04-08T20:00:00Z",
        "value": 0.08,
        "unit": "µSv/h",
        "validated": 2,
        "nuclide": "Gamma-ODL-Brutto",
        "duration": "1h",
    },
}


def _make_args(once: bool):
    return argparse.Namespace(
        command="feed",
        connection_string="BootstrapServer=localhost:9092;EntityPath=eurdep-radiation",
        polling_interval=1,
        state_file="",
        once=once,
    )


@patch("eurdep_radiation.eurdep_radiation.time.sleep")
@patch("eurdep_radiation.eurdep_radiation.EuJrcEurdepEventProducer")
@patch("eurdep_radiation.eurdep_radiation.Producer")
@patch("eurdep_radiation.eurdep_radiation.EurdepAPI.fetch_all_features")
def test_once_mode_exits_after_one_cycle(
    mock_fetch, mock_producer_cls, mock_event_producer_cls, mock_sleep
):
    mock_fetch.return_value = [SAMPLE_FEATURE]
    mock_producer_cls.return_value = MagicMock()
    mock_event_producer_cls.return_value = MagicMock()

    # Should return (not loop) when --once is set.
    feed(_make_args(once=True))

    # Initial reference fetch + one telemetry fetch = 2 calls; no third.
    assert mock_fetch.call_count == 1
    # No sleep should be executed in --once mode after the cycle.
    mock_sleep.assert_not_called()
