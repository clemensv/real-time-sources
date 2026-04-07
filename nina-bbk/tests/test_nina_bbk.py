"""Tests for NINA/BBK bridge."""

import asyncio
import json
import os
import tempfile
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from nina_bbk.nina_bbk import (
    NINABBKPoller,
    _collect_areas,
    _find_event_code,
    _find_param,
    _first_info,
    _safe_str,
    normalize_warning,
    parse_connection_string,
)


# --- helpers ---

SAMPLE_MAP_STUB = {
    "id": "mow.DE-HE-DA-W184-20240723-000",
    "version": 5,
    "startDate": "2024-07-23T14:28:14+02:00",
    "severity": "Minor",
    "urgency": "Immediate",
    "type": "Alert",
    "i18nTitle": {"de": "Test Warning"},
    "transKeys": {"event": "BBK-EVC-067"},
}

SAMPLE_DETAIL = {
    "identifier": "mow.DE-HE-DA-W184-20240723-000",
    "sender": "DE-HE-DA-W184",
    "sent": "2024-07-23T14:28:14+02:00",
    "status": "Actual",
    "msgType": "Alert",
    "scope": "Public",
    "code": ["DVN:5"],
    "info": [
        {
            "language": "de",
            "category": ["Health"],
            "event": "Gefahreninformation",
            "urgency": "Immediate",
            "severity": "Minor",
            "certainty": "Observed",
            "eventCode": [
                {"valueName": "profile:DE-BBK-EVENTCODE", "value": "BBK-EVC-067"}
            ],
            "headline": "Betrieb Infotelefon",
            "description": "Test description text",
            "instruction": "Test instruction",
            "web": "www.darmstadt.de",
            "contact": "06151 / 115",
            "parameter": [
                {"valueName": "sender_langname", "value": "Integrierte Leitstelle Stadt Darmstadt"},
                {"valueName": "warnVerwaltungsbereiche", "value": "064110000000"},
            ],
            "area": [
                {
                    "areaDesc": "Stadt Darmstadt",
                    "geocode": [{"valueName": "AreaId", "value": "0"}],
                }
            ],
        }
    ],
}

SAMPLE_DETAIL_MULTILANG = {
    "identifier": "mow.DE-HE-KS-SE106-20260304-106-000",
    "sender": "DE-HE-KB-W195",
    "sent": "2026-03-04T10:32:16+01:00",
    "status": "Actual",
    "msgType": "Alert",
    "scope": "Public",
    "references": "DE-HE-KB-W195,mow.DE-HE-KB-W195-20260304-000,2026-03-04T09:30:49-00:00",
    "info": [
        {
            "language": "de",
            "category": ["Health"],
            "event": "Gefahreninformation",
            "urgency": "Immediate",
            "severity": "Minor",
            "certainty": "Observed",
            "eventCode": [{"valueName": "profile:DE-BBK-EVENTCODE", "value": "BBK-EVC-067"}],
            "headline": "Headline DE",
            "parameter": [
                {"valueName": "sender_langname", "value": "Leitstelle WF"},
                {"valueName": "warnVerwaltungsbereiche", "value": "066350001001"},
            ],
            "area": [{"areaDesc": "LK Waldeck-Frankenberg"}],
        },
        {
            "language": "EN",
            "category": ["Health"],
            "event": "Gefahreninformation",
            "urgency": "Immediate",
            "severity": "Minor",
            "certainty": "Observed",
            "headline": "Headline EN",
            "area": [{"areaDesc": "LK Waldeck-Frankenberg EN"}],
        },
    ],
}


# --- _safe_str ---

class TestSafeStr:
    def test_none(self):
        assert _safe_str(None) is None

    def test_empty(self):
        assert _safe_str("") is None

    def test_whitespace(self):
        assert _safe_str("  ") is None

    def test_value(self):
        assert _safe_str("hello") == "hello"

    def test_strips(self):
        assert _safe_str("  hello  ") == "hello"

    def test_int(self):
        assert _safe_str(42) == "42"


# --- _first_info ---

class TestFirstInfo:
    def test_empty_info(self):
        assert _first_info({"info": []}) is None

    def test_no_info_key(self):
        assert _first_info({}) is None

    def test_prefers_german(self):
        detail = {
            "info": [
                {"language": "EN", "event": "English"},
                {"language": "de", "event": "German"},
            ]
        }
        assert _first_info(detail)["event"] == "German"

    def test_prefers_de_de(self):
        detail = {
            "info": [
                {"language": "EN", "event": "English"},
                {"language": "de-DE", "event": "German DE"},
            ]
        }
        assert _first_info(detail)["event"] == "German DE"

    def test_falls_back_to_english(self):
        detail = {
            "info": [
                {"language": "FR", "event": "French"},
                {"language": "EN", "event": "English"},
            ]
        }
        assert _first_info(detail)["event"] == "English"

    def test_falls_back_to_first(self):
        detail = {
            "info": [
                {"language": "FR", "event": "French"},
                {"language": "PL", "event": "Polish"},
            ]
        }
        assert _first_info(detail)["event"] == "French"


# --- _find_param ---

class TestFindParam:
    def test_found(self):
        info = {"parameter": [
            {"valueName": "sender_langname", "value": "Leitstelle"},
        ]}
        assert _find_param(info, "sender_langname") == "Leitstelle"

    def test_not_found(self):
        info = {"parameter": [{"valueName": "other", "value": "x"}]}
        assert _find_param(info, "sender_langname") is None

    def test_empty(self):
        assert _find_param({}, "x") is None


# --- _find_event_code ---

class TestFindEventCode:
    def test_found(self):
        info = {"eventCode": [
            {"valueName": "profile:DE-BBK-EVENTCODE", "value": "BBK-EVC-067"},
        ]}
        assert _find_event_code(info) == "BBK-EVC-067"

    def test_not_found(self):
        info = {"eventCode": [{"valueName": "other", "value": "x"}]}
        assert _find_event_code(info) is None

    def test_no_key(self):
        assert _find_event_code({}) is None


# --- _collect_areas ---

class TestCollectAreas:
    def test_single_area(self):
        info = {"area": [{"areaDesc": "Stadt Darmstadt"}]}
        assert _collect_areas(info) == "Stadt Darmstadt"

    def test_multiple_areas(self):
        info = {"area": [{"areaDesc": "A"}, {"areaDesc": "B"}]}
        assert _collect_areas(info) == "A; B"

    def test_empty(self):
        assert _collect_areas({}) == ""

    def test_missing_desc(self):
        info = {"area": [{"geocode": []}]}
        assert _collect_areas(info) == ""


# --- normalize_warning ---

class TestNormalizeWarning:
    def test_basic(self):
        w = normalize_warning(SAMPLE_DETAIL, "mowas", 5)
        assert w is not None
        assert w.warning_id == "mow.DE-HE-DA-W184-20240723-000"
        assert w.provider == "mowas"
        assert w.version == 5
        assert w.sender == "DE-HE-DA-W184"
        assert w.status == "Actual"
        assert w.msg_type == "Alert"
        assert w.scope == "Public"
        assert w.event == "Gefahreninformation"
        assert w.event_code == "BBK-EVC-067"
        assert w.category == "Health"
        assert w.severity == "Minor"
        assert w.urgency == "Immediate"
        assert w.certainty == "Observed"
        assert w.headline == "Betrieb Infotelefon"
        assert w.description == "Test description text"
        assert w.instruction == "Test instruction"
        assert w.area_desc == "Stadt Darmstadt"
        assert w.verwaltungsbereiche == "064110000000"
        assert w.sender_name == "Integrierte Leitstelle Stadt Darmstadt"
        assert w.language == "de"

    def test_multilang_prefers_german(self):
        w = normalize_warning(SAMPLE_DETAIL_MULTILANG, "mowas", 12)
        assert w is not None
        assert w.headline == "Headline DE"
        assert w.references is not None

    def test_no_identifier(self):
        detail = {**SAMPLE_DETAIL, "identifier": None}
        assert normalize_warning(detail, "mowas") is None

    def test_no_info(self):
        detail = {**SAMPLE_DETAIL, "info": []}
        assert normalize_warning(detail, "mowas") is None

    def test_missing_required_fields(self):
        detail = dict(SAMPLE_DETAIL)
        detail = {**detail, "info": [{"language": "de", "event": "X"}]}
        assert normalize_warning(detail, "mowas") is None


# --- parse_connection_string ---

class TestParseConnectionString:
    def test_event_hubs(self):
        cs = "Endpoint=sb://ns.servicebus.windows.net/;SharedAccessKeyName=policy;SharedAccessKey=key123;EntityPath=topic1"
        result = parse_connection_string(cs)
        assert "bootstrap.servers" in result
        assert result["bootstrap.servers"] == "ns.servicebus.windows.net:9093"
        assert result["kafka_topic"] == "topic1"
        assert result["sasl.username"] == "$ConnectionString"

    def test_empty_returns_no_servers(self):
        result = parse_connection_string("")
        assert "bootstrap.servers" not in result


# --- NINABBKPoller state ---

class TestPollerState:
    def test_load_save_state(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("{}")
            tmp = f.name
        try:
            poller = NINABBKPoller(state_file=tmp)
            state = poller.load_state()
            assert state == {}
            state["test_id"] = "5"
            poller.save_state(state)
            state2 = poller.load_state()
            assert state2 == {"test_id": "5"}
        finally:
            os.unlink(tmp)

    def test_load_missing_file(self):
        poller = NINABBKPoller(state_file="/tmp/nonexistent_nina_state.json")
        assert poller.load_state() == {}


# --- NINABBKPoller poll_and_send ---

class TestPollerPollAndSend:
    @pytest.mark.asyncio
    async def test_poll_once_sends_new_warnings(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("{}")
            tmp = f.name

        try:
            poller = NINABBKPoller(state_file=tmp, providers=["mowas"])
            mock_producer = MagicMock()
            mock_event_producer = MagicMock()
            mock_event_producer.send_nina_civil_warning = AsyncMock()
            mock_event_producer.producer = mock_producer
            poller.event_producer = mock_event_producer

            async def mock_fetch_map(session, provider):
                return [SAMPLE_MAP_STUB]

            async def mock_fetch_detail(session, warning_id):
                return SAMPLE_DETAIL

            poller.fetch_map_data = mock_fetch_map
            poller.fetch_detail = mock_fetch_detail

            await poller.poll_and_send(once=True)

            mock_event_producer.send_nina_civil_warning.assert_called_once()
            call_kwargs = mock_event_producer.send_nina_civil_warning.call_args
            assert call_kwargs[1]["_warning_id"] == "mow.DE-HE-DA-W184-20240723-000"
            mock_producer.flush.assert_called_once()
        finally:
            os.unlink(tmp)

    @pytest.mark.asyncio
    async def test_poll_skips_seen_version(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"mow.DE-HE-DA-W184-20240723-000": "5"}, f)
            tmp = f.name

        try:
            poller = NINABBKPoller(state_file=tmp, providers=["mowas"])
            mock_producer = MagicMock()
            mock_event_producer = MagicMock()
            mock_event_producer.send_nina_civil_warning = AsyncMock()
            mock_event_producer.producer = mock_producer
            poller.event_producer = mock_event_producer

            async def mock_fetch_map(session, provider):
                return [SAMPLE_MAP_STUB]

            async def mock_fetch_detail(session, warning_id):
                return SAMPLE_DETAIL

            poller.fetch_map_data = mock_fetch_map
            poller.fetch_detail = mock_fetch_detail

            await poller.poll_and_send(once=True)

            mock_event_producer.send_nina_civil_warning.assert_not_called()
        finally:
            os.unlink(tmp)

    @pytest.mark.asyncio
    async def test_poll_sends_updated_version(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"mow.DE-HE-DA-W184-20240723-000": "3"}, f)
            tmp = f.name

        try:
            poller = NINABBKPoller(state_file=tmp, providers=["mowas"])
            mock_producer = MagicMock()
            mock_event_producer = MagicMock()
            mock_event_producer.send_nina_civil_warning = AsyncMock()
            mock_event_producer.producer = mock_producer
            poller.event_producer = mock_event_producer

            async def mock_fetch_map(session, provider):
                return [SAMPLE_MAP_STUB]

            async def mock_fetch_detail(session, warning_id):
                return SAMPLE_DETAIL

            poller.fetch_map_data = mock_fetch_map
            poller.fetch_detail = mock_fetch_detail

            await poller.poll_and_send(once=True)

            mock_event_producer.send_nina_civil_warning.assert_called_once()
        finally:
            os.unlink(tmp)

    @pytest.mark.asyncio
    async def test_poll_no_producer(self):
        """Test poll with no kafka producer (dry-run mode)."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("{}")
            tmp = f.name

        try:
            poller = NINABBKPoller(state_file=tmp, providers=["mowas"])

            async def mock_fetch_map(session, provider):
                return [SAMPLE_MAP_STUB]

            async def mock_fetch_detail(session, warning_id):
                return SAMPLE_DETAIL

            poller.fetch_map_data = mock_fetch_map
            poller.fetch_detail = mock_fetch_detail

            await poller.poll_and_send(once=True)

            state = poller.load_state()
            assert "mow.DE-HE-DA-W184-20240723-000" in state
        finally:
            os.unlink(tmp)

    @pytest.mark.asyncio
    async def test_poll_handles_detail_404(self):
        """Test that a missing detail (404) is gracefully skipped."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("{}")
            tmp = f.name

        try:
            poller = NINABBKPoller(state_file=tmp, providers=["mowas"])

            async def mock_fetch_map(session, provider):
                return [SAMPLE_MAP_STUB]

            async def mock_fetch_detail(session, warning_id):
                return None

            poller.fetch_map_data = mock_fetch_map
            poller.fetch_detail = mock_fetch_detail

            await poller.poll_and_send(once=True)

            state = poller.load_state()
            assert "mow.DE-HE-DA-W184-20240723-000" not in state
        finally:
            os.unlink(tmp)
