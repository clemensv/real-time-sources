# German Waters Bridge Events

This document describes the events emitted by the German Waters Bridge.

- [DE.Waters.Hydrology](#message-group-dewatershydrology)
  - [DE.Waters.Hydrology.Station](#message-dewatershydrologystation)
  - [DE.Waters.Hydrology.WaterLevelObservation](#message-dewatershydrologywaterlevelobservation)

---

## Message Group: DE.Waters.Hydrology

Events from Germany's state-level hydrological monitoring networks, aggregated
from 12 federal state open data portals covering ~2,724 gauging stations.

**Kafka topic**: `german-waters`
**Kafka key**: `{station_id}`
**Envelope**: CloudEvents/1.0, structured JSON (`application/cloudevents+json`)

---

### Message: DE.Waters.Hydrology.Station

Station reference data for a hydrological monitoring station.

#### CloudEvents Attributes:

| **Name** | **Description** | **Type** | **Required** | **Value** |
|----------|-----------------|----------|--------------|-----------|
| `type` | Event type | string | Yes | `DE.Waters.Hydrology.Station` |
| `source` | Data origin | URI | Yes | `https://github.com/clemensv/real-time-sources/german-waters` |
| `subject` | Station identifier | string | Yes | `{station_id}` |
| `datacontenttype` | Content type | string | Yes | `application/json` |

#### Data Schema:

| **Field** | **Type** | **Required** | **Description** |
|-----------|----------|--------------|-----------------|
| `station_id` | string | Yes | Unique station identifier (provider-specific) |
| `station_name` | string | Yes | Human-readable station name |
| `water_body` | string | Yes | Name of the river or lake being monitored |
| `state` | string | No | Federal state name (e.g., `Bayern`, `Hessen`) |
| `region` | string | No | Sub-regional designation |
| `provider` | string | Yes | Provider key (e.g., `bayern_gkd`, `nrw_hygon`) |
| `latitude` | double | No | WGS84 latitude of the station |
| `longitude` | double | No | WGS84 longitude of the station |
| `river_km` | double | No | River kilometre marker |
| `altitude` | double | No | Station altitude in metres |
| `station_type` | string | No | Classification of the station |
| `warn_level_cm` | double | No | Warning water level threshold in cm |
| `alarm_level_cm` | double | No | Alarm water level threshold in cm |
| `warn_level_m3s` | double | No | Warning discharge threshold in m³/s |
| `alarm_level_m3s` | double | No | Alarm discharge threshold in m³/s |

#### Example:

```json
{
  "specversion": "1.0",
  "type": "DE.Waters.Hydrology.Station",
  "source": "https://github.com/clemensv/real-time-sources/german-waters",
  "subject": "bayern_gkd_16005701",
  "id": "...",
  "datacontenttype": "application/json",
  "data": {
    "station_id": "bayern_gkd_16005701",
    "station_name": "München / Isar",
    "water_body": "Isar",
    "state": "Bayern",
    "region": "",
    "provider": "bayern_gkd",
    "latitude": 48.1351,
    "longitude": 11.5820,
    "river_km": 153.8,
    "altitude": 519.0,
    "station_type": "",
    "warn_level_cm": 200.0,
    "alarm_level_cm": 300.0,
    "warn_level_m3s": 0.0,
    "alarm_level_m3s": 0.0
  }
}
```

---

### Message: DE.Waters.Hydrology.WaterLevelObservation

A hydrological observation containing water level and/or discharge readings
from a monitoring station.

#### CloudEvents Attributes:

| **Name** | **Description** | **Type** | **Required** | **Value** |
|----------|-----------------|----------|--------------|-----------|
| `type` | Event type | string | Yes | `DE.Waters.Hydrology.WaterLevelObservation` |
| `source` | Data origin | URI | Yes | `https://github.com/clemensv/real-time-sources/german-waters` |
| `subject` | Station identifier | string | Yes | `{station_id}` |
| `datacontenttype` | Content type | string | Yes | `application/json` |

#### Data Schema:

| **Field** | **Type** | **Required** | **Description** |
|-----------|----------|--------------|-----------------|
| `station_id` | string | Yes | Unique station identifier |
| `provider` | string | Yes | Provider key (e.g., `bayern_gkd`) |
| `water_level` | double | No | Water level reading |
| `water_level_unit` | string | No | Unit of measurement (typically `cm`) |
| `water_level_timestamp` | datetime | No | ISO 8601 timestamp of the water level reading |
| `discharge` | double | No | Water discharge reading |
| `discharge_unit` | string | No | Unit of measurement (typically `m3/s`) |
| `discharge_timestamp` | datetime | No | ISO 8601 timestamp of the discharge reading |
| `trend` | int32 | No | Trend indicator (e.g., rising, falling, stable) |
| `situation` | int32 | No | Situation/alarm level indicator |

#### Example:

```json
{
  "specversion": "1.0",
  "type": "DE.Waters.Hydrology.WaterLevelObservation",
  "source": "https://github.com/clemensv/real-time-sources/german-waters",
  "subject": "bayern_gkd_16005701",
  "id": "...",
  "datacontenttype": "application/json",
  "data": {
    "station_id": "bayern_gkd_16005701",
    "provider": "bayern_gkd",
    "water_level": 134.0,
    "water_level_unit": "cm",
    "water_level_timestamp": "2025-01-15T14:30:00+01:00",
    "discharge": 78.5,
    "discharge_unit": "m3/s",
    "discharge_timestamp": "2025-01-15T14:30:00+01:00",
    "trend": 0,
    "situation": 0
  }
}
```

## Schema Formats

The event data schemas are defined in both JSON Structure and Apache Avro
formats in the [xRegistry manifest](xreg/german_waters.xreg.json). The bridge
defaults to JSON encoding, but the generated producer code supports both
`application/json` and `avro/binary` content types.
