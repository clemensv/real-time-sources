"""Refresh the public, bounded upstream evidence used to author the native contract."""

import json
from datetime import datetime, timezone
from pathlib import Path

import requests


def main():
    root = Path(__file__).parent / "tests" / "fixtures"
    root.mkdir(exist_ok=True)
    base = "https://api.waterdata.usgs.gov/ogcapi/v1/collections"
    evidence = {"retrieved_at": datetime.now(timezone.utc).isoformat(), "collections": {}}
    for collection in ("continuous", "monitoring-locations", "time-series-metadata", "parameter-codes"):
        url = f"{base}/{collection}"
        response = requests.get(f"{url}/schema", params={"f": "json"}, timeout=60)
        response.raise_for_status()
        schema = response.json()
        params = {"f": "json", "limit": 10}
        if collection in ("continuous", "time-series-metadata"):
            params.update(monitoring_location_id="USGS-01646500", parameter_code="00010,00060")
        if collection == "continuous":
            params["time"] = "PT2H"
        elif collection == "monitoring-locations":
            params["id"] = "USGS-01646500"
        elif collection == "parameter-codes":
            params["id"] = "00060"
        response = requests.get(f"{url}/items", params=params, timeout=60)
        response.raise_for_status()
        evidence["collections"][collection] = {
            "schema_url": f"{url}/schema?f=json",
            "schema": schema,
            "sample_url": response.url,
            "features": response.json()["features"],
        }
    response = requests.get(
        f"{base}/time-series-metadata/items",
        params={"f": "json", "limit": 10000, "computation_identifier": "Instantaneous",
                "computation_period_identifier": "Points"},
        timeout=120,
    )
    response.raise_for_status()
    rows = response.json()["features"]
    thresholds = [t for row in rows for t in row["properties"].get("thresholds", [])]
    evidence["thresholds"] = {
        "url": response.url,
        "inspected_series": len(rows),
        "fields": sorted({key for t in thresholds for key in t}),
        "period_fields": sorted({key for t in thresholds for p in t.get("Periods", []) for key in p}),
        "samples": [row for row in rows if row["properties"].get("thresholds")][:2],
    }
    (root / "contract-evidence.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(evidence["thresholds"]["fields"], evidence["thresholds"]["period_fields"])


if __name__ == "__main__":
    main()
