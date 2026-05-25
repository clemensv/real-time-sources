# GDACS — Global Disaster Alert and Coordination System Events

MQTT/5.0 transport variant for GDACS disaster alerts. Non-retained QoS-1 alert events route by disaster event type, event-level GDACS alert color, affected country, and event id under alerts/intl/gdacs/gdacs/... GDACS is both provider and source in this single-feed namespace branch; subscribe with wildcards across the color axis to follow episode-level alert transitions.

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

### Endpoint `GDACS.Alerts.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`GDACS.Alerts`](#messagegroup-gdacsalerts) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `gdacs` |
| Kafka key | `{event_type}/{event_id}` |
| Deployed | False |

### Endpoint `GDACS.Alerts.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`GDACS.Alerts.mqtt`](#messagegroup-gdacsalertsmqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

## Messagegroups

### Messagegroup `GDACS.Alerts`
<a id="messagegroup-gdacsalerts"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `GDACS.Alerts.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `GDACS.DisasterAlert`
<a id="message-gdacsdisasteralert"></a>

A disaster alert from the Global Disaster Alert and Coordination System (GDACS), covering earthquakes, tropical cyclones, floods, volcanoes, forest fires, and droughts worldwide.

| Field | Value |
| --- | --- |
| Name | DisasterAlert |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/GDACS.jstruct/schemas/GDACS.DisasterAlert`](#schema-gdacsdisasteralert) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `GDACS.DisasterAlert` |
| `source` |  | `string` | `False` | `https://www.gdacs.org` |
| `subject` |  | `uritemplate` | `False` | `{event_type}/{event_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `GDACS.Alerts.Kafka` | `KAFKA` | topic `gdacs`; key `{event_type}/{event_id}` |

### Messagegroup `GDACS.Alerts.mqtt`
<a id="messagegroup-gdacsalertsmqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 transport variant for GDACS disaster alerts. Non-retained QoS-1 alert events route by disaster event type, event-level GDACS alert color, affected country, and event id under alerts/intl/gdacs/gdacs/... GDACS is both provider and source in this single-feed namespace branch; subscribe with wildcards across the color axis to follow episode-level alert transitions. |
| Transport bindings | `GDACS.Alerts.Mqtt` (MQTT/5.0) |
| Messages | 1 |

#### Message `GDACS.Alerts.mqtt.DisasterAlert`
<a id="message-gdacsalertsmqttdisasteralert"></a>

A disaster alert from the Global Disaster Alert and Coordination System (GDACS), covering earthquakes, tropical cyclones, floods, volcanoes, forest fires, and droughts worldwide.

| Field | Value |
| --- | --- |
| Name | DisasterAlert |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/GDACS.jstruct/schemas/GDACS.DisasterAlert`](#schema-gdacsdisasteralert) |
| Base message chain | `/messagegroups/GDACS.Alerts/messages/GDACS.DisasterAlert` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `GDACS.DisasterAlert` |
| `source` |  | `string` | `False` | `https://www.gdacs.org` |
| `subject` |  | `uritemplate` | `False` | `{event_type}/{event_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `GDACS.Alerts.Mqtt` | `MQTT/5.0` | topic `alerts/intl/gdacs/gdacs/{event_type}/{alert_color}/{country}/{event_id}/alert` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `alerts/intl/gdacs/gdacs/{event_type}/{alert_color}/{country}/{event_id}/alert` |
| QoS | 1 |
| Retain | False |

## Schemagroups

### Schemagroup `GDACS.jstruct`
<a id="schemagroup-gdacsjstruct"></a>

#### Schema `GDACS.DisasterAlert`
<a id="schema-gdacsdisasteralert"></a>

| Field | Value |
| --- | --- |
| Name | DisasterAlert |
| Format | JsonStructure/draft-02 |
| Default version | 1 |
| Description | A disaster alert from the Global Disaster Alert and Coordination System (GDACS), representing a single episode of a natural disaster event such as an earthquake, tropical cyclone, flood, volcano eruption, forest fire, or drought. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://gdacs.org/schemas/GDACS/DisasterAlert` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `DisasterAlert`
<a id="schema-node-disasteralert"></a>

A disaster alert from the Global Disaster Alert and Coordination System (GDACS), representing a single episode of a natural disaster event such as an earthquake, tropical cyclone, flood, volcano eruption, forest fire, or drought.

| Field | Value |
| --- | --- |
| $id | `https://gdacs.org/schemas/GDACS/DisasterAlert` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `event_type` | enum `['EQ', 'TC', 'FL', 'VO', 'FF', 'DR']` | `True` | The type of natural disaster reported by GDACS. EQ = Earthquake, TC = Tropical Cyclone, FL = Flood, VO = Volcano, FF = Forest Fire, DR = Drought. | altnames=`{"xml": "gdacs:eventtype"}` | - | - |
| `event_id` | `string` | `True` | The unique numeric identifier assigned to the disaster event by GDACS, stable across all episodes and updates for the same event. | altnames=`{"xml": "gdacs:eventid"}` | - | - |
| `episode_id` | `string` | `False` | The unique numeric identifier for a specific episode within an event. Events such as tropical cyclones may have multiple episodes as they evolve over time. | altnames=`{"xml": "gdacs:episodeid"}` | - | - |
| `alert_level` | enum `['Green', 'Orange', 'Red']` | `True` | The overall GDACS alert level for the event, indicating the expected humanitarian impact. Green = low impact, Orange = moderate impact, Red = high impact requiring international response. | altnames=`{"xml": "gdacs:alertlevel"}` | - | - |
| `alert_score` | `double` | `False` | A numeric score (0.0–3.0) representing the overall alert severity. Higher values indicate greater expected impact. Derived from severity, population exposure, and vulnerability. | altnames=`{"xml": "gdacs:alertscore"}` | - | - |
| `episode_alert_level` | `string` | `False` | The GDACS alert level specific to this episode, which may differ from the overall event alert level as conditions evolve. | altnames=`{"xml": "gdacs:episodealertlevel"}` | - | - |
| `episode_alert_score` | `double` | `False` | A numeric score (0.0–3.0) representing the alert severity for this specific episode. | altnames=`{"xml": "gdacs:episodealertscore"}` | - | - |
| `event_name` | `string` | `False` | The human-readable name assigned to the event by GDACS, such as a cyclone name or descriptive location label. | altnames=`{"xml": "gdacs:eventname"}` | - | - |
| `severity_value` | `double` | `True` | The numeric severity measure for the event. The meaning depends on the event type: magnitude for earthquakes, wind speed for cyclones, water level for floods, VEI for volcanoes. | - | - | - |
| `severity_unit` | `string` | `True` | The unit of measurement for the severity value. Examples: 'M' (Richter magnitude), 'km/h' (wind speed), 'm' (water level), 'VEI' (Volcanic Explosivity Index). | - | - | - |
| `severity_text` | `string` | `False` | A human-readable text description of the severity, as provided in the GDACS RSS feed severity element text content. | - | - | - |
| `country` | `string` | `True` | Affected country name or normalized unknown sentinel when GDACS omits the country. Matches the {country} MQTT topic axis. | altnames=`{"xml": "gdacs:country"}` | - | - |
| `iso3` | `string` | `False` | The ISO 3166-1 alpha-3 country code(s) for the affected country or countries. | altnames=`{"xml": "gdacs:iso3"}` | - | - |
| `latitude` | `double` | `True` | The latitude of the disaster event epicenter or centroid in decimal degrees (WGS84). | altnames=`{"xml": "geo:lat"}` | - | - |
| `longitude` | `double` | `True` | The longitude of the disaster event epicenter or centroid in decimal degrees (WGS84). | altnames=`{"xml": "geo:long"}` | - | - |
| `from_date` | `datetime` | `True` | The date and time when the disaster event was first detected or began, in ISO-8601 format. | altnames=`{"xml": "gdacs:fromdate"}` | - | - |
| `to_date` | `datetime` | `False` | The date and time when the disaster event ended or was last observed, in ISO-8601 format. May be absent for ongoing events. | altnames=`{"xml": "gdacs:todate"}` | - | - |
| `population_value` | `double` | `False` | The estimated number of people exposed to or affected by the disaster event, as calculated by GDACS impact models. | - | - | - |
| `population_unit` | `string` | `False` | The unit for the population value, typically 'Pop' (population count) or a radius-based exposure descriptor. | - | - | - |
| `vulnerability` | `double` | `False` | A GDACS-calculated vulnerability score (0.0–3.0) that reflects the affected region's capacity to cope with the disaster, factoring in infrastructure, governance, and socioeconomic conditions. | altnames=`{"xml": "gdacs:vulnerability"}` | - | - |
| `bbox_min_lon` | `double` | `False` | The minimum longitude of the bounding box that encloses the affected area, in decimal degrees. | - | - | - |
| `bbox_max_lon` | `double` | `False` | The maximum longitude of the bounding box that encloses the affected area, in decimal degrees. | - | - | - |
| `bbox_min_lat` | `double` | `False` | The minimum latitude of the bounding box that encloses the affected area, in decimal degrees. | - | - | - |
| `bbox_max_lat` | `double` | `False` | The maximum latitude of the bounding box that encloses the affected area, in decimal degrees. | - | - | - |
| `is_current` | `boolean` | `False` | Whether this disaster event is currently ongoing according to GDACS. True if the event is still active, false if it has concluded. | altnames=`{"xml": "gdacs:iscurrent"}` | - | - |
| `version` | `int32` | `False` | The version number of this event record in GDACS. Incremented each time the event data is updated or revised. | altnames=`{"xml": "gdacs:version"}` | - | - |
| `description` | `string` | `False` | The RSS item description text, typically a brief HTML or plain-text summary of the disaster event with key impact details. | - | - | - |
| `link` | `string` | `False` | The URL linking to the full GDACS event report page for this disaster event. | - | - | - |
| `pub_date` | `datetime` | `False` | The date and time when this RSS item was published or last updated, in ISO-8601 format. | - | - | - |
| `alert_color` | enum `['green', 'orange', 'red']` | `True` | Lowercase GDACS alert color derived from alert_level (green, orange, or red). Matches the {alert_color} MQTT topic axis. | - | - | - |
