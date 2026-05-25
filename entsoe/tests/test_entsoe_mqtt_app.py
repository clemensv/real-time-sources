from entsoe_core import sample_points
from entsoe_mqtt.app import _build_data


def test_mqtt_builds_sample_payloads_for_all_families():
    payloads = [_build_data(point) for point in sample_points()]
    assert len(payloads) == 11
    assert {type(p).__name__ for p in payloads} >= {"DayAheadPrices", "CrossBorderPhysicalFlows", "ActualGenerationPerType"}
