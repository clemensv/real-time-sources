"""Tests for the upstream HFP topic parser and payload unwrapper.

These lock down the *acquisition* contract: the bridge derives the stable
``operator_id``/``vehicle_number`` key from the **topic** (never the mutable
payload ``oper``), joins the variable multi-level geohash tail verbatim, and
peels the trailing junction id (``sid``) off ``tlr``/``tla`` topics.
"""

from __future__ import annotations

from hsl_hfp.hfp_source import parse_topic, unwrap_payload


VP_TOPIC = (
    "/hfp/v2/journey/ongoing/vp/bus/0055/01216/1059/1/"
    "Kamppi/08:30/1284/4/60;24/19/73/44"
)
TLR_TOPIC = (
    "/hfp/v2/journey/ongoing/tlr/tram/0040/00123/1007/2/"
    "Pasila/12:05/1130/4/60;24/19/73/44/255"
)


class TestParseTopic:
    def test_vp_extracts_vehicle_identity_from_topic(self):
        parsed = parse_topic(VP_TOPIC)
        assert parsed is not None
        event_type, params = parsed
        assert event_type == "vp"
        # Identity comes from the topic, zero-padded, NOT from payload `oper`.
        assert params["operator_id"] == "0055"
        assert params["vehicle_number"] == "01216"

    def test_vp_head_levels_are_named(self):
        _, params = parse_topic(VP_TOPIC)
        assert params["temporal_type"] == "ongoing"
        assert params["transport_mode"] == "bus"
        assert params["route_id"] == "1059"
        assert params["direction_id"] == "1"
        assert params["headsign"] == "Kamppi"
        assert params["start_time"] == "08:30"
        assert params["next_stop"] == "1284"
        assert params["geohash_level"] == "4"

    def test_multi_level_geohash_tail_joined_verbatim(self):
        _, params = parse_topic(VP_TOPIC)
        # The geohash is the integer pair plus the interleaved fractional
        # levels, rejoined with '/' exactly as it arrived.
        assert params["geohash"] == "60;24/19/73/44"

    def test_tlr_peels_trailing_sid_off_geohash(self):
        event_type, params = parse_topic(TLR_TOPIC)
        assert event_type == "tlr"
        assert params["sid"] == "255"
        # sid must not bleed into the geohash tail.
        assert params["geohash"] == "60;24/19/73/44"

    def test_non_journey_topic_returns_none(self):
        assert parse_topic("/hfp/v2/deadrun/ongoing/vp/bus") is None

    def test_short_topic_returns_none(self):
        assert parse_topic("/hfp/v2/journey/ongoing") is None


class TestUnwrapPayload:
    def test_unwraps_single_key_event_wrapper(self):
        raw = b'{"VP": {"oper": 55, "veh": 1216, "spd": 8.1}}'
        inner = unwrap_payload(raw)
        assert inner == {"oper": 55, "veh": 1216, "spd": 8.1}

    def test_invalid_json_returns_none(self):
        assert unwrap_payload(b"not json") is None

    def test_non_object_returns_none(self):
        assert unwrap_payload(b"[1, 2, 3]") is None
