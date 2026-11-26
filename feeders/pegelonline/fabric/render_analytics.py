"""Bind analytics to table schemas read back from the target KQL database."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

STATION_COLUMNS = {
    "station_id": {"string"}, "shortname": {"string"}, "longname": {"string"},
    "agency": {"string"}, "latitude": {"real"}, "longitude": {"real"},
    "water": {"dynamic"}, "___time": {"datetime", "string"},
}
MEASUREMENT_COLUMNS = {
    "station_id": {"string"}, "value": {"real"}, "timestamp": {"datetime", "string"},
    "stateMnwMhw": {"string"}, "stateNswHsw": {"string"}, "___time": {"datetime", "string"},
}


def table_name(schema: dict[str, Any], expected: dict[str, set[str]]) -> str:
    name = schema["Name"]
    if not isinstance(name, str) or not name.strip() or any(ord(char) < 32 for char in name):
        raise ValueError("Expected a nonempty table name from the service schema")
    columns = {column["Name"]: column["CslType"] for column in schema["OrderedColumns"]}
    for column, types in expected.items():
        if columns.get(column) not in types:
            raise ValueError(f"Table {name!r} column {column!r} must have one of {sorted(types)}")
    return json.dumps(name, ensure_ascii=True)


def render(station_schema: dict[str, Any], measurement_schema: dict[str, Any]) -> str:
    stations = table_name(station_schema, STATION_COLUMNS)
    measurements = table_name(measurement_schema, MEASUREMENT_COLUMNS)
    if station_schema["Name"] == measurement_schema["Name"]:
        raise ValueError("Station and measurement families require distinct typed tables")
    adapters = (
        '.create-or-alter function with (folder="Pegelonline analytics") PegelStations() {\n'
        f"    table({stations})\n"
        "    | project station_id, shortname, longname, agency, latitude, longitude, water,\n"
        "              station_event_time=todatetime(___time)\n"
        "}\n\n"
        '.create-or-alter function with (folder="Pegelonline analytics") PegelMeasurements() {\n'
        f"    table({measurements})\n"
        "    | project station_id, value, timestamp=todatetime(timestamp), stateMnwMhw, stateNswHsw,\n"
        "              measurement_event_time=todatetime(___time)\n"
        "}\n\n"
    )
    return adapters + Path(__file__).with_name("analytics.kql").read_text(encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--station-schema", type=Path, required=True)
    parser.add_argument("--measurement-schema", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[3]
    output = args.output.resolve()
    if output.is_relative_to(root) or output in {
        args.station_schema.resolve(), args.measurement_schema.resolve(),
    }:
        parser.error("Write bound analytics outside the checkout, distinct from both inputs")
    try:
        text = render(
            json.loads(args.station_schema.read_text(encoding="utf-8-sig")),
            json.loads(args.measurement_schema.read_text(encoding="utf-8-sig")),
        )
        output.write_text(text, encoding="utf-8")
    except (ValueError, KeyError, TypeError, OSError) as error:
        parser.exit(1, f"Analytics binding failed: {error}\n")


if __name__ == "__main__":
    main()
