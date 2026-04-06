"""Unit tests for NDL Netherlands bridge normalization and diffing logic."""

from __future__ import annotations

import json
import pytest
from datetime import datetime, timezone

from ndl_netherlands.ndl_netherlands import (
    normalize_location,
    normalize_evse,
    normalize_connector,
    normalize_tariff,
    parse_connection_string,
    NdlPoller,
    _parse_optional_float,
    _parse_optional_bool,
    _safe_string,
    _safe_string_list,
    _to_datetime,
)


# ── Helper fixtures ──────────────────────────────────────────────────────────

def _make_raw_connector(**overrides):
    base = {
        "id": "1",
        "standard": "IEC_62196_T2",
        "format": "SOCKET",
        "power_type": "AC_3_PHASE",
        "max_voltage": 230,
        "max_amperage": 32,
    }
    base.update(overrides)
    return base


def _make_raw_evse(**overrides):
    base = {
        "uid": "EVSE001",
        "evse_id": "NL*ABC*E001",
        "status": "AVAILABLE",
        "connectors": [_make_raw_connector()],
        "last_updated": "2024-01-15T10:30:00Z",
    }
    base.update(overrides)
    return base


def _make_raw_location(**overrides):
    base = {
        "id": "LOC001",
        "country_code": "NL",
        "party_id": "ABC",
        "publish": True,
        "name": "Test Station",
        "address": "Keizersgracht 100",
        "city": "Amsterdam",
        "postal_code": "1015AA",
        "country": "NLD",
        "coordinates": {"latitude": "52.370216", "longitude": "4.895168"},
        "time_zone": "Europe/Amsterdam",
        "evses": [_make_raw_evse()],
        "last_updated": "2024-01-15T10:30:00Z",
    }
    base.update(overrides)
    return base


def _make_raw_tariff(**overrides):
    base = {
        "id": "TAR001",
        "country_code": "NL",
        "party_id": "ABC",
        "currency": "EUR",
        "elements": [
            {
                "price_components": [
                    {"type": "ENERGY", "price": 0.25, "step_size": 1}
                ]
            }
        ],
        "last_updated": "2024-01-15T10:30:00Z",
    }
    base.update(overrides)
    return base


# ── Utility function tests ───────────────────────────────────────────────────

class TestParseOptionalFloat:
    @pytest.mark.unit
    def test_none_returns_none(self):
        assert _parse_optional_float(None) is None

    @pytest.mark.unit
    def test_empty_string_returns_none(self):
        assert _parse_optional_float("") is None

    @pytest.mark.unit
    def test_valid_float(self):
        assert _parse_optional_float("52.37") == 52.37

    @pytest.mark.unit
    def test_comma_decimal(self):
        assert _parse_optional_float("52,37") == 52.37

    @pytest.mark.unit
    def test_integer_value(self):
        assert _parse_optional_float(230) == 230.0

    @pytest.mark.unit
    def test_undefined_returns_none(self):
        assert _parse_optional_float("undefined") is None

    @pytest.mark.unit
    def test_invalid_string_returns_none(self):
        assert _parse_optional_float("not-a-number") is None


class TestParseOptionalBool:
    @pytest.mark.unit
    def test_none_returns_none(self):
        assert _parse_optional_bool(None) is None

    @pytest.mark.unit
    def test_true_bool(self):
        assert _parse_optional_bool(True) is True

    @pytest.mark.unit
    def test_false_bool(self):
        assert _parse_optional_bool(False) is False

    @pytest.mark.unit
    def test_true_string(self):
        assert _parse_optional_bool("true") is True

    @pytest.mark.unit
    def test_false_string(self):
        assert _parse_optional_bool("false") is False

    @pytest.mark.unit
    def test_yes_string(self):
        assert _parse_optional_bool("yes") is True


class TestSafeString:
    @pytest.mark.unit
    def test_none_returns_none(self):
        assert _safe_string(None) is None

    @pytest.mark.unit
    def test_empty_returns_none(self):
        assert _safe_string("") is None

    @pytest.mark.unit
    def test_whitespace_returns_none(self):
        assert _safe_string("   ") is None

    @pytest.mark.unit
    def test_valid_string(self):
        assert _safe_string("hello") == "hello"

    @pytest.mark.unit
    def test_strips_whitespace(self):
        assert _safe_string("  hello  ") == "hello"


class TestSafeStringList:
    @pytest.mark.unit
    def test_non_list_returns_none(self):
        assert _safe_string_list("not a list") is None

    @pytest.mark.unit
    def test_empty_list_returns_none(self):
        assert _safe_string_list([]) is None

    @pytest.mark.unit
    def test_valid_list(self):
        assert _safe_string_list(["a", "b"]) == ["a", "b"]

    @pytest.mark.unit
    def test_filters_nones(self):
        assert _safe_string_list(["a", None, "b"]) == ["a", "b"]


class TestToDatetime:
    @pytest.mark.unit
    def test_iso_string(self):
        result = _to_datetime("2024-01-15T10:30:00Z")
        assert isinstance(result, datetime)
        assert result.year == 2024
        assert result.month == 1

    @pytest.mark.unit
    def test_datetime_passthrough(self):
        dt = datetime(2024, 1, 15, tzinfo=timezone.utc)
        assert _to_datetime(dt) is dt

    @pytest.mark.unit
    def test_none_returns_now(self):
        result = _to_datetime(None)
        assert isinstance(result, datetime)


# ── Connector normalization ──────────────────────────────────────────────────

class TestNormalizeConnector:
    @pytest.mark.unit
    def test_basic_connector(self):
        raw = _make_raw_connector()
        result = normalize_connector(raw)
        assert result["connector_id"] == "1"
        assert result["standard"] == "IEC_62196_T2"
        assert result["format"] == "SOCKET"
        assert result["power_type"] == "AC_3_PHASE"
        assert result["max_voltage"] == 230
        assert result["max_amperage"] == 32
        assert result["max_electric_power"] is None
        assert result["tariff_ids"] is None

    @pytest.mark.unit
    def test_connector_with_max_power(self):
        raw = _make_raw_connector(max_electric_power=150000)
        result = normalize_connector(raw)
        assert result["max_electric_power"] == 150000

    @pytest.mark.unit
    def test_connector_with_tariff_ids(self):
        raw = _make_raw_connector(tariff_ids=["TAR001", "TAR002"])
        result = normalize_connector(raw)
        assert result["tariff_ids"] == ["TAR001", "TAR002"]

    @pytest.mark.unit
    def test_dc_connector(self):
        raw = _make_raw_connector(
            standard="IEC_62196_T2_COMBO",
            format="CABLE",
            power_type="DC",
            max_voltage=920,
            max_amperage=400,
            max_electric_power=350000,
        )
        result = normalize_connector(raw)
        assert result["standard"] == "IEC_62196_T2_COMBO"
        assert result["format"] == "CABLE"
        assert result["power_type"] == "DC"
        assert result["max_electric_power"] == 350000


# ── EVSE normalization ───────────────────────────────────────────────────────

class TestNormalizeEvse:
    @pytest.mark.unit
    def test_basic_evse(self):
        raw = _make_raw_evse()
        result = normalize_evse("LOC001", raw)
        assert result is not None
        assert result["location_id"] == "LOC001"
        assert result["evse_uid"] == "EVSE001"
        assert result["evse_id"] == "NL*ABC*E001"
        assert result["status"] == "AVAILABLE"
        assert len(result["connectors"]) == 1
        assert result["last_updated"] == "2024-01-15T10:30:00Z"

    @pytest.mark.unit
    def test_missing_uid_returns_none(self):
        raw = _make_raw_evse()
        del raw["uid"]
        assert normalize_evse("LOC001", raw) is None

    @pytest.mark.unit
    def test_no_connectors_returns_none(self):
        raw = _make_raw_evse(connectors=[])
        assert normalize_evse("LOC001", raw) is None

    @pytest.mark.unit
    def test_evse_with_coordinates(self):
        raw = _make_raw_evse(coordinates={"latitude": "52.1", "longitude": "4.9"})
        result = normalize_evse("LOC001", raw)
        assert result["latitude"] == 52.1
        assert result["longitude"] == 4.9

    @pytest.mark.unit
    def test_evse_without_coordinates(self):
        raw = _make_raw_evse()
        result = normalize_evse("LOC001", raw)
        assert result["latitude"] is None
        assert result["longitude"] is None

    @pytest.mark.unit
    def test_evse_with_capabilities(self):
        raw = _make_raw_evse(capabilities=["RFID_READER", "REMOTE_START_STOP_CAPABLE"])
        result = normalize_evse("LOC001", raw)
        assert result["capabilities"] == ["RFID_READER", "REMOTE_START_STOP_CAPABLE"]

    @pytest.mark.unit
    def test_evse_removed_status(self):
        raw = _make_raw_evse(status="REMOVED", evse_id=None)
        result = normalize_evse("LOC001", raw)
        assert result["status"] == "REMOVED"
        assert result["evse_id"] is None

    @pytest.mark.unit
    def test_evse_all_statuses(self):
        for status in ("AVAILABLE", "BLOCKED", "CHARGING", "INOPERATIVE",
                       "OUTOFORDER", "PLANNED", "REMOVED", "RESERVED", "UNKNOWN"):
            raw = _make_raw_evse(status=status)
            result = normalize_evse("LOC001", raw)
            assert result["status"] == status

    @pytest.mark.unit
    def test_evse_multiple_connectors(self):
        raw = _make_raw_evse(connectors=[
            _make_raw_connector(id="1", standard="IEC_62196_T2"),
            _make_raw_connector(id="2", standard="IEC_62196_T2_COMBO"),
        ])
        result = normalize_evse("LOC001", raw)
        assert len(result["connectors"]) == 2
        assert result["connectors"][0]["standard"] == "IEC_62196_T2"
        assert result["connectors"][1]["standard"] == "IEC_62196_T2_COMBO"


# ── Location normalization ───────────────────────────────────────────────────

class TestNormalizeLocation:
    @pytest.mark.unit
    def test_basic_location(self):
        raw = _make_raw_location()
        result = normalize_location(raw)
        assert result is not None
        assert result["location_id"] == "LOC001"
        assert result["country_code"] == "NL"
        assert result["party_id"] == "ABC"
        assert result["publish"] is True
        assert result["name"] == "Test Station"
        assert result["address"] == "Keizersgracht 100"
        assert result["city"] == "Amsterdam"
        assert result["postal_code"] == "1015AA"
        assert result["country"] == "NLD"
        assert result["latitude"] == pytest.approx(52.370216)
        assert result["longitude"] == pytest.approx(4.895168)
        assert result["time_zone"] == "Europe/Amsterdam"
        assert result["evse_count"] == 1
        assert result["connector_count"] == 1

    @pytest.mark.unit
    def test_missing_id_returns_none(self):
        raw = _make_raw_location()
        del raw["id"]
        assert normalize_location(raw) is None

    @pytest.mark.unit
    def test_missing_coordinates_returns_none(self):
        raw = _make_raw_location(coordinates={})
        assert normalize_location(raw) is None

    @pytest.mark.unit
    def test_location_with_operator(self):
        raw = _make_raw_location(operator={"name": "Allego", "website": "https://allego.eu"})
        result = normalize_location(raw)
        assert result["operator_name"] == "Allego"
        assert result["operator_website"] == "https://allego.eu"

    @pytest.mark.unit
    def test_location_with_parking_type(self):
        raw = _make_raw_location(parking_type="ON_STREET")
        result = normalize_location(raw)
        assert result["parking_type"] == "ON_STREET"

    @pytest.mark.unit
    def test_location_with_facilities(self):
        raw = _make_raw_location(facilities=["SUPERMARKET", "WIFI"])
        result = normalize_location(raw)
        assert result["facilities"] == ["SUPERMARKET", "WIFI"]

    @pytest.mark.unit
    def test_location_with_energy_mix(self):
        raw = _make_raw_location(energy_mix={"is_green_energy": True, "supplier_name": "GreenChoice"})
        result = normalize_location(raw)
        assert result["energy_mix_is_green_energy"] is True
        assert result["energy_mix_supplier_name"] == "GreenChoice"

    @pytest.mark.unit
    def test_location_with_opening_times(self):
        raw = _make_raw_location(opening_times={"twentyfourseven": True})
        result = normalize_location(raw)
        assert result["opening_times_twentyfourseven"] is True

    @pytest.mark.unit
    def test_location_evse_count(self):
        raw = _make_raw_location(evses=[
            _make_raw_evse(uid="E1"),
            _make_raw_evse(uid="E2", connectors=[_make_raw_connector(id="1"), _make_raw_connector(id="2")]),
        ])
        result = normalize_location(raw)
        assert result["evse_count"] == 2
        assert result["connector_count"] == 3

    @pytest.mark.unit
    def test_location_no_evses(self):
        raw = _make_raw_location(evses=[])
        result = normalize_location(raw)
        assert result["evse_count"] == 0
        assert result["connector_count"] == 0

    @pytest.mark.unit
    def test_location_null_optional_fields(self):
        raw = _make_raw_location()
        raw["name"] = None
        raw["postal_code"] = None
        raw["state"] = None
        result = normalize_location(raw)
        assert result["name"] is None
        assert result["postal_code"] is None
        assert result["state"] is None


# ── Tariff normalization ─────────────────────────────────────────────────────

class TestNormalizeTariff:
    @pytest.mark.unit
    def test_basic_tariff(self):
        raw = _make_raw_tariff()
        result = normalize_tariff(raw)
        assert result is not None
        assert result["tariff_id"] == "TAR001"
        assert result["country_code"] == "NL"
        assert result["party_id"] == "ABC"
        assert result["currency"] == "EUR"
        assert len(result["elements"]) == 1
        assert result["elements"][0]["price_components"][0]["type"] == "ENERGY"
        assert result["elements"][0]["price_components"][0]["price"] == 0.25

    @pytest.mark.unit
    def test_missing_id_returns_none(self):
        raw = _make_raw_tariff()
        del raw["id"]
        assert normalize_tariff(raw) is None

    @pytest.mark.unit
    def test_no_elements_returns_none(self):
        raw = _make_raw_tariff(elements=[])
        assert normalize_tariff(raw) is None

    @pytest.mark.unit
    def test_tariff_with_vat(self):
        raw = _make_raw_tariff(elements=[
            {"price_components": [{"type": "ENERGY", "price": 0.25, "vat": 21.0, "step_size": 1}]}
        ])
        result = normalize_tariff(raw)
        assert result["elements"][0]["price_components"][0]["vat"] == 21.0

    @pytest.mark.unit
    def test_tariff_with_parking_time(self):
        raw = _make_raw_tariff(elements=[
            {"price_components": [
                {"type": "ENERGY", "price": 0.25, "step_size": 1},
                {"type": "PARKING_TIME", "price": 2.0, "step_size": 900},
            ]}
        ])
        result = normalize_tariff(raw)
        pcs = result["elements"][0]["price_components"]
        assert len(pcs) == 2
        assert pcs[1]["type"] == "PARKING_TIME"
        assert pcs[1]["step_size"] == 900

    @pytest.mark.unit
    def test_tariff_with_restrictions(self):
        raw = _make_raw_tariff(elements=[
            {
                "price_components": [{"type": "ENERGY", "price": 0.25, "step_size": 1}],
                "restrictions": {
                    "day_of_week": ["MONDAY", "TUESDAY"],
                    "start_time": "08:00",
                    "end_time": "20:00",
                    "max_power": 22.0,
                },
            }
        ])
        result = normalize_tariff(raw)
        r = result["elements"][0]["restrictions"]
        assert r is not None
        assert r["day_of_week"] == ["MONDAY", "TUESDAY"]
        assert r["start_time"] == "08:00"
        assert r["end_time"] == "20:00"
        assert r["max_power"] == 22.0

    @pytest.mark.unit
    def test_tariff_with_alt_text(self):
        raw = _make_raw_tariff(tariff_alt_text=[{"language": "nl", "text": "€0,25 per kWh"}])
        result = normalize_tariff(raw)
        assert result["tariff_alt_text"] == "€0,25 per kWh"

    @pytest.mark.unit
    def test_tariff_with_type(self):
        raw = _make_raw_tariff(type="AD_HOC_PAYMENT")
        result = normalize_tariff(raw)
        assert result["tariff_type"] == "AD_HOC_PAYMENT"

    @pytest.mark.unit
    def test_tariff_with_price_limits(self):
        raw = _make_raw_tariff(
            min_price={"excl_vat": 1.0, "incl_vat": 1.21},
            max_price={"excl_vat": 50.0, "incl_vat": 60.5},
        )
        result = normalize_tariff(raw)
        assert result["min_price_excl_vat"] == 1.0
        assert result["min_price_incl_vat"] == 1.21
        assert result["max_price_excl_vat"] == 50.0
        assert result["max_price_incl_vat"] == 60.5

    @pytest.mark.unit
    def test_tariff_with_validity_period(self):
        raw = _make_raw_tariff(
            start_date_time="2024-01-01T00:00:00Z",
            end_date_time="2024-12-31T23:59:59Z",
        )
        result = normalize_tariff(raw)
        assert result["start_date_time"] == "2024-01-01T00:00:00Z"
        assert result["end_date_time"] == "2024-12-31T23:59:59Z"

    @pytest.mark.unit
    def test_tariff_all_dimension_types(self):
        for dim in ("ENERGY", "FLAT", "PARKING_TIME", "TIME"):
            raw = _make_raw_tariff(elements=[
                {"price_components": [{"type": dim, "price": 1.0, "step_size": 1}]}
            ])
            result = normalize_tariff(raw)
            assert result["elements"][0]["price_components"][0]["type"] == dim

    @pytest.mark.unit
    def test_tariff_with_reservation_restriction(self):
        raw = _make_raw_tariff(elements=[
            {
                "price_components": [{"type": "TIME", "price": 5.0, "step_size": 60}],
                "restrictions": {"reservation": "RESERVATION"},
            }
        ])
        result = normalize_tariff(raw)
        assert result["elements"][0]["restrictions"]["reservation"] == "RESERVATION"

    @pytest.mark.unit
    def test_tariff_multiple_elements(self):
        raw = _make_raw_tariff(elements=[
            {"price_components": [{"type": "FLAT", "price": 0.5, "step_size": 1}]},
            {"price_components": [{"type": "ENERGY", "price": 0.25, "step_size": 1}]},
            {
                "price_components": [{"type": "PARKING_TIME", "price": 2.0, "step_size": 900}],
                "restrictions": {"start_time": "18:00", "end_time": "08:00"},
            },
        ])
        result = normalize_tariff(raw)
        assert len(result["elements"]) == 3


# ── Connection string parsing ────────────────────────────────────────────────

class TestParseConnectionString:
    @pytest.mark.unit
    def test_event_hub_connection_string(self):
        cs = "Endpoint=sb://test.servicebus.windows.net/;SharedAccessKeyName=send;SharedAccessKey=abc123;EntityPath=my-topic"
        config = parse_connection_string(cs)
        assert "bootstrap.servers" in config
        assert config["bootstrap.servers"] == "test.servicebus.windows.net:9093"
        assert config["sasl.username"] == "$ConnectionString"
        assert config["security.protocol"] == "SASL_SSL"
        assert config["kafka_topic"] == "my-topic"

    @pytest.mark.unit
    def test_bootstrap_server_config(self):
        cs = "BootstrapServer=localhost:9092"
        config = parse_connection_string(cs)
        assert config["bootstrap.servers"] == "localhost:9092"


# ── Poller state and diffing ─────────────────────────────────────────────────

class TestPollerProcessLocations:
    @pytest.mark.unit
    def test_first_poll_emits_all(self):
        poller = NdlPoller()
        poller._first_poll = True
        raw_locations = [_make_raw_location()]
        stats = poller.process_locations(raw_locations)
        assert stats["locations"]["emitted"] == 1
        assert stats["evse"]["appeared"] == 1

    @pytest.mark.unit
    def test_second_poll_no_change(self):
        poller = NdlPoller()
        poller._first_poll = True
        raw_locations = [_make_raw_location()]
        poller.process_locations(raw_locations)
        # Second poll: same data, no changes
        poller._first_poll = False
        stats = poller.process_locations(raw_locations)
        assert stats["locations"]["emitted"] == 0
        assert stats["evse"]["unchanged"] == 1
        assert stats["evse"]["appeared"] == 0
        assert stats["evse"]["updated"] == 0

    @pytest.mark.unit
    def test_status_change_detected(self):
        poller = NdlPoller()
        poller._first_poll = True
        raw_locations = [_make_raw_location()]
        poller.process_locations(raw_locations)
        # Change EVSE status
        poller._first_poll = False
        raw_locations[0]["evses"][0]["status"] = "CHARGING"
        stats = poller.process_locations(raw_locations)
        assert stats["evse"]["updated"] == 1

    @pytest.mark.unit
    def test_new_evse_appears(self):
        poller = NdlPoller()
        poller._first_poll = True
        raw_locations = [_make_raw_location()]
        poller.process_locations(raw_locations)
        # Add a new EVSE
        poller._first_poll = False
        raw_locations[0]["evses"].append(_make_raw_evse(uid="EVSE002"))
        stats = poller.process_locations(raw_locations)
        assert stats["evse"]["appeared"] == 1
        assert stats["evse"]["unchanged"] == 1

    @pytest.mark.unit
    def test_evse_disappears(self):
        poller = NdlPoller()
        poller._first_poll = True
        raw_locations = [_make_raw_location(evses=[
            _make_raw_evse(uid="E1"),
            _make_raw_evse(uid="E2"),
        ])]
        poller.process_locations(raw_locations)
        # Remove one EVSE
        poller._first_poll = False
        raw_locations[0]["evses"] = [_make_raw_evse(uid="E1")]
        stats = poller.process_locations(raw_locations)
        assert stats["evse"]["resolved"] == 1

    @pytest.mark.unit
    def test_skips_invalid_locations(self):
        poller = NdlPoller()
        poller._first_poll = True
        stats = poller.process_locations([{"invalid": True}, None, "not a dict"])
        assert stats["locations"]["skipped"] == 1  # only the dict without id

    @pytest.mark.unit
    def test_multiple_locations(self):
        poller = NdlPoller()
        poller._first_poll = True
        raw_locations = [
            _make_raw_location(id="LOC1", evses=[_make_raw_evse(uid="E1")]),
            _make_raw_location(id="LOC2", evses=[
                _make_raw_evse(uid="E2"),
                _make_raw_evse(uid="E3"),
            ]),
        ]
        stats = poller.process_locations(raw_locations)
        assert stats["locations"]["emitted"] == 2
        assert stats["evse"]["appeared"] == 3

    @pytest.mark.unit
    def test_location_reference_not_emitted_second_poll(self):
        poller = NdlPoller()
        poller._first_poll = True
        raw_locations = [_make_raw_location()]
        poller.process_locations(raw_locations)
        poller._first_poll = False
        stats = poller.process_locations(raw_locations)
        assert stats["locations"]["emitted"] == 0


class TestPollerProcessTariffs:
    @pytest.mark.unit
    def test_first_poll_emits_tariffs(self):
        poller = NdlPoller()
        poller._first_poll = True
        raw_tariffs = [_make_raw_tariff()]
        stats = poller.process_tariffs(raw_tariffs)
        assert stats["emitted"] == 1

    @pytest.mark.unit
    def test_second_poll_skips_tariffs(self):
        poller = NdlPoller()
        poller._first_poll = False
        raw_tariffs = [_make_raw_tariff()]
        stats = poller.process_tariffs(raw_tariffs)
        assert stats["emitted"] == 0

    @pytest.mark.unit
    def test_skips_invalid_tariffs(self):
        poller = NdlPoller()
        poller._first_poll = True
        stats = poller.process_tariffs([{"no_id": True}, _make_raw_tariff(elements=[])])
        assert stats["skipped"] == 2
        assert stats["emitted"] == 0

    @pytest.mark.unit
    def test_multiple_tariffs(self):
        poller = NdlPoller()
        poller._first_poll = True
        raw_tariffs = [
            _make_raw_tariff(id="T1"),
            _make_raw_tariff(id="T2"),
            _make_raw_tariff(id="T3"),
        ]
        stats = poller.process_tariffs(raw_tariffs)
        assert stats["emitted"] == 3


# ── State persistence ────────────────────────────────────────────────────────

class TestPollerState:
    @pytest.mark.unit
    def test_save_and_load_state(self, tmp_path):
        state_file = str(tmp_path / "state.json")
        poller = NdlPoller(state_file=state_file)
        poller.evse_state = {"LOC1/E1": "AVAILABLE", "LOC1/E2": "CHARGING"}
        poller.save_state()

        poller2 = NdlPoller(state_file=state_file)
        poller2.load_state()
        assert poller2.evse_state == {"LOC1/E1": "AVAILABLE", "LOC1/E2": "CHARGING"}
        assert poller2._first_poll is False

    @pytest.mark.unit
    def test_load_missing_state(self, tmp_path):
        state_file = str(tmp_path / "nonexistent.json")
        poller = NdlPoller(state_file=state_file)
        poller.load_state()
        assert poller.evse_state == {}
        assert poller._first_poll is True

    @pytest.mark.unit
    def test_load_corrupted_state(self, tmp_path):
        state_file = tmp_path / "state.json"
        state_file.write_text("not valid json")
        poller = NdlPoller(state_file=str(state_file))
        poller.load_state()
        assert poller.evse_state == {}


# ── Edge cases ───────────────────────────────────────────────────────────────

class TestEdgeCases:
    @pytest.mark.unit
    def test_location_with_null_coordinates_value(self):
        raw = _make_raw_location(coordinates={"latitude": None, "longitude": None})
        assert normalize_location(raw) is None

    @pytest.mark.unit
    def test_evse_with_non_dict_connectors(self):
        raw = _make_raw_evse(connectors=["not a dict"])
        assert normalize_evse("LOC1", raw) is None

    @pytest.mark.unit
    def test_tariff_with_non_dict_elements(self):
        raw = _make_raw_tariff(elements=["not a dict"])
        assert normalize_tariff(raw) is None

    @pytest.mark.unit
    def test_tariff_with_empty_price_components(self):
        raw = _make_raw_tariff(elements=[{"price_components": []}])
        assert normalize_tariff(raw) is None

    @pytest.mark.unit
    def test_location_string_coordinates(self):
        raw = _make_raw_location(coordinates={"latitude": "52.370", "longitude": "4.895"})
        result = normalize_location(raw)
        assert result["latitude"] == pytest.approx(52.370)
        assert result["longitude"] == pytest.approx(4.895)

    @pytest.mark.unit
    def test_connector_missing_optional_fields(self):
        raw = {"id": "1", "standard": "CHADEMO", "format": "CABLE", "power_type": "DC", "max_voltage": 500, "max_amperage": 200}
        result = normalize_connector(raw)
        assert result["max_electric_power"] is None
        assert result["tariff_ids"] is None

    @pytest.mark.unit
    def test_tariff_restrictions_all_none(self):
        raw = _make_raw_tariff(elements=[
            {"price_components": [{"type": "FLAT", "price": 0, "step_size": 1}], "restrictions": {}}
        ])
        result = normalize_tariff(raw)
        r = result["elements"][0]["restrictions"]
        assert all(v is None for v in r.values())
