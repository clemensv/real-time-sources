# GIOŚ Poland Air Quality Bridge Events

This document describes the events emitted by the GIOŚ Poland Air Quality Bridge.

- [pl.gov.gios.airquality](#message-group-plgovgiosairquality)
  - [pl.gov.gios.airquality.Station](#message-plgovgiosairqualitystation)
  - [pl.gov.gios.airquality.Sensor](#message-plgovgiosairqualitysensor)
  - [pl.gov.gios.airquality.Measurement](#message-plgovgiosairqualitymeasurement)
  - [pl.gov.gios.airquality.AirQualityIndex](#message-plgovgiosairqualityairqualityindex)

---

## Message Group: pl.gov.gios.airquality

---

### Message: pl.gov.gios.airquality.Station

*Reference data — sent once at startup before telemetry polling begins.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `pl.gov.gios.airquality.Station` |
| `source` | CloudEvent source | `string` | `True` | `https://api.gios.gov.pl/pjp-api/v1/rest/` |

#### Schema: Station

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `station_id` | *integer* | Unique numeric station identifier |
| `station_code` | *string* | Short alphanumeric station code |
| `name` | *string* | Human-readable station name |
| `latitude` | *number* | Latitude in decimal degrees (WGS84) |
| `longitude` | *number* | Longitude in decimal degrees (WGS84) |
| `city_id` | *integer* | Numeric city identifier |
| `city_name` | *string* | City name |
| `commune` | *string* | Commune (gmina) name |
| `district` | *string* | District (powiat) name |
| `voivodeship` | *string* | Voivodeship (province) name |
| `street` | *string* | Street address |

---

### Message: pl.gov.gios.airquality.Sensor

*Reference data — sent once at startup after station data.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `pl.gov.gios.airquality.Sensor` |
| `source` | CloudEvent source | `string` | `True` | `https://api.gios.gov.pl/pjp-api/v1/rest/` |

#### Schema: Sensor

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `sensor_id` | *integer* | Unique numeric sensor identifier |
| `station_id` | *integer* | Parent station identifier |
| `parameter_name` | *string* | Polish name of the pollutant |
| `parameter_formula` | *string* | Chemical formula (PM10, NO2, etc.) |
| `parameter_code` | *string* | Short pollutant code |
| `parameter_id` | *integer* | Numeric parameter identifier |

---

### Message: pl.gov.gios.airquality.Measurement

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `pl.gov.gios.airquality.Measurement` |
| `source` | CloudEvent source | `string` | `True` | `https://api.gios.gov.pl/pjp-api/v1/rest/` |

#### Schema: Measurement

| **Field Name** | **Type** | **Unit** | **Description** |
|----------------|----------|----------|-----------------|
| `station_id` | *integer* | — | Parent station identifier |
| `sensor_id` | *integer* | — | Sensor identifier |
| `sensor_code` | *string* | — | Sensor code with aggregation period |
| `timestamp` | *string (date-time)* | — | Measurement timestamp |
| `value` | *number* | µg/m³ | Pollutant concentration (nullable) |

---

### Message: pl.gov.gios.airquality.AirQualityIndex

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `pl.gov.gios.airquality.AirQualityIndex` |
| `source` | CloudEvent source | `string` | `True` | `https://api.gios.gov.pl/pjp-api/v1/rest/` |

#### Schema: AirQualityIndex

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `station_id` | *integer* | Station identifier |
| `calculation_timestamp` | *string (date-time)* | When the index was calculated |
| `index_value` | *integer* | Overall AQI value (0–5) |
| `index_category` | *string* | Polish AQI category name |
| `so2_index_value` | *integer* | SO₂ sub-index (0–5) |
| `no2_index_value` | *integer* | NO₂ sub-index (0–5) |
| `pm10_index_value` | *integer* | PM10 sub-index (0–5) |
| `pm25_index_value` | *integer* | PM2.5 sub-index (0–5) |
| `o3_index_value` | *integer* | O₃ sub-index (0–5) |
| `overall_status` | *boolean* | Whether the index is valid |
| `critical_pollutant_code` | *string* | Pollutant determining the index |
