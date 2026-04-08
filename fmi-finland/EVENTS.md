# FMI Finland Air Quality Bridge Events

This document describes the CloudEvents emitted by the FMI Finland air quality
bridge.

- Message group: `fi.fmi.opendata.airquality`
- Kafka topic: `fmi-finland-airquality`
- Kafka key and CloudEvents subject: `{fmisid}`

---

## Message: `fi.fmi.opendata.airquality.Station`

Reference data for an FMI air quality monitoring station.

### CloudEvents attributes

| Name | Value |
|---|---|
| `type` | `fi.fmi.opendata.airquality.Station` |
| `source` | `https://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=getFeature&storedquery_id=fmi::ef::stations` |
| `subject` | `{fmisid}` |

### Data fields

| Field | Type | Description |
|---|---|---|
| `fmisid` | `string` | Stable FMI station identifier used as Kafka key and CloudEvents subject. |
| `station_name` | `string` | Station name from FMI station metadata. |
| `latitude` | `double` | WGS84 latitude in decimal degrees. |
| `longitude` | `double` | WGS84 longitude in decimal degrees. |
| `municipality` | `string \| null` | Municipality or region from station metadata, if available. |

---

## Message: `fi.fmi.opendata.airquality.Observation`

Hourly air quality observation aggregated per station and observation time.

### CloudEvents attributes

| Name | Value |
|---|---|
| `type` | `fi.fmi.opendata.airquality.Observation` |
| `source` | `https://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=getFeature&storedquery_id=urban::observations::airquality::hourly::simple` |
| `subject` | `{fmisid}` |

### Data fields

| Field | Type | Description |
|---|---|---|
| `fmisid` | `string` | Stable FMI station identifier. |
| `station_name` | `string` | Station name resolved from reference data. |
| `observation_time` | `string` | UTC ISO-8601 timestamp for the observed hour, for example `2024-01-15T13:00:00Z`. |
| `aqindex` | `double \| null` | Finnish Air Quality Index 1-hour average (`AQINDEX_PT1H_avg`). |
| `pm10_ug_m3` | `double \| null` | PM10 1-hour average in µg/m³ (`PM10_PT1H_avg`). |
| `pm2_5_ug_m3` | `double \| null` | PM2.5 1-hour average in µg/m³ (`PM25_PT1H_avg`). |
| `no2_ug_m3` | `double \| null` | NO₂ 1-hour average in µg/m³ (`NO2_PT1H_avg`). |
| `o3_ug_m3` | `double \| null` | O₃ 1-hour average in µg/m³ (`O3_PT1H_avg`). |
| `so2_ug_m3` | `double \| null` | SO₂ 1-hour average in µg/m³ (`SO2_PT1H_avg`). |
| `co_mg_m3` | `double \| null` | CO 1-hour average in mg/m³ (`CO_PT1H_avg`). |
