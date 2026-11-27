"""Unit tests for the KMI Belgium weather bridge."""

import json
import socket
import sys
import threading
import types
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest
import requests
from urllib3.util import connection as urllib3_connection
from urllib3.util import retry as urllib3_retry


confluent_kafka = types.ModuleType("confluent_kafka")


class Producer:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


confluent_kafka.Producer = Producer
sys.modules.setdefault("confluent_kafka", confluent_kafka)

producer_data = types.ModuleType("kmi_belgium_producer_data")


@dataclass
class Station:
    station_code: str
    latitude: float
    longitude: float
    region: str | None = None


@dataclass
class WeatherObservation:
    station_code: str
    observation_time: datetime
    precip_quantity: float | None = None
    temp_dry_shelter_avg: float | None = None
    temp_grass_pt100_avg: float | None = None
    temp_soil_avg: float | None = None
    temp_soil_avg_5cm: float | None = None
    temp_soil_avg_10cm: float | None = None
    temp_soil_avg_20cm: float | None = None
    temp_soil_avg_50cm: float | None = None
    wind_speed_10m: float | None = None
    wind_speed_avg_30m: float | None = None
    wind_direction: float | None = None
    wind_gusts_speed: float | None = None
    humidity_rel_shelter_avg: float | None = None
    pressure: float | None = None
    sun_duration: float | None = None
    short_wave_from_sky_avg: float | None = None
    sun_int_avg: float | None = None
    region: str | None = None


producer_data.Station = Station
producer_data.WeatherObservation = WeatherObservation
sys.modules.setdefault("kmi_belgium_producer_data", producer_data)

producer_pkg = types.ModuleType("kmi_belgium_producer_kafka_producer")
producer_mod = types.ModuleType("kmi_belgium_producer_kafka_producer.producer")


class BEGovKMIWeatherEventProducer:
    pass


producer_mod.BEGovKMIWeatherEventProducer = BEGovKMIWeatherEventProducer
producer_pkg.producer = producer_mod
sys.modules.setdefault("kmi_belgium_producer_kafka_producer", producer_pkg)
sys.modules.setdefault("kmi_belgium_producer_kafka_producer.producer", producer_mod)

from kmi_belgium.kmi_belgium import KMIBelgiumAPI, extract_stations, parse_connection_string


SAMPLE_FEATURE = {
    "type": "Feature",
    "id": "aws_10min.example-1",
    "geometry": {"type": "Point", "coordinates": [4.357, 50.797]},
    "properties": {
        "code": 6418,
        "timestamp": "2024-05-01T10:20:00Z",
        "precip_quantity": 0.4,
        "temp_dry_shelter_avg": 7.5,
        "temp_grass_pt100_avg": 5.1,
        "temp_soil_avg": 8.0,
        "temp_soil_avg_5cm": 8.3,
        "temp_soil_avg_10cm": 8.9,
        "temp_soil_avg_20cm": 9.4,
        "temp_soil_avg_50cm": 10.2,
        "wind_speed_10m": 4.5,
        "wind_speed_avg_30m": None,
        "wind_direction": 210.0,
        "wind_gusts_speed": 6.8,
        "humidity_rel_shelter_avg": 82.0,
        "pressure": 1008.5,
        "sun_duration": 2.0,
        "short_wave_from_sky_avg": 112.4,
        "sun_int_avg": 75.1,
    },
}


class TestConnectionString:
    def test_parse_plain_bootstrap(self):
        config = parse_connection_string("BootstrapServer=localhost:9092;EntityPath=kmi-belgium")
        assert config["bootstrap.servers"] == "localhost:9092"
        assert config["_entity_path"] == "kmi-belgium"

    def test_parse_event_hubs(self):
        cs = "Endpoint=sb://namespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=abc123;EntityPath=kmi-belgium"
        config = parse_connection_string(cs)
        assert config["bootstrap.servers"] == "namespace.servicebus.windows.net:9093"
        assert config["sasl.username"] == "$ConnectionString"
        assert config["sasl.password"] == cs
        assert config["sasl.mechanism"] == "PLAIN"
        assert config["security.protocol"] == "SASL_SSL"


class TestGeoJsonParsing:
    def test_parse_weather_observation_feature(self):
        observation = KMIBelgiumAPI.parse_observation(SAMPLE_FEATURE)
        assert observation.station_code == "6418"
        assert observation.observation_time == datetime(2024, 5, 1, 10, 20, tzinfo=timezone.utc)
        assert observation.temp_dry_shelter_avg == 7.5
        assert observation.wind_speed_avg_30m is None
        assert observation.sun_int_avg == 75.1

    def test_extract_stations_from_features(self):
        duplicate = deepcopy(SAMPLE_FEATURE)
        duplicate["properties"]["timestamp"] = "2024-05-01T10:30:00Z"
        second_station = deepcopy(SAMPLE_FEATURE)
        second_station["geometry"]["coordinates"] = [5.587, 49.62]
        second_station["properties"]["code"] = 6484
        stations = extract_stations([SAMPLE_FEATURE, duplicate, second_station])
        assert len(stations) == 2
        by_code = {station.station_code: station for station in stations}
        assert by_code["6418"].latitude == 50.797
        assert by_code["6418"].longitude == 4.357
        assert by_code["6484"].latitude == 49.62
        assert by_code["6484"].longitude == 5.587


@pytest.fixture
def local_wfs(monkeypatch):
    outcomes = []
    paths = []
    sleeps = []
    release_timeouts = threading.Event()
    monkeypatch.setattr(urllib3_retry.time, "sleep", sleeps.append)

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            paths.append(self.path)
            outcome = outcomes.pop(0) if outcomes else 200
            if outcome == "reset":
                self.connection.shutdown(socket.SHUT_RDWR)
                self.connection.close()
                return
            if outcome == "timeout":
                release_timeouts.wait(timeout=2)
                return
            body = json.dumps({"features": [SAMPLE_FEATURE]}).encode("utf-8")
            self.send_response(outcome)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            if outcome == 429:
                self.send_header("Retry-After", "1")
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    worker = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.01}, daemon=True)
    worker.start()
    api = KMIBelgiumAPI(base_url=f"http://127.0.0.1:{server.server_port}/wfs")
    api.session.trust_env = False
    try:
        yield api, outcomes, paths, sleeps
    finally:
        release_timeouts.set()
        api.session.close()
        server.shutdown()
        server.server_close()
        worker.join(timeout=2)
        assert not worker.is_alive()


@pytest.mark.parametrize("status", [429, 500, 502, 503, 504])
def test_live_wfs_retries_transient_get_statuses_and_returns_features(local_wfs, status):
    api, outcomes, paths, sleeps = local_wfs
    outcomes.extend([status, status, 200])

    assert api.get_observations() == [SAMPLE_FEATURE]

    assert len(paths) == 3
    assert sleeps == ([1, 1] if status == 429 else [2.0])


def test_live_wfs_retry_exhaustion_is_an_error_after_five_attempts(local_wfs):
    api, outcomes, paths, sleeps = local_wfs
    outcomes.extend([502] * 5)

    with pytest.raises(requests.exceptions.RetryError, match="502"):
        api.get_observations()

    assert len(paths) == 5
    assert sleeps == [2.0, 4.0, 8.0]


def test_live_wfs_does_not_retry_permanent_http_errors(local_wfs):
    api, outcomes, paths, sleeps = local_wfs
    outcomes.append(400)

    with pytest.raises(requests.exceptions.HTTPError, match="400"):
        api.get_observations()

    assert len(paths) == 1
    assert sleeps == []


def test_live_wfs_retries_read_resets(local_wfs):
    api, outcomes, paths, sleeps = local_wfs
    outcomes.extend(["reset", "reset", 200])

    assert api.get_observations() == [SAMPLE_FEATURE]

    assert len(paths) == 3
    assert sleeps == [2.0]


def test_live_wfs_read_timeout_exhaustion_is_bounded(local_wfs, monkeypatch):
    api, outcomes, paths, sleeps = local_wfs
    outcomes.extend(["timeout"] * 5)
    request = api.session.request

    def short_timeout(method, url, **kwargs):
        kwargs["timeout"] = (0.2, 0.05)
        return request(method, url, **kwargs)

    monkeypatch.setattr(api.session, "request", short_timeout)
    with pytest.raises(requests.exceptions.ConnectionError, match="Read timed out"):
        api.get_observations()

    assert len(paths) == 5
    assert sleeps == [2.0, 4.0, 8.0]


@pytest.mark.parametrize("failed_connections", [2, 5])
def test_live_wfs_connect_retries_are_bounded(local_wfs, monkeypatch, failed_connections):
    api, _, paths, sleeps = local_wfs
    connect = urllib3_connection.create_connection
    attempts = []

    def interrupted_connection(*args, **kwargs):
        attempts.append(args[0])
        if len(attempts) <= failed_connections:
            raise ConnectionRefusedError("test connection refused")
        return connect(*args, **kwargs)

    monkeypatch.setattr(urllib3_connection, "create_connection", interrupted_connection)
    if failed_connections == 5:
        with pytest.raises(requests.exceptions.ConnectionError, match="test connection refused"):
            api.get_observations()
        assert len(attempts) == 5
        assert paths == []
        assert sleeps == [2.0, 4.0, 8.0]
    else:
        assert api.get_observations() == [SAMPLE_FEATURE]
        assert len(attempts) == 3
        assert len(paths) == 1
        assert sleeps == [2.0]
