# Meteoalarm European Weather Warnings Bridge Events

MQTT/5.0 transport variant for Meteoalarm CAP weather warnings. Non-retained QoS-1 warning events route by country feed slug, native CAP severity, normalized Meteoalarm awareness type, and CAP identifier under alerts/intl/meteoalarm/meteoalarm/... The awareness_type axis is derived from the Meteoalarm awareness_type parameter label and normalized for MQTT topic safety.

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

### Endpoint `Meteoalarm.Warnings.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`Meteoalarm.Warnings`](#messagegroup-meteoalarmwarnings) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `meteoalarm` |
| Kafka key | `{identifier}` |
| Deployed | False |

### Endpoint `Meteoalarm.Warnings.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`Meteoalarm.Warnings.mqtt`](#messagegroup-meteoalarmwarningsmqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

## Messagegroups

### Messagegroup `Meteoalarm.Warnings`
<a id="messagegroup-meteoalarmwarnings"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `Meteoalarm.Warnings.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `Meteoalarm.WeatherWarning`
<a id="message-meteoalarmweatherwarning"></a>

A severe weather warning from the EUMETNET Meteoalarm system, aggregating warnings from 30+ European national meteorological services. Each warning follows the CAP (Common Alerting Protocol) structure with awareness levels and hazard types.

| Field | Value |
| --- | --- |
| Name | WeatherWarning |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Meteoalarm.jstruct/schemas/Meteoalarm.WeatherWarning`](#schema-meteoalarmweatherwarning) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Meteoalarm.WeatherWarning` |
| `source` |  | `string` | `False` | `https://feeds.meteoalarm.org` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Meteoalarm.Warnings.Kafka` | `KAFKA` | topic `meteoalarm`; key `{identifier}` |

### Messagegroup `Meteoalarm.Warnings.mqtt`
<a id="messagegroup-meteoalarmwarningsmqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 transport variant for Meteoalarm CAP weather warnings. Non-retained QoS-1 warning events route by country feed slug, native CAP severity, normalized Meteoalarm awareness type, and CAP identifier under alerts/intl/meteoalarm/meteoalarm/... The awareness_type axis is derived from the Meteoalarm awareness_type parameter label and normalized for MQTT topic safety. |
| Transport bindings | `Meteoalarm.Warnings.Mqtt` (MQTT/5.0) |
| Messages | 1 |

#### Message `Meteoalarm.Warnings.mqtt.WeatherWarning`
<a id="message-meteoalarmwarningsmqttweatherwarning"></a>

A severe weather warning from the EUMETNET Meteoalarm system, aggregating warnings from 30+ European national meteorological services. Each warning follows the CAP (Common Alerting Protocol) structure with awareness levels and hazard types.

| Field | Value |
| --- | --- |
| Name | WeatherWarning |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Meteoalarm.jstruct/schemas/Meteoalarm.WeatherWarning`](#schema-meteoalarmweatherwarning) |
| Base message chain | `/messagegroups/Meteoalarm.Warnings/messages/Meteoalarm.WeatherWarning` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Meteoalarm.WeatherWarning` |
| `source` |  | `string` | `False` | `https://feeds.meteoalarm.org` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Meteoalarm.Warnings.Mqtt` | `MQTT/5.0` | topic `alerts/intl/meteoalarm/meteoalarm/{country}/{severity}/{awareness_type}/{identifier}/warning` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `alerts/intl/meteoalarm/meteoalarm/{country}/{severity}/{awareness_type}/{identifier}/warning` |
| QoS | 1 |
| Retain | False |

## Schemagroups

### Schemagroup `Meteoalarm.jstruct`
<a id="schemagroup-meteoalarmjstruct"></a>

#### Schema `Meteoalarm.WeatherWarning`
<a id="schema-meteoalarmweatherwarning"></a>

| Field | Value |
| --- | --- |
| Name | WeatherWarning |
| Format | JsonStructure/draft-02 |
| Default version | 1 |
| Description | A severe weather warning from the EUMETNET Meteoalarm system. Contains CAP-structured alert data with awareness level and type, geographic area with EMMA/NUTS geocodes, and multilingual info blocks. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://meteoalarm.org/schemas/Meteoalarm/WeatherWarning` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `WeatherWarning`
<a id="schema-node-weatherwarning"></a>

A severe weather warning from the EUMETNET Meteoalarm system. Contains CAP-structured alert data with awareness level and type, geographic area with EMMA/NUTS geocodes, and multilingual info blocks.

| Field | Value |
| --- | --- |
| $id | `https://meteoalarm.org/schemas/Meteoalarm/WeatherWarning` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `identifier` | `string` | `True` | The unique CAP alert identifier assigned by the issuing national meteorological service. | - | - | - |
| `sender` | `string` | `True` | The identifier of the issuing national meteorological service (e.g., 'opendata@dwd.de'). | - | - | - |
| `sent` | `datetime` | `True` | The date and time when the warning was issued, in ISO-8601 format. | - | - | - |
| `status` | enum `['Actual', 'Exercise', 'System', 'Test', 'Draft']` | `True` | The CAP alert status. 'Actual' for real warnings, 'Test' for test messages. | - | - | - |
| `msg_type` | enum `['Alert', 'Update', 'Cancel', 'Ack', 'Error']` | `True` | The CAP message type indicating the nature of the alert. | altnames=`{"json": "msgType"}` | - | - |
| `scope` | enum `['Public', 'Restricted', 'Private']` | `True` | The CAP scope of the alert. Typically 'Public' for weather warnings. | - | - | - |
| `country` | `string` | `True` | Country feed slug where the warning applies (for example germany or france). Matches the {country} MQTT topic axis. | - | - | - |
| `event` | `string` | `True` | The weather event description, typically in the national language of the issuing service (e.g., 'STURMBÖEN', 'Thunderstorm'). | - | - | - |
| `category` | enum `['Met', 'Geo', 'Safety', 'Security', 'Rescue', 'Fire', 'Health', 'Env', 'Transport', 'Infra', 'CBRNE', 'Other']` | `False` | The CAP alert category. 'Met' for meteorological warnings. | - | - | - |
| `severity` | enum `['Extreme', 'Severe', 'Moderate', 'Minor', 'Unknown']` | `True` | Native CAP severity level (Minor, Moderate, Severe, Extreme, or Unknown). Matches the {severity} MQTT topic axis without further bucketing. | - | - | - |
| `urgency` | enum `['Immediate', 'Expected', 'Future', 'Past', 'Unknown']` | `True` | The CAP urgency level indicating the time-frame for protective action. | - | - | - |
| `certainty` | enum `['Observed', 'Likely', 'Possible', 'Unlikely', 'Unknown']` | `True` | The CAP certainty level indicating the confidence in the forecast. | - | - | - |
| `headline` | `string` | `False` | A brief human-readable headline summarizing the warning, often in the national language. | - | - | - |
| `description` | `string` | `False` | A detailed description of the weather warning, often in the national language. | - | - | - |
| `instruction` | `string` | `False` | Recommended protective actions for the public. | - | - | - |
| `effective` | `datetime` | `False` | The date and time when the warning becomes effective, in ISO-8601 format. | - | - | - |
| `onset` | `datetime` | `False` | The expected date and time of onset of the weather event, in ISO-8601 format. | - | - | - |
| `expires` | `datetime` | `False` | The date and time when the warning expires, in ISO-8601 format. | - | - | - |
| `web` | `string` | `False` | A URL to the full warning details on the issuing service's website. | - | - | - |
| `contact` | `string` | `False` | Contact information for the issuing meteorological service. | - | - | - |
| `awareness_level` | `string` | `False` | The Meteoalarm awareness level as a string combining the numeric level and color, e.g., '2; yellow; Moderate'. Values range from '1; green' (no significant weather) to '4; red' (very dangerous). | - | - | - |
| `awareness_type` | `string` | `True` | Meteoalarm awareness type label normalized to lowercase kebab-case for MQTT topic routing (for example wind, snow-ice, thunderstorm, flooding). Matches the {awareness_type} MQTT topic axis. | - | - | - |
| `area_desc` | `string` | `True` | A textual description of the affected geographic area. | - | - | - |
| `geocodes` | `string` | `False` | A semicolon-separated list of geocode values (EMMA_ID or WARNCELLID) identifying the specific warning zones. | - | - | - |
| `language` | `string` | `False` | The language of the info block used to populate this event (e.g., 'de-DE', 'en-GB'). | - | - | - |
| `awareness_type_raw` | `string` | `False` | Raw Meteoalarm awareness_type parameter value as provided by CAP, for example "2; Snow/Ice". | - | - | - |
