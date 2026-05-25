# JMA Bosai AMeDAS Bridge Events

This source bridges the Japan Meteorological Agency (JMA / 気象庁) Bosai AMeDAS public data feed into Apache Kafka, Azure Event Hubs, or Microsoft Fabric Event Streams as CloudEvents.

## Table of Contents

- [Registry](#registry)
- [Endpoints](#endpoints)
- [Messagegroups](#messagegroups)
- [Schemagroups](#schemagroups)

---

## Registry

| Field | Value |
| --- | --- |
| Endpoints | 1 |
| Messagegroups | 1 |
| Schemagroups | 2 |

## Endpoints

### Endpoint `JP.JMA.Amedas.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`JP.JMA.Amedas`](#messagegroup-jpjmaamedas) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `jma-bosai-amedas` |
| Kafka key | `jp.jma.amedas/{station_code}` |
| Deployed | False |

## Messagegroups

### Messagegroup `JP.JMA.Amedas`
<a id="messagegroup-jpjmaamedas"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `JP.JMA.Amedas.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `JP.JMA.Amedas.Station`
<a id="message-jpjmaamedasstation"></a>

Reference event for one JMA AMeDAS station from the Bosai amedastable.json station table, including names, geodetic position, elevation, station capability tier, and measurement capability bitmask.

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/JP.JMA.Amedas.jstruct/schemas/JP.JMA.Amedas.Station`](#schema-jpjmaamedasstation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `JP.JMA.Amedas.Station` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `jp.jma.amedas/{station_code}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `JP.JMA.Amedas.Kafka` | `KAFKA` | topic `jma-bosai-amedas`; key `jp.jma.amedas/{station_code}` |

#### Message `JP.JMA.Amedas.Observation`
<a id="message-jpjmaamedasobservation"></a>

Telemetry event for one JMA AMeDAS station observation in a ten-minute Bosai map snapshot. Each measurement value is nullable because JMA publishes different fields by station capability and by observation availability.

| Field | Value |
| --- | --- |
| Name | Observation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/JP.JMA.Amedas.jstruct/schemas/JP.JMA.Amedas.Observation`](#schema-jpjmaamedasobservation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `JP.JMA.Amedas.Observation` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `jp.jma.amedas/{station_code}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `JP.JMA.Amedas.Kafka` | `KAFKA` | topic `jma-bosai-amedas`; key `jp.jma.amedas/{station_code}` |

## Schemagroups

### Schemagroup `JP.JMA.Amedas.jstruct`
<a id="schemagroup-jpjmaamedasjstruct"></a>

#### Schema `JP.JMA.Amedas.Station`
<a id="schema-jpjmaamedasstation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://www.jma.go.jp/schemas/bosai/amedas/Station` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| $root | `#/definitions/JP/JMA/Amedas/Station` |
| Type | `object` |

###### Object `Station`
<a id="schema-node-station"></a>

Reference event for one JMA AMeDAS station from the Bosai amedastable.json station table, including names, geodetic position, elevation, station capability tier, and measurement capability bitmask.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_code` | `string` | `True` | JMA AMeDAS five-digit station code used as the stable identifier in the Bosai AMeDAS station table and observation map. | - | pattern=`^[0-9]{5}$` | - |
| `kj_name` | `string` | `True` | Japanese kanji station name from the JMA AMeDAS station table (kjName), used by the Bosai web application for Japanese display labels. | altnames=`{"lang:ja-Kanji": "kjName"}` | - | - |
| `kana` | `string` | `True` | Japanese kana station reading from the JMA AMeDAS station table (knName in live payloads, kana in older examples), used by the Bosai web application for phonetic Japanese display. | altnames=`{"lang:ja-Kana": "knName"}` | - | - |
| `en_name` | `string` | `True` | English station name from the JMA AMeDAS station table. | altnames=`{"json": "enName"}` | - | - |
| `latitude` | `double` | `True` | Station latitude in WGS84 decimal degrees. The JMA station table publishes latitude as [degrees, minutes]; the bridge converts it with degrees + minutes/60. | unit=`degree` symbol=`°`<br>altnames=`{"jma-bosai": "lat"}` | maximum=`90`<br>minimum=`-90` | - |
| `longitude` | `double` | `True` | Station longitude in WGS84 decimal degrees. The JMA station table publishes longitude as [degrees, minutes]; the bridge converts it with degrees + minutes/60. | unit=`degree` symbol=`°`<br>altnames=`{"jma-bosai": "lon"}` | maximum=`180`<br>minimum=`-180` | - |
| `altitude_m` | `double` | `True` | Station elevation above sea level in meters from the JMA station table alt field. | unit=`meter`<br>altnames=`{"json": "alt"}` | - | - |
| `station_type` | enum `['A', 'B', 'C']` | `True` | JMA AMeDAS station capability tier as published in the station table. The tier controls which measurements may be emitted for a station. | descriptions=`{"A": "JMA AMeDAS capability tier A station, typically a major station with pressure and broader meteorological observations.", "B": "JMA AMeDAS capability tier B station.", "C": "JMA AMeDAS capability tier C station, commonly an automated regional station with a smaller measurement set."}` | - | - |
| `elems_bitmask` | `string` | `True` | JMA Bosai AMeDAS element bitmask string from the station table. Each non-zero character indicates that the corresponding station capability is enabled in the Bosai web application. | altnames=`{"json": "elems"}` | - | - |
| `enabled_measurements` | array of `string` | `True` | Measurement capability names derived by the bridge from the JMA elems_bitmask. The values describe which observation families the station can emit, such as precipitation, wind, temperature, sunshine_duration, snow_depth, humidity, pressure, or visibility. | - | - | - |

#### Schema `JP.JMA.Amedas.Observation`
<a id="schema-jpjmaamedasobservation"></a>

| Field | Value |
| --- | --- |
| Name | Observation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://www.jma.go.jp/schemas/bosai/amedas/Observation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| $root | `#/definitions/JP/JMA/Amedas/Observation` |
| Type | `object` |

###### Object `Observation`
<a id="schema-node-observation"></a>

Telemetry event for one JMA AMeDAS station observation in a ten-minute Bosai map snapshot. Each measurement value is nullable because JMA publishes different fields by station capability and by observation availability.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_code` | `string` | `True` | JMA AMeDAS five-digit station code used as the stable identifier in the Bosai AMeDAS station table and observation map. | - | pattern=`^[0-9]{5}$` | - |
| `observed_at` | `datetime` | `True` | Observation snapshot timestamp converted from JMA latest_time.txt to UTC and serialized as RFC3339. AMeDAS map snapshots are published every ten minutes. | - | - | - |
| `observed_at_local` | `datetime` | `True` | Original JMA latest_time.txt timestamp in Japan Standard Time with +09:00 offset, serialized as RFC3339. | - | - | - |
| `temp` | `union` | `True` | Air temperature observed automatically by AMeDAS, expressed in degrees Celsius. JMA documents temperature as air temperature displayed in 0.1 °C units. | unit=`celsius`<br>altnames=`{"jma-bosai": "temp"}` | - | - |
| `temp_qc_flag` | `union` | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | - | - | - |
| `humidity` | `union` | `True` | Relative humidity of the air observed automatically by AMeDAS, expressed as percent. JMA documents humidity as relative humidity displayed in 1 percent units. | unit=`percent`<br>altnames=`{"jma-bosai": "humidity"}` | maximum=`100`<br>minimum=`0` | - |
| `humidity_qc_flag` | `union` | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | - | - | - |
| `pressure` | `union` | `True` | Station pressure from JMA Bosai AMeDAS where available, expressed in hectopascals. | unit=`hectopascal`<br>altnames=`{"jma-bosai": "pressure"}` | - | - |
| `pressure_qc_flag` | `union` | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | - | - | - |
| `normal_pressure` | `union` | `True` | Sea-level adjusted pressure (normalPressure in the Bosai payload) where available, expressed in hectopascals. | unit=`hectopascal`<br>altnames=`{"jma-bosai": "normalPressure"}` | - | - |
| `normal_pressure_qc_flag` | `union` | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | - | - | - |
| `wind_speed` | `union` | `True` | Wind speed averaged over the ten minutes before observation time, expressed in meters per second. JMA documents wind speed as the speed of the wind over the preceding ten minutes. | unit=`meter_per_second`<br>altnames=`{"jma-bosai": "wind"}` | - | - |
| `wind_speed_qc_flag` | `union` | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | - | - | - |
| `wind_direction` | `union` | `True` | Wind direction from which the wind blows, converted by the bridge from JMA 16-direction codes to degrees clockwise from true north. | unit=`degree`<br>altnames=`{"jma-bosai": "windDirection"}` | exclusiveMaximum=`360`<br>minimum=`0` | - |
| `wind_direction_qc_flag` | `union` | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | - | - | - |
| `wind_gust` | `union` | `True` | Maximum instantaneous wind speed (gust) for the observation interval from the JMA Bosai per-station point payload, expressed in meters per second. The bridge enriches map observations with this value only for configured point-detail stations. | unit=`meter_per_second`<br>altnames=`{"jma-bosai": "gust"}` | - | - |
| `wind_gust_qc_flag` | `union` | `True` | JMA quality-control flag accompanying the gust tuple in the Bosai AMeDAS per-station point payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA non-normal quality states as represented by the Bosai web application. | - | - | - |
| `wind_gust_direction` | `union` | `True` | Direction from which the maximum instantaneous wind gust blew, converted by the bridge from JMA 16-direction codes in gustDirection to degrees clockwise from true north. The field is present only when point-detail enrichment is configured and JMA publishes a gust direction. | unit=`degree`<br>altnames=`{"jma-bosai": "gustDirection"}` | exclusiveMaximum=`360`<br>minimum=`0` | - |
| `wind_gust_time` | `union` | `True` | UTC RFC3339 timestamp for the maximum instantaneous wind gust time from the JMA Bosai per-station gustTime object. JMA publishes hour and minute in local time; the bridge resolves the date relative to the observation timestamp and converts it to UTC. | altnames=`{"jma-bosai": "gustTime"}` | - | - |
| `max_temp` | `union` | `True` | Maximum air temperature from the JMA Bosai per-station point payload, expressed in degrees Celsius. The bridge enriches map observations with this value only for configured point-detail stations. | unit=`celsius`<br>altnames=`{"jma-bosai": "maxTemp"}` | - | - |
| `max_temp_time` | `union` | `True` | UTC RFC3339 timestamp for the maximum air temperature time from the JMA Bosai per-station maxTempTime object. JMA publishes hour and minute in local time; the bridge resolves the date relative to the observation timestamp and converts it to UTC. | altnames=`{"jma-bosai": "maxTempTime"}` | - | - |
| `min_temp` | `union` | `True` | Minimum air temperature from the JMA Bosai per-station point payload, expressed in degrees Celsius. The bridge enriches map observations with this value only for configured point-detail stations. | unit=`celsius`<br>altnames=`{"jma-bosai": "minTemp"}` | - | - |
| `min_temp_time` | `union` | `True` | UTC RFC3339 timestamp for the minimum air temperature time from the JMA Bosai per-station minTempTime object. JMA publishes hour and minute in local time; the bridge resolves the date relative to the observation timestamp and converts it to UTC. | altnames=`{"jma-bosai": "minTempTime"}` | - | - |
| `precipitation10m` | `union` | `True` | Precipitation amount for the previous 10 minutes, expressed in millimeters of liquid water equivalent. JMA documents precipitation as rain or snow amount melted to water and displayed in 0.5 mm units. | unit=`millimeter`<br>altnames=`{"jma-bosai": "precipitation10m"}` | - | - |
| `precipitation10m_qc_flag` | `union` | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | - | - | - |
| `precipitation1h` | `union` | `True` | Precipitation amount for the previous 1 hour, expressed in millimeters of liquid water equivalent. | unit=`millimeter`<br>altnames=`{"jma-bosai": "precipitation1h"}` | - | - |
| `precipitation1h_qc_flag` | `union` | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | - | - | - |
| `precipitation3h` | `union` | `True` | Precipitation amount for the previous 3 hours, expressed in millimeters of liquid water equivalent. | unit=`millimeter`<br>altnames=`{"jma-bosai": "precipitation3h"}` | - | - |
| `precipitation3h_qc_flag` | `union` | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | - | - | - |
| `precipitation24h` | `union` | `True` | Precipitation amount for the previous 24 hours, expressed in millimeters of liquid water equivalent. | unit=`millimeter`<br>altnames=`{"jma-bosai": "precipitation24h"}` | - | - |
| `precipitation24h_qc_flag` | `union` | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | - | - | - |
| `sun10m` | `union` | `True` | Sunshine duration for the previous 10 minutes, expressed in minutes. JMA publishes this ten-minute map field in minutes, so its unit intentionally differs from the hourly sun1h field. | unit=`minute`<br>altnames=`{"jma-bosai": "sun10m"}` | - | - |
| `sun10m_qc_flag` | `union` | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | - | - | - |
| `sun1h` | `union` | `True` | Sunshine duration for the previous 1 hour, expressed in hours as published by the Bosai AMeDAS map. JMA publishes this hourly field in hours, so its unit intentionally differs from the ten-minute sun10m field. | unit=`hour`<br>altnames=`{"jma-bosai": "sun1h"}` | - | - |
| `sun1h_qc_flag` | `union` | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | - | - | - |
| `snow` | `union` | `True` | Snow depth, the height of snow on the ground, expressed in centimeters. JMA documents snow depth as the height from the ground surface to the top of accumulated snow. | unit=`centimeter`<br>altnames=`{"jma-bosai": "snow"}` | - | - |
| `snow_qc_flag` | `union` | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | - | - | - |
| `snow1h` | `union` | `True` | Change in snow depth over the previous 1 hour, expressed in centimeters. | unit=`centimeter`<br>altnames=`{"jma-bosai": "snow1h"}` | - | - |
| `snow1h_qc_flag` | `union` | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | - | - | - |
| `snow6h` | `union` | `True` | Change in snow depth over the previous 6 hours, expressed in centimeters. | unit=`centimeter`<br>altnames=`{"jma-bosai": "snow6h"}` | - | - |
| `snow6h_qc_flag` | `union` | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | - | - | - |
| `snow12h` | `union` | `True` | Change in snow depth over the previous 12 hours, expressed in centimeters. | unit=`centimeter`<br>altnames=`{"jma-bosai": "snow12h"}` | - | - |
| `snow12h_qc_flag` | `union` | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | - | - | - |
| `snow24h` | `union` | `True` | Change in snow depth over the previous 24 hours, expressed in centimeters. | unit=`centimeter`<br>altnames=`{"jma-bosai": "snow24h"}` | - | - |
| `snow24h_qc_flag` | `union` | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | - | - | - |
| `visibility` | `union` | `True` | Horizontal visibility where published by JMA Bosai AMeDAS, expressed in meters. | unit=`meter`<br>altnames=`{"jma-bosai": "visibility"}` | - | - |
| `visibility_qc_flag` | `union` | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | - | - | - |
| `cloud` | `union` | `True` | Cloud amount code from JMA Bosai AMeDAS where available. The Bosai map exposes this as a numeric measurement tuple for stations that publish cloud information. | altnames=`{"jma-bosai": "cloud"}` | - | - |
| `cloud_qc_flag` | `union` | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | - | - | - |
| `weather` | `union` | `True` | Present weather code from JMA Bosai AMeDAS where available. The Bosai map exposes this as a numeric measurement tuple for stations that publish weather information. | altnames=`{"jma-bosai": "weather"}` | - | - |
| `weather_qc_flag` | `union` | `True` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | - | - | - |

### Schemagroup `JP.JMA.Amedas.avro`
<a id="schemagroup-jpjmaamedasavro"></a>

#### Schema `JP.JMA.Amedas.Station`
<a id="schema-jpjmaamedasstation"></a>

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Station |
| Namespace | JP.JMA.Amedas |
| Type | `record` |
| Doc | Reference event for one JMA AMeDAS station from the Bosai amedastable.json station table, including names, geodetic position, elevation, station capability tier, and measurement capability bitmask. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_code` | `string` | JMA AMeDAS five-digit station code used as the stable identifier in the Bosai AMeDAS station table and observation map. | `-` |
| `kj_name` | `string` | Japanese kanji station name from the JMA AMeDAS station table (kjName), used by the Bosai web application for Japanese display labels. | `-` |
| `kana` | `string` | Japanese kana station reading from the JMA AMeDAS station table (knName in live payloads, kana in older examples), used by the Bosai web application for phonetic Japanese display. | `-` |
| `en_name` | `string` | English station name from the JMA AMeDAS station table. | `-` |
| `latitude` | `double` | Station latitude in WGS84 decimal degrees. The JMA station table publishes latitude as [degrees, minutes]; the bridge converts it with degrees + minutes/60. | `-` |
| `longitude` | `double` | Station longitude in WGS84 decimal degrees. The JMA station table publishes longitude as [degrees, minutes]; the bridge converts it with degrees + minutes/60. | `-` |
| `altitude_m` | `double` | Station elevation above sea level in meters from the JMA station table alt field. | `-` |
| `station_type` | `string` | JMA AMeDAS station capability tier as published in the station table. The tier controls which measurements may be emitted for a station. | `-` |
| `elems_bitmask` | `string` | JMA Bosai AMeDAS element bitmask string from the station table. Each non-zero character indicates that the corresponding station capability is enabled in the Bosai web application. | `-` |
| `enabled_measurements` | array of `string` | Measurement capability names derived by the bridge from the JMA elems_bitmask. The values describe which observation families the station can emit, such as precipitation, wind, temperature, sunshine_duration, snow_depth, humidity, pressure, or visibility. | `-` |

#### Schema `JP.JMA.Amedas.Observation`
<a id="schema-jpjmaamedasobservation"></a>

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Observation |
| Namespace | JP.JMA.Amedas |
| Type | `record` |
| Doc | Telemetry event for one JMA AMeDAS station observation in a ten-minute Bosai map snapshot. Each measurement value is nullable because JMA publishes different fields by station capability and by observation availability. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_code` | `string` | JMA AMeDAS five-digit station code used as the stable identifier in the Bosai AMeDAS station table and observation map. | `-` |
| `observed_at` | `string` | Observation snapshot timestamp converted from JMA latest_time.txt to UTC and serialized as RFC3339. AMeDAS map snapshots are published every ten minutes. | `-` |
| `observed_at_local` | `string` | Original JMA latest_time.txt timestamp in Japan Standard Time with +09:00 offset, serialized as RFC3339. | `-` |
| `temp` | `null` \| `double` | Air temperature observed automatically by AMeDAS, expressed in degrees Celsius. JMA documents temperature as air temperature displayed in 0.1 °C units. | `-` |
| `temp_qc_flag` | `null` \| `int` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | `-` |
| `humidity` | `null` \| `double` | Relative humidity of the air observed automatically by AMeDAS, expressed as percent. JMA documents humidity as relative humidity displayed in 1 percent units. | `-` |
| `humidity_qc_flag` | `null` \| `int` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | `-` |
| `pressure` | `null` \| `double` | Station pressure from JMA Bosai AMeDAS where available, expressed in hectopascals. | `-` |
| `pressure_qc_flag` | `null` \| `int` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | `-` |
| `normal_pressure` | `null` \| `double` | Sea-level adjusted pressure (normalPressure in the Bosai payload) where available, expressed in hectopascals. | `-` |
| `normal_pressure_qc_flag` | `null` \| `int` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | `-` |
| `wind_speed` | `null` \| `double` | Wind speed averaged over the ten minutes before observation time, expressed in meters per second. JMA documents wind speed as the speed of the wind over the preceding ten minutes. | `-` |
| `wind_speed_qc_flag` | `null` \| `int` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | `-` |
| `wind_direction` | `null` \| `double` | Wind direction from which the wind blows, converted by the bridge from JMA 16-direction codes to degrees clockwise from true north. | `-` |
| `wind_direction_qc_flag` | `null` \| `int` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | `-` |
| `wind_gust` | `null` \| `double` | Maximum instantaneous wind speed (gust) for the observation interval from the JMA Bosai per-station point payload, expressed in meters per second. The bridge enriches map observations with this value only for configured point-detail stations. | `-` |
| `wind_gust_qc_flag` | `null` \| `int` | JMA quality-control flag accompanying the gust tuple in the Bosai AMeDAS per-station point payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA non-normal quality states as represented by the Bosai web application. | `-` |
| `wind_gust_direction` | `null` \| `double` | Direction from which the maximum instantaneous wind gust blew, converted by the bridge from JMA 16-direction codes in gustDirection to degrees clockwise from true north. The field is present only when point-detail enrichment is configured and JMA publishes a gust direction. | `-` |
| `wind_gust_time` | `null` \| `string` | UTC RFC3339 timestamp for the maximum instantaneous wind gust time from the JMA Bosai per-station gustTime object. JMA publishes hour and minute in local time; the bridge resolves the date relative to the observation timestamp and converts it to UTC. | `-` |
| `max_temp` | `null` \| `double` | Maximum air temperature from the JMA Bosai per-station point payload, expressed in degrees Celsius. The bridge enriches map observations with this value only for configured point-detail stations. | `-` |
| `max_temp_time` | `null` \| `string` | UTC RFC3339 timestamp for the maximum air temperature time from the JMA Bosai per-station maxTempTime object. JMA publishes hour and minute in local time; the bridge resolves the date relative to the observation timestamp and converts it to UTC. | `-` |
| `min_temp` | `null` \| `double` | Minimum air temperature from the JMA Bosai per-station point payload, expressed in degrees Celsius. The bridge enriches map observations with this value only for configured point-detail stations. | `-` |
| `min_temp_time` | `null` \| `string` | UTC RFC3339 timestamp for the minimum air temperature time from the JMA Bosai per-station minTempTime object. JMA publishes hour and minute in local time; the bridge resolves the date relative to the observation timestamp and converts it to UTC. | `-` |
| `precipitation10m` | `null` \| `double` | Precipitation amount for the previous 10 minutes, expressed in millimeters of liquid water equivalent. JMA documents precipitation as rain or snow amount melted to water and displayed in 0.5 mm units. | `-` |
| `precipitation10m_qc_flag` | `null` \| `int` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | `-` |
| `precipitation1h` | `null` \| `double` | Precipitation amount for the previous 1 hour, expressed in millimeters of liquid water equivalent. | `-` |
| `precipitation1h_qc_flag` | `null` \| `int` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | `-` |
| `precipitation3h` | `null` \| `double` | Precipitation amount for the previous 3 hours, expressed in millimeters of liquid water equivalent. | `-` |
| `precipitation3h_qc_flag` | `null` \| `int` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | `-` |
| `precipitation24h` | `null` \| `double` | Precipitation amount for the previous 24 hours, expressed in millimeters of liquid water equivalent. | `-` |
| `precipitation24h_qc_flag` | `null` \| `int` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | `-` |
| `sun10m` | `null` \| `double` | Sunshine duration for the previous 10 minutes, expressed in minutes. JMA publishes this ten-minute map field in minutes, so its unit intentionally differs from the hourly sun1h field. | `-` |
| `sun10m_qc_flag` | `null` \| `int` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | `-` |
| `sun1h` | `null` \| `double` | Sunshine duration for the previous 1 hour, expressed in hours as published by the Bosai AMeDAS map. JMA publishes this hourly field in hours, so its unit intentionally differs from the ten-minute sun10m field. | `-` |
| `sun1h_qc_flag` | `null` \| `int` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | `-` |
| `snow` | `null` \| `double` | Snow depth, the height of snow on the ground, expressed in centimeters. JMA documents snow depth as the height from the ground surface to the top of accumulated snow. | `-` |
| `snow_qc_flag` | `null` \| `int` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | `-` |
| `snow1h` | `null` \| `double` | Change in snow depth over the previous 1 hour, expressed in centimeters. | `-` |
| `snow1h_qc_flag` | `null` \| `int` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | `-` |
| `snow6h` | `null` \| `double` | Change in snow depth over the previous 6 hours, expressed in centimeters. | `-` |
| `snow6h_qc_flag` | `null` \| `int` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | `-` |
| `snow12h` | `null` \| `double` | Change in snow depth over the previous 12 hours, expressed in centimeters. | `-` |
| `snow12h_qc_flag` | `null` \| `int` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | `-` |
| `snow24h` | `null` \| `double` | Change in snow depth over the previous 24 hours, expressed in centimeters. | `-` |
| `snow24h_qc_flag` | `null` \| `int` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | `-` |
| `visibility` | `null` \| `double` | Horizontal visibility where published by JMA Bosai AMeDAS, expressed in meters. | `-` |
| `visibility_qc_flag` | `null` \| `int` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | `-` |
| `cloud` | `null` \| `double` | Cloud amount code from JMA Bosai AMeDAS where available. The Bosai map exposes this as a numeric measurement tuple for stations that publish cloud information. | `-` |
| `cloud_qc_flag` | `null` \| `int` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | `-` |
| `weather` | `null` \| `double` | Present weather code from JMA Bosai AMeDAS where available. The Bosai map exposes this as a numeric measurement tuple for stations that publish weather information. | `-` |
| `weather_qc_flag` | `null` \| `int` | JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application. | `-` |
