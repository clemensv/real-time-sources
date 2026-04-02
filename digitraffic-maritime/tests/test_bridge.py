"""Tests for the Digitraffic Maritime bridge logic."""

from unittest.mock import MagicMock

from digitraffic_maritime.bridge import (
    _emit_event, _mmsi_key_mapper, parse_connection_string,
    _MESSAGE_MAP, DigitraficBridge,
)


class TestMmsiKeyMapper:
    def test_returns_mmsi_string(self):
        data = MagicMock()
        data.mmsi = 230629000
        result = _mmsi_key_mapper(None, data)
        assert result == "230629000"


class TestParseConnectionString:
    def test_event_hubs_style(self):
        cs = "Endpoint=sb://myhub.servicebus.windows.net/;SharedAccessKeyName=send;SharedAccessKey=abc123;EntityPath=mytopic"
        cfg = parse_connection_string(cs)
        assert cfg["bootstrap.servers"] == "myhub.servicebus.windows.net:9093"
        assert cfg["kafka_topic"] == "mytopic"
        assert cfg["sasl.username"] == "$ConnectionString"
        assert cfg["security.protocol"] == "SASL_SSL"

    def test_bootstrap_server_override(self):
        cs = "BootstrapServer=localhost:9092;EntityPath=test"
        cfg = parse_connection_string(cs)
        assert cfg["bootstrap.servers"] == "localhost:9092"
        assert cfg["kafka_topic"] == "test"


class TestMessageMap:
    def test_has_location_and_metadata(self):
        assert "location" in _MESSAGE_MAP
        assert "metadata" in _MESSAGE_MAP
        assert len(_MESSAGE_MAP) == 2

    def test_location_maps_to_vessel_location(self):
        data_class, method = _MESSAGE_MAP["location"]
        assert data_class.__name__ == "VesselLocation"
        assert method == "send_fi_digitraffic_marine_ais_vessel_location"

    def test_metadata_maps_to_vessel_metadata(self):
        data_class, method = _MESSAGE_MAP["metadata"]
        assert data_class.__name__ == "VesselMetadata"
        assert method == "send_fi_digitraffic_marine_ais_vessel_metadata"


class TestEmitEvent:
    def test_location_event(self):
        producer = MagicMock()
        payload = {
            "time": 1775137137,
            "sog": 10.7,
            "cog": 326.6,
            "navStat": 0,
            "rot": 0,
            "posAcc": True,
            "raim": False,
            "heading": 325,
            "lon": 20.345818,
            "lat": 60.03802,
        }
        result = _emit_event(producer, "location", 230629000, payload)
        assert result is True
        producer.send_fi_digitraffic_marine_ais_vessel_location.assert_called_once()

    def test_metadata_event(self):
        producer = MagicMock()
        payload = {
            "timestamp": 1668075026035,
            "destination": "UST LUGA",
            "name": "ARUNA CIHAN",
            "draught": 68,
            "eta": 733376,
            "posType": 15,
            "refA": 160,
            "refB": 33,
            "refC": 20,
            "refD": 12,
            "callSign": "V7WW7",
            "imo": 9543756,
            "type": 70,
        }
        result = _emit_event(producer, "metadata", 538007963, payload)
        assert result is True
        producer.send_fi_digitraffic_marine_ais_vessel_metadata.assert_called_once()

    def test_unknown_type_returns_false(self):
        producer = MagicMock()
        result = _emit_event(producer, "status", 0, {})
        assert result is False

    def test_mmsi_injected_into_payload(self):
        """Verify MMSI from topic is injected into the data class."""
        producer = MagicMock()
        payload = {
            "time": 1775137137, "sog": 0, "cog": 0, "navStat": 0,
            "rot": 0, "posAcc": False, "raim": False, "heading": 0,
            "lon": 0, "lat": 0,
        }
        _emit_event(producer, "location", 230629000, payload)
        call_args = producer.send_fi_digitraffic_marine_ais_vessel_location.call_args
        data = call_args.kwargs.get("data") or call_args[1].get("data")
        assert data.mmsi == 230629000


class TestBridgeFiltering:
    def test_mmsi_filter_blocks(self):
        mqtt = MagicMock()
        kafka = MagicMock()
        event_prod = MagicMock()

        bridge = DigitraficBridge(
            mqtt_source=mqtt,
            kafka_producer=kafka,
            event_producer=event_prod,
            mmsi_filter={230629000},
        )

        bridge._on_message("location", 999999999, {
            "time": 0, "sog": 0, "cog": 0, "navStat": 0,
            "rot": 0, "posAcc": False, "raim": False, "heading": 0,
            "lon": 0, "lat": 0,
        })
        assert event_prod.send_fi_digitraffic_marine_ais_vessel_location.call_count == 0

    def test_mmsi_filter_allows(self):
        mqtt = MagicMock()
        kafka = MagicMock()
        event_prod = MagicMock()

        bridge = DigitraficBridge(
            mqtt_source=mqtt,
            kafka_producer=kafka,
            event_producer=event_prod,
            mmsi_filter={230629000},
        )

        bridge._on_message("location", 230629000, {
            "time": 1775137137, "sog": 10.7, "cog": 326.6, "navStat": 0,
            "rot": 0, "posAcc": True, "raim": False, "heading": 325,
            "lon": 20.345818, "lat": 60.03802,
        })
        event_prod.send_fi_digitraffic_marine_ais_vessel_location.assert_called_once()

    def test_no_filter_allows_all(self):
        mqtt = MagicMock()
        kafka = MagicMock()
        event_prod = MagicMock()

        bridge = DigitraficBridge(
            mqtt_source=mqtt,
            kafka_producer=kafka,
            event_producer=event_prod,
            mmsi_filter=None,
        )

        bridge._on_message("location", 999999999, {
            "time": 0, "sog": 0, "cog": 0, "navStat": 0,
            "rot": 0, "posAcc": False, "raim": False, "heading": 0,
            "lon": 0, "lat": 0,
        })
        event_prod.send_fi_digitraffic_marine_ais_vessel_location.assert_called_once()
