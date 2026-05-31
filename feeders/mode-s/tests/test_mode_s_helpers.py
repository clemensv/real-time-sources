import pytest

from mode_s_amqp.app import (
    _decode_rssi as decode_rssi_amqp,
    _norm_segment as norm_segment_amqp,
    _parse_amqp_broker_url,
)
from mode_s_mqtt.app import (
    _decode_rssi as decode_rssi_mqtt,
    _hex_icao,
    _norm_segment as norm_segment_mqtt,
    _parse_broker,
)


@pytest.mark.parametrize("normalizer", [norm_segment_mqtt, norm_segment_amqp])
def test_norm_segment_normalizes_topic_and_subject_fragments(normalizer):
    assert normalizer(" AB/CD+# ") == "ab_cd__"
    assert normalizer(None) == ""


def test_hex_icao_uses_same_normalization():
    assert _hex_icao("A0/B1+#") == "a0_b1__"
    assert _hex_icao(None) == ""


@pytest.mark.parametrize("decoder", [decode_rssi_mqtt, decode_rssi_amqp])
def test_decode_rssi_handles_short_and_valid_frames(decoder):
    assert decoder(b"\x00\x01\x02") is None
    assert decoder(b"\x00\x00\x00\x00\x00\x00\x80") == pytest.approx(-6.0, abs=0.05)


def test_parse_broker_applies_default_scheme_and_ports():
    assert _parse_broker("broker.example") == ("broker.example", 1883, False)
    assert _parse_broker("mqtts://broker.example:8884") == ("broker.example", 8884, True)


def test_parse_amqp_broker_url_extracts_auth_and_address():
    assert _parse_amqp_broker_url("broker.example") == ("broker.example", 5672, False, None, None, None)
    assert _parse_amqp_broker_url("amqps://user:pass@broker.example:5678/mode-s") == (
        "broker.example",
        5678,
        True,
        "user",
        "pass",
        "mode-s",
    )
