"""Functional test of the downstream MQTT publish path.

This proves the *keep-structure* directive on the publish side: the generated
MQTT client, driven through the hand-written :class:`MqttSink`, mirrors the full
upstream HFP topic tree verbatim -- including the variable multi-level geohash
tail -- and carries the CloudEvents envelope as MQTT 5 user properties in binary
mode while leaving the HFP payload untouched in the message body.
"""

from __future__ import annotations

import json

from hsl_hfp_mqtt_producer_data import VehicleEvent
from hsl_hfp_mqtt_producer_mqtt_client.client import (
    FiHslGtfsOperatorMqttMqttClient,
    FiHslGtfsRouteMqttMqttClient,
    FiHslGtfsStopMqttMqttClient,
    FiHslHfpMqttMqttClient,
)
from hsl_hfp.mapping import vehicle_event_kwargs
from hsl_hfp_mqtt.app import MqttSink


VP_PAYLOAD = {
    "desi": "550", "dir": "1", "oper": 6, "veh": 117,
    "tst": "2024-05-01T08:30:01.000Z", "tsi": 1714552201,
    "spd": 12.3, "hdg": 117, "lat": 60.19, "long": 24.94, "route": "1059",
}

PARAMS = {
    "operator_id": "0055",
    "vehicle_number": "01216",
    "temporal_type": "ongoing",
    "transport_mode": "bus",
    "route_id": "1059",
    "direction_id": "1",
    "headsign": "Kamppi",
    "start_time": "08:30",
    "next_stop": "1284",
    "geohash_level": "4",
    "geohash": "60;24/19/73/44",
}

EXPECTED_TOPIC = (
    "hfp/v2/journey/ongoing/vp/bus/0055/01216/1059/1/"
    "Kamppi/08:30/1284/4/60;24/19/73/44"
)


class _FakeInfo:
    rc = 0
    mid = 1

    def wait_for_publish(self, timeout=None):
        return None

    def is_published(self):
        return True


class _FakePaho:
    def __init__(self):
        self.published = []

    def publish(self, topic, payload=None, qos=0, retain=False, properties=None):
        self.published.append({
            "topic": topic, "payload": payload, "qos": qos,
            "retain": retain, "properties": properties,
        })
        return _FakeInfo()


def _sink(content_mode="binary") -> tuple:
    fake = _FakePaho()
    tele = FiHslHfpMqttMqttClient(fake, content_mode=content_mode)
    operator = FiHslGtfsOperatorMqttMqttClient(fake, content_mode=content_mode)
    route = FiHslGtfsRouteMqttMqttClient(fake, content_mode=content_mode)
    stop = FiHslGtfsStopMqttMqttClient(fake, content_mode=content_mode)
    return MqttSink(tele, operator, route, stop,
                    "mqtts://mqtt.hsl.fi:8883/hfp/v2/journey"), fake


class TestDownstreamTopicMirrorsUpstream:
    def test_topic_mirrors_full_hfp_tree_with_geohash_slashes(self):
        sink, fake = _sink()
        sink.send_vehicle("vp", PARAMS, vehicle_event_kwargs(VP_PAYLOAD, PARAMS))
        assert len(fake.published) == 1
        assert fake.published[0]["topic"] == EXPECTED_TOPIC

    def test_binary_payload_preserves_hfp_fields(self):
        sink, fake = _sink("binary")
        sink.send_vehicle("vp", PARAMS, vehicle_event_kwargs(VP_PAYLOAD, PARAMS))
        payload = fake.published[0]["payload"]
        assert isinstance(payload, (bytes, bytearray))
        body = json.loads(payload.decode("utf-8"))
        for key, value in VP_PAYLOAD.items():
            assert body[key] == value

    def test_binary_mode_carries_cloudevents_user_properties(self):
        sink, fake = _sink("binary")
        sink.send_vehicle("vp", PARAMS, vehicle_event_kwargs(VP_PAYLOAD, PARAMS))
        props = fake.published[0]["properties"]
        user_props = dict(getattr(props, "UserProperty", []) or [])
        values = set(user_props.values())
        assert "fi.hsl.hfp.vp" in values          # CE type
        assert "0055/01216" in values             # CE subject == Kafka key


class TestReferenceTopic:
    def test_operator_reference_topic(self):
        from hsl_hfp_mqtt_producer_data import Operator
        sink, fake = _sink()
        kwargs = {f.name: None for f in __import__("dataclasses").fields(Operator)}
        kwargs["operator_id"] = "0055"
        kwargs["name"] = "Test Operator"
        sink.send_operator("0055", kwargs)
        assert fake.published[0]["topic"] == "hfp/v2/reference/operator/0055"
        assert fake.published[0]["retain"] is True
