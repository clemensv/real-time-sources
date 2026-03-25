"""Container integration tests for Waterinfo VMM bridge with KafkaContainer."""

import json
import time
import pytest
import requests
from unittest.mock import patch, MagicMock
from testcontainers.kafka import KafkaContainer
from confluent_kafka import Producer, Consumer, KafkaError

from waterinfo_vmm.waterinfo_vmm import WaterinfoVMMAPI
from waterinfo_vmm.waterinfo_vmm_producer.producer_client import BEVlaanderenWaterinfoVMMEventProducer
from waterinfo_vmm.waterinfo_vmm_producer.be.vlaanderen.waterinfo.vmm.station import Station
from waterinfo_vmm.waterinfo_vmm_producer.be.vlaanderen.waterinfo.vmm.water_level_reading import WaterLevelReading


KAFKA_TOPIC = "test-waterinfo-vmm"


def _create_consumer(bootstrap_servers: str) -> Consumer:
    """Create a Kafka consumer for testing."""
    return Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test-waterinfo-vmm-group',
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


class TestWaterinfoContainerIntegration:
    """Tests with KafkaContainer using mocked HTTP data."""

    def test_readings_delivered_to_kafka(self):
        """Test that water level readings are delivered to Kafka."""
        with KafkaContainer() as kafka:
            bootstrap_servers = kafka.get_bootstrap_server()
            producer = Producer({'bootstrap.servers': bootstrap_servers})
            waterinfo_producer = BEVlaanderenWaterinfoVMMEventProducer(producer, KAFKA_TOPIC)

            # Send a mock water level reading
            reading = WaterLevelReading(
                ts_id="306367042",
                station_no="S02_44H",
                station_name="Kleit/Ede",
                timestamp="2026-03-25T10:15:00.000Z",
                value=6.118,
                unit_name="meter",
                parameter_name="H",
            )
            waterinfo_producer.send_be_vlaanderen_waterinfo_vmm_water_level_reading(reading)

            # Send a mock station
            station = Station(
                station_no="S02_44H",
                station_name="Kleit/Ede",
                station_id="441678",
                station_latitude=51.179,
                station_longitude=3.463,
                river_name="Ede",
                stationparameter_name="H",
                ts_id="306367042",
                ts_unitname="meter",
            )
            waterinfo_producer.send_be_vlaanderen_waterinfo_vmm_station(station)

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

                if ce_type == "BE.Vlaanderen.Waterinfo.VMM.WaterLevelReading":
                    data = payload["data"]
                    assert data["ts_id"] == "306367042"
                    assert data["value"] == 6.118
                elif ce_type == "BE.Vlaanderen.Waterinfo.VMM.Station":
                    data = payload["data"]
                    assert data["station_no"] == "S02_44H"

            assert "BE.Vlaanderen.Waterinfo.VMM.WaterLevelReading" in types_found
            assert "BE.Vlaanderen.Waterinfo.VMM.Station" in types_found


class TestWaterinfoLiveContainerIntegration:
    """Tests with KafkaContainer using the real Waterinfo API."""

    def test_live_stations_to_kafka(self):
        """Test real station data flows through to Kafka."""
        with KafkaContainer() as kafka:
            bootstrap_servers = kafka.get_bootstrap_server()
            producer = Producer({'bootstrap.servers': bootstrap_servers})
            waterinfo_producer = BEVlaanderenWaterinfoVMMEventProducer(producer, KAFKA_TOPIC)

            # Fetch real station data (just first page)
            api = WaterinfoVMMAPI()
            station_data = api.list_stations()
            headers = station_data[0] if station_data else []
            rows = station_data[1:6]  # Just 5 stations

            for row in rows:
                d = dict(zip(headers, row))
                station = Station(
                    station_no=d.get("station_no", ""),
                    station_name=d.get("station_name", ""),
                    station_id=str(d.get("station_id", "")),
                    station_latitude=float(d.get("station_latitude", 0) or 0),
                    station_longitude=float(d.get("station_longitude", 0) or 0),
                    river_name=d.get("river_name", "") or "",
                    stationparameter_name="",
                    ts_id="",
                    ts_unitname="",
                )
                waterinfo_producer.send_be_vlaanderen_waterinfo_vmm_station(station, flush_producer=False)
            producer.flush()

            consumer = _create_consumer(bootstrap_servers)
            messages = _consume_messages(consumer, KAFKA_TOPIC, 5)
            assert len(messages) == 5

            for msg in messages:
                payload = json.loads(msg.value())
                assert payload["type"] == "BE.Vlaanderen.Waterinfo.VMM.Station"
                data = payload["data"]
                assert data["station_no"] != ""
                assert data["station_name"] != ""

    def test_live_readings_to_kafka(self):
        """Test real water level readings flow through to Kafka."""
        with KafkaContainer() as kafka:
            bootstrap_servers = kafka.get_bootstrap_server()
            producer = Producer({'bootstrap.servers': bootstrap_servers})
            waterinfo_producer = BEVlaanderenWaterinfoVMMEventProducer(producer, KAFKA_TOPIC)

            # Fetch real water level data
            api = WaterinfoVMMAPI()
            entries = api.get_latest_water_levels()

            sent_count = 0
            for entry in entries[:5]:  # Just 5 readings
                ts_value = entry.get("ts_value")
                ts_timestamp = entry.get("timestamp")
                if ts_value is None or ts_timestamp is None:
                    continue

                reading = WaterLevelReading(
                    ts_id=str(entry.get("ts_id", "")),
                    station_no=entry.get("station_no", ""),
                    station_name=entry.get("station_name", ""),
                    timestamp=ts_timestamp,
                    value=float(ts_value),
                    unit_name=entry.get("ts_unitname", "meter"),
                    parameter_name=entry.get("stationparameter_name", "H"),
                )
                waterinfo_producer.send_be_vlaanderen_waterinfo_vmm_water_level_reading(reading, flush_producer=False)
                sent_count += 1
            producer.flush()

            assert sent_count > 0
            consumer = _create_consumer(bootstrap_servers)
            messages = _consume_messages(consumer, KAFKA_TOPIC, sent_count)
            assert len(messages) == sent_count

            for msg in messages:
                payload = json.loads(msg.value())
                assert payload["type"] == "BE.Vlaanderen.Waterinfo.VMM.WaterLevelReading"
                data = payload["data"]
                assert data["ts_id"] != ""
                assert isinstance(data["value"], (int, float))
