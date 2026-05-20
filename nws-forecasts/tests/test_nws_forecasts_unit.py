"""Unit tests for the NWS forecasts bridge."""

from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest
import requests

from nws_forecasts.nws_forecasts import NWSForecastPoller, parse_connection_string, parse_zone_list
from nws_forecasts_producer_data import ForecastZone, LandForecastPeriod, LandZoneForecast, MarineForecastPeriod, MarineZoneForecast, ZoneTypeenum


SAMPLE_MARINE_TEXT = """Expires:202604141045;;317911
FZUS56 KSEW 132142
CWFSEW

Coastal Waters Forecast for Washington
National Weather Service Seattle WA
242 PM PDT Mon Apr 13 2026

Inland waters of western Washington and the northern and central
Washington coastal waters including the Olympic Coast National
Marine Sanctuary


PZZ135-141045-
Puget Sound and Hood Canal-
242 PM PDT Mon Apr 13 2026

.TONIGHT...S wind 10 to 15 kt. Waves around 2 ft or less. A chance of rain.
.TUE...S wind 15 to 20 kt. Waves around 2 ft or less. Rain.
.TUE NIGHT...SW wind 10 to 15 kt. Waves around 2 ft or less. Rain in the evening.

$$
"""


@pytest.fixture
def mock_kafka_config():
    return {"bootstrap.servers": "localhost:9092", "security.protocol": "PLAINTEXT"}


@pytest.fixture
def temp_state_file():
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.unlink(path)


def _zone(zone_id: str, zone_type: ZoneTypeenum) -> ForecastZone:
    return ForecastZone(
        zone_id=zone_id,
        zone_type=zone_type,
        name=zone_id,
        state=zone_id[:2],
        forecast_office_url="https://api.weather.gov/offices/SEW",
        grid_identifier="SEW" if zone_type == ZoneTypeenum.public else None,
        awips_location_identifier="SEW" if zone_type == ZoneTypeenum.public else None,
        cwa_ids=["SEW"],
        forecast_office_urls=["https://api.weather.gov/offices/SEW"],
        time_zones=["America/Los_Angeles"],
        observation_station_ids=["KSEA"],
        radar_station="ATX",
        effective_date=datetime.now(timezone.utc),
        expiration_date=datetime.now(timezone.utc),
    )


def _land_forecast(zone_id: str) -> LandZoneForecast:
    return LandZoneForecast(
        zone_id=zone_id,
        updated=datetime(2026, 4, 14, 1, 0, tzinfo=timezone.utc),
        periods=[
            LandForecastPeriod(period_number=1, period_name="Tonight", detailed_forecast="Cloudy."),
            LandForecastPeriod(period_number=2, period_name="Tuesday", detailed_forecast="Rain."),
        ],
    )


def _marine_forecast(zone_id: str) -> MarineZoneForecast:
    return MarineZoneForecast(
        zone_id=zone_id,
        zone_name="Puget Sound and Hood Canal",
        product_title="Coastal Waters Forecast for Washington",
        office_name="National Weather Service Seattle WA",
        issued_at_text="242 PM PDT Mon Apr 13 2026",
        expires_text="202604141045;;317911",
        wmo_header="FZUS56 KSEW 132142",
        bulletin_awips_id="CWFSEW",
        synopsis="Inland waters of western Washington.",
        periods=[
            MarineForecastPeriod(period_name="TONIGHT", forecast_text="S wind 10 to 15 kt."),
            MarineForecastPeriod(period_name="TUE", forecast_text="S wind 15 to 20 kt."),
        ],
        bulletin_text="Marine bulletin body",
    )


def _build_poller(mock_kafka_config, temp_state_file):
    with patch("nws_forecasts.nws_forecasts.Producer") as producer_class, patch(
        "nws_forecasts.nws_forecasts.MicrosoftOpenDataUSNOAANWSForecastsEventProducer"
    ) as event_producer_class:
        producer_instance = MagicMock()
        producer_instance.flush.return_value = 0
        producer_class.return_value = producer_instance
        event_producer = MagicMock()
        event_producer_class.return_value = event_producer
        poller = NWSForecastPoller(
            kafka_config=mock_kafka_config,
            kafka_topic="test-topic",
            zones=["WAZ315", "PZZ135"],
            state_file=temp_state_file,
        )
        poller.kafka_client = producer_instance
        poller.producer = event_producer
        return poller


@pytest.mark.unit
class TestHelpers:
    def test_parse_connection_string_event_hubs(self):
        result = parse_connection_string(
            "Endpoint=sb://demo.servicebus.windows.net/;SharedAccessKeyName=name;SharedAccessKey=key;EntityPath=topic"
        )
        assert result["bootstrap.servers"] == "demo.servicebus.windows.net:9093"
        assert result["kafka_topic"] == "topic"
        assert result["sasl.username"] == "$ConnectionString"

    def test_parse_connection_string_bootstrap(self):
        result = parse_connection_string("BootstrapServer=localhost:9092;EntityPath=test", enable_tls=False)
        assert result["bootstrap.servers"] == "localhost:9092"
        assert result["security.protocol"] == "PLAINTEXT"
        assert result["kafka_topic"] == "test"

    def test_parse_zone_list(self):
        assert parse_zone_list(" WAZ315, pzz135 ") == ["WAZ315", "PZZ135"]


@pytest.mark.unit
class TestMarineParsing:
    def test_parse_marine_forecast(self, mock_kafka_config, temp_state_file):
        poller = _build_poller(mock_kafka_config, temp_state_file)
        forecast = poller.parse_marine_forecast("PZZ135", SAMPLE_MARINE_TEXT)
        assert forecast.zone_id == "PZZ135"
        assert forecast.zone_name == "Puget Sound and Hood Canal"
        assert forecast.wmo_header == "FZUS56 KSEW 132142"
        assert [period.period_name for period in forecast.periods] == ["TONIGHT", "TUE", "TUE NIGHT"]
        assert "Waves around 2 ft or less." in forecast.periods[0].forecast_text


@pytest.mark.unit
class TestPollerResilience:
    def test_reference_refresh_keeps_cached_zone_on_failure(self, mock_kafka_config, temp_state_file):
        poller = _build_poller(mock_kafka_config, temp_state_file)
        poller.zones = ["WAZ315"]
        poller.zone_cache = {"WAZ315": _zone("WAZ315", ZoneTypeenum.public)}
        with patch.object(poller, "fetch_zone", side_effect=requests.Timeout("boom")):
            poller.refresh_zone_cache()
        assert "WAZ315" in poller.zone_cache
        assert poller.zone_cache["WAZ315"].zone_id == "WAZ315"

    def test_poll_once_flush_failure_does_not_advance_state(self, mock_kafka_config, temp_state_file):
        with open(temp_state_file, "w", encoding="utf-8") as handle:
            json.dump({"land_updates": {}, "marine_hashes": {}}, handle)

        poller = _build_poller(mock_kafka_config, temp_state_file)
        poller.zones = ["WAZ315"]
        poller.zone_cache = {"WAZ315": _zone("WAZ315", ZoneTypeenum.public)}
        poller.kafka_client.flush.return_value = 1
        with patch.object(poller, "fetch_land_forecast", return_value=_land_forecast("WAZ315")):
            with pytest.raises(RuntimeError):
                poller.poll_once()

        with open(temp_state_file, "r", encoding="utf-8") as handle:
            state = json.load(handle)
        assert state == {"land_updates": {}, "marine_hashes": {}}

    def test_poll_once_skips_failed_slice_and_emits_other_slice(self, mock_kafka_config, temp_state_file):
        poller = _build_poller(mock_kafka_config, temp_state_file)
        poller.zone_cache = {
            "WAZ315": _zone("WAZ315", ZoneTypeenum.public),
            "PZZ135": _zone("PZZ135", ZoneTypeenum.marine),
        }

        with patch.object(poller, "fetch_land_forecast", side_effect=requests.Timeout("land failed")), patch.object(
            poller, "fetch_marine_forecast", return_value=_marine_forecast("PZZ135")
        ):
            emitted = poller.poll_once()

        assert emitted == 1
        poller.producer.send_microsoft_open_data_us_noaa_nws_land_zone_forecast.assert_not_called()
        poller.producer.send_microsoft_open_data_us_noaa_nws_marine_zone_forecast.assert_called_once()
        with open(temp_state_file, "r", encoding="utf-8") as handle:
            state = json.load(handle)
        assert state["land_updates"] == {}
        assert state["marine_hashes"]["PZZ135"]
