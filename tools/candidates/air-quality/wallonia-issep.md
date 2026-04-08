# Wallonia ISSeP Air Quality Sensors

**Country/Region**: Belgium (Wallonia)
**Publisher**: ISSeP via Open Data Wallonie-Bruxelles
**API Endpoint**: `https://www.odwb.be/api/explore/v2.1/catalog/datasets/last-data-capteurs-qualite-de-l-air-issep/records`
**Documentation**: `https://www.odwb.be/explore/dataset/last-data-capteurs-qualite-de-l-air-issep/information/`
**Protocol**: REST JSON (Opendatasoft API)
**Auth**: None
**Data Format**: JSON, CSV, RDF, XLSX, Parquet
**Update Frequency**: Near-real-time latest-record feed
**License**: CC BY 4.0

## What It Provides

This dataset exposes the latest observations from Wallonia's ISSeP air-quality sensors
through a simple Opendatasoft API. It is not a Belgium-wide umbrella feed like
IRCELINE. It is smaller and more direct: fetch the latest records and get pollutant
plus environmental sensor fields in one JSON object.

That makes it useful as a lightweight regional source and as a very easy Opendatasoft
integration pattern.

## API Details

### Latest records endpoint

```text
GET https://www.odwb.be/api/explore/v2.1/catalog/datasets/last-data-capteurs-qualite-de-l-air-issep/records?limit=2
```

Sample record:

```json
{
  "id_configuration": 10412,
  "moment": "2026-04-08T09:09:13+02:00",
  "co": 156,
  "no": 19,
  "no2": -4,
  "ppbno": 2.711,
  "ppbo3": 8.635,
  "pm1": 9.76,
  "pm25": 7.409,
  "pm10": 12.092,
  "bme_t": 8.51,
  "bme_pres": 101729,
  "bme_rh": 61.35,
  "pm25_statut": 100,
  "pm10_statut": 100
}
```

### Exposed formats confirmed through the catalog

- JSON
- CSV
- RDF/XML
- RDF/Turtle
- JSON-LD
- XLSX
- Parquet

## Freshness Assessment

Confirmed live on 2026-04-08. The API returned records timestamped on the same day,
with the sample showing `moment = 2026-04-08T09:09:13+02:00`. The dataset returned a
small latest-record set quickly and without authentication.

## Entity Model

- **Sensor Configuration** - stable `id_configuration`
- **Observation** - timestamped latest record
- **Pollutant Fields** - `co`, `no`, `no2`, ozone-related values, particulate matter
- **Environmental Fields** - temperature, pressure, humidity, battery
- **Quality/Status Fields** - `*_statut` per measured dimension

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Same-day latest records confirmed |
| Openness | 3 | No auth; multiple export formats |
| Stability | 2 | Opendatasoft-hosted regional platform rather than a national canonical API |
| Structure | 3 | Clean JSON with stable field names |
| Identifiers | 2 | Configuration id is stable; station/location model needs second-pass confirmation |
| Additive Value | 2 | Regional subset that complements, rather than replaces, IRCELINE |
| **Total** | **15/18** | |

## Notes

- This is best understood as a Wallonia-specific complement to `irceline-belgium.md`.
- The API is much simpler than the SOS-style IRCELINE surface, which makes it a nice
  low-friction source if a regional feed is acceptable.
- The field set looks sensor-oriented and may represent a subset or specialized sensor
  network rather than the full Belgian regulatory station estate.
