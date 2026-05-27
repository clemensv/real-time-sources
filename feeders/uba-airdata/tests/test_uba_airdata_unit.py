"""Unit tests for the UBA AirData bridge."""

import pytest

from uba_airdata.uba_airdata import UBAAirDataAPI, _measure_feed_url, _measure_date_range


STATIONS_PAYLOAD = {
    "request": {"lang": "en", "recent": False, "index": "id"},
    "indices": [
        "station id", "station code", "station name", "station city", "station synonym",
        "station active from", "station active to", "station longitude", "station latitude",
        "network id", "station setting id", "station type id", "network code", "network name",
        "station setting name", "station setting short name", "station type name",
        "station street", "station street nr", "station zip code"
    ],
    "data": {
        "21": [
            "21", "DEBE021", "Berlin Wedding", "Berlin", "BEWT", "2000-01-01", None,
            "13.3495", "52.5491", "3", "1", "2", "BE", "Berlin",
            "urban area", "urban", "background", "Amrumer Str.", "4-6", "13353"
        ],
        "3": [
            "3", "DEBB003", "Brandenburg a.d. Havel", "Brandenburg", "", "1991-03-01", "2001-06-07",
            "12.5444", "52.4121", "4", "1", "3", "BB", "Brandenburg",
            "urban area", "urban", "traffic", "Gertrud-Pieter-Platz", "9", "14770"
        ],
    },
}

COMPONENTS_PAYLOAD = {
    "count": 2,
    "indices": ["component id", "component code", "component symbol", "component unit", "component name"],
    "1": ["1", "PM10", "PM₁₀", "µg/m³", "Particulate matter"],
    "5": ["5", "NO2", "NO₂", "µg/m³", "Nitrogen dioxide"],
}

MEASURES_PAYLOAD = {
    "request": {"component": "5", "scope": "2", "date_from": "2026-04-07", "date_to": "2026-04-08", "lang": "en"},
    "indices": {"data": {"station id": {"date start": ["component id", "scope id", "value", "date end", "index"]}}},
    "data": {
        "21": {
            "2026-04-07 12:00:00": [5, 2, 4, "2026-04-07 13:00:00", "0"],
            "2026-04-07 13:00:00": [5, 2, None, "2026-04-07 14:00:00", "1"],
        },
        "3": {
            "2026-04-07 12:00:00": [5, 2, 99, "2026-04-07 13:00:00", "0"],
        },
    },
}


@pytest.mark.unit
class TestUBAAirDataAPIInitialization:
    """Test client initialization."""

    def test_init_sets_defaults(self):
        api = UBAAirDataAPI()
        assert api.base_url.endswith("/api/air_data/v3")
        assert api.polling_interval == 3600
        assert api.scope_id == 2
        assert api.session is not None


@pytest.mark.unit
class TestConnectionStringParsing:
    """Test connection string parsing."""

    def test_parse_event_hubs_connection_string(self):
        api = UBAAirDataAPI()
        connection_string = (
            "Endpoint=sb://mynamespace.servicebus.windows.net/;"
            "SharedAccessKeyName=RootManageSharedAccessKey;"
            "SharedAccessKey=abc123==;"
            "EntityPath=uba-airdata"
        )
        result = api.parse_connection_string(connection_string)
        assert result["bootstrap.servers"] == "mynamespace.servicebus.windows.net:9093"
        assert result["kafka_topic"] == "uba-airdata"
        assert result["sasl.username"] == "$ConnectionString"
        assert result["sasl.password"] == connection_string
        assert result["security.protocol"] == "SASL_SSL"
        assert result["sasl.mechanism"] == "PLAIN"

    def test_parse_plain_kafka_connection_string(self):
        api = UBAAirDataAPI()
        result = api.parse_connection_string("BootstrapServer=localhost:9092;EntityPath=uba-airdata")
        assert result["bootstrap.servers"] == "localhost:9092"
        assert result["kafka_topic"] == "uba-airdata"
        assert "sasl.username" not in result

    def test_parse_invalid_connection_string_raises(self):
        api = UBAAirDataAPI()
        with pytest.raises(ValueError, match="Invalid connection string format"):
            api.parse_connection_string("EndpointWithoutEquals;EntityPathAlsoInvalid")


@pytest.mark.unit
class TestPayloadParsing:
    """Test indexed UBA payload parsing."""

    def test_parse_station_data(self):
        stations = UBAAirDataAPI.parse_station_data(STATIONS_PAYLOAD)
        assert len(stations) == 2
        active = next(station for station in stations if station.station_id == 21)
        assert active.station_code == "DEBE021"
        assert active.active_to is None
        assert active.latitude == pytest.approx(52.5491)
        assert active.network_name == "Berlin"
        assert active.type_name == "background"

    def test_parse_component_data(self):
        components = UBAAirDataAPI.parse_component_data(COMPONENTS_PAYLOAD)
        assert len(components) == 2
        no2 = next(component for component in components if component.component_id == 5)
        assert no2.component_code == "NO2"
        assert no2.symbol == "NO₂"
        assert no2.unit == "µg/m³"

    def test_parse_measure_data_filters_inactive_stations_and_handles_nulls(self):
        measures = UBAAirDataAPI.parse_measure_data(MEASURES_PAYLOAD, active_station_ids={21})
        assert len(measures) == 2
        first = measures[0]
        second = measures[1]
        assert first.station_id == 21
        assert first.component_id == 5
        assert first.scope_id == 2
        assert first.value == pytest.approx(4.0)
        assert second.value is None
        assert all(measure.station_id == 21 for measure in measures)


@pytest.mark.unit
class TestHelpers:
    """Test helper functions."""

    def test_measure_feed_url_contains_all_parameters(self):
        url = _measure_feed_url("https://example.test/api", 5, 2, "2026-04-07", "2026-04-08")
        assert url == "https://example.test/api/measures/json?component=5&scope=2&date_from=2026-04-07&date_to=2026-04-08&lang=en"

    def test_measure_date_range_returns_iso_dates(self):
        date_from, date_to = _measure_date_range()
        assert len(date_from) == 10
        assert len(date_to) == 10
        assert date_from <= date_to
