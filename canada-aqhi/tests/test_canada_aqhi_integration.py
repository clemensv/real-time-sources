"""Integration tests for the Canada AQHI bridge with mocked upstream responses."""

from unittest.mock import MagicMock

import pytest

from canada_aqhi.canada_aqhi import CanadaAQHIBridge


COMMUNITY_GEOJSON = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "Latitude": "47.082841",
                "Longitude": "-55.175272",
                "cgndb_key": "AADCE",
                "region_name_en": "Burin",
                "region_name_fr": "Burin",
            },
            "geometry": {"type": "Point", "coordinates": [-55.175272, 47.082841]},
        }
    ],
}

STATION_GEOJSON = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "name": {"en": "Burin", "fr": "Burin"},
                "cgndb": "AADCE",
                "path_to_current_observation": "https://dd.weather.gc.ca/today/air_quality/aqhi/atl/observation/realtime/xml/AQ_OBS_AADCE_CURRENT.xml",
                "path_to_current_forecast": "https://dd.weather.gc.ca/today/air_quality/aqhi/atl/forecast/realtime/xml/AQ_FCST_AADCE_CURRENT.xml",
            },
        }
    ],
}

OBSERVATION_XML = """<?xml version='1.0' encoding='utf-8'?>
<conditionAirQuality productHeader="AQ_OBS">
  <region nameEn="Burin" nameFr="Burin">AADCE</region>
  <dateStamp name="aqObserved" zoneEn="NDT" zoneFr="HAT">
    <year>2026</year><month nameEn="April" nameFr="avril">4</month><day nameEn="Wednesday" nameFr="mercredi">8</day>
    <hour clock="12h" ampm="AM">8</hour><minute>30</minute><second/><UTCStamp>20260408110000</UTCStamp>
  </dateStamp>
  <airQualityHealthIndex>1.9</airQualityHealthIndex>
</conditionAirQuality>
"""

FORECAST_XML = """<?xml version="1.0" encoding="ISO-8859-1"?>
<forecastAirQuality productHeader="AQ_FCST" status="issued">
  <region nameEn="Burin" nameFr="Burin">AADCE</region>
  <dateStamp name="aqForecastIssued" zoneEn="NDT" zoneFr="HAT">
    <year>2026</year><month nameEn="April" nameFr="avril">4</month><day nameEn="Wednesday" nameFr="mercredi">8</day>
    <hour clock="12h" ampm="AM">6</hour><minute>0</minute><second/><UTCStamp>20260408083000</UTCStamp>
  </dateStamp>
  <forecastGroup>
    <forecast periodID="1"><period forecastName="Today" lang="EN">Wednesday</period><airQualityHealthIndex>2</airQualityHealthIndex></forecast>
    <forecast periodID="2"><period forecastName="Tonight" lang="EN">Wednesday night</period><airQualityHealthIndex>2</airQualityHealthIndex></forecast>
    <forecast periodID="3"><period forecastName="Tomorrow" lang="EN">Thursday</period><airQualityHealthIndex>3</airQualityHealthIndex></forecast>
    <forecast periodID="4"><period forecastName="Tomorrow Night" lang="EN">Thursday night</period><airQualityHealthIndex>4</airQualityHealthIndex></forecast>
  </forecastGroup>
</forecastAirQuality>
"""


class FakeEventProducer:
    def __init__(self):
        self.producer = MagicMock()
        self.community_events = []
        self.observation_events = []
        self.forecast_events = []

    def send_ca_gc_weather_aqhi_community(self, _province, _community_name, data, flush_producer=False):
        self.community_events.append((_province, _community_name, data, flush_producer))

    def send_ca_gc_weather_aqhi_observation(self, _province, _community_name, data, flush_producer=False):
        self.observation_events.append((_province, _community_name, data, flush_producer))

    def send_ca_gc_weather_aqhi_forecast(self, _province, _community_name, data, flush_producer=False):
        self.forecast_events.append((_province, _community_name, data, flush_producer))


@pytest.mark.integration
class TestBridgePolling:
    def test_poll_once_emits_reference_observation_and_forecasts(self, requests_mock, tmp_path):
        state_file = tmp_path / "aqhi-state.json"
        bridge = CanadaAQHIBridge(state_file=str(state_file))
        producer = FakeEventProducer()

        requests_mock.get(
            "https://collaboration.cmc.ec.gc.ca/cmc/cmos/public_doc/msc-data/aqhi/aqhi_community.geojson",
            json=COMMUNITY_GEOJSON,
        )
        requests_mock.get(
            "https://collaboration.cmc.ec.gc.ca/cmc/cmos/public_doc/msc-data/aqhi/aqhi_station.geojson",
            json=STATION_GEOJSON,
        )
        requests_mock.get(
            "https://geolocator.api.geo.ca/",
            json=[{"province": "Newfoundland and Labrador", "lat": 47.082841, "lng": -55.175272}],
        )
        requests_mock.get(
            "https://dd.weather.gc.ca/today/air_quality/aqhi/atl/observation/realtime/xml/AQ_OBS_AADCE_CURRENT.xml",
            text=OBSERVATION_XML,
        )
        requests_mock.get(
            "https://dd.weather.gc.ca/today/air_quality/aqhi/atl/forecast/realtime/xml/AQ_FCST_AADCE_CURRENT.xml",
            text=FORECAST_XML,
        )

        counts = bridge.poll_once(producer, {"NL"}, reference_refresh_interval=86400)

        assert counts == {"communities": 1, "observations": 1, "forecasts": 4}
        assert len(producer.community_events) == 1
        assert len(producer.observation_events) == 1
        assert len(producer.forecast_events) == 4
        assert producer.community_events[0][2].province == "NL"
        assert producer.observation_events[0][2].aqhi == pytest.approx(1.9)
        assert producer.forecast_events[0][2].forecast_period_label == "Today"

    def test_second_poll_deduplicates_existing_events(self, requests_mock, tmp_path):
        state_file = tmp_path / "aqhi-state.json"
        bridge = CanadaAQHIBridge(state_file=str(state_file))
        producer = FakeEventProducer()

        requests_mock.get(
            "https://collaboration.cmc.ec.gc.ca/cmc/cmos/public_doc/msc-data/aqhi/aqhi_community.geojson",
            json=COMMUNITY_GEOJSON,
        )
        requests_mock.get(
            "https://collaboration.cmc.ec.gc.ca/cmc/cmos/public_doc/msc-data/aqhi/aqhi_station.geojson",
            json=STATION_GEOJSON,
        )
        requests_mock.get(
            "https://geolocator.api.geo.ca/",
            json=[{"province": "Newfoundland and Labrador", "lat": 47.082841, "lng": -55.175272}],
        )
        requests_mock.get(
            "https://dd.weather.gc.ca/today/air_quality/aqhi/atl/observation/realtime/xml/AQ_OBS_AADCE_CURRENT.xml",
            text=OBSERVATION_XML,
        )
        requests_mock.get(
            "https://dd.weather.gc.ca/today/air_quality/aqhi/atl/forecast/realtime/xml/AQ_FCST_AADCE_CURRENT.xml",
            text=FORECAST_XML,
        )

        first_counts = bridge.poll_once(producer, {"NL"}, reference_refresh_interval=86400)
        second_counts = bridge.poll_once(producer, {"NL"}, reference_refresh_interval=86400)

        assert first_counts == {"communities": 1, "observations": 1, "forecasts": 4}
        assert second_counts == {"communities": 0, "observations": 0, "forecasts": 0}
