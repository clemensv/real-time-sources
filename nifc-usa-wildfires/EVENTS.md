# NIFC USA Wildfires - Active Wildfire Incident Feed Events

**NIFC-USA-Wildfires** is a tool designed to interact with the [National Interagency Fire Center (NIFC)](https://www.nifc.gov/) ArcGIS Feature Service to fetch active wildfire incident data from the USA. The tool can list recent incidents or continuously poll the API to send wildfire events to a Kafka topic.

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

### Endpoint `Gov.NIFC.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`Gov.NIFC.Wildfires`](#messagegroup-govnifcwildfires) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `nifc-usa-wildfires` |
| Kafka key | `{irwin_id}` |
| Deployed | False |

## Messagegroups

### Messagegroup `Gov.NIFC.Wildfires`
<a id="messagegroup-govnifcwildfires"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `Gov.NIFC.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `Gov.NIFC.Wildfires.WildfireIncident`
<a id="message-govnifcwildfireswildfireincident"></a>

Active wildfire incident data from the National Interagency Fire Center (NIFC) IRWIN system, published via ArcGIS Feature Service.

| Field | Value |
| --- | --- |
| Name | WildfireIncident |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Gov.NIFC.Wildfires.jstruct/schemas/Gov.NIFC.Wildfires.WildfireIncident`](#schema-govnifcwildfireswildfireincident) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Gov.NIFC.Wildfires.WildfireIncident` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{irwin_id}` |
| `time` |  | `uritemplate` | `False` | `{modified_on_datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Gov.NIFC.Kafka` | `KAFKA` | topic `nifc-usa-wildfires`; key `{irwin_id}` |

## Schemagroups

### Schemagroup `Gov.NIFC.Wildfires.jstruct`
<a id="schemagroup-govnifcwildfiresjstruct"></a>

#### Schema `Gov.NIFC.Wildfires.WildfireIncident`
<a id="schema-govnifcwildfireswildfireincident"></a>

| Field | Value |
| --- | --- |
| Name | WildfireIncident |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/Gov/NIFC/Wildfires/WildfireIncident` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/Gov/NIFC/Wildfires/WildfireIncident` |
| Type | `object` |

###### Object `WildfireIncident`
<a id="schema-node-wildfireincident"></a>

Active wildfire incident data from the National Interagency Fire Center (NIFC) IRWIN system, published via ArcGIS Feature Service.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `irwin_id` | `string` | `True` | IRWIN incident identifier, a globally unique GUID assigned by the Integrated Reporting of Wildland-Fire Information (IRWIN) system. Primary key for wildfire incidents. | - | - | - |
| `incident_name` | `string` | `True` | The name assigned to the wildfire incident (e.g. 'Pinnacle', 'Backbone'). | - | - | - |
| `unique_fire_identifier` | `union` | `False` | Unique fire identifier string assigned by the dispatching agency (e.g. '2025-ORRSF-000389'). May be null for incidents not yet assigned. | - | - | - |
| `incident_type_category` | `union` | `False` | Category of the incident type: WF (Wildfire), RX (Prescribed Fire), or other NWCG-defined categories. | - | - | - |
| `incident_type_kind` | `union` | `False` | Kind of incident from NWCG classification (e.g. 'FI' for Fire). | - | - | - |
| `fire_discovery_datetime` | `union` | `False` | Date and time when the fire was first discovered, in ISO 8601 format. Converted from ArcGIS epoch milliseconds. | - | - | - |
| `daily_acres` | `union` | `False` | Most recently reported fire size in acres from the daily situation report. | - | - | - |
| `calculated_acres` | `union` | `False` | GIS-calculated fire area in acres, derived from perimeter mapping when available. | - | - | - |
| `discovery_acres` | `union` | `False` | Size of the fire in acres at the time of initial discovery. | - | - | - |
| `percent_contained` | `union` | `False` | Percentage of the fire perimeter that is contained (0-100). Null if not reported. | - | - | - |
| `poo_state` | `union` | `False` | US state or territory where the point of origin is located, as a two-letter code prefixed with 'US-' (e.g. 'US-OR', 'US-CA'). | - | - | - |
| `poo_county` | `union` | `False` | County where the point of origin of the fire is located (e.g. 'Curry', 'Kings'). | - | - | - |
| `latitude` | `union` | `False` | Latitude of the fire incident point of origin in decimal degrees (WGS 84). | - | - | - |
| `longitude` | `union` | `False` | Longitude of the fire incident point of origin in decimal degrees (WGS 84). | - | - | - |
| `fire_cause` | `union` | `False` | General cause of the fire (e.g. 'Natural', 'Human', 'Undetermined'). | - | - | - |
| `fire_cause_general` | `union` | `False` | Specific fire cause category when known (e.g. 'Lightning', 'Arson', 'Equipment Use'). | - | - | - |
| `gacc` | `union` | `False` | Geographic Area Coordination Center responsible for the incident (e.g. 'NWCC', 'OSCC', 'EACC'). GACCs coordinate wildfire management resources across regions. | - | - | - |
| `total_incident_personnel` | `union` | `False` | Total number of personnel assigned to the incident including all resources. | - | - | - |
| `incident_management_organization` | `union` | `False` | Name or type of the incident management organization or team managing the fire. | - | - | - |
| `fire_mgmt_complexity` | `union` | `False` | Complexity level of the fire management effort, typically a Type designation (e.g. 'Type 1' for the most complex). | - | - | - |
| `residences_destroyed` | `union` | `False` | Number of residential structures destroyed by the fire. | - | - | - |
| `other_structures_destroyed` | `union` | `False` | Number of non-residential structures (outbuildings, commercial, etc.) destroyed by the fire. | - | - | - |
| `injuries` | `union` | `False` | Number of injuries reported in connection with the incident. | - | - | - |
| `fatalities` | `union` | `False` | Number of fatalities reported in connection with the incident. | - | - | - |
| `containment_datetime` | `union` | `False` | Date and time the fire was fully contained, in ISO 8601 format. Null if not yet contained. | - | - | - |
| `control_datetime` | `union` | `False` | Date and time the fire was declared under control, in ISO 8601 format. Null if not yet controlled. | - | - | - |
| `fire_out_datetime` | `union` | `False` | Date and time the fire was declared out, in ISO 8601 format. Null if the fire is still active. | - | - | - |
| `final_acres` | `union` | `False` | Final fire size in acres after the fire is declared out. | - | - | - |
| `modified_on_datetime` | `string` | `True` | Date and time when the incident record was last modified in the IRWIN system, in ISO 8601 format. | - | - | - |

### Schemagroup `Gov.NIFC.Wildfires.avro`
<a id="schemagroup-govnifcwildfiresavro"></a>

#### Schema `Gov.NIFC.Wildfires.WildfireIncident`
<a id="schema-govnifcwildfireswildfireincident"></a>

| Field | Value |
| --- | --- |
| Name | WildfireIncident |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | Active wildfire incident data from the National Interagency Fire Center (NIFC) IRWIN system, published via ArcGIS Feature Service. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | WildfireIncident |
| Namespace | Gov.NIFC.Wildfires |
| Type | `record` |
| Doc | Active wildfire incident data from the National Interagency Fire Center (NIFC) IRWIN system, published via ArcGIS Feature Service. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `irwin_id` | `string` | IRWIN incident identifier, a globally unique GUID assigned by the Integrated Reporting of Wildland-Fire Information (IRWIN) system. | `-` |
| `incident_name` | `string` | The name assigned to the wildfire incident. | `-` |
| `unique_fire_identifier` | `string` \| `null` | Unique fire identifier string assigned by the dispatching agency. | `-` |
| `incident_type_category` | `string` \| `null` | Category of the incident type: WF (Wildfire), RX (Prescribed Fire), etc. | `-` |
| `incident_type_kind` | `string` \| `null` | Kind of incident from NWCG classification. | `-` |
| `fire_discovery_datetime` | `string` \| `null` | Date and time when the fire was first discovered, in ISO 8601 format. | `-` |
| `daily_acres` | `double` \| `null` | Most recently reported fire size in acres from the daily situation report. | `-` |
| `calculated_acres` | `double` \| `null` | GIS-calculated fire area in acres. | `-` |
| `discovery_acres` | `double` \| `null` | Size of the fire in acres at the time of initial discovery. | `-` |
| `percent_contained` | `double` \| `null` | Percentage of the fire perimeter that is contained (0-100). | `-` |
| `poo_state` | `string` \| `null` | US state where the point of origin is located. | `-` |
| `poo_county` | `string` \| `null` | County where the point of origin of the fire is located. | `-` |
| `latitude` | `double` \| `null` | Latitude of the fire incident point of origin in decimal degrees (WGS 84). | `-` |
| `longitude` | `double` \| `null` | Longitude of the fire incident point of origin in decimal degrees (WGS 84). | `-` |
| `fire_cause` | `string` \| `null` | General cause of the fire. | `-` |
| `fire_cause_general` | `string` \| `null` | Specific fire cause category when known. | `-` |
| `gacc` | `string` \| `null` | Geographic Area Coordination Center responsible for the incident. | `-` |
| `total_incident_personnel` | `int` \| `null` | Total number of personnel assigned to the incident. | `-` |
| `incident_management_organization` | `string` \| `null` | Name or type of the incident management organization. | `-` |
| `fire_mgmt_complexity` | `string` \| `null` | Complexity level of the fire management effort. | `-` |
| `residences_destroyed` | `int` \| `null` | Number of residential structures destroyed by the fire. | `-` |
| `other_structures_destroyed` | `int` \| `null` | Number of non-residential structures destroyed by the fire. | `-` |
| `injuries` | `int` \| `null` | Number of injuries reported in connection with the incident. | `-` |
| `fatalities` | `int` \| `null` | Number of fatalities reported in connection with the incident. | `-` |
| `containment_datetime` | `string` \| `null` | Date and time the fire was fully contained, in ISO 8601 format. | `-` |
| `control_datetime` | `string` \| `null` | Date and time the fire was declared under control, in ISO 8601 format. | `-` |
| `fire_out_datetime` | `string` \| `null` | Date and time the fire was declared out, in ISO 8601 format. | `-` |
| `final_acres` | `double` \| `null` | Final fire size in acres after the fire is declared out. | `-` |
| `modified_on_datetime` | `string` | Date and time when the incident record was last modified in the IRWIN system, in ISO 8601 format. | `-` |
