"""Unit tests for the NWS CAP alerts bridge."""

import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from nws_alerts.nws_alerts import (
    NWSAlertsPoller,
    normalize_alert,
    parse_connection_string,
    _safe_str,
    _join_codes,
    _find_nws_headline,
    _find_vtec,
)


def _make_props(**overrides) -> dict:
    """Build a minimal valid NWS alert properties dict."""
    defaults = {
        "id": "urn:oid:2.49.0.1.840.0.abc123",
        "areaDesc": "Montgomery",
        "geocode": {"SAME": ["024031"], "UGC": ["MDC031"]},
        "sent": "2026-04-07T10:00:00+00:00",
        "effective": "2026-04-07T10:00:00+00:00",
        "onset": "2026-04-07T12:00:00+00:00",
        "expires": "2026-04-07T20:00:00+00:00",
        "ends": "2026-04-07T22:00:00+00:00",
        "status": "Actual",
        "messageType": "Alert",
        "category": "Met",
        "severity": "Severe",
        "certainty": "Likely",
        "urgency": "Immediate",
        "event": "Tornado Warning",
        "sender": "w-nws.webmaster@noaa.gov",
        "senderName": "NWS Tulsa OK",
        "headline": "Tornado Warning for Montgomery County",
        "description": "A tornado warning has been issued.",
        "instruction": "Take shelter immediately.",
        "response": "Shelter",
        "scope": "Public",
        "code": "IPAWSv1.0",
        "web": "http://www.weather.gov",
        "parameters": {
            "NWSheadline": ["Tornado Warning"],
            "VTEC": ["/O.NEW.KTSA.TO.W.0001.260407T1200Z-260407T2200Z/"],
        },
    }
    defaults.update(overrides)
    return defaults


class TestSafeStr:
    def test_none(self):
        assert _safe_str(None) is None

    def test_empty(self):
        assert _safe_str("") is None

    def test_value(self):
        assert _safe_str("hello") == "hello"


class TestJoinCodes:
    def test_join(self):
        assert _join_codes({"SAME": ["1", "2", "3"]}, "SAME") == "1; 2; 3"

    def test_missing_key(self):
        assert _join_codes({"SAME": ["1"]}, "UGC") is None

    def test_none_geocode(self):
        assert _join_codes(None, "SAME") is None

    def test_empty_list(self):
        assert _join_codes({"SAME": []}, "SAME") is None


class TestFindNwsHeadline:
    def test_found(self):
        assert _find_nws_headline({"NWSheadline": ["Test"]}) == "Test"

    def test_not_found(self):
        assert _find_nws_headline({"other": "x"}) is None

    def test_none(self):
        assert _find_nws_headline(None) is None


class TestFindVtec:
    def test_found(self):
        assert _find_vtec({"VTEC": ["/O.NEW.KTSA.TO.W.0001/"]}) == "/O.NEW.KTSA.TO.W.0001/"

    def test_not_found(self):
        assert _find_vtec({}) is None


class TestNormalizeAlert:
    def test_valid(self):
        a = normalize_alert(_make_props())
        assert a is not None
        assert a.alert_id == "urn:oid:2.49.0.1.840.0.abc123"
        assert a.event == "Tornado Warning"
        assert a.severity == "Severe"
        assert a.same_codes == "024031"
        assert a.ugc_codes == "MDC031"
        assert a.vtec == "/O.NEW.KTSA.TO.W.0001.260407T1200Z-260407T2200Z/"
        assert a.nws_headline == "Tornado Warning"

    def test_no_id(self):
        assert normalize_alert(_make_props(id=None)) is None

    def test_no_event(self):
        assert normalize_alert(_make_props(event=None)) is None

    def test_no_severity(self):
        assert normalize_alert(_make_props(severity=None)) is None

    def test_minimal(self):
        a = normalize_alert({
            "id": "urn:oid:123",
            "event": "Test",
            "severity": "Minor",
            "urgency": "Unknown",
            "certainty": "Unknown",
            "sent": "2026-04-07T00:00:00Z",
            "status": "Actual",
            "messageType": "Alert",
        })
        assert a is not None
        assert a.alert_id == "urn:oid:123"
        assert a.same_codes is None
        assert a.vtec is None


class TestPollerState:
    def test_empty(self, tmp_path):
        p = NWSAlertsPoller(state_file=str(tmp_path / "s.json"))
        assert p.load_state() == {}

    def test_save_load(self, tmp_path):
        sf = str(tmp_path / "s.json")
        p = NWSAlertsPoller(state_file=sf)
        p.save_state({"a": "b"})
        assert p.load_state() == {"a": "b"}


class TestPollerPollAndSend:
    @pytest.mark.asyncio
    async def test_emits_new(self, tmp_path):
        poller = NWSAlertsPoller(state_file=str(tmp_path / "s.json"))
        poller.event_producer = MagicMock()
        poller.event_producer.send_nws_weather_alert = AsyncMock()
        poller.event_producer.producer = MagicMock()

        features = [{"properties": _make_props()}]
        with patch.object(poller, "fetch_alerts", new_callable=AsyncMock, return_value=features):
            await poller.poll_and_send(once=True)

        poller.event_producer.send_nws_weather_alert.assert_called_once()

    @pytest.mark.asyncio
    async def test_skips_seen(self, tmp_path):
        sf = str(tmp_path / "s.json")
        poller = NWSAlertsPoller(state_file=sf)
        poller.save_state({"urn:oid:2.49.0.1.840.0.abc123": "2026-04-07T10:00:00+00:00"})
        poller.event_producer = MagicMock()
        poller.event_producer.send_nws_weather_alert = AsyncMock()
        poller.event_producer.producer = MagicMock()

        features = [{"properties": _make_props()}]
        with patch.object(poller, "fetch_alerts", new_callable=AsyncMock, return_value=features):
            await poller.poll_and_send(once=True)

        poller.event_producer.send_nws_weather_alert.assert_not_called()

    @pytest.mark.asyncio
    async def test_handles_error(self, tmp_path):
        poller = NWSAlertsPoller(state_file=str(tmp_path / "s.json"))
        poller.event_producer = MagicMock()
        poller.event_producer.send_nws_weather_alert = AsyncMock()
        poller.event_producer.producer = MagicMock()

        with patch.object(poller, "fetch_alerts", new_callable=AsyncMock, side_effect=Exception("fail")):
            await poller.poll_and_send(once=True)

        poller.event_producer.send_nws_weather_alert.assert_not_called()


class TestParseConnectionString:
    def test_event_hubs(self):
        cs = "Endpoint=sb://ns.servicebus.windows.net/;SharedAccessKeyName=p;SharedAccessKey=k;EntityPath=t"
        r = parse_connection_string(cs)
        assert "ns.servicebus.windows.net:9093" in r["bootstrap.servers"]
        assert r["kafka_topic"] == "t"
