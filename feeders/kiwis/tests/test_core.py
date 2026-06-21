from kiwis_core import KiWISClient, MOCK_ENDPOINTS, load_endpoints
from kiwis_core.core import normalize_station, normalize_timeseries, normalize_value


def test_default_mock_cycle_shapes():
    endpoint = load_endpoints(mock=True)[0]
    client = KiWISClient(endpoint, mock=True)
    station = normalize_station(endpoint, client.stations()[0])
    assert station["kiwis_id"] == "sepa"
    assert station["station_id"] == "36870"
    ts = normalize_timeseries(endpoint, client.timeseries()[0])
    assert ts["ts_id"] == "65452010"
    value = normalize_value(endpoint, client.timeseries()[0], client.values(["65452010"])["65452010"][0])
    assert value["value"] == 0.2
    assert value["quality_code"] == 254


def test_csv_endpoint_config():
    endpoints = load_endpoints("x,https://example.invalid/KiWIS,0,station_id=1,station_id=1,2,PT1H,")
    assert endpoints[0].kiwis_id == "x"
    assert endpoints[0].ts_ids == "2"
