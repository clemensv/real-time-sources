"""Capture legacy evidence before WaterServices is retired."""

from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import html
import logging
from pathlib import Path
import re
from typing import Any

from .client import WaterDataClient, time_interval, utc_datetime
from .state import write_json

logger = logging.getLogger(__name__)
LEGACY_BASE = "https://waterservices.usgs.gov/nwis"


def parse_rdb(text: str) -> list[dict[str, str]]:
    lines = [line for line in text.splitlines() if line and not line.startswith("#")]
    if not lines:
        raise ValueError("USGS site response contains no RDB table")
    headers = lines[0].split("\t")
    if "site_no" not in headers or len(lines) < 2:
        raise ValueError("USGS site response lacks an RDB header/type row")
    rows = []
    for line in lines[2:]:
        fields = line.split("\t")
        if len(fields) != len(headers):
            raise ValueError("USGS site RDB row has the wrong number of columns")
        rows.append(dict(zip(headers, fields)))
    return rows


def _points(values: list[dict[str, Any]]) -> dict[str, Decimal]:
    result: dict[str, Decimal] = {}
    for row in values:
        instant = row.get("dateTime", row.get("time"))
        raw = row.get("value")
        if not isinstance(instant, str) or not isinstance(raw, str):
            continue
        try:
            number = Decimal(raw)
        except InvalidOperation:
            continue
        if number.is_finite() and number != Decimal("-999999"):
            timestamp = utc_datetime(instant).isoformat()
            if timestamp in result and result[timestamp] != number:
                raise ValueError("Conflicting USGS values at one instant; cannot infer crosswalk")
            result[timestamp] = number
    return result


def crosswalk_candidates(
    legacy: dict[str, Any], features: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for feature in features:
        properties = feature["properties"]
        groups[(properties["monitoring_location_id"], properties["parameter_code"])].append(properties)
    candidates = []
    for timeseries in legacy.get("value", {}).get("timeSeries", []):
        source = timeseries["sourceInfo"]["siteCode"][0]
        location_id = f"{source['agencyCode']}-{source['value']}"
        variable = timeseries["variable"]
        parameter_code = variable["variableCode"][0]["value"]
        native_rows = groups.get((location_id, parameter_code), [])
        by_series: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for properties in native_rows:
            by_series[properties["time_series_id"]].append(properties)
        for values in timeseries.get("values", []):
            legacy_points = _points(values.get("value", []))
            methods = values.get("method", [])
            if not legacy_points or len(methods) != 1:
                continue
            for series_id, observations in by_series.items():
                new_points = _points(observations)
                common = sorted(legacy_points.keys() & new_points.keys())
                matches = [instant for instant in common if legacy_points[instant] == new_points[instant]]
                if len(matches) < 3 or len(matches) != len(common):
                    continue
                candidates.append(
                    {
                        "time_series_id": series_id,
                        "agency_cd": source["agencyCode"],
                        "site_no": source["value"],
                        "parameter_cd": parameter_code,
                        "candidate_method_id": str(methods[0]["methodID"]),
                        "method_description": methods[0].get("methodDescription"),
                        "matching_points": len(matches),
                        "distinct_values": len({legacy_points[instant] for instant in matches}),
                        "first_match": matches[0],
                        "last_match": matches[-1],
                        "unit": variable["unit"]["unitCode"],
                        "upstream_units": sorted({row["unit_of_measure"] for row in observations}),
                        "parameter_name": html.unescape(variable.get("variableDescription", "")),
                        "status": "candidate",
                    }
                )
    return candidates


def capture(
    client: WaterDataClient,
    *,
    sites: list[str],
    parameters: str,
    start: datetime,
    end: datetime,
) -> dict[str, Any]:
    if not sites or any(not re.fullmatch(r"\d{8,15}", site) for site in sites):
        raise ValueError("Capture requires explicit 8-15 digit USGS site numbers")
    time_interval(start, end)
    captured_at = datetime.now(timezone.utc).isoformat()
    sites_query = ",".join(sites)
    with client.session.get(
        f"{LEGACY_BASE}/site/",
        params={"format": "rdb", "sites": sites_query, "siteOutput": "expanded"},
        timeout=120,
        allow_redirects=False,
        headers={"X-Api-Key": None},
    ) as response:
        if 300 <= response.status_code < 400:
            raise RuntimeError("Legacy site capture redirected")
        response.raise_for_status()
        site_text = response.text
    with client.session.get(
        f"{LEGACY_BASE}/iv/",
        params={
            "format": "json",
            "sites": sites_query,
            "parameterCd": parameters,
            "startDT": start.isoformat(),
            "endDT": end.isoformat(),
        },
        timeout=120,
        allow_redirects=False,
        headers={"X-Api-Key": None},
    ) as response:
        if 300 <= response.status_code < 400:
            raise RuntimeError("Legacy IV capture redirected")
        response.raise_for_status()
        waterml = response.json()
    with client.session.get(
        f"{LEGACY_BASE}/iv/",
        params={
            "format": "rdb",
            "sites": sites_query,
            "parameterCd": parameters,
            "startDT": start.isoformat(),
            "endDT": end.isoformat(),
        },
        timeout=120,
        allow_redirects=False,
        headers={"X-Api-Key": None},
    ) as response:
        if 300 <= response.status_code < 400:
            raise RuntimeError("Legacy RDB observation capture redirected")
        response.raise_for_status()
        iv_text = response.text
    iv_rows = parse_rdb(iv_text)
    identities = {
        f"{row['agency_cd']}/{row['site_no']}/{match[2]}/{match[1]}"
        for row in iv_rows
        for column in row
        if (match := re.fullmatch(r"(\d+)_(\d{5})", column)) is not None
    }
    legacy_sites = {
        f"{row['agency_cd']}-{row['site_no']}": {
            "captured_at": captured_at,
            "source": f"{LEGACY_BASE}/site/",
            "fields": row,
        }
        for row in parse_rdb(site_text)
    }
    if set(legacy_sites) != {f"USGS-{site}" for site in sites}:
        raise ValueError("Legacy site capture did not return every requested USGS site")
    features = list(
        client.observations(
            start,
            end,
            location_ids=",".join(f"USGS-{site}" for site in sites),
            parameter_codes=parameters,
        )
    )
    metadata = list(
        client.features(
            "time-series-metadata",
            monitoring_location_id=",".join(legacy_sites),
            parameter_code=parameters,
            computation_identifier="Instantaneous",
        )
    )
    return {
        "version": 1,
        "captured_at": captured_at,
        "query": {"sites": sites, "parameter_codes": parameters, "interval": time_interval(start, end)},
        "legacy_sites": legacy_sites,
        "series": {},
        "candidates": crosswalk_candidates(waterml, features),
        "legacy_rdb_identities": sorted(identities),
        "evidence": {
            "legacy_site_rdb": site_text,
            "legacy_waterml": waterml,
            "legacy_iv_rdb": iv_text,
            "continuous": features,
            "time_series_metadata": metadata,
        },
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sites", required=True, help="Comma-separated USGS site numbers")
    parser.add_argument("--parameter-codes", required=True)
    parser.add_argument("--start", required=True, type=utc_datetime)
    parser.add_argument("--end", required=True, type=utc_datetime)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    if args.output.exists():
        parser.error("Output already exists; choose a new evidence filename")
    if not all(re.fullmatch(r"\d{5}", code) for code in args.parameter_codes.split(",")):
        parser.error("Parameter codes must be comma-separated five-digit codes")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    with WaterDataClient() as client:
        document = capture(
            client,
            sites=args.sites.split(","),
            parameters=args.parameter_codes,
            start=args.start,
            end=args.end,
        )
    write_json(args.output, document)
    logger.info(
        "Captured %d sites, %d observations and %d unverified candidates; no mappings auto-approved",
        len(document["legacy_sites"]),
        len(document["evidence"]["continuous"]),
        len(document["candidates"]),
    )


if __name__ == "__main__":
    main()
