"""Tests for the ``pegelonline_mqtt`` feeder.

We do not run a real broker here — the generated MQTT client publishes via
``client.publish(...)`` on its underlying paho instance, so we substitute a
fake paho client that records every publish call and let the feeder run
exactly one polling cycle in ``--once`` mode.
"""

from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Tuple
from unittest import mock

import pytest

from pegelonline_mqtt import app as mqtt_app


class FakeMQTTMessageInfo:
    def __init__(self):
        self.rc = 0
        self.mid = 1

    def wait_for_publish(self, timeout: float = 1.0) -> None:
        return None


class FakePahoClient:
    """A minimal stand-in for paho.mqtt.client.Client.

    Captures every publish() call so tests can assert topic/qos/retain plus
    MQTT 5 user-property mapping for binary-mode CloudEvents.
    """

    def __init__(self, *args, **kwargs):
        self.publishes: List[Dict[str, Any]] = []
        self._on_connect = None
        self._on_disconnect = None
        self._connect_args: Tuple = ()
        self._user_data = None

    def username_pw_set(self, username, password):
        self._creds = (username, password)

    def tls_set(self, *args, **kwargs):
        self._tls = True

    def user_data_set(self, data):
        self._user_data = data

    @property
    def on_connect(self):
        return self._on_connect

    @on_connect.setter
    def on_connect(self, value):
        self._on_connect = value

    @property
    def on_disconnect(self):
        return self._on_disconnect

    @on_disconnect.setter
    def on_disconnect(self, value):
        self._on_disconnect = value

    def connect(self, host, port, keepalive=60):
        self._connect_args = (host, port, keepalive)
        if self._on_connect:
            try:
                self._on_connect(self, self._user_data, {}, 0, None)
            except TypeError:
                self._on_connect(self, self._user_data, {}, 0)

    def loop_start(self):
        pass

    def loop_stop(self):
        pass

    def disconnect(self):
        if self._on_disconnect:
            try:
                self._on_disconnect(self, self._user_data, 0, None)
            except TypeError:
                self._on_disconnect(self, self._user_data, 0)

    def publish(self, topic, payload=None, qos=0, retain=False, properties=None):
        self.publishes.append({
            "topic": topic,
            "payload": payload,
            "qos": qos,
            "retain": retain,
            "properties": properties,
        })
        return FakeMQTTMessageInfo()


def _user_properties(props) -> Dict[str, str]:
    if props is None:
        return {}
    user = getattr(props, "UserProperty", None) or []
    return {k: v for k, v in user}


@pytest.mark.unit
def test_water_shortname_sanitization():
    assert mqtt_app._water_shortname({"water": {"shortname": "RHEIN"}}) == "rhein"
    assert mqtt_app._water_shortname({"water": {"shortname": "ELBE-SEITENKANAL"}}) == "elbe-seitenkanal"
    assert mqtt_app._water_shortname({"water": {"shortname": "MAIN / RHEIN"}}) == "main-rhein"
    assert mqtt_app._water_shortname({"water": {}}) == "unknown"


@pytest.mark.unit
def test_mqtt_feed_publishes_station_and_measurement(tmp_path):
    fake = FakePahoClient()
    api = mock.Mock()
    api.list_stations.return_value = [{
        "uuid": "STATION-1",
        "number": "1",
        "shortname": "MAXAU",
        "longname": "MAXAU",
        "km": 362.3,
        "agency": "WSV",
        "longitude": 8.31,
        "latitude": 49.01,
        "water": {"shortname": "RHEIN", "longname": "RHEIN"},
    }]
    api.get_water_levels.return_value = {
        "STATION-1": {
            "timestamp": "2024-01-15T12:00:00+01:00",
            "value": 450,
            "stateMnwMhw": "normal",
            "stateNswHsw": "unknown",
        }
    }

    with mock.patch("pegelonline_mqtt.app.mqtt.Client", return_value=fake):
        asyncio.run(mqtt_app.feed(
            api=api,
            broker_host="localhost",
            broker_port=1883,
            polling_interval=1,
            state_file=str(tmp_path / "state.json"),
            once=True,
        ))

    topics = [p["topic"] for p in fake.publishes]
    assert "hydro/de/wsv/pegelonline/rhein/STATION-1/info" in topics
    assert "hydro/de/wsv/pegelonline/rhein/STATION-1/water-level" in topics

    measurement_pub = next(p for p in fake.publishes if p["topic"].endswith("/water-level"))
    assert measurement_pub["qos"] == 1
    assert measurement_pub["retain"] is True

    headers = _user_properties(measurement_pub["properties"])
    assert headers.get("type") == "de.wsv.pegelonline.CurrentMeasurement"
    assert headers.get("subject") == "STATION-1"
    assert "id" in headers and "source" in headers and "time" in headers
