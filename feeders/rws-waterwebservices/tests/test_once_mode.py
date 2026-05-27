"""Test that --once flag causes feed_stations() to exit after one polling cycle."""

from unittest.mock import MagicMock, patch

from rws_waterwebservices.rws_waterwebservices import RWSWaterwebservicesAPI


def test_once_mode_exits_after_one_cycle():
    """feed_stations(..., once=True) must return after exactly one cycle."""
    api = RWSWaterwebservicesAPI()

    api.get_water_level_stations = MagicMock(return_value=[
        {"Code": "HOlv", "Naam": "Test", "Lat": 52.0, "Lon": 4.0, "Coordinatenstelsel": "25831"},
    ])
    api.get_latest_observations = MagicMock(return_value=[
        {
            "Locatie": {"Code": "HOlv", "Naam": "Test"},
            "AquoMetadata": {"Eenheid": {"Code": "cm"}},
            "MetingenLijst": [
                {
                    "Tijdstip": "2025-01-01T00:00:00.000+00:00",
                    "Meetwaarde": {"Waarde_Numeriek": 12.3},
                    "WaarnemingMetadata": {"Kwaliteitswaardecode": "00", "Statuswaarde": "Gecontroleerd"},
                }
            ],
        }
    ])

    with patch("rws_waterwebservices.rws_waterwebservices.time.sleep") as mock_sleep, \
         patch("confluent_kafka.Producer") as mock_producer_cls, \
         patch("rws_waterwebservices.rws_waterwebservices.NLRWSWaterwebservicesEventProducer") as mock_rws_producer_cls:
        mock_producer_cls.return_value = MagicMock()
        mock_rws_producer_cls.return_value = MagicMock()

        api.feed_stations(
            kafka_config={"bootstrap.servers": "localhost:9092"},
            kafka_topic="test-topic",
            polling_interval=1,
            state_file="",
            once=True,
        )

        # Latest observations fetched exactly once
        assert api.get_latest_observations.call_count == 1
        # No sleep call after the cycle (once-mode breaks before sleep)
        mock_sleep.assert_not_called()
