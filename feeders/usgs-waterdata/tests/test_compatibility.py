from copy import deepcopy

import pytest

from usgs_waterdata_core.capture import crosswalk_candidates, parse_rdb
from usgs_waterdata_core.compat import CompatibilityError, Enrollment, qualifiers


def document():
    return {
        "version": 1,
        "legacy_rdb_identities": ["USGS/01646500/00010/252060"],
        "legacy_sites": {
            "USGS-01646500": {
                "captured_at": "2026-11-16T12:00:00Z",
                "fields": {"site_no": "01646500", "station_nm": "Potomac", "map_nm": "Historical map"},
            }
        },
        "series": {
            "opaque-id": {
                "status": "verified",
                "verified_by": "fixture",
                "verified_at": "2026-11-16T12:00:00Z",
                "agency_cd": "USGS",
                "site_no": "01646500",
                "parameter_cd": "00010",
                "timeseries_cd": "252060",
                "unit": "deg C",
                "upstream_units": ["degC"],
                "parameter_name": "Temperature, water, degrees Celsius",
                "qualifier_codes": {"Estimated": "e"},
            }
        },
    }


def properties():
    return {
        "monitoring_location_id": "USGS-01646500",
        "time_series_id": "opaque-id",
        "parameter_code": "00010",
        "time": "2026-11-16T07:50:00-05:00",
        "unit_of_measure": "degC",
        "value": "9.6",
        "approval_status": "Provisional",
        "qualifier": None,
    }


def test_preserves_legacy_identity_leading_zeros_and_unit_without_rescaling():
    enrollment = Enrollment(document())
    row = enrollment.iv_record(properties())
    assert row["site_no"] == "01646500"
    assert row["252060_00010"] == "9.6"
    assert row["252060_00010_cd"] == "P"
    reading = enrollment.wq_reading(properties())
    assert reading["unit"] == "deg C"
    assert reading["value"] == 9.6
    assert reading["date_time"] == "2026-11-16T12:50:00+00:00"


def test_unverified_mapping_and_unknown_series_cannot_emit():
    data = document()
    data["series"]["opaque-id"]["status"] = "candidate"
    with pytest.raises(CompatibilityError, match="not enrolled"):
        Enrollment(data).iv_record(properties())
    with pytest.raises(CompatibilityError, match="not enrolled"):
        Enrollment(document()).iv_record({**properties(), "time_series_id": "new-series"})


def test_identity_and_units_are_validated_not_silently_reinterpreted():
    enrollment = Enrollment(document())
    with pytest.raises(CompatibilityError, match="identity"):
        enrollment.iv_record({**properties(), "parameter_code": "00060"})
    with pytest.raises(CompatibilityError, match="unit"):
        enrollment.iv_record({**properties(), "unit_of_measure": "degF"})


def test_duplicate_legacy_id_mapping_is_rejected():
    data = document()
    data["series"]["second-id"] = deepcopy(data["series"]["opaque-id"])
    with pytest.raises(CompatibilityError, match="Multiple"):
        Enrollment(data)


def test_numeric_id_cannot_be_invented_when_marking_a_mapping_verified():
    data = document()
    data["series"]["opaque-id"]["timeseries_cd"] = "999999"
    with pytest.raises(CompatibilityError, match="not captured"):
        Enrollment(data)


def test_historical_site_is_not_mutated_or_filled_with_invented_values():
    enrollment = Enrollment(document())
    first = enrollment.site("USGS-01646500")
    first["map_nm"] = "modified"
    assert enrollment.site("USGS-01646500")["map_nm"] == "Historical map"
    with pytest.raises(CompatibilityError, match="snapshot"):
        enrollment.site("USGS-99999999")


def test_approval_and_other_qualifiers_are_separate():
    assert qualifiers({**properties(), "qualifier": "Estimated"}, {"Estimated": "e"}) == ["P", "e"]
    with pytest.raises(CompatibilityError, match="translation"):
        qualifiers({**properties(), "qualifier": "new-code"}, {})


@pytest.mark.parametrize("value", ["NaN", "Infinity", "-999999", "Ice", "1e999"])
def test_does_not_publish_exceptional_wq_values_as_measurements(value):
    with pytest.raises(CompatibilityError):
        Enrollment(document()).wq_reading({**properties(), "value": value})


def test_rdb_parser_preserves_trailing_empty_columns():
    rows = parse_rdb("# comment\nagency_cd\tsite_no\tmap_nm\n5s\t15s\t20s\nUSGS\t01646500\t\n")
    assert rows == [{"agency_cd": "USGS", "site_no": "01646500", "map_nm": ""}]


def test_value_matches_generate_candidates_not_approved_crosswalks():
    values = [
        {"dateTime": f"2026-11-16T12:{minute}:00Z", "value": str(value)}
        for minute, value in [("00", 1), ("15", 2), ("30", 3)]
    ]
    legacy = {
        "value": {
            "timeSeries": [
                {
                    "sourceInfo": {"siteCode": [{"agencyCode": "USGS", "value": "01646500"}]},
                    "variable": {
                        "variableCode": [{"value": "00010"}],
                        "unit": {"unitCode": "deg C"},
                    },
                    "values": [{"value": values, "method": [{"methodID": 252060}]}],
                }
            ]
        }
    }
    features = [
        {"properties": {**properties(), "time": row["dateTime"], "value": row["value"]}}
        for row in values
    ]
    candidates = crosswalk_candidates(legacy, features)
    assert len(candidates) == 1
    assert candidates[0]["status"] == "candidate"
    assert candidates[0]["candidate_method_id"] == "252060"
    assert "timeseries_cd" not in candidates[0]
