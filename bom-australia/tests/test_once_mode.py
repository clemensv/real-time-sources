"""Unit test for the ``--once`` single-cycle execution mode added to support
Fabric notebook hosting (see notebook-feeder-retrofit skill)."""

import sys
import types
from unittest.mock import MagicMock, patch


def _stub_producer_modules():
    """Insert lightweight stubs for the generated producer packages.

    This keeps the test runnable in environments where the path-installed
    ``bom_australia_producer_*`` sub-packages are not yet pip-installed.
    """
    for mod in (
        "bom_australia_producer_kafka_producer",
        "bom_australia_producer_kafka_producer.producer",
        "bom_australia_producer_data",
    ):
        sys.modules.setdefault(mod, types.ModuleType(mod))
    sys.modules["bom_australia_producer_kafka_producer.producer"].AUGovBOMWarningEventProducer = MagicMock()
    sys.modules["bom_australia_producer_kafka_producer.producer"].AUGovBOMWeatherEventProducer = MagicMock()
    sys.modules["bom_australia_producer_data"].Station = MagicMock()
    sys.modules["bom_australia_producer_data"].WarningBulletin = MagicMock()
    sys.modules["bom_australia_producer_data"].WeatherObservation = MagicMock()


def test_once_mode_exits_after_single_cycle():
    """``--once`` must cause main() to return after exactly one cycle without sleeping."""
    _stub_producer_modules()
    from bom_australia import bom_australia as bridge

    with patch.object(bridge, "time") as mock_time, \
         patch.object(bridge, "feed_warnings", return_value=0) as mock_feed_warnings, \
         patch.object(bridge, "feed_observations", return_value=0) as mock_feed_observations, \
         patch.object(bridge, "send_stations"), \
         patch.object(bridge, "_save_state"), \
         patch.object(bridge, "_load_state", return_value={"observations": {}, "warnings": {}}), \
         patch.object(bridge, "AUGovBOMWarningEventProducer"), \
         patch.object(bridge, "AUGovBOMWeatherEventProducer"), \
         patch.object(bridge, "Producer"), \
         patch.object(bridge, "BOMAustraliaAPI") as mock_api_cls:
        mock_api_cls.return_value.discover_stations.return_value = [("IDN60901", 94767)]

        argv = [
            "bom-australia",
            "--connection-string", "PLAINTEXT://localhost:9092",
            "--topic", "bom-australia",
            "--stations", "IDN60901:94767",
            "--once",
            "feed",
        ]
        with patch.object(sys, "argv", argv):
            bridge.main()

        assert mock_feed_observations.call_count == 1, "feed_observations should run exactly once"
        assert mock_feed_warnings.call_count == 1, "feed_warnings should run exactly once"
        mock_time.sleep.assert_not_called()
