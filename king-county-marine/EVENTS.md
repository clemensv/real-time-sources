# King County Marine Bridge Events

MQTT/5.0 transport variants for King County marine station reference data and water-quality readings. The station-only UNS topic tree is maritime/us/wa/king-county/king-county-marine/{station_id}/{event}. Station info and latest water-quality readings are retained with QoS 1 so late subscribers can discover stations and their latest values.

## Table of Contents

- [Registry](#registry)
- [Endpoints](#endpoints)
- [Messagegroups](#messagegroups)
- [Schemagroups](#schemagroups)

---

## Registry

| Field | Value |
| --- | --- |
| Endpoints | 2 |
| Messagegroups | 2 |
| Schemagroups | 1 |

## Endpoints

### Endpoint `US.WA.KingCounty.Marine.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`US.WA.KingCounty.Marine`](#messagegroup-uswakingcountymarine) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `king-county-marine` |
| Kafka key | `{station_id}` |
| Deployed | False |

### Endpoint `US.WA.KingCounty.Marine.Mqtt`

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 binary-mode CloudEvents producer for the King County Marine UNS topic tree. |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`US.WA.KingCounty.Marine.mqtt`](#messagegroup-uswakingcountymarinemqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

## Messagegroups

### Messagegroup `US.WA.KingCounty.Marine`
<a id="messagegroup-uswakingcountymarine"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `US.WA.KingCounty.Marine.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `US.WA.KingCounty.Marine.Station`
<a id="message-uswakingcountymarinestation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/US.WA.KingCounty.Marine.jstruct/schemas/US.WA.KingCounty.Marine.Station`](#schema-uswakingcountymarinestation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `US.WA.KingCounty.Marine.Station` |
| `source` |  | `string` | `False` | `https://data.kingcounty.gov/` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `US.WA.KingCounty.Marine.Kafka` | `KAFKA` | topic `king-county-marine`; key `{station_id}` |

#### Message `US.WA.KingCounty.Marine.WaterQualityReading`
<a id="message-uswakingcountymarinewaterqualityreading"></a>

| Field | Value |
| --- | --- |
| Name | WaterQualityReading |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/US.WA.KingCounty.Marine.jstruct/schemas/US.WA.KingCounty.Marine.WaterQualityReading`](#schema-uswakingcountymarinewaterqualityreading) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `US.WA.KingCounty.Marine.WaterQualityReading` |
| `source` |  | `string` | `False` | `https://data.kingcounty.gov/` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `US.WA.KingCounty.Marine.Kafka` | `KAFKA` | topic `king-county-marine`; key `{station_id}` |

### Messagegroup `US.WA.KingCounty.Marine.mqtt`
<a id="messagegroup-uswakingcountymarinemqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 transport variants for King County marine station reference data and water-quality readings. The station-only UNS topic tree is maritime/us/wa/king-county/king-county-marine/{station_id}/{event}. Station info and latest water-quality readings are retained with QoS 1 so late subscribers can discover stations and their latest values. |
| Transport bindings | `US.WA.KingCounty.Marine.Mqtt` (MQTT/5.0) |
| Messages | 2 |

#### Message `US.WA.KingCounty.Marine.mqtt.Station`
<a id="message-uswakingcountymarinemqttstation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/US.WA.KingCounty.Marine.jstruct/schemas/US.WA.KingCounty.Marine.Station`](#schema-uswakingcountymarinestation) |
| Base message chain | `/messagegroups/US.WA.KingCounty.Marine/messages/US.WA.KingCounty.Marine.Station` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `US.WA.KingCounty.Marine.Station` |
| `source` |  | `string` | `False` | `https://data.kingcounty.gov/` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `US.WA.KingCounty.Marine.Mqtt` | `MQTT/5.0` | topic `maritime/us/wa/king-county/king-county-marine/{station_id}/info` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `maritime/us/wa/king-county/king-county-marine/{station_id}/info` |
| QoS | 1 |
| Retain | True |

#### Message `US.WA.KingCounty.Marine.mqtt.WaterQualityReading`
<a id="message-uswakingcountymarinemqttwaterqualityreading"></a>

| Field | Value |
| --- | --- |
| Name | WaterQualityReading |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/US.WA.KingCounty.Marine.jstruct/schemas/US.WA.KingCounty.Marine.WaterQualityReading`](#schema-uswakingcountymarinewaterqualityreading) |
| Base message chain | `/messagegroups/US.WA.KingCounty.Marine/messages/US.WA.KingCounty.Marine.WaterQualityReading` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `US.WA.KingCounty.Marine.WaterQualityReading` |
| `source` |  | `string` | `False` | `https://data.kingcounty.gov/` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `US.WA.KingCounty.Marine.Mqtt` | `MQTT/5.0` | topic `maritime/us/wa/king-county/king-county-marine/{station_id}/water-quality` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `maritime/us/wa/king-county/king-county-marine/{station_id}/water-quality` |
| QoS | 1 |
| Retain | True |
| Additional protocol metadata | `{"message_expiry_interval": 3600}` |

## Schemagroups

### Schemagroup `US.WA.KingCounty.Marine.jstruct`
<a id="schemagroup-uswakingcountymarinejstruct"></a>

#### Schema `US.WA.KingCounty.Marine.Station`
<a id="schema-uswakingcountymarinestation"></a>

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
| $id | `https://github.com/clemensv/real-time-sources/king-county-marine/schemas/US.WA.KingCounty.Marine.Station.json` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Station`
<a id="schema-node-station"></a>

Reference metadata for one active King County buoy or mooring raw-data dataset.

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/king-county-marine/schemas/US.WA.KingCounty.Marine.Station.json` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | Stable bridge identifier for the buoy or mooring dataset. | - | - | - |
| `station_name` | `string` | `True` | Human-readable station name derived from the dataset title. | - | - | - |
| `dataset_id` | `string` | `True` | Socrata dataset identifier for the source dataset. | - | - | - |
| `dataset_name` | `string` | `True` | Original King County dataset title. | - | - | - |
| `dataset_url` | `string` | `True` | Dataset page URL on data.kingcounty.gov. | - | - | - |
| `sensor_level` | `string` | `True` | Sensor position classification inferred from the dataset title, such as surface, bottom, or water-column. | - | - | - |
| `latitude` | `union` | `False` | Station latitude in decimal degrees north, parsed from the dataset description. | - | - | - |
| `longitude` | `union` | `False` | Station longitude in decimal degrees east of Greenwich; King County locations are negative because they lie west of Greenwich. | - | - | - |

#### Schema `US.WA.KingCounty.Marine.WaterQualityReading`
<a id="schema-uswakingcountymarinewaterqualityreading"></a>

| Field | Value |
| --- | --- |
| Name | WaterQualityReading |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/king-county-marine/schemas/US.WA.KingCounty.Marine.WaterQualityReading.json` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `WaterQualityReading`
<a id="schema-node-waterqualityreading"></a>

Normalized King County buoy or mooring reading carrying the documented water-quality and weather measurements published by the current raw-data datasets.

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/king-county-marine/schemas/US.WA.KingCounty.Marine.WaterQualityReading.json` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | Stable bridge identifier for the buoy or mooring dataset. | - | - | - |
| `station_name` | `string` | `True` | Human-readable station name derived from the dataset title. | - | - | - |
| `observation_time` | `string` | `True` | Observation timestamp normalized to UTC ISO 8601 form. | - | - | - |
| `water_temperature_c` | `union` | `False` | Water temperature in degrees Celsius. | unit=`Cel` symbol=`Â°C` | - | - |
| `conductivity_s_m` | `union` | `False` | Electrical conductivity in siemens per meter. | unit=`S/m` symbol=`S/m` | - | - |
| `pressure_dbar` | `union` | `False` | Water pressure in decibar as published by the raw datasets. | unit=`dbar` symbol=`dbar` | - | - |
| `dissolved_oxygen_mg_l` | `union` | `False` | Dissolved oxygen concentration in milligrams per liter. | unit=`mg/L` symbol=`mg/L` | - | - |
| `ph` | `union` | `False` | Measured pH value. | - | - | - |
| `chlorophyll_ug_l` | `union` | `False` | Chlorophyll fluorescence or chlorophyll concentration in micrograms per liter. | unit=`ug/L` symbol=`Âµg/L` | - | - |
| `turbidity_ntu` | `union` | `False` | Turbidity in nephelometric turbidity units. | unit=`NTU` symbol=`NTU` | - | - |
| `chlorophyll_stddev_ug_l` | `union` | `False` | Standard deviation of chlorophyll fluorescence in micrograms per liter. | unit=`ug/L` symbol=`Âµg/L` | - | - |
| `turbidity_stddev_ntu` | `union` | `False` | Standard deviation of turbidity in nephelometric turbidity units. | unit=`NTU` symbol=`NTU` | - | - |
| `salinity_psu` | `union` | `False` | Salinity in practical salinity units. | unit=`PSU` symbol=`PSU` | - | - |
| `specific_conductivity_s_m` | `union` | `False` | Specific conductivity in siemens per meter. | unit=`S/m` symbol=`S/m` | - | - |
| `dissolved_oxygen_saturation_pct` | `union` | `False` | Dissolved oxygen saturation as a percentage. | unit=`P1` symbol=`%` | - | - |
| `nitrate_umol` | `union` | `False` | Nitrate or nitrate-plus-nitrite concentration in micromoles. | unit=`umol` symbol=`Âµmol` | - | - |
| `nitrate_mg_l` | `union` | `False` | Nitrate or nitrate-plus-nitrite concentration in milligrams per liter. | unit=`mg/L` symbol=`mg/L` | - | - |
| `wind_direction_deg` | `union` | `False` | Wind direction in degrees at the buoy surface. | unit=`deg` symbol=`Â°` | - | - |
| `wind_speed_m_s` | `union` | `False` | Wind speed in meters per second at the buoy surface. | unit=`m/s` symbol=`m/s` | - | - |
| `photosynthetically_active_radiation_umol_s_m2` | `union` | `False` | Photosynthetically active radiation in micromoles per second per square meter. | unit=`umol/s/m2` symbol=`Âµmol/s/mÂ²` | - | - |
| `air_temperature_f` | `union` | `False` | Air temperature in degrees Fahrenheit. | unit=`[degF]` symbol=`Â°F` | - | - |
| `air_humidity_pct` | `union` | `False` | Relative humidity percentage. | unit=`P1` symbol=`%` | - | - |
| `air_pressure_in_hg` | `union` | `False` | Air pressure in inches of mercury. | unit=`[in_i'Hg]` symbol=`inHg` | - | - |
| `system_battery_v` | `union` | `False` | System battery voltage in volts. | unit=`V` symbol=`V` | - | - |
| `sensor_battery_v` | `union` | `False` | Sensor or sonde battery voltage in volts. | unit=`V` symbol=`V` | - | - |
