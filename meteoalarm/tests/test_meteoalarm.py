"""Unit tests for the Meteoalarm bridge."""

import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from meteoalarm.meteoalarm import (
    MeteoalarmPoller,
    normalize_warning,
    parse_connection_string,
    _safe_str,
    _first_info,
    _collect_areas,
    _find_param,
)


# ── Helpers ──────────────────────────────────────────────────────────────────

def _make_alert(**overrides) -> dict:
    """Build a minimal valid Meteoalarm alert dict."""
    defaults = {
        "identifier": "2.49.0.0.276.0.DWD.PVW.12345.abc",
        "sender": "opendata@dwd.de",
        "sent": "2026-04-07T10:00:00+02:00",
        "status": "Actual",
        "msgType": "Alert",
        "scope": "Public",
        "info": [
            {
                "language": "de-DE",
                "category": ["Met"],
                "event": "STURMBÖEN",
                "severity": "Moderate",
                "urgency": "Immediate",
                "certainty": "Likely",
                "headline": "Amtliche WARNUNG vor STURMBÖEN",
                "description": "Es treten Sturmböen auf.",
                "instruction": "Sichern Sie lose Gegenstände.",
                "effective": "2026-04-07T10:00:00+02:00",
                "onset": "2026-04-07T12:00:00+02:00",
                "expires": "2026-04-07T20:00:00+02:00",
                "web": "https://www.dwd.de",
                "contact": "DWD",
                "parameter": [
                    {"valueName": "awareness_level", "value": "2; yellow; Moderate"},
                    {"valueName": "awareness_type", "value": "1; Wind"},
                ],
                "area": [
                    {
                        "areaDesc": "Kreis Bayreuth",
                        "geocode": [
                            {"valueName": "EMMA_ID", "value": "DE042"},
                            {"valueName": "WARNCELLID", "value": "909472999"},
                        ],
                    }
                ],
            }
        ],
    }
    defaults.update(overrides)
    return defaults


# ── Helpers tests ────────────────────────────────────────────────────────────

class TestSafeStr:
    def test_none(self):
        assert _safe_str(None) is None

    def test_empty(self):
        assert _safe_str("") is None

    def test_whitespace(self):
        assert _safe_str("  ") is None

    def test_value(self):
        assert _safe_str("hello") == "hello"

    def test_strip(self):
        assert _safe_str("  hi  ") == "hi"

    def test_number(self):
        assert _safe_str(42) == "42"


class TestFirstInfo:
    def test_empty_info(self):
        assert _first_info({"info": []}) is None

    def test_no_info_key(self):
        assert _first_info({}) is None

    def test_prefers_english(self):
        alert = {
            "info": [
                {"language": "de-DE", "event": "german"},
                {"language": "en-GB", "event": "english"},
            ]
        }
        assert _first_info(alert)["event"] == "english"

    def test_falls_back_to_first(self):
        alert = {"info": [{"language": "de-DE", "event": "german"}]}
        assert _first_info(alert)["event"] == "german"


class TestCollectAreas:
    def test_multiple_areas(self):
        info = {
            "area": [
                {"areaDesc": "A", "geocode": [{"value": "X1"}]},
                {"areaDesc": "B", "geocode": [{"value": "X2"}]},
            ]
        }
        desc, codes = _collect_areas(info)
        assert desc == "A; B"
        assert codes == "X1; X2"

    def test_empty_areas(self):
        desc, codes = _collect_areas({"area": []})
        assert desc == ""
        assert codes == ""

    def test_no_area_key(self):
        desc, codes = _collect_areas({})
        assert desc == ""
        assert codes == ""


class TestFindParam:
    def test_found(self):
        info = {"parameter": [{"valueName": "awareness_level", "value": "2; yellow; Moderate"}]}
        assert _find_param(info, "awareness_level") == "2; yellow; Moderate"

    def test_not_found(self):
        info = {"parameter": [{"valueName": "other", "value": "x"}]}
        assert _find_param(info, "awareness_level") is None

    def test_empty(self):
        assert _find_param({}, "awareness_level") is None


# ── Normalizer tests ────────────────────────────────────────────────────────

class TestNormalizeWarning:
    def test_valid_warning(self):
        w = normalize_warning(_make_alert(), "germany")
        assert w is not None
        assert w.identifier == "2.49.0.0.276.0.DWD.PVW.12345.abc"
        assert w.country == "germany"
        assert w.severity == "Moderate"
        assert w.urgency == "Immediate"
        assert w.event == "STURMBÖEN"
        assert w.awareness_level == "2; yellow; Moderate"
        assert w.awareness_type == "1; Wind"
        assert "Bayreuth" in w.area_desc
        assert "DE042" in w.geocodes
        assert w.msg_type == "Alert"

    def test_no_identifier(self):
        assert normalize_warning(_make_alert(identifier=None), "germany") is None

    def test_no_info(self):
        assert normalize_warning(_make_alert(info=[]), "germany") is None

    def test_no_severity(self):
        alert = _make_alert()
        alert["info"][0]["severity"] = None
        assert normalize_warning(alert, "germany") is None

    def test_no_event(self):
        alert = _make_alert()
        alert["info"][0]["event"] = None
        assert normalize_warning(alert, "germany") is None

    def test_with_english_preferred(self):
        alert = _make_alert()
        alert["info"].insert(0, {
            "language": "en-GB",
            "category": ["Met"],
            "event": "Storm Gusts",
            "severity": "Moderate",
            "urgency": "Immediate",
            "certainty": "Likely",
            "headline": "Official WARNING of STORM GUSTS",
            "area": [{"areaDesc": "Bavaria", "geocode": []}],
            "parameter": [],
        })
        w = normalize_warning(alert, "germany")
        assert w.event == "Storm Gusts"
        assert w.headline == "Official WARNING of STORM GUSTS"

    def test_cancel_message(self):
        w = normalize_warning(_make_alert(msgType="Cancel"), "france")
        assert w is not None
        assert w.msg_type == "Cancel"
        assert w.country == "france"


# ── Poller tests ─────────────────────────────────────────────────────────────

class TestPollerState:
    def test_load_empty_state(self, tmp_path):
        poller = MeteoalarmPoller(state_file=str(tmp_path / "state.json"))
        assert poller.load_state() == {}

    def test_save_and_load(self, tmp_path):
        sf = str(tmp_path / "state.json")
        poller = MeteoalarmPoller(state_file=sf)
        state = {"abc": "2026-04-07T10:00:00+02:00"}
        poller.save_state(state)
        assert poller.load_state() == state

    def test_corrupt_state(self, tmp_path):
        sf = str(tmp_path / "state.json")
        with open(sf, "w") as f:
            f.write("not json")
        poller = MeteoalarmPoller(state_file=sf)
        assert poller.load_state() == {}


class TestPollerPollAndSend:
    @pytest.mark.asyncio
    async def test_emits_new_warnings(self, tmp_path):
        sf = str(tmp_path / "state.json")
        poller = MeteoalarmPoller(
            state_file=sf, countries=["germany"],
        )
        poller.event_producer = MagicMock()
        poller.event_producer.send_meteoalarm_weather_warning = AsyncMock()
        poller.event_producer.producer = MagicMock()

        alert_data = [{"alert": _make_alert()}]

        with patch.object(poller, "fetch_country", new_callable=AsyncMock, return_value=alert_data):
            await poller.poll_and_send(once=True)

        poller.event_producer.send_meteoalarm_weather_warning.assert_called_once()
        poller.event_producer.producer.flush.assert_called_once()
        state = poller.load_state()
        assert "2.49.0.0.276.0.DWD.PVW.12345.abc" in state

    @pytest.mark.asyncio
    async def test_skips_already_seen(self, tmp_path):
        sf = str(tmp_path / "state.json")
        poller = MeteoalarmPoller(state_file=sf, countries=["germany"])
        poller.event_producer = MagicMock()
        poller.event_producer.send_meteoalarm_weather_warning = AsyncMock()
        poller.event_producer.producer = MagicMock()

        # Pre-populate state with same sent timestamp
        poller.save_state({"2.49.0.0.276.0.DWD.PVW.12345.abc": "2026-04-07T10:00:00+02:00"})

        alert_data = [{"alert": _make_alert()}]
        with patch.object(poller, "fetch_country", new_callable=AsyncMock, return_value=alert_data):
            await poller.poll_and_send(once=True)

        poller.event_producer.send_meteoalarm_weather_warning.assert_not_called()

    @pytest.mark.asyncio
    async def test_emits_updated_warning(self, tmp_path):
        sf = str(tmp_path / "state.json")
        poller = MeteoalarmPoller(state_file=sf, countries=["germany"])
        poller.event_producer = MagicMock()
        poller.event_producer.send_meteoalarm_weather_warning = AsyncMock()
        poller.event_producer.producer = MagicMock()

        # Old state has earlier timestamp
        poller.save_state({"2.49.0.0.276.0.DWD.PVW.12345.abc": "2026-04-06T10:00:00+02:00"})

        alert_data = [{"alert": _make_alert()}]
        with patch.object(poller, "fetch_country", new_callable=AsyncMock, return_value=alert_data):
            await poller.poll_and_send(once=True)

        poller.event_producer.send_meteoalarm_weather_warning.assert_called_once()

    @pytest.mark.asyncio
    async def test_handles_fetch_error(self, tmp_path):
        sf = str(tmp_path / "state.json")
        poller = MeteoalarmPoller(state_file=sf, countries=["germany"])
        poller.event_producer = MagicMock()
        poller.event_producer.send_meteoalarm_weather_warning = AsyncMock()
        poller.event_producer.producer = MagicMock()

        with patch.object(poller, "fetch_country", new_callable=AsyncMock, side_effect=Exception("network error")):
            await poller.poll_and_send(once=True)

        poller.event_producer.send_meteoalarm_weather_warning.assert_not_called()


# ── Connection string tests ──────────────────────────────────────────────────

class TestParseConnectionString:
    def test_event_hubs(self):
        cs = "Endpoint=sb://ns.servicebus.windows.net/;SharedAccessKeyName=policy;SharedAccessKey=key123;EntityPath=topic1"
        result = parse_connection_string(cs)
        assert "ns.servicebus.windows.net:9093" in result["bootstrap.servers"]
        assert result["kafka_topic"] == "topic1"
        assert result["sasl.username"] == "$ConnectionString"
        assert result["security.protocol"] == "SASL_SSL"

    def test_empty_returns_no_servers(self):
        result = parse_connection_string("")
        assert "bootstrap.servers" not in result
