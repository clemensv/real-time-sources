"""Invented observations and WaterML structure, unrelated to a live station."""

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


def waterml():
    return {"value": {"timeSeries": [{
        "sourceInfo": {
            "siteName": "SYNTHETIC TEST CHANNEL",
            "siteCode": [{"value": "99000001", "agencyCode": "USGS"}],
            "geoLocation": {"geogLocation": {"latitude": 0.125, "longitude": -0.25}},
            "siteProperty": [{"name": "siteTypeCd", "value": "ST"}, {"name": "stateCd", "value": "24"}],
        },
        "variable": {
            "variableCode": [{"value": "00010"}],
            "variableDescription": "Temperature, water, degrees Celsius",
            "unit": {"unitCode": "deg C"},
        },
        "values": [{"value": [
            {"value": feature["properties"]["value"], "dateTime": feature["properties"]["time"], "qualifiers": ["P"]}
            for feature in observations() if feature["properties"]["parameter_code"] == "00010"
        ]}],
    }]}}
