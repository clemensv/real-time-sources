# NVE Hydrology Bridge Events

This document describes the events emitted by the NVE Hydrology Bridge.

- [NO.NVE.Hydrology](#message-group-nonvehydrology)
  - [NO.NVE.Hydrology.Station](#message-nonvehydrologystation)
  - [NO.NVE.Hydrology.WaterLevelObservation](#message-nonvehydrologywaterlevelobservation)

---

## Message Group: NO.NVE.Hydrology

Events from the Norwegian Water Resources and Energy Directorate's hydrological
monitoring network, delivered via the NVE HydAPI.

**Kafka topic**: `nve-hydro`
**Kafka key**: `{station_id}`
**Envelope**: CloudEvents/1.0, structured JSON (`application/cloudevents+json`)

---

### Message: NO.NVE.Hydrology.Station

Station reference data for a hydrological monitoring station.

#### CloudEvents Attributes:

| **Name** | **Description** | **Type** | **Required** | **Value** |
|----------|-----------------|----------|--------------|-----------|
| `type` | Event type | string | Yes | `NO.NVE.Hydrology.Station` |
| `source` | Data origin | URI | Yes | `https://hydapi.nve.no` |
| `subject` | Station identifier | string | Yes | `{station_id}` |
| `datacontenttype` | Content type | string | Yes | `application/json` |

#### Data Schema:

| **Field** | **Type** | **Required** | **Description** |
|-----------|----------|--------------|-----------------|
| `station_id` | string | Yes | NVE station identifier |
| `station_name` | string | Yes | Human-readable station name |
| `river_name` | string | No | Name of the river being monitored |
| `latitude` | double | Yes | WGS84 latitude of the station |
| `longitude` | double | Yes | WGS84 longitude of the station |
| `masl` | double | No | Elevation in meters above sea level |
| `council_name` | string | No | Municipality (kommune) name |
| `county_name` | string | No | County (fylke) name |
| `drainage_basin_area` | double | No | Drainage basin area in km² |

#### Example:

```json
{
  "specversion": "1.0",
  "type": "NO.NVE.Hydrology.Station",
  "source": "https://hydapi.nve.no",
  "subject": "2.268.0",
  "id": "...",
  "datacontenttype": "application/json",
  "data": {
    "station_id": "2.268.0",
    "station_name": "Gryta",
    "river_name": "Glomma",
    "latitude": 59.9853,
    "longitude": 11.1172,
    "masl": 101.0,
    "council_name": "Kongsvinger",
    "county_name": "Innlandet",
    "drainage_basin_area": 20235.0
  }
}
```

---

### Message: NO.NVE.Hydrology.WaterLevelObservation

A hydrological observation containing water level and/or discharge readings
from a monitoring station.

#### CloudEvents Attributes:

| **Name** | **Description** | **Type** | **Required** | **Value** |
|----------|-----------------|----------|--------------|-----------|
| `type` | Event type | string | Yes | `NO.NVE.Hydrology.WaterLevelObservation` |
| `source` | Data origin | URI | Yes | `https://hydapi.nve.no` |
| `subject` | Station identifier | string | Yes | `{station_id}` |
| `datacontenttype` | Content type | string | Yes | `application/json` |

#### Data Schema:

| **Field** | **Type** | **Required** | **Description** |
|-----------|----------|--------------|-----------------|
| `station_id` | string | Yes | NVE station identifier |
| `water_level` | double | No | Water level reading |
| `water_level_unit` | string | No | Unit of measurement (typically `m`) |
| `water_level_timestamp` | datetime | No | ISO 8601 timestamp of the water level reading |
| `discharge` | double | No | Water discharge reading |
| `discharge_unit` | string | No | Unit of measurement (typically `m3/s`) |
| `discharge_timestamp` | datetime | No | ISO 8601 timestamp of the discharge reading |

#### Example:

```json
{
  "specversion": "1.0",
  "type": "NO.NVE.Hydrology.WaterLevelObservation",
  "source": "https://hydapi.nve.no",
  "subject": "2.268.0",
  "id": "...",
  "datacontenttype": "application/json",
  "data": {
    "station_id": "2.268.0",
    "water_level": 3.47,
    "water_level_unit": "m",
    "water_level_timestamp": "2025-01-15T14:00:00+00:00",
    "discharge": 185.3,
    "discharge_unit": "m3/s",
    "discharge_timestamp": "2025-01-15T14:00:00+00:00"
  }
}
```

## Schema Formats

The event data schemas are defined in both JSON Structure and Apache Avro
formats in the [xRegistry manifest](xreg/nve_hydro.xreg.json). The bridge
defaults to JSON encoding, but the generated producer code supports both
`application/json` and `avro/binary` content types.
