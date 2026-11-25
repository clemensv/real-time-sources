import base64
import json
import sys
import time
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from usgs_waterdata_core.delivery import AcknowledgedKafkaProducer, fabric_kafka_config


@pytest.mark.parametrize("error,callback,remaining", [("rejected", True, 0), (None, False, 0), (None, True, 1)])
def test_failed_or_missing_kafka_delivery_is_visible(error, callback, remaining):
    raw = Mock()
    producer = AcknowledgedKafkaProducer(raw)
    producer.produce("topic", value=b"data")
    if callback:
        raw.produce.call_args.kwargs["on_delivery"](error, object())
    raw.flush.return_value = remaining
    with pytest.raises(RuntimeError, match="Kafka delivery failed"):
        producer.flush()


def test_success_requires_callback_and_empty_flush():
    raw = Mock()
    producer = AcknowledgedKafkaProducer(raw)
    producer.produce("topic", value=b"data")
    raw.produce.call_args.kwargs["on_delivery"](None, object())
    raw.flush.return_value = 0
    assert producer.flush() == 0


def _token(claims):
    payload = base64.urlsafe_b64encode(json.dumps(claims).encode()).decode().rstrip("=")
    return "synthetic." + payload + ".signature"


def test_fabric_oauth_refreshes_tokens_and_preserves_default_config(monkeypatch):
    config = {"bootstrap.servers": "synthetic.servicebus.windows.net:9093", "security.protocol": "SSL"}
    monkeypatch.delenv("KAFKA_AUTH_MODE", raising=False)
    assert fabric_kafka_config(config) == config
    expiry = int(time.time()) + 3600
    tokens = [_token({"aud": "https://synthetic.servicebus.windows.net/", "exp": expiry}),
              _token({"aud": "https://synthetic.servicebus.windows.net", "exp": expiry + 3600})]
    credential = Mock(side_effect=tokens)
    monkeypatch.setitem(sys.modules, "notebookutils", SimpleNamespace(
        credentials=SimpleNamespace(getToken=credential)))
    monkeypatch.setenv("KAFKA_AUTH_MODE", "fabric-entra")
    result = fabric_kafka_config(config)
    assert result["sasl.mechanism"] == "OAUTHBEARER"
    assert result["security.protocol"] == "SASL_SSL"
    assert result["oauth_cb"]("") == (tokens[0], float(expiry))
    assert result["oauth_cb"]("") == (tokens[1], float(expiry + 3600))
    assert credential.call_count == 2
    credential.assert_called_with("https://synthetic.servicebus.windows.net/")
    assert config == {"bootstrap.servers": "synthetic.servicebus.windows.net:9093", "security.protocol": "SSL"}


@pytest.mark.parametrize("claims", [
    {"aud": "https://storage.azure.com/", "exp": 9999999999},
    {"aud": "https://eventhubs.azure.net/", "exp": 9999999999},
    {"aud": "https://synthetic.servicebus.windows.net/", "exp": 1},
    {"aud": "https://synthetic.servicebus.windows.net/", "exp": True},
    {"aud": "https://synthetic.servicebus.windows.net/", "exp": float("inf")},
    {"aud": "https://synthetic.servicebus.windows.net/"},
])
def test_fabric_oauth_rejects_wrong_audience_and_invalid_expiration(monkeypatch, claims):
    monkeypatch.setenv("KAFKA_AUTH_MODE", "fabric-entra")
    monkeypatch.setitem(sys.modules, "notebookutils", SimpleNamespace(
        credentials=SimpleNamespace(getToken=lambda audience: _token(claims))))
    callback = fabric_kafka_config({"security.protocol": "SSL",
                                    "bootstrap.servers": "synthetic.servicebus.windows.net:9093"})["oauth_cb"]
    with pytest.raises(ValueError, match="NotebookUtils"):
        callback("")


@pytest.mark.parametrize("config", [
    {"security.protocol": "PLAINTEXT"},
    {"security.protocol": "SASL_PLAINTEXT"},
    {"security.protocol": "SASL_SSL", "sasl.username": "$ConnectionString", "sasl.password": "synthetic"},
])
def test_fabric_oauth_rejects_plaintext_and_password_fallback(monkeypatch, config):
    monkeypatch.setenv("KAFKA_AUTH_MODE", "fabric-entra")
    with pytest.raises(ValueError, match="Fabric Entra"):
        fabric_kafka_config(config)
