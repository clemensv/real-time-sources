"""Invented observations; never an upstream capture or live enrollment."""

from datetime import datetime, timedelta, timezone


def observations():
    start = datetime(2026, 11, 16, 13, 30, tzinfo=timezone.utc)
    return [
        {
            "type": "Feature", "id": f"synthetic-{parameter}-{index}", "geometry": None,
            "properties": {
                "monitoring_location_id": "USGS-99000001", "parameter_code": parameter,
                "time_series_id": series, "unit_of_measure": unit,
                "time": (start + timedelta(minutes=5 * index)).isoformat(),
                "last_modified": "2026-11-16T15:00:00+00:00",
                "value": str(base + index / 8), "approval_status": "Provisional",
                "qualifier": None,
            },
        }
        for parameter, series, unit, base in (
            ("00010", "synthetic-temperature", "degC", 2),
            ("00060", "synthetic-discharge", "ft^3/s", 40),
        )
        for index in range(17)
    ]
