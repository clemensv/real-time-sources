"""Unit tests for the Wikimedia EventStreams bridge."""

from pathlib import Path
from unittest.mock import MagicMock, patch

from wikimedia_eventstreams.wikimedia_eventstreams import (
    BridgeState,
    StateStore,
    WikimediaRecentChangeBridge,
    build_stream_url,
    normalize_recent_change,
    parse_connection_string,
)


SAMPLE_EVENT = {
    "$schema": "/mediawiki/recentchange/1.0.0",
    "meta": {
        "uri": "https://www.wikidata.org/wiki/Lexeme:L236207",
        "request_id": "12c47e2c-f5b8-4b72-9747-34ef82dcc475",
        "id": "ded39d54-8ad6-43bd-baf5-8b06c2607a56",
        "domain": "www.wikidata.org",
        "stream": "mediawiki.recentchange",
        "topic": "eqiad.mediawiki.recentchange",
        "partition": 0,
        "offset": 6002030074,
        "dt": "2026-04-07T10:57:48.160Z",
    },
    "id": 2555986212,
    "type": "edit",
    "namespace": 146,
    "title": "Lexeme:L236207",
    "title_url": "https://www.wikidata.org/wiki/Lexeme:L236207",
    "comment": "changed page",
    "timestamp": 1775559467,
    "user": "Vesihiisi",
    "bot": False,
    "minor": False,
    "patrolled": True,
    "length": {"old": 4191, "new": 4467},
    "revision": {"old": 2479093568, "new": 2479093572},
    "server_url": "https://www.wikidata.org",
    "server_name": "www.wikidata.org",
    "server_script_path": "/w",
    "wiki": "wikidatawiki",
    "parsedcomment": "<span>changed</span>",
    "notify_url": "https://www.wikidata.org/w/index.php?diff=2479093572&oldid=2479093568&rcid=2555986212",
}


class TestConnectionString:
    def test_event_hubs_connection_string(self) -> None:
        result = parse_connection_string(
            "Endpoint=sb://namespace.servicebus.windows.net/;"
            "SharedAccessKeyName=Root;"
            "SharedAccessKey=secret;"
            "EntityPath=topic"
        )
        assert result["bootstrap.servers"] == "namespace.servicebus.windows.net:9093"
        assert result["kafka_topic"] == "topic"
        assert result["sasl.username"] == "$ConnectionString"
        assert result["security.protocol"] == "SASL_SSL"

    def test_plain_bootstrap_server_connection_string(self) -> None:
        result = parse_connection_string("BootstrapServer=localhost:9092;EntityPath=topic")
        assert result["bootstrap.servers"] == "localhost:9092"
        assert result["kafka_topic"] == "topic"


class TestHelpers:
    def test_build_stream_url_without_since(self) -> None:
        assert build_stream_url("https://example.invalid/stream", None) == "https://example.invalid/stream"

    def test_build_stream_url_with_since(self) -> None:
        assert (
            build_stream_url("https://example.invalid/stream", "2026-04-07T10:57:48.160Z")
            == "https://example.invalid/stream?since=2026-04-07T10%3A57%3A48.160Z"
        )

    def test_normalize_recent_change_renames_schema_and_log_params(self) -> None:
        payload = dict(SAMPLE_EVENT)
        payload["log_params"] = {"target": "Q42"}
        normalized = normalize_recent_change(payload)
        assert normalized["event_id"] == SAMPLE_EVENT["meta"]["id"]
        assert normalized["event_time"] == SAMPLE_EVENT["meta"]["dt"]
        assert normalized["id"] == str(SAMPLE_EVENT["id"])
        assert normalized["meta"]["offset"] == str(SAMPLE_EVENT["meta"]["offset"])
        assert normalized["revision"]["new"] == str(SAMPLE_EVENT["revision"]["new"])
        assert normalized["schema_uri"] == "/mediawiki/recentchange/1.0.0"
        assert normalized["log_params_json"] == '{"target":"Q42"}'


class TestStateStore:
    def test_roundtrip(self, tmp_path: Path) -> None:
        path = tmp_path / "state.json"
        store = StateStore(str(path), dedupe_size=3)
        store.save(BridgeState(since="2026-04-07T10:57:48.160Z", recent_event_ids=["a", "b", "c", "d"]))
        loaded = store.load()
        assert loaded.since == "2026-04-07T10:57:48.160Z"
        assert loaded.recent_event_ids == ["b", "c", "d"]


class TestBridgeHandleEvent:
    def test_emits_recentchange(self, tmp_path: Path) -> None:
        event_producer = MagicMock()
        kafka_producer = MagicMock()
        state_store = StateStore(str(tmp_path / "state.json"), dedupe_size=10)

        with patch(
            "wikimedia_eventstreams.wikimedia_eventstreams.RecentChange.from_serializer_dict",
            side_effect=lambda payload: payload,
        ):
            bridge = WikimediaRecentChangeBridge(
                event_producer,
                kafka_producer,
                state_store=state_store,
                flush_interval=100,
                dedupe_size=10,
            )
            handled = bridge._handle_event(dict(SAMPLE_EVENT))

        assert handled is True
        event_producer.send_wikimedia_event_streams_recent_change.assert_called_once()
        call = event_producer.send_wikimedia_event_streams_recent_change.call_args
        assert call.kwargs["_event_id"] == SAMPLE_EVENT["meta"]["id"]
        assert call.kwargs["_event_time"] == SAMPLE_EVENT["meta"]["dt"]

    def test_skips_canary(self, tmp_path: Path) -> None:
        event_producer = MagicMock()
        kafka_producer = MagicMock()
        state_store = StateStore(str(tmp_path / "state.json"), dedupe_size=10)
        bridge = WikimediaRecentChangeBridge(
            event_producer,
            kafka_producer,
            state_store=state_store,
            flush_interval=100,
            dedupe_size=10,
        )
        payload = dict(SAMPLE_EVENT)
        payload["meta"] = dict(SAMPLE_EVENT["meta"])
        payload["meta"]["domain"] = "canary"

        assert bridge._handle_event(payload) is False
        event_producer.send_wikimedia_event_streams_recent_change.assert_not_called()

    def test_dedupes_event_id(self, tmp_path: Path) -> None:
        event_producer = MagicMock()
        kafka_producer = MagicMock()
        state_store = StateStore(str(tmp_path / "state.json"), dedupe_size=10)

        with patch(
            "wikimedia_eventstreams.wikimedia_eventstreams.RecentChange.from_serializer_dict",
            side_effect=lambda payload: payload,
        ):
            bridge = WikimediaRecentChangeBridge(
                event_producer,
                kafka_producer,
                state_store=state_store,
                flush_interval=100,
                dedupe_size=10,
            )
            assert bridge._handle_event(dict(SAMPLE_EVENT)) is True
            assert bridge._handle_event(dict(SAMPLE_EVENT)) is False

        assert event_producer.send_wikimedia_event_streams_recent_change.call_count == 1
