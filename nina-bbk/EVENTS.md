# NINA/BBK German Civil Protection Warnings Bridge Events

MQTT/5.0 transport variant for Germany NINA/BBK CAP warnings. Non-retained QoS-1 warning events route by German federal state, native CAP severity, and warning id under alerts/de/nina/nina-bbk/... The state axis is derived from CAP area administrative codes (warnVerwaltungsbereiche) with sender-code fallback.

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

### Endpoint `NINA.Warnings.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`NINA.Warnings`](#messagegroup-ninawarnings) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `nina-bbk` |
| Kafka key | `{warning_id}` |
| Deployed | False |

### Endpoint `NINA.Warnings.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`NINA.Warnings.mqtt`](#messagegroup-ninawarningsmqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

## Messagegroups

### Messagegroup `NINA.Warnings`
<a id="messagegroup-ninawarnings"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `NINA.Warnings.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `NINA.CivilWarning`
<a id="message-ninacivilwarning"></a>

A civil protection warning from Germany's NINA/BBK warning system. Aggregates warnings from MOWAS (federal), KATWARN (municipal), BIWAPP (municipal), DWD (weather service), LHP (flood centers), and police services. Each warning follows the CAP (Common Alerting Protocol) structure with multi-language support.

| Field | Value |
| --- | --- |
| Name | CivilWarning |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NINA.jstruct/schemas/NINA.CivilWarning`](#schema-ninacivilwarning) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NINA.CivilWarning` |
| `source` |  | `string` | `False` | `https://warnung.bund.de` |
| `subject` |  | `uritemplate` | `False` | `{warning_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NINA.Warnings.Kafka` | `KAFKA` | topic `nina-bbk`; key `{warning_id}` |

### Messagegroup `NINA.Warnings.mqtt`
<a id="messagegroup-ninawarningsmqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 transport variant for Germany NINA/BBK CAP warnings. Non-retained QoS-1 warning events route by German federal state, native CAP severity, and warning id under alerts/de/nina/nina-bbk/... The state axis is derived from CAP area administrative codes (warnVerwaltungsbereiche) with sender-code fallback. |
| Transport bindings | `NINA.Warnings.Mqtt` (MQTT/5.0) |
| Messages | 1 |

#### Message `NINA.Warnings.mqtt.CivilWarning`
<a id="message-ninawarningsmqttcivilwarning"></a>

A civil protection warning from Germany's NINA/BBK warning system. Aggregates warnings from MOWAS (federal), KATWARN (municipal), BIWAPP (municipal), DWD (weather service), LHP (flood centers), and police services. Each warning follows the CAP (Common Alerting Protocol) structure with multi-language support.

| Field | Value |
| --- | --- |
| Name | CivilWarning |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NINA.jstruct/schemas/NINA.CivilWarning`](#schema-ninacivilwarning) |
| Base message chain | `/messagegroups/NINA.Warnings/messages/NINA.CivilWarning` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NINA.CivilWarning` |
| `source` |  | `string` | `False` | `https://warnung.bund.de` |
| `subject` |  | `uritemplate` | `False` | `{warning_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NINA.Warnings.Mqtt` | `MQTT/5.0` | topic `alerts/de/nina/nina-bbk/{state}/{severity}/{warning_id}/warning` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `alerts/de/nina/nina-bbk/{state}/{severity}/{warning_id}/warning` |
| QoS | 1 |
| Retain | False |

## Schemagroups

### Schemagroup `NINA.jstruct`
<a id="schemagroup-ninajstruct"></a>

#### Schema `NINA.CivilWarning`
<a id="schema-ninacivilwarning"></a>

| Field | Value |
| --- | --- |
| Name | CivilWarning |
| Format | JsonStructure/draft-02 |
| Default version | 1 |
| Description | A civil protection warning from Germany's NINA/BBK system. Contains CAP-structured alert data with multi-language info blocks, BBK event codes, and German administrative area geocodes (Verwaltungsbereiche). |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://warnung.bund.de/schemas/NINA/CivilWarning` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `CivilWarning`
<a id="schema-node-civilwarning"></a>

A civil protection warning from Germany's NINA/BBK system. Contains CAP-structured alert data with multi-language info blocks, BBK event codes, and German administrative area geocodes (Verwaltungsbereiche).

| Field | Value |
| --- | --- |
| $id | `https://warnung.bund.de/schemas/NINA/CivilWarning` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `warning_id` | `string` | `True` | The unique warning identifier assigned by the NINA/BBK system (e.g., 'mow.DE-HE-DA-W184-20240723-000'). | - | - | - |
| `provider` | enum `['mowas', 'katwarn', 'biwapp', 'dwd', 'lhp', 'police']` | `True` | The NINA provider that issued the warning. | - | - | - |
| `version` | `integer` | `False` | The version number of this warning, incremented with each update. | - | - | - |
| `sender` | `string` | `True` | The identifier of the issuing authority (e.g., 'DE-HE-DA-W184'). | - | - | - |
| `sender_name` | `string` | `False` | The human-readable long name of the issuing authority (e.g., 'Integrierte Leitstelle Stadt Darmstadt'). | - | - | - |
| `sent` | `datetime` | `True` | The date and time when the warning was issued, in ISO-8601 format. | - | - | - |
| `status` | enum `['Actual', 'Exercise', 'System', 'Test', 'Draft']` | `True` | The CAP alert status. | - | - | - |
| `msg_type` | enum `['Alert', 'Update', 'Cancel', 'Ack', 'Error']` | `True` | The CAP message type indicating the nature of the warning. | altnames=`{"json": "msgType"}` | - | - |
| `scope` | enum `['Public', 'Restricted', 'Private']` | `True` | The CAP scope of the warning. Typically 'Public'. | - | - | - |
| `references` | `string` | `False` | CAP references to prior related warnings, in the format 'sender,identifier,sent'. | - | - | - |
| `event` | `string` | `True` | The event type description (e.g., 'Gefahreninformation', 'Hochwasserinformation'). | - | - | - |
| `event_code` | `string` | `False` | The BBK event code identifying the hazard type (e.g., 'BBK-EVC-067' for animal disease, 'BBK-EVC-045' for flood). | - | - | - |
| `category` | enum `['Met', 'Geo', 'Safety', 'Security', 'Rescue', 'Fire', 'Health', 'Env', 'Transport', 'Infra', 'CBRNE', 'Other']` | `False` | The CAP alert category. | - | - | - |
| `severity` | enum `['Extreme', 'Severe', 'Moderate', 'Minor', 'Unknown']` | `True` | Native CAP severity level (Minor, Moderate, Severe, Extreme, or Unknown). Matches the {severity} MQTT topic axis without further bucketing. | - | - | - |
| `urgency` | enum `['Immediate', 'Expected', 'Future', 'Past', 'Unknown']` | `True` | The CAP urgency level. | - | - | - |
| `certainty` | enum `['Observed', 'Likely', 'Possible', 'Unlikely', 'Unknown']` | `True` | The CAP certainty level. | - | - | - |
| `headline` | `string` | `False` | A brief human-readable headline summarizing the warning. | - | - | - |
| `description` | `string` | `False` | A detailed description of the warning situation. | - | - | - |
| `instruction` | `string` | `False` | Recommended protective actions for the public. | - | - | - |
| `web` | `string` | `False` | A URL to further information about the warning. | - | - | - |
| `contact` | `string` | `False` | Contact information for the issuing authority. | - | - | - |
| `area_desc` | `string` | `False` | A textual description of the affected geographic area. | - | - | - |
| `verwaltungsbereiche` | `string` | `False` | Comma-separated German administrative area codes (Amtliche Gemeindeschlüssel) affected by the warning. | - | - | - |
| `language` | `string` | `False` | The language of the info block used to populate this event (e.g., 'de', 'EN'). | - | - | - |
| `state` | `string` | `True` | German federal-state slug derived from CAP area administrative codes (warnVerwaltungsbereiche), with sender-code fallback. Matches the {state} MQTT topic axis. | - | - | - |
