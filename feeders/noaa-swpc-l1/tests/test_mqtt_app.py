from __future__ import annotations

import asyncio
from unittest import mock

import pytest

from noaa_swpc_l1_mqtt import app as mqtt_app


class FakePahoClient:
    def __init__(self, *args, **kwargs):
        self.credentials = None
        self.tls = False
        self.connected = None
        self.loop_started = False

    def username_pw_set(self, username, password):
        self.credentials = (username, password)

    def tls_set(self):
        self.tls = True

    def connect(self, host, port, keepalive=60, clean_start=True, properties=None):
        self.connected = (host, port, keepalive, clean_start, properties)

    def loop_start(self):
        self.loop_started = True

    def disconnect(self):
        pass


class FakeGeneratedMqttClient:
    instances: list["FakeGeneratedMqttClient"] = []

    def __init__(self, client, content_mode, loop):
        self.client = client
        self.content_mode = content_mode
        self.loop = loop
        self.connected = None
        self.published = []
        self.disconnected = False
        FakeGeneratedMqttClient.instances.append(self)

    async def connect(self, host, port):
        self.connected = (host, port)

    async def publish_gov_noaa_swpc_l1_mqtt_propagated_solar_wind(self, **kwargs):
        self.published.append(kwargs)

    async def disconnect(self):
        self.disconnected = True


@pytest.mark.unit
def test_parse_broker_url_extracts_auth_tls_and_path_defaults():
    assert mqtt_app._parse_broker_url("mqtts://user:pass@example.test:8884") == (
        "example.test",
        8884,
        True,
        "user",
        "pass",
    )
    assert mqtt_app._parse_broker_url("broker.test") == (
        "broker.test",
        1883,
        False,
        None,
        None,
    )


@pytest.mark.unit
def test_row_to_data_preserves_fields(sample_row):
    data = mqtt_app._row_to_data(sample_row)

    assert data.spacecraft.value == "dscovr"
    assert data.time_tag == sample_row.time_tag
    assert data.propagated_time_tag == sample_row.propagated_time_tag
    assert data.speed == sample_row.speed
    assert data.vz is None


@pytest.mark.unit
def test_main_parses_broker_url_and_invokes_feed(tmp_path):
    calls = []

    async def fake_feed(*args, **kwargs):
        calls.append((args, kwargs))

    with mock.patch.object(mqtt_app, "SwpcL1API", return_value=mock.Mock()), \
         mock.patch.object(mqtt_app, "feed", side_effect=fake_feed):
        mqtt_app.main([
            "feed",
            "--broker-url",
            "mqtts://user:pass@broker.test:8884",
            "--state-file",
            str(tmp_path / "state.json"),
            "--once",
        ])

    args, kwargs = calls[0]
    assert args[1:] == ("broker.test", 8884)
    assert kwargs["username"] == "user"
    assert kwargs["password"] == "pass"
    assert kwargs["tls"] is True
    assert kwargs["once"] is True


@pytest.mark.unit
def test_feed_once_publishes_row_and_saves_state(tmp_path, sample_row):
    FakeGeneratedMqttClient.instances.clear()
    api = mock.Mock()
    api.fetch_new_rows.return_value = [sample_row]
    paho = FakePahoClient()

    state_file = tmp_path / "state.json"
    with mock.patch.object(mqtt_app.mqtt, "Client", return_value=paho), \
         mock.patch.object(
             mqtt_app,
             "GovNoaaSwpcL1MqttMqttClient",
             FakeGeneratedMqttClient,
         ):
        asyncio.run(mqtt_app.feed(
            api,
            "broker.test",
            1883,
            spacecraft="dscovr",
            polling_interval=1,
            username="u",
            password="p",
            state_file=str(state_file),
            once=True,
            backfill_minutes=60,
        ))

    client = FakeGeneratedMqttClient.instances[0]
    assert paho.credentials == ("u", "p")
    assert client.connected == ("broker.test", 1883)
    assert client.disconnected is True
    assert len(client.published) == 1
    published = client.published[0]
    assert published["feedurl"] == mqtt_app.FEED_URL
    assert published["spacecraft"] == "dscovr"
    assert published["time_tag"] == sample_row.time_tag.isoformat()
    assert published["data"].speed == sample_row.speed
    assert mqtt_app.load_state(str(state_file))["last_time_tag"] == sample_row.time_tag.isoformat()
