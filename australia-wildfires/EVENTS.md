# Australian State Wildfires Bridge Events

MQTT/5.0 transport variant for Australian bushfire incidents. The UNS topic tree is wildfire/au/{state}/{status}/{incident_id}/incident. QoS 1 and retain=false are used because incident updates are time-varying event updates rather than static reference data; consumers deduplicate by {state}/{incident_id} and CloudEvents id.

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

### Endpoint `AU.Gov.Emergency.Wildfires.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`AU.Gov.Emergency.Wildfires`](#messagegroup-augovemergencywildfires) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `australia-wildfires` |
| Kafka key | `{state}/{incident_id}` |
| Deployed | False |

### Endpoint `AU.Gov.Emergency.Wildfires.Mqtt`

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 binary-mode CloudEvents producer for the Australian wildfires UNS topic tree. |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`AU.Gov.Emergency.Wildfires.mqtt`](#messagegroup-augovemergencywildfiresmqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

## Messagegroups

### Messagegroup `AU.Gov.Emergency.Wildfires`
<a id="messagegroup-augovemergencywildfires"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `AU.Gov.Emergency.Wildfires.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `AU.Gov.Emergency.Wildfires.FireIncident`
<a id="message-augovemergencywildfiresfireincident"></a>

| Field | Value |
| --- | --- |
| Name | FireIncident |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/AU.Gov.Emergency.Wildfires.jstruct/schemas/AU.Gov.Emergency.Wildfires.FireIncident`](#schema-augovemergencywildfiresfireincident) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `AU.Gov.Emergency.Wildfires.FireIncident` |
| `source` |  | `string` | `False` | `https://github.com/clemensv/real-time-sources/tree/main/australia-wildfires` |
| `subject` |  | `uritemplate` | `False` | `{state}/{incident_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `AU.Gov.Emergency.Wildfires.Kafka` | `KAFKA` | topic `australia-wildfires`; key `{state}/{incident_id}` |

### Messagegroup `AU.Gov.Emergency.Wildfires.mqtt`
<a id="messagegroup-augovemergencywildfiresmqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 transport variant for Australian bushfire incidents. The UNS topic tree is wildfire/au/{state}/{status}/{incident_id}/incident. QoS 1 and retain=false are used because incident updates are time-varying event updates rather than static reference data; consumers deduplicate by {state}/{incident_id} and CloudEvents id. |
| Transport bindings | `AU.Gov.Emergency.Wildfires.Mqtt` (MQTT/5.0) |
| Messages | 1 |

#### Message `AU.Gov.Emergency.Wildfires.mqtt.FireIncident`
<a id="message-augovemergencywildfiresmqttfireincident"></a>

| Field | Value |
| --- | --- |
| Name | FireIncident |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/AU.Gov.Emergency.Wildfires.jstruct/schemas/AU.Gov.Emergency.Wildfires.FireIncident`](#schema-augovemergencywildfiresfireincident) |
| Base message chain | `/messagegroups/AU.Gov.Emergency.Wildfires/messages/AU.Gov.Emergency.Wildfires.FireIncident` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `AU.Gov.Emergency.Wildfires.FireIncident` |
| `source` |  | `string` | `False` | `https://github.com/clemensv/real-time-sources/tree/main/australia-wildfires` |
| `subject` |  | `uritemplate` | `False` | `{state}/{incident_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `AU.Gov.Emergency.Wildfires.Mqtt` | `MQTT/5.0` | topic `wildfire/au/{state}/{status}/{incident_id}/incident` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `wildfire/au/{state}/{status}/{incident_id}/incident` |
| QoS | 1 |
| Retain | False |
| Additional protocol metadata | `{"message_expiry_interval": 604800}` |

## Schemagroups

### Schemagroup `AU.Gov.Emergency.Wildfires.jstruct`
<a id="schemagroup-augovemergencywildfiresjstruct"></a>

#### Schema `AU.Gov.Emergency.Wildfires.FireIncident`
<a id="schema-augovemergencywildfiresfireincident"></a>

| Field | Value |
| --- | --- |
| Name | FireIncident |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://emergency.gov.au/schemas/AU/Gov/Emergency/Wildfires/FireIncident` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `FireIncident`
<a id="schema-node-fireincident"></a>

Normalized bushfire or grass fire incident record aggregated from three Australian state emergency services: NSW Rural Fire Service (GeoJSON major-incidents feed), VicEmergency (GeoJSON all-hazards feed filtered to fire events), and Queensland Fire Department (GeoJSON bushfire-alert feed). Each record represents a single active fire incident with its alert level, location, size, and responsible agency.

| Field | Value |
| --- | --- |
| $id | `https://emergency.gov.au/schemas/AU/Gov/Emergency/Wildfires/FireIncident` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `incident_id` | `string` | `True` | Stable identifier for the fire incident, derived from the source system. NSW: numeric incident ID extracted from the RFS GUID URL. VIC: numeric sourceId from the VicEmergency feed. QLD: alphanumeric UniqueID from the QFD feed (e.g. 'IF39-5661721'). | - | - | - |
| `state` | `string` | `True` | Australian state abbreviation indicating which emergency service reported this incident. One of 'NSW' (New South Wales Rural Fire Service), 'VIC' (VicEmergency / Country Fire Authority / Fire Rescue Victoria), or 'QLD' (Queensland Fire Department). | - | - | - |
| `title` | `string` | `True` | Human-readable title or headline for the incident as provided by the source agency. NSW: location-based title from the RFS feed (e.g. '(GWYDIR HWY), MATHESON'). VIC: warning name or sourceTitle from VicEmergency. QLD: WarningTitle from the QFD feed. | - | - | - |
| `alert_level` | `string` | `True` | Fire danger alert level as classified by the issuing agency. Common values across states: 'Advice' (fire is under control or low threat), 'Watch and Act' (conditions are changing, prepare to leave), 'Emergency Warning' (immediate danger, take action now). NSW uses 'category' field, VIC uses 'action' or category1, QLD uses 'WarningLevel'. | - | - | - |
| `status` | `string` | `True` | Topic-safe lowercase-kebab operational status for the incident (e.g. under-control, being-controlled, out-of-control, unknown). The MQTT feeder maps missing upstream status values to unknown so the {status} topic segment is never null or empty. | - | pattern=`^[a-z0-9][a-z0-9-]*$` | - |
| `location` | `union` | `False` | Human-readable location description for the incident. NSW: full location string extracted from the HTML description (e.g. 'B76 (GWYDIR HWY), MATHESON 2370'). VIC: locality names from the location field. QLD: derived from the WarningTitle or Header text. | - | - | - |
| `latitude` | `union` | `False` | Latitude of the incident centroid in decimal degrees (WGS84). Extracted from the GeoJSON Point geometry where available, or computed as the centroid of a Polygon geometry. Negative values indicate Southern Hemisphere. | unit=`degree` symbol=`\u00b0` | - | - |
| `longitude` | `union` | `False` | Longitude of the incident centroid in decimal degrees (WGS84). Extracted from the GeoJSON Point geometry where available, or computed as the centroid of a Polygon geometry. | unit=`degree` symbol=`\u00b0` | - | - |
| `size_hectares` | `union` | `False` | Estimated area of the fire in hectares as reported by the source agency. NSW: extracted from the SIZE field in the HTML description. VIC: parsed from sizeFmt if available. QLD: not typically provided, may be null. | unit=`hectare` symbol=`ha` | - | - |
| `type` | `union` | `False` | Classification of the fire type as reported by the source agency. NSW: extracted from the TYPE field in the HTML description (e.g. 'Bush Fire', 'Grass Fire', 'Hazard Reduction'). VIC: event field from the CAP envelope (e.g. 'Grass Fire', 'Scrub Fire', 'Bush Fire'). QLD: derived from CallToAction text. | - | - | - |
| `responsible_agency` | `union` | `False` | Name of the fire-fighting agency responsible for the incident. NSW: extracted from RESPONSIBLE AGENCY in the HTML description (e.g. 'Rural Fire Service', 'Fire and Rescue NSW'). VIC: senderName from the CAP envelope (e.g. 'Country Fire Authority', 'Fire Rescue Victoria'). QLD: defaults to 'Queensland Fire Department'. | - | - | - |
| `updated` | `datetime` | `True` | Timestamp when the incident record was last updated by the source agency, in ISO 8601 format with UTC timezone. NSW: parsed from the UPDATED field in the HTML description or pubDate. VIC: 'updated' field from the VicEmergency feed. QLD: parsed from the WarningTitle date reference or current fetch time. | - | - | - |
| `source_url` | `string` | `True` | URL pointing to the original incident details or the source feed. NSW: GUID permalink from the RFS feed (e.g. 'https://incidents.rfs.nsw.gov.au/api/v1/incidents/653509'). VIC: constructed URL to the VicEmergency warning page. QLD: static URL of the QFD bushfire alert feed. | - | - | - |
