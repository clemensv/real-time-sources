"""Unit tests for the Blitzortung live bridge."""

from pathlib import Path
from unittest.mock import MagicMock, patch

from blitzortung.blitzortung import (
    BridgeState,
    BlitzortungBridge,
    StateStore,
    build_request,
    epoch_millis_to_iso8601,
    normalize_stroke,
    parse_bbox,
    parse_connection_string,
    parse_ws_urls,
)


SAMPLE_STROKE = {
    "time": 1775637660093,
    "lat": 27.443801,
    "lon": -72.454861,
    "src": 2,
    "srv": 1,
    "sta": {
        "1073": 64,
        "1188": 65,
        "1232": 0,
    },
    "id": 2341268,
    "del": 1737,
    "dev": 993,
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
    def test_parse_ws_urls_defaults(self) -> None:
        urls = parse_ws_urls(None)
        assert urls[0].startswith("wss://live.lightningmaps.org")
        assert len(urls) == 2

    def test_parse_bbox(self) -> None:
        assert parse_bbox("50,20,10,-5") == (50.0, 20.0, 10.0, -5.0)

    def test_epoch_millis_to_iso8601(self) -> None:
        assert epoch_millis_to_iso8601(1775637660093) == "2026-04-08T08:41:00.093000Z"

    def test_build_request_contains_resume_and_bbox(self) -> None:
        payload = build_request(
            {"2": 2341268},
            include_stations=True,
            bbox=(90.0, 180.0, -90.0, -180.0),
            source_mask=4,
        )
        assert '"i":{"2":2341268}' in payload
        assert '"s":true' in payload
        assert '"p":[90.0,180.0,-90.0,-180.0]' in payload

    def test_normalize_stroke(self) -> None:
        normalized = normalize_stroke(SAMPLE_STROKE)
        assert normalized["source_id"] == 2
        assert normalized["stroke_id"] == "2341268"
        assert normalized["event_timestamp_ms"] == 1775637660093
        assert normalized["latitude"] == 27.443801
        assert normalized["longitude"] == -72.454861
        assert normalized["server_delay_ms"] == 1737
        assert normalized["accuracy_diameter_m"] == 993.0
        assert normalized["detector_participations"] == [
            {"station_id": 1073, "status": 64},
            {"station_id": 1188, "status": 65},
            {"station_id": 1232, "status": 0},
        ]


class TestStateStore:
    def test_roundtrip(self, tmp_path: Path) -> None:
        path = tmp_path / "state.json"
        store = StateStore(str(path), dedupe_size=3)
        store.save(BridgeState(last_ids={"2": 5}, recent_keys=["a", "b", "c", "d"]))
        loaded = store.load()
        assert loaded.last_ids == {"2": 5}
        assert loaded.recent_keys == ["b", "c", "d"]


class TestBridge:
    def test_emits_and_updates_state(self, tmp_path: Path) -> None:
        event_producer = MagicMock()
        kafka_producer = MagicMock()
        state_store = StateStore(str(tmp_path / "state.json"), dedupe_size=10)

        with patch(
            "blitzortung.blitzortung.LightningStroke.from_serializer_dict",
            side_effect=lambda payload: type("Stroke", (), payload)(),
        ):
            bridge = BlitzortungBridge(
                event_producer,
                kafka_producer,
                state_store=state_store,
                ws_urls=["wss://example.invalid/"],
                bbox=(90.0, 180.0, -90.0, -180.0),
                include_stations=True,
                flush_interval=100,
                dedupe_size=10,
            )
            assert bridge._handle_stroke(dict(SAMPLE_STROKE)) is True
            assert bridge._handle_stroke(dict(SAMPLE_STROKE)) is False

        event_producer.send_blitzortung_lightning_lightning_stroke.assert_called_once()
        call = event_producer.send_blitzortung_lightning_lightning_stroke.call_args
        assert call.kwargs["_source_id"] == 2
        assert call.kwargs["_stroke_id"] == "2341268"
        assert call.kwargs["_event_time"] == "2026-04-08T08:41:00.093000Z"

    def test_handle_message_ignores_handshake_frame(self, tmp_path: Path) -> None:
        bridge = BlitzortungBridge(
            MagicMock(),
            MagicMock(),
            state_store=StateStore(str(tmp_path / "state.json"), dedupe_size=10),
            ws_urls=["wss://example.invalid/"],
            bbox=(90.0, 180.0, -90.0, -180.0),
            include_stations=True,
            flush_interval=100,
            dedupe_size=10,
        )
        assert bridge._handle_message({"cid": 1, "time": 1775637850.891, "k": 1}) == 0
