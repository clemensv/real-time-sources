"""Explicit legacy enrollment without invented identities or metadata."""

from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy
from decimal import Decimal, InvalidOperation
import json
import logging
import math
from pathlib import Path
from typing import Any

from .client import utc_datetime

logger = logging.getLogger(__name__)
LEGACY_SOURCE = "https://waterservices.usgs.gov/nwis/iv/"


class CompatibilityError(ValueError):
    """An observation cannot be represented by its enrolled legacy contract."""


def qualifiers(properties: Mapping[str, Any], translations: Mapping[str, str]) -> list[str]:
    approval = properties.get("approval_status")
    if approval not in ("Approved", "Provisional"):
        raise CompatibilityError(f"Unknown approval status: {approval!r}")
    result = ["A" if approval == "Approved" else "P"]
    qualifier = properties.get("qualifier")
    if qualifier is not None:
        if not isinstance(qualifier, str) or qualifier not in translations:
            raise CompatibilityError(f"No reviewed legacy qualifier translation: {qualifier!r}")
        mapped = translations[qualifier]
        if mapped and mapped not in result:
            result.append(mapped)
    return result


class Enrollment:
    def __init__(self, document: dict[str, Any]) -> None:
        if document.get("version") != 1:
            raise CompatibilityError("Unsupported compatibility enrollment version")
        self.document = deepcopy(document)
        self.sites = self.document.get("legacy_sites")
        self.mappings = self.document.get("series")
        captured_identities = self.document.get("legacy_rdb_identities", [])
        if not isinstance(self.sites, dict) or not isinstance(self.mappings, dict):
            raise CompatibilityError("Enrollment requires legacy_sites and series objects")
        if not isinstance(captured_identities, list):
            raise CompatibilityError("Enrollment requires an array of captured legacy RDB identities")
        reverse: set[tuple[str, str, str]] = set()
        for series_id, entry in self.mappings.items():
            if not isinstance(series_id, str) or not isinstance(entry, dict):
                raise CompatibilityError("Invalid series mapping")
            if entry.get("status") != "verified":
                continue
            required = (
                "agency_cd", "site_no", "parameter_cd", "timeseries_cd",
                "unit", "parameter_name", "verified_by", "verified_at",
            )
            if any(not isinstance(entry.get(key), str) or not entry[key] for key in required):
                raise CompatibilityError(f"Incomplete verified series mapping: {series_id}")
            if not entry["timeseries_cd"].isdigit() or len(entry["parameter_cd"]) != 5:
                raise CompatibilityError(f"Invalid legacy identity: {series_id}")
            utc_datetime(entry["verified_at"])
            location_id = f"{entry['agency_cd']}-{entry['site_no']}"
            if location_id not in self.sites:
                raise CompatibilityError(f"Missing legacy site snapshot: {location_id}")
            key = (location_id, entry["parameter_cd"], entry["timeseries_cd"])
            identity = "/".join(
                entry[field] for field in ("agency_cd", "site_no", "parameter_cd", "timeseries_cd")
            )
            if identity not in captured_identities:
                raise CompatibilityError(f"Legacy identity was not captured from RDB: {identity}")
            if key in reverse:
                raise CompatibilityError(f"Multiple OGC series map to legacy identity: {key}")
            reverse.add(key)

    @classmethod
    def load(cls, path: Path) -> Enrollment:
        document = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(document, dict):
            raise CompatibilityError("Enrollment must be a JSON object")
        return cls(document)

    def mapping(self, properties: Mapping[str, Any]) -> dict[str, Any]:
        series_id = properties.get("time_series_id")
        entry = self.mappings.get(series_id)
        if not isinstance(entry, dict) or entry.get("status") != "verified":
            raise CompatibilityError(f"Series is not enrolled: {series_id!r}")
        expected = f"{entry['agency_cd']}-{entry['site_no']}"
        if (
            properties.get("monitoring_location_id") != expected
            or properties.get("parameter_code") != entry["parameter_cd"]
        ):
            raise CompatibilityError(f"Observation disagrees with enrolled identity: {series_id}")
        upstream_unit = properties.get("unit_of_measure")
        accepted = entry.get("upstream_units", [entry["unit"]])
        if not isinstance(accepted, list) or upstream_unit not in accepted:
            raise CompatibilityError(f"Unreviewed unit for {series_id}: {upstream_unit!r}")
        return entry

    def site(self, location_id: str) -> dict[str, Any]:
        snapshot = self.sites.get(location_id)
        if not isinstance(snapshot, dict) or not isinstance(snapshot.get("fields"), dict):
            raise CompatibilityError(f"No legacy metadata snapshot: {location_id}")
        if not snapshot.get("captured_at"):
            raise CompatibilityError(f"Snapshot lacks provenance: {location_id}")
        logger.info("Using historical USGS site metadata %s captured %s", location_id, snapshot["captured_at"])
        return deepcopy(snapshot["fields"])

    def iv_record(self, properties: Mapping[str, Any]) -> dict[str, str]:
        entry = self.mapping(properties)
        value = properties.get("value")
        if not isinstance(value, str):
            raise CompatibilityError("Legacy IV projection requires a documented string value")
        column = f"{entry['timeseries_cd']}_{entry['parameter_cd']}"
        return {
            "agency_cd": entry["agency_cd"],
            "site_no": entry["site_no"],
            "datetime": utc_datetime(properties["time"]).isoformat(),
            "tz_cd": "UTC",
            column: value,
            f"{column}_cd": ",".join(qualifiers(properties, entry.get("qualifier_codes", {}))),
        }

    def wq_reading(self, properties: Mapping[str, Any]) -> dict[str, Any]:
        entry = self.mapping(properties)
        site = self.site(f"{entry['agency_cd']}-{entry['site_no']}")
        raw = properties.get("value")
        if not isinstance(raw, str):
            raise CompatibilityError("Legacy WQ projection requires a numeric string value")
        try:
            number = Decimal(raw)
        except InvalidOperation as exc:
            raise CompatibilityError(f"Non-numeric WQ value needs a reviewed policy: {raw!r}") from exc
        if not number.is_finite() or number == Decimal("-999999"):
            raise CompatibilityError(f"WQ value is not a finite measurement: {raw!r}")
        value = float(number)
        if not math.isfinite(value):
            raise CompatibilityError(f"WQ value exceeds double precision range: {raw!r}")
        return {
            "site_number": entry["site_no"],
            "site_name": site["station_nm"],
            "parameter_code": entry["parameter_cd"],
            "parameter_name": entry["parameter_name"],
            "value": value,
            "unit": entry["unit"],
            "qualifier": qualifiers(properties, entry.get("qualifier_codes", {}))[0],
            "date_time": utc_datetime(properties["time"]).isoformat(),
            "state": None,
        }
