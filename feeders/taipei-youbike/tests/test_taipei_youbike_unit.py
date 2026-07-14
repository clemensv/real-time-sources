"""Unit tests for the Taiwan YouBike 2.0 core: station normalization, dedup
signatures, the HTTP acquisition client, and Kafka connection-string parsing.
No network access; the acquisition client is exercised against a fake
``requests.Session``.
"""

import datetime
import sys
from pathlib import Path

import pytest

THIS_DIR = Path(__file__).resolve().parent
SOURCE_DIR = THIS_DIR.parent
CORE_DIR = SOURCE_DIR / "taipei_youbike_core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from taipei_youbike_core.acquisition import YouBikeAPI  # noqa: E402
from taipei_youbike_core.config import (  # noqa: E402
    build_kafka_config,
    parse_kafka_connection_string,
)
from taipei_youbike_core.normalize import parse_station  # noqa: E402


# ---------------------------------------------------------------------------
# Sample payload modelled on the live
# https://apis.youbike.com.tw/json/station-yb2.json feed. One flat station
# object carrying both reference and availability fields.
# ---------------------------------------------------------------------------

SAMPLE_STATION = {
    "station_no": "500101001",
    "name_tw": "捷運科技大樓站",
    "name_en": "MRT Technology Bldg. Sta.",
    "name_cn": "",
    "district_tw": "大安區",
    "district_en": "Daan Dist.",
    "district_cn": "",
    "address_tw": "復興南路二段235號前",
    "address_en": "No.235, Sec. 2, Fuxing S. Rd.",
    "address_cn": "",
    "lat": 25.02605,
    "lng": 121.5436,
    "parking_spaces": 28,
    "type": 2,
    "country_code": "00",
    "area_code": "00",
    "img": "",
    "available_spaces": 10,
    "available_spaces_detail": {"yb1": 0, "yb2": 8, "eyb": 2},
    "empty_spaces": 18,
    "forbidden_spaces": 0,
    "available_spaces_level": 40,
    "status": 1,
    "updated_at": "2026-07-15 01:30:34",
    "time": "2026-07-15 01:30:04",
}


class _FakeResponse:
    def __init__(self, payload, status_ok=True):
        self._payload = payload
        self._status_ok = status_ok

    def raise_for_status(self):
        if not self._status_ok:
            raise RuntimeError("HTTP error")

    def json(self):
        return self._payload


class _FakeSession:
    def __init__(self, payload):
        self.payload = payload
        self.headers = {}
        self.last_url = None
        self.last_timeout = None

    def get(self, url, params=None, timeout=None):
        self.last_url = url
        self.last_timeout = timeout
        return _FakeResponse(self.payload)


# ---------------------------------------------------------------------------
# parse_station -- reference fields
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_parse_station_reference_fields():
    station = parse_station(SAMPLE_STATION)
    assert station.station_id == "500101001"
    assert station.name_tw == "捷運科技大樓站"
    assert station.name_en == "MRT Technology Bldg. Sta."
    assert station.district_tw == "大安區"
    assert station.address_en == "No.235, Sec. 2, Fuxing S. Rd."
    assert station.lat == pytest.approx(25.02605)
    # longitude comes from the upstream ``lng`` key.
    assert station.lon == pytest.approx(121.5436)
    assert station.capacity == 28
    assert station.station_type == 2
    assert station.country_code == "00"
    assert station.area_code == "00"


@pytest.mark.unit
def test_parse_station_empty_strings_become_none():
    station = parse_station(SAMPLE_STATION)
    # The upstream fills unavailable text fields (Simplified Chinese, img) with "".
    assert station.name_cn is None
    assert station.district_cn is None
    assert station.address_cn is None
    assert station.img is None


# ---------------------------------------------------------------------------
# parse_station -- availability / status fields
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_parse_station_status_fields():
    station = parse_station(SAMPLE_STATION)
    assert station.num_bikes_available == 10
    assert station.num_bikes_yb1 == 0
    assert station.num_bikes_yb2 == 8
    assert station.num_ebikes_available == 2
    assert station.num_empty_docks == 18
    assert station.num_forbidden_docks == 0
    assert station.availability_level == 40
    assert station.service_status == 1


@pytest.mark.unit
def test_parse_station_timestamps_converted_taipei_to_utc():
    station = parse_station(SAMPLE_STATION)
    # 2026-07-15 01:30:34 in UTC+8 == 2026-07-14 17:30:34 UTC.
    assert station.updated_at == datetime.datetime(
        2026, 7, 14, 17, 30, 34, tzinfo=datetime.timezone.utc
    )
    assert station.snapshot_time == datetime.datetime(
        2026, 7, 14, 17, 30, 4, tzinfo=datetime.timezone.utc
    )


@pytest.mark.unit
def test_parse_station_missing_updated_at_falls_back_to_now():
    raw = dict(SAMPLE_STATION)
    raw.pop("updated_at")
    before = datetime.datetime.now(datetime.timezone.utc)
    station = parse_station(raw)
    after = datetime.datetime.now(datetime.timezone.utc)
    assert before <= station.updated_at <= after


@pytest.mark.unit
def test_parse_station_handles_missing_optionals():
    raw = {
        "station_no": "500101999",
        "name_tw": "Sparse",
        "lat": 25.0,
        "lng": 121.5,
    }
    station = parse_station(raw)
    assert station.capacity is None
    assert station.station_type is None
    assert station.num_bikes_available is None
    assert station.num_bikes_yb1 is None
    assert station.num_empty_docks is None
    assert station.availability_level is None
    assert station.service_status is None
    assert station.snapshot_time is None
    # updated_at always resolves (falls back to now()).
    assert station.updated_at.tzinfo is not None


# ---------------------------------------------------------------------------
# Signatures
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_status_signature_excludes_timestamps():
    station = parse_station(SAMPLE_STATION)
    sig = station.status_signature()
    assert "updated_at" not in sig
    assert "snapshot_time" not in sig
    assert sig["num_bikes_available"] == 10
    assert sig["num_empty_docks"] == 18


@pytest.mark.unit
def test_status_signature_changes_with_availability():
    station = parse_station(SAMPLE_STATION)
    sig1 = station.status_signature()
    station.num_bikes_available = 3
    sig2 = station.status_signature()
    assert sig1 != sig2


@pytest.mark.unit
def test_info_signature_excludes_availability():
    station = parse_station(SAMPLE_STATION)
    sig = station.info_signature()
    assert "num_bikes_available" not in sig
    assert "service_status" not in sig
    assert sig["capacity"] == 28
    assert sig["name_tw"] == "捷運科技大樓站"


# ---------------------------------------------------------------------------
# Acquisition client
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_list_stations_returns_stations():
    session = _FakeSession([SAMPLE_STATION])
    api = YouBikeAPI(session=session)
    result = api.list_stations()
    assert isinstance(result, list)
    assert result[0]["station_no"] == "500101001"
    assert session.last_url.endswith("station-yb2.json")


@pytest.mark.unit
def test_list_stations_non_list_payload_yields_empty():
    session = _FakeSession({"error": "nope"})
    api = YouBikeAPI(session=session)
    assert api.list_stations() == []


@pytest.mark.unit
def test_feed_url_override():
    session = _FakeSession([SAMPLE_STATION])
    api = YouBikeAPI(session=session, feed_url="https://mirror.example/yb.json")
    api.list_stations()
    assert session.last_url == "https://mirror.example/yb.json"


# ---------------------------------------------------------------------------
# Kafka connection-string parsing / config
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_parse_harness_connection_string():
    cfg = parse_kafka_connection_string(
        "BootstrapServer=broker:9092;EntityPath=taipei-youbike"
    )
    assert cfg["bootstrap.servers"] == "broker:9092"
    assert cfg["kafka_topic"] == "taipei-youbike"
    assert "security.protocol" not in cfg


@pytest.mark.unit
def test_parse_eventhubs_connection_string():
    conn = (
        "Endpoint=sb://ns.servicebus.windows.net/;"
        "SharedAccessKeyName=RootKey;SharedAccessKey=abc123;EntityPath=taipei-youbike"
    )
    cfg = parse_kafka_connection_string(conn)
    assert cfg["bootstrap.servers"] == "ns.servicebus.windows.net:9093"
    assert cfg["kafka_topic"] == "taipei-youbike"
    assert cfg["security.protocol"] == "SASL_SSL"
    assert cfg["sasl.mechanism"] == "PLAIN"
    assert cfg["sasl.username"] == "$ConnectionString"
    assert cfg["sasl.password"] == conn.strip()


@pytest.mark.unit
def test_build_kafka_config_plain():
    cfg = build_kafka_config(bootstrap_servers="localhost:9092", tls_enabled=False)
    assert cfg["bootstrap.servers"] == "localhost:9092"
    assert cfg["client.id"] == "taipei-youbike"
    assert "security.protocol" not in cfg


@pytest.mark.unit
def test_build_kafka_config_sasl():
    cfg = build_kafka_config(
        bootstrap_servers="ns:9093",
        sasl_username="$ConnectionString",
        sasl_password="secret",
        tls_enabled=True,
    )
    assert cfg["security.protocol"] == "SASL_SSL"
    assert cfg["sasl.mechanisms"] == "PLAIN"
    assert cfg["sasl.username"] == "$ConnectionString"
