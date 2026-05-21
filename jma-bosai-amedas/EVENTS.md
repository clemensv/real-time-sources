# JMA Bosai AMeDAS Bridge Events

This document describes CloudEvents emitted by the JMA Bosai AMeDAS bridge.

- [JP.JMA.Amedas](#message-group-jpjmaamedas)
  - [JP.JMA.Amedas.Station](#message-jpjmaamedasstation)
  - [JP.JMA.Amedas.Observation](#message-jpjmaamedasobservation)

---

## Message Group: JP.JMA.Amedas
---
### Message: JP.JMA.Amedas.Station
*Reference event for one JMA AMeDAS station from the Bosai amedastable.json station table, including names, geodetic position, elevation, station capability tier, and measurement capability bitmask.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `JP.JMA.Amedas.Station` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `jp.jma.amedas/{station_code}` |

#### Schema:
##### Object: Station
*Reference event for one JMA AMeDAS station from the Bosai amedastable.json station table, including names, geodetic position, elevation, station capability tier, and measurement capability bitmask.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_code` | *string* | - | `True` | JMA AMeDAS five-digit station code used as the stable identifier in the Bosai AMeDAS station table and observation map. |
| `kj_name` | *string* | - | `True` | Japanese kanji station name from the JMA AMeDAS station table (kjName), used by the Bosai web application for Japanese display labels. |
| `kana` | *string* | - | `True` | Japanese kana station reading from the JMA AMeDAS station table (knName in live payloads, kana in older examples), used by the Bosai web application for phonetic Japanese display. |
| `en_name` | *string* | - | `True` | English station name from the JMA AMeDAS station table. |
| `latitude` | *double* | degree (°) | `True` | Station latitude in WGS84 decimal degrees. The JMA station table publishes latitude as [degrees, minutes]; the bridge converts it with degrees + minutes/60. |
| `longitude` | *double* | degree (°) | `True` | Station longitude in WGS84 decimal degrees. The JMA station table publishes longitude as [degrees, minutes]; the bridge converts it with degrees + minutes/60. |
| `altitude_m` | *double* | meter | `True` | Station elevation above sea level in meters from the JMA station table alt field. |
| `station_type` | *string* | - | `True` | JMA AMeDAS station capability tier as published in the station table. The tier controls which measurements may be emitted for a station. |
| `elems_bitmask` | *string* | - | `True` | JMA Bosai AMeDAS element bitmask string from the station table. Each non-zero character indicates that the corresponding station capability is enabled in the Bosai web application. |
| `enabled_measurements` | array of *string* | - | `True` | Measurement capability names derived by the bridge from the JMA elems_bitmask. The values describe which observation families the station can emit, such as precipitation, wind, temperature, sunshine_duration, snow_depth, humidity, pressure, or visibility. |
---
### Message: JP.JMA.Amedas.Observation
*Telemetry event for one JMA AMeDAS station observation in a ten-minute Bosai map snapshot. Each measurement value is nullable because JMA publishes different fields by station capability and by observation availability.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `JP.JMA.Amedas.Observation` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `jp.jma.amedas/{station_code}` |

#### Schema:
##### Object: Observation
*Telemetry event for one JMA AMeDAS station observation in a ten-minute Bosai map snapshot. Each measurement value is nullable because JMA publishes different fields by station capability and by observation availability.*

The bridge always polls the 10-minute `data/map/{YYYYMMDDHHMM}00.json` snapshot. Gust and daily maximum/minimum temperature fields come from `data/point/{station_code}/{YYYYMMDD_HH}.json` and are populated only when point-detail enrichment is configured with `POINT_STATION_CODES`; otherwise those fields are emitted as `null`.

| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_code` | *string* | - | `True` | JMA AMeDAS five-digit station code used as the stable identifier in the Bosai AMeDAS station table and observation map. |
| `observed_at` | *string* | - | `True` | Observation snapshot timestamp converted from JMA latest_time.txt to UTC and serialized as RFC3339. AMeDAS map snapshots are published every ten minutes. |
| `observed_at_local` | *string* | - | `True` | Original JMA latest_time.txt timestamp in Japan Standard Time with +09:00 offset, serialized as RFC3339. |
| `temp` | *double* (optional) | celsius | `True` | Air temperature observed automatically by AMeDAS, expressed in degrees Celsius. JMA documents temperature as air temperature displayed in 0.1 °C units. |
| `temp_qc_flag` | *int32* (optional) | - | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. |
| `humidity` | *double* (optional) | percent | `True` | Relative humidity of the air observed automatically by AMeDAS, expressed as percent. JMA documents humidity as relative humidity displayed in 1 percent units. |
| `humidity_qc_flag` | *int32* (optional) | - | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. |
| `pressure` | *double* (optional) | hectopascal | `True` | Station pressure from JMA Bosai AMeDAS where available, expressed in hectopascals. |
| `pressure_qc_flag` | *int32* (optional) | - | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. |
| `normal_pressure` | *double* (optional) | hectopascal | `True` | Sea-level adjusted pressure (normalPressure in the Bosai payload) where available, expressed in hectopascals. |
| `normal_pressure_qc_flag` | *int32* (optional) | - | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. |
| `wind_speed` | *double* (optional) | meter_per_second | `True` | Wind speed averaged over the ten minutes before observation time, expressed in meters per second. JMA documents wind speed as the speed of the wind over the preceding ten minutes. |
| `wind_speed_qc_flag` | *int32* (optional) | - | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. |
| `wind_direction` | *double* (optional) | degree | `True` | Wind direction from which the wind blows, converted by the bridge from JMA 16-direction codes to degrees clockwise from true north. |
| `wind_direction_qc_flag` | *int32* (optional) | - | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. |
| `wind_gust` | *double* (optional) | meter_per_second | `True` | Maximum instantaneous wind speed (gust) for the observation interval from the JMA Bosai per-station point payload, expressed in meters per second. The bridge enriches map observations with this value only for configured point-detail stations. |
| `wind_gust_qc_flag` | *int32* (optional) | - | `True` | JMA quality-control flag accompanying the gust tuple in the Bosai AMeDAS per-station point payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA non-normal quality states as represented by the Bosai web application. |
| `wind_gust_direction` | *double* (optional) | degree | `True` | Direction from which the maximum instantaneous wind gust blew, converted by the bridge from JMA 16-direction codes in gustDirection to degrees clockwise from true north. The field is present only when point-detail enrichment is configured and JMA publishes a gust direction. |
| `wind_gust_time` | *string* (optional) | - | `True` | UTC RFC3339 timestamp for the maximum instantaneous wind gust time from the JMA Bosai per-station gustTime object. JMA publishes hour and minute in local time; the bridge resolves the date relative to the observation timestamp and converts it to UTC. |
| `max_temp` | *double* (optional) | celsius | `True` | Maximum air temperature from the JMA Bosai per-station point payload, expressed in degrees Celsius. The bridge enriches map observations with this value only for configured point-detail stations. |
| `max_temp_time` | *string* (optional) | - | `True` | UTC RFC3339 timestamp for the maximum air temperature time from the JMA Bosai per-station maxTempTime object. JMA publishes hour and minute in local time; the bridge resolves the date relative to the observation timestamp and converts it to UTC. |
| `min_temp` | *double* (optional) | celsius | `True` | Minimum air temperature from the JMA Bosai per-station point payload, expressed in degrees Celsius. The bridge enriches map observations with this value only for configured point-detail stations. |
| `min_temp_time` | *string* (optional) | - | `True` | UTC RFC3339 timestamp for the minimum air temperature time from the JMA Bosai per-station minTempTime object. JMA publishes hour and minute in local time; the bridge resolves the date relative to the observation timestamp and converts it to UTC. |
| `precipitation10m` | *double* (optional) | millimeter | `True` | Precipitation amount for the previous 10 minutes, expressed in millimeters of liquid water equivalent. JMA documents precipitation as rain or snow amount melted to water and displayed in 0.5 mm units. |
| `precipitation10m_qc_flag` | *int32* (optional) | - | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. |
| `precipitation1h` | *double* (optional) | millimeter | `True` | Precipitation amount for the previous 1 hour, expressed in millimeters of liquid water equivalent. |
| `precipitation1h_qc_flag` | *int32* (optional) | - | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. |
| `precipitation3h` | *double* (optional) | millimeter | `True` | Precipitation amount for the previous 3 hours, expressed in millimeters of liquid water equivalent. |
| `precipitation3h_qc_flag` | *int32* (optional) | - | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. |
| `precipitation24h` | *double* (optional) | millimeter | `True` | Precipitation amount for the previous 24 hours, expressed in millimeters of liquid water equivalent. |
| `precipitation24h_qc_flag` | *int32* (optional) | - | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. |
| `sun10m` | *double* (optional) | minute | `True` | Sunshine duration for the previous 10 minutes, expressed in minutes. JMA publishes this ten-minute map field in minutes, so its unit intentionally differs from the hourly sun1h field. |
| `sun10m_qc_flag` | *int32* (optional) | - | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. |
| `sun1h` | *double* (optional) | hour | `True` | Sunshine duration for the previous 1 hour, expressed in hours as published by the Bosai AMeDAS map. JMA publishes this hourly field in hours, so its unit intentionally differs from the ten-minute sun10m field. |
| `sun1h_qc_flag` | *int32* (optional) | - | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. |
| `snow` | *double* (optional) | centimeter | `True` | Snow depth, the height of snow on the ground, expressed in centimeters. JMA documents snow depth as the height from the ground surface to the top of accumulated snow. |
| `snow_qc_flag` | *int32* (optional) | - | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. |
| `snow1h` | *double* (optional) | centimeter | `True` | Change in snow depth over the previous 1 hour, expressed in centimeters. |
| `snow1h_qc_flag` | *int32* (optional) | - | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. |
| `snow6h` | *double* (optional) | centimeter | `True` | Change in snow depth over the previous 6 hours, expressed in centimeters. |
| `snow6h_qc_flag` | *int32* (optional) | - | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. |
| `snow12h` | *double* (optional) | centimeter | `True` | Change in snow depth over the previous 12 hours, expressed in centimeters. |
| `snow12h_qc_flag` | *int32* (optional) | - | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. |
| `snow24h` | *double* (optional) | centimeter | `True` | Change in snow depth over the previous 24 hours, expressed in centimeters. |
| `snow24h_qc_flag` | *int32* (optional) | - | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. |
| `visibility` | *double* (optional) | meter | `True` | Horizontal visibility where published by JMA Bosai AMeDAS, expressed in meters. |
| `visibility_qc_flag` | *int32* (optional) | - | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. |
| `cloud` | *double* (optional) | - | `True` | Cloud amount code from JMA Bosai AMeDAS where available. The Bosai map exposes this as a numeric measurement tuple for stations that publish cloud information. |
| `cloud_qc_flag` | *int32* (optional) | - | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. |
| `weather` | *double* (optional) | - | `True` | Present weather code from JMA Bosai AMeDAS where available. The Bosai map exposes this as a numeric measurement tuple for stations that publish weather information. |
| `weather_qc_flag` | *int32* (optional) | - | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. |
