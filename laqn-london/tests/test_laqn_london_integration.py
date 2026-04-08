"""Integration tests for the LAQN London bridge with mocked HTTP responses."""

from datetime import date

import pytest
import requests_mock

from laqn_london.laqn_london import LAQNLondonAPI


class _FakeKafkaProducer:
    def __init__(self):
        self.flush_count = 0

    def flush(self):
        self.flush_count += 1


class _FakeSiteEventProducer:
    def __init__(self):
        self.producer = _FakeKafkaProducer()
        self.sites = []
        self.measurements = []
        self.daily_index = []

    def send_uk_kcl_laqn_site(self, _site_code, data, flush_producer=True):
        self.sites.append((_site_code, data))

    def send_uk_kcl_laqn_measurement(self, _site_code, data, flush_producer=True):
        self.measurements.append((_site_code, data))

    def send_uk_kcl_laqn_daily_index(self, _site_code, data, flush_producer=True):
        self.daily_index.append((_site_code, data))


class _FakeSpeciesEventProducer:
    def __init__(self, shared_producer):
        self.producer = shared_producer
        self.species = []

    def send_uk_kcl_laqn_species(self, _species_code, data, flush_producer=True):
        self.species.append((_species_code, data))


@pytest.mark.integration
class TestLAQNLondonIntegration:
    """Reference and telemetry flows with mocked upstream responses."""

    def test_emit_reference_data_returns_active_sites_and_emits_species(self):
        api = LAQNLondonAPI()
        site_producer = _FakeSiteEventProducer()
        species_producer = _FakeSpeciesEventProducer(site_producer.producer)

        with requests_mock.Mocker() as mocker:
            mocker.get(
                "http://api.erg.ic.ac.uk/AirQuality/Information/MonitoringSites/GroupName=All/Json",
                json={
                    "Sites": {
                        "Site": [
                            {
                                "@LocalAuthorityCode": "3",
                                "@LocalAuthorityName": "Bexley",
                                "@SiteCode": "BX1",
                                "@SiteName": "Bexley - Slade Green",
                                "@SiteType": "Suburban",
                                "@DateOpened": "1994-03-01 00:00:00",
                                "@Latitude": "51.4659832746662",
                                "@Longitude": "0.184877126994369",
                                "@DataOwner": "Bexley",
                                "@DataManager": "King's College London",
                            },
                            {
                                "@LocalAuthorityCode": "27",
                                "@LocalAuthorityName": "Richmond",
                                "@SiteCode": "TD0",
                                "@SiteName": "National Physical Laboratory, Teddington",
                                "@SiteType": "Suburban",
                                "@DateOpened": "1996-08-08 00:00:00",
                                "@DateClosed": "2018-01-01 00:00:00",
                                "@Latitude": "51.4243043441456",
                                "@Longitude": "-0.345714576446947",
                                "@DataOwner": "Richmond",
                                "@DataManager": "King's College London",
                            },
                        ]
                    }
                },
            )
            mocker.get(
                "http://api.erg.ic.ac.uk/AirQuality/Information/Species/Json",
                json={
                    "AirQualitySpecies": {
                        "Species": [
                            {
                                "@SpeciesCode": "NO2",
                                "@SpeciesName": "Nitrogen Dioxide",
                                "@Description": "Description",
                                "@HealthEffect": "Health effect",
                                "@Link": "http://example.com/no2",
                            }
                        ]
                    }
                },
            )

            active_sites = api.emit_reference_data(site_producer, species_producer)

        assert active_sites == ["BX1"]
        assert len(site_producer.sites) == 2
        assert len(species_producer.species) == 1
        assert site_producer.producer.flush_count == 1

    def test_emit_measurements_skips_empty_values_and_dedupes(self):
        api = LAQNLondonAPI()
        site_producer = _FakeSiteEventProducer()
        measurement_state = {}

        with requests_mock.Mocker() as mocker:
            mocker.get(
                "http://api.erg.ic.ac.uk/AirQuality/Data/Site/SiteCode=BX1/StartDate=2026-04-06/EndDate=2026-04-07/Json",
                json={
                    "AirQualityData": {
                        "@SiteCode": "BX1",
                        "Data": [
                            {
                                "@SpeciesCode": "NO2",
                                "@MeasurementDateGMT": "2026-04-07 00:00:00",
                                "@Value": "35.5",
                            },
                            {
                                "@SpeciesCode": "SO2",
                                "@MeasurementDateGMT": "2026-04-07 00:00:00",
                                "@Value": "",
                            },
                        ]
                    }
                },
            )

            first_count = api.emit_measurements(
                ["BX1"], site_producer, measurement_state, date(2026, 4, 6), date(2026, 4, 7)
            )
            second_count = api.emit_measurements(
                ["BX1"], site_producer, measurement_state, date(2026, 4, 6), date(2026, 4, 7)
            )

        assert first_count == 1
        assert second_count == 0
        assert len(site_producer.measurements) == 1
        assert site_producer.measurements[0][1].value == 35.5

    def test_emit_daily_index_flattens_nested_response_and_dedupes(self):
        api = LAQNLondonAPI()
        site_producer = _FakeSiteEventProducer()
        daily_index_state = {}

        with requests_mock.Mocker() as mocker:
            mocker.get(
                "http://api.erg.ic.ac.uk/AirQuality/Daily/MonitoringIndex/Latest/GroupName=London/Json",
                json={
                    "DailyAirQualityIndex": {
                        "@MonitoringIndexDate": "2026-04-07 00:00:00",
                        "@GroupName": "London",
                        "LocalAuthority": [
                            {
                                "@LocalAuthorityCode": "3",
                                "@LocalAuthorityName": "Bexley",
                                "Site": [
                                    {
                                        "@BulletinDate": "2026-04-07 00:00:00",
                                        "@SiteCode": "BX1",
                                        "@SiteName": "Bexley - Slade Green",
                                        "Species": [
                                            {
                                                "@SpeciesCode": "NO2",
                                                "@AirQualityIndex": "2",
                                                "@AirQualityBand": "Low",
                                                "@IndexSource": "Measurement",
                                            }
                                        ],
                                    }
                                ],
                            },
                            {
                                "@LocalAuthorityCode": "4",
                                "@LocalAuthorityName": "Brent",
                                "Site": [
                                    {
                                        "@BulletinDate": "2026-04-07 00:00:00",
                                        "@SiteCode": "BR1",
                                        "Species": " ",
                                    }
                                ],
                            },
                        ],
                    }
                },
            )

            first_count = api.emit_daily_index(site_producer, daily_index_state)
            second_count = api.emit_daily_index(site_producer, daily_index_state)

        assert first_count == 1
        assert second_count == 0
        assert len(site_producer.daily_index) == 1
        assert site_producer.daily_index[0][1].site_code == "BX1"
        assert site_producer.daily_index[0][1].species_code == "NO2"
