# Ireland OPW waterlevel.ie Bridge Events

This document describes the events emitted by the Ireland OPW waterlevel.ie bridge.

- [ie.gov.opw.waterlevel](#message-group-iegovopwwaterlevel)
  - [ie.gov.opw.waterlevel.Station](#message-iegovopwwaterlevelstation)
  - [ie.gov.opw.waterlevel.WaterLevelReading](#message-iegovopwwaterlevelwaterlevelreading)

---

## Message Group: ie.gov.opw.waterlevel

---

### Message: ie.gov.opw.waterlevel.Station

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `ie.gov.opw.waterlevel.Station` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Station | `uritemplate` | `False` | `{station_ref}` |

#### Schema:

##### Record: Station

*Reference data for an OPW hydrometric station in Ireland, including location and region.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `station_ref` | *string* | Zero-padded 10-digit station reference code (e.g. '0000001041'). |
| `station_name` | *string* | Human-readable name of the station (e.g. 'Sandy Mills'). |
| `region_id` | *int* | OPW hydrometric region identifier. |
| `longitude` | *double* | Longitude in WGS84 decimal degrees. |
| `latitude` | *double* | Latitude in WGS84 decimal degrees. |

---

### Message: ie.gov.opw.waterlevel.WaterLevelReading

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `ie.gov.opw.waterlevel.WaterLevelReading` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Station | `uritemplate` | `False` | `{station_ref}` |

#### Schema:

##### Record: WaterLevelReading

*A sensor reading from an OPW hydrometric station.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `station_ref` | *string* | Zero-padded 10-digit station reference code. |
| `station_name` | *string* | Human-readable station name. |
| `sensor_ref` | *string* | Sensor code: '0001' (level), '0002' (temperature), '0003' (voltage), 'OD' (Ordnance Datum). |
| `value` | *double (nullable)* | Sensor reading value. Units depend on sensor_ref. |
| `datetime` | *string* | ISO 8601 timestamp of the reading. |
| `err_code` | *int* | Error code (99 = OK). |
