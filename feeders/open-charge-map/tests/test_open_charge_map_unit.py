"""Unit tests for the Open Charge Map core: POI normalization, reference-data
flattening, the ``DateLastStatusUpdate`` dedup watermark, datetime parsing, the
HTTP acquisition client (exercised against a fake ``requests.Session`` -- no
network), and Kafka connection-string / config parsing.
"""

import datetime
import json
import sys
import tempfile
from pathlib import Path

import pytest

THIS_DIR = Path(__file__).resolve().parent
SOURCE_DIR = THIS_DIR.parent
CORE_DIR = SOURCE_DIR / "open_charge_map_core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from open_charge_map_core.acquisition import OpenChargeMapAPI  # noqa: E402
from open_charge_map_core.config import (  # noqa: E402
    FeedConfig,
    build_kafka_config,
    parse_kafka_connection_string,
)
from open_charge_map_core.normalize import (  # noqa: E402
    parse_ocm_datetime,
    parse_poi,
    parse_reference_data,
)
from open_charge_map_core.state import load_state, save_state  # noqa: E402


# ---------------------------------------------------------------------------
# Sample payloads modelled on the live https://api.openchargemap.io/v3/ feeds.
# ---------------------------------------------------------------------------

SAMPLE_POI = {
    "ID": 498664,
    "UUID": "1B0E3F2A-1234-4C0D-8AAA-000000000001",
    "DataProviderID": 1,
    "OperatorID": 45,
    "OperatorInfo": {"ID": 45, "Title": "ESB ecars"},
    "UsageTypeID": 4,
    "UsageType": {"ID": 4, "Title": "Public - Membership Required"},
    "UsageCost": "Free",
    "StatusTypeID": 50,
    "StatusType": {"ID": 50, "Title": "Operational", "IsOperational": True},
    "SubmissionStatusTypeID": 200,
    "SubmissionStatus": {"ID": 200, "Title": "Submission Published"},
    "DataQualityLevel": 1,
    "NumberOfPoints": 2,
    "GeneralComments": "  Beside the town hall  ",
    "IsRecentlyVerified": True,
    "DateCreated": "2011-11-24T00:00:00Z",
    "DateLastStatusUpdate": "2026-07-13T10:00:00Z",
    "DateLastVerified": "2026-07-01T09:00:00Z",
    "AddressInfo": {
        "ID": 500001,
        "Title": "Cork City Hall",
        "AddressLine1": "Anglesea Street",
        "AddressLine2": "",
        "Town": "Cork",
        "StateOrProvince": "Munster",
        "Postcode": "T12 X8H6",
        "CountryID": 2,
        "Country": {"ID": 2, "ISOCode": "IE", "Title": "Ireland"},
        "Latitude": 51.91434912424549,
        "Longitude": -8.177792617023329,
        "ContactTelephone1": "",
        "AccessComments": "24 hours",
    },
    "Connections": [
        {
            "ID": 900001,
            "ConnectionTypeID": 25,
            "ConnectionType": {"ID": 25, "Title": "Type 2 (Socket Only)", "FormalName": "IEC 62196-2 Type 2"},
            "Reference": "A",
            "StatusTypeID": 50,
            "StatusType": {"ID": 50, "IsOperational": True},
            "LevelID": 2,
            "Level": {"ID": 2, "Title": "Level 2 : Medium", "IsFastChargeCapable": False},
            "Amps": 32,
            "Voltage": 400,
            "PowerKW": 22.0,
            "CurrentTypeID": 20,
            "CurrentType": {"ID": 20, "Title": "AC (Three-Phase)"},
            "Quantity": 1,
            "Comments": "",
        }
    ],
}

SAMPLE_REFERENCE_DATA = {
    "Operators": [
        {
            "ID": 45,
            "Title": "ESB ecars",
            "WebsiteURL": "https://esb.ie/ecars",
            "Comments": "",
            "PhonePrimaryContact": "1800 372 757",
            "ContactEmail": "ecars@esb.ie",
            "IsPrivateIndividual": False,
            "IsRestrictedEdit": True,
        }
    ],
    "ConnectionTypes": [
        {"ID": 25, "Title": "Type 2 (Socket Only)", "FormalName": "IEC 62196-2 Type 2", "IsDiscontinued": False, "IsObsolete": False}
    ],
    "CurrentTypes": [{"ID": 20, "Title": "AC (Three-Phase)", "Description": "Alternating Current - Three Phase"}],
    "ChargerTypes": [{"ID": 2, "Title": "Level 2 : Medium (Over 2kW)", "Comments": "", "IsFastChargeCapable": False}],
    "Countries": [{"ID": 2, "Title": "Ireland", "ISOCode": "IE", "ContinentCode": "EU"}],
    "DataProviders": [
        {
            "ID": 1,
            "Title": "Open Charge Map Contributors",
            "WebsiteURL": "https://openchargemap.org",
            "License": "Open Data",
            "IsOpenDataLicensed": True,
            "IsRestrictedEdit": False,
            "IsApprovedImport": False,
            "DataProviderStatusType": {"ID": 1, "IsProviderEnabled": True, "Title": "Automated Import"},
            "DateLastImported": "2026-07-10T12:00:00Z",
        }
    ],
    "StatusTypes": [{"ID": 50, "Title": "Operational", "IsOperational": True, "IsUserSelectable": True}],
    "UsageTypes": [
        {"ID": 4, "Title": "Public - Membership Required", "IsPayAtLocation": False, "IsMembershipRequired": True, "IsAccessKeyRequired": True}
    ],
    "SubmissionStatusTypes": [{"ID": 200, "Title": "Submission Published", "IsLive": True}],
    # A table the feeder does NOT emit -- must be ignored.
    "UserCommentTypes": [{"ID": 10, "Title": "General Comment"}],
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
        self.last_timeout = None

    def get(self, url, params=None, timeout=None):
        self.last_url = url
        self.last_params = params
        self.last_timeout = timeout
        return _FakeResponse(self.payload)


# ---------------------------------------------------------------------------
# parse_poi -- identity, denormalized labels, address, connections
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_parse_poi_identity_and_labels():
    loc = parse_poi(SAMPLE_POI)
    assert loc.poi_id == 498664
    assert loc.uuid == "1B0E3F2A-1234-4C0D-8AAA-000000000001"
    assert loc.operator_id == 45
    assert loc.operator_title == "ESB ecars"
    assert loc.usage_type_title == "Public - Membership Required"
    assert loc.status_title == "Operational"
    assert loc.is_operational is True
    assert loc.submission_status_title == "Submission Published"
    assert loc.number_of_points == 2
    # GeneralComments is trimmed.
    assert loc.general_comments == "Beside the town hall"


@pytest.mark.unit
def test_parse_poi_flattened_address_and_coords():
    loc = parse_poi(SAMPLE_POI)
    assert loc.address_title == "Cork City Hall"
    assert loc.town == "Cork"
    assert loc.postcode == "T12 X8H6"
    assert loc.country_iso_code == "IE"
    assert loc.country_title == "Ireland"
    assert loc.latitude == pytest.approx(51.91434912424549)
    assert loc.longitude == pytest.approx(-8.177792617023329)
    # Empty strings normalize to None.
    assert loc.address_line2 is None
    assert loc.contact_telephone1 is None


@pytest.mark.unit
def test_parse_poi_connections():
    loc = parse_poi(SAMPLE_POI)
    assert len(loc.connections) == 1
    c = loc.connections[0]
    assert c.connection_id == 900001
    assert c.connection_type_title == "Type 2 (Socket Only)"
    assert c.connection_type_formal_name == "IEC 62196-2 Type 2"
    assert c.is_operational is True
    assert c.level_title == "Level 2 : Medium"
    assert c.is_fast_charge_capable is False
    assert c.amps == 32
    assert c.voltage == 400
    assert c.power_kw == pytest.approx(22.0)
    assert c.current_type_title == "AC (Three-Phase)"
    assert c.quantity == 1
    assert c.comments is None


@pytest.mark.unit
def test_parse_poi_datetimes_utc():
    loc = parse_poi(SAMPLE_POI)
    assert loc.date_created == datetime.datetime(2011, 11, 24, 0, 0, 0, tzinfo=datetime.timezone.utc)
    assert loc.date_last_status_update == datetime.datetime(2026, 7, 13, 10, 0, 0, tzinfo=datetime.timezone.utc)
    assert loc.date_last_verified == datetime.datetime(2026, 7, 1, 9, 0, 0, tzinfo=datetime.timezone.utc)
    # DatePlanned / DateLastConfirmed absent -> None.
    assert loc.date_planned is None
    assert loc.date_last_confirmed is None


@pytest.mark.unit
def test_parse_poi_sparse_record():
    raw = {"ID": 777, "AddressInfo": {"Latitude": 1.0, "Longitude": 2.0}}
    loc = parse_poi(raw)
    assert loc.poi_id == 777
    assert loc.operator_id is None
    assert loc.operator_title is None
    assert loc.status_title is None
    assert loc.number_of_points is None
    assert loc.connections == []
    assert loc.date_last_status_update is None
    assert loc.latitude == pytest.approx(1.0)


@pytest.mark.unit
def test_parse_poi_missing_id_yields_zero():
    loc = parse_poi({"UUID": "x"})
    assert loc.poi_id == 0


# ---------------------------------------------------------------------------
# Watermark / dedup signatures
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_change_signature_uses_last_status_update():
    loc = parse_poi(SAMPLE_POI)
    assert loc.change_signature() == "2026-07-13T10:00:00+00:00"


@pytest.mark.unit
def test_change_signature_falls_back_to_created():
    raw = dict(SAMPLE_POI)
    raw.pop("DateLastStatusUpdate")
    loc = parse_poi(raw)
    assert loc.change_signature() == "2011-11-24T00:00:00+00:00"


@pytest.mark.unit
def test_change_signature_none_when_no_dates():
    loc = parse_poi({"ID": 1})
    assert loc.change_signature() is None


@pytest.mark.unit
def test_latest_change_is_max_instant():
    loc = parse_poi(SAMPLE_POI)
    # DateLastStatusUpdate (2026-07-13) is the most recent of the populated instants.
    assert loc.latest_change() == datetime.datetime(2026, 7, 13, 10, 0, 0, tzinfo=datetime.timezone.utc)


# ---------------------------------------------------------------------------
# parse_ocm_datetime
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_parse_ocm_datetime_z_suffix():
    dt = parse_ocm_datetime("2026-07-13T10:00:00Z")
    assert dt == datetime.datetime(2026, 7, 13, 10, 0, 0, tzinfo=datetime.timezone.utc)


@pytest.mark.unit
def test_parse_ocm_datetime_naive_assumed_utc():
    dt = parse_ocm_datetime("2026-07-13T10:00:00")
    assert dt.tzinfo == datetime.timezone.utc


@pytest.mark.unit
def test_parse_ocm_datetime_empty_and_bad():
    assert parse_ocm_datetime("") is None
    assert parse_ocm_datetime(None) is None
    assert parse_ocm_datetime("not-a-date") is None


# ---------------------------------------------------------------------------
# parse_reference_data -- all nine tables
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_parse_reference_data_counts_and_types():
    refs = parse_reference_data(SAMPLE_REFERENCE_DATA)
    by_type = {}
    for r in refs:
        by_type[r.reference_type] = by_type.get(r.reference_type, 0) + 1
    assert by_type == {
        "operator": 1,
        "connection_type": 1,
        "current_type": 1,
        "charger_type": 1,
        "country": 1,
        "data_provider": 1,
        "status_type": 1,
        "usage_type": 1,
        "submission_status_type": 1,
    }
    # The non-emitted table is ignored.
    assert "user_comment_type" not in by_type


@pytest.mark.unit
def test_parse_reference_operator_fields():
    refs = parse_reference_data(SAMPLE_REFERENCE_DATA)
    op = next(r for r in refs if r.reference_type == "operator")
    assert op.reference_id == 45
    assert op.fields["reference_type"] == "operator"
    assert op.fields["reference_id"] == 45
    assert op.fields["title"] == "ESB ecars"
    assert op.fields["website_url"] == "https://esb.ie/ecars"
    assert op.fields["contact_email"] == "ecars@esb.ie"
    assert op.fields["is_private_individual"] is False
    assert op.fields["is_restricted_edit"] is True
    assert op.fields["comments"] is None


@pytest.mark.unit
def test_parse_reference_data_provider_status_mapping():
    refs = parse_reference_data(SAMPLE_REFERENCE_DATA)
    dp = next(r for r in refs if r.reference_type == "data_provider")
    # DataProviderStatusType.Title / .IsProviderEnabled are hoisted onto flat fields.
    assert dp.fields["status_title"] == "Automated Import"
    assert dp.fields["is_provider_enabled"] is True
    assert dp.fields["is_open_data_licensed"] is True
    assert dp.fields["license"] == "Open Data"
    assert dp.fields["date_last_imported"] is not None
    assert dp.fields["date_last_imported"].year == 2026


@pytest.mark.unit
def test_parse_reference_country_and_status_fields():
    refs = parse_reference_data(SAMPLE_REFERENCE_DATA)
    country = next(r for r in refs if r.reference_type == "country")
    assert country.fields["iso_code"] == "IE"
    assert country.fields["continent_code"] == "EU"
    status = next(r for r in refs if r.reference_type == "status_type")
    assert status.fields["is_operational"] is True
    assert status.fields["is_user_selectable"] is True


@pytest.mark.unit
def test_parse_reference_skips_records_without_id():
    refs = parse_reference_data({"Operators": [{"Title": "no id"}]})
    assert refs == []


# ---------------------------------------------------------------------------
# Acquisition client
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_api_requires_key(monkeypatch):
    monkeypatch.delenv("OPENCHARGEMAP_API_KEY", raising=False)
    with pytest.raises(ValueError):
        OpenChargeMapAPI(session=_FakeSession([]))


@pytest.mark.unit
def test_api_sets_key_header():
    session = _FakeSession([])
    OpenChargeMapAPI(api_key="secret-key", session=session)
    assert session.headers["X-API-Key"] == "secret-key"
    assert "User-Agent" in session.headers


@pytest.mark.unit
def test_list_reference_data_dict():
    session = _FakeSession(SAMPLE_REFERENCE_DATA)
    api = OpenChargeMapAPI(api_key="k", session=session)
    data = api.list_reference_data()
    assert "Operators" in data
    assert session.last_url.endswith("referencedata/")


@pytest.mark.unit
def test_list_reference_data_non_dict_yields_empty():
    session = _FakeSession(["not", "a", "dict"])
    api = OpenChargeMapAPI(api_key="k", session=session)
    assert api.list_reference_data() == {}


@pytest.mark.unit
def test_list_pois_returns_list_and_params():
    session = _FakeSession([SAMPLE_POI])
    api = OpenChargeMapAPI(api_key="k", session=session)
    since = datetime.datetime(2026, 7, 10, 8, 30, 0, tzinfo=datetime.timezone.utc)
    result = api.list_pois(modified_since=since, country_code="IE", max_results=25, opendata=True)
    assert result[0]["ID"] == 498664
    assert session.last_url.endswith("poi/")
    p = session.last_params
    assert p["compact"] == "false"
    assert p["verbose"] == "false"
    assert p["maxresults"] == 25
    assert p["opendata"] == "true"
    assert p["countrycode"] == "IE"
    assert p["modifiedsince"] == "2026-07-10T08:30:00Z"


@pytest.mark.unit
def test_list_pois_no_scope_omits_optional_params():
    session = _FakeSession([])
    api = OpenChargeMapAPI(api_key="k", session=session)
    api.list_pois(opendata=False)
    p = session.last_params
    assert "countrycode" not in p
    assert "modifiedsince" not in p
    assert "opendata" not in p


@pytest.mark.unit
def test_list_pois_non_list_yields_empty():
    session = _FakeSession({"error": "nope"})
    api = OpenChargeMapAPI(api_key="k", session=session)
    assert api.list_pois() == []


# ---------------------------------------------------------------------------
# Config / connection-string parsing
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_parse_harness_connection_string():
    cfg = parse_kafka_connection_string("BootstrapServer=broker:9092;EntityPath=open-charge-map")
    assert cfg["bootstrap.servers"] == "broker:9092"
    assert cfg["kafka_topic"] == "open-charge-map"
    assert "security.protocol" not in cfg


@pytest.mark.unit
def test_parse_eventhubs_connection_string():
    conn = (
        "Endpoint=sb://ns.servicebus.windows.net/;"
        "SharedAccessKeyName=RootKey;SharedAccessKey=abc123;EntityPath=open-charge-map"
    )
    cfg = parse_kafka_connection_string(conn)
    assert cfg["bootstrap.servers"] == "ns.servicebus.windows.net:9093"
    assert cfg["kafka_topic"] == "open-charge-map"
    assert cfg["security.protocol"] == "SASL_SSL"
    assert cfg["sasl.mechanism"] == "PLAIN"
    assert cfg["sasl.username"] == "$ConnectionString"


@pytest.mark.unit
def test_build_kafka_config_plain():
    cfg = build_kafka_config(bootstrap_servers="localhost:9092", tls_enabled=False)
    assert cfg["bootstrap.servers"] == "localhost:9092"
    assert cfg["client.id"] == "open-charge-map"
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


@pytest.mark.unit
def test_feed_config_from_env_defaults(monkeypatch):
    for var in (
        "POLLING_INTERVAL", "STATE_FILE", "ONCE_MODE", "REFERENCE_REFRESH_INTERVAL",
        "OCM_COUNTRYCODE", "OCM_MODIFIED_SINCE_DAYS", "OCM_MAX_RESULTS", "OCM_OPENDATA",
    ):
        monkeypatch.delenv(var, raising=False)
    cfg = FeedConfig.from_env()
    assert cfg.polling_interval == 600
    assert cfg.reference_refresh_interval == 86400
    assert cfg.modified_since_days == 1
    assert cfg.max_results == 5000
    assert cfg.opendata is True
    assert cfg.country_code is None


@pytest.mark.unit
def test_feed_config_from_env_overrides(monkeypatch):
    monkeypatch.setenv("OCM_COUNTRYCODE", "GB")
    monkeypatch.setenv("OCM_OPENDATA", "false")
    monkeypatch.setenv("OCM_MAX_RESULTS", "100")
    cfg = FeedConfig.from_env()
    assert cfg.country_code == "GB"
    assert cfg.opendata is False
    assert cfg.max_results == 100


# ---------------------------------------------------------------------------
# State persistence
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_state_roundtrip():
    with tempfile.TemporaryDirectory() as d:
        path = str(Path(d) / "state.json")
        payload = {"watermark": "2026-07-13T10:00:00+00:00", "pois": {"1": "sig-a"}}
        save_state(path, payload)
        assert json.loads(Path(path).read_text()) == payload
        assert load_state(path) == payload


@pytest.mark.unit
def test_load_state_missing_returns_empty():
    assert load_state(str(Path(tempfile.gettempdir()) / "does-not-exist-ocm.json")) == {}


@pytest.mark.unit
def test_load_state_empty_path_returns_empty():
    assert load_state("") == {}
