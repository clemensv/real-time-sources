import json
import os
import sys
from pathlib import Path

import pytest

THIS_DIR = Path(__file__).resolve().parent
SOURCE_DIR = THIS_DIR.parent
CORE_DIR = SOURCE_DIR / "gbfs_bikeshare_core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from gbfs_bikeshare_core.acquisition import (  # noqa: E402
    GbfsSourceClient,
    GbfsSource,
    StationInformationRecord,
    discover_sources,
    should_publish_free_bike_status,
    should_publish_station_status,
)
from gbfs_bikeshare_core.config import ConfiguredFeed, parse_feed_configuration  # noqa: E402


class FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


class FakeSession:
    def __init__(self, mapping):
        self.mapping = mapping
        self.headers = {}

    def get(self, url, timeout=30):
        if url not in self.mapping:
            raise AssertionError(f"Unexpected URL {url}")
        payload = self.mapping[url]
        if isinstance(payload, Exception):
            raise payload
        return FakeResponse(payload)


SAMPLE_DISCOVERY_URL = "https://example.test/gbfs/gbfs.json"
SAMPLE_SYSTEM_URL = "https://example.test/gbfs/system_information.json"
SAMPLE_STATION_INFO_URL = "https://example.test/gbfs/station_information.json"
SAMPLE_STATION_STATUS_URL = "https://example.test/gbfs/station_status.json"
SAMPLE_FREE_BIKE_URL = "https://example.test/gbfs/free_bike_status.json"

SAMPLE_MANIFEST = {
    "data": {
        "en": {
            "feeds": [
                {"name": "system_information", "url": SAMPLE_SYSTEM_URL},
                {"name": "station_information", "url": SAMPLE_STATION_INFO_URL},
                {"name": "station_status", "url": SAMPLE_STATION_STATUS_URL},
                {"name": "free_bike_status", "url": SAMPLE_FREE_BIKE_URL},
            ]
        }
    },
    "ttl": 60,
    "version": "2.3",
}

SAMPLE_SYSTEM = {
    "data": {
        "system_id": "sample-system",
        "name": "Sample Bikes",
        "operator": "Sample Operator",
        "url": "https://example.test",
        "timezone": "Europe/London",
        "language": "en",
        "phone_number": "+44-0000-000000",
    }
}

SAMPLE_STATION_INFO = {
    "data": {
        "stations": [
            {
                "station_id": "station-1",
                "name": "Main Square",
                "short_name": "001",
                "lat": 51.5,
                "lon": -0.12,
                "capacity": 20,
                "region_id": "central",
                "address": "1 Main Square",
                "post_code": "AB1 2CD",
            },
            {
                "station_id": "station-2",
                "name": "No Capacity",
                "lat": 51.51,
                "lon": -0.13,
            },
        ]
    }
}

SAMPLE_STATION_STATUS = {
    "ttl": 30,
    "data": {
        "stations": [
            {
                "station_id": "station-1",
                "num_bikes_available": 5,
                "num_docks_available": 15,
                "num_ebikes_available": 2,
                "is_installed": 1,
                "is_renting": 0,
                "is_returning": True,
                "last_reported": 1717488123,
            }
        ]
    }
}

SAMPLE_FREE_BIKES = {
    "ttl": 15,
    "data": {
        "bikes": [
            {
                "bike_id": "bike-1",
                "lat": 51.49,
                "lon": -0.11,
                "is_reserved": False,
                "is_disabled": 0,
                "vehicle_type_id": "ebike",
                "current_range_meters": 15000,
                "last_reported": 1717488100,
            },
            {
                "bike_id": "bike-2",
                "is_reserved": True,
                "is_disabled": False,
            },
        ]
    }
}


def _client(mapping=None):
    mapping = mapping or {
        SAMPLE_DISCOVERY_URL: SAMPLE_MANIFEST,
        SAMPLE_SYSTEM_URL: SAMPLE_SYSTEM,
        SAMPLE_STATION_INFO_URL: SAMPLE_STATION_INFO,
        SAMPLE_STATION_STATUS_URL: SAMPLE_STATION_STATUS,
        SAMPLE_FREE_BIKE_URL: SAMPLE_FREE_BIKES,
    }
    return GbfsSourceClient(session=FakeSession(mapping))


@pytest.mark.unit
def test_parse_feed_configuration_with_overrides():
    configured = parse_feed_configuration("https://a.example/gbfs.json,https://b.example/gbfs.json", "alpha,beta")
    assert [item.autodiscovery_url for item in configured] == ["https://a.example/gbfs.json", "https://b.example/gbfs.json"]
    assert [item.system_id_override for item in configured] == ["alpha", "beta"]


@pytest.mark.unit
def test_discover_sources_uses_system_information_system_id():
    sources = discover_sources(_client(), [ConfiguredFeed(SAMPLE_DISCOVERY_URL)])
    assert len(sources) == 1
    assert sources[0].system_id == "sample-system"
    assert sources[0].feeds["station_status"] == SAMPLE_STATION_STATUS_URL


@pytest.mark.unit
def test_discover_sources_respects_override():
    sources = discover_sources(_client(), [ConfiguredFeed(SAMPLE_DISCOVERY_URL, "custom-system")])
    assert sources[0].system_id == "custom-system"


@pytest.mark.unit
def test_fetch_station_information_normalizes_nullable_fields():
    source = GbfsSource(SAMPLE_DISCOVERY_URL, "sample-system", {"station_information": SAMPLE_STATION_INFO_URL}, "en")
    records, feed_url = _client().fetch_station_information(source)
    assert feed_url == SAMPLE_STATION_INFO_URL
    assert isinstance(records[0], StationInformationRecord)
    assert records[0].capacity == 20
    assert records[1].capacity is None
    assert records[1].short_name is None


@pytest.mark.unit
def test_fetch_station_status_normalizes_boolean_and_int_fields():
    source = GbfsSource(SAMPLE_DISCOVERY_URL, "sample-system", {"station_status": SAMPLE_STATION_STATUS_URL}, "en")
    records, _, ttl = _client().fetch_station_status(source)
    assert ttl == 30
    assert records[0].is_installed is True
    assert records[0].is_renting is False
    assert records[0].num_ebikes_available == 2


@pytest.mark.unit
def test_fetch_free_bike_status_allows_null_location():
    source = GbfsSource(SAMPLE_DISCOVERY_URL, "sample-system", {"free_bike_status": SAMPLE_FREE_BIKE_URL}, "en")
    records, _, ttl = _client().fetch_free_bike_status(source)
    assert ttl == 15
    assert records[0].current_range_meters == 15000.0
    assert records[1].lat is None
    assert records[1].lon is None
    assert records[1].last_reported is None


@pytest.mark.unit
def test_offline_mock_corpus_round_trips_reference_and_telemetry():
    from gbfs_bikeshare_core.acquisition import discover_sources as _discover
    from gbfs_bikeshare_core.samples import MOCK_SYSTEM_ID, build_offline_client_and_feeds

    client, feeds = build_offline_client_and_feeds()
    sources = _discover(client, feeds)
    assert len(sources) == 1
    source = sources[0]
    assert source.system_id == MOCK_SYSTEM_ID

    system = client.fetch_system_information(source)
    assert system is not None
    system_record, _ = system
    assert system_record.system_id == MOCK_SYSTEM_ID

    stations, station_feed_url = client.fetch_station_information(source)
    assert station_feed_url is not None
    assert len(stations) == 3

    statuses, _, _ = client.fetch_station_status(source)
    assert len(statuses) == 3
    assert statuses[0].is_renting is True

    bikes, _, _ = client.fetch_free_bike_status(source)
    assert len(bikes) == 2
    assert bikes[1].current_range_meters is None


@pytest.mark.unit
def test_dedupe_helpers_only_publish_on_change():
    source = GbfsSource(SAMPLE_DISCOVERY_URL, "sample-system", {"station_status": SAMPLE_STATION_STATUS_URL, "free_bike_status": SAMPLE_FREE_BIKE_URL}, "en")
    client = _client()
    statuses, _, _ = client.fetch_station_status(source)
    bikes, _, _ = client.fetch_free_bike_status(source)
    state = {"station_status": {}, "free_bike_status": {}}
    assert should_publish_station_status(statuses[0], state) is True
    assert should_publish_station_status(statuses[0], state) is False
    assert should_publish_free_bike_status(bikes[0], state) is True
    assert should_publish_free_bike_status(bikes[0], state) is False
