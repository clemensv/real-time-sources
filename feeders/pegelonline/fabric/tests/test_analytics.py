"""Analytics bindings accept discovered typed schemas, never guessed table names."""

import importlib.util
import json
import sys
from pathlib import Path

import pytest

FABRIC = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("render_analytics", FABRIC / "render_analytics.py")
assert SPEC and SPEC.loader
analytics = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(analytics)


def schema(name, columns, timestamp_type="string"):
    return {"Name": name, "OrderedColumns": [
        {"Name": column, "CslType": timestamp_type if column in ("timestamp", "___time")
         else sorted(types)[0]} for column, types in columns.items()
    ]}


@pytest.mark.parametrize("timestamp_type", ["datetime", "string"])
def test_analytics_bind_discovered_tables_without_ingestion_commands(timestamp_type):
    stations = schema('Synthetic "station" table', analytics.STATION_COLUMNS, timestamp_type)
    measurements = schema("Synthetic measurements", analytics.MEASUREMENT_COLUMNS, timestamp_type)
    text = analytics.render(stations, measurements)
    assert f'table({json.dumps(stations["Name"])})' in text
    assert f'table({json.dumps(measurements["Name"])})' in text
    assert "timestamp=todatetime(timestamp)" in text
    commands = [line for line in text.splitlines() if line.startswith(".")]
    assert commands and all(line.startswith(".create-or-alter function ") for line in commands)
    assert "_cloudevents_dispatch" not in text


@pytest.mark.parametrize("failure", ["missing", "wrong-type", "same-table", "empty-name"])
def test_analytics_reject_unqualified_table_bindings(failure):
    stations = schema("Synthetic stations", analytics.STATION_COLUMNS)
    measurements = schema("Synthetic measurements", analytics.MEASUREMENT_COLUMNS)
    if failure == "missing":
        measurements["OrderedColumns"].pop(0)
    elif failure == "wrong-type":
        next(column for column in measurements["OrderedColumns"]
             if column["Name"] == "value")["CslType"] = "string"
    elif failure == "same-table":
        measurements["Name"] = stations["Name"]
    else:
        stations["Name"] = ""
    with pytest.raises(ValueError):
        analytics.render(stations, measurements)


def test_analytics_accept_windows_powershell_schema_bom(monkeypatch, tmp_path):
    stations = tmp_path / "station.json"
    measurements = tmp_path / "measurement.json"
    output = tmp_path / "analytics.kql"
    stations.write_text(json.dumps(schema("Synthetic stations", analytics.STATION_COLUMNS)),
                        encoding="utf-8-sig")
    measurements.write_text(json.dumps(schema("Synthetic measurements", analytics.MEASUREMENT_COLUMNS)),
                            encoding="utf-8-sig")
    monkeypatch.setattr(sys, "argv", [
        "render_analytics", "--station-schema", str(stations),
        "--measurement-schema", str(measurements), "--output", str(output),
    ])
    analytics.main()
    assert 'table("Synthetic stations")' in output.read_text(encoding="utf-8")
