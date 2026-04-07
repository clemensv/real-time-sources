"""Unit tests for the iRail bridge."""

import json
import unittest
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from irail.irail import IRailAPI, _parse_connection_string


# --- Sample API responses ---

SAMPLE_STATIONS_RESPONSE = {
    "version": "1.1",
    "timestamp": 1712500000,
    "station": [
        {
            "@id": "http://irail.be/stations/NMBS/008814001",
            "id": "BE.NMBS.008814001",
            "name": "Brussels-South",
            "locationX": "4.336531",
            "locationY": "50.835707",
            "standardname": "Bruxelles-Midi / Brussel-Zuid"
        },
        {
            "@id": "http://irail.be/stations/NMBS/008821006",
            "id": "BE.NMBS.008821006",
            "name": "Antwerp-Central",
            "locationX": "4.421101",
            "locationY": "51.2172",
            "standardname": "Antwerpen-Centraal"
        }
    ]
}

SAMPLE_LIVEBOARD_RESPONSE = {
    "version": "1.1",
    "timestamp": "1712500000",
    "station": "Brussels-South",
    "stationinfo": {
        "@id": "http://irail.be/stations/NMBS/008814001",
        "id": "BE.NMBS.008814001",
        "name": "Brussels-South",
        "locationX": "4.336531",
        "locationY": "50.835707",
        "standardname": "Bruxelles-Midi / Brussel-Zuid"
    },
    "departures": {
        "number": 2,
        "departure": [
            {
                "id": "0",
                "station": "Antwerp-Central",
                "stationinfo": {
                    "@id": "http://irail.be/stations/NMBS/008821006",
                    "id": "BE.NMBS.008821006",
                    "name": "Antwerp-Central",
                    "locationX": "4.421101",
                    "locationY": "51.2172",
                    "standardname": "Antwerpen-Centraal"
                },
                "time": "1712502000",
                "delay": "300",
                "canceled": "0",
                "left": "0",
                "isExtra": "0",
                "vehicle": "BE.NMBS.IC2117",
                "vehicleinfo": {
                    "name": "BE.NMBS.IC2117",
                    "shortname": "IC 2117",
                    "number": "2117",
                    "type": "IC",
                    "locationX": "0",
                    "locationY": "0",
                    "@id": "http://irail.be/vehicle/IC2117"
                },
                "platform": "13",
                "platforminfo": {
                    "name": "13",
                    "normal": "1"
                },
                "occupancy": {
                    "@id": "http://api.irail.be/terms/low",
                    "name": "low"
                },
                "departureConnection": "http://irail.be/connections/8814001/20260407/IC2117"
            },
            {
                "id": "1",
                "station": "Ghent-Sint-Pieters",
                "stationinfo": {
                    "@id": "http://irail.be/stations/NMBS/008892007",
                    "id": "BE.NMBS.008892007",
                    "name": "Ghent-Sint-Pieters",
                    "locationX": "3.710675",
                    "locationY": "51.035896",
                    "standardname": "Gent-Sint-Pieters"
                },
                "time": "1712503800",
                "delay": "0",
                "canceled": "1",
                "left": "1",
                "isExtra": "1",
                "vehicle": "BE.NMBS.S51507",
                "vehicleinfo": {
                    "name": "BE.NMBS.S51507",
                    "shortname": "S5 1507",
                    "number": "1507",
                    "type": "S5",
                    "locationX": "0",
                    "locationY": "0",
                    "@id": "http://irail.be/vehicle/S51507"
                },
                "platform": "4",
                "platforminfo": {
                    "name": "4",
                    "normal": "0"
                },
                "occupancy": {
                    "@id": "http://api.irail.be/terms/high",
                    "name": "high"
                },
                "departureConnection": "http://irail.be/connections/8814001/20260407/S51507"
            }
        ]
    }
}


class TestParseStation(unittest.TestCase):
    """Test station parsing."""

    def test_parse_station_basic(self):
        raw = SAMPLE_STATIONS_RESPONSE["station"][0]
        station = IRailAPI.parse_station(raw)
        self.assertEqual(station.station_id, "008814001")
        self.assertEqual(station.name, "Brussels-South")
        self.assertEqual(station.standard_name, "Bruxelles-Midi / Brussel-Zuid")
        self.assertAlmostEqual(station.longitude, 4.336531, places=4)
        self.assertAlmostEqual(station.latitude, 50.835707, places=4)
        self.assertEqual(station.uri, "http://irail.be/stations/NMBS/008814001")

    def test_parse_station_strips_prefix(self):
        raw = {"id": "BE.NMBS.008821006", "name": "Antwerp-Central",
               "standardname": "Antwerpen-Centraal", "locationX": "4.421101",
               "locationY": "51.2172", "@id": "http://irail.be/stations/NMBS/008821006"}
        station = IRailAPI.parse_station(raw)
        self.assertEqual(station.station_id, "008821006")

    def test_parse_station_no_prefix(self):
        raw = {"id": "008821006", "name": "Test", "standardname": "Test",
               "locationX": "0", "locationY": "0", "@id": ""}
        station = IRailAPI.parse_station(raw)
        self.assertEqual(station.station_id, "008821006")

    def test_parse_station_missing_fields(self):
        raw = {"id": "BE.NMBS.008800001"}
        station = IRailAPI.parse_station(raw)
        self.assertEqual(station.station_id, "008800001")
        self.assertEqual(station.name, "")
        self.assertEqual(station.standard_name, "")


class TestParseDeparture(unittest.TestCase):
    """Test departure parsing."""

    def test_parse_departure_with_delay(self):
        raw = SAMPLE_LIVEBOARD_RESPONSE["departures"]["departure"][0]
        dep = IRailAPI.parse_departure(raw)
        self.assertEqual(dep.destination_station_id, "008821006")
        self.assertEqual(dep.destination_name, "Antwerp-Central")
        self.assertEqual(dep.delay_seconds, 300)
        self.assertFalse(dep.is_canceled)
        self.assertFalse(dep.has_left)
        self.assertFalse(dep.is_extra_stop)
        self.assertEqual(dep.vehicle_id, "BE.NMBS.IC2117")
        self.assertEqual(dep.vehicle_short_name, "IC 2117")
        self.assertEqual(dep.vehicle_type, "IC")
        self.assertEqual(dep.vehicle_number, "2117")
        self.assertEqual(dep.platform, "13")
        self.assertTrue(dep.is_normal_platform)
        self.assertEqual(dep.occupancy, "low")
        self.assertEqual(dep.departure_connection_uri, "http://irail.be/connections/8814001/20260407/IC2117")

    def test_parse_departure_canceled_and_left(self):
        raw = SAMPLE_LIVEBOARD_RESPONSE["departures"]["departure"][1]
        dep = IRailAPI.parse_departure(raw)
        self.assertTrue(dep.is_canceled)
        self.assertTrue(dep.has_left)
        self.assertTrue(dep.is_extra_stop)
        self.assertEqual(dep.occupancy, "high")
        self.assertFalse(dep.is_normal_platform)

    def test_parse_departure_time_conversion(self):
        raw = SAMPLE_LIVEBOARD_RESPONSE["departures"]["departure"][0]
        dep = IRailAPI.parse_departure(raw)
        # timestamp 1712502000 = 2024-04-07T18:00:00Z
        dt = datetime.fromisoformat(dep.scheduled_time)
        self.assertEqual(dt.tzinfo, timezone.utc)

    def test_parse_departure_empty_platform(self):
        raw = dict(SAMPLE_LIVEBOARD_RESPONSE["departures"]["departure"][0])
        raw["platform"] = ""
        raw["platforminfo"] = {"name": "", "normal": "1"}
        dep = IRailAPI.parse_departure(raw)
        self.assertIsNone(dep.platform)

    def test_parse_departure_question_mark_platform(self):
        raw = dict(SAMPLE_LIVEBOARD_RESPONSE["departures"]["departure"][0])
        raw["platform"] = "?"
        dep = IRailAPI.parse_departure(raw)
        self.assertIsNone(dep.platform)

    def test_parse_departure_unknown_occupancy(self):
        raw = dict(SAMPLE_LIVEBOARD_RESPONSE["departures"]["departure"][0])
        raw["occupancy"] = {"@id": "http://api.irail.be/terms/something", "name": "xyz"}
        dep = IRailAPI.parse_departure(raw)
        self.assertEqual(dep.occupancy, "unknown")


class TestParseLiveboard(unittest.TestCase):
    """Test liveboard parsing."""

    def test_parse_liveboard_basic(self):
        board = IRailAPI.parse_liveboard(SAMPLE_LIVEBOARD_RESPONSE, "008814001")
        self.assertEqual(board.station_id, "008814001")
        self.assertEqual(board.station_name, "Brussels-South")
        self.assertEqual(board.departure_count, 2)
        self.assertEqual(len(board.departures), 2)

    def test_parse_liveboard_timestamp(self):
        board = IRailAPI.parse_liveboard(SAMPLE_LIVEBOARD_RESPONSE, "008814001")
        dt = datetime.fromisoformat(board.retrieved_at)
        self.assertEqual(dt.tzinfo, timezone.utc)

    def test_parse_liveboard_empty_departures(self):
        raw = {"timestamp": "1712500000", "station": "Test", "stationinfo": {},
               "departures": {"number": 0, "departure": []}}
        board = IRailAPI.parse_liveboard(raw, "008800001")
        self.assertEqual(board.departure_count, 0)
        self.assertEqual(board.departures, [])

    def test_parse_liveboard_malformed_departure_skipped(self):
        raw = {
            "timestamp": "1712500000",
            "station": "Test",
            "stationinfo": {},
            "departures": {
                "number": 1,
                "departure": [
                    {"time": "not_a_number"}  # will fail int conversion
                ]
            }
        }
        board = IRailAPI.parse_liveboard(raw, "008800001")
        self.assertEqual(board.departure_count, 0)


class TestConnectionString(unittest.TestCase):
    """Test connection string parsing."""

    def test_parse_bootstrap_server(self):
        conn = "BootstrapServer=localhost:9092;EntityPath=irail"
        config, topic = _parse_connection_string(conn)
        self.assertEqual(config["bootstrap.servers"], "localhost:9092")
        self.assertEqual(topic, "irail")

    def test_parse_event_hubs(self):
        conn = "Endpoint=sb://mynamespace.servicebus.windows.net/;SharedAccessKeyName=send;SharedAccessKey=abc123=;EntityPath=irail"
        config, topic = _parse_connection_string(conn)
        self.assertIn("bootstrap.servers", config)
        self.assertEqual(topic, "irail")
        self.assertEqual(config["sasl.username"], "$ConnectionString")
        self.assertEqual(config["security.protocol"], "SASL_SSL")


class TestDataClassSerialization(unittest.TestCase):
    """Test that generated data classes serialize/deserialize correctly."""

    def test_station_roundtrip(self):
        from irail_producer_data.be.irail.station import Station
        station = Station(
            station_id="008814001", name="Brussels-South",
            standard_name="Bruxelles-Midi / Brussel-Zuid",
            longitude=4.336531, latitude=50.835707,
            uri="http://irail.be/stations/NMBS/008814001"
        )
        d = station.to_serializer_dict()
        self.assertEqual(d["station_id"], "008814001")
        station2 = Station.from_serializer_dict(d)
        self.assertEqual(station2.station_id, "008814001")

    def test_departure_roundtrip(self):
        from irail_producer_data.be.irail.departure import Departure
        dep = Departure(
            destination_station_id="008821006", destination_name="Antwerp-Central",
            scheduled_time="2026-04-07T18:00:00+00:00", delay_seconds=300,
            is_canceled=False, has_left=False, is_extra_stop=False,
            vehicle_id="BE.NMBS.IC2117", vehicle_short_name="IC 2117",
            vehicle_type="IC", vehicle_number="2117",
            platform="13", is_normal_platform=True,
            occupancy="low",
            departure_connection_uri="http://irail.be/connections/8814001/20260407/IC2117"
        )
        d = dep.to_serializer_dict()
        self.assertEqual(d["delay_seconds"], 300)
        dep2 = Departure.from_serializer_dict(d)
        self.assertEqual(dep2.vehicle_type, "IC")

    def test_stationboard_roundtrip(self):
        from irail_producer_data.be.irail.stationboard import StationBoard
        from irail_producer_data.be.irail.departure import Departure
        dep = Departure(
            destination_station_id="008821006", destination_name="Antwerp-Central",
            scheduled_time="2026-04-07T18:00:00+00:00", delay_seconds=0,
            is_canceled=False, has_left=False, is_extra_stop=False,
            vehicle_id="BE.NMBS.IC2117", vehicle_short_name="IC 2117",
            vehicle_type="IC", vehicle_number="2117",
            platform=None, is_normal_platform=True,
            occupancy="unknown",
            departure_connection_uri="http://irail.be/connections/8814001/20260407/IC2117"
        )
        board = StationBoard(
            station_id="008814001", station_name="Brussels-South",
            retrieved_at="2026-04-07T18:00:00+00:00", departure_count=1,
            departures=[dep]
        )
        d = board.to_serializer_dict()
        self.assertEqual(d["departure_count"], 1)
        self.assertEqual(len(d["departures"]), 1)
        self.assertEqual(d["departures"][0]["vehicle_type"], "IC")

    def test_station_avro_roundtrip(self):
        from irail_producer_data.be.irail.station import Station
        station = Station(
            station_id="008814001", name="Brussels-South",
            standard_name="Bruxelles-Midi", longitude=4.33, latitude=50.83,
            uri="http://irail.be/stations/NMBS/008814001"
        )
        avro_bytes = station.to_byte_array("avro/binary")
        station2 = Station.from_data(avro_bytes, "avro/binary")
        self.assertEqual(station2.station_id, "008814001")

    def test_departure_null_platform_serialization(self):
        from irail_producer_data.be.irail.departure import Departure
        dep = Departure(
            destination_station_id="008821006", destination_name="Antwerp",
            scheduled_time="2026-04-07T18:00:00+00:00", delay_seconds=0,
            is_canceled=False, has_left=False, is_extra_stop=False,
            vehicle_id="BE.NMBS.IC1", vehicle_short_name="IC 1",
            vehicle_type="IC", vehicle_number="1",
            platform=None, is_normal_platform=True,
            occupancy="unknown",
            departure_connection_uri=""
        )
        d = dep.to_serializer_dict()
        self.assertIsNone(d["platform"])
        avro_bytes = dep.to_byte_array("avro/binary")
        dep2 = Departure.from_data(avro_bytes, "avro/binary")
        self.assertIsNone(dep2.platform)


class TestFetchStations(unittest.TestCase):
    """Test API fetch methods with mocking."""

    @patch("irail.irail.requests.Session")
    def test_fetch_stations(self, mock_session_cls):
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = SAMPLE_STATIONS_RESPONSE
        mock_response.raise_for_status = MagicMock()
        mock_session.get.return_value = mock_response
        mock_session_cls.return_value = mock_session

        api = IRailAPI()
        api.session = mock_session
        stations = api.fetch_stations()
        self.assertEqual(len(stations), 2)
        self.assertEqual(stations[0]["id"], "BE.NMBS.008814001")

    @patch("irail.irail.requests.Session")
    def test_fetch_liveboard_404(self, mock_session_cls):
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_session.get.return_value = mock_response
        mock_session_cls.return_value = mock_session

        api = IRailAPI()
        api.session = mock_session
        result = api.fetch_liveboard("008814001")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
