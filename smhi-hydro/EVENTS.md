# SMHI Hydrological Data Bridge Events

MQTT/5.0 transport variants of the SMHI Hydrology CloudEvents, mapping each message to a retained, QoS-1 Unified Namespace topic under hydro/se/smhi/smhi-hydro/{catchment_name}/{station_id}/... The {catchment_name} placeholder is sourced from the SMHI station catalog (field 'catchmentName', e.g. 'Torneälven', 'Dalälven') and normalized by the bridge to lowercase kebab-case before publishing so subscribers can wildcard whole catchments (e.g. hydro/se/smhi/smhi-hydro/tornealven/+/discharge).

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

### Endpoint `SE.Gov.SMHI.Hydro.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`SE.Gov.SMHI.Hydro`](#messagegroup-segovsmhihydro) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `smhi-hydro` |
| Kafka key | `{station_id}` |
| Deployed | False |

### Endpoint `SE.Gov.SMHI.Hydro.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`SE.Gov.SMHI.Hydro.mqtt`](#messagegroup-segovsmhihydromqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

## Messagegroups

### Messagegroup `SE.Gov.SMHI.Hydro`
<a id="messagegroup-segovsmhihydro"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `SE.Gov.SMHI.Hydro.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `SE.Gov.SMHI.Hydro.Station`
<a id="message-segovsmhihydrostation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/SE.Gov.SMHI.Hydro.jstruct/schemas/SE.Gov.SMHI.Hydro.Station`](#schema-segovsmhihydrostation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `SE.Gov.SMHI.Hydro.Station` |
| `source` |  | `string` | `False` | `https://opendata-download-hydroobs.smhi.se` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `SE.Gov.SMHI.Hydro.Kafka` | `KAFKA` | topic `smhi-hydro`; key `{station_id}` |

#### Message `SE.Gov.SMHI.Hydro.DischargeObservation`
<a id="message-segovsmhihydrodischargeobservation"></a>

| Field | Value |
| --- | --- |
| Name | DischargeObservation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/SE.Gov.SMHI.Hydro.jstruct/schemas/SE.Gov.SMHI.Hydro.DischargeObservation`](#schema-segovsmhihydrodischargeobservation) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `SE.Gov.SMHI.Hydro.DischargeObservation` |
| `source` |  | `string` | `False` | `https://opendata-download-hydroobs.smhi.se` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `SE.Gov.SMHI.Hydro.Kafka` | `KAFKA` | topic `smhi-hydro`; key `{station_id}` |

### Messagegroup `SE.Gov.SMHI.Hydro.mqtt`
<a id="messagegroup-segovsmhihydromqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 transport variants of the SMHI Hydrology CloudEvents, mapping each message to a retained, QoS-1 Unified Namespace topic under hydro/se/smhi/smhi-hydro/{catchment_name}/{station_id}/... The {catchment_name} placeholder is sourced from the SMHI station catalog (field 'catchmentName', e.g. 'Torneälven', 'Dalälven') and normalized by the bridge to lowercase kebab-case before publishing so subscribers can wildcard whole catchments (e.g. hydro/se/smhi/smhi-hydro/tornealven/+/discharge). |
| Transport bindings | `SE.Gov.SMHI.Hydro.Mqtt` (MQTT/5.0) |
| Messages | 2 |

#### Message `SE.Gov.SMHI.Hydro.mqtt.Station`
<a id="message-segovsmhihydromqttstation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/SE.Gov.SMHI.Hydro.jstruct/schemas/SE.Gov.SMHI.Hydro.Station`](#schema-segovsmhihydrostation) |
| Base message chain | `/messagegroups/SE.Gov.SMHI.Hydro/messages/SE.Gov.SMHI.Hydro.Station` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `SE.Gov.SMHI.Hydro.Station` |
| `source` |  | `string` | `False` | `https://opendata-download-hydroobs.smhi.se` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `SE.Gov.SMHI.Hydro.Mqtt` | `MQTT/5.0` | topic `hydro/se/smhi/smhi-hydro/{catchment_name}/{station_id}/info` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/se/smhi/smhi-hydro/{catchment_name}/{station_id}/info` |
| QoS | 1 |
| Retain | True |

#### Message `SE.Gov.SMHI.Hydro.mqtt.DischargeObservation`
<a id="message-segovsmhihydromqttdischargeobservation"></a>

| Field | Value |
| --- | --- |
| Name | DischargeObservation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/SE.Gov.SMHI.Hydro.jstruct/schemas/SE.Gov.SMHI.Hydro.DischargeObservation`](#schema-segovsmhihydrodischargeobservation) |
| Base message chain | `/messagegroups/SE.Gov.SMHI.Hydro/messages/SE.Gov.SMHI.Hydro.DischargeObservation` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `SE.Gov.SMHI.Hydro.DischargeObservation` |
| `source` |  | `string` | `False` | `https://opendata-download-hydroobs.smhi.se` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `SE.Gov.SMHI.Hydro.Mqtt` | `MQTT/5.0` | topic `hydro/se/smhi/smhi-hydro/{catchment_name}/{station_id}/discharge` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/se/smhi/smhi-hydro/{catchment_name}/{station_id}/discharge` |
| QoS | 1 |
| Retain | True |

## Schemagroups

### Schemagroup `SE.Gov.SMHI.Hydro.jstruct`
<a id="schemagroup-segovsmhihydrojstruct"></a>

#### Schema `SE.Gov.SMHI.Hydro.Station`
<a id="schema-segovsmhihydrostation"></a>

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
| $id | `https://example.com/schemas/SE/Gov/SMHI/Hydro/Station` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Station`
<a id="schema-node-station"></a>

Station

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/SE/Gov/SMHI/Hydro/Station` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` |  | - | - | - |
| `name` | `string` | `True` |  | - | - | - |
| `owner` | `string` | `False` |  | - | - | - |
| `measuring_stations` | `string` | `False` |  | - | - | - |
| `region` | `int32` | `False` |  | - | - | - |
| `catchment_name` | `string` | `True` | Name of the catchment area the station belongs to (SMHI 'catchmentName' field, e.g. 'Torneälven', 'Dalälven'). Sourced by the bridge from the SMHI bulk API station catalog. When the catalog has no catchmentName for a station the bridge substitutes the lowercase sentinel 'unknown' so the field stays non-null and the {catchment_name} MQTT topic segment remains populated. Normalized to lowercase kebab-case before publishing. | - | - | - |
| `catchment_number` | `int32` | `False` |  | - | - | - |
| `catchment_size` | `double` | `False` |  | - | - | - |
| `latitude` | `double` | `True` |  | - | - | - |
| `longitude` | `double` | `True` |  | - | - | - |

#### Schema `SE.Gov.SMHI.Hydro.DischargeObservation`
<a id="schema-segovsmhihydrodischargeobservation"></a>

| Field | Value |
| --- | --- |
| Name | DischargeObservation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/SE/Gov/SMHI/Hydro/DischargeObservation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `DischargeObservation`
<a id="schema-node-dischargeobservation"></a>

DischargeObservation

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/SE/Gov/SMHI/Hydro/DischargeObservation` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` |  | - | - | - |
| `station_name` | `string` | `True` |  | - | - | - |
| `catchment_name` | `string` | `True` | Name of the catchment area the station belongs to (SMHI 'catchmentName' field, e.g. 'Torneälven', 'Dalälven'). Sourced by the bridge from the SMHI bulk API station catalog and propagated onto every observation so subscribers do not need an out-of-band catalog join to route by catchment. When the catalog has no catchmentName the bridge substitutes the lowercase sentinel 'unknown'. Used as the {catchment_name} segment of the MQTT/UNS topic and normalized to lowercase kebab-case before publishing. | - | - | - |
| `timestamp` | `datetime` | `True` |  | - | - | - |
| `discharge` | `double` | `True` |  | - | - | - |
| `quality` | `string` | `False` |  | - | - | - |

### Schemagroup `SE.Gov.SMHI.Hydro.avro`
<a id="schemagroup-segovsmhihydroavro"></a>

#### Schema `SE.Gov.SMHI.Hydro.Station`
<a id="schema-segovsmhihydrostation"></a>

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
| Namespace | SE.Gov.SMHI.Hydro |
| Type | `record` |
| Doc | Station |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` |  | `-` |
| `name` | `string` |  | `-` |
| `owner` | `null` \| `string` |  | `-` |
| `measuring_stations` | `null` \| `string` |  | `-` |
| `region` | `null` \| `int` |  | `-` |
| `catchment_name` | `string` | SMHI catchmentName, e.g. 'Torneälven'. Bridge substitutes the lowercase sentinel 'unknown' when the catalog lookup is empty so the field is always non-null. | `-` |
| `catchment_number` | `null` \| `int` |  | `-` |
| `catchment_size` | `null` \| `double` |  | `-` |
| `latitude` | `double` |  | `-` |
| `longitude` | `double` |  | `-` |

#### Schema `SE.Gov.SMHI.Hydro.DischargeObservation`
<a id="schema-segovsmhihydrodischargeobservation"></a>

| Field | Value |
| --- | --- |
| Name | DischargeObservation |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | DischargeObservation |
| Namespace | SE.Gov.SMHI.Hydro |
| Type | `record` |
| Doc | DischargeObservation |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` |  | `-` |
| `station_name` | `string` |  | `-` |
| `catchment_name` | `string` | SMHI catchmentName the station belongs to. Bridge substitutes the lowercase sentinel 'unknown' when the catalog lookup is empty so the field is always non-null and the MQTT topic segment remains populated. | `-` |
| `timestamp` | `string` |  | `-` |
| `discharge` | `double` |  | `-` |
| `quality` | `null` \| `string` |  | `-` |
