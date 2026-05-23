# NWS CAP Weather Alerts Events

CloudEvents contract for NWS CAP weather alerts. Kafka uses topic `nws-alerts` keyed by `{alert_id}`. MQTT publishes binary-mode CloudEvents to `alerts/us/noaa/nws-alerts/{state}/<severity>/{event_type}/{alert_id}/alert` with CAP severity baked as one of `minor`, `moderate`, `severe`, `extreme`, or `unknown`.

- [NWS.Alerts](#message-group-nwsalerts)
  - [NWS.WeatherAlert](#message-nwsweatheralert)
- [NWS.Alerts.mqtt](#message-group-nwsalertsmqtt)
  - [NWS.WeatherAlert.Minor.mqtt](#message-nwsweatheralertminormqtt)
  - [NWS.WeatherAlert.Moderate.mqtt](#message-nwsweatheralertmoderatemqtt)
  - [NWS.WeatherAlert.Severe.mqtt](#message-nwsweatheralertseveremqtt)
  - [NWS.WeatherAlert.Extreme.mqtt](#message-nwsweatheralertextrememqtt)
  - [NWS.WeatherAlert.Unknown.mqtt](#message-nwsweatheralertunknownmqtt)

---

## Message Group: NWS.Alerts
---
### Message: NWS.WeatherAlert
*A weather or non-weather alert from the US National Weather Service, distributed through the Integrated Public Alert and Warning System (IPAWS). Follows the CAP (Common Alerting Protocol) standard.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `NWS.WeatherAlert` |
| `source` |  | `` | `False` | `https://api.weather.gov` |
| `subject` |  | `uritemplate` | `False` | `{alert_id}` |

#### Schema:
##### Object: WeatherAlert
*A weather or non-weather alert from the US National Weather Service (NWS/NOAA). Contains full CAP properties including severity, urgency, certainty, VTEC codes for event tracking, and UGC/SAME zone geocodes.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `alert_id` | *string* | - | `True` | The unique URN-based identifier for the alert (e.g., 'urn:oid:2.49.0.1.840.0.xxx'). Stable across the lifecycle of the alert. |
| `area_desc` | *string* | - | `False` | A textual description of the affected geographic area (e.g., county names). |
| `same_codes` | *string* | - | `False` | Semicolon-separated SAME (Specific Area Message Encoding) codes identifying affected counties/zones. Used by the Emergency Alert System (EAS). |
| `ugc_codes` | *string* | - | `False` | Semicolon-separated UGC (Universal Geographic Code) zone identifiers (e.g., 'MDC031', 'TXZ001'). |
| `sent` | *datetime* | - | `True` | The date and time when the alert was sent, in ISO-8601 format. |
| `effective` | *datetime* | - | `False` | The date and time when the alert becomes effective. |
| `onset` | *datetime* | - | `False` | The expected date and time of onset of the weather event. |
| `expires` | *datetime* | - | `False` | The date and time when the alert expires. |
| `ends` | *datetime* | - | `False` | The expected end time of the weather event. |
| `status` | *string* | - | `True` | The CAP alert status. |
| `message_type` | *string* | - | `True` | The CAP message type. |
| `category` | *string* | - | `False` | The CAP alert category (e.g., 'Met' for meteorological). |
| `severity` | *string* | - | `True` | The CAP severity level. |
| `certainty` | *string* | - | `True` | The CAP certainty level. |
| `urgency` | *string* | - | `True` | The CAP urgency level. |
| `event` | *string* | - | `True` | The type of weather event (e.g., 'Tornado Warning', 'Flood Watch', 'Heat Advisory'). |
| `sender` | *string* | - | `False` | The email address or identifier of the alert sender. |
| `sender_name` | *string* | - | `False` | The human-readable name of the sender (e.g., 'NWS Tulsa OK'). |
| `headline` | *string* | - | `False` | A brief headline summarizing the alert. |
| `description` | *string* | - | `False` | The full textual description of the alert. |
| `instruction` | *string* | - | `False` | Recommended protective actions. |
| `response` | *string* | - | `False` | The recommended response type (e.g., 'Shelter', 'Evacuate', 'None'). |
| `scope` | *string* | - | `False` | The CAP scope of the alert. |
| `code` | *string* | - | `False` | The IPAWS code (e.g., 'IPAWSv1.0'). |
| `nws_headline` | *string* | - | `False` | The NWS-specific headline from the parameters block. |
| `vtec` | *string* | - | `False` | The P-VTEC (Valid Time Event Code) string for NWS event tracking. |
| `web` | *string* | - | `False` | A URL to the full alert details. |
| `state` | *string* | - | `True` | Lowercase USPS state or territory code enriched by the bridge from NWS UGC/SAME zone identifiers; nostate when no state can be resolved. |
| `event_type` | *string* | - | `True` | Lowercase kebab-case slug derived from the CAP event field for topic partitioning. |
## Message Group: NWS.Alerts.mqtt
---
### Message: NWS.WeatherAlert.Minor.mqtt
*A weather or non-weather alert from the US National Weather Service, distributed through the Integrated Public Alert and Warning System (IPAWS). Follows the CAP (Common Alerting Protocol) standard.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `NWS.WeatherAlert` |
| `source` |  | `` | `False` | `https://api.weather.gov` |
| `subject` |  | `uritemplate` | `False` | `{alert_id}` |

#### Schema:
##### Object: WeatherAlert
*A weather or non-weather alert from the US National Weather Service (NWS/NOAA). Contains full CAP properties including severity, urgency, certainty, VTEC codes for event tracking, and UGC/SAME zone geocodes.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `alert_id` | *string* | - | `True` | The unique URN-based identifier for the alert (e.g., 'urn:oid:2.49.0.1.840.0.xxx'). Stable across the lifecycle of the alert. |
| `area_desc` | *string* | - | `False` | A textual description of the affected geographic area (e.g., county names). |
| `same_codes` | *string* | - | `False` | Semicolon-separated SAME (Specific Area Message Encoding) codes identifying affected counties/zones. Used by the Emergency Alert System (EAS). |
| `ugc_codes` | *string* | - | `False` | Semicolon-separated UGC (Universal Geographic Code) zone identifiers (e.g., 'MDC031', 'TXZ001'). |
| `sent` | *datetime* | - | `True` | The date and time when the alert was sent, in ISO-8601 format. |
| `effective` | *datetime* | - | `False` | The date and time when the alert becomes effective. |
| `onset` | *datetime* | - | `False` | The expected date and time of onset of the weather event. |
| `expires` | *datetime* | - | `False` | The date and time when the alert expires. |
| `ends` | *datetime* | - | `False` | The expected end time of the weather event. |
| `status` | *string* | - | `True` | The CAP alert status. |
| `message_type` | *string* | - | `True` | The CAP message type. |
| `category` | *string* | - | `False` | The CAP alert category (e.g., 'Met' for meteorological). |
| `severity` | *string* | - | `True` | The CAP severity level. |
| `certainty` | *string* | - | `True` | The CAP certainty level. |
| `urgency` | *string* | - | `True` | The CAP urgency level. |
| `event` | *string* | - | `True` | The type of weather event (e.g., 'Tornado Warning', 'Flood Watch', 'Heat Advisory'). |
| `sender` | *string* | - | `False` | The email address or identifier of the alert sender. |
| `sender_name` | *string* | - | `False` | The human-readable name of the sender (e.g., 'NWS Tulsa OK'). |
| `headline` | *string* | - | `False` | A brief headline summarizing the alert. |
| `description` | *string* | - | `False` | The full textual description of the alert. |
| `instruction` | *string* | - | `False` | Recommended protective actions. |
| `response` | *string* | - | `False` | The recommended response type (e.g., 'Shelter', 'Evacuate', 'None'). |
| `scope` | *string* | - | `False` | The CAP scope of the alert. |
| `code` | *string* | - | `False` | The IPAWS code (e.g., 'IPAWSv1.0'). |
| `nws_headline` | *string* | - | `False` | The NWS-specific headline from the parameters block. |
| `vtec` | *string* | - | `False` | The P-VTEC (Valid Time Event Code) string for NWS event tracking. |
| `web` | *string* | - | `False` | A URL to the full alert details. |
| `state` | *string* | - | `True` | Lowercase USPS state or territory code enriched by the bridge from NWS UGC/SAME zone identifiers; nostate when no state can be resolved. |
| `event_type` | *string* | - | `True` | Lowercase kebab-case slug derived from the CAP event field for topic partitioning. |
---
### Message: NWS.WeatherAlert.Moderate.mqtt
*A weather or non-weather alert from the US National Weather Service, distributed through the Integrated Public Alert and Warning System (IPAWS). Follows the CAP (Common Alerting Protocol) standard.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `NWS.WeatherAlert` |
| `source` |  | `` | `False` | `https://api.weather.gov` |
| `subject` |  | `uritemplate` | `False` | `{alert_id}` |

#### Schema:
##### Object: WeatherAlert
*A weather or non-weather alert from the US National Weather Service (NWS/NOAA). Contains full CAP properties including severity, urgency, certainty, VTEC codes for event tracking, and UGC/SAME zone geocodes.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `alert_id` | *string* | - | `True` | The unique URN-based identifier for the alert (e.g., 'urn:oid:2.49.0.1.840.0.xxx'). Stable across the lifecycle of the alert. |
| `area_desc` | *string* | - | `False` | A textual description of the affected geographic area (e.g., county names). |
| `same_codes` | *string* | - | `False` | Semicolon-separated SAME (Specific Area Message Encoding) codes identifying affected counties/zones. Used by the Emergency Alert System (EAS). |
| `ugc_codes` | *string* | - | `False` | Semicolon-separated UGC (Universal Geographic Code) zone identifiers (e.g., 'MDC031', 'TXZ001'). |
| `sent` | *datetime* | - | `True` | The date and time when the alert was sent, in ISO-8601 format. |
| `effective` | *datetime* | - | `False` | The date and time when the alert becomes effective. |
| `onset` | *datetime* | - | `False` | The expected date and time of onset of the weather event. |
| `expires` | *datetime* | - | `False` | The date and time when the alert expires. |
| `ends` | *datetime* | - | `False` | The expected end time of the weather event. |
| `status` | *string* | - | `True` | The CAP alert status. |
| `message_type` | *string* | - | `True` | The CAP message type. |
| `category` | *string* | - | `False` | The CAP alert category (e.g., 'Met' for meteorological). |
| `severity` | *string* | - | `True` | The CAP severity level. |
| `certainty` | *string* | - | `True` | The CAP certainty level. |
| `urgency` | *string* | - | `True` | The CAP urgency level. |
| `event` | *string* | - | `True` | The type of weather event (e.g., 'Tornado Warning', 'Flood Watch', 'Heat Advisory'). |
| `sender` | *string* | - | `False` | The email address or identifier of the alert sender. |
| `sender_name` | *string* | - | `False` | The human-readable name of the sender (e.g., 'NWS Tulsa OK'). |
| `headline` | *string* | - | `False` | A brief headline summarizing the alert. |
| `description` | *string* | - | `False` | The full textual description of the alert. |
| `instruction` | *string* | - | `False` | Recommended protective actions. |
| `response` | *string* | - | `False` | The recommended response type (e.g., 'Shelter', 'Evacuate', 'None'). |
| `scope` | *string* | - | `False` | The CAP scope of the alert. |
| `code` | *string* | - | `False` | The IPAWS code (e.g., 'IPAWSv1.0'). |
| `nws_headline` | *string* | - | `False` | The NWS-specific headline from the parameters block. |
| `vtec` | *string* | - | `False` | The P-VTEC (Valid Time Event Code) string for NWS event tracking. |
| `web` | *string* | - | `False` | A URL to the full alert details. |
| `state` | *string* | - | `True` | Lowercase USPS state or territory code enriched by the bridge from NWS UGC/SAME zone identifiers; nostate when no state can be resolved. |
| `event_type` | *string* | - | `True` | Lowercase kebab-case slug derived from the CAP event field for topic partitioning. |
---
### Message: NWS.WeatherAlert.Severe.mqtt
*A weather or non-weather alert from the US National Weather Service, distributed through the Integrated Public Alert and Warning System (IPAWS). Follows the CAP (Common Alerting Protocol) standard.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `NWS.WeatherAlert` |
| `source` |  | `` | `False` | `https://api.weather.gov` |
| `subject` |  | `uritemplate` | `False` | `{alert_id}` |

#### Schema:
##### Object: WeatherAlert
*A weather or non-weather alert from the US National Weather Service (NWS/NOAA). Contains full CAP properties including severity, urgency, certainty, VTEC codes for event tracking, and UGC/SAME zone geocodes.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `alert_id` | *string* | - | `True` | The unique URN-based identifier for the alert (e.g., 'urn:oid:2.49.0.1.840.0.xxx'). Stable across the lifecycle of the alert. |
| `area_desc` | *string* | - | `False` | A textual description of the affected geographic area (e.g., county names). |
| `same_codes` | *string* | - | `False` | Semicolon-separated SAME (Specific Area Message Encoding) codes identifying affected counties/zones. Used by the Emergency Alert System (EAS). |
| `ugc_codes` | *string* | - | `False` | Semicolon-separated UGC (Universal Geographic Code) zone identifiers (e.g., 'MDC031', 'TXZ001'). |
| `sent` | *datetime* | - | `True` | The date and time when the alert was sent, in ISO-8601 format. |
| `effective` | *datetime* | - | `False` | The date and time when the alert becomes effective. |
| `onset` | *datetime* | - | `False` | The expected date and time of onset of the weather event. |
| `expires` | *datetime* | - | `False` | The date and time when the alert expires. |
| `ends` | *datetime* | - | `False` | The expected end time of the weather event. |
| `status` | *string* | - | `True` | The CAP alert status. |
| `message_type` | *string* | - | `True` | The CAP message type. |
| `category` | *string* | - | `False` | The CAP alert category (e.g., 'Met' for meteorological). |
| `severity` | *string* | - | `True` | The CAP severity level. |
| `certainty` | *string* | - | `True` | The CAP certainty level. |
| `urgency` | *string* | - | `True` | The CAP urgency level. |
| `event` | *string* | - | `True` | The type of weather event (e.g., 'Tornado Warning', 'Flood Watch', 'Heat Advisory'). |
| `sender` | *string* | - | `False` | The email address or identifier of the alert sender. |
| `sender_name` | *string* | - | `False` | The human-readable name of the sender (e.g., 'NWS Tulsa OK'). |
| `headline` | *string* | - | `False` | A brief headline summarizing the alert. |
| `description` | *string* | - | `False` | The full textual description of the alert. |
| `instruction` | *string* | - | `False` | Recommended protective actions. |
| `response` | *string* | - | `False` | The recommended response type (e.g., 'Shelter', 'Evacuate', 'None'). |
| `scope` | *string* | - | `False` | The CAP scope of the alert. |
| `code` | *string* | - | `False` | The IPAWS code (e.g., 'IPAWSv1.0'). |
| `nws_headline` | *string* | - | `False` | The NWS-specific headline from the parameters block. |
| `vtec` | *string* | - | `False` | The P-VTEC (Valid Time Event Code) string for NWS event tracking. |
| `web` | *string* | - | `False` | A URL to the full alert details. |
| `state` | *string* | - | `True` | Lowercase USPS state or territory code enriched by the bridge from NWS UGC/SAME zone identifiers; nostate when no state can be resolved. |
| `event_type` | *string* | - | `True` | Lowercase kebab-case slug derived from the CAP event field for topic partitioning. |
---
### Message: NWS.WeatherAlert.Extreme.mqtt
*A weather or non-weather alert from the US National Weather Service, distributed through the Integrated Public Alert and Warning System (IPAWS). Follows the CAP (Common Alerting Protocol) standard.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `NWS.WeatherAlert` |
| `source` |  | `` | `False` | `https://api.weather.gov` |
| `subject` |  | `uritemplate` | `False` | `{alert_id}` |

#### Schema:
##### Object: WeatherAlert
*A weather or non-weather alert from the US National Weather Service (NWS/NOAA). Contains full CAP properties including severity, urgency, certainty, VTEC codes for event tracking, and UGC/SAME zone geocodes.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `alert_id` | *string* | - | `True` | The unique URN-based identifier for the alert (e.g., 'urn:oid:2.49.0.1.840.0.xxx'). Stable across the lifecycle of the alert. |
| `area_desc` | *string* | - | `False` | A textual description of the affected geographic area (e.g., county names). |
| `same_codes` | *string* | - | `False` | Semicolon-separated SAME (Specific Area Message Encoding) codes identifying affected counties/zones. Used by the Emergency Alert System (EAS). |
| `ugc_codes` | *string* | - | `False` | Semicolon-separated UGC (Universal Geographic Code) zone identifiers (e.g., 'MDC031', 'TXZ001'). |
| `sent` | *datetime* | - | `True` | The date and time when the alert was sent, in ISO-8601 format. |
| `effective` | *datetime* | - | `False` | The date and time when the alert becomes effective. |
| `onset` | *datetime* | - | `False` | The expected date and time of onset of the weather event. |
| `expires` | *datetime* | - | `False` | The date and time when the alert expires. |
| `ends` | *datetime* | - | `False` | The expected end time of the weather event. |
| `status` | *string* | - | `True` | The CAP alert status. |
| `message_type` | *string* | - | `True` | The CAP message type. |
| `category` | *string* | - | `False` | The CAP alert category (e.g., 'Met' for meteorological). |
| `severity` | *string* | - | `True` | The CAP severity level. |
| `certainty` | *string* | - | `True` | The CAP certainty level. |
| `urgency` | *string* | - | `True` | The CAP urgency level. |
| `event` | *string* | - | `True` | The type of weather event (e.g., 'Tornado Warning', 'Flood Watch', 'Heat Advisory'). |
| `sender` | *string* | - | `False` | The email address or identifier of the alert sender. |
| `sender_name` | *string* | - | `False` | The human-readable name of the sender (e.g., 'NWS Tulsa OK'). |
| `headline` | *string* | - | `False` | A brief headline summarizing the alert. |
| `description` | *string* | - | `False` | The full textual description of the alert. |
| `instruction` | *string* | - | `False` | Recommended protective actions. |
| `response` | *string* | - | `False` | The recommended response type (e.g., 'Shelter', 'Evacuate', 'None'). |
| `scope` | *string* | - | `False` | The CAP scope of the alert. |
| `code` | *string* | - | `False` | The IPAWS code (e.g., 'IPAWSv1.0'). |
| `nws_headline` | *string* | - | `False` | The NWS-specific headline from the parameters block. |
| `vtec` | *string* | - | `False` | The P-VTEC (Valid Time Event Code) string for NWS event tracking. |
| `web` | *string* | - | `False` | A URL to the full alert details. |
| `state` | *string* | - | `True` | Lowercase USPS state or territory code enriched by the bridge from NWS UGC/SAME zone identifiers; nostate when no state can be resolved. |
| `event_type` | *string* | - | `True` | Lowercase kebab-case slug derived from the CAP event field for topic partitioning. |
---
### Message: NWS.WeatherAlert.Unknown.mqtt
*A weather or non-weather alert from the US National Weather Service, distributed through the Integrated Public Alert and Warning System (IPAWS). Follows the CAP (Common Alerting Protocol) standard.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `NWS.WeatherAlert` |
| `source` |  | `` | `False` | `https://api.weather.gov` |
| `subject` |  | `uritemplate` | `False` | `{alert_id}` |

#### Schema:
##### Object: WeatherAlert
*A weather or non-weather alert from the US National Weather Service (NWS/NOAA). Contains full CAP properties including severity, urgency, certainty, VTEC codes for event tracking, and UGC/SAME zone geocodes.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `alert_id` | *string* | - | `True` | The unique URN-based identifier for the alert (e.g., 'urn:oid:2.49.0.1.840.0.xxx'). Stable across the lifecycle of the alert. |
| `area_desc` | *string* | - | `False` | A textual description of the affected geographic area (e.g., county names). |
| `same_codes` | *string* | - | `False` | Semicolon-separated SAME (Specific Area Message Encoding) codes identifying affected counties/zones. Used by the Emergency Alert System (EAS). |
| `ugc_codes` | *string* | - | `False` | Semicolon-separated UGC (Universal Geographic Code) zone identifiers (e.g., 'MDC031', 'TXZ001'). |
| `sent` | *datetime* | - | `True` | The date and time when the alert was sent, in ISO-8601 format. |
| `effective` | *datetime* | - | `False` | The date and time when the alert becomes effective. |
| `onset` | *datetime* | - | `False` | The expected date and time of onset of the weather event. |
| `expires` | *datetime* | - | `False` | The date and time when the alert expires. |
| `ends` | *datetime* | - | `False` | The expected end time of the weather event. |
| `status` | *string* | - | `True` | The CAP alert status. |
| `message_type` | *string* | - | `True` | The CAP message type. |
| `category` | *string* | - | `False` | The CAP alert category (e.g., 'Met' for meteorological). |
| `severity` | *string* | - | `True` | The CAP severity level. |
| `certainty` | *string* | - | `True` | The CAP certainty level. |
| `urgency` | *string* | - | `True` | The CAP urgency level. |
| `event` | *string* | - | `True` | The type of weather event (e.g., 'Tornado Warning', 'Flood Watch', 'Heat Advisory'). |
| `sender` | *string* | - | `False` | The email address or identifier of the alert sender. |
| `sender_name` | *string* | - | `False` | The human-readable name of the sender (e.g., 'NWS Tulsa OK'). |
| `headline` | *string* | - | `False` | A brief headline summarizing the alert. |
| `description` | *string* | - | `False` | The full textual description of the alert. |
| `instruction` | *string* | - | `False` | Recommended protective actions. |
| `response` | *string* | - | `False` | The recommended response type (e.g., 'Shelter', 'Evacuate', 'None'). |
| `scope` | *string* | - | `False` | The CAP scope of the alert. |
| `code` | *string* | - | `False` | The IPAWS code (e.g., 'IPAWSv1.0'). |
| `nws_headline` | *string* | - | `False` | The NWS-specific headline from the parameters block. |
| `vtec` | *string* | - | `False` | The P-VTEC (Valid Time Event Code) string for NWS event tracking. |
| `web` | *string* | - | `False` | A URL to the full alert details. |
| `state` | *string* | - | `True` | Lowercase USPS state or territory code enriched by the bridge from NWS UGC/SAME zone identifiers; nostate when no state can be resolved. |
| `event_type` | *string* | - | `True` | Lowercase kebab-case slug derived from the CAP event field for topic partitioning. |


## Subscription patterns

MQTT subscribers can use standard wildcards over the severity-partitioned UNS tree:

- All NWS alerts: `alerts/us/noaa/nws-alerts/+/+/+/+/alert`
- All extreme severity alerts in California: `alerts/us/noaa/nws-alerts/ca/extreme/+/+/alert`
- Tornado warnings across all states and severities: `alerts/us/noaa/nws-alerts/+/+/tornado-warning/+/alert`
- All severe or extreme alerts in Texas: subscribe to both `alerts/us/noaa/nws-alerts/tx/severe/+/+/alert` and `alerts/us/noaa/nws-alerts/tx/extreme/+/+/alert`
- All alerts with no resolved state: `alerts/us/noaa/nws-alerts/nostate/+/+/+/alert`
