"""HFP payload mapping contract test.

The HSL bridge preserves upstream scalar values and maps non-Python HFP keys
such as ``tlp-requestid`` to stable schema property names such as
``tlp_requestid``. Codegen must not emit alternate JSON names for those fields:
the downstream CloudEvent wire contract is the xRegistry property name.
"""

from __future__ import annotations

import json

from hsl_hfp_producer_data import DriverBlockEvent, TrafficLightEvent, VehicleEvent
from hsl_hfp.mapping import (
    driver_block_event_kwargs,
    traffic_light_event_kwargs,
    vehicle_event_kwargs,
)


def _roundtrip(cls, kwargs) -> dict:
    raw = cls(**kwargs).to_byte_array("application/json")
    if isinstance(raw, str):
        raw = raw.encode("utf-8")
    return json.loads(raw.decode("utf-8"))


# A representative ``vp`` payload (digitransit HFP docs example shape). ``tsi``
# is kept inside int32 range (valid until 2038-01-19) so it round-trips as a
# JSON number rather than an int64 precision-safety string.
VP_PAYLOAD = {
    "desi": "550",
    "dir": "1",
    "oper": 6,
    "veh": 117,
    "tst": "2024-05-01T08:30:01.000Z",
    "tsi": 1714552201,
    "spd": 12.3,
    "hdg": 117,
    "lat": 60.19,
    "long": 24.94,
    "acc": 0.5,
    "dl": -30,
    "odo": 2819,
    "drst": 0,
    "oday": "2024-05-01",
    "jrn": 215,
    "line": 35,
    "start": "08:30",
    "loc": "GPS",
    "stop": 1284,
    "route": "1059",
    "occu": 0,
}

TLR_PAYLOAD = {
    "oper": 40,
    "veh": 123,
    "tst": "2024-05-01T12:05:11.000Z",
    "tsi": 1714564711,
    "spd": 0.0,
    "hdg": 88,
    "lat": 60.20,
    "long": 24.93,
    "acc": 0.0,
    "dl": 0,
    "loc": "GPS",
    "tlp-requestid": 5,
    "tlp-requesttype": "NORMAL",
    "tlp-prioritylevel": "normal",
    "tlp-reason": "GLOBAL",
    "sid": 255,
    "signal-groupid": 3,
    "tlp-decision": "ACK",
}

DA_PAYLOAD = {
    "oper": 50,
    "veh": 401,
    "tst": "2024-05-01T05:00:00.000Z",
    "tsi": 1714539600,
    "spd": 0.0,
    "hdg": 0,
    "lat": 60.17,
    "long": 24.95,
    "acc": 0.0,
    "loc": "GPS",
    "oday": "2024-05-01",
    "dr-type": 1,
}


def _assert_present_keys_preserved(payload: dict, serialized: dict) -> None:
    for key, value in payload.items():
        wire_key = key.replace("-", "_")
        assert wire_key in serialized, f"wire key {wire_key!r} dropped"
        assert serialized[wire_key] == value, (
            f"value for {wire_key!r} changed: {serialized[wire_key]!r} != {value!r}"
        )


class TestVerbatimRoundtrip:
    def test_vp_payload_preserved(self):
        serialized = _roundtrip(VehicleEvent, vehicle_event_kwargs(VP_PAYLOAD, {}))
        _assert_present_keys_preserved(VP_PAYLOAD, serialized)

    def test_vp_absent_optionals_are_null(self):
        serialized = _roundtrip(VehicleEvent, vehicle_event_kwargs(VP_PAYLOAD, {}))
        # `seq` (metro only) and `label` (ferry only) were not in the payload.
        assert serialized["seq"] is None
        assert serialized["label"] is None

    def test_tlr_payload_preserved_including_hyphenated_keys(self):
        serialized = _roundtrip(
            TrafficLightEvent, traffic_light_event_kwargs(TLR_PAYLOAD, {}))
        _assert_present_keys_preserved(TLR_PAYLOAD, serialized)
        # Spot-check the upstream->schema remap explicitly.
        assert serialized["tlp_requestid"] == 5
        assert serialized["signal_groupid"] == 3

    def test_da_payload_preserved(self):
        serialized = _roundtrip(
            DriverBlockEvent, driver_block_event_kwargs(DA_PAYLOAD, {}))
        _assert_present_keys_preserved(DA_PAYLOAD, serialized)
        assert serialized["dr_type"] == 1


# Parsed HFP topic levels (see hfp_source.parse_topic). These become real schema
# fields so the CloudEvents subject / Kafka key {operator_id}/{vehicle_number}
# resolves from data carried on the event itself.
VP_PARAMS = {
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


class TestTopicIdentityFields:
    def test_topic_levels_serialize_onto_the_event(self):
        serialized = _roundtrip(VehicleEvent, vehicle_event_kwargs(VP_PAYLOAD, VP_PARAMS))
        for key, value in VP_PARAMS.items():
            assert serialized[key] == value, f"topic field {key!r} not preserved"
        # The payload fields are still preserved verbatim alongside them.
        _assert_present_keys_preserved(VP_PAYLOAD, serialized)

    def test_required_identity_present_optional_levels_null_when_absent(self):
        # da/dout/ba/bout topics carry the required identity but leave the
        # journey-context levels empty; absent params materialize as JSON null.
        serialized = _roundtrip(VehicleEvent, vehicle_event_kwargs(
            VP_PAYLOAD, {"operator_id": "0055", "vehicle_number": "01216",
                         "temporal_type": "ongoing", "transport_mode": "bus"}))
        assert serialized["operator_id"] == "0055"
        assert serialized["vehicle_number"] == "01216"
        assert serialized["route_id"] is None
        assert serialized["geohash"] is None
