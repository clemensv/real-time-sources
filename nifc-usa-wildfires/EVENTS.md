# NIFC USA Wildfires Events

This document describes the events emitted by the NIFC USA Wildfires bridge.

- [Gov.NIFC.Wildfires](#message-group-govnifcwildfires)
  - [Gov.NIFC.Wildfires.WildfireIncident](#message-govnifcwildfireswildfireincident)

---

## Message Group: Gov.NIFC.Wildfires

---

### Message: Gov.NIFC.Wildfires.WildfireIncident

*Active wildfire incident data from the National Interagency Fire Center (NIFC) IRWIN system, published via ArcGIS Feature Service.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `Gov.NIFC.Wildfires.WildfireIncident` |
| `source` | Source URI | `uritemplate` | `True` | `{source_uri}` |
| `subject` | IRWIN incident ID | `uritemplate` | `True` | `{irwin_id}` |
| `time` | Last modification time | `uritemplate` | `True` | `{modified_on_datetime}` |

#### Schema: Gov.NIFC.Wildfires.WildfireIncident (Avro)

| **Field** | **Type** | **Description** |
|-----------|----------|-----------------|
| `irwin_id` | `string` | IRWIN incident identifier, a globally unique GUID. |
| `incident_name` | `string` | The name assigned to the wildfire incident. |
| `unique_fire_identifier` | `string?` | Unique fire identifier string assigned by the dispatching agency. |
| `incident_type_category` | `string?` | Category of the incident type: WF (Wildfire), RX (Prescribed Fire), etc. |
| `incident_type_kind` | `string?` | Kind of incident from NWCG classification. |
| `fire_discovery_datetime` | `string?` | Date and time when the fire was first discovered, in ISO 8601 format. |
| `daily_acres` | `double?` | Most recently reported fire size in acres. |
| `calculated_acres` | `double?` | GIS-calculated fire area in acres. |
| `discovery_acres` | `double?` | Size of the fire in acres at the time of initial discovery. |
| `percent_contained` | `double?` | Percentage of the fire perimeter that is contained (0-100). |
| `poo_state` | `string?` | US state where the point of origin is located. |
| `poo_county` | `string?` | County where the point of origin of the fire is located. |
| `latitude` | `double?` | Latitude of the fire incident point of origin (WGS 84). |
| `longitude` | `double?` | Longitude of the fire incident point of origin (WGS 84). |
| `fire_cause` | `string?` | General cause of the fire. |
| `fire_cause_general` | `string?` | Specific fire cause category when known. |
| `gacc` | `string?` | Geographic Area Coordination Center responsible for the incident. |
| `total_incident_personnel` | `int?` | Total number of personnel assigned to the incident. |
| `incident_management_organization` | `string?` | Name or type of the incident management organization. |
| `fire_mgmt_complexity` | `string?` | Complexity level of the fire management effort. |
| `residences_destroyed` | `int?` | Number of residential structures destroyed. |
| `other_structures_destroyed` | `int?` | Number of non-residential structures destroyed. |
| `injuries` | `int?` | Number of injuries reported. |
| `fatalities` | `int?` | Number of fatalities reported. |
| `containment_datetime` | `string?` | Date and time the fire was fully contained, in ISO 8601 format. |
| `control_datetime` | `string?` | Date and time the fire was declared under control, in ISO 8601 format. |
| `fire_out_datetime` | `string?` | Date and time the fire was declared out, in ISO 8601 format. |
| `final_acres` | `double?` | Final fire size in acres after the fire is declared out. |
| `modified_on_datetime` | `string` | Date and time when the incident record was last modified in IRWIN. |
