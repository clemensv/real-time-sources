# Waterinfo VMM (Belgium/Flanders) Water Level Bridge Events

This project bridges water level data from the Belgian [Waterinfo.be](https://waterinfo.vlaanderen.be/) KIWIS API (VMM provider) to Apache Kafka, emitting CloudEvents.

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

### Endpoint `BE.Vlaanderen.Waterinfo.VMM.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`BE.Vlaanderen.Waterinfo.VMM`](#messagegroup-bevlaanderenwaterinfovmm) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `waterinfo-vmm` |
| Kafka key | `{station_no}` |
| Deployed | False |

## Messagegroups

### Messagegroup `BE.Vlaanderen.Waterinfo.VMM`
<a id="messagegroup-bevlaanderenwaterinfovmm"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `BE.Vlaanderen.Waterinfo.VMM.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `BE.Vlaanderen.Waterinfo.VMM.Station`
<a id="message-bevlaanderenwaterinfovmmstation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/BE.Vlaanderen.Waterinfo.VMM.jstruct/schemas/BE.Vlaanderen.Waterinfo.VMM.Station`](#schema-bevlaanderenwaterinfovmmstation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `BE.Vlaanderen.Waterinfo.VMM.Station` |
| `source` |  | `string` | `False` | `https://waterinfo.vlaanderen.be` |
| `subject` |  | `uritemplate` | `False` | `{station_no}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `BE.Vlaanderen.Waterinfo.VMM.Kafka` | `KAFKA` | topic `waterinfo-vmm`; key `{station_no}` |

#### Message `BE.Vlaanderen.Waterinfo.VMM.WaterLevelReading`
<a id="message-bevlaanderenwaterinfovmmwaterlevelreading"></a>

| Field | Value |
| --- | --- |
| Name | WaterLevelReading |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/BE.Vlaanderen.Waterinfo.VMM.jstruct/schemas/BE.Vlaanderen.Waterinfo.VMM.WaterLevelReading`](#schema-bevlaanderenwaterinfovmmwaterlevelreading) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `BE.Vlaanderen.Waterinfo.VMM.WaterLevelReading` |
| `source` |  | `string` | `False` | `https://waterinfo.vlaanderen.be` |
| `subject` |  | `uritemplate` | `False` | `{station_no}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `BE.Vlaanderen.Waterinfo.VMM.Kafka` | `KAFKA` | topic `waterinfo-vmm`; key `{station_no}` |

## Schemagroups

### Schemagroup `BE.Vlaanderen.Waterinfo.VMM.jstruct`
<a id="schemagroup-bevlaanderenwaterinfovmmjstruct"></a>

#### Schema `BE.Vlaanderen.Waterinfo.VMM.Station`
<a id="schema-bevlaanderenwaterinfovmmstation"></a>

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
| $id | `https://example.com/schemas/BE/Vlaanderen/Waterinfo/VMM/Station` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Station`
<a id="schema-node-station"></a>

Station

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/BE/Vlaanderen/Waterinfo/VMM/Station` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_no` | `string` | `True` |  | - | - | - |
| `station_name` | `string` | `True` |  | - | - | - |
| `station_id` | `string` | `False` |  | - | - | - |
| `station_latitude` | `double` | `True` |  | - | - | - |
| `station_longitude` | `double` | `True` |  | - | - | - |
| `river_name` | `union` | `False` |  | - | - | - |
| `stationparameter_name` | `union` | `False` |  | - | - | - |
| `ts_id` | `union` | `False` |  | - | - | - |
| `ts_unitname` | `union` | `False` |  | - | - | - |

#### Schema `BE.Vlaanderen.Waterinfo.VMM.WaterLevelReading`
<a id="schema-bevlaanderenwaterinfovmmwaterlevelreading"></a>

| Field | Value |
| --- | --- |
| Name | WaterLevelReading |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/BE/Vlaanderen/Waterinfo/VMM/WaterLevelReading` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `WaterLevelReading`
<a id="schema-node-waterlevelreading"></a>

WaterLevelReading

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/BE/Vlaanderen/Waterinfo/VMM/WaterLevelReading` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `ts_id` | `string` | `True` |  | - | - | - |
| `station_no` | `string` | `True` |  | - | - | - |
| `station_name` | `string` | `False` |  | - | - | - |
| `timestamp` | `datetime` | `True` |  | - | - | - |
| `value` | `double` | `True` |  | - | - | - |
| `unit_name` | `string` | `False` |  | - | - | - |
| `parameter_name` | `string` | `False` |  | - | - | - |

### Schemagroup `BE.Vlaanderen.Waterinfo.VMM.avro`
<a id="schemagroup-bevlaanderenwaterinfovmmavro"></a>

#### Schema `BE.Vlaanderen.Waterinfo.VMM.Station`
<a id="schema-bevlaanderenwaterinfovmmstation"></a>

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
| Namespace | BE.Vlaanderen.Waterinfo.VMM |
| Type | `record` |
| Doc | Station |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_no` | `string` |  | `-` |
| `station_name` | `string` |  | `-` |
| `station_id` | `null` \| `string` |  | `-` |
| `station_latitude` | `double` |  | `-` |
| `station_longitude` | `double` |  | `-` |
| `river_name` | `null` \| `string` |  | `-` |
| `stationparameter_name` | `null` \| `string` |  | `-` |
| `ts_id` | `null` \| `string` |  | `-` |
| `ts_unitname` | `null` \| `string` |  | `-` |

#### Schema `BE.Vlaanderen.Waterinfo.VMM.WaterLevelReading`
<a id="schema-bevlaanderenwaterinfovmmwaterlevelreading"></a>

| Field | Value |
| --- | --- |
| Name | WaterLevelReading |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | WaterLevelReading |
| Namespace | BE.Vlaanderen.Waterinfo.VMM |
| Type | `record` |
| Doc | WaterLevelReading |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `ts_id` | `string` |  | `-` |
| `station_no` | `string` |  | `-` |
| `station_name` | `null` \| `string` |  | `-` |
| `timestamp` | `string` |  | `-` |
| `value` | `double` |  | `-` |
| `unit_name` | `null` \| `string` |  | `-` |
| `parameter_name` | `null` \| `string` |  | `-` |
