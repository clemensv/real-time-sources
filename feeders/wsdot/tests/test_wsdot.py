"""Tests for the WSDOT bridge."""

import json
from argparse import Namespace
from unittest.mock import MagicMock, patch

import pytest

from wsdot.wsdot import (
    feed,
    WSDOTApi,
    _parse_connection_string,
    _parse_wcf_date,
    _FLOW_READING_MAP,
    _emit_batch,
)


# ---------------------------------------------------------------------------
# Sample upstream payloads
# ---------------------------------------------------------------------------

SAMPLE_FLOW_DATA = {
    "FlowDataID": 1234,
    "StationName": "I-5 at Seneca",
    "Region": "Northwest",
    "FlowReadingValue": 1,
    "Time": "/Date(1617235200000)/",
    "FlowStationLocation": {
        "Description": "I-5 at Seneca St",
        "RoadName": "I-5",
        "Direction": "NB",
        "MilePost": 167.52,
        "Latitude": 47.6062,
        "Longitude": -122.3321,
    },
}

SAMPLE_FLOW_NO_LOCATION = {
    "FlowDataID": 5678,
    "StationName": "SR 520 at Montlake",
    "Region": "Northwest",
    "FlowReadingValue": 3,
    "Time": "/Date(1617235260000-0700)/",
    "FlowStationLocation": None,
}

SAMPLE_FLOW_EMPTY_DIRECTION = {
    "FlowDataID": 9999,
    "StationName": "I-90 at Mercer Island",
    "Region": "Northwest",
    "FlowReadingValue": 0,
    "Time": "/Date(1617235320000)/",
    "FlowStationLocation": {
        "Description": None,
        "RoadName": "I-90",
        "Direction": "",
        "MilePost": None,
        "Latitude": 47.5872,
        "Longitude": -122.2296,
    },
}


# ---------------------------------------------------------------------------
# WCF date parsing
# ---------------------------------------------------------------------------

class TestParseWcfDate:
    def test_basic_date(self):
        result = _parse_wcf_date("/Date(1617235200000)/")
        assert result == "2021-04-01T00:00:00+00:00"

    def test_date_with_offset(self):
        # The offset in WCF dates is display-only; millis are always UTC-based
        result = _parse_wcf_date("/Date(1617235200000-0700)/")
        assert result == "2021-04-01T00:00:00+00:00"

    def test_zero_epoch(self):
        result = _parse_wcf_date("/Date(0)/")
        assert result == "1970-01-01T00:00:00+00:00"

    def test_invalid_format(self):
        result = _parse_wcf_date("not a date")
        assert result == "not a date"

    def test_empty_string(self):
        result = _parse_wcf_date("")
        assert result == ""


# ---------------------------------------------------------------------------
# Flow reading value mapping
# ---------------------------------------------------------------------------

class TestFlowReadingMap:
    def test_all_values(self):
        expected = {
            0: "Unknown",
            1: "WideOpen",
            2: "Moderate",
            3: "Heavy",
            4: "StopAndGo",
            5: "NoData",
        }
        assert _FLOW_READING_MAP == expected

    def test_out_of_range(self):
        assert _FLOW_READING_MAP.get(99, "Unknown") == "Unknown"


# ---------------------------------------------------------------------------
# Station parsing
# ---------------------------------------------------------------------------

class TestParseStation:
    def test_full_record(self):
        station = WSDOTApi.parse_station(SAMPLE_FLOW_DATA)
        assert station.flow_data_id == "1234"
        assert station.station_name == "I-5 at Seneca"
        assert station.region == "Northwest"
        assert station.description == "I-5 at Seneca St"
        assert station.road_name == "I-5"
        assert station.direction == "NB"
        assert station.milepost == pytest.approx(167.52)
        assert station.latitude == pytest.approx(47.6062)
        assert station.longitude == pytest.approx(-122.3321)

    def test_null_location(self):
        station = WSDOTApi.parse_station(SAMPLE_FLOW_NO_LOCATION)
        assert station.flow_data_id == "5678"
        assert station.station_name == "SR 520 at Montlake"
        assert station.description is None
        assert station.road_name == ""
        assert station.direction is None
        assert station.milepost is None
        assert station.latitude == 0.0
        assert station.longitude == 0.0

    def test_empty_direction_treated_as_null(self):
        station = WSDOTApi.parse_station(SAMPLE_FLOW_EMPTY_DIRECTION)
        assert station.direction is None
        assert station.description is None
        assert station.milepost is None

    def test_flow_data_id_is_string(self):
        station = WSDOTApi.parse_station(SAMPLE_FLOW_DATA)
        assert isinstance(station.flow_data_id, str)


# ---------------------------------------------------------------------------
# Reading parsing
# ---------------------------------------------------------------------------

class TestParseReading:
    def test_full_record(self):
        reading = WSDOTApi.parse_reading(SAMPLE_FLOW_DATA)
        assert reading.flow_data_id == "1234"
        assert reading.station_name == "I-5 at Seneca"
        assert reading.region == "Northwest"
        assert reading.flow_reading == "WideOpen"
        assert reading.reading_time == "2021-04-01T00:00:00+00:00"

    def test_heavy_traffic(self):
        reading = WSDOTApi.parse_reading(SAMPLE_FLOW_NO_LOCATION)
        assert reading.flow_reading == "Heavy"

    def test_unknown_reading(self):
        reading = WSDOTApi.parse_reading(SAMPLE_FLOW_EMPTY_DIRECTION)
        assert reading.flow_reading == "Unknown"

    def test_all_flow_values(self):
        for byte_val, expected_str in _FLOW_READING_MAP.items():
            raw = {**SAMPLE_FLOW_DATA, "FlowReadingValue": byte_val}
            reading = WSDOTApi.parse_reading(raw)
            assert reading.flow_reading == expected_str

    def test_out_of_range_flow_value(self):
        raw = {**SAMPLE_FLOW_DATA, "FlowReadingValue": 99}
        reading = WSDOTApi.parse_reading(raw)
        assert reading.flow_reading == "Unknown"

    def test_reading_time_parsed(self):
        reading = WSDOTApi.parse_reading(SAMPLE_FLOW_DATA)
        assert "T" in reading.reading_time
        assert "+00:00" in reading.reading_time

    def test_flow_data_id_is_string(self):
        reading = WSDOTApi.parse_reading(SAMPLE_FLOW_DATA)
        assert isinstance(reading.flow_data_id, str)


# ---------------------------------------------------------------------------
# Connection string parsing
# ---------------------------------------------------------------------------

class TestParseConnectionString:
    def test_plain_kafka(self):
        config, topic = _parse_connection_string(
            "BootstrapServer=localhost:9092;EntityPath=wsdot"
        )
        assert config["bootstrap.servers"] == "localhost:9092"
        assert topic == "wsdot"

    def test_event_hubs(self):
        conn = (
            "Endpoint=sb://myns.servicebus.windows.net/;"
            "SharedAccessKeyName=policy;"
            "SharedAccessKey=secret123;"
            "EntityPath=wsdot"
        )
        config, topic = _parse_connection_string(conn)
        assert "myns.servicebus.windows.net" in config["bootstrap.servers"]
        assert topic == "wsdot"
        assert config["security.protocol"] == "SASL_SSL"
        assert config["sasl.mechanism"] == "PLAIN"

    def test_missing_topic(self):
        config, topic = _parse_connection_string("BootstrapServer=localhost:9092")
        assert topic is None


# ---------------------------------------------------------------------------
# API client
# ---------------------------------------------------------------------------

class TestWSDOTApiClient:
    def test_fetch_traffic_flows(self):
        api = WSDOTApi(access_code="test-key")
        with patch.object(api.session, "get") as mock_get:
            mock_resp = MagicMock()
            mock_resp.json.return_value = [SAMPLE_FLOW_DATA]
            mock_resp.raise_for_status = MagicMock()
            mock_get.return_value = mock_resp

            flows = api.fetch_traffic_flows()
            assert len(flows) == 1
            assert flows[0]["FlowDataID"] == 1234

            # Verify access code is passed
            call_kwargs = mock_get.call_args
            assert call_kwargs[1]["params"]["AccessCode"] == "test-key"

    def test_api_url(self):
        api = WSDOTApi(access_code="test-key")
        with patch.object(api.session, "get") as mock_get:
            mock_resp = MagicMock()
            mock_resp.json.return_value = []
            mock_resp.raise_for_status = MagicMock()
            mock_get.return_value = mock_resp

            api.fetch_traffic_flows()
            call_args = mock_get.call_args[0][0]
            assert "TrafficFlow" in call_args
            assert "GetTrafficFlowsAsJson" in call_args


# ---------------------------------------------------------------------------
# Data class serialization
# ---------------------------------------------------------------------------

class TestDataClassSerialization:
    def test_station_to_json(self):
        station = WSDOTApi.parse_station(SAMPLE_FLOW_DATA)
        json_str = station.to_json()
        data = json.loads(json_str)
        assert data["flow_data_id"] == "1234"
        assert data["station_name"] == "I-5 at Seneca"
        assert data["latitude"] == pytest.approx(47.6062)

    def test_reading_to_json(self):
        reading = WSDOTApi.parse_reading(SAMPLE_FLOW_DATA)
        json_str = reading.to_json()
        data = json.loads(json_str)
        assert data["flow_data_id"] == "1234"
        assert data["flow_reading"] == "WideOpen"

    def test_station_nullable_fields_in_json(self):
        station = WSDOTApi.parse_station(SAMPLE_FLOW_NO_LOCATION)
        json_str = station.to_json()
        data = json.loads(json_str)
        assert data["description"] is None
        assert data["direction"] is None
        assert data["milepost"] is None

    def test_station_roundtrip(self):
        station = WSDOTApi.parse_station(SAMPLE_FLOW_DATA)
        json_str = station.to_json()
        restored = station.from_json(json_str)
        assert restored.flow_data_id == station.flow_data_id
        assert restored.latitude == station.latitude

    def test_reading_roundtrip(self):
        reading = WSDOTApi.parse_reading(SAMPLE_FLOW_DATA)
        json_str = reading.to_json()
        restored = reading.from_json(json_str)
        assert restored.flow_data_id == reading.flow_data_id
        assert restored.flow_reading == reading.flow_reading


# ---------------------------------------------------------------------------
# Sample payloads for new channels
# ---------------------------------------------------------------------------

SAMPLE_TRAVEL_TIME = {
    "TravelTimeID": 42,
    "Name": "Everett-Seattle HOV",
    "Description": "Everett to Downtown Seattle using HOV lanes",
    "Distance": 30.5,
    "AverageTime": 35,
    "CurrentTime": 42,
    "TimeUpdated": "/Date(1617235200000)/",
    "StartPoint": {
        "Description": "I-5 @ 41st St in Everett",
        "RoadName": "I-5",
        "Direction": "SB",
        "MilePost": 192.0,
        "Latitude": 47.978,
        "Longitude": -122.202,
    },
    "EndPoint": {
        "Description": "I-5 @ University St in Seattle",
        "RoadName": "I-5",
        "Direction": "SB",
        "MilePost": 165.5,
        "Latitude": 47.607,
        "Longitude": -122.334,
    },
}

SAMPLE_MOUNTAIN_PASS = {
    "MountainPassId": 1,
    "MountainPassName": "Snoqualmie Pass I-90",
    "ElevationInFeet": 3022,
    "Latitude": 47.3925,
    "Longitude": -121.4097,
    "TemperatureInFahrenheit": 38,
    "WeatherCondition": "Rain",
    "RoadCondition": "Wet",
    "TravelAdvisoryActive": True,
    "RestrictionOne": {
        "TravelDirection": "Eastbound",
        "RestrictionText": "Traction tires advised",
    },
    "RestrictionTwo": {
        "TravelDirection": "Westbound",
        "RestrictionText": "No restrictions",
    },
    "DateUpdated": "/Date(1617235200000)/",
}

SAMPLE_WEATHER_STATION = {
    "StationCode": 504,
    "StationName": "S 144th St on SB I-5 at mp 155.32",
    "Latitude": 47.458,
    "Longitude": -122.267,
}

SAMPLE_WEATHER_READING = {
    "StationID": 504,
    "StationName": "S 144th St on SB I-5 at mp 155.32",
    "ReadingTime": "/Date(1617235200000)/",
    "TemperatureInFahrenheit": 52.3,
    "PrecipitationInInches": None,
    "WindSpeedInMPH": 8,
    "WindGustSpeedInMPH": 15,
    "WindDirection": 180,
    "WindDirectionCardinal": "S",
    "BarometricPressure": 1013.25,
    "RelativeHumidity": 72,
    "Visibility": 10.0,
    "SkyCoverage": "Overcast",
    "Latitude": 47.458,
    "Longitude": -122.267,
}

SAMPLE_TOLL_RATE = {
    "TripName": "099tp03268",
    "StateRoute": "099",
    "TravelDirection": "N",
    "CurrentToll": 155,
    "CurrentMessage": None,
    "TimeUpdated": "/Date(1617235200000)/",
    "StartLocationName": "SB S Portal",
    "StartLatitude": 47.543,
    "StartLongitude": -122.335,
    "StartMilepost": 32.68,
    "EndLocationName": "NB S Portal",
    "EndLatitude": 47.589,
    "EndLongitude": -122.339,
    "EndMilepost": 35.10,
}

SAMPLE_CV_RESTRICTION = {
    "StateRouteID": "SR 10",
    "BridgeNumber": "10/142",
    "BridgeName": "Teanaway River",
    "RestrictionType": "BridgeRestriction",
    "VehicleType": "All commercial vehicles",
    "RestrictionWeightInPounds": 40000,
    "MaximumGrossVehicleWeightInPounds": 80000,
    "RestrictionHeightInInches": None,
    "RestrictionWidthInInches": None,
    "RestrictionLengthInInches": None,
    "IsPermanentRestriction": True,
    "IsWarning": False,
    "IsDetourAvailable": True,
    "IsExceptionsAllowed": False,
    "RestrictionComment": "Max 40,000 lbs per axle",
    "DatePosted": "/Date(1514764800000)/",
    "DateEffective": "/Date(1514764800000)/",
    "DateExpires": "/Date(4102444800000)/",
    "StartRoadwayLocation": {
        "Description": "1.3 E Jct SR 970",
        "RoadName": "SR 10",
        "Latitude": 47.215,
        "Longitude": -120.795,
        "State": "WA",
    },
    "EndRoadwayLocation": {
        "Latitude": 47.22,
        "Longitude": -120.78,
    },
}

SAMPLE_BORDER_CROSSING = {
    "CrossingName": "I5",
    "WaitTime": 15,
    "Time": "/Date(1617235200000)/",
    "BorderCrossingLocation": {
        "Description": "I-5 General Purpose",
        "RoadName": "I-5",
        "Latitude": 48.999,
        "Longitude": -122.757,
    },
}

SAMPLE_VESSEL_LOCATION = {
    "VesselID": 7,
    "VesselName": "Chelan",
    "Mmsi": 366772000,
    "InService": True,
    "AtDock": False,
    "Latitude": 48.509,
    "Longitude": -122.673,
    "Speed": 15.8,
    "Heading": 315,
    "DepartingTerminalID": 1,
    "DepartingTerminalName": "Anacortes",
    "DepartingTerminalAbbrev": "ANA",
    "ArrivingTerminalID": 10,
    "ArrivingTerminalName": "Friday Harbor",
    "ArrivingTerminalAbbrev": "FRH",
    "ScheduledDeparture": "/Date(1617235200000)/",
    "LeftDock": "/Date(1617235260000)/",
    "Eta": "/Date(1617238800000)/",
    "EtaBasis": "Vessel Chelan departed Anacortes going to Friday Harbor",
    "OpRouteAbbrev": ["ana-sj"],
    "TimeStamp": "/Date(1617236000000)/",
}


# ---------------------------------------------------------------------------
# Travel Time parsing
# ---------------------------------------------------------------------------

class TestParseTravelTime:
    def test_full_record(self):
        tt = WSDOTApi.parse_travel_time(SAMPLE_TRAVEL_TIME)
        assert tt.travel_time_id == "42"
        assert tt.name == "Everett-Seattle HOV"
        assert tt.distance == pytest.approx(30.5)
        assert tt.average_time == 35
        assert tt.current_time == 42
        assert tt.start_latitude == pytest.approx(47.978)
        assert tt.end_road_name == "I-5"
        assert "T" in tt.time_updated

    def test_null_start_point(self):
        raw = {**SAMPLE_TRAVEL_TIME, "StartPoint": None}
        tt = WSDOTApi.parse_travel_time(raw)
        assert tt.start_description is None
        assert tt.start_latitude == 0.0

    def test_id_is_string(self):
        tt = WSDOTApi.parse_travel_time(SAMPLE_TRAVEL_TIME)
        assert isinstance(tt.travel_time_id, str)

    def test_serialization(self):
        tt = WSDOTApi.parse_travel_time(SAMPLE_TRAVEL_TIME)
        data = json.loads(tt.to_json())
        assert data["travel_time_id"] == "42"
        assert data["distance"] == pytest.approx(30.5)


# ---------------------------------------------------------------------------
# Mountain Pass parsing
# ---------------------------------------------------------------------------

class TestParseMountainPass:
    def test_full_record(self):
        mp = WSDOTApi.parse_mountain_pass(SAMPLE_MOUNTAIN_PASS)
        assert mp.mountain_pass_id == "1"
        assert mp.mountain_pass_name == "Snoqualmie Pass I-90"
        assert mp.elevation_in_feet == 3022
        assert mp.temperature_in_fahrenheit == 38
        assert mp.weather_condition == "Rain"
        assert mp.road_condition == "Wet"
        assert mp.travel_advisory_active is True
        assert mp.restriction_one_direction == "Eastbound"
        assert mp.restriction_one_text == "Traction tires advised"
        assert mp.restriction_two_direction == "Westbound"

    def test_null_temperature(self):
        raw = {**SAMPLE_MOUNTAIN_PASS, "TemperatureInFahrenheit": None}
        mp = WSDOTApi.parse_mountain_pass(raw)
        assert mp.temperature_in_fahrenheit is None

    def test_null_restrictions(self):
        raw = {**SAMPLE_MOUNTAIN_PASS, "RestrictionOne": None, "RestrictionTwo": None}
        mp = WSDOTApi.parse_mountain_pass(raw)
        assert mp.restriction_one_direction is None
        assert mp.restriction_two_text is None

    def test_serialization(self):
        mp = WSDOTApi.parse_mountain_pass(SAMPLE_MOUNTAIN_PASS)
        data = json.loads(mp.to_json())
        assert data["elevation_in_feet"] == 3022
        assert data["travel_advisory_active"] is True


# ---------------------------------------------------------------------------
# Weather Station parsing
# ---------------------------------------------------------------------------

class TestParseWeatherStation:
    def test_full_record(self):
        ws = WSDOTApi.parse_weather_station(SAMPLE_WEATHER_STATION)
        assert ws.station_id == "504"
        assert ws.station_name == "S 144th St on SB I-5 at mp 155.32"
        assert ws.latitude == pytest.approx(47.458)

    def test_id_is_string(self):
        ws = WSDOTApi.parse_weather_station(SAMPLE_WEATHER_STATION)
        assert isinstance(ws.station_id, str)


# ---------------------------------------------------------------------------
# Weather Reading parsing
# ---------------------------------------------------------------------------

class TestParseWeatherReading:
    def test_full_record(self):
        wr = WSDOTApi.parse_weather_reading(SAMPLE_WEATHER_READING)
        assert wr.station_id == "504"
        assert wr.temperature_in_fahrenheit == pytest.approx(52.3)
        assert wr.precipitation_in_inches is None
        assert wr.wind_speed_in_mph == pytest.approx(8.0)
        assert wr.wind_direction == 180
        assert wr.wind_direction_cardinal == "S"
        assert wr.barometric_pressure == pytest.approx(1013.25)
        assert wr.relative_humidity == 72
        assert wr.sky_coverage == "Overcast"
        assert "T" in wr.reading_time

    def test_all_null_sensors(self):
        raw = {
            "StationID": 1, "StationName": "Test", "ReadingTime": "/Date(0)/",
            "TemperatureInFahrenheit": None, "PrecipitationInInches": None,
            "WindSpeedInMPH": None, "WindGustSpeedInMPH": None,
            "WindDirection": None, "WindDirectionCardinal": None,
            "BarometricPressure": None, "RelativeHumidity": None,
            "Visibility": None, "SkyCoverage": None,
            "Latitude": 0.0, "Longitude": 0.0,
        }
        wr = WSDOTApi.parse_weather_reading(raw)
        assert wr.temperature_in_fahrenheit is None
        assert wr.wind_speed_in_mph is None
        assert wr.barometric_pressure is None

    def test_serialization(self):
        wr = WSDOTApi.parse_weather_reading(SAMPLE_WEATHER_READING)
        data = json.loads(wr.to_json())
        assert data["station_id"] == "504"
        assert data["temperature_in_fahrenheit"] == pytest.approx(52.3)


# ---------------------------------------------------------------------------
# Toll Rate parsing
# ---------------------------------------------------------------------------

class TestParseTollRate:
    def test_full_record(self):
        tr = WSDOTApi.parse_toll_rate(SAMPLE_TOLL_RATE)
        assert tr.trip_name == "099tp03268"
        assert tr.state_route == "099"
        assert tr.travel_direction == "N"
        assert tr.current_toll == 155
        assert tr.current_message is None
        assert tr.start_location_name == "SB S Portal"
        assert tr.start_milepost == pytest.approx(32.68)
        assert "T" in tr.time_updated

    def test_with_message(self):
        raw = {**SAMPLE_TOLL_RATE, "CurrentMessage": "Toll suspended"}
        tr = WSDOTApi.parse_toll_rate(raw)
        assert tr.current_message == "Toll suspended"

    def test_serialization(self):
        tr = WSDOTApi.parse_toll_rate(SAMPLE_TOLL_RATE)
        data = json.loads(tr.to_json())
        assert data["current_toll"] == 155


# ---------------------------------------------------------------------------
# CV Restriction parsing
# ---------------------------------------------------------------------------

class TestParseCVRestriction:
    def test_full_record(self):
        cv = WSDOTApi.parse_cv_restriction(SAMPLE_CV_RESTRICTION)
        assert cv.state_route_id == "SR 10"
        assert cv.bridge_number == "10/142"
        assert cv.bridge_name == "Teanaway River"
        assert cv.restriction_weight_in_pounds == 40000
        assert cv.maximum_gross_vehicle_weight_in_pounds == 80000
        assert cv.is_permanent_restriction is True
        assert cv.is_warning is False
        assert cv.latitude == pytest.approx(47.215)

    def test_null_dimensions(self):
        cv = WSDOTApi.parse_cv_restriction(SAMPLE_CV_RESTRICTION)
        assert cv.restriction_height_in_inches is None
        assert cv.restriction_width_in_inches is None
        assert cv.restriction_length_in_inches is None

    def test_dates_parsed(self):
        cv = WSDOTApi.parse_cv_restriction(SAMPLE_CV_RESTRICTION)
        assert cv.date_posted is not None
        assert "T" in cv.date_posted

    def test_serialization(self):
        cv = WSDOTApi.parse_cv_restriction(SAMPLE_CV_RESTRICTION)
        data = json.loads(cv.to_json())
        assert data["state_route_id"] == "SR 10"
        assert data["bridge_number"] == "10/142"


# ---------------------------------------------------------------------------
# Border Crossing parsing
# ---------------------------------------------------------------------------

class TestParseBorderCrossing:
    def test_full_record(self):
        bc = WSDOTApi.parse_border_crossing(SAMPLE_BORDER_CROSSING)
        assert bc.crossing_name == "I5"
        assert bc.wait_time == 15
        assert bc.description == "I-5 General Purpose"
        assert bc.road_name == "I-5"
        assert bc.latitude == pytest.approx(48.999)
        assert "T" in bc.time

    def test_null_wait_time(self):
        raw = {**SAMPLE_BORDER_CROSSING, "WaitTime": None}
        bc = WSDOTApi.parse_border_crossing(raw)
        assert bc.wait_time is None

    def test_null_location(self):
        raw = {**SAMPLE_BORDER_CROSSING, "BorderCrossingLocation": None}
        bc = WSDOTApi.parse_border_crossing(raw)
        assert bc.description is None
        assert bc.latitude == 0.0

    def test_serialization(self):
        bc = WSDOTApi.parse_border_crossing(SAMPLE_BORDER_CROSSING)
        data = json.loads(bc.to_json())
        assert data["crossing_name"] == "I5"
        assert data["wait_time"] == 15


# ---------------------------------------------------------------------------
# Vessel Location parsing
# ---------------------------------------------------------------------------

class TestParseVesselLocation:
    def test_full_record(self):
        vl = WSDOTApi.parse_vessel_location(SAMPLE_VESSEL_LOCATION)
        assert vl.vessel_id == "7"
        assert vl.vessel_name == "Chelan"
        assert vl.mmsi == 366772000
        assert vl.in_service is True
        assert vl.at_dock is False
        assert vl.speed == pytest.approx(15.8)
        assert vl.heading == 315
        assert vl.departing_terminal_name == "Anacortes"
        assert vl.arriving_terminal_abbrev == "FRH"
        assert vl.route_abbreviation == "ana-sj"
        assert "T" in vl.timestamp
        assert "T" in vl.scheduled_departure
        assert vl.eta_basis is not None

    def test_out_of_service_vessel(self):
        raw = {
            **SAMPLE_VESSEL_LOCATION,
            "InService": False,
            "AtDock": True,
            "Speed": None,
            "Heading": None,
            "DepartingTerminalID": None,
            "DepartingTerminalName": None,
            "DepartingTerminalAbbrev": None,
            "ArrivingTerminalID": None,
            "ArrivingTerminalName": None,
            "ArrivingTerminalAbbrev": None,
            "ScheduledDeparture": None,
            "LeftDock": None,
            "Eta": None,
            "EtaBasis": None,
            "OpRouteAbbrev": [],
        }
        vl = WSDOTApi.parse_vessel_location(raw)
        assert vl.in_service is False
        assert vl.at_dock is True
        assert vl.speed is None
        assert vl.heading is None
        assert vl.route_abbreviation is None

    def test_id_is_string(self):
        vl = WSDOTApi.parse_vessel_location(SAMPLE_VESSEL_LOCATION)
        assert isinstance(vl.vessel_id, str)

    def test_serialization(self):
        vl = WSDOTApi.parse_vessel_location(SAMPLE_VESSEL_LOCATION)
        data = json.loads(vl.to_json())
        assert data["vessel_id"] == "7"
        assert data["vessel_name"] == "Chelan"
        assert data["mmsi"] == 366772000


# ---------------------------------------------------------------------------
# API client extended methods
# ---------------------------------------------------------------------------

class TestWSDOTApiExtended:
    def _mock_api_call(self, api, method_name, return_data):
        with patch.object(api.session, "get") as mock_get:
            mock_resp = MagicMock()
            mock_resp.json.return_value = return_data
            mock_resp.raise_for_status = MagicMock()
            mock_get.return_value = mock_resp
            method = getattr(api, method_name)
            result = method()
            return result, mock_get

    def test_fetch_travel_times(self):
        api = WSDOTApi(access_code="test-key")
        result, mock_get = self._mock_api_call(api, "fetch_travel_times", [SAMPLE_TRAVEL_TIME])
        assert len(result) == 1
        call_url = mock_get.call_args[0][0]
        assert "TravelTimes" in call_url

    def test_fetch_mountain_pass_conditions(self):
        api = WSDOTApi(access_code="test-key")
        result, mock_get = self._mock_api_call(api, "fetch_mountain_pass_conditions", [SAMPLE_MOUNTAIN_PASS])
        assert len(result) == 1
        call_url = mock_get.call_args[0][0]
        assert "MountainPassConditions" in call_url

    def test_fetch_weather_information_uses_current_endpoint(self):
        api = WSDOTApi(access_code="test-key")
        result, mock_get = self._mock_api_call(api, "fetch_weather_information", [SAMPLE_WEATHER_READING])
        assert len(result) == 1
        call_url = mock_get.call_args[0][0]
        assert "WeatherInformation" in call_url
        assert "GetCurrentWeatherInformationAsJson" in call_url

    def test_fetch_toll_rates(self):
        api = WSDOTApi(access_code="test-key")
        result, _ = self._mock_api_call(api, "fetch_toll_rates", [SAMPLE_TOLL_RATE])
        assert len(result) == 1

    def test_fetch_border_crossings(self):
        api = WSDOTApi(access_code="test-key")
        result, _ = self._mock_api_call(api, "fetch_border_crossings", [SAMPLE_BORDER_CROSSING])
        assert len(result) == 1

    def test_fetch_vessel_locations(self):
        api = WSDOTApi(access_code="test-key")
        result, mock_get = self._mock_api_call(api, "fetch_vessel_locations", [SAMPLE_VESSEL_LOCATION])
        assert len(result) == 1
        call_url = mock_get.call_args[0][0]
        assert "ferries" in call_url
        assert mock_get.call_args[1]["params"]["apiaccesscode"] == "test-key"


class TestFeedProducerRouting:
    def test_feed_uses_group_specific_producers(self):
        sent = []

        class FakeTrafficProducer:
            def __init__(self, *_args, **_kwargs):
                pass

            def send_us_wa_wsdot_traffic_traffic_flow_station(self, **_kwargs):
                sent.append("traffic_station")

            def send_us_wa_wsdot_traffic_traffic_flow_reading(self, **_kwargs):
                sent.append("traffic_reading")

        class FakeTraveltimesProducer:
            def __init__(self, *_args, **_kwargs):
                pass

            def send_us_wa_wsdot_traveltimes_travel_time_route(self, **_kwargs):
                sent.append("travel_time")

        class FakeMountainpassProducer:
            def __init__(self, *_args, **_kwargs):
                pass

            def send_us_wa_wsdot_mountainpass_mountain_pass_condition(self, **_kwargs):
                sent.append("mountain_pass")

        class FakeWeatherProducer:
            def __init__(self, *_args, **_kwargs):
                pass

            def send_us_wa_wsdot_weather_weather_station(self, **_kwargs):
                sent.append("weather_station")

            def send_us_wa_wsdot_weather_weather_reading(self, **_kwargs):
                sent.append("weather_reading")

        class FakeTollsProducer:
            def __init__(self, *_args, **_kwargs):
                pass

            def send_us_wa_wsdot_tolls_toll_rate(self, **_kwargs):
                sent.append("toll_rate")

        class FakeCvRestrictionsProducer:
            def __init__(self, *_args, **_kwargs):
                pass

            def send_us_wa_wsdot_cvrestrictions_commercial_vehicle_restriction(self, **_kwargs):
                sent.append("cv_restriction")

        class FakeBorderProducer:
            def __init__(self, *_args, **_kwargs):
                pass

            def send_us_wa_wsdot_border_border_crossing(self, **_kwargs):
                sent.append("border_crossing")

        class FakeFerriesProducer:
            def __init__(self, *_args, **_kwargs):
                pass

            def send_us_wa_wsdot_ferries_vessel_location(self, **_kwargs):
                sent.append("vessel_location")

        fake_kafka_producer = MagicMock()

        args = Namespace(
            connection_string="BootstrapServer=localhost:9092;EntityPath=test-topic",
            access_code="test-key",
            polling_interval="120",
            region_filter="",
        )

        with patch("wsdot.wsdot._parse_connection_string", return_value=({"bootstrap.servers": "localhost:9092"}, "test-topic")), \
             patch("wsdot.wsdot.Producer", return_value=fake_kafka_producer), \
             patch("wsdot.wsdot.UsWaWsdotTrafficEventProducer", FakeTrafficProducer), \
             patch("wsdot.wsdot.UsWaWsdotTraveltimesEventProducer", FakeTraveltimesProducer), \
             patch("wsdot.wsdot.UsWaWsdotMountainpassEventProducer", FakeMountainpassProducer), \
             patch("wsdot.wsdot.UsWaWsdotWeatherEventProducer", FakeWeatherProducer), \
             patch("wsdot.wsdot.UsWaWsdotTollsEventProducer", FakeTollsProducer), \
             patch("wsdot.wsdot.UsWaWsdotCvrestrictionsEventProducer", FakeCvRestrictionsProducer), \
             patch("wsdot.wsdot.UsWaWsdotBorderEventProducer", FakeBorderProducer), \
             patch("wsdot.wsdot.UsWaWsdotFerriesEventProducer", FakeFerriesProducer), \
             patch.object(WSDOTApi, "fetch_traffic_flows", return_value=[SAMPLE_FLOW_DATA]), \
             patch.object(WSDOTApi, "fetch_travel_times", return_value=[SAMPLE_TRAVEL_TIME]), \
             patch.object(WSDOTApi, "fetch_mountain_pass_conditions", return_value=[SAMPLE_MOUNTAIN_PASS]), \
             patch.object(WSDOTApi, "fetch_weather_stations", return_value=[SAMPLE_WEATHER_STATION]), \
             patch.object(WSDOTApi, "fetch_weather_information", return_value=[SAMPLE_WEATHER_READING]), \
             patch.object(WSDOTApi, "fetch_toll_rates", return_value=[SAMPLE_TOLL_RATE]), \
             patch.object(WSDOTApi, "fetch_cv_restrictions", return_value=[SAMPLE_CV_RESTRICTION]), \
             patch.object(WSDOTApi, "fetch_border_crossings", return_value=[SAMPLE_BORDER_CROSSING]), \
             patch.object(WSDOTApi, "fetch_vessel_locations", return_value=[SAMPLE_VESSEL_LOCATION]), \
             patch("wsdot.wsdot.time.sleep", side_effect=KeyboardInterrupt):
            feed(args)

        assert sent == [
            "traffic_station",
            "traffic_reading",
            "travel_time",
            "mountain_pass",
            "weather_station",
            "weather_reading",
            "toll_rate",
            "cv_restriction",
            "border_crossing",
            "vessel_location",
        ]


# ---------------------------------------------------------------------------
# Resilience: _emit_batch per-item errors and partial channel failures
# ---------------------------------------------------------------------------

class TestEmitBatchResilience:
    def test_item_error_does_not_stop_batch(self):
        """A per-item exception inside _emit_batch does not prevent remaining items from being sent."""
        sent = []
        errors = []

        def send_fn(item):
            if item == "bad":
                raise ValueError("bad item")
            sent.append(item)

        producer = MagicMock()
        count = _emit_batch(producer, send_fn, ["ok1", "bad", "ok2"], "test")

        assert sent == ["ok1", "ok2"]
        assert count == 2
        producer.flush.assert_called_once()

    def test_all_items_fail_returns_zero(self):
        """When every item raises, _emit_batch returns 0 and still calls flush."""
        def _always_raise(item):
            raise RuntimeError("fail")

        producer = MagicMock()
        count = _emit_batch(producer, _always_raise, ["a", "b"], "test")
        assert count == 0
        producer.flush.assert_called_once()


class TestPartialChannelFailure:
    """One channel fetch raises; unaffected channels still emit events."""

    def _make_fake_producer(self, sent, event_type):
        class FakeEP:
            def __init__(self, *a, **kw):
                pass
            def __getattr__(self, name):
                def _send(**kwargs):
                    sent.append(event_type)
                return _send
        return FakeEP

    def test_traffic_failure_does_not_prevent_travel_times(self):
        """fetch_traffic_flows raising does not stop travel_time events from being sent."""
        sent = []
        args = Namespace(
            connection_string="BootstrapServer=localhost:9092;EntityPath=test-topic",
            access_code="test-key",
            polling_interval="120",
            region_filter="",
        )

        fake_kafka = MagicMock()

        class FakeTrafficEP:
            def __init__(self, *a, **kw): pass
            def send_us_wa_wsdot_traffic_traffic_flow_station(self, **kw): sent.append("traffic_station")
            def send_us_wa_wsdot_traffic_traffic_flow_reading(self, **kw): sent.append("traffic_reading")

        class FakeTraveltimesEP:
            def __init__(self, *a, **kw): pass
            def send_us_wa_wsdot_traveltimes_travel_time_route(self, **kw): sent.append("travel_time")

        # Remaining producers are silent no-ops
        class _NoOpEP:
            def __init__(self, *a, **kw): pass
            def __getattr__(self, name):
                return lambda **kw: None

        with patch("wsdot.wsdot._parse_connection_string",
                   return_value=({"bootstrap.servers": "localhost:9092"}, "test-topic")), \
             patch("wsdot.wsdot.Producer", return_value=fake_kafka), \
             patch("wsdot.wsdot.UsWaWsdotTrafficEventProducer", FakeTrafficEP), \
             patch("wsdot.wsdot.UsWaWsdotTraveltimesEventProducer", FakeTraveltimesEP), \
             patch("wsdot.wsdot.UsWaWsdotMountainpassEventProducer", _NoOpEP), \
             patch("wsdot.wsdot.UsWaWsdotWeatherEventProducer", _NoOpEP), \
             patch("wsdot.wsdot.UsWaWsdotTollsEventProducer", _NoOpEP), \
             patch("wsdot.wsdot.UsWaWsdotCvrestrictionsEventProducer", _NoOpEP), \
             patch("wsdot.wsdot.UsWaWsdotBorderEventProducer", _NoOpEP), \
             patch("wsdot.wsdot.UsWaWsdotFerriesEventProducer", _NoOpEP), \
             patch.object(WSDOTApi, "fetch_traffic_flows", side_effect=RuntimeError("API down")), \
             patch.object(WSDOTApi, "fetch_travel_times", return_value=[SAMPLE_TRAVEL_TIME]), \
             patch.object(WSDOTApi, "fetch_mountain_pass_conditions", return_value=[]), \
             patch.object(WSDOTApi, "fetch_weather_stations", return_value=[]), \
             patch.object(WSDOTApi, "fetch_weather_information", return_value=[]), \
             patch.object(WSDOTApi, "fetch_toll_rates", return_value=[]), \
             patch.object(WSDOTApi, "fetch_cv_restrictions", return_value=[]), \
             patch.object(WSDOTApi, "fetch_border_crossings", return_value=[]), \
             patch.object(WSDOTApi, "fetch_vessel_locations", return_value=[]), \
             patch("wsdot.wsdot.time.sleep", side_effect=KeyboardInterrupt):
            feed(args)

        # Traffic failed but travel times still emitted
        assert "traffic_station" not in sent
        assert "traffic_reading" not in sent
        assert "travel_time" in sent


class TestReferenceRefreshInterval:
    """Reference data only re-emitted once the 6-hour window has elapsed."""

    def test_reference_not_re_emitted_before_6h(self):
        """With time.sleep mocked to advance < 6 hours, reference events are not re-emitted on the second cycle."""
        reference_sent = []
        telemetry_sent = []

        class FakeTrafficEP:
            def __init__(self, *a, **kw): pass
            def send_us_wa_wsdot_traffic_traffic_flow_station(self, **kw):
                reference_sent.append("traffic_station")
            def send_us_wa_wsdot_traffic_traffic_flow_reading(self, **kw):
                telemetry_sent.append("traffic_reading")

        class _NoOpEP:
            def __init__(self, *a, **kw): pass
            def __getattr__(self, name):
                return lambda **kw: None

        fake_kafka = MagicMock()
        args = Namespace(
            connection_string="BootstrapServer=localhost:9092;EntityPath=test-topic",
            access_code="test-key",
            polling_interval="1",
            region_filter="",
        )

        # Simulate two polling cycles: first sleep does nothing (enters loop a second time),
        # second sleep raises KeyboardInterrupt (exits).
        call_count = [0]

        def _fake_sleep(_t):
            call_count[0] += 1
            if call_count[0] >= 2:
                raise KeyboardInterrupt

        with patch("wsdot.wsdot._parse_connection_string",
                   return_value=({"bootstrap.servers": "localhost:9092"}, "test-topic")), \
             patch("wsdot.wsdot.Producer", return_value=fake_kafka), \
             patch("wsdot.wsdot.UsWaWsdotTrafficEventProducer", FakeTrafficEP), \
             patch("wsdot.wsdot.UsWaWsdotTraveltimesEventProducer", _NoOpEP), \
             patch("wsdot.wsdot.UsWaWsdotMountainpassEventProducer", _NoOpEP), \
             patch("wsdot.wsdot.UsWaWsdotWeatherEventProducer", _NoOpEP), \
             patch("wsdot.wsdot.UsWaWsdotTollsEventProducer", _NoOpEP), \
             patch("wsdot.wsdot.UsWaWsdotCvrestrictionsEventProducer", _NoOpEP), \
             patch("wsdot.wsdot.UsWaWsdotBorderEventProducer", _NoOpEP), \
             patch("wsdot.wsdot.UsWaWsdotFerriesEventProducer", _NoOpEP), \
             patch.object(WSDOTApi, "fetch_traffic_flows", return_value=[SAMPLE_FLOW_DATA]), \
             patch.object(WSDOTApi, "fetch_travel_times", return_value=[]), \
             patch.object(WSDOTApi, "fetch_mountain_pass_conditions", return_value=[]), \
             patch.object(WSDOTApi, "fetch_weather_stations", return_value=[]), \
             patch.object(WSDOTApi, "fetch_weather_information", return_value=[]), \
             patch.object(WSDOTApi, "fetch_toll_rates", return_value=[]), \
             patch.object(WSDOTApi, "fetch_cv_restrictions", return_value=[]), \
             patch.object(WSDOTApi, "fetch_border_crossings", return_value=[]), \
             patch.object(WSDOTApi, "fetch_vessel_locations", return_value=[]), \
             patch("wsdot.wsdot.time.sleep", side_effect=_fake_sleep):
            feed(args)

        # Reference station emitted once (initial batch) but NOT on the second cycle
        # (< 6 h elapsed since the reference was last sent)
        assert reference_sent.count("traffic_station") == 1
        # Telemetry (readings) emitted on both cycles
        assert telemetry_sent.count("traffic_reading") >= 2
