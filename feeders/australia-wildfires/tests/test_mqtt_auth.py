import os
import sys
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'australia_wildfires_mqtt')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'australia_wildfires_mqtt_producer', 'australia_wildfires_mqtt_producer_data', 'src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'australia_wildfires_mqtt_producer', 'australia_wildfires_mqtt_producer_mqtt_client', 'src')))

import australia_wildfires_mqtt.app as app


def test_resolve_mqtt_auth_entra_fetches_imds_token(monkeypatch):
    monkeypatch.setenv("MQTT_AUTH_MODE", "entra")
    monkeypatch.setenv("MQTT_ENTRA_AUDIENCE", "https://eventgrid.azure.net/")
    monkeypatch.setenv("MQTT_ENTRA_CLIENT_ID", "user-assigned-mi")
    monkeypatch.setenv("MQTT_CLIENT_ID", "managed-identity-object-id")

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self):
            return b'{"accessToken": "jwt-token"}'

    with patch("australia_wildfires_mqtt.app.urlopen", return_value=FakeResponse()) as open_mock:
        username, password = app._resolve_mqtt_auth(
            username=None,
            password=None,
            client_id=None,
            auth_mode="entra",
        )

    assert username == "managed-identity-object-id"
    assert password == "jwt-token"
    assert open_mock.call_count == 1
    request = open_mock.call_args[0][0]
    assert request.full_url.startswith("http://169.254.169.254/metadata/identity/oauth2/token?")
    assert "resource=https%3A%2F%2Feventgrid.azure.net%2F" in request.full_url
    assert "client_id=user-assigned-mi" in request.full_url


def test_resolve_mqtt_auth_password_mode_keeps_cli_credentials():
    username, password = app._resolve_mqtt_auth(
        username="broker-user",
        password="broker-pass",
        client_id="mqtt-client-id",
        auth_mode="password",
    )

    assert username == "broker-user"
    assert password == "broker-pass"
