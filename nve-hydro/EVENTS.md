# NVE Hydrology Bridge Usage Guide Events

MQTT/5.0 transport variants of the NVE Hydrology CloudEvents, mapping each message to a retained, QoS-1 Unified Namespace topic under hydro/no/nve/nve-hydro/{river_name}/{station_id}/... The {river_name} placeholder is sourced from the NVE HydAPI station catalog field 'riverName' (Norwegian: 'Vassdrag', e.g. 'Glomma', 'Drammenselva') and normalized by the bridge to lowercase kebab-case before publishing so subscribers can wildcard whole rivers (e.g. hydro/no/nve/nve-hydro/glomma/+/water-level).

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
| Schemagroups | 2 |

## Endpoints

### Endpoint `NO.NVE.Hydrology.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`NO.NVE.Hydrology`](#messagegroup-nonvehydrology) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `nve-hydro` |
| Kafka key | `{station_id}` |
| Deployed | False |

### Endpoint `NO.NVE.Hydrology.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`NO.NVE.Hydrology.mqtt`](#messagegroup-nonvehydrologymqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

## Messagegroups

### Messagegroup `NO.NVE.Hydrology`
<a id="messagegroup-nonvehydrology"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `NO.NVE.Hydrology.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `NO.NVE.Hydrology.Station`
<a id="message-nonvehydrologystation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NO.NVE.Hydrology.jstruct/schemas/NO.NVE.Hydrology.Station`](#schema-nonvehydrologystation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NO.NVE.Hydrology.Station` |
| `source` |  | `string` | `False` | `https://hydapi.nve.no` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NO.NVE.Hydrology.Kafka` | `KAFKA` | topic `nve-hydro`; key `{station_id}` |

#### Message `NO.NVE.Hydrology.WaterLevelObservation`
<a id="message-nonvehydrologywaterlevelobservation"></a>

| Field | Value |
| --- | --- |
| Name | WaterLevelObservation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NO.NVE.Hydrology.jstruct/schemas/NO.NVE.Hydrology.WaterLevelObservation`](#schema-nonvehydrologywaterlevelobservation) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NO.NVE.Hydrology.WaterLevelObservation` |
| `source` |  | `string` | `False` | `https://hydapi.nve.no` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NO.NVE.Hydrology.Kafka` | `KAFKA` | topic `nve-hydro`; key `{station_id}` |

### Messagegroup `NO.NVE.Hydrology.mqtt`
<a id="messagegroup-nonvehydrologymqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 transport variants of the NVE Hydrology CloudEvents, mapping each message to a retained, QoS-1 Unified Namespace topic under hydro/no/nve/nve-hydro/{river_name}/{station_id}/... The {river_name} placeholder is sourced from the NVE HydAPI station catalog field 'riverName' (Norwegian: 'Vassdrag', e.g. 'Glomma', 'Drammenselva') and normalized by the bridge to lowercase kebab-case before publishing so subscribers can wildcard whole rivers (e.g. hydro/no/nve/nve-hydro/glomma/+/water-level). |
| Transport bindings | `NO.NVE.Hydrology.Mqtt` (MQTT/5.0) |
| Messages | 2 |

#### Message `NO.NVE.Hydrology.mqtt.Station`
<a id="message-nonvehydrologymqttstation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NO.NVE.Hydrology.jstruct/schemas/NO.NVE.Hydrology.Station`](#schema-nonvehydrologystation) |
| Base message chain | `/messagegroups/NO.NVE.Hydrology/messages/NO.NVE.Hydrology.Station` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NO.NVE.Hydrology.Station` |
| `source` |  | `string` | `False` | `https://hydapi.nve.no` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NO.NVE.Hydrology.Mqtt` | `MQTT/5.0` | topic `hydro/no/nve/nve-hydro/{river_name}/{station_id}/info` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/no/nve/nve-hydro/{river_name}/{station_id}/info` |
| QoS | 1 |
| Retain | True |

#### Message `NO.NVE.Hydrology.mqtt.WaterLevelObservation`
<a id="message-nonvehydrologymqttwaterlevelobservation"></a>

| Field | Value |
| --- | --- |
| Name | WaterLevelObservation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NO.NVE.Hydrology.jstruct/schemas/NO.NVE.Hydrology.WaterLevelObservation`](#schema-nonvehydrologywaterlevelobservation) |
| Base message chain | `/messagegroups/NO.NVE.Hydrology/messages/NO.NVE.Hydrology.WaterLevelObservation` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NO.NVE.Hydrology.WaterLevelObservation` |
| `source` |  | `string` | `False` | `https://hydapi.nve.no` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NO.NVE.Hydrology.Mqtt` | `MQTT/5.0` | topic `hydro/no/nve/nve-hydro/{river_name}/{station_id}/water-level` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/no/nve/nve-hydro/{river_name}/{station_id}/water-level` |
| QoS | 1 |
| Retain | True |

## Schemagroups

### Schemagroup `NO.NVE.Hydrology.jstruct`
<a id="schemagroup-nonvehydrologyjstruct"></a>

#### Schema `NO.NVE.Hydrology.Station`
<a id="schema-nonvehydrologystation"></a>

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
| $id | `https://example.com/schemas/NO/NVE/Hydrology/Station` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Station`
<a id="schema-node-station"></a>

Station

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/NO/NVE/Hydrology/Station` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` |  | - | - | - |
| `station_name` | `string` | `True` |  | - | - | - |
| `river_name` | `string` | `False` |  | - | - | - |
| `latitude` | `double` | `True` |  | - | - | - |
| `longitude` | `double` | `True` |  | - | - | - |
| `masl` | `double` | `False` |  | - | - | - |
| `council_name` | `string` | `False` |  | - | - | - |
| `county_name` | `string` | `False` |  | - | - | - |
| `drainage_basin_area` | `double` | `False` |  | - | - | - |

#### Schema `NO.NVE.Hydrology.WaterLevelObservation`
<a id="schema-nonvehydrologywaterlevelobservation"></a>

| Field | Value |
| --- | --- |
| Name | WaterLevelObservation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/NO/NVE/Hydrology/WaterLevelObservation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `WaterLevelObservation`
<a id="schema-node-waterlevelobservation"></a>

WaterLevelObservation

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/NO/NVE/Hydrology/WaterLevelObservation` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` |  | - | - | - |
| `river_name` | `string` | `True` | Name of the river the station observes (NVE HydAPI 'riverName' field, in Norwegian 'Vassdrag', e.g. 'Glomma', 'Drammenselva'). Sourced by the bridge from the station catalog (https://hydapi.nve.no/api/v1/Stations) and propagated onto every observation so subscribers do not need an out-of-band catalog join to route by river. Used as the {river_name} segment of the MQTT/UNS topic and normalized to lowercase kebab-case before publishing. | - | - | - |
| `water_level` | `double` | `False` |  | - | - | - |
| `water_level_unit` | `string` | `False` |  | - | - | - |
| `water_level_timestamp` | `datetime` | `False` |  | - | - | - |
| `discharge` | `double` | `False` |  | - | - | - |
| `discharge_unit` | `string` | `False` |  | - | - | - |
| `discharge_timestamp` | `datetime` | `False` |  | - | - | - |

### Schemagroup `NO.NVE.Hydrology.avro`
<a id="schemagroup-nonvehydrologyavro"></a>

#### Schema `NO.NVE.Hydrology.Station`
<a id="schema-nonvehydrologystation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Station |
| Namespace | NO.NVE.Hydrology |
| Type | `record` |
| Doc | Station |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` |  | `-` |
| `station_name` | `string` |  | `-` |
| `river_name` | `null` \| `string` |  | `-` |
| `latitude` | `double` |  | `-` |
| `longitude` | `double` |  | `-` |
| `masl` | `null` \| `double` |  | `-` |
| `council_name` | `null` \| `string` |  | `-` |
| `county_name` | `null` \| `string` |  | `-` |
| `drainage_basin_area` | `null` \| `double` |  | `-` |

#### Schema `NO.NVE.Hydrology.WaterLevelObservation`
<a id="schema-nonvehydrologywaterlevelobservation"></a>

| Field | Value |
| --- | --- |
| Name | WaterLevelObservation |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | WaterLevelObservation |
| Namespace | NO.NVE.Hydrology |
| Type | `record` |
| Doc | WaterLevelObservation |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` |  | `-` |
| `river_name` | `string` | Name of the river the station observes (NVE HydAPI 'riverName' / Norwegian 'Vassdrag'). Sourced from the station catalog and propagated to telemetry so consumers can route by river without a separate catalog join. | `-` |
| `water_level` | `null` \| `double` |  | `-` |
| `water_level_unit` | `null` \| `string` |  | `-` |
| `water_level_timestamp` | `null` \| `string` |  | `-` |
| `discharge` | `null` \| `double` |  | `-` |
| `discharge_unit` | `null` \| `string` |  | `-` |
| `discharge_timestamp` | `null` \| `string` |  | `-` |
