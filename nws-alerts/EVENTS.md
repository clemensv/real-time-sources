# NWS CAP Weather Alerts Bridge Events

MQTT/5.0 mirror of NWS CAP weather alerts, published into the Unified-Namespace topic tree 'alerts/us/noaa/nws-alerts/{state}/<severity>/{event_type}/{alert_id}/alert'. CAP severity is baked as one of five literal sub-tree partitions (minor, moderate, severe, extreme, unknown) so every template placeholder resolves from an enriched WeatherAlert schema field. Alerts are QoS-1 non-retained one-shot lifecycle events.

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

### Endpoint `NWS.Alerts.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`NWS.Alerts`](#messagegroup-nwsalerts) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `nws-alerts` |
| Kafka key | `{alert_id}` |
| Deployed | False |

### Endpoint `NWS.Alerts.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`NWS.Alerts.mqtt`](#messagegroup-nwsalertsmqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

## Messagegroups

### Messagegroup `NWS.Alerts`
<a id="messagegroup-nwsalerts"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `NWS.Alerts.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `NWS.WeatherAlert`
<a id="message-nwsweatheralert"></a>

A weather or non-weather alert from the US National Weather Service, distributed through the Integrated Public Alert and Warning System (IPAWS). Follows the CAP (Common Alerting Protocol) standard.

| Field | Value |
| --- | --- |
| Name | WeatherAlert |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NWS.jstruct/schemas/NWS.WeatherAlert`](#schema-nwsweatheralert) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NWS.WeatherAlert` |
| `source` |  | `string` | `False` | `https://api.weather.gov` |
| `subject` |  | `uritemplate` | `False` | `{alert_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NWS.Alerts.Kafka` | `KAFKA` | topic `nws-alerts`; key `{alert_id}` |

### Messagegroup `NWS.Alerts.mqtt`
<a id="messagegroup-nwsalertsmqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 mirror of NWS CAP weather alerts, published into the Unified-Namespace topic tree 'alerts/us/noaa/nws-alerts/{state}/<severity>/{event_type}/{alert_id}/alert'. CAP severity is baked as one of five literal sub-tree partitions (minor, moderate, severe, extreme, unknown) so every template placeholder resolves from an enriched WeatherAlert schema field. Alerts are QoS-1 non-retained one-shot lifecycle events. |
| Transport bindings | `NWS.Alerts.Mqtt` (MQTT/5.0) |
| Messages | 5 |

#### Message `NWS.WeatherAlert.Minor.mqtt`
<a id="message-nwsweatheralertminormqtt"></a>

A weather or non-weather alert from the US National Weather Service, distributed through the Integrated Public Alert and Warning System (IPAWS). Follows the CAP (Common Alerting Protocol) standard.

| Field | Value |
| --- | --- |
| Name | WeatherAlertMinor |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NWS.jstruct/schemas/NWS.WeatherAlert`](#schema-nwsweatheralert) |
| Base message chain | `/messagegroups/NWS.Alerts/messages/NWS.WeatherAlert` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NWS.WeatherAlert` |
| `source` |  | `string` | `False` | `https://api.weather.gov` |
| `subject` |  | `uritemplate` | `False` | `{alert_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NWS.Alerts.Mqtt` | `MQTT/5.0` | topic `alerts/us/noaa/nws-alerts/{state}/minor/{event_type}/{alert_id}/alert` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `alerts/us/noaa/nws-alerts/{state}/minor/{event_type}/{alert_id}/alert` |
| QoS | 1 |
| Retain | False |

#### Message `NWS.WeatherAlert.Moderate.mqtt`
<a id="message-nwsweatheralertmoderatemqtt"></a>

A weather or non-weather alert from the US National Weather Service, distributed through the Integrated Public Alert and Warning System (IPAWS). Follows the CAP (Common Alerting Protocol) standard.

| Field | Value |
| --- | --- |
| Name | WeatherAlertModerate |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NWS.jstruct/schemas/NWS.WeatherAlert`](#schema-nwsweatheralert) |
| Base message chain | `/messagegroups/NWS.Alerts/messages/NWS.WeatherAlert` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NWS.WeatherAlert` |
| `source` |  | `string` | `False` | `https://api.weather.gov` |
| `subject` |  | `uritemplate` | `False` | `{alert_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NWS.Alerts.Mqtt` | `MQTT/5.0` | topic `alerts/us/noaa/nws-alerts/{state}/moderate/{event_type}/{alert_id}/alert` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `alerts/us/noaa/nws-alerts/{state}/moderate/{event_type}/{alert_id}/alert` |
| QoS | 1 |
| Retain | False |

#### Message `NWS.WeatherAlert.Severe.mqtt`
<a id="message-nwsweatheralertseveremqtt"></a>

A weather or non-weather alert from the US National Weather Service, distributed through the Integrated Public Alert and Warning System (IPAWS). Follows the CAP (Common Alerting Protocol) standard.

| Field | Value |
| --- | --- |
| Name | WeatherAlertSevere |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NWS.jstruct/schemas/NWS.WeatherAlert`](#schema-nwsweatheralert) |
| Base message chain | `/messagegroups/NWS.Alerts/messages/NWS.WeatherAlert` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NWS.WeatherAlert` |
| `source` |  | `string` | `False` | `https://api.weather.gov` |
| `subject` |  | `uritemplate` | `False` | `{alert_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NWS.Alerts.Mqtt` | `MQTT/5.0` | topic `alerts/us/noaa/nws-alerts/{state}/severe/{event_type}/{alert_id}/alert` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `alerts/us/noaa/nws-alerts/{state}/severe/{event_type}/{alert_id}/alert` |
| QoS | 1 |
| Retain | False |

#### Message `NWS.WeatherAlert.Extreme.mqtt`
<a id="message-nwsweatheralertextrememqtt"></a>

A weather or non-weather alert from the US National Weather Service, distributed through the Integrated Public Alert and Warning System (IPAWS). Follows the CAP (Common Alerting Protocol) standard.

| Field | Value |
| --- | --- |
| Name | WeatherAlertExtreme |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NWS.jstruct/schemas/NWS.WeatherAlert`](#schema-nwsweatheralert) |
| Base message chain | `/messagegroups/NWS.Alerts/messages/NWS.WeatherAlert` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NWS.WeatherAlert` |
| `source` |  | `string` | `False` | `https://api.weather.gov` |
| `subject` |  | `uritemplate` | `False` | `{alert_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NWS.Alerts.Mqtt` | `MQTT/5.0` | topic `alerts/us/noaa/nws-alerts/{state}/extreme/{event_type}/{alert_id}/alert` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `alerts/us/noaa/nws-alerts/{state}/extreme/{event_type}/{alert_id}/alert` |
| QoS | 1 |
| Retain | False |

#### Message `NWS.WeatherAlert.Unknown.mqtt`
<a id="message-nwsweatheralertunknownmqtt"></a>

A weather or non-weather alert from the US National Weather Service, distributed through the Integrated Public Alert and Warning System (IPAWS). Follows the CAP (Common Alerting Protocol) standard.

| Field | Value |
| --- | --- |
| Name | WeatherAlertUnknown |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NWS.jstruct/schemas/NWS.WeatherAlert`](#schema-nwsweatheralert) |
| Base message chain | `/messagegroups/NWS.Alerts/messages/NWS.WeatherAlert` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NWS.WeatherAlert` |
| `source` |  | `string` | `False` | `https://api.weather.gov` |
| `subject` |  | `uritemplate` | `False` | `{alert_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NWS.Alerts.Mqtt` | `MQTT/5.0` | topic `alerts/us/noaa/nws-alerts/{state}/unknown/{event_type}/{alert_id}/alert` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `alerts/us/noaa/nws-alerts/{state}/unknown/{event_type}/{alert_id}/alert` |
| QoS | 1 |
| Retain | False |

## Schemagroups

### Schemagroup `NWS.jstruct`
<a id="schemagroup-nwsjstruct"></a>

#### Schema `NWS.WeatherAlert`
<a id="schema-nwsweatheralert"></a>

| Field | Value |
| --- | --- |
| Name | WeatherAlert |
| Format | JsonStructure/draft-02 |
| Default version | 1 |
| Description | A weather or non-weather alert from the US National Weather Service (NWS/NOAA). Contains full CAP properties including severity, urgency, certainty, VTEC codes for event tracking, and UGC/SAME zone geocodes. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://api.weather.gov/schemas/NWS/WeatherAlert` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `WeatherAlert`
<a id="schema-node-weatheralert"></a>

A weather or non-weather alert from the US National Weather Service (NWS/NOAA). Contains full CAP properties including severity, urgency, certainty, VTEC codes for event tracking, and UGC/SAME zone geocodes.

| Field | Value |
| --- | --- |
| $id | `https://api.weather.gov/schemas/NWS/WeatherAlert` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `alert_id` | `string` | `True` | The unique URN-based identifier for the alert (e.g., 'urn:oid:2.49.0.1.840.0.xxx'). Stable across the lifecycle of the alert. | altnames=`{"json": "id"}` | - | - |
| `area_desc` | `string` | `False` | A textual description of the affected geographic area (e.g., county names). | altnames=`{"json": "areaDesc"}` | - | - |
| `same_codes` | `string` | `False` | Semicolon-separated SAME (Specific Area Message Encoding) codes identifying affected counties/zones. Used by the Emergency Alert System (EAS). | - | - | - |
| `ugc_codes` | `string` | `False` | Semicolon-separated UGC (Universal Geographic Code) zone identifiers (e.g., 'MDC031', 'TXZ001'). | - | - | - |
| `sent` | `datetime` | `True` | The date and time when the alert was sent, in ISO-8601 format. | - | - | - |
| `effective` | `datetime` | `False` | The date and time when the alert becomes effective. | - | - | - |
| `onset` | `datetime` | `False` | The expected date and time of onset of the weather event. | - | - | - |
| `expires` | `datetime` | `False` | The date and time when the alert expires. | - | - | - |
| `ends` | `datetime` | `False` | The expected end time of the weather event. | - | - | - |
| `status` | enum `['Actual', 'Exercise', 'System', 'Test', 'Draft']` | `True` | The CAP alert status. | - | - | - |
| `message_type` | enum `['Alert', 'Update', 'Cancel', 'Ack', 'Error']` | `True` | The CAP message type. | altnames=`{"json": "messageType"}` | - | - |
| `category` | `string` | `False` | The CAP alert category (e.g., 'Met' for meteorological). | - | - | - |
| `severity` | enum `['Extreme', 'Severe', 'Moderate', 'Minor', 'Unknown']` | `True` | The CAP severity level. | - | - | - |
| `certainty` | enum `['Observed', 'Likely', 'Possible', 'Unlikely', 'Unknown']` | `True` | The CAP certainty level. | - | - | - |
| `urgency` | enum `['Immediate', 'Expected', 'Future', 'Past', 'Unknown']` | `True` | The CAP urgency level. | - | - | - |
| `event` | `string` | `True` | The type of weather event (e.g., 'Tornado Warning', 'Flood Watch', 'Heat Advisory'). | - | - | - |
| `sender` | `string` | `False` | The email address or identifier of the alert sender. | - | - | - |
| `sender_name` | `string` | `False` | The human-readable name of the sender (e.g., 'NWS Tulsa OK'). | altnames=`{"json": "senderName"}` | - | - |
| `headline` | `string` | `False` | A brief headline summarizing the alert. | - | - | - |
| `description` | `string` | `False` | The full textual description of the alert. | - | - | - |
| `instruction` | `string` | `False` | Recommended protective actions. | - | - | - |
| `response` | `string` | `False` | The recommended response type (e.g., 'Shelter', 'Evacuate', 'None'). | - | - | - |
| `scope` | `string` | `False` | The CAP scope of the alert. | - | - | - |
| `code` | `string` | `False` | The IPAWS code (e.g., 'IPAWSv1.0'). | - | - | - |
| `nws_headline` | `string` | `False` | The NWS-specific headline from the parameters block. | - | - | - |
| `vtec` | `string` | `False` | The P-VTEC (Valid Time Event Code) string for NWS event tracking. | - | - | - |
| `web` | `string` | `False` | A URL to the full alert details. | - | - | - |
| `state` | `string` | `True` | Lowercase USPS state or territory code enriched by the bridge from NWS UGC/SAME zone identifiers; nostate when no state can be resolved. | - | - | - |
| `event_type` | `string` | `True` | Lowercase kebab-case slug derived from the CAP event field for topic partitioning. | - | - | - |
