"""Tests for the Digitraffic Road bridge logic."""

from unittest.mock import MagicMock

from digitraffic_road.bridge import (
    _emit_event,
    parse_connection_string,
    DigitrafficRoadBridge,
)


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


class TestEmitEvent:
    def test_tms_event_emits(self):
        producer = MagicMock()
        payload = {"value": 108.0, "time": 1667972911, "start": 1667966400, "end": 1667970000}
        result = _emit_event(producer, "tms", 23001, 5122, payload)
        assert result is True
        producer.send_fi_digitraffic_road_sensors_tms_sensor_data.assert_called_once()

    def test_tms_event_passes_station_and_sensor_placeholders(self):
        producer = MagicMock()
        payload = {"value": 108.0, "time": 1667972911, "start": 1667966400, "end": 1667970000}
        _emit_event(producer, "tms", 23001, 5122, payload)
        call_kwargs = producer.send_fi_digitraffic_road_sensors_tms_sensor_data.call_args
        assert call_kwargs.kwargs["_station_id"] == "23001"
        assert call_kwargs.kwargs["_sensor_id"] == "5122"

    def test_tms_event_without_time_window(self):
        """Rolling-window sensors don't have start/end fields."""
        producer = MagicMock()
        payload = {"value": 107.0, "time": 1667972911}
        result = _emit_event(producer, "tms", 23001, 5072, payload)
        assert result is True
        call_kwargs = producer.send_fi_digitraffic_road_sensors_tms_sensor_data.call_args
        data = call_kwargs.kwargs["data"]
        assert data.start is None
        assert data.end is None

    def test_weather_event_emits(self):
        producer = MagicMock()
        payload = {"value": 2.9, "time": 1667973021}
        result = _emit_event(producer, "weather", 1012, 1, payload)
        assert result is True
        producer.send_fi_digitraffic_road_sensors_weather_sensor_data.assert_called_once()

    def test_weather_event_passes_station_and_sensor_placeholders(self):
        producer = MagicMock()
        payload = {"value": 2.9, "time": 1667973021}
        _emit_event(producer, "weather", 1012, 1, payload)
        call_kwargs = producer.send_fi_digitraffic_road_sensors_weather_sensor_data.call_args
        assert call_kwargs.kwargs["_station_id"] == "1012"
        assert call_kwargs.kwargs["_sensor_id"] == "1"

    def test_tms_data_class_fields(self):
        producer = MagicMock()
        payload = {"value": 308.0, "time": 1667973021, "start": 1667966400, "end": 1667970000}
        _emit_event(producer, "tms", 23001, 5054, payload)
        call_kwargs = producer.send_fi_digitraffic_road_sensors_tms_sensor_data.call_args
        data = call_kwargs.kwargs["data"]
        assert data.station_id == 23001
        assert data.sensor_id == 5054
        assert data.value == 308.0
        assert data.time == 1667973021
        assert data.start == 1667966400
        assert data.end == 1667970000

    def test_weather_data_class_fields(self):
        producer = MagicMock()
        payload = {"value": -1.5, "time": 1667973021}
        _emit_event(producer, "weather", 1012, 9, payload)
        call_kwargs = producer.send_fi_digitraffic_road_sensors_weather_sensor_data.call_args
        data = call_kwargs.kwargs["data"]
        assert data.station_id == 1012
        assert data.sensor_id == 9
        assert data.value == -1.5
        assert data.time == 1667973021

    def test_unknown_type_returns_false(self):
        producer = MagicMock()
        result = _emit_event(producer, "unknown", 1, 1, {"value": 0, "time": 0})
        assert result is False

    def test_flush_producer_false(self):
        """Verify events are sent without flushing (batched flush in bridge)."""
        producer = MagicMock()
        payload = {"value": 1.0, "time": 1667972911}
        _emit_event(producer, "weather", 1012, 1, payload)
        call_kwargs = producer.send_fi_digitraffic_road_sensors_weather_sensor_data.call_args
        assert call_kwargs.kwargs["flush_producer"] is False


class TestDigitrafficRoadBridge:
    def test_on_message_counts(self):
        mqtt = MagicMock()
        kafka = MagicMock()
        event_producer = MagicMock()
        bridge = DigitrafficRoadBridge(mqtt, kafka, event_producer, flush_interval=2)
        bridge._start_time = 1000.0

        bridge._on_message("tms", 23001, 5122, {"value": 100.0, "time": 1667972911, "start": None, "end": None})
        assert bridge._total == 1
        assert bridge._count == 1

        bridge._on_message("weather", 1012, 1, {"value": 2.9, "time": 1667973021})
        assert bridge._total == 2
        # count should reset after flush_interval
        assert bridge._count == 0

    def test_on_message_skips_unknown(self):
        mqtt = MagicMock()
        kafka = MagicMock()
        event_producer = MagicMock()
        bridge = DigitrafficRoadBridge(mqtt, kafka, event_producer)
        bridge._start_time = 1000.0

        bridge._on_message("bogus", 1, 1, {"value": 0, "time": 0})
        assert bridge._skipped == 1
        assert bridge._total == 0


class TestMQTTSource:
    def test_topic_construction_all(self):
        from digitraffic_road.mqtt_source import MQTTSource
        src = MQTTSource(subscribe_tms=True, subscribe_weather=True)
        topics = src._get_topics()
        assert "tms-v2/#" in topics
        assert "weather-v2/#" in topics

    def test_topic_construction_tms_only(self):
        from digitraffic_road.mqtt_source import MQTTSource
        src = MQTTSource(subscribe_tms=True, subscribe_weather=False)
        topics = src._get_topics()
        assert "tms-v2/#" in topics
        assert "weather-v2/#" not in topics

    def test_topic_construction_weather_only(self):
        from digitraffic_road.mqtt_source import MQTTSource
        src = MQTTSource(subscribe_tms=False, subscribe_weather=True)
        topics = src._get_topics()
        assert "tms-v2/#" not in topics
        assert "weather-v2/#" in topics

    def test_topic_construction_with_station_filter(self):
        from digitraffic_road.mqtt_source import MQTTSource
        src = MQTTSource(
            subscribe_tms=True, subscribe_weather=True,
            station_filter={23001, 1012},
        )
        topics = src._get_topics()
        assert len(topics) == 4
        assert "tms-v2/23001/+" in topics
        assert "tms-v2/1012/+" in topics
        assert "weather-v2/23001/+" in topics
        assert "weather-v2/1012/+" in topics
