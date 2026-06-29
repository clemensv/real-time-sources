"""Tests for the payload-to-data-class field mappers.

The mapper is the single place that enumerates every schema field, so its
contract is: the kwargs it returns must cover **exactly** the fields of the
generated data class -- no missing field (which would raise ``TypeError`` at
construction, since the generated fields are keyword-only with no default) and
no stray key. It must also remap the hyphenated wire keys (``dr-type``,
``tlp-requestid`` ...) onto the sanitized Python field names and fill absent
optionals with ``None``.
"""

from __future__ import annotations

import dataclasses

from hsl_hfp_producer_data import DriverBlockEvent, TrafficLightEvent, VehicleEvent
from hsl_hfp.mapping import (
    driver_block_event_kwargs,
    traffic_light_event_kwargs,
    vehicle_event_kwargs,
)


def _field_names(cls) -> set:
    return {f.name for f in dataclasses.fields(cls)}


class TestKwargsCoverFields:
    def test_vehicle_event_kwargs_cover_all_fields(self):
        kwargs = vehicle_event_kwargs({}, {})
        assert set(kwargs) == _field_names(VehicleEvent)
        # Must construct without TypeError (every kw-only field supplied).
        VehicleEvent(**kwargs)

    def test_traffic_light_event_kwargs_cover_all_fields(self):
        kwargs = traffic_light_event_kwargs({}, {})
        assert set(kwargs) == _field_names(TrafficLightEvent)
        TrafficLightEvent(**kwargs)

    def test_driver_block_event_kwargs_cover_all_fields(self):
        kwargs = driver_block_event_kwargs({}, {})
        assert set(kwargs) == _field_names(DriverBlockEvent)
        DriverBlockEvent(**kwargs)


class TestWireKeyRemap:
    def test_vehicle_dr_type_from_hyphenated_wire_key(self):
        kwargs = vehicle_event_kwargs({"dr-type": 100}, {})
        assert kwargs["dr_type"] == 100

    def test_traffic_light_hyphenated_keys_remapped(self):
        payload = {
            "tlp-requestid": 7,
            "tlp-requesttype": "NORMAL",
            "signal-groupid": 42,
            "tlp-decision": "ACK",
        }
        kwargs = traffic_light_event_kwargs(payload, {})
        assert kwargs["tlp_requestid"] == 7
        assert kwargs["tlp_requesttype"] == "NORMAL"
        assert kwargs["signal_groupid"] == 42
        assert kwargs["tlp_decision"] == "ACK"


class TestAbsentOptionalsNullFilled:
    def test_absent_vehicle_fields_are_none(self):
        kwargs = vehicle_event_kwargs({"oper": 55, "veh": 1216}, {})
        assert kwargs["oper"] == 55
        assert kwargs["veh"] == 1216
        # Everything the payload omitted is explicitly None.
        assert kwargs["lat"] is None
        assert kwargs["occu"] is None
        assert kwargs["dr_type"] is None


class TestTrafficLightSidFallback:
    def test_sid_taken_from_payload_when_present(self):
        kwargs = traffic_light_event_kwargs({"sid": 99}, {"sid": "255"})
        assert kwargs["sid"] == 99

    def test_sid_falls_back_to_topic_level(self):
        kwargs = traffic_light_event_kwargs({}, {"sid": "255"})
        assert kwargs["sid"] == 255

    def test_sid_none_when_absent_everywhere(self):
        kwargs = traffic_light_event_kwargs({}, {})
        assert kwargs["sid"] is None
