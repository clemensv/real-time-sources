# USGS Geomagnetism Program

## Source Identity

| Field            | Value |
|------------------|-------|
| **Full Name**    | USGS Geomagnetism Program |
| **Operator**     | United States Geological Survey |
| **URL**          | https://geomag.usgs.gov/ |
| **API Base**     | `https://geomag.usgs.gov/ws/` |
| **OpenAPI Spec** | `https://geomag.usgs.gov/ws/openapi.json` |
| **Coverage**     | Global (14 USGS-operated magnetic observatories) |
| **Update Freq.** | 1-second to 1-minute cadence; real-time |

## What It Does

The USGS Geomagnetism Program operates a network of 14 magnetic observatories across the United States and US territories (Boulder, Barrow, College, Deadhorse, Fresno, Guam, Honolulu, Newport, San Juan, Sitka, Stennis, Tucson, plus test stations). These observatories continuously measure Earth's magnetic field — the same field that protects us from solar wind, guides compass needles, and occasionally delivers stunning aurora displays.

The data API is modern, well-documented (Swagger UI), and provides access to real-time and historical magnetic field variations. It serves INTERMAGNET-format data through a clean REST interface — making it effectively a premium INTERMAGNET node with a much better developer experience.

## Endpoints Verified

| Endpoint | Status | Notes |
|----------|--------|-------|
| `/ws/data/?id=BOU&type=variation&elements=H&sampling_period=60&format=json` | ✅ 200 | 1-minute variation data, JSON |
| `/ws/observatories/` | ✅ 200 | GeoJSON FeatureCollection of all observatories |
| `/ws/openapi.json` | ✅ Documented | Full OpenAPI/Swagger specification |
| `/ws/data/?format=iaga2002` | ✅ 200 | IAGA-2002 text format (industry standard) |

### Sample Response — Observatory List (GeoJSON, trimmed)

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "id": "BOU",
      "properties": {
        "name": "Boulder",
        "agency": "USGS",
        "agency_name": "United States Geological Survey (USGS)",
        "sensor_orientation": "HDZ",
        "sensor_sampling_rate": 100.0,
        "declination_base": 5527
      },
      "geometry": {
        "type": "Point",
        "coordinates": [254.763, 40.137, 1682]
      }
    }
  ]
}
```

### Sample Response — Timeseries Data (JSON, trimmed)

```json
{
  "type": "Timeseries",
  "metadata": {
    "intermagnet": {
      "imo": {
        "iaga_code": "BOU",
        "name": "Boulder",
        "coordinates": [254.763, 40.137, 1682.0]
      },
      "reported_orientation": "H",
      "sensor_orientation": "HDZ",
      "data_type": "variation",
      "sampling_period": 60.0
    },
    "status": 200,
    "generated": "2026-04-06T11:15:48Z"
  },
  "times": ["2026-04-05T00:00:00.000Z", "2026-04-05T00:01:00.000Z", ...],
  "values": [{"id": "H", "values": [20651.89, 20651.94, ...]}]
}
```

## Authentication & Licensing

- **Auth**: None. Anonymous access.
- **Rate Limits**: Not explicitly stated; reasonable use expected.
- **License**: US Government public domain. No restrictions.

## Integration Notes

This is an exemplary geoscience data API. The Swagger/OpenAPI documentation means you can literally generate client code. The GeoJSON observatory list follows standard geospatial conventions. The timeseries data includes full INTERMAGNET metadata.

Key parameters:
- `id`: Observatory IAGA code (BOU, BRW, CMO, DED, FRN, GUA, HON, NEW, SJG, SIT, etc.)
- `type`: `variation` (real-time), `adjusted`, `quasi-definitive`, `definitive`
- `elements`: `H` (horizontal), `D` (declination), `Z` (vertical), `F` (total field), `X`, `Y`
- `sampling_period`: `1` (1-second), `60` (1-minute), `3600` (hourly)
- `format`: `json`, `iaga2002`

The `variation` data type is near-real-time — updated within minutes. Higher data quality levels (`adjusted`, `quasi-definitive`, `definitive`) have increasing delay but better calibration.

The data complements NOAA SWPC (which provides derived indices like Kp, Dst, alerts) with raw magnetic field measurements. USGS provides the ground truth; NOAA provides the interpretation.

## Feasibility Rating

| Dimension                    | Score | Notes |
|------------------------------|-------|-------|
| **API Maturity & Docs**      | 3     | OpenAPI spec; Swagger UI; excellent |
| **Data Freshness**           | 3     | 1-minute cadence; near-real-time |
| **Format / Schema Quality**  | 3     | GeoJSON observatories; clean JSON timeseries |
| **Auth / Access Simplicity** | 3     | Anonymous; US public domain |
| **Coverage Relevance**       | 2     | US observatories; 14 stations |
| **Operational Reliability**  | 3     | USGS; running for decades; critical infrastructure |
| **Total**                    | **17 / 18** | |

## Verdict

✅ **Build** — The best geomagnetic data API discovered in this survey. Modern REST with OpenAPI spec, GeoJSON, clean JSON timeseries, public domain, 1-minute cadence. This is what every geoscience data API should look like. Covers US territory comprehensively, and the global magnetic field means even a US-centric network has global relevance. Build alongside NOAA SWPC for a complete space weather monitoring picture.
