"""
Container integration tests for Hub'Eau Hydrométrie poller.
Tests with a real Kafka container using testcontainers.
"""

import pytest
import json
import time
from unittest.mock import patch, Mock


SAMPLE_STATIONS_RESPONSE = {
    "count": 2,
    "data": [
        {
            "code_station": "A694102004",
            "libelle_station": "La Moselle à Pont-à-Mousson",
            "code_site": "A6941020",
            "longitude_station": 6.179,
            "latitude_station": 48.711,
            "libelle_cours_eau": "La Moselle",
            "libelle_commune": "PONT-A-MOUSSON",
            "code_departement": "54",
            "en_service": True,
            "date_ouverture_station": "2012-11-11T00:00:00Z"
        },
        {
            "code_station": "H320001001",
            "libelle_station": "La Seine à Paris [Austerlitz]",
            "code_site": "H3200010",
            "longitude_station": 2.366,
            "latitude_station": 48.843,
            "libelle_cours_eau": "La Seine",
            "libelle_commune": "PARIS",
            "code_departement": "75",
            "en_service": True,
            "date_ouverture_station": "1985-01-01T00:00:00Z"
        }
    ],
    "next": None
}

SAMPLE_OBSERVATIONS_RESPONSE = {
    "count": 2,
    "data": [
        {
            "code_station": "A694102004",
            "date_obs": "2024-06-15T12:00:00Z",
            "resultat_obs": 1203.0,
            "grandeur_hydro": "H",
            "libelle_methode_obs": "Mesurée",
            "libelle_qualification_obs": "Non qualifiée"
        },
        {
            "code_station": "H320001001",
            "date_obs": "2024-06-15T12:00:00Z",
            "resultat_obs": 28000.0,
            "grandeur_hydro": "Q",
            "libelle_methode_obs": "Calculée",
            "libelle_qualification_obs": "Non qualifiée"
        }
    ],
    "next": None
}


@pytest.mark.integration
class TestHubEauContainerIntegration:
    @pytest.fixture(scope="class")
    def kafka_container(self):
        from testcontainers.kafka import KafkaContainer
        container = KafkaContainer()
        container.start()
        yield container
        container.stop()

    @pytest.fixture
    def kafka_config(self, kafka_container):
        return {
            'bootstrap.servers': kafka_container.get_bootstrap_server(),
            'security.protocol': 'PLAINTEXT',
        }

    def _create_topic(self, kafka_container, topic_name):
        from confluent_kafka.admin import AdminClient, NewTopic
        admin = AdminClient({'bootstrap.servers': kafka_container.get_bootstrap_server()})
        futures = admin.create_topics([NewTopic(topic_name, num_partitions=1, replication_factor=1)])
        for t, f in futures.items():
            try: f.result()
            except: pass

    @patch('hubeau_hydrometrie.hubeau_hydrometrie.HubEauHydrometrieAPI.list_stations')
    @patch('hubeau_hydrometrie.hubeau_hydrometrie.HubEauHydrometrieAPI.get_latest_observations')
    def test_observations_delivered_to_kafka(self, mock_obs, mock_stations,
                                              kafka_container, kafka_config):
        topic = 'test-hubeau-obs'
        self._create_topic(kafka_container, topic)

        mock_stations.return_value = SAMPLE_STATIONS_RESPONSE["data"]
        mock_obs.return_value = SAMPLE_OBSERVATIONS_RESPONSE["data"]

        from hubeau_hydrometrie.hubeau_hydrometrie import HubEauHydrometrieAPI
        from hubeau_hydrometrie.hubeau_hydrometrie_producer.producer_client import FRGovEaufranceHubEauHydrometrieEventProducer
        from hubeau_hydrometrie.hubeau_hydrometrie_producer.fr.gov.eaufrance.hubeau.hydrometrie.station import Station
        from hubeau_hydrometrie.hubeau_hydrometrie_producer.fr.gov.eaufrance.hubeau.hydrometrie.observation import Observation
        from confluent_kafka import Producer

        producer = Producer(kafka_config)
        hubeau_producer = FRGovEaufranceHubEauHydrometrieEventProducer(producer, topic)

        api = HubEauHydrometrieAPI()
        stations = api.list_stations()
        for s in stations:
            station_data = Station(
                code_station=s["code_station"], libelle_station=s["libelle_station"],
                code_site=s["code_site"], longitude_station=s["longitude_station"],
                latitude_station=s["latitude_station"],
                libelle_cours_eau=s.get("libelle_cours_eau", ""),
                libelle_commune=s.get("libelle_commune", ""),
                code_departement=s.get("code_departement", ""),
                en_service=s.get("en_service", False),
                date_ouverture_station=s.get("date_ouverture_station", "")
            )
            hubeau_producer.send_fr_gov_eaufrance_hubeau_hydrometrie_station(
                station_data, flush_producer=False)

        observations = api.get_latest_observations()
        for obs in observations:
            obs_data = Observation(
                code_station=obs["code_station"], date_obs=obs["date_obs"],
                resultat_obs=float(obs["resultat_obs"]),
                grandeur_hydro=obs["grandeur_hydro"],
                libelle_methode_obs=obs.get("libelle_methode_obs", ""),
                libelle_qualification_obs=obs.get("libelle_qualification_obs", "")
            )
            hubeau_producer.send_fr_gov_eaufrance_hubeau_hydrometrie_observation(
                obs_data, flush_producer=False)
        producer.flush()

        from confluent_kafka import Consumer
        consumer = Consumer({
            'bootstrap.servers': kafka_container.get_bootstrap_server(),
            'group.id': 'test-hubeau', 'auto.offset.reset': 'earliest',
            'security.protocol': 'PLAINTEXT',
        })
        consumer.subscribe([topic])

        messages = []
        deadline = time.time() + 30
        while len(messages) < 4 and time.time() < deadline:
            msg = consumer.poll(timeout=1.0)
            if msg is not None and not msg.error():
                messages.append(msg)
        consumer.close()

        assert len(messages) == 4, f"Expected 4 messages, got {len(messages)}"


@pytest.mark.integration
class TestHubEauLiveContainerIntegration:
    @pytest.fixture(scope="class")
    def kafka_container(self):
        from testcontainers.kafka import KafkaContainer
        container = KafkaContainer()
        container.start()
        yield container
        container.stop()

    @pytest.fixture
    def kafka_config(self, kafka_container):
        return {
            'bootstrap.servers': kafka_container.get_bootstrap_server(),
            'security.protocol': 'PLAINTEXT',
        }

    def _create_topic(self, kafka_container, topic_name):
        from confluent_kafka.admin import AdminClient, NewTopic
        admin = AdminClient({'bootstrap.servers': kafka_container.get_bootstrap_server()})
        futures = admin.create_topics([NewTopic(topic_name, num_partitions=1, replication_factor=1)])
        for t, f in futures.items():
            try: f.result()
            except: pass

    def test_live_stations_to_kafka(self, kafka_container, kafka_config):
        topic = 'test-hubeau-live-stations'
        self._create_topic(kafka_container, topic)

        from hubeau_hydrometrie.hubeau_hydrometrie_producer.producer_client import FRGovEaufranceHubEauHydrometrieEventProducer
        from hubeau_hydrometrie.hubeau_hydrometrie_producer.fr.gov.eaufrance.hubeau.hydrometrie.station import Station
        from confluent_kafka import Producer
        import requests

        response = requests.get(
            "https://hubeau.eaufrance.fr/api/v2/hydrometrie/referentiel/stations",
            params={"format": "json", "size": 5, "page": 1},
            timeout=30
        )
        response.raise_for_status()
        stations = response.json().get("data", [])
        assert len(stations) > 0

        producer = Producer(kafka_config)
        hubeau_producer = FRGovEaufranceHubEauHydrometrieEventProducer(producer, topic)

        for s in stations:
            station_data = Station(
                code_station=s.get("code_station", ""),
                libelle_station=s.get("libelle_station", ""),
                code_site=s.get("code_site", ""),
                longitude_station=s.get("longitude_station", 0.0) or 0.0,
                latitude_station=s.get("latitude_station", 0.0) or 0.0,
                libelle_cours_eau=s.get("libelle_cours_eau", "") or "",
                libelle_commune=s.get("libelle_commune", "") or "",
                code_departement=s.get("code_departement", "") or "",
                en_service=s.get("en_service", False) or False,
                date_ouverture_station=s.get("date_ouverture_station", "") or ""
            )
            hubeau_producer.send_fr_gov_eaufrance_hubeau_hydrometrie_station(
                station_data, flush_producer=False)
        producer.flush()

        from confluent_kafka import Consumer
        consumer = Consumer({
            'bootstrap.servers': kafka_container.get_bootstrap_server(),
            'group.id': 'test-hubeau-live', 'auto.offset.reset': 'earliest',
            'security.protocol': 'PLAINTEXT',
        })
        consumer.subscribe([topic])

        messages = []
        deadline = time.time() + 30
        while len(messages) < len(stations) and time.time() < deadline:
            msg = consumer.poll(timeout=1.0)
            if msg is not None and not msg.error():
                messages.append(msg)
        consumer.close()

        assert len(messages) == len(stations)
        for msg in messages:
            value = json.loads(msg.value().decode('utf-8'))
            data = value.get('data', value)
            assert 'code_station' in data

    def test_live_observations_to_kafka(self, kafka_container, kafka_config):
        topic = 'test-hubeau-live-obs'
        self._create_topic(kafka_container, topic)

        from hubeau_hydrometrie.hubeau_hydrometrie_producer.producer_client import FRGovEaufranceHubEauHydrometrieEventProducer
        from hubeau_hydrometrie.hubeau_hydrometrie_producer.fr.gov.eaufrance.hubeau.hydrometrie.observation import Observation
        from confluent_kafka import Producer
        import requests

        response = requests.get(
            "https://hubeau.eaufrance.fr/api/v2/hydrometrie/observations_tr",
            params={"format": "json", "size": 5},
            timeout=30
        )
        response.raise_for_status()
        observations = response.json().get("data", [])
        assert len(observations) > 0

        producer = Producer(kafka_config)
        hubeau_producer = FRGovEaufranceHubEauHydrometrieEventProducer(producer, topic)

        sent = 0
        for obs in observations:
            if obs.get("resultat_obs") is None:
                continue
            obs_data = Observation(
                code_station=obs.get("code_station", ""),
                date_obs=obs.get("date_obs", ""),
                resultat_obs=float(obs["resultat_obs"]),
                grandeur_hydro=obs.get("grandeur_hydro", ""),
                libelle_methode_obs=obs.get("libelle_methode_obs", "") or "",
                libelle_qualification_obs=obs.get("libelle_qualification_obs", "") or ""
            )
            hubeau_producer.send_fr_gov_eaufrance_hubeau_hydrometrie_observation(
                obs_data, flush_producer=False)
            sent += 1
        producer.flush()

        assert sent > 0

        from confluent_kafka import Consumer
        consumer = Consumer({
            'bootstrap.servers': kafka_container.get_bootstrap_server(),
            'group.id': 'test-hubeau-live-obs', 'auto.offset.reset': 'earliest',
            'security.protocol': 'PLAINTEXT',
        })
        consumer.subscribe([topic])

        messages = []
        deadline = time.time() + 30
        while len(messages) < sent and time.time() < deadline:
            msg = consumer.poll(timeout=1.0)
            if msg is not None and not msg.error():
                messages.append(msg)
        consumer.close()

        assert len(messages) == sent
        for msg in messages:
            value = json.loads(msg.value().decode('utf-8'))
            data = value.get('data', value)
            assert 'code_station' in data
            assert 'resultat_obs' in data
