from openaq_core import build_mock_client, should_publish_measurement
from openaq.app import build_location, build_measurement, build_sensor


def test_mock_cycle_builds_all_payloads():
    client = build_mock_client()
    location = next(client.iter_locations([], [], None))
    sensors = {s.sensor_id: s for s in client.sensors_for_location(location)}
    measurements = client.latest_for_location(location, sensors)
    assert build_location(location).location_id == 1001
    assert build_sensor(next(iter(sensors.values()))).sensor_id == 2001
    assert build_measurement(measurements[0]).value == 11.2


def test_measurement_dedupe_state():
    client = build_mock_client()
    location = next(client.iter_locations([], [], None))
    sensors = {s.sensor_id: s for s in client.sensors_for_location(location)}
    measurement = client.latest_for_location(location, sensors)[0]
    state = {}
    assert should_publish_measurement(measurement, state) is True
    assert should_publish_measurement(measurement, state) is False
