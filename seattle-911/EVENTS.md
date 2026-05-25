# Seattle Fire 911 Bridge Events

MQTT/5.0 transport variant for Seattle Fire 911 dispatch incidents. Topics are non-retained QoS-1 event messages under civic-events/us/wa/seattle/public-safety/fire-dispatch/{incident_type_slug}/{incident_number}. The incident_type_slug field is the deterministic lowercase kebab-case routing key derived from the display incident_type; incident_number preserves the CloudEvents subject/Kafka key for per-incident subscriptions. Message expiry is 86400 seconds for queued/offline delivery only; this event stream does not use retained MQTT state.

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

### Endpoint `US.WA.Seattle.Fire911.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`US.WA.Seattle.Fire911`](#messagegroup-uswaseattlefire911) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `seattle-911` |
| Kafka key | `{incident_number}` |
| Deployed | False |

### Endpoint `US.WA.Seattle.Fire911.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`US.WA.Seattle.Fire911.mqtt`](#messagegroup-uswaseattlefire911mqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

## Messagegroups

### Messagegroup `US.WA.Seattle.Fire911`
<a id="messagegroup-uswaseattlefire911"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `US.WA.Seattle.Fire911.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `US.WA.Seattle.Fire911.Incident`
<a id="message-uswaseattlefire911incident"></a>

| Field | Value |
| --- | --- |
| Name | Incident |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/US.WA.Seattle.Fire911.jstruct/schemas/US.WA.Seattle.Fire911.Incident`](#schema-uswaseattlefire911incident) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `US.WA.Seattle.Fire911.Incident` |
| `source` |  | `string` | `False` | `https://data.seattle.gov/Public-Safety/Seattle-Real-Time-Fire-911-Calls/kzjm-xkqj` |
| `subject` |  | `uritemplate` | `False` | `{incident_number}` |
| `time` |  | `uritemplate` | `False` | `{incident_datetime_utc}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `US.WA.Seattle.Fire911.Kafka` | `KAFKA` | topic `seattle-911`; key `{incident_number}` |

### Messagegroup `US.WA.Seattle.Fire911.mqtt`
<a id="messagegroup-uswaseattlefire911mqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 transport variant for Seattle Fire 911 dispatch incidents. Topics are non-retained QoS-1 event messages under civic-events/us/wa/seattle/public-safety/fire-dispatch/{incident_type_slug}/{incident_number}. The incident_type_slug field is the deterministic lowercase kebab-case routing key derived from the display incident_type; incident_number preserves the CloudEvents subject/Kafka key for per-incident subscriptions. Message expiry is 86400 seconds for queued/offline delivery only; this event stream does not use retained MQTT state. |
| Transport bindings | `US.WA.Seattle.Fire911.Mqtt` (MQTT/5.0) |
| Messages | 1 |

#### Message `US.WA.Seattle.Fire911.mqtt.Incident`
<a id="message-uswaseattlefire911mqttincident"></a>

| Field | Value |
| --- | --- |
| Name | Incident |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/US.WA.Seattle.Fire911.jstruct/schemas/US.WA.Seattle.Fire911.Incident`](#schema-uswaseattlefire911incident) |
| Base message chain | `/messagegroups/US.WA.Seattle.Fire911/messages/US.WA.Seattle.Fire911.Incident` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `US.WA.Seattle.Fire911.Incident` |
| `source` |  | `string` | `False` | `https://data.seattle.gov/Public-Safety/Seattle-Real-Time-Fire-911-Calls/kzjm-xkqj` |
| `subject` |  | `uritemplate` | `False` | `{incident_number}` |
| `time` |  | `uritemplate` | `False` | `{incident_datetime_utc}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `US.WA.Seattle.Fire911.Mqtt` | `MQTT/5.0` | topic `civic-events/us/wa/seattle/public-safety/fire-dispatch/{incident_type_slug}/{incident_number}` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `civic-events/us/wa/seattle/public-safety/fire-dispatch/{incident_type_slug}/{incident_number}` |
| QoS | 1 |
| Retain | False |
| Additional protocol metadata | `{"message_expiry_interval": 86400}` |

## Schemagroups

### Schemagroup `US.WA.Seattle.Fire911.jstruct`
<a id="schemagroup-uswaseattlefire911jstruct"></a>

#### Schema `US.WA.Seattle.Fire911.Incident`
<a id="schema-uswaseattlefire911incident"></a>

| Field | Value |
| --- | --- |
| Name | Incident |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/seattle-911/schemas/US.WA.Seattle.Fire911.Incident.json` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Incident`
<a id="schema-node-incident"></a>

Seattle Fire Department 911 dispatch record from the City of Seattle real-time fire calls dataset.

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/seattle-911/schemas/US.WA.Seattle.Fire911.Incident.json` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `incident_number` | `string` | `True` | Stable Seattle Fire Department incident identifier for the dispatch record. | alternates=`[{"description": "Original field name in the Seattle Open Data dataset.", "name": "incident_number"}]` | - | - |
| `incident_type` | `string` | `True` | Seattle Fire Department response type display string for the incident, such as Aid Response or Medic Response. | alternates=`[{"description": "Original field name in the Seattle Open Data dataset.", "name": "type"}]` | - | - |
| `incident_datetime` | `string` | `True` | Date and time of the call as published by the Seattle Open Data dataset, in local dataset timestamp form without an explicit UTC offset. | alternates=`[{"description": "Original field name in the Seattle Open Data dataset.", "name": "datetime"}]` | - | - |
| `address` | `union` | `False` | Incident location text as published by the dataset. | alternates=`[{"description": "Original field name in the Seattle Open Data dataset.", "name": "address"}]` | - | - |
| `latitude` | `union` | `False` | Latitude of the incident location in decimal degrees north. | alternates=`[{"description": "Original field name in the Seattle Open Data dataset.", "name": "latitude"}]` | - | - |
| `longitude` | `union` | `False` | Longitude of the incident location in decimal degrees east of Greenwich; Seattle values are negative because they lie west of Greenwich. | alternates=`[{"description": "Original field name in the Seattle Open Data dataset.", "name": "longitude"}]` | - | - |
| `incident_type_slug` | `string` | `True` | Deterministic lowercase kebab-case routing slug derived from incident_type by lowercasing ASCII alphanumerics, replacing every run of non-alphanumeric characters with a single hyphen, and trimming leading/trailing hyphens (example: Aid Response - 7 per Unit -> aid-response-7-per-unit). | - | pattern=`^[a-z0-9]+(-[a-z0-9]+)*$` | - |
| `incident_datetime_utc` | `datetime` | `True` | Incident timestamp normalized to RFC 3339 UTC using America/Los_Angeles for the upstream local dataset timestamp. | - | - | - |
