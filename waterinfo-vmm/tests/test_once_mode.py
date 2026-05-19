"""Test that --once mode causes a single polling cycle then exits."""

from unittest.mock import patch, MagicMock

from waterinfo_vmm.waterinfo_vmm import WaterinfoVMMAPI


def test_once_mode_exits_after_one_cycle():
    api = WaterinfoVMMAPI()

    stations_payload = [
        ["station_no", "station_name", "station_id", "station_latitude",
         "station_longitude", "river_name"],
        ["L04_007", "Test Station", "1", 51.0, 4.0, "Test River"],
    ]
    readings_payload = [
        {
            "ts_id": "1001",
            "station_no": "L04_007",
            "station_name": "Test Station",
            "timestamp": "2024-01-01T00:00:00Z",
            "ts_value": 1.23,
            "ts_unitname": "m",
            "stationparameter_name": "H",
        }
    ]

    fake_producer = MagicMock()

    with patch.object(api, "list_stations", return_value=stations_payload) as ls, \
            patch.object(api, "get_latest_water_levels", return_value=readings_payload) as gw, \
            patch("confluent_kafka.Producer", return_value=fake_producer), \
            patch("time.sleep") as sleep_mock:
        api.feed_stations(
            kafka_config={"bootstrap.servers": "localhost:9092"},
            kafka_topic="test-topic",
            polling_interval=1,
            state_file="",
            once=True,
        )

    # Reference + telemetry queried exactly once.
    assert ls.call_count == 1
    assert gw.call_count == 1
    # In --once mode no inter-cycle sleep should occur.
    assert sleep_mock.call_count == 0
