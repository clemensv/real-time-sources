"""Unit tests for the german-waters bridge."""

import pytest
from unittest.mock import MagicMock, call, patch

from german_waters.german_waters import (
    parse_connection_string,
    _resolve_providers,
    _station_to_event,
    _obs_to_event,
    send_stations,
    feed_observations,
    PROVIDER_CLASSES,
    ALL_PROVIDERS,
)
from german_waters.providers import BaseProvider, StationData, ObservationData
from german_waters_producer_data.de.waters.hydrology.station import Station
from german_waters_producer_data.de.waters.hydrology.waterlevelobservation import WaterLevelObservation


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

def _make_station(station_id: str = "by_12345", provider: str = "bayern_gkd") -> StationData:
    return StationData(
        station_id=station_id,
        station_name="Regensburg",
        water_body="Donau",
        provider=provider,
        state="Bayern",
        region="Oberpfalz",
        latitude=49.01,
        longitude=12.10,
        river_km=1347.5,
        altitude=335.0,
        station_type="Pegel",
        warn_level_cm=400.0,
        alarm_level_cm=550.0,
        warn_level_m3s=800.0,
        alarm_level_m3s=1500.0,
    )


def _make_obs(station_id: str = "by_12345", ts: str = "2026-04-01T12:00:00+01:00") -> ObservationData:
    return ObservationData(
        station_id=station_id,
        provider="bayern_gkd",
        water_level=325.0,
        water_level_unit="cm",
        water_level_timestamp=ts,
        discharge=620.0,
        discharge_unit="m3/s",
        discharge_timestamp=ts,
        trend=1,
        situation=2,
    )


class _StubProvider(BaseProvider):
    """Minimal provider stub used by several tests."""

    def __init__(self, name_: str, stations=None, observations=None, raises=False):
        self._name = name_
        self._stations = stations or []
        self._observations = observations or []
        self._raises = raises

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return "stub"

    def get_stations(self):
        if self._raises:
            raise RuntimeError("simulated station fetch error")
        return self._stations

    def get_observations(self):
        if self._raises:
            raise RuntimeError("simulated observation fetch error")
        return self._observations


# ---------------------------------------------------------------------------
# parse_connection_string
# ---------------------------------------------------------------------------

class TestParseConnectionString:
    """Parsing of Event Hubs and plain Kafka connection strings."""

    def test_event_hubs_full_string(self):
        conn = (
            "Endpoint=sb://mynamespace.servicebus.windows.net/;"
            "SharedAccessKeyName=RootManageSharedAccessKey;"
            "SharedAccessKey=supersecret;"
            "EntityPath=german-waters"
        )
        cfg = parse_connection_string(conn)
        assert cfg["bootstrap.servers"] == "mynamespace.servicebus.windows.net:9093"
        assert cfg["kafka_topic"] == "german-waters"
        assert cfg["sasl.username"] == "$ConnectionString"
        assert cfg["sasl.password"] == conn.strip()
        assert cfg["security.protocol"] == "SASL_SSL"
        assert cfg["sasl.mechanism"] == "PLAIN"

    def test_bootstrap_server_plain(self):
        conn = "BootstrapServer=localhost:9092;EntityPath=waters"
        cfg = parse_connection_string(conn)
        assert cfg["bootstrap.servers"] == "localhost:9092"
        assert cfg["kafka_topic"] == "waters"
        assert "sasl.username" not in cfg
        assert "security.protocol" not in cfg

    def test_entity_path_only(self):
        conn = "EntityPath=my-topic"
        cfg = parse_connection_string(conn)
        assert cfg["kafka_topic"] == "my-topic"
        assert "bootstrap.servers" not in cfg

    def test_empty_string_returns_empty_dict(self):
        assert parse_connection_string("") == {}

    def test_sb_url_stripped_correctly(self):
        conn = "Endpoint=sb://hub.servicebus.windows.net/"
        cfg = parse_connection_string(conn)
        # trailing slash and sb:// prefix must both be removed
        assert not cfg["bootstrap.servers"].startswith("sb://")
        assert not cfg["bootstrap.servers"].endswith("/")
        assert cfg["bootstrap.servers"].endswith(":9093")

    def test_sasl_triggers_protocol_fields(self):
        conn = (
            "Endpoint=sb://ns.servicebus.windows.net/;"
            "SharedAccessKeyName=key;"
            "SharedAccessKey=secret"
        )
        cfg = parse_connection_string(conn)
        assert cfg["security.protocol"] == "SASL_SSL"
        assert cfg["sasl.mechanism"] == "PLAIN"


# ---------------------------------------------------------------------------
# _resolve_providers
# ---------------------------------------------------------------------------

class TestResolveProviders:
    """Provider include/exclude filtering."""

    def test_no_filter_returns_all(self):
        providers = _resolve_providers(None, None)
        names = {p.name for p in providers}
        assert names == set(PROVIDER_CLASSES.keys())

    def test_include_single(self):
        providers = _resolve_providers("bayern_gkd", None)
        assert len(providers) == 1
        assert providers[0].name == "bayern_gkd"

    def test_include_multiple(self):
        providers = _resolve_providers("bayern_gkd,nrw_hygon", None)
        names = {p.name for p in providers}
        assert names == {"bayern_gkd", "nrw_hygon"}

    def test_exclude_single(self):
        providers = _resolve_providers(None, "bayern_gkd")
        names = {p.name for p in providers}
        assert "bayern_gkd" not in names
        assert len(names) == len(PROVIDER_CLASSES) - 1

    def test_exclude_multiple(self):
        providers = _resolve_providers(None, "bayern_gkd,nrw_hygon")
        names = {p.name for p in providers}
        assert "bayern_gkd" not in names
        assert "nrw_hygon" not in names

    def test_include_and_exclude_disjoint(self):
        # include overrides; exclude is applied after include filter
        providers = _resolve_providers("bayern_gkd,nrw_hygon", "nrw_hygon")
        names = {p.name for p in providers}
        assert names == {"bayern_gkd"}

    def test_include_unknown_key_returns_empty(self):
        providers = _resolve_providers("nonexistent_provider", None)
        assert providers == []

    def test_whitespace_in_csv_is_stripped(self):
        providers = _resolve_providers(" bayern_gkd , nrw_hygon ", None)
        names = {p.name for p in providers}
        assert names == {"bayern_gkd", "nrw_hygon"}

    def test_all_providers_constant_matches_registry(self):
        assert set(ALL_PROVIDERS) == set(PROVIDER_CLASSES.keys())


# ---------------------------------------------------------------------------
# _station_to_event
# ---------------------------------------------------------------------------

class TestStationToEvent:
    """StationData → Station (generated data class) field mapping."""

    def test_all_fields_mapped(self):
        src = _make_station()
        evt = _station_to_event(src)
        assert isinstance(evt, Station)
        assert evt.station_id == src.station_id
        assert evt.station_name == src.station_name
        assert evt.water_body == src.water_body
        assert evt.state == src.state
        assert evt.region == src.region
        assert evt.provider == src.provider
        assert evt.latitude == src.latitude
        assert evt.longitude == src.longitude
        assert evt.river_km == src.river_km
        assert evt.altitude == src.altitude
        assert evt.station_type == src.station_type
        assert evt.warn_level_cm == src.warn_level_cm
        assert evt.alarm_level_cm == src.alarm_level_cm
        assert evt.warn_level_m3s == src.warn_level_m3s
        assert evt.alarm_level_m3s == src.alarm_level_m3s

    def test_optional_fields_default_zero(self):
        src = StationData(
            station_id="nrw_99",
            station_name="Köln",
            water_body="Rhein",
            provider="nrw_hygon",
        )
        evt = _station_to_event(src)
        assert evt.latitude == 0.0
        assert evt.longitude == 0.0
        assert evt.river_km == 0.0
        assert evt.altitude == 0.0
        assert evt.warn_level_cm == 0.0
        assert evt.alarm_level_cm == 0.0


# ---------------------------------------------------------------------------
# _obs_to_event
# ---------------------------------------------------------------------------

class TestObsToEvent:
    """ObservationData → WaterLevelObservation (generated data class) field mapping."""

    def test_all_fields_mapped(self):
        src = _make_obs()
        evt = _obs_to_event(src)
        assert isinstance(evt, WaterLevelObservation)
        assert evt.station_id == src.station_id
        assert evt.provider == src.provider
        assert evt.water_level == src.water_level
        assert evt.water_level_unit == src.water_level_unit
        assert evt.water_level_timestamp == src.water_level_timestamp
        assert evt.discharge == src.discharge
        assert evt.discharge_unit == src.discharge_unit
        assert evt.discharge_timestamp == src.discharge_timestamp
        assert evt.trend == src.trend
        assert evt.situation == src.situation

    def test_defaults_survive_mapping(self):
        src = ObservationData(station_id="sh_001", provider="sh_lkn")
        evt = _obs_to_event(src)
        assert evt.water_level == 0.0
        assert evt.discharge == 0.0
        assert evt.trend == 0
        assert evt.situation == 0
        assert evt.water_level_unit == "cm"
        assert evt.discharge_unit == "m3/s"


# ---------------------------------------------------------------------------
# send_stations (startup station emission)
# ---------------------------------------------------------------------------

class TestSendStations:
    """Station events are emitted once per station at startup."""

    def test_emits_one_event_per_station(self):
        mock_producer = MagicMock()
        stations = [_make_station("by_1"), _make_station("by_2"), _make_station("by_3")]
        count = send_stations(mock_producer, stations)
        assert count == 3
        assert mock_producer.send_de_waters_hydrology_station.call_count == 3

    def test_flush_producer_false(self):
        mock_producer = MagicMock()
        send_stations(mock_producer, [_make_station()])
        _, kwargs = mock_producer.send_de_waters_hydrology_station.call_args
        assert kwargs.get("flush_producer") is False

    def test_empty_list_returns_zero(self):
        mock_producer = MagicMock()
        count = send_stations(mock_producer, [])
        assert count == 0
        mock_producer.send_de_waters_hydrology_station.assert_not_called()

    def test_station_data_passed_through(self):
        mock_producer = MagicMock()
        s = _make_station("by_42")
        send_stations(mock_producer, [s])
        args, kwargs = mock_producer.send_de_waters_hydrology_station.call_args
        sent: Station = kwargs["data"]
        assert sent.station_id == "by_42"


# ---------------------------------------------------------------------------
# feed_observations (observation feed with mocked provider and producer)
# ---------------------------------------------------------------------------

class TestFeedObservations:
    """Observation events are deduplicated and forwarded to the producer."""

    def _run(self, providers, previous=None):
        mock_producer = MagicMock()
        mock_kafka = MagicMock()
        prev = previous if previous is not None else {}
        count = feed_observations(mock_producer, providers, prev, mock_kafka)
        return count, mock_producer, mock_kafka, prev

    def test_single_observation_emitted(self):
        obs = _make_obs("by_1", "2026-04-01T10:00:00+01:00")
        provider = _StubProvider("p1", observations=[obs])
        count, mock_producer, mock_kafka, prev = self._run([provider])
        assert count == 1
        mock_producer.send_de_waters_hydrology_water_level_observation.assert_called_once()
        mock_kafka.flush.assert_called_once()

    def test_dedup_skips_same_timestamp(self):
        ts = "2026-04-01T10:00:00+01:00"
        obs = _make_obs("by_1", ts)
        provider = _StubProvider("p1", observations=[obs])
        previous = {"by_1": ts}
        count, mock_producer, _, _ = self._run([provider], previous)
        assert count == 0
        mock_producer.send_de_waters_hydrology_water_level_observation.assert_not_called()

    def test_new_timestamp_replaces_old(self):
        old_ts = "2026-04-01T09:00:00+01:00"
        new_ts = "2026-04-01T10:00:00+01:00"
        obs = _make_obs("by_1", new_ts)
        provider = _StubProvider("p1", observations=[obs])
        previous = {"by_1": old_ts}
        count, mock_producer, _, prev = self._run([provider], previous)
        assert count == 1
        assert prev["by_1"] == new_ts

    def test_obs_without_timestamp_skipped(self):
        obs = ObservationData(
            station_id="by_99",
            provider="bayern_gkd",
            water_level=100.0,
            water_level_timestamp="",
            discharge_timestamp="",
        )
        provider = _StubProvider("p1", observations=[obs])
        count, mock_producer, _, _ = self._run([provider])
        assert count == 0
        mock_producer.send_de_waters_hydrology_water_level_observation.assert_not_called()

    def test_multiple_stations_all_emitted(self):
        obs_list = [
            _make_obs("by_1", "2026-04-01T10:00:00+01:00"),
            _make_obs("by_2", "2026-04-01T10:05:00+01:00"),
            _make_obs("by_3", "2026-04-01T10:10:00+01:00"),
        ]
        provider = _StubProvider("p1", observations=obs_list)
        count, mock_producer, _, _ = self._run([provider])
        assert count == 3
        assert mock_producer.send_de_waters_hydrology_water_level_observation.call_count == 3

    def test_flush_called_once_per_run(self):
        obs_list = [
            _make_obs("by_1", "2026-04-01T10:00:00+01:00"),
            _make_obs("by_2", "2026-04-01T10:05:00+01:00"),
        ]
        provider = _StubProvider("p1", observations=obs_list)
        _, _, mock_kafka, _ = self._run([provider])
        mock_kafka.flush.assert_called_once()

    def test_flush_producer_false_for_each_event(self):
        obs = _make_obs("by_1", "2026-04-01T10:00:00+01:00")
        provider = _StubProvider("p1", observations=[obs])
        _, mock_producer, _, _ = self._run([provider])
        _, kwargs = mock_producer.send_de_waters_hydrology_water_level_observation.call_args
        assert kwargs.get("flush_producer") is False


# ---------------------------------------------------------------------------
# Partial-failure: one provider error must not abort the others
# ---------------------------------------------------------------------------

class TestPartialFailure:
    """A provider that raises during get_observations must not stop remaining providers."""

    def test_failing_provider_does_not_abort_others(self):
        good_obs = _make_obs("by_10", "2026-04-01T12:00:00+01:00")
        good_provider = _StubProvider("good", observations=[good_obs])
        bad_provider = _StubProvider("bad", raises=True)

        mock_producer = MagicMock()
        mock_kafka = MagicMock()
        previous = {}
        count = feed_observations(mock_producer, [bad_provider, good_provider], previous, mock_kafka)

        assert count == 1
        mock_producer.send_de_waters_hydrology_water_level_observation.assert_called_once()
        mock_kafka.flush.assert_called_once()

    def test_all_failing_returns_zero(self):
        bad1 = _StubProvider("bad1", raises=True)
        bad2 = _StubProvider("bad2", raises=True)
        mock_producer = MagicMock()
        mock_kafka = MagicMock()
        count = feed_observations(mock_producer, [bad1, bad2], {}, mock_kafka)
        assert count == 0
        mock_producer.send_de_waters_hydrology_water_level_observation.assert_not_called()

    def test_failure_logged(self, caplog):
        import logging
        bad_provider = _StubProvider("bad", raises=True)
        mock_producer = MagicMock()
        mock_kafka = MagicMock()
        with caplog.at_level(logging.ERROR, logger="german_waters.german_waters"):
            feed_observations(mock_producer, [bad_provider], {}, mock_kafka)
        assert any("bad" in r.message for r in caplog.records)
