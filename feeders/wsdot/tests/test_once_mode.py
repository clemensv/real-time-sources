"""Verify that the --once flag causes wsdot.feed() to exit after one cycle."""
from argparse import Namespace
from unittest.mock import MagicMock, patch

from wsdot import wsdot


def _make_args(**overrides):
    base = dict(
        connection_string="BootstrapServer=localhost:9092;EntityPath=test",
        access_code="dummy",
        polling_interval=1,
        region_filter=None,
        once=True,
    )
    base.update(overrides)
    return Namespace(**base)


def test_feed_once_exits_after_first_cycle():
    """With --once, feed() must return after the initial reference + telemetry
    batch without entering the polling loop or calling time.sleep."""
    with patch.object(wsdot, "Producer") as mock_producer_cls, \
         patch.object(wsdot, "WSDOTApi") as mock_api_cls, \
         patch.object(wsdot, "UsWaWsdotTrafficEventProducer"), \
         patch.object(wsdot, "UsWaWsdotTraveltimesEventProducer"), \
         patch.object(wsdot, "UsWaWsdotMountainpassEventProducer"), \
         patch.object(wsdot, "UsWaWsdotWeatherEventProducer"), \
         patch.object(wsdot, "UsWaWsdotTollsEventProducer"), \
         patch.object(wsdot, "UsWaWsdotCvrestrictionsEventProducer"), \
         patch.object(wsdot, "UsWaWsdotBorderEventProducer"), \
         patch.object(wsdot, "UsWaWsdotFerriesEventProducer"), \
         patch.object(wsdot.time, "sleep") as mock_sleep:
        api = mock_api_cls.return_value
        for fetch in (
            "fetch_traffic_flows",
            "fetch_travel_times",
            "fetch_mountain_pass_conditions",
            "fetch_weather_stations",
            "fetch_weather_information",
            "fetch_toll_rates",
            "fetch_cv_restrictions",
            "fetch_border_crossings",
            "fetch_vessel_locations",
        ):
            getattr(api, fetch).return_value = []

        mock_producer_cls.return_value = MagicMock()

        wsdot.feed(_make_args())

        mock_sleep.assert_not_called()


def test_feed_once_env_var_triggers_single_cycle(monkeypatch):
    """ONCE_MODE env var should also trigger single-cycle exit even when the
    CLI flag is absent."""
    monkeypatch.setenv("ONCE_MODE", "true")
    args = _make_args(once=False)

    with patch.object(wsdot, "Producer") as mock_producer_cls, \
         patch.object(wsdot, "WSDOTApi") as mock_api_cls, \
         patch.object(wsdot, "UsWaWsdotTrafficEventProducer"), \
         patch.object(wsdot, "UsWaWsdotTraveltimesEventProducer"), \
         patch.object(wsdot, "UsWaWsdotMountainpassEventProducer"), \
         patch.object(wsdot, "UsWaWsdotWeatherEventProducer"), \
         patch.object(wsdot, "UsWaWsdotTollsEventProducer"), \
         patch.object(wsdot, "UsWaWsdotCvrestrictionsEventProducer"), \
         patch.object(wsdot, "UsWaWsdotBorderEventProducer"), \
         patch.object(wsdot, "UsWaWsdotFerriesEventProducer"), \
         patch.object(wsdot.time, "sleep") as mock_sleep:
        api = mock_api_cls.return_value
        for fetch in (
            "fetch_traffic_flows",
            "fetch_travel_times",
            "fetch_mountain_pass_conditions",
            "fetch_weather_stations",
            "fetch_weather_information",
            "fetch_toll_rates",
            "fetch_cv_restrictions",
            "fetch_border_crossings",
            "fetch_vessel_locations",
        ):
            getattr(api, fetch).return_value = []
        mock_producer_cls.return_value = MagicMock()

        wsdot.feed(args)
        mock_sleep.assert_not_called()
