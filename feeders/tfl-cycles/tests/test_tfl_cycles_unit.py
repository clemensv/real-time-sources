"""Unit tests for the TfL Santander Cycles core: BikePoint normalization,
dedup signatures, the HTTP acquisition client, and Kafka connection-string
parsing. No network access; the acquisition client is exercised against a
fake ``requests.Session``.
"""

import datetime
import sys
from pathlib import Path

import pytest

THIS_DIR = Path(__file__).resolve().parent
SOURCE_DIR = THIS_DIR.parent
CORE_DIR = SOURCE_DIR / "tfl_cycles_core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from tfl_cycles_core.acquisition import TfLCyclesAPI  # noqa: E402
from tfl_cycles_core.config import (  # noqa: E402
    build_kafka_config,
    parse_kafka_connection_string,
)
from tfl_cycles_core.normalize import parse_bikepoint  # noqa: E402


# ---------------------------------------------------------------------------
# Sample payloads modelled on the live https://api.tfl.gov.uk/BikePoint feed.
# ---------------------------------------------------------------------------

def _prop(key, value, modified="2026-07-14T08:43:26.893Z"):
    return {"key": key, "value": value, "modified": modified}


SAMPLE_STATION = {
    "id": "BikePoints_1",
    "commonName": "River Street , Clerkenwell",
    "lat": 51.529163,
    "lon": -0.10997,
    "additionalProperties": [
        _prop("TerminalName", "001023"),
        _prop("Installed", "true"),
        _prop("Locked", "false"),
        _prop("InstallDate", "1278947280000"),
        _prop("RemovalDate", ""),
        _prop("Temporary", "false"),
        _prop("NbBikes", "12", modified="2026-07-14T08:44:00.000Z"),
        _prop("NbEmptyDocks", "6", modified="2026-07-14T08:44:00.000Z"),
        _prop("NbDocks", "19"),
        _prop("NbStandardBikes", "10", modified="2026-07-14T08:44:00.000Z"),
        _prop("NbEBikes", "2", modified="2026-07-14T08:44:00.000Z"),
    ],
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
        self.last_params = None

    def get(self, url, params=None, timeout=None):
        self.last_url = url
        self.last_params = params
        return _FakeResponse(self.payload)


# ---------------------------------------------------------------------------
# parse_bikepoint
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_parse_bikepoint_reference_fields():
    station = parse_bikepoint(SAMPLE_STATION)
    assert station.station_id == "BikePoints_1"
    assert station.name == "River Street , Clerkenwell"
    assert station.lat == pytest.approx(51.529163)
    assert station.lon == pytest.approx(-0.10997)
    assert station.terminal_name == "001023"
    assert station.capacity == 19
    assert station.temporary is False


@pytest.mark.unit
def test_parse_bikepoint_status_fields():
    station = parse_bikepoint(SAMPLE_STATION)
    assert station.num_bikes_available == 12
    assert station.num_standard_bikes_available == 10
    assert station.num_ebikes_available == 2
    assert station.num_empty_docks == 6
    assert station.num_docks == 19
    assert station.is_installed is True
    assert station.is_locked is False


@pytest.mark.unit
def test_parse_bikepoint_install_date_epoch_ms():
    station = parse_bikepoint(SAMPLE_STATION)
    assert station.install_date is not None
    assert station.install_date.tzinfo is not None
    # 1278947280000 ms == 2010-07-12T15:08:00Z
    assert station.install_date == datetime.datetime(
        2010, 7, 12, 15, 8, 0, tzinfo=datetime.timezone.utc
    )


@pytest.mark.unit
def test_parse_bikepoint_empty_removal_date_is_none():
    station = parse_bikepoint(SAMPLE_STATION)
    assert station.removal_date is None


@pytest.mark.unit
def test_parse_bikepoint_modified_is_newest():
    station = parse_bikepoint(SAMPLE_STATION)
    # newest modified across all additionalProperties entries is 08:44:00
    assert station.modified == datetime.datetime(
        2026, 7, 14, 8, 44, 0, tzinfo=datetime.timezone.utc
    )


@pytest.mark.unit
def test_parse_bikepoint_no_modified_falls_back_to_now():
    raw = {
        "id": "BikePoints_x",
        "commonName": "No Modified",
        "lat": 51.5,
        "lon": -0.1,
        "additionalProperties": [{"key": "NbBikes", "value": "3"}],
    }
    before = datetime.datetime.now(datetime.timezone.utc)
    station = parse_bikepoint(raw)
    after = datetime.datetime.now(datetime.timezone.utc)
    assert before <= station.modified <= after


@pytest.mark.unit
def test_parse_bikepoint_handles_missing_optionals():
    raw = {
        "id": "BikePoints_2",
        "commonName": "Sparse",
        "lat": 51.5,
        "lon": -0.1,
        "additionalProperties": [],
    }
    station = parse_bikepoint(raw)
    assert station.capacity is None
    assert station.num_bikes_available is None
    assert station.num_docks is None
    assert station.is_installed is None
    assert station.terminal_name is None
    assert station.install_date is None


# ---------------------------------------------------------------------------
# Signatures
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_status_signature_excludes_modified():
    station = parse_bikepoint(SAMPLE_STATION)
    sig = station.status_signature()
    assert "modified" not in sig
    assert sig["num_bikes_available"] == 12
    assert sig["num_empty_docks"] == 6


@pytest.mark.unit
def test_status_signature_changes_with_availability():
    station = parse_bikepoint(SAMPLE_STATION)
    sig1 = station.status_signature()
    station.num_bikes_available = 5
    sig2 = station.status_signature()
    assert sig1 != sig2


@pytest.mark.unit
def test_info_signature_excludes_availability():
    station = parse_bikepoint(SAMPLE_STATION)
    sig = station.info_signature()
    assert "num_bikes_available" not in sig
    assert sig["capacity"] == 19
    assert sig["name"] == "River Street , Clerkenwell"


# ---------------------------------------------------------------------------
# Acquisition client
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_list_bikepoints_returns_places():
    session = _FakeSession([SAMPLE_STATION])
    api = TfLCyclesAPI(session=session)
    result = api.list_bikepoints()
    assert isinstance(result, list)
    assert result[0]["id"] == "BikePoints_1"
    assert session.last_url.endswith("/BikePoint")


@pytest.mark.unit
def test_list_bikepoints_non_list_payload_yields_empty():
    session = _FakeSession({"error": "nope"})
    api = TfLCyclesAPI(session=session)
    assert api.list_bikepoints() == []


@pytest.mark.unit
def test_app_key_added_to_params():
    session = _FakeSession([SAMPLE_STATION])
    api = TfLCyclesAPI(session=session, app_key="secret-key")
    api.list_bikepoints()
    assert session.last_params == {"app_key": "secret-key"}


@pytest.mark.unit
def test_no_app_key_means_empty_params():
    session = _FakeSession([SAMPLE_STATION])
    api = TfLCyclesAPI(session=session)
    api.list_bikepoints()
    assert session.last_params == {}


# ---------------------------------------------------------------------------
# Kafka connection-string parsing / config
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_parse_harness_connection_string():
    cfg = parse_kafka_connection_string("BootstrapServer=broker:9092;EntityPath=tfl-cycles")
    assert cfg["bootstrap.servers"] == "broker:9092"
    assert cfg["kafka_topic"] == "tfl-cycles"
    assert "security.protocol" not in cfg


@pytest.mark.unit
def test_parse_eventhubs_connection_string():
    conn = (
        "Endpoint=sb://ns.servicebus.windows.net/;"
        "SharedAccessKeyName=RootKey;SharedAccessKey=abc123;EntityPath=tfl-cycles"
    )
    cfg = parse_kafka_connection_string(conn)
    assert cfg["bootstrap.servers"] == "ns.servicebus.windows.net:9093"
    assert cfg["kafka_topic"] == "tfl-cycles"
    assert cfg["security.protocol"] == "SASL_SSL"
    assert cfg["sasl.mechanism"] == "PLAIN"
    assert cfg["sasl.username"] == "$ConnectionString"
    assert cfg["sasl.password"] == conn.strip()


@pytest.mark.unit
def test_build_kafka_config_plain():
    cfg = build_kafka_config(bootstrap_servers="localhost:9092", tls_enabled=False)
    assert cfg["bootstrap.servers"] == "localhost:9092"
    assert cfg["client.id"] == "tfl-cycles"
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
