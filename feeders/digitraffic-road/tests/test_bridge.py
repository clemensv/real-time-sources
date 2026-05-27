"""Tests for the Digitraffic Road bridge logic."""

import json
from unittest.mock import MagicMock, patch

from digitraffic_road.bridge import (
    _emit_sensor_event,
    _emit_traffic_message,
    _emit_maintenance,
    _flatten_traffic_message,
    _flatten_station,
    fetch_and_emit_tms_stations,
    fetch_and_emit_weather_stations,
    fetch_and_emit_maintenance_tasks,
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


class TestEmitSensorEvent:
    def test_tms_event_emits(self):
        producer = MagicMock()
        payload = {"value": 108.0, "time": 1667972911, "start": 1667966400, "end": 1667970000}
        result = _emit_sensor_event(producer, "tms", 23001, 5122, payload)
        assert result is True
        producer.send_fi_digitraffic_road_sensors_tms_sensor_data.assert_called_once()

    def test_tms_event_passes_station_and_sensor_placeholders(self):
        producer = MagicMock()
        payload = {"value": 108.0, "time": 1667972911, "start": 1667966400, "end": 1667970000}
        _emit_sensor_event(producer, "tms", 23001, 5122, payload)
        call_kwargs = producer.send_fi_digitraffic_road_sensors_tms_sensor_data.call_args
        assert call_kwargs.kwargs["_station_id"] == "23001"
        assert call_kwargs.kwargs["_sensor_id"] == "5122"

    def test_tms_event_without_time_window(self):
        producer = MagicMock()
        payload = {"value": 107.0, "time": 1667972911}
        result = _emit_sensor_event(producer, "tms", 23001, 5072, payload)
        assert result is True
        call_kwargs = producer.send_fi_digitraffic_road_sensors_tms_sensor_data.call_args
        data = call_kwargs.kwargs["data"]
        assert data.start is None
        assert data.end is None

    def test_weather_event_emits(self):
        producer = MagicMock()
        payload = {"value": 2.9, "time": 1667973021}
        result = _emit_sensor_event(producer, "weather", 1012, 1, payload)
        assert result is True
        producer.send_fi_digitraffic_road_sensors_weather_sensor_data.assert_called_once()

    def test_weather_event_passes_station_and_sensor_placeholders(self):
        producer = MagicMock()
        payload = {"value": 2.9, "time": 1667973021}
        _emit_sensor_event(producer, "weather", 1012, 1, payload)
        call_kwargs = producer.send_fi_digitraffic_road_sensors_weather_sensor_data.call_args
        assert call_kwargs.kwargs["_station_id"] == "1012"
        assert call_kwargs.kwargs["_sensor_id"] == "1"

    def test_tms_data_class_fields(self):
        producer = MagicMock()
        payload = {"value": 308.0, "time": 1667973021, "start": 1667966400, "end": 1667970000}
        _emit_sensor_event(producer, "tms", 23001, 5054, payload)
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
        _emit_sensor_event(producer, "weather", 1012, 9, payload)
        call_kwargs = producer.send_fi_digitraffic_road_sensors_weather_sensor_data.call_args
        data = call_kwargs.kwargs["data"]
        assert data.station_id == 1012
        assert data.sensor_id == 9
        assert data.value == -1.5
        assert data.time == 1667973021

    def test_unknown_type_returns_false(self):
        producer = MagicMock()
        result = _emit_sensor_event(producer, "unknown", 1, 1, {"value": 0, "time": 0})
        assert result is False

    def test_flush_producer_false(self):
        producer = MagicMock()
        payload = {"value": 1.0, "time": 1667972911}
        _emit_sensor_event(producer, "weather", 1012, 1, payload)
        call_kwargs = producer.send_fi_digitraffic_road_sensors_weather_sensor_data.call_args
        assert call_kwargs.kwargs["flush_producer"] is False


class TestFlattenTrafficMessage:
    """Test traffic message GeoJSON → flat schema conversion."""

    SAMPLE_GEOJSON = {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [25.0, 62.0]},
        "properties": {
            "situationId": "GUID50455291",
            "situationType": "traffic announcement",
            "trafficAnnouncementType": "preliminary accident report",
            "version": 3,
            "releaseTime": "2025-10-22T06:39:54.787Z",
            "versionTime": "2025-10-22T07:09:57.237Z",
            "announcements": [{
                "language": "fi",
                "title": "Tie 4, Sodankylä. Ensitiedote.",
                "sender": "Fintraffic Helsinki",
                "location": {"description": "Tie 4 Sodankylä"},
                "features": [{"name": "lane closure"}],
                "timeAndDuration": {
                    "startTime": "2025-10-22T06:30:00Z",
                    "endTime": "2025-10-22T11:00:00Z",
                },
                "comment": "Drive carefully",
                "additionalInformation": "https://liikennetilanne.fintraffic.fi",
            }],
            "contact": {"phone": "02002100", "email": "test@fintraffic.fi"},
        },
    }

    def test_extracts_situation_id(self):
        flat = _flatten_traffic_message("TRAFFIC_ANNOUNCEMENT", self.SAMPLE_GEOJSON)
        assert flat["situation_id"] == "GUID50455291"

    def test_maps_situation_type_label(self):
        flat = _flatten_traffic_message("TRAFFIC_ANNOUNCEMENT", self.SAMPLE_GEOJSON)
        assert flat["situation_type"] == "traffic announcement"

    def test_maps_road_work_label(self):
        rw = dict(self.SAMPLE_GEOJSON)
        rw["properties"] = dict(rw["properties"], situationType="road work")
        flat = _flatten_traffic_message("ROAD_WORK", rw)
        assert flat["situation_type"] == "road work"

    def test_extracts_announcement_fields(self):
        flat = _flatten_traffic_message("TRAFFIC_ANNOUNCEMENT", self.SAMPLE_GEOJSON)
        assert flat["title"] == "Tie 4, Sodankylä. Ensitiedote."
        assert flat["sender"] == "Fintraffic Helsinki"
        assert flat["language"] == "fi"
        assert flat["location_description"] == "Tie 4 Sodankylä"
        assert flat["comment"] == "Drive carefully"

    def test_extracts_time_window(self):
        flat = _flatten_traffic_message("TRAFFIC_ANNOUNCEMENT", self.SAMPLE_GEOJSON)
        assert flat["start_time"] == "2025-10-22T06:30:00Z"
        assert flat["end_time"] == "2025-10-22T11:00:00Z"

    def test_extracts_contact(self):
        flat = _flatten_traffic_message("TRAFFIC_ANNOUNCEMENT", self.SAMPLE_GEOJSON)
        assert flat["contact_phone"] == "02002100"
        assert flat["contact_email"] == "test@fintraffic.fi"

    def test_serializes_features_json(self):
        flat = _flatten_traffic_message("TRAFFIC_ANNOUNCEMENT", self.SAMPLE_GEOJSON)
        assert json.loads(flat["features_json"]) == [{"name": "lane closure"}]

    def test_road_work_phases_null_for_non_roadwork(self):
        flat = _flatten_traffic_message("TRAFFIC_ANNOUNCEMENT", self.SAMPLE_GEOJSON)
        assert flat["road_work_phases_json"] is None

    def test_road_work_phases_serialized(self):
        rw = dict(self.SAMPLE_GEOJSON)
        ann = dict(self.SAMPLE_GEOJSON["properties"]["announcements"][0])
        ann["roadWorkPhases"] = [{"workTypes": [{"type": "bridge"}]}]
        props = dict(rw["properties"])
        props["announcements"] = [ann]
        rw["properties"] = props
        flat = _flatten_traffic_message("ROAD_WORK", rw)
        parsed = json.loads(flat["road_work_phases_json"])
        assert parsed[0]["workTypes"][0]["type"] == "bridge"

    def test_serializes_announcements_json(self):
        flat = _flatten_traffic_message("TRAFFIC_ANNOUNCEMENT", self.SAMPLE_GEOJSON)
        anns = json.loads(flat["announcements_json"])
        assert len(anns) == 1
        assert anns[0]["title"] == "Tie 4, Sodankylä. Ensitiedote."

    def test_geometry_extraction(self):
        flat = _flatten_traffic_message("TRAFFIC_ANNOUNCEMENT", self.SAMPLE_GEOJSON)
        assert flat["geometry_type"] == "Point"
        assert json.loads(flat["geometry_coordinates_json"]) == [25.0, 62.0]

    def test_missing_geometry(self):
        no_geom = dict(self.SAMPLE_GEOJSON)
        del no_geom["geometry"]
        flat = _flatten_traffic_message("TRAFFIC_ANNOUNCEMENT", no_geom)
        assert flat["geometry_type"] is None
        assert flat["geometry_coordinates_json"] is None

    def test_version_fields(self):
        flat = _flatten_traffic_message("TRAFFIC_ANNOUNCEMENT", self.SAMPLE_GEOJSON)
        assert flat["version"] == 3
        assert flat["release_time"] == "2025-10-22T06:39:54.787Z"
        assert flat["version_time"] == "2025-10-22T07:09:57.237Z"


class TestEmitTrafficMessage:
    def test_traffic_announcement_emits(self):
        producer = MagicMock()
        payload = TestFlattenTrafficMessage.SAMPLE_GEOJSON
        result = _emit_traffic_message(producer, "TRAFFIC_ANNOUNCEMENT", payload)
        assert result is True
        producer.send_fi_digitraffic_road_messages_traffic_announcement.assert_called_once()

    def test_road_work_emits(self):
        producer = MagicMock()
        result = _emit_traffic_message(producer, "ROAD_WORK", TestFlattenTrafficMessage.SAMPLE_GEOJSON)
        assert result is True
        producer.send_fi_digitraffic_road_messages_road_work.assert_called_once()

    def test_weight_restriction_emits(self):
        producer = MagicMock()
        result = _emit_traffic_message(producer, "WEIGHT_RESTRICTION", TestFlattenTrafficMessage.SAMPLE_GEOJSON)
        assert result is True
        producer.send_fi_digitraffic_road_messages_weight_restriction.assert_called_once()

    def test_exempted_transport_emits(self):
        producer = MagicMock()
        result = _emit_traffic_message(producer, "EXEMPTED_TRANSPORT", TestFlattenTrafficMessage.SAMPLE_GEOJSON)
        assert result is True
        producer.send_fi_digitraffic_road_messages_exempted_transport.assert_called_once()

    def test_unknown_situation_type_returns_false(self):
        producer = MagicMock()
        result = _emit_traffic_message(producer, "UNKNOWN_TYPE", {})
        assert result is False

    def test_passes_situation_id_as_key(self):
        producer = MagicMock()
        _emit_traffic_message(producer, "TRAFFIC_ANNOUNCEMENT", TestFlattenTrafficMessage.SAMPLE_GEOJSON)
        call_kwargs = producer.send_fi_digitraffic_road_messages_traffic_announcement.call_args
        assert call_kwargs.kwargs["_situation_id"] == "GUID50455291"

    def test_flush_producer_false(self):
        producer = MagicMock()
        _emit_traffic_message(producer, "TRAFFIC_ANNOUNCEMENT", TestFlattenTrafficMessage.SAMPLE_GEOJSON)
        call_kwargs = producer.send_fi_digitraffic_road_messages_traffic_announcement.call_args
        assert call_kwargs.kwargs["flush_producer"] is False


class TestEmitMaintenance:
    SAMPLE_PAYLOAD = {
        "time": 1668157878,
        "source": "Harja/Väylävirasto",
        "tasks": ["SALTING"],
        "x": 22.031937,
        "y": 62.567092,
    }

    def test_emits_maintenance(self):
        producer = MagicMock()
        result = _emit_maintenance(producer, "state-roads", self.SAMPLE_PAYLOAD)
        assert result is True
        producer.send_fi_digitraffic_road_maintenance_maintenance_tracking.assert_called_once()

    def test_enriches_domain(self):
        producer = MagicMock()
        _emit_maintenance(producer, "state-roads", self.SAMPLE_PAYLOAD)
        call_kwargs = producer.send_fi_digitraffic_road_maintenance_maintenance_tracking.call_args
        data = call_kwargs.kwargs["data"]
        assert data.domain == "state-roads"

    def test_passes_domain_as_key(self):
        producer = MagicMock()
        _emit_maintenance(producer, "autori-kuopio", self.SAMPLE_PAYLOAD)
        call_kwargs = producer.send_fi_digitraffic_road_maintenance_maintenance_tracking.call_args
        assert call_kwargs.kwargs["_domain"] == "autori-kuopio"

    def test_data_class_fields(self):
        producer = MagicMock()
        _emit_maintenance(producer, "state-roads", self.SAMPLE_PAYLOAD)
        call_kwargs = producer.send_fi_digitraffic_road_maintenance_maintenance_tracking.call_args
        data = call_kwargs.kwargs["data"]
        assert data.time == 1668157878
        assert data.source == "Harja/Väylävirasto"
        assert data.tasks == ["SALTING"]
        assert data.x == 22.031937
        assert data.y == 62.567092
        assert data.direction is None

    def test_with_direction(self):
        producer = MagicMock()
        payload = dict(self.SAMPLE_PAYLOAD, direction=180.0)
        _emit_maintenance(producer, "state-roads", payload)
        call_kwargs = producer.send_fi_digitraffic_road_maintenance_maintenance_tracking.call_args
        data = call_kwargs.kwargs["data"]
        assert data.direction == 180.0

    def test_missing_source(self):
        producer = MagicMock()
        payload = {"time": 1000, "tasks": ["BRUSHING"], "x": 25.0, "y": 61.0}
        result = _emit_maintenance(producer, "state-roads", payload)
        assert result is True
        data = producer.send_fi_digitraffic_road_maintenance_maintenance_tracking.call_args.kwargs["data"]
        assert data.source is None

    def test_flush_producer_false(self):
        producer = MagicMock()
        _emit_maintenance(producer, "state-roads", self.SAMPLE_PAYLOAD)
        call_kwargs = producer.send_fi_digitraffic_road_maintenance_maintenance_tracking.call_args
        assert call_kwargs.kwargs["flush_producer"] is False


class TestDigitrafficRoadBridge:
    def test_on_message_counts_sensor(self):
        mqtt = MagicMock()
        kafka = MagicMock()
        sensors = MagicMock()
        bridge = DigitrafficRoadBridge(mqtt, kafka, sensors_producer=sensors, flush_interval=2)
        bridge._start_time = 1000.0

        bridge._on_message("tms", {"station_id": 23001, "sensor_id": 5122}, {"value": 100.0, "time": 1667972911, "start": None, "end": None})
        assert bridge._total == 1
        assert bridge._count == 1

        bridge._on_message("weather", {"station_id": 1012, "sensor_id": 1}, {"value": 2.9, "time": 1667973021})
        assert bridge._total == 2
        assert bridge._count == 0  # flushed

    def test_on_message_counts_traffic(self):
        mqtt = MagicMock()
        kafka = MagicMock()
        messages = MagicMock()
        bridge = DigitrafficRoadBridge(mqtt, kafka, messages_producer=messages, flush_interval=100)
        bridge._start_time = 1000.0

        bridge._on_message("traffic-announcement", {"situation_type": "TRAFFIC_ANNOUNCEMENT"}, TestFlattenTrafficMessage.SAMPLE_GEOJSON)
        assert bridge._total == 1

    def test_on_message_counts_maintenance(self):
        mqtt = MagicMock()
        kafka = MagicMock()
        maint = MagicMock()
        bridge = DigitrafficRoadBridge(mqtt, kafka, maintenance_producer=maint, flush_interval=100)
        bridge._start_time = 1000.0

        bridge._on_message("maintenance", {"domain": "state-roads"}, TestEmitMaintenance.SAMPLE_PAYLOAD)
        assert bridge._total == 1

    def test_on_message_skips_without_producer(self):
        mqtt = MagicMock()
        kafka = MagicMock()
        bridge = DigitrafficRoadBridge(mqtt, kafka, flush_interval=100)
        bridge._start_time = 1000.0

        bridge._on_message("tms", {"station_id": 1, "sensor_id": 1}, {"value": 0, "time": 0})
        assert bridge._skipped == 1
        assert bridge._total == 0


class TestMQTTSource:
    def test_topic_construction_all(self):
        from digitraffic_road.mqtt_source import MQTTSource
        src = MQTTSource(subscribe_tms=True, subscribe_weather=True,
                         subscribe_traffic_messages=True, subscribe_maintenance=True)
        topics = src._get_topics()
        assert "tms-v2/#" in topics
        assert "weather-v2/#" in topics
        assert "traffic-message-v3/simple/#" in topics
        assert "maintenance-v2/routes/#" in topics

    def test_topic_construction_sensors_only(self):
        from digitraffic_road.mqtt_source import MQTTSource
        src = MQTTSource(subscribe_tms=True, subscribe_weather=True,
                         subscribe_traffic_messages=False, subscribe_maintenance=False)
        topics = src._get_topics()
        assert "tms-v2/#" in topics
        assert "weather-v2/#" in topics
        assert "traffic-message-v3/simple/#" not in topics
        assert "maintenance-v2/routes/#" not in topics

    def test_topic_construction_with_station_filter(self):
        from digitraffic_road.mqtt_source import MQTTSource
        src = MQTTSource(
            subscribe_tms=True, subscribe_weather=True,
            subscribe_traffic_messages=True, subscribe_maintenance=True,
            station_filter={23001, 1012},
        )
        topics = src._get_topics()
        assert "tms-v2/23001/+" in topics
        assert "tms-v2/1012/+" in topics
        assert "weather-v2/23001/+" in topics
        assert "weather-v2/1012/+" in topics
        # traffic messages and maintenance are unaffected by station filter
        assert "traffic-message-v3/simple/#" in topics
        assert "maintenance-v2/routes/#" in topics

    def test_sensor_handler_parses_topic(self):
        from digitraffic_road.mqtt_source import MQTTSource
        src = MQTTSource()
        results = []
        src._callback = lambda dt, meta, payload: results.append((dt, meta, payload))
        src._handle_sensor("tms-v2", ["tms-v2", "23001", "5122"], b'{"value":100,"time":1000}')
        assert len(results) == 1
        assert results[0][0] == "tms"
        assert results[0][1] == {"station_id": 23001, "sensor_id": 5122}
        assert results[0][2]["value"] == 100

    def test_sensor_handler_skips_status(self):
        from digitraffic_road.mqtt_source import MQTTSource
        src = MQTTSource()
        results = []
        src._callback = lambda dt, meta, payload: results.append((dt, meta, payload))
        src._handle_sensor("tms-v2", ["tms-v2", "status", "ok"], b'{}')
        assert len(results) == 0

    def test_traffic_message_handler(self):
        import base64, gzip
        from digitraffic_road.mqtt_source import MQTTSource
        src = MQTTSource()
        results = []
        src._callback = lambda dt, meta, payload: results.append((dt, meta, payload))

        raw_json = json.dumps({"properties": {"situationId": "GUID123"}}).encode()
        compressed = gzip.compress(raw_json)
        encoded = base64.b64encode(compressed)

        src._handle_traffic_message(["traffic-message-v3", "simple", "TRAFFIC_ANNOUNCEMENT"], encoded)
        assert len(results) == 1
        assert results[0][0] == "traffic-announcement"
        assert results[0][1] == {"situation_type": "TRAFFIC_ANNOUNCEMENT"}
        assert results[0][2]["properties"]["situationId"] == "GUID123"

    def test_maintenance_handler(self):
        from digitraffic_road.mqtt_source import MQTTSource
        src = MQTTSource()
        results = []
        src._callback = lambda dt, meta, payload: results.append((dt, meta, payload))
        src._handle_maintenance(
            ["maintenance-v2", "routes", "state-roads"],
            b'{"time":1000,"tasks":["SALTING"],"x":22.0,"y":62.0}',
        )
        assert len(results) == 1
        assert results[0][0] == "maintenance"
        assert results[0][1] == {"domain": "state-roads"}


class TestFlattenStation:
    SAMPLE_TMS_FEATURE = {
        "type": "Feature",
        "id": 23001,
        "geometry": {"type": "Point", "coordinates": [25.689529, 60.417002, 0.0]},
        "properties": {
            "id": 23001,
            "name": "vt7_Rita",
            "tmsNumber": 1,
            "names": {"fi": "Tie 7 Porvoo, Rita", "sv": "Väg 7 Borgå, Rita", "en": "Road 7 Porvoo, Rita"},
            "municipality": "Porvoo",
            "municipalityCode": 638,
            "province": "Uusimaa",
            "provinceCode": 1,
            "roadAddress": {
                "roadNumber": 7,
                "roadSection": 10,
                "distanceFromRoadSectionStart": 950,
                "carriageway": "DUAL_CARRIAGEWAY_RIGHT_IN_INCREASING_DIRECTION",
                "side": "LEFT",
            },
            "stationType": "DSL_6",
            "collectionStatus": "GATHERING",
            "state": "OK",
            "freeFlowSpeed1": 105.0,
            "freeFlowSpeed2": 95.0,
            "bearing": 60,
            "startTime": "2001-11-07T00:00:00Z",
            "liviId": "Livi968639",
            "sensors": [5054, 5055, 5056],
            "dataUpdatedTime": "2024-01-15T10:00:00Z",
        },
    }

    SAMPLE_WEATHER_FEATURE = {
        "type": "Feature",
        "id": 1012,
        "geometry": {"type": "Point", "coordinates": [24.667305, 60.153507, 0.0]},
        "properties": {
            "id": 1012,
            "name": "kt51_Espoo_Kivenlahti",
            "names": {"fi": "Tie 51 Espoo, Kivenlahti", "sv": "Väg 51 Esbo, Stensvik", "en": "Road 51 Espoo, Kivenlahti"},
            "municipality": "Espoo",
            "municipalityCode": 49,
            "province": "Uusimaa",
            "provinceCode": 1,
            "roadAddress": {
                "roadNumber": 51,
                "roadSection": 6,
                "distanceFromRoadSectionStart": 2237,
                "carriageway": "DUAL_CARRIAGEWAY_LEFT_IN_INCREASING_DIRECTION",
                "side": "LEFT",
                "contractArea": "Espoo 19-24",
                "contractAreaCode": 142,
            },
            "stationType": "RWS_200",
            "master": True,
            "collectionStatus": "GATHERING",
            "collectionInterval": 300,
            "state": None,
            "startTime": "1995-06-02T00:00:00Z",
            "liviId": "Livi1090115",
            "sensors": [1, 2, 3],
            "dataUpdatedTime": "2024-07-06T03:06:05Z",
        },
    }

    def test_flattens_tms_station(self):
        flat = _flatten_station(self.SAMPLE_TMS_FEATURE)
        assert flat["station_id"] == 23001
        assert flat["name"] == "vt7_Rita"
        assert flat["tms_number"] == 1
        assert flat["names_fi"] == "Tie 7 Porvoo, Rita"
        assert flat["names_sv"] == "Väg 7 Borgå, Rita"
        assert flat["longitude"] == 25.689529
        assert flat["latitude"] == 60.417002
        assert flat["municipality"] == "Porvoo"
        assert flat["municipality_code"] == 638
        assert flat["province"] == "Uusimaa"
        assert flat["province_code"] == 1
        assert flat["road_number"] == 7
        assert flat["road_section"] == 10
        assert flat["distance_from_section_start"] == 950
        assert flat["carriageway"] == "DUAL_CARRIAGEWAY_RIGHT_IN_INCREASING_DIRECTION"
        assert flat["side"] == "LEFT"
        assert flat["station_type"] == "DSL_6"
        assert flat["collection_status"] == "GATHERING"
        assert flat["state"] == "OK"
        assert flat["free_flow_speed_1"] == 105.0
        assert flat["free_flow_speed_2"] == 95.0
        assert flat["bearing"] == 60
        assert flat["start_time"] == "2001-11-07T00:00:00Z"
        assert flat["livi_id"] == "Livi968639"
        assert flat["sensors"] == [5054, 5055, 5056]
        assert flat["data_updated_time"] == "2024-01-15T10:00:00Z"

    def test_flattens_weather_station(self):
        flat = _flatten_station(self.SAMPLE_WEATHER_FEATURE)
        assert flat["station_id"] == 1012
        assert flat["name"] == "kt51_Espoo_Kivenlahti"
        assert flat["master"] is True
        assert flat["collection_interval"] == 300
        assert flat["contract_area"] == "Espoo 19-24"
        assert flat["contract_area_code"] == 142
        assert flat["state"] is None

    def test_altitude_zero_becomes_none(self):
        flat = _flatten_station(self.SAMPLE_TMS_FEATURE)
        assert flat["altitude"] is None

    def test_altitude_nonzero_preserved(self):
        feature = dict(self.SAMPLE_TMS_FEATURE)
        feature["geometry"] = {"type": "Point", "coordinates": [25.0, 60.0, 42.5]}
        flat = _flatten_station(feature)
        assert flat["altitude"] == 42.5


class TestFetchAndEmitStations:
    TMS_API_RESPONSE = {
        "type": "FeatureCollection",
        "features": [TestFlattenStation.SAMPLE_TMS_FEATURE],
    }
    WEATHER_API_RESPONSE = {
        "type": "FeatureCollection",
        "features": [TestFlattenStation.SAMPLE_WEATHER_FEATURE],
    }

    @patch("digitraffic_road.bridge.requests.get")
    def test_fetch_tms_stations(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.json.return_value = self.TMS_API_RESPONSE
        mock_get.return_value = mock_resp
        producer = MagicMock()

        count = fetch_and_emit_tms_stations(producer)
        assert count == 1
        producer.send_fi_digitraffic_road_stations_tms_station.assert_called_once()
        call_kwargs = producer.send_fi_digitraffic_road_stations_tms_station.call_args.kwargs
        assert call_kwargs["_station_id"] == "23001"
        assert call_kwargs["flush_producer"] is False

    @patch("digitraffic_road.bridge.requests.get")
    def test_fetch_weather_stations(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.json.return_value = self.WEATHER_API_RESPONSE
        mock_get.return_value = mock_resp
        producer = MagicMock()

        count = fetch_and_emit_weather_stations(producer)
        assert count == 1
        producer.send_fi_digitraffic_road_stations_weather_station.assert_called_once()
        call_kwargs = producer.send_fi_digitraffic_road_stations_weather_station.call_args.kwargs
        assert call_kwargs["_station_id"] == "1012"

    @patch("digitraffic_road.bridge.requests.get")
    def test_tms_station_data_fields(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.json.return_value = self.TMS_API_RESPONSE
        mock_get.return_value = mock_resp
        producer = MagicMock()

        fetch_and_emit_tms_stations(producer)
        data = producer.send_fi_digitraffic_road_stations_tms_station.call_args.kwargs["data"]
        assert data.station_id == 23001
        assert data.name == "vt7_Rita"
        assert data.municipality == "Porvoo"
        assert data.sensors == [5054, 5055, 5056]

    @patch("digitraffic_road.bridge.requests.get")
    def test_weather_station_data_fields(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.json.return_value = self.WEATHER_API_RESPONSE
        mock_get.return_value = mock_resp
        producer = MagicMock()

        fetch_and_emit_weather_stations(producer)
        data = producer.send_fi_digitraffic_road_stations_weather_station.call_args.kwargs["data"]
        assert data.station_id == 1012
        assert data.master is True
        assert data.collection_interval == 300


class TestFetchAndEmitMaintenanceTasks:
    TASKS_API_RESPONSE = [
        {
            "id": "BRUSHING",
            "nameFi": "Harjaus",
            "nameEn": "Brushing",
            "nameSv": "Borstning",
            "dataUpdatedTime": "2020-03-30T00:00:00Z",
        },
        {
            "id": "SALTING",
            "nameFi": "Suolaus",
            "nameEn": "Salting",
            "nameSv": "Saltning",
            "dataUpdatedTime": "2020-03-30T00:00:00Z",
        },
    ]

    @patch("digitraffic_road.bridge.requests.get")
    def test_fetch_tasks(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.json.return_value = self.TASKS_API_RESPONSE
        mock_get.return_value = mock_resp
        producer = MagicMock()

        count = fetch_and_emit_maintenance_tasks(producer)
        assert count == 2
        assert producer.send_fi_digitraffic_road_maintenance_tasks_maintenance_task_type.call_count == 2

    @patch("digitraffic_road.bridge.requests.get")
    def test_task_data_fields(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.json.return_value = self.TASKS_API_RESPONSE
        mock_get.return_value = mock_resp
        producer = MagicMock()

        fetch_and_emit_maintenance_tasks(producer)
        first_call = producer.send_fi_digitraffic_road_maintenance_tasks_maintenance_task_type.call_args_list[0]
        assert first_call.kwargs["_task_id"] == "BRUSHING"
        data = first_call.kwargs["data"]
        assert data.task_id == "BRUSHING"
        assert data.name_fi == "Harjaus"
        assert data.name_en == "Brushing"
        assert data.name_sv == "Borstning"
        assert data.data_updated_time == "2020-03-30T00:00:00Z"

    @patch("digitraffic_road.bridge.requests.get")
    def test_flush_producer_false(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.json.return_value = self.TASKS_API_RESPONSE
        mock_get.return_value = mock_resp
        producer = MagicMock()

        fetch_and_emit_maintenance_tasks(producer)
        for call in producer.send_fi_digitraffic_road_maintenance_tasks_maintenance_task_type.call_args_list:
            assert call.kwargs["flush_producer"] is False


class TestBridgeReferenceDataEmission:
    @patch("digitraffic_road.bridge.fetch_and_emit_maintenance_tasks", return_value=3)
    @patch("digitraffic_road.bridge.fetch_and_emit_weather_stations", return_value=5)
    @patch("digitraffic_road.bridge.fetch_and_emit_tms_stations", return_value=10)
    def test_emit_reference_data_calls_all(self, mock_tms, mock_weather, mock_tasks):
        mqtt = MagicMock()
        kafka = MagicMock()
        stations = MagicMock()
        tasks = MagicMock()
        bridge = DigitrafficRoadBridge(
            mqtt, kafka,
            stations_producer=stations,
            tasks_producer=tasks,
        )
        bridge._start_time = 1000.0
        bridge._emit_reference_data()

        mock_tms.assert_called_once_with(stations)
        mock_weather.assert_called_once_with(stations)
        mock_tasks.assert_called_once_with(tasks)
        kafka.flush.assert_called_once()
        assert bridge._total == 18  # 10 + 5 + 3

    @patch("digitraffic_road.bridge.fetch_and_emit_weather_stations", return_value=0)
    @patch("digitraffic_road.bridge.fetch_and_emit_tms_stations", return_value=0)
    def test_emit_reference_data_no_flush_when_zero(self, mock_tms, mock_weather):
        mqtt = MagicMock()
        kafka = MagicMock()
        stations = MagicMock()
        bridge = DigitrafficRoadBridge(mqtt, kafka, stations_producer=stations)
        bridge._start_time = 1000.0
        bridge._emit_reference_data()
        kafka.flush.assert_not_called()

    def test_emit_reference_data_skips_without_producers(self):
        mqtt = MagicMock()
        kafka = MagicMock()
        bridge = DigitrafficRoadBridge(mqtt, kafka)
        bridge._start_time = 1000.0
        bridge._emit_reference_data()
        kafka.flush.assert_not_called()
        assert bridge._total == 0
