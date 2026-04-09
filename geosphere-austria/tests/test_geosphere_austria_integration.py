"""Integration tests for GeoSphere Austria TAWES bridge with mocked HTTP."""

import json

import pytest
import requests_mock as rm

from geosphere_austria.geosphere_austria import (
    METADATA_URL,
    OBSERVATIONS_URL,
    run_feed_cycle,
)
from geosphere_austria_producer_kafka_producer.producer import AtGeosphereTawesEventProducer

pytestmark = pytest.mark.integration


MOCK_METADATA = {
    "title": "TAWES",
    "parameters": [],
    "stations": [
        {
            "type": "INDIVIDUAL",
            "id": "11035",
            "name": "WIEN HOHE WARTE",
            "state": "Wien",
            "lat": 48.2486,
            "lon": 16.3564,
            "altitude": 198.0,
            "is_active": True,
        },
    ],
}

MOCK_GEOJSON = {
    "media_type": "application/json",
    "type": "FeatureCollection",
    "version": "v1",
    "timestamps": ["2024-01-15T13:00+00:00"],
    "features": [
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [16.3564, 48.2486]},
            "properties": {
                "parameters": {
                    "TL": {"name": "Lufttemperatur", "unit": "°C", "data": [3.9]},
                    "RF": {"name": "Relative Feuchte", "unit": "%", "data": [64.0]},
                    "RR": {"name": "Niederschlag", "unit": "mm", "data": [0.0]},
                    "DD": {"name": "Windrichtung", "unit": "°", "data": [296.0]},
                    "FF": {"name": "Windgeschwindigkeit", "unit": "m/s", "data": [3.2]},
                    "P": {"name": "Luftdruck", "unit": "hPa", "data": [999.7]},
                    "SO": {"name": "Sonnenscheindauer", "unit": "sec", "data": [0.0]},
                    "GLOW": {"name": "Globalstrahlung", "unit": "W/m²", "data": [0.0]},
                },
                "station": "11035",
            },
        },
    ],
}


class FakeProducer:
    def __init__(self):
        self.messages = []

    def produce(self, topic, key=None, value=None, headers=None):
        self.messages.append({"topic": topic, "key": key, "value": value, "headers": headers})

    def flush(self):
        pass


class TestRunFeedCycle:
    """Integration test for a full feed cycle with mocked HTTP."""

    def test_first_cycle_emits_stations_and_observations(self):
        with rm.Mocker() as m:
            m.get(METADATA_URL, json=MOCK_METADATA)
            m.get(OBSERVATIONS_URL, json=MOCK_GEOJSON)

            fake = FakeProducer()
            producer = AtGeosphereTawesEventProducer(fake, "test-topic")
            import requests
            session = requests.Session()
            state = {}

            stations_emitted, obs_emitted, stations = run_feed_cycle(
                producer, session, state, station_refresh_due=True
            )

            assert stations_emitted == 1
            assert obs_emitted == 1
            assert len(stations) == 1
            assert stations[0].station_id == "11035"

            # Verify station event
            station_msgs = [m for m in fake.messages if "WeatherStation" in json.loads(m["value"]).get("type", "")]
            assert len(station_msgs) == 1
            station_ce = json.loads(station_msgs[0]["value"])
            assert station_ce["data"]["station_id"] == "11035"
            assert station_ce["data"]["state"] == "Wien"

            # Verify observation event
            obs_msgs = [m for m in fake.messages if "WeatherObservation" in json.loads(m["value"]).get("type", "")]
            assert len(obs_msgs) == 1
            obs_ce = json.loads(obs_msgs[0]["value"])
            assert obs_ce["data"]["temperature"] == 3.9

    def test_second_cycle_dedup(self):
        with rm.Mocker() as m:
            m.get(METADATA_URL, json=MOCK_METADATA)
            m.get(OBSERVATIONS_URL, json=MOCK_GEOJSON)

            fake = FakeProducer()
            producer = AtGeosphereTawesEventProducer(fake, "test-topic")
            import requests
            session = requests.Session()
            state = {}

            run_feed_cycle(producer, session, state, station_refresh_due=True)
            fake.messages.clear()

            # Second cycle with same data should dedup observations
            stations_emitted, obs_emitted, _ = run_feed_cycle(
                producer, session, state, station_refresh_due=False
            )

            assert stations_emitted == 0
            assert obs_emitted == 0

    def test_no_station_refresh(self):
        with rm.Mocker() as m:
            m.get(METADATA_URL, json=MOCK_METADATA)
            m.get(OBSERVATIONS_URL, json=MOCK_GEOJSON)

            fake = FakeProducer()
            producer = AtGeosphereTawesEventProducer(fake, "test-topic")
            import requests
            session = requests.Session()
            state = {}

            stations_emitted, obs_emitted, _ = run_feed_cycle(
                producer, session, state, station_refresh_due=False
            )

            assert stations_emitted == 0
            assert obs_emitted == 1
            # Only observation events, no station events
            types = {json.loads(m["value"])["type"] for m in fake.messages}
            assert "at.geosphere.tawes.WeatherObservation" in types
            assert "at.geosphere.tawes.WeatherStation" not in types
