"""Container integration tests for RWS Waterwebservices bridge with KafkaContainer."""

import json
import time
import pytest
import requests
from unittest.mock import patch, MagicMock
from testcontainers.kafka import KafkaContainer
from confluent_kafka import Producer, Consumer, KafkaError

from rws_waterwebservices.rws_waterwebservices import RWSWaterwebservicesAPI
from rws_waterwebservices_producer_kafka_producer.producer import NLRWSWaterwebservicesEventProducer
from rws_waterwebservices_producer_data import Station
from rws_waterwebservices_producer_data import WaterLevelObservation

KAFKA_TOPIC = "test-rws-waterwebservices"


def _create_consumer(bootstrap_servers: str) -> Consumer:
    """Create a Kafka consumer for testing."""
    return Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test-rws-waterwebservices-group',
        'auto.offset.reset': 'earliest',
        'session.timeout.ms': 10000,
    })


def _consume_messages(consumer: Consumer, topic: str, expected_count: int, timeout_seconds: int = 30) -> list:
    """Consume messages from a Kafka topic."""
    consumer.subscribe([topic])
    messages = []
    start = time.time()
    while len(messages) < expected_count and (time.time() - start) < timeout_seconds:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            raise Exception(f"Kafka error: {msg.error()}")
        messages.append(msg)
    consumer.close()
    return messages


class TestRWSContainerIntegration:
    """Tests with KafkaContainer using mocked HTTP data."""

    def test_observations_delivered_to_kafka(self):
        """Test that water level observations are delivered to Kafka."""
        with KafkaContainer() as kafka:
            bootstrap_servers = kafka.get_bootstrap_server()
            producer = Producer({'bootstrap.servers': bootstrap_servers})
            rws_producer = NLRWSWaterwebservicesEventProducer(producer, KAFKA_TOPIC)

            # Send a mock water level observation
            observation = WaterLevelObservation(
                location_code="HOlv",
                location_name="Hoek van Holland",
                timestamp="2026-03-25T10:00:00.000+01:00",
                value=123.0,
                unit="cm",
                quality_code="25",
                status="Ongecontroleerd",
                compartment="OW",
                parameter="WATHTE",
            )
            rws_producer.send_nl_rws_waterwebservices_water_level_observation(observation)

            # Send a mock station
            station = Station(
                code="HOlv",
                name="Hoek van Holland",
                latitude=51.979,
                longitude=4.120,
                coordinate_system="25831",
            )
            rws_producer.send_nl_rws_waterwebservices_station(station)

            # Consume and verify
            consumer = _create_consumer(bootstrap_servers)
            messages = _consume_messages(consumer, KAFKA_TOPIC, 2)

            assert len(messages) == 2

            # Parse CloudEvents
            types_found = set()
            for msg in messages:
                payload = json.loads(msg.value())
                ce_type = payload.get("type")
                types_found.add(ce_type)
                assert "data" in payload

                if ce_type == "NL.RWS.Waterwebservices.WaterLevelObservation":
                    data = payload["data"]
                    assert data["location_code"] == "HOlv"
                    assert data["value"] == 123.0
                elif ce_type == "NL.RWS.Waterwebservices.Station":
                    data = payload["data"]
                    assert data["code"] == "HOlv"

            assert "NL.RWS.Waterwebservices.WaterLevelObservation" in types_found
            assert "NL.RWS.Waterwebservices.Station" in types_found


class TestRWSLiveContainerIntegration:
    """Tests with KafkaContainer using the real RWS API."""

    def test_live_stations_to_kafka(self):
        """Test real station data flows through to Kafka."""
        with KafkaContainer() as kafka:
            bootstrap_servers = kafka.get_bootstrap_server()
            producer = Producer({'bootstrap.servers': bootstrap_servers})
            rws_producer = NLRWSWaterwebservicesEventProducer(producer, KAFKA_TOPIC)

            # Fetch real station data (just first 5 stations)
            api = RWSWaterwebservicesAPI()
            stations = api.get_water_level_stations()
            assert len(stations) > 0

            sent = 0
            for loc in stations[:5]:
                station = Station(
                    code=loc.get("Code", ""),
                    name=loc.get("Naam", ""),
                    latitude=float(loc.get("Lat", 0) or 0),
                    longitude=float(loc.get("Lon", 0) or 0),
                    coordinate_system=loc.get("Coordinatenstelsel", ""),
                )
                rws_producer.send_nl_rws_waterwebservices_station(station, flush_producer=False)
                sent += 1
            producer.flush()

            consumer = _create_consumer(bootstrap_servers)
            messages = _consume_messages(consumer, KAFKA_TOPIC, sent)
            assert len(messages) == sent

            for msg in messages:
                payload = json.loads(msg.value())
                assert payload["type"] == "NL.RWS.Waterwebservices.Station"
                data = payload["data"]
                assert data["code"] != ""
                assert data["name"] != ""

    def test_live_observations_to_kafka(self):
        """Test real water level observations flow through to Kafka."""
        with KafkaContainer() as kafka:
            bootstrap_servers = kafka.get_bootstrap_server()
            producer = Producer({'bootstrap.servers': bootstrap_servers})
            rws_producer = NLRWSWaterwebservicesEventProducer(producer, KAFKA_TOPIC)

            # Fetch real water level data for a known station
            api = RWSWaterwebservicesAPI()
            observations = api.get_latest_observations(["hoekvanholland", "delfzijl", "ijmuiden"])

            sent_count = 0
            for entry in observations:
                loc = entry.get("Locatie", {})
                aquo = entry.get("AquoMetadata", {})
                unit = aquo.get("Eenheid", {}).get("Code", "cm")
                for meting in entry.get("MetingenLijst", []):
                    waarde = meting.get("Meetwaarde", {}).get("Waarde_Numeriek")
                    tijdstip = meting.get("Tijdstip")
                    if waarde is None or tijdstip is None:
                        continue

                    obs = WaterLevelObservation(
                        location_code=loc.get("Code", ""),
                        location_name=loc.get("Naam", ""),
                        timestamp=tijdstip,
                        value=float(waarde),
                        unit=unit,
                        quality_code=meting.get("WaarnemingMetadata", {}).get("Kwaliteitswaardecode", ""),
                        status=meting.get("WaarnemingMetadata", {}).get("Statuswaarde", ""),
                        compartment="OW",
                        parameter="WATHTE",
                    )
                    rws_producer.send_nl_rws_waterwebservices_water_level_observation(obs, flush_producer=False)
                    sent_count += 1
                    if sent_count >= 5:
                        break
                if sent_count >= 5:
                    break
            producer.flush()

            assert sent_count > 0
            consumer = _create_consumer(bootstrap_servers)
            messages = _consume_messages(consumer, KAFKA_TOPIC, sent_count)
            assert len(messages) == sent_count

            for msg in messages:
                payload = json.loads(msg.value())
                assert payload["type"] == "NL.RWS.Waterwebservices.WaterLevelObservation"
                data = payload["data"]
                assert data["location_code"] != ""
                assert isinstance(data["value"], (int, float))
