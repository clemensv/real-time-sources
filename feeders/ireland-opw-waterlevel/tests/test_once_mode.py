"""Unit test for --once mode: feed() exits after a single polling cycle."""

from unittest.mock import MagicMock, patch

from ireland_opw_waterlevel import ireland_opw_waterlevel as bridge


SAMPLE_FEATURES = [
    {
        "type": "Feature",
        "properties": {
            "station_ref": "0000001041",
            "station_name": "Sandy Mills",
            "sensor_ref": "0001",
            "region_id": 3,
            "datetime": "2024-01-15T12:00:00Z",
            "value": "0.368",
            "err_code": 99,
        },
        "geometry": {"type": "Point", "coordinates": [-7.5, 54.8]},
    }
]


def test_feed_once_exits_after_one_cycle():
    """feed(..., once=True) must return after one polling cycle, not loop."""
    with patch.object(bridge, "fetch_geojson", return_value=SAMPLE_FEATURES) as mock_fetch, \
         patch.object(bridge, "Producer") as mock_producer_cls, \
         patch.object(bridge, "IeGovOpwWaterlevelEventProducer") as mock_pc_cls, \
         patch.object(bridge.time, "sleep") as mock_sleep:
        mock_producer_cls.return_value = MagicMock()
        mock_pc_cls.return_value = MagicMock()

        bridge.feed(
            kafka_config={"bootstrap.servers": "localhost:9092"},
            kafka_topic="test-topic",
            polling_interval=0,
            state_file="",
            once=True,
        )

        # One fetch for initial reference data + one fetch in the loop
        assert mock_fetch.call_count == 2
        # Must not sleep when --once is set
        mock_sleep.assert_not_called()
