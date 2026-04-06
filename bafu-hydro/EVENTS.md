# BAFU Hydrology Bridge Events

This document describes the events emitted by the BAFU Hydrology Bridge.

- [CH.BAFU.Hydrology](#message-group-chbafuhydrology)
  - [CH.BAFU.Hydrology.Station](#message-chbafuhydrologystation)
  - [CH.BAFU.Hydrology.WaterLevelObservation](#message-chbafuhydrologywaterlevelobservation)

---

## Message Group: CH.BAFU.Hydrology

Events from the Swiss Federal Office for the Environment's hydrological
monitoring network, delivered via the existenz.ch Hydro API.

**Kafka topic**: `bafu-hydro`
**Kafka key**: `{station_id}`
**Envelope**: CloudEvents/1.0, structured JSON (`application/cloudevents+json`)

---

### Message: CH.BAFU.Hydrology.Station

Station reference data for a hydrological monitoring station.

#### CloudEvents Attributes:

| **Name** | **Description** | **Type** | **Required** | **Value** |
|----------|-----------------|----------|--------------|-----------|
| `type` | Event type | string | Yes | `CH.BAFU.Hydrology.Station` |
| `source` | Data origin | URI | Yes | `https://www.hydrodaten.admin.ch` |
| `subject` | Station identifier | string | Yes | `{station_id}` |
| `datacontenttype` | Content type | string | Yes | `application/json` |

#### Data Schema:

| **Field** | **Type** | **Required** | **Description** |
|-----------|----------|--------------|-----------------|
| `station_id` | string | Yes | BAFU station identifier |
| `name` | string | Yes | Human-readable station name |
| `water_body_name` | string | No | Name of the river or lake being monitored |
| `water_body_type` | string | No | Classification of the water body |
| `latitude` | double | Yes | WGS84 latitude of the station |
| `longitude` | double | Yes | WGS84 longitude of the station |

#### Example:

```json
{
  "specversion": "1.0",
  "type": "CH.BAFU.Hydrology.Station",
  "source": "https://www.hydrodaten.admin.ch",
  "subject": "2009",
  "id": "...",
  "datacontenttype": "application/json",
  "data": {
    "station_id": "2009",
    "name": "Rhein - Basel, Rheinhalle",
    "water_body_name": "Rhein",
    "water_body_type": "river",
    "latitude": 47.559,
    "longitude": 7.616
  }
}
```

---

### Message: CH.BAFU.Hydrology.WaterLevelObservation

A hydrological observation containing water level, discharge, and/or water
temperature readings from a monitoring station.

#### CloudEvents Attributes:

| **Name** | **Description** | **Type** | **Required** | **Value** |
|----------|-----------------|----------|--------------|-----------|
| `type` | Event type | string | Yes | `CH.BAFU.Hydrology.WaterLevelObservation` |
| `source` | Data origin | URI | Yes | `https://www.hydrodaten.admin.ch` |
| `subject` | Station identifier | string | Yes | `{station_id}` |
| `datacontenttype` | Content type | string | Yes | `application/json` |

#### Data Schema:

| **Field** | **Type** | **Required** | **Description** |
|-----------|----------|--------------|-----------------|
| `station_id` | string | Yes | BAFU station identifier |
| `water_level` | double | No | Water level reading |
| `water_level_unit` | string | No | Unit of measurement (typically `m`) |
| `water_level_timestamp` | datetime | No | ISO 8601 timestamp of the water level reading |
| `discharge` | double | No | Water discharge reading |
| `discharge_unit` | string | No | Unit of measurement (typically `m3/s`) |
| `discharge_timestamp` | datetime | No | ISO 8601 timestamp of the discharge reading |
| `water_temperature` | double | No | Water temperature reading |
| `water_temperature_unit` | string | No | Unit of measurement (typically `C`) |
| `water_temperature_timestamp` | datetime | No | ISO 8601 timestamp of the temperature reading |

#### Example:

```json
{
  "specversion": "1.0",
  "type": "CH.BAFU.Hydrology.WaterLevelObservation",
  "source": "https://www.hydrodaten.admin.ch",
  "subject": "2009",
  "id": "...",
  "datacontenttype": "application/json",
  "data": {
    "station_id": "2009",
    "water_level": 245.62,
    "water_level_unit": "m",
    "water_level_timestamp": "2025-01-15T14:30:00+00:00",
    "discharge": 1045.0,
    "discharge_unit": "m3/s",
    "discharge_timestamp": "2025-01-15T14:30:00+00:00",
    "water_temperature": 7.2,
    "water_temperature_unit": "C",
    "water_temperature_timestamp": "2025-01-15T14:30:00+00:00"
  }
}
```

## Schema Formats

The event data schemas are defined in both JSON Structure and Apache Avro
formats in the [xRegistry manifest](xreg/bafu_hydro.xreg.json). The bridge
defaults to JSON encoding, but the generated producer code supports both
`application/json` and `avro/binary` content types.
