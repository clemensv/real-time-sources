"""Unit tests for the KMI Belgium weather bridge."""

import sys
import types
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone


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
