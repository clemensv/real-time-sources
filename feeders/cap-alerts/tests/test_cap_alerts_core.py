from cap_alerts_core import mock_client_and_sources, parse_cap_xml


def test_mock_cap_xml_preserves_multi_info_and_extensions():
    client, sources = mock_client_and_sources()
    alerts = client.fetch_alerts(sources[0])
    assert len(alerts) == 1
    alert = alerts[0]
    assert alert["cap_source_id"] == "mock-cap"
    assert alert["identifier"] == "mock-20260620-001"
    assert len(alert["info"]) == 2
    assert alert["ugc_codes"] == ["CAZ001"]
    assert alert["same_codes"] == ["006001"]
    assert alert["vtec"] == ["/O.NEW.KMTR.FL.W.0001.260620T1800Z-260621T0000Z/"]
    assert alert["awareness_level"] == "3; orange; Severe"


def test_mock_zones_reference():
    client, sources = mock_client_and_sources()
    zones = client.fetch_zones(sources[0])
    assert zones[0]["zone_id"] == "CAZ001"
    assert zones[0]["cap_source_id"] == "mock-cap"
