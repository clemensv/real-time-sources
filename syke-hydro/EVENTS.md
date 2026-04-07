# SYKE Hydrology Bridge Events

This document describes the events emitted by the SYKE Hydrology Bridge.

- [FI.SYKE.Hydrology](#message-group-fisykehydrology)
  - [FI.SYKE.Hydrology.Station](#message-fisykehydrologystation)
  - [FI.SYKE.Hydrology.WaterLevelObservation](#message-fisykehydrologywaterlevelobservation)

---

## Message Group: FI.SYKE.Hydrology

Events from the Finnish Environment Institute's hydrological monitoring network,
delivered via the SYKE Hydrology OData API.

**Kafka topic**: `syke-hydro`
**Kafka key**: `{station_id}`
**Envelope**: CloudEvents/1.0, structured JSON (`application/cloudevents+json`)

---

### Message: FI.SYKE.Hydrology.Station

Station reference data for a hydrological monitoring station.

#### CloudEvents Attributes:

| **Name** | **Description** | **Type** | **Required** | **Value** |
|----------|-----------------|----------|--------------|-----------|
| `type` | Event type | string | Yes | `FI.SYKE.Hydrology.Station` |
| `source` | Data origin | URI | Yes | `https://rajapinnat.ymparisto.fi` |
| `subject` | Station identifier | string | Yes | `{station_id}` |
| `datacontenttype` | Content type | string | Yes | `application/json` |

#### Data Schema:

| **Field** | **Type** | **Required** | **Description** |
|-----------|----------|--------------|-----------------|
| `station_id` | string | Yes | SYKE station identifier (Paikka_Id) |
| `name` | string | Yes | Human-readable station name |
| `river_name` | string | No | Main water area name (PaaVesalNimi) |
| `water_area_name` | string | No | Water area name (VesalNimi) |
| `municipality` | string | No | Municipality name (KuntaNimi) |
| `latitude` | double | Yes | WGS84 latitude of the station |
| `longitude` | double | Yes | WGS84 longitude of the station |

#### Example:

```json
{
  "specversion": "1.0",
  "type": "FI.SYKE.Hydrology.Station",
  "source": "https://rajapinnat.ymparisto.fi",
  "subject": "3100",
  "id": "...",
  "datacontenttype": "application/json",
  "data": {
    "station_id": "3100",
    "name": "Iisalmi, Porovesi",
    "river_name": "Vuoksen vesistö",
    "water_area_name": "Porovesi",
    "municipality": "Iisalmi",
    "latitude": 63.5572,
    "longitude": 27.1897
  }
}
```

---

### Message: FI.SYKE.Hydrology.WaterLevelObservation

A hydrological observation containing water level and/or discharge readings
from a monitoring station.

#### CloudEvents Attributes:

| **Name** | **Description** | **Type** | **Required** | **Value** |
|----------|-----------------|----------|--------------|-----------|
| `type` | Event type | string | Yes | `FI.SYKE.Hydrology.WaterLevelObservation` |
| `source` | Data origin | URI | Yes | `https://rajapinnat.ymparisto.fi` |
| `subject` | Station identifier | string | Yes | `{station_id}` |
| `datacontenttype` | Content type | string | Yes | `application/json` |

#### Data Schema:

| **Field** | **Type** | **Required** | **Description** |
|-----------|----------|--------------|-----------------|
| `station_id` | string | Yes | SYKE station identifier (Paikka_Id) |
| `water_level` | double | No | Water level reading |
| `water_level_unit` | string | No | Unit of measurement (typically `cm`) |
| `water_level_timestamp` | datetime | No | ISO 8601 timestamp of the water level reading |
| `discharge` | double | No | Water discharge reading |
| `discharge_unit` | string | No | Unit of measurement (typically `m3/s`) |
| `discharge_timestamp` | datetime | No | ISO 8601 timestamp of the discharge reading |

#### Example:

```json
{
  "specversion": "1.0",
  "type": "FI.SYKE.Hydrology.WaterLevelObservation",
  "source": "https://rajapinnat.ymparisto.fi",
  "subject": "3100",
  "id": "...",
  "datacontenttype": "application/json",
  "data": {
    "station_id": "3100",
    "water_level": 8432.0,
    "water_level_unit": "cm",
    "water_level_timestamp": "2025-01-15T12:00:00+00:00",
    "discharge": 42.5,
    "discharge_unit": "m3/s",
    "discharge_timestamp": "2025-01-15T12:00:00+00:00"
  }
}
```

## Schema Formats

The event data schemas are defined in both JSON Structure and Apache Avro
formats in the [xRegistry manifest](xreg/syke_hydro.xreg.json). The bridge
defaults to JSON encoding, but the generated producer code supports both
`application/json` and `avro/binary` content types.
