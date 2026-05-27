from digitraffic_maritime_mqtt.app import _parse_broker_url


def test_parse_broker_url_defaults_plain_mqtt():
    host, port, tls = _parse_broker_url('mqtt.example.local')
    assert host == 'mqtt.example.local'
    assert port == 1883
    assert tls is False


def test_parse_broker_url_mqtts():
    host, port, tls = _parse_broker_url('mqtts://broker.example.local:8883')
    assert host == 'broker.example.local'
    assert port == 8883
    assert tls is True
