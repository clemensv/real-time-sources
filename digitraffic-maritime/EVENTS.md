# Digitraffic Marine Bridge Usage Guide Events

**Digitraffic Marine Bridge** connects to Finland's [Digitraffic](https://www.digitraffic.fi/) MQTT stream for real-time AIS vessel tracking and also polls Digitraffic's Port Call REST APIs for vessel visit and companion reference data. Both paths are forwarded to Kafka as [CloudEvents](https://cloudevents.io/) in JSON format.

## Table of Contents

- [Registry](#registry)
- [Endpoints](#endpoints)
- [Messagegroups](#messagegroups)
- [Schemagroups](#schemagroups)

---

## Registry

| Field | Value |
| --- | --- |
| Endpoints | 4 |
| Messagegroups | 4 |
| Schemagroups | 4 |

## Endpoints

### Endpoint `fi.digitraffic.marine.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`fi.digitraffic.marine.ais`](#messagegroup-fidigitrafficmarineais) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `digitraffic-maritime` |
| Kafka key | `{mmsi}` |
| Deployed | False |

### Endpoint `fi.digitraffic.marine.portcall.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`fi.digitraffic.marine.portcall`](#messagegroup-fidigitrafficmarineportcall) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `digitraffic-maritime` |
| Kafka key | `{port_call_id}` |
| Deployed | False |

### Endpoint `fi.digitraffic.marine.portcall.vesseldetails.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`fi.digitraffic.marine.portcall.vesseldetails`](#messagegroup-fidigitrafficmarineportcallvesseldetails) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `digitraffic-maritime` |
| Kafka key | `{vessel_id}` |
| Deployed | False |

### Endpoint `fi.digitraffic.marine.portcall.portlocation.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`fi.digitraffic.marine.portcall.portlocation`](#messagegroup-fidigitrafficmarineportcallportlocation) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `digitraffic-maritime` |
| Kafka key | `{locode}` |
| Deployed | False |

## Messagegroups

### Messagegroup `fi.digitraffic.marine.ais`
<a id="messagegroup-fidigitrafficmarineais"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `fi.digitraffic.marine.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `fi.digitraffic.marine.ais.VesselLocation`
<a id="message-fidigitrafficmarineaisvessellocation"></a>

| Field | Value |
| --- | --- |
| Name | VesselLocation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/fi.digitraffic.marine.ais.jstruct/schemas/fi.digitraffic.marine.ais.VesselLocation`](#schema-fidigitrafficmarineaisvessellocation) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `fi.digitraffic.marine.ais.VesselLocation` |
| `source` |  | `string` | `False` | `wss://meri.digitraffic.fi/mqtt` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `fi.digitraffic.marine.Kafka` | `KAFKA` | topic `digitraffic-maritime`; key `{mmsi}` |

#### Message `fi.digitraffic.marine.ais.VesselMetadata`
<a id="message-fidigitrafficmarineaisvesselmetadata"></a>

| Field | Value |
| --- | --- |
| Name | VesselMetadata |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/fi.digitraffic.marine.ais.jstruct/schemas/fi.digitraffic.marine.ais.VesselMetadata`](#schema-fidigitrafficmarineaisvesselmetadata) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `fi.digitraffic.marine.ais.VesselMetadata` |
| `source` |  | `string` | `False` | `wss://meri.digitraffic.fi/mqtt` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `fi.digitraffic.marine.Kafka` | `KAFKA` | topic `digitraffic-maritime`; key `{mmsi}` |

### Messagegroup `fi.digitraffic.marine.portcall`
<a id="messagegroup-fidigitrafficmarineportcall"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `fi.digitraffic.marine.portcall.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `fi.digitraffic.marine.portcall.PortCall`
<a id="message-fidigitrafficmarineportcallportcall"></a>

| Field | Value |
| --- | --- |
| Name | PortCall |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/fi.digitraffic.marine.portcall.jstruct/schemas/fi.digitraffic.marine.portcall.PortCall`](#schema-fidigitrafficmarineportcallportcall) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `fi.digitraffic.marine.portcall.PortCall` |
| `source` |  | `string` | `False` | `https://meri.digitraffic.fi/api/port-call/v1/port-calls` |
| `subject` |  | `uritemplate` | `False` | `{port_call_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `fi.digitraffic.marine.portcall.Kafka` | `KAFKA` | topic `digitraffic-maritime`; key `{port_call_id}` |

### Messagegroup `fi.digitraffic.marine.portcall.vesseldetails`
<a id="messagegroup-fidigitrafficmarineportcallvesseldetails"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `fi.digitraffic.marine.portcall.vesseldetails.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `fi.digitraffic.marine.portcall.VesselDetails`
<a id="message-fidigitrafficmarineportcallvesseldetails"></a>

| Field | Value |
| --- | --- |
| Name | VesselDetails |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/fi.digitraffic.marine.portcall.reference.jstruct/schemas/fi.digitraffic.marine.portcall.VesselDetails`](#schema-fidigitrafficmarineportcallvesseldetails) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `fi.digitraffic.marine.portcall.VesselDetails` |
| `source` |  | `string` | `False` | `https://meri.digitraffic.fi/api/port-call/v1/vessel-details` |
| `subject` |  | `uritemplate` | `False` | `{vessel_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `fi.digitraffic.marine.portcall.vesseldetails.Kafka` | `KAFKA` | topic `digitraffic-maritime`; key `{vessel_id}` |

### Messagegroup `fi.digitraffic.marine.portcall.portlocation`
<a id="messagegroup-fidigitrafficmarineportcallportlocation"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `fi.digitraffic.marine.portcall.portlocation.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `fi.digitraffic.marine.portcall.PortLocation`
<a id="message-fidigitrafficmarineportcallportlocation"></a>

| Field | Value |
| --- | --- |
| Name | PortLocation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/fi.digitraffic.marine.portcall.reference.jstruct/schemas/fi.digitraffic.marine.portcall.PortLocation`](#schema-fidigitrafficmarineportcallportlocation) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `fi.digitraffic.marine.portcall.PortLocation` |
| `source` |  | `string` | `False` | `https://meri.digitraffic.fi/api/port-call/v1/ports` |
| `subject` |  | `uritemplate` | `False` | `{locode}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `fi.digitraffic.marine.portcall.portlocation.Kafka` | `KAFKA` | topic `digitraffic-maritime`; key `{locode}` |

## Schemagroups

### Schemagroup `fi.digitraffic.marine.ais.jstruct`
<a id="schemagroup-fidigitrafficmarineaisjstruct"></a>

#### Schema `fi.digitraffic.marine.ais.VesselLocation`
<a id="schema-fidigitrafficmarineaisvessellocation"></a>

| Field | Value |
| --- | --- |
| Name | VesselLocation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/fi/digitraffic/marine/ais/VesselLocation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `VesselLocation`
<a id="schema-node-vessellocation"></a>

AIS vessel position report from Digitraffic MQTT stream. Represents a decoded AIS message type 1/2/3/18/19 position update.

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/fi/digitraffic/marine/ais/VesselLocation` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `mmsi` | `int32` | `False` |  | - | - | - |
| `time` | `int32` | `True` |  | - | - | - |
| `sog` | `double` | `True` |  | - | - | - |
| `cog` | `double` | `True` |  | - | - | - |
| `navStat` | `int32` | `True` |  | - | - | - |
| `rot` | `int32` | `True` |  | - | - | - |
| `posAcc` | `boolean` | `True` |  | - | - | - |
| `raim` | `boolean` | `True` |  | - | - | - |
| `heading` | `int32` | `True` |  | - | - | - |
| `lon` | `double` | `True` |  | - | - | - |
| `lat` | `double` | `True` |  | - | - | - |

#### Schema `fi.digitraffic.marine.ais.VesselMetadata`
<a id="schema-fidigitrafficmarineaisvesselmetadata"></a>

| Field | Value |
| --- | --- |
| Name | VesselMetadata |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/fi/digitraffic/marine/ais/VesselMetadata` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `VesselMetadata`
<a id="schema-node-vesselmetadata"></a>

AIS vessel static and voyage data from Digitraffic MQTT stream. Represents decoded AIS message type 5/24 data.

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/fi/digitraffic/marine/ais/VesselMetadata` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `mmsi` | `int32` | `False` |  | - | - | - |
| `timestamp` | `int32` | `True` |  | - | - | - |
| `name` | `string` | `False` |  | - | - | - |
| `callSign` | `string` | `False` |  | - | - | - |
| `imo` | `int32` | `False` |  | - | - | - |
| `type` | `int32` | `False` |  | - | - | - |
| `draught` | `int32` | `False` |  | - | - | - |
| `eta` | `int32` | `False` |  | - | - | - |
| `destination` | `string` | `False` |  | - | - | - |
| `posType` | `int32` | `False` |  | - | - | - |
| `refA` | `int32` | `False` |  | - | - | - |
| `refB` | `int32` | `False` |  | - | - | - |
| `refC` | `int32` | `False` |  | - | - | - |
| `refD` | `int32` | `False` |  | - | - | - |

### Schemagroup `fi.digitraffic.marine.portcall.jstruct`
<a id="schemagroup-fidigitrafficmarineportcalljstruct"></a>

#### Schema `fi.digitraffic.marine.portcall.PortCall`
<a id="schema-fidigitrafficmarineportcallportcall"></a>

| Field | Value |
| --- | --- |
| Name | PortCall |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://meri.digitraffic.fi/schemas/fi/digitraffic/marine/portcall/PortCall` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `PortCall`
<a id="schema-node-portcall"></a>

Port call update from Digitraffic's Portnet-backed port-call API. Each event represents one vessel visit plan or update keyed by the Digitraffic port call identifier and carries the vessel identity, routing context, assigned agents, and berth-area timing details.

| Field | Value |
| --- | --- |
| $id | `https://meri.digitraffic.fi/schemas/fi/digitraffic/marine/portcall/PortCall` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `port_call_id` | `int32` | `True` | Digitraffic port call identifier for this Portnet vessel visit record. | - | - | - |
| `updated_at` | `datetime` | `True` | Timestamp when this port call record was last updated in Digitraffic, from the portCallTimestamp field. | - | - | - |
| `customs_reference` | `union` | `False` | Customs reference string carried with the port call when available. | - | - | - |
| `port_to_visit` | `string` | `True` | UN/LOCODE of the destination port that this call is scheduled to visit. | - | - | - |
| `previous_port` | `union` | `False` | UN/LOCODE of the vessel's previous port when reported by Portnet. | - | - | - |
| `next_port` | `union` | `False` | UN/LOCODE of the vessel's next announced port when reported by Portnet. | - | - | - |
| `mmsi` | `union` | `False` | Maritime Mobile Service Identity associated with the visiting vessel, when available. | - | - | - |
| `imo_lloyds` | `union` | `False` | IMO or Lloyd's vessel number carried with the port call when available. | - | - | - |
| `vessel_name` | `string` | `True` | Reported vessel name for the visit. | - | - | - |
| `vessel_name_prefix` | `union` | `False` | Reported vessel name prefix such as 'ms' or 'mt' when present. | - | - | - |
| `radio_call_sign` | `union` | `False` | Radio call sign for the visiting vessel when reported by Portnet. | - | - | - |
| `nationality` | `union` | `False` | Flag or nationality code reported for the vessel. | - | - | - |
| `vessel_type_code` | `union` | `False` | Digitraffic vessel type code for the visiting vessel. | - | - | - |
| `domestic_traffic_arrival` | `boolean` | `True` | True when the arrival leg is domestic traffic. | - | - | - |
| `domestic_traffic_departure` | `boolean` | `True` | True when the departure leg is domestic traffic. | - | - | - |
| `arrival_with_cargo` | `boolean` | `True` | True when the vessel is reported as arriving with cargo. | - | - | - |
| `not_loading` | `boolean` | `True` | True when the vessel is reported as not loading cargo at the call. | - | - | - |
| `discharge` | `union` | `False` | Digitraffic discharge indicator value for the call when reported. | - | - | - |
| `current_security_level` | `union` | `False` | Current ISPS security level reported for the vessel at this call. | - | - | - |
| `agents` | array of [object `PortCallAgent`](#schema-node-portcallagent) | `True` | Agent and manager organizations attached to the port call. | - | - | - |
| `port_areas` | array of [object `PortCallAreaDetail`](#schema-node-portcallareadetail) | `True` | Planned or actual berth and port-area timing details associated with the call. | - | - | - |

###### Object `PortCallAgent`
<a id="schema-node-portcallagent"></a>

One agent or manager assignment attached to the port call.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `name` | `string` | `True` | Organization name for the assigned ship agent or manager. | - | - | - |
| `port_call_direction` | `string` | `True` | Direction scope for the assignment, such as arrival, departure, or whole port call. | - | - | - |
| `role` | `int32` | `True` | Digitraffic role code for the assignment, for example agent or ship manager. | - | - | - |

###### Object `PortCallAreaDetail`
<a id="schema-node-portcallareadetail"></a>

A berth or port-area schedule detail attached to the port call.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `port_area_code` | `union` | `False` | Code of the destination port area when assigned. | - | - | - |
| `port_area_name` | `union` | `False` | Human-readable name of the destination port area when assigned. | - | - | - |
| `berth_code` | `union` | `False` | Berth code within the destination port area when assigned. | - | - | - |
| `berth_name` | `union` | `False` | Human-readable berth name when assigned. | - | - | - |
| `eta` | `union` | `False` | Estimated time of arrival for this port-area assignment. | - | - | - |
| `eta_source` | `union` | `False` | Source of the ETA value, for example an agent update. | - | - | - |
| `etd` | `union` | `False` | Estimated time of departure for this port-area assignment. | - | - | - |
| `etd_source` | `union` | `False` | Source of the ETD value, for example an agent update. | - | - | - |
| `ata` | `union` | `False` | Actual time of arrival for this port-area assignment when recorded. | - | - | - |
| `ata_source` | `union` | `False` | Source of the ATA value when recorded. | - | - | - |
| `atd` | `union` | `False` | Actual time of departure for this port-area assignment when recorded. | - | - | - |
| `atd_source` | `union` | `False` | Source of the ATD value when recorded. | - | - | - |
| `arrival_draught` | `double` | `True` | Arrival draught reported for this berth or port-area assignment in meters. | unit=`m` symbol=`m` | - | - |
| `departure_draught` | `double` | `True` | Departure draught reported for this berth or port-area assignment in meters. | unit=`m` symbol=`m` | - | - |

### Schemagroup `fi.digitraffic.marine.portcall.reference.jstruct`
<a id="schemagroup-fidigitrafficmarineportcallreferencejstruct"></a>

#### Schema `fi.digitraffic.marine.portcall.VesselDetails`
<a id="schema-fidigitrafficmarineportcallvesseldetails"></a>

| Field | Value |
| --- | --- |
| Name | VesselDetails |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://meri.digitraffic.fi/schemas/fi/digitraffic/marine/portcall/VesselDetails` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `VesselDetails`
<a id="schema-node-vesseldetails"></a>

Reference record from Digitraffic's Port Call vessel-details API. Each event represents the current known metadata for one vessel entity keyed by Digitraffic's stable vessel identifier and includes identity, construction, dimensions, registration, and contact details sourced from Portnet.

| Field | Value |
| --- | --- |
| $id | `https://meri.digitraffic.fi/schemas/fi/digitraffic/marine/portcall/VesselDetails` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `vessel_id` | `integer` | `True` | Digitraffic vessel identifier from the vesselId field. This is the stable identifier used as the CloudEvents subject and Kafka record key for vessel reference events. | - | - | - |
| `updated_at` | `datetime` | `True` | Timestamp when Digitraffic last updated the vessel metadata record, from the updateTimestamp field. | - | - | - |
| `mmsi` | `union` | `False` | Maritime Mobile Service Identity associated with this vessel when available. | - | - | - |
| `name` | `union` | `False` | Reported vessel name. | - | - | - |
| `name_prefix` | `union` | `False` | Reported vessel-name prefix such as ms when available. | - | - | - |
| `imo_lloyds` | `union` | `False` | IMO or Lloyd's number associated with the vessel when available. | - | - | - |
| `radio_call_sign` | `union` | `False` | Radio call sign associated with the vessel when available. | - | - | - |
| `radio_call_sign_type` | `union` | `False` | Type of radio call sign reported by Digitraffic, for example REAL. | - | - | - |
| `data_source` | `union` | `False` | Upstream data source reported by Digitraffic for the vessel metadata, for example Portnet. | - | - | - |
| `vessel_construction` | `union` | `False` | Construction and classification attributes for the vessel. | - | - | - |
| `vessel_dimensions` | `union` | `False` | Tonnage and dimensional attributes for the vessel. | - | - | - |
| `vessel_registration` | `union` | `False` | Registry and nationality details for the vessel. | - | - | - |
| `vessel_system` | `union` | `False` | System and contact details carried with the vessel metadata. | - | - | - |

#### Schema `fi.digitraffic.marine.portcall.PortLocation`
<a id="schema-fidigitrafficmarineportcallportlocation"></a>

| Field | Value |
| --- | --- |
| Name | PortLocation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://meri.digitraffic.fi/schemas/fi/digitraffic/marine/portcall/PortLocation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `PortLocation`
<a id="schema-node-portlocation"></a>

Reference record from Digitraffic's Port Call ports API. Each event represents one SafeSeaNet port location keyed by UN/LOCODE together with its point geometry, port-area definitions, and berth catalog from the same upstream snapshot.

| Field | Value |
| --- | --- |
| $id | `https://meri.digitraffic.fi/schemas/fi/digitraffic/marine/portcall/PortLocation` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `locode` | `string` | `True` | UN/LOCODE identifying the port location. This value is used as the CloudEvents subject and Kafka record key for port-location reference events. | - | - | - |
| `data_updated_time` | `datetime` | `True` | Timestamp when the ports snapshot used for this location was last updated in Digitraffic. | - | - | - |
| `location_name` | `string` | `True` | Human-readable port or location name from the ssnLocations feature properties. | - | - | - |
| `country` | `string` | `True` | Country name reported for the location in the ssnLocations feature properties. | - | - | - |
| `longitude` | `union` | `False` | Longitude of the port location point in decimal degrees east when the upstream feature includes geometry. | unit=`deg` symbol=`deg` | - | - |
| `latitude` | `union` | `False` | Latitude of the port location point in decimal degrees north when the upstream feature includes geometry. | unit=`deg` symbol=`deg` | - | - |
| `port_areas` | array of [object `PortArea`](#schema-node-portarea) | `True` | Port areas associated with this location from the portAreas feature collection. | - | - | - |
| `berths` | array of [object `Berth`](#schema-node-berth) | `True` | Berth catalog entries associated with this location from the berths collection. | - | - | - |

###### Object `PortArea`
<a id="schema-node-portarea"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `port_area_code` | `string` | `True` | Port-area code identifying one sub-area of the port location. | - | - | - |
| `port_area_name` | `string` | `True` | Human-readable name of the port area. | - | - | - |
| `longitude` | `union` | `False` | Longitude of the port-area point in decimal degrees east when the upstream feature includes geometry. | unit=`deg` symbol=`deg` | - | - |
| `latitude` | `union` | `False` | Latitude of the port-area point in decimal degrees north when the upstream feature includes geometry. | unit=`deg` symbol=`deg` | - | - |

###### Object `Berth`
<a id="schema-node-berth"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `port_area_code` | `string` | `True` | Code of the port area that contains this berth. | - | - | - |
| `berth_code` | `string` | `True` | Berth code within the port area. | - | - | - |
| `berth_name` | `string` | `True` | Human-readable berth name. | - | - | - |

### Schemagroup `fi.digitraffic.marine.ais.avro`
<a id="schemagroup-fidigitrafficmarineaisavro"></a>

#### Schema `fi.digitraffic.marine.ais.VesselLocation`
<a id="schema-fidigitrafficmarineaisvessellocation"></a>

| Field | Value |
| --- | --- |
| Name | VesselLocation |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | VesselLocation |
| Namespace | - |
| Type | `record` |
| Doc | AIS vessel position report from Digitraffic MQTT stream. Represents a decoded AIS message type 1/2/3/18/19 position update. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `mmsi` | `null` \| `int` |  | `-` |
| `time` | `int` |  | `-` |
| `sog` | `double` |  | `-` |
| `cog` | `double` |  | `-` |
| `navStat` | `int` |  | `-` |
| `rot` | `int` |  | `-` |
| `posAcc` | `boolean` |  | `-` |
| `raim` | `boolean` |  | `-` |
| `heading` | `int` |  | `-` |
| `lon` | `double` |  | `-` |
| `lat` | `double` |  | `-` |

#### Schema `fi.digitraffic.marine.ais.VesselMetadata`
<a id="schema-fidigitrafficmarineaisvesselmetadata"></a>

| Field | Value |
| --- | --- |
| Name | VesselMetadata |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | VesselMetadata |
| Namespace | - |
| Type | `record` |
| Doc | AIS vessel static and voyage data from Digitraffic MQTT stream. Represents decoded AIS message type 5/24 data. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `mmsi` | `null` \| `int` |  | `-` |
| `timestamp` | `int` |  | `-` |
| `name` | `null` \| `string` |  | `-` |
| `callSign` | `null` \| `string` |  | `-` |
| `imo` | `null` \| `int` |  | `-` |
| `type` | `null` \| `int` |  | `-` |
| `draught` | `null` \| `int` |  | `-` |
| `eta` | `null` \| `int` |  | `-` |
| `destination` | `null` \| `string` |  | `-` |
| `posType` | `null` \| `int` |  | `-` |
| `refA` | `null` \| `int` |  | `-` |
| `refB` | `null` \| `int` |  | `-` |
| `refC` | `null` \| `int` |  | `-` |
| `refD` | `null` \| `int` |  | `-` |
