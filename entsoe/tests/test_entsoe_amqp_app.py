from entsoe_core import sample_points
from entsoe_amqp.app import _build_data


def test_amqp_builds_sample_payloads_for_all_families():
    payloads = [_build_data(point) for point in sample_points()]
    assert len(payloads) == 11
    assert payloads[0].inDomain == "10Y1001A1001A83F"
    assert payloads[-1].outDomain == "10YFR-RTE------C"
