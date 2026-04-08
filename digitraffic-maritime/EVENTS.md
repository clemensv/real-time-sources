# Table of Contents

- [fi.digitraffic.marine.ais](#message-group-fidigitrafficmarineais)
  - [fi.digitraffic.marine.ais.VesselLocation](#message-fidigitrafficmarineaisvessellocation)
  - [fi.digitraffic.marine.ais.VesselMetadata](#message-fidigitrafficmarineaisvesselmetadata)
- [fi.digitraffic.marine.portcall](#message-group-fidigitrafficmarineportcall)
  - [fi.digitraffic.marine.portcall.PortCall](#message-fidigitrafficmarineportcallportcall)
- [fi.digitraffic.marine.portcall.vesseldetails](#message-group-fidigitrafficmarineportcallvesseldetails)
  - [fi.digitraffic.marine.portcall.VesselDetails](#message-fidigitrafficmarineportcallvesseldetails)
- [fi.digitraffic.marine.portcall.portlocation](#message-group-fidigitrafficmarineportcallportlocation)
  - [fi.digitraffic.marine.portcall.PortLocation](#message-fidigitrafficmarineportcallportlocation)

---

## Message Group: fi.digitraffic.marine.ais
---
### Message: fi.digitraffic.marine.ais.VesselLocation
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `fi.digitraffic.marine.ais.VesselLocation` |
| `source` |  | `` | `False` | `wss://meri.digitraffic.fi/mqtt` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

#### Schema:
##### Object: VesselLocation
*AIS vessel position report from Digitraffic MQTT stream. Represents a decoded AIS message type 1/2/3/18/19 position update.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `mmsi` | *int32* | - | `False` |  |
| `time` | *int32* | - | `True` |  |
| `sog` | *double* | - | `True` |  |
| `cog` | *double* | - | `True` |  |
| `navStat` | *int32* | - | `True` |  |
| `rot` | *int32* | - | `True` |  |
| `posAcc` | *boolean* | - | `True` |  |
| `raim` | *boolean* | - | `True` |  |
| `heading` | *int32* | - | `True` |  |
| `lon` | *double* | - | `True` |  |
| `lat` | *double* | - | `True` |  |
---
### Message: fi.digitraffic.marine.ais.VesselMetadata
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `fi.digitraffic.marine.ais.VesselMetadata` |
| `source` |  | `` | `False` | `wss://meri.digitraffic.fi/mqtt` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

#### Schema:
##### Object: VesselMetadata
*AIS vessel static and voyage data from Digitraffic MQTT stream. Represents decoded AIS message type 5/24 data.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `mmsi` | *int32* | - | `False` |  |
| `timestamp` | *int32* | - | `True` |  |
| `name` | *string* | - | `False` |  |
| `callSign` | *string* | - | `False` |  |
| `imo` | *int32* | - | `False` |  |
| `type` | *int32* | - | `False` |  |
| `draught` | *int32* | - | `False` |  |
| `eta` | *int32* | - | `False` |  |
| `destination` | *string* | - | `False` |  |
| `posType` | *int32* | - | `False` |  |
| `refA` | *int32* | - | `False` |  |
| `refB` | *int32* | - | `False` |  |
| `refC` | *int32* | - | `False` |  |
| `refD` | *int32* | - | `False` |  |
## Message Group: fi.digitraffic.marine.portcall
---
### Message: fi.digitraffic.marine.portcall.PortCall
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `fi.digitraffic.marine.portcall.PortCall` |
| `source` |  | `` | `False` | `https://meri.digitraffic.fi/api/port-call/v1/port-calls` |
| `subject` |  | `uritemplate` | `False` | `{port_call_id}` |

#### Schema:
##### Object: PortCall
*Port call update from Digitraffic's Portnet-backed port-call API. Each event represents one vessel visit plan or update keyed by the Digitraffic port call identifier and carries the vessel identity, routing context, assigned agents, and berth-area timing details.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `port_call_id` | *int32* | - | `True` | Digitraffic port call identifier for this Portnet vessel visit record. |
| `updated_at` | *datetime* | - | `True` | Timestamp when this port call record was last updated in Digitraffic, from the portCallTimestamp field. |
| `customs_reference` | *string* (optional) | - | `False` | Customs reference string carried with the port call when available. |
| `port_to_visit` | *string* | - | `True` | UN/LOCODE of the destination port that this call is scheduled to visit. |
| `previous_port` | *string* (optional) | - | `False` | UN/LOCODE of the vessel's previous port when reported by Portnet. |
| `next_port` | *string* (optional) | - | `False` | UN/LOCODE of the vessel's next announced port when reported by Portnet. |
| `mmsi` | *int32* (optional) | - | `False` | Maritime Mobile Service Identity associated with the visiting vessel, when available. |
| `imo_lloyds` | *int32* (optional) | - | `False` | IMO or Lloyd's vessel number carried with the port call when available. |
| `vessel_name` | *string* | - | `True` | Reported vessel name for the visit. |
| `vessel_name_prefix` | *string* (optional) | - | `False` | Reported vessel name prefix such as 'ms' or 'mt' when present. |
| `radio_call_sign` | *string* (optional) | - | `False` | Radio call sign for the visiting vessel when reported by Portnet. |
| `nationality` | *string* (optional) | - | `False` | Flag or nationality code reported for the vessel. |
| `vessel_type_code` | *int32* (optional) | - | `False` | Digitraffic vessel type code for the visiting vessel. |
| `domestic_traffic_arrival` | *boolean* | - | `True` | True when the arrival leg is domestic traffic. |
| `domestic_traffic_departure` | *boolean* | - | `True` | True when the departure leg is domestic traffic. |
| `arrival_with_cargo` | *boolean* | - | `True` | True when the vessel is reported as arriving with cargo. |
| `not_loading` | *boolean* | - | `True` | True when the vessel is reported as not loading cargo at the call. |
| `discharge` | *int32* (optional) | - | `False` | Digitraffic discharge indicator value for the call when reported. |
| `current_security_level` | *int32* (optional) | - | `False` | Current ISPS security level reported for the vessel at this call. |
| `agents` | array of [Object PortCallAgent](#object-portcallagent) | - | `True` | Agent and manager organizations attached to the port call. |
| `port_areas` | array of [Object PortCallAreaDetail](#object-portcallareadetail) | - | `True` | Planned or actual berth and port-area timing details associated with the call. |

---
##### Object: PortCallAgent
*One agent or manager assignment attached to the port call.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `name` | *string* | - | `True` | Organization name for the assigned ship agent or manager. |
| `port_call_direction` | *string* | - | `True` | Direction scope for the assignment, such as arrival, departure, or whole port call. |
| `role` | *int32* | - | `True` | Digitraffic role code for the assignment, for example agent or ship manager. |

---
##### Object: PortCallAreaDetail
*A berth or port-area schedule detail attached to the port call.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `port_area_code` | *string* (optional) | - | `False` | Code of the destination port area when assigned. |
| `port_area_name` | *string* (optional) | - | `False` | Human-readable name of the destination port area when assigned. |
| `berth_code` | *string* (optional) | - | `False` | Berth code within the destination port area when assigned. |
| `berth_name` | *string* (optional) | - | `False` | Human-readable berth name when assigned. |
| `eta` | *datetime* (optional) | - | `False` | Estimated time of arrival for this port-area assignment. |
| `eta_source` | *string* (optional) | - | `False` | Source of the ETA value, for example an agent update. |
| `etd` | *datetime* (optional) | - | `False` | Estimated time of departure for this port-area assignment. |
| `etd_source` | *string* (optional) | - | `False` | Source of the ETD value, for example an agent update. |
| `ata` | *datetime* (optional) | - | `False` | Actual time of arrival for this port-area assignment when recorded. |
| `ata_source` | *string* (optional) | - | `False` | Source of the ATA value when recorded. |
| `atd` | *datetime* (optional) | - | `False` | Actual time of departure for this port-area assignment when recorded. |
| `atd_source` | *string* (optional) | - | `False` | Source of the ATD value when recorded. |
| `arrival_draught` | *double* | m | `True` | Arrival draught reported for this berth or port-area assignment in meters. |
| `departure_draught` | *double* | m | `True` | Departure draught reported for this berth or port-area assignment in meters. |
## Message Group: fi.digitraffic.marine.portcall.vesseldetails
---
### Message: fi.digitraffic.marine.portcall.VesselDetails
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `fi.digitraffic.marine.portcall.VesselDetails` |
| `source` |  | `` | `False` | `https://meri.digitraffic.fi/api/port-call/v1/vessel-details` |
| `subject` |  | `uritemplate` | `False` | `{vessel_id}` |

#### Schema:
##### Object: VesselDetails
*Reference record from Digitraffic's Port Call vessel-details API. Each event represents the current known metadata for one vessel entity keyed by Digitraffic's stable vessel identifier and includes identity, construction, dimensions, registration, and contact details sourced from Portnet.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `vessel_id` | *integer* | - | `True` | Digitraffic vessel identifier from the vesselId field. This is the stable identifier used as the CloudEvents subject and Kafka record key for vessel reference events. |
| `updated_at` | *datetime* | - | `True` | Timestamp when Digitraffic last updated the vessel metadata record, from the updateTimestamp field. |
| `mmsi` | *int32* (optional) | - | `False` | Maritime Mobile Service Identity associated with this vessel when available. |
| `name` | *string* (optional) | - | `False` | Reported vessel name. |
| `name_prefix` | *string* (optional) | - | `False` | Reported vessel-name prefix such as ms when available. |
| `imo_lloyds` | *int32* (optional) | - | `False` | IMO or Lloyd's number associated with the vessel when available. |
| `radio_call_sign` | *string* (optional) | - | `False` | Radio call sign associated with the vessel when available. |
| `radio_call_sign_type` | *string* (optional) | - | `False` | Type of radio call sign reported by Digitraffic, for example REAL. |
| `data_source` | *string* (optional) | - | `False` | Upstream data source reported by Digitraffic for the vessel metadata, for example Portnet. |
| `vessel_construction` | *{'$ref': '#/definitions/VesselConstruction'}* (optional) | - | `False` | Construction and classification attributes for the vessel. |
| `vessel_dimensions` | *{'$ref': '#/definitions/VesselDimensions'}* (optional) | - | `False` | Tonnage and dimensional attributes for the vessel. |
| `vessel_registration` | *{'$ref': '#/definitions/VesselRegistration'}* (optional) | - | `False` | Registry and nationality details for the vessel. |
| `vessel_system` | *{'$ref': '#/definitions/VesselSystem'}* (optional) | - | `False` | System and contact details carried with the vessel metadata. |
## Message Group: fi.digitraffic.marine.portcall.portlocation
---
### Message: fi.digitraffic.marine.portcall.PortLocation
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `fi.digitraffic.marine.portcall.PortLocation` |
| `source` |  | `` | `False` | `https://meri.digitraffic.fi/api/port-call/v1/ports` |
| `subject` |  | `uritemplate` | `False` | `{locode}` |

#### Schema:
##### Object: PortLocation
*Reference record from Digitraffic's Port Call ports API. Each event represents one SafeSeaNet port location keyed by UN/LOCODE together with its point geometry, port-area definitions, and berth catalog from the same upstream snapshot.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `locode` | *string* | - | `True` | UN/LOCODE identifying the port location. This value is used as the CloudEvents subject and Kafka record key for port-location reference events. |
| `data_updated_time` | *datetime* | - | `True` | Timestamp when the ports snapshot used for this location was last updated in Digitraffic. |
| `location_name` | *string* | - | `True` | Human-readable port or location name from the ssnLocations feature properties. |
| `country` | *string* | - | `True` | Country name reported for the location in the ssnLocations feature properties. |
| `longitude` | *double* (optional) | deg | `False` | Longitude of the port location point in decimal degrees east when the upstream feature includes geometry. |
| `latitude` | *double* (optional) | deg | `False` | Latitude of the port location point in decimal degrees north when the upstream feature includes geometry. |
| `port_areas` | array of [Object PortArea](#object-portarea) | - | `True` | Port areas associated with this location from the portAreas feature collection. |
| `berths` | array of [Object Berth](#object-berth) | - | `True` | Berth catalog entries associated with this location from the berths collection. |

---
##### Object: PortArea
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `port_area_code` | *string* | - | `True` | Port-area code identifying one sub-area of the port location. |
| `port_area_name` | *string* | - | `True` | Human-readable name of the port area. |
| `longitude` | *double* (optional) | deg | `False` | Longitude of the port-area point in decimal degrees east when the upstream feature includes geometry. |
| `latitude` | *double* (optional) | deg | `False` | Latitude of the port-area point in decimal degrees north when the upstream feature includes geometry. |

---
##### Object: Berth
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `port_area_code` | *string* | - | `True` | Code of the port area that contains this berth. |
| `berth_code` | *string* | - | `True` | Berth code within the port area. |
| `berth_name` | *string* | - | `True` | Human-readable berth name. |
