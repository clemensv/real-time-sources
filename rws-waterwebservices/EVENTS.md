# RWS Waterwebservices (Netherlands) Water Level Bridge Events

MQTT/5.0 transport variants of the RWS Waterwebservices CloudEvents, mapping each message to retained, QoS-1 Unified Namespace topics under hydro/nl/rws/rws-waterwebservices/{station_code}/... RWS Waterwebservices does not expose a stable shared water-body axis in the station catalog, so the MQTT tree intentionally uses the station code as the stable subscriber axis.

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

### Endpoint `NL.RWS.Waterwebservices.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`NL.RWS.Waterwebservices`](#messagegroup-nlrwswaterwebservices) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `rws-waterwebservices` |
| Kafka key | `{station_code}` |
| Deployed | False |

### Endpoint `NL.RWS.Waterwebservices.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`NL.RWS.Waterwebservices.mqtt`](#messagegroup-nlrwswaterwebservicesmqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

## Messagegroups

### Messagegroup `NL.RWS.Waterwebservices`
<a id="messagegroup-nlrwswaterwebservices"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `NL.RWS.Waterwebservices.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `NL.RWS.Waterwebservices.Station`
<a id="message-nlrwswaterwebservicesstation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NL.RWS.Waterwebservices.jstruct/schemas/NL.RWS.Waterwebservices.Station`](#schema-nlrwswaterwebservicesstation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NL.RWS.Waterwebservices.Station` |
| `source` |  | `string` | `False` | `https://waterwebservices.rijkswaterstaat.nl` |
| `subject` |  | `uritemplate` | `False` | `{station_code}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NL.RWS.Waterwebservices.Kafka` | `KAFKA` | topic `rws-waterwebservices`; key `{station_code}` |

#### Message `NL.RWS.Waterwebservices.WaterLevelObservation`
<a id="message-nlrwswaterwebserviceswaterlevelobservation"></a>

| Field | Value |
| --- | --- |
| Name | WaterLevelObservation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NL.RWS.Waterwebservices.jstruct/schemas/NL.RWS.Waterwebservices.WaterLevelObservation`](#schema-nlrwswaterwebserviceswaterlevelobservation) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NL.RWS.Waterwebservices.WaterLevelObservation` |
| `source` |  | `string` | `False` | `https://waterwebservices.rijkswaterstaat.nl` |
| `subject` |  | `uritemplate` | `False` | `{station_code}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NL.RWS.Waterwebservices.Kafka` | `KAFKA` | topic `rws-waterwebservices`; key `{station_code}` |

### Messagegroup `NL.RWS.Waterwebservices.mqtt`
<a id="messagegroup-nlrwswaterwebservicesmqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 transport variants of the RWS Waterwebservices CloudEvents, mapping each message to retained, QoS-1 Unified Namespace topics under hydro/nl/rws/rws-waterwebservices/{station_code}/... RWS Waterwebservices does not expose a stable shared water-body axis in the station catalog, so the MQTT tree intentionally uses the station code as the stable subscriber axis. |
| Transport bindings | `NL.RWS.Waterwebservices.Mqtt` (MQTT/5.0) |
| Messages | 2 |

#### Message `NL.RWS.Waterwebservices.mqtt.Station`
<a id="message-nlrwswaterwebservicesmqttstation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NL.RWS.Waterwebservices.jstruct/schemas/NL.RWS.Waterwebservices.Station`](#schema-nlrwswaterwebservicesstation) |
| Base message chain | `/messagegroups/NL.RWS.Waterwebservices/messages/NL.RWS.Waterwebservices.Station` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NL.RWS.Waterwebservices.Station` |
| `source` |  | `string` | `False` | `https://waterwebservices.rijkswaterstaat.nl` |
| `subject` |  | `uritemplate` | `False` | `{station_code}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NL.RWS.Waterwebservices.Mqtt` | `MQTT/5.0` | topic `hydro/nl/rws/rws-waterwebservices/{station_code}/info` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/nl/rws/rws-waterwebservices/{station_code}/info` |
| QoS | 1 |
| Retain | True |

#### Message `NL.RWS.Waterwebservices.mqtt.WaterLevelObservation`
<a id="message-nlrwswaterwebservicesmqttwaterlevelobservation"></a>

| Field | Value |
| --- | --- |
| Name | WaterLevelObservation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NL.RWS.Waterwebservices.jstruct/schemas/NL.RWS.Waterwebservices.WaterLevelObservation`](#schema-nlrwswaterwebserviceswaterlevelobservation) |
| Base message chain | `/messagegroups/NL.RWS.Waterwebservices/messages/NL.RWS.Waterwebservices.WaterLevelObservation` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NL.RWS.Waterwebservices.WaterLevelObservation` |
| `source` |  | `string` | `False` | `https://waterwebservices.rijkswaterstaat.nl` |
| `subject` |  | `uritemplate` | `False` | `{station_code}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NL.RWS.Waterwebservices.Mqtt` | `MQTT/5.0` | topic `hydro/nl/rws/rws-waterwebservices/{station_code}/water-level` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/nl/rws/rws-waterwebservices/{station_code}/water-level` |
| QoS | 1 |
| Retain | True |
| Additional protocol metadata | `{"message_expiry_interval": 3600}` |

## Schemagroups

### Schemagroup `NL.RWS.Waterwebservices.jstruct`
<a id="schemagroup-nlrwswaterwebservicesjstruct"></a>

#### Schema `NL.RWS.Waterwebservices.Station`
<a id="schema-nlrwswaterwebservicesstation"></a>

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
| $id | `https://example.com/schemas/NL/RWS/Waterwebservices/Station` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Station`
<a id="schema-node-station"></a>

Station

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/NL/RWS/Waterwebservices/Station` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_code` | `string` | `True` |  | - | - | - |
| `name` | `string` | `True` |  | altnames=`{"lang:nl": "Naam"}` | - | - |
| `latitude` | `double` | `True` |  | - | - | - |
| `longitude` | `double` | `True` |  | - | - | - |
| `coordinate_system` | `string` | `False` |  | altnames=`{"lang:nl": "Coordinatenstelsel"}` | - | - |

#### Schema `NL.RWS.Waterwebservices.WaterLevelObservation`
<a id="schema-nlrwswaterwebserviceswaterlevelobservation"></a>

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
| $id | `https://example.com/schemas/NL/RWS/Waterwebservices/WaterLevelObservation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `WaterLevelObservation`
<a id="schema-node-waterlevelobservation"></a>

WaterLevelObservation

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/NL/RWS/Waterwebservices/WaterLevelObservation` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_code` | `string` | `True` |  | - | - | - |
| `location_name` | `string` | `False` |  | altnames=`{"lang:nl": "Naam"}` | - | - |
| `timestamp` | `datetime` | `True` |  | altnames=`{"lang:nl": "Tijdstip"}` | - | - |
| `value` | `double` | `True` |  | altnames=`{"lang:nl": "Waarde_Numeriek"}` | - | - |
| `unit` | `string` | `False` |  | - | - | - |
| `quality_code` | `string` | `False` |  | altnames=`{"lang:nl": "Kwaliteitswaardecode"}` | - | - |
| `status` | `string` | `False` |  | altnames=`{"lang:nl": "Statuswaarde"}` | - | - |
| `compartment` | `string` | `False` |  | - | - | - |
| `parameter` | `string` | `False` |  | - | - | - |

### Schemagroup `NL.RWS.Waterwebservices.avro`
<a id="schemagroup-nlrwswaterwebservicesavro"></a>

#### Schema `NL.RWS.Waterwebservices.Station`
<a id="schema-nlrwswaterwebservicesstation"></a>

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
| Namespace | NL.RWS.Waterwebservices |
| Type | `record` |
| Doc | Station |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_code` | `string` |  | `-` |
| `name` | `string` |  | `-` |
| `latitude` | `double` |  | `-` |
| `longitude` | `double` |  | `-` |
| `coordinate_system` | `null` \| `string` |  | `-` |

#### Schema `NL.RWS.Waterwebservices.WaterLevelObservation`
<a id="schema-nlrwswaterwebserviceswaterlevelobservation"></a>

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
| Namespace | NL.RWS.Waterwebservices |
| Type | `record` |
| Doc | WaterLevelObservation |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_code` | `string` |  | `-` |
| `location_name` | `null` \| `string` |  | `-` |
| `timestamp` | `string` |  | `-` |
| `value` | `double` |  | `-` |
| `unit` | `null` \| `string` |  | `-` |
| `quality_code` | `null` \| `string` |  | `-` |
| `status` | `null` \| `string` |  | `-` |
| `compartment` | `null` \| `string` |  | `-` |
| `parameter` | `null` \| `string` |  | `-` |
