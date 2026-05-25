# NDW Road Traffic Events

Real-time road traffic data from the Dutch [Nationaal Dataportaal Wegverkeer (NDW)](https://www.ndw.nu/), the Netherlands national road traffic data platform. Provides live traffic speed, travel time, Dynamic Route Information Panel (DRIP) signs, Matrix Signal Installation (MSI) lane signals, and situation events (road works, bridge openings, temporary closures, speed limits, safety messages) for the Dutch national road network (rijkswegen and provinciale wegen).

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
| Schemagroups | 1 |

## Endpoints

### Endpoint `NL.NDW.AVG.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`NL.NDW.AVG`](#messagegroup-nlndwavg) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `ndw-road-traffic` |
| Kafka key | `measurement-sites/{measurement_site_id}` |
| Deployed | False |

### Endpoint `NL.NDW.DRIP.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`NL.NDW.DRIP`](#messagegroup-nlndwdrip) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `ndw-road-traffic` |
| Kafka key | `drips/{vms_controller_id}/{vms_index}` |
| Deployed | False |

### Endpoint `NL.NDW.MSI.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`NL.NDW.MSI`](#messagegroup-nlndwmsi) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `ndw-road-traffic` |
| Kafka key | `msi-signs/{sign_id}` |
| Deployed | False |

### Endpoint `NL.NDW.Situations.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`NL.NDW.Situations`](#messagegroup-nlndwsituations) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `ndw-road-traffic` |
| Kafka key | `situations/{situation_record_id}` |
| Deployed | False |

## Messagegroups

### Messagegroup `NL.NDW.AVG`
<a id="messagegroup-nlndwavg"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `NL.NDW.AVG.Kafka` (KAFKA) |
| Messages | 4 |

#### Message `NL.NDW.AVG.PointMeasurementSite`
<a id="message-nlndwavgpointmeasurementsite"></a>

Reference record for a point measurement site from the Dutch NDW DATEX II measurement_current feed. Contains location, sensor technology type, and lane configuration for a fixed inductive-loop or microwave sensor.

| Field | Value |
| --- | --- |
| Name | PointMeasurementSite |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NL.NDW.jstruct/schemas/NL.NDW.AVG.PointMeasurementSite`](#schema-nlndwavgpointmeasurementsite) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NL.NDW.AVG.PointMeasurementSite` |
| `source` |  | `string` | `False` | `https://opendata.ndw.nu/measurement_current.xml.gz` |
| `subject` |  | `uritemplate` | `False` | `measurement-sites/{measurement_site_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NL.NDW.AVG.Kafka` | `KAFKA` | topic `ndw-road-traffic`; key `measurement-sites/{measurement_site_id}` |

#### Message `NL.NDW.AVG.RouteMeasurementSite`
<a id="message-nlndwavgroutemeasurementsite"></a>

Reference record for a route (section) measurement site from the Dutch NDW DATEX II measurement_current feed. Covers a road segment between two coordinates used for travel time computation.

| Field | Value |
| --- | --- |
| Name | RouteMeasurementSite |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NL.NDW.jstruct/schemas/NL.NDW.AVG.RouteMeasurementSite`](#schema-nlndwavgroutemeasurementsite) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NL.NDW.AVG.RouteMeasurementSite` |
| `source` |  | `string` | `False` | `https://opendata.ndw.nu/measurement_current.xml.gz` |
| `subject` |  | `uritemplate` | `False` | `measurement-sites/{measurement_site_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NL.NDW.AVG.Kafka` | `KAFKA` | topic `ndw-road-traffic`; key `measurement-sites/{measurement_site_id}` |

#### Message `NL.NDW.AVG.TrafficObservation`
<a id="message-nlndwavgtrafficobservation"></a>

Aggregated traffic speed and flow observation from the Dutch NDW DATEX II trafficspeed feed. Each record represents one measurement site with speed averaged and flow summed across all reporting lanes.

| Field | Value |
| --- | --- |
| Name | TrafficObservation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NL.NDW.jstruct/schemas/NL.NDW.AVG.TrafficObservation`](#schema-nlndwavgtrafficobservation) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NL.NDW.AVG.TrafficObservation` |
| `source` |  | `string` | `False` | `https://opendata.ndw.nu/trafficspeed.xml.gz` |
| `subject` |  | `uritemplate` | `False` | `measurement-sites/{measurement_site_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NL.NDW.AVG.Kafka` | `KAFKA` | topic `ndw-road-traffic`; key `measurement-sites/{measurement_site_id}` |

#### Message `NL.NDW.AVG.TravelTimeObservation`
<a id="message-nlndwavgtraveltimeobservation"></a>

Travel time observation for a road segment from the Dutch NDW DATEX II traveltime feed. Contains the actual measured travel time and the static free-flow reference time for a route measurement site.

| Field | Value |
| --- | --- |
| Name | TravelTimeObservation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NL.NDW.jstruct/schemas/NL.NDW.AVG.TravelTimeObservation`](#schema-nlndwavgtraveltimeobservation) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NL.NDW.AVG.TravelTimeObservation` |
| `source` |  | `string` | `False` | `https://opendata.ndw.nu/traveltime.xml.gz` |
| `subject` |  | `uritemplate` | `False` | `measurement-sites/{measurement_site_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NL.NDW.AVG.Kafka` | `KAFKA` | topic `ndw-road-traffic`; key `measurement-sites/{measurement_site_id}` |

### Messagegroup `NL.NDW.DRIP`
<a id="messagegroup-nlndwdrip"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `NL.NDW.DRIP.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `NL.NDW.DRIP.DripSign`
<a id="message-nlndwdripdripsign"></a>

Reference record for a Dynamic Route Information Panel (DRIP) sign from the Dutch NDW DATEX II dynamische_route_informatie_paneel feed. Describes the physical installation, location, and type of an individual VMS sign unit.

| Field | Value |
| --- | --- |
| Name | DripSign |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NL.NDW.jstruct/schemas/NL.NDW.DRIP.DripSign`](#schema-nlndwdripdripsign) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NL.NDW.DRIP.DripSign` |
| `source` |  | `string` | `False` | `https://opendata.ndw.nu/dynamische_route_informatie_paneel.xml.gz` |
| `subject` |  | `uritemplate` | `False` | `drips/{vms_controller_id}/{vms_index}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NL.NDW.DRIP.Kafka` | `KAFKA` | topic `ndw-road-traffic`; key `drips/{vms_controller_id}/{vms_index}` |

#### Message `NL.NDW.DRIP.DripDisplayState`
<a id="message-nlndwdripdripdisplaystate"></a>

Current display state of a Dynamic Route Information Panel (DRIP) sign from the Dutch NDW DATEX II dynamische_route_informatie_paneel feed. Captures the active text, pictogram codes, and operational state of the sign.

| Field | Value |
| --- | --- |
| Name | DripDisplayState |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NL.NDW.jstruct/schemas/NL.NDW.DRIP.DripDisplayState`](#schema-nlndwdripdripdisplaystate) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NL.NDW.DRIP.DripDisplayState` |
| `source` |  | `string` | `False` | `https://opendata.ndw.nu/dynamische_route_informatie_paneel.xml.gz` |
| `subject` |  | `uritemplate` | `False` | `drips/{vms_controller_id}/{vms_index}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NL.NDW.DRIP.Kafka` | `KAFKA` | topic `ndw-road-traffic`; key `drips/{vms_controller_id}/{vms_index}` |

### Messagegroup `NL.NDW.MSI`
<a id="messagegroup-nlndwmsi"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `NL.NDW.MSI.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `NL.NDW.MSI.MsiSign`
<a id="message-nlndwmsimsisign"></a>

Reference record for a Matrix Signal Installation (MSI) sign from the Dutch NDW DATEX II Matrixsignaalinformatie feed. Describes the physical location, lane assignment, and type of a matrix signal sign above a motorway lane.

| Field | Value |
| --- | --- |
| Name | MsiSign |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NL.NDW.jstruct/schemas/NL.NDW.MSI.MsiSign`](#schema-nlndwmsimsisign) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NL.NDW.MSI.MsiSign` |
| `source` |  | `string` | `False` | `https://opendata.ndw.nu/Matrixsignaalinformatie.xml.gz` |
| `subject` |  | `uritemplate` | `False` | `msi-signs/{sign_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NL.NDW.MSI.Kafka` | `KAFKA` | topic `ndw-road-traffic`; key `msi-signs/{sign_id}` |

#### Message `NL.NDW.MSI.MsiDisplayState`
<a id="message-nlndwmsimsidisplaystate"></a>

Current display state of a Matrix Signal Installation (MSI) sign from the Dutch NDW DATEX II Matrixsignaalinformatie feed. Captures the displayed image code, operational state, and any speed limit shown.

| Field | Value |
| --- | --- |
| Name | MsiDisplayState |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NL.NDW.jstruct/schemas/NL.NDW.MSI.MsiDisplayState`](#schema-nlndwmsimsidisplaystate) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NL.NDW.MSI.MsiDisplayState` |
| `source` |  | `string` | `False` | `https://opendata.ndw.nu/Matrixsignaalinformatie.xml.gz` |
| `subject` |  | `uritemplate` | `False` | `msi-signs/{sign_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NL.NDW.MSI.Kafka` | `KAFKA` | topic `ndw-road-traffic`; key `msi-signs/{sign_id}` |

### Messagegroup `NL.NDW.Situations`
<a id="messagegroup-nlndwsituations"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `NL.NDW.Situations.Kafka` (KAFKA) |
| Messages | 5 |

#### Message `NL.NDW.Situations.Roadwork`
<a id="message-nlndwsituationsroadwork"></a>

Road construction or maintenance work event from the Dutch NDW DATEX II planningsfeed_wegwerkzaamheden_en_evenementen feed. Represents a planned or active roadwork situation on the Dutch national road network.

| Field | Value |
| --- | --- |
| Name | Roadwork |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NL.NDW.jstruct/schemas/NL.NDW.Situations.Roadwork`](#schema-nlndwsituationsroadwork) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NL.NDW.Situations.Roadwork` |
| `source` |  | `string` | `False` | `https://opendata.ndw.nu/planningsfeed_wegwerkzaamheden_en_evenementen.xml.gz` |
| `subject` |  | `uritemplate` | `False` | `situations/{situation_record_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NL.NDW.Situations.Kafka` | `KAFKA` | topic `ndw-road-traffic`; key `situations/{situation_record_id}` |

#### Message `NL.NDW.Situations.BridgeOpening`
<a id="message-nlndwsituationsbridgeopening"></a>

Bridge opening event from the Dutch NDW DATEX II planningsfeed_brugopeningen feed. Represents a scheduled or active bridge opening that causes temporary road closure.

| Field | Value |
| --- | --- |
| Name | BridgeOpening |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NL.NDW.jstruct/schemas/NL.NDW.Situations.BridgeOpening`](#schema-nlndwsituationsbridgeopening) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NL.NDW.Situations.BridgeOpening` |
| `source` |  | `string` | `False` | `https://opendata.ndw.nu/planningsfeed_brugopeningen.xml.gz` |
| `subject` |  | `uritemplate` | `False` | `situations/{situation_record_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NL.NDW.Situations.Kafka` | `KAFKA` | topic `ndw-road-traffic`; key `situations/{situation_record_id}` |

#### Message `NL.NDW.Situations.TemporaryClosure`
<a id="message-nlndwsituationstemporaryclosure"></a>

Temporary road closure from the Dutch NDW DATEX II tijdelijke_verkeersmaatregelen_afsluitingen feed. Represents a temporary closure of a road section or lane on the Dutch national road network.

| Field | Value |
| --- | --- |
| Name | TemporaryClosure |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NL.NDW.jstruct/schemas/NL.NDW.Situations.TemporaryClosure`](#schema-nlndwsituationstemporaryclosure) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NL.NDW.Situations.TemporaryClosure` |
| `source` |  | `string` | `False` | `https://opendata.ndw.nu/tijdelijke_verkeersmaatregelen_afsluitingen.xml.gz` |
| `subject` |  | `uritemplate` | `False` | `situations/{situation_record_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NL.NDW.Situations.Kafka` | `KAFKA` | topic `ndw-road-traffic`; key `situations/{situation_record_id}` |

#### Message `NL.NDW.Situations.TemporarySpeedLimit`
<a id="message-nlndwsituationstemporaryspeedlimit"></a>

Temporary speed limit measure from the Dutch NDW DATEX II tijdelijke_verkeersmaatregelen_maximum_snelheden feed. Represents a temporary reduction in maximum speed on a section of the national road network.

| Field | Value |
| --- | --- |
| Name | TemporarySpeedLimit |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NL.NDW.jstruct/schemas/NL.NDW.Situations.TemporarySpeedLimit`](#schema-nlndwsituationstemporaryspeedlimit) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NL.NDW.Situations.TemporarySpeedLimit` |
| `source` |  | `string` | `False` | `https://opendata.ndw.nu/tijdelijke_verkeersmaatregelen_maximum_snelheden.xml.gz` |
| `subject` |  | `uritemplate` | `False` | `situations/{situation_record_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NL.NDW.Situations.Kafka` | `KAFKA` | topic `ndw-road-traffic`; key `situations/{situation_record_id}` |

#### Message `NL.NDW.Situations.SafetyRelatedMessage`
<a id="message-nlndwsituationssafetyrelatedmessage"></a>

Safety-related traffic information message from the Dutch NDW DATEX II veiligheidsgerelateerde_berichten_srti feed. Contains urgent safety alerts and hazard notifications on the national road network.

| Field | Value |
| --- | --- |
| Name | SafetyRelatedMessage |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NL.NDW.jstruct/schemas/NL.NDW.Situations.SafetyRelatedMessage`](#schema-nlndwsituationssafetyrelatedmessage) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NL.NDW.Situations.SafetyRelatedMessage` |
| `source` |  | `string` | `False` | `https://opendata.ndw.nu/veiligheidsgerelateerde_berichten_srti.xml.gz` |
| `subject` |  | `uritemplate` | `False` | `situations/{situation_record_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NL.NDW.Situations.Kafka` | `KAFKA` | topic `ndw-road-traffic`; key `situations/{situation_record_id}` |

## Schemagroups

### Schemagroup `NL.NDW.jstruct`
<a id="schemagroup-nlndwjstruct"></a>

#### Schema `NL.NDW.AVG.PointMeasurementSite`
<a id="schema-nlndwavgpointmeasurementsite"></a>

| Field | Value |
| --- | --- |
| Name | PointMeasurementSite |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://opendata.ndw.nu/schemas/NL/NDW/AVG/PointMeasurementSite` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `PointMeasurementSite`
<a id="schema-node-pointmeasurementsite"></a>

Reference data for a point measurement site from the NDW DATEX II measurement_current feed. A point site uses a fixed sensor (inductive loop or microwave) to measure speed and flow at a single cross-section of road.

| Field | Value |
| --- | --- |
| $id | `https://opendata.ndw.nu/schemas/NL/NDW/AVG/PointMeasurementSite` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `measurement_site_id` | `string` | `True` | Unique identifier of the NDW measurement site, from the DATEX II measurementSiteRecord id attribute. Example: RWS01_MST_0001-01. | - | - | - |
| `name` | `union` | `False` | Human-readable name of the measurement site from the DATEX II measurementSiteName element. | - | - | - |
| `measurement_site_type` | `union` | `False` | Sensor technology type used at this measurement site, from the DATEX II measurementEquipmentTypeUsed element. Example values: inductionLoop, microwave. | - | - | - |
| `period` | `union` | `False` | Measurement aggregation period in seconds, from the DATEX II measurementSpecificCharacteristics period element. | unit=`s` | - | - |
| `latitude` | `union` | `False` | WGS84 latitude of the measurement point in decimal degrees, from the DATEX II pointByCoordinates/pointCoordinates/latitude element. | unit=`deg` | - | - |
| `longitude` | `union` | `False` | WGS84 longitude of the measurement point in decimal degrees, from the DATEX II pointByCoordinates/pointCoordinates/longitude element. | unit=`deg` | - | - |
| `road_name` | `union` | `False` | Road identifier on which the sensor is located, from the DATEX II roadInformation/roadName element. Example values: A1, N205. | - | - | - |
| `lane_count` | `union` | `False` | Number of lanes monitored at this measurement site, derived from the number of measurementSpecificCharacteristics elements. | - | - | - |
| `carriageway_type` | `union` | `False` | Carriageway type from the DATEX II carriagewayType element. Example values: mainCarriageway, slipRoad, connectingCarriageway. | - | - | - |

#### Schema `NL.NDW.AVG.RouteMeasurementSite`
<a id="schema-nlndwavgroutemeasurementsite"></a>

| Field | Value |
| --- | --- |
| Name | RouteMeasurementSite |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://opendata.ndw.nu/schemas/NL/NDW/AVG/RouteMeasurementSite` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `RouteMeasurementSite`
<a id="schema-node-routemeasurementsite"></a>

Reference data for a route (section) measurement site from the NDW DATEX II measurement_current feed. A route site covers a road segment between two geographic endpoints used for travel time computation.

| Field | Value |
| --- | --- |
| $id | `https://opendata.ndw.nu/schemas/NL/NDW/AVG/RouteMeasurementSite` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `measurement_site_id` | `string` | `True` | Unique identifier of the NDW route measurement site, from the DATEX II measurementSiteRecord id attribute. | - | - | - |
| `name` | `union` | `False` | Human-readable name of the route measurement site from the DATEX II measurementSiteName element. | - | - | - |
| `measurement_site_type` | `union` | `False` | Measurement method type, from the DATEX II measurementEquipmentTypeUsed element. Example values: detectLoop, floatingCar. | - | - | - |
| `period` | `union` | `False` | Measurement aggregation period in seconds, from the DATEX II measurementSpecificCharacteristics period element. | unit=`s` | - | - |
| `start_latitude` | `union` | `False` | WGS84 latitude of the route start point in decimal degrees. | unit=`deg` | - | - |
| `start_longitude` | `union` | `False` | WGS84 longitude of the route start point in decimal degrees. | unit=`deg` | - | - |
| `end_latitude` | `union` | `False` | WGS84 latitude of the route end point in decimal degrees. | unit=`deg` | - | - |
| `end_longitude` | `union` | `False` | WGS84 longitude of the route end point in decimal degrees. | unit=`deg` | - | - |
| `road_name` | `union` | `False` | Road identifier for the route section. Example values: A1, A10, N44. | - | - | - |
| `length_metres` | `union` | `False` | Length of the route section in metres, from the DATEX II length element. | unit=`m` | - | - |

#### Schema `NL.NDW.AVG.TrafficObservation`
<a id="schema-nlndwavgtrafficobservation"></a>

| Field | Value |
| --- | --- |
| Name | TrafficObservation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://opendata.ndw.nu/schemas/NL/NDW/AVG/TrafficObservation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `TrafficObservation`
<a id="schema-node-trafficobservation"></a>

Aggregated traffic speed and flow observation per road segment from the NDW DATEX II trafficspeed feed. Speed is averaged and flow summed across all reporting lanes at the measurement site.

| Field | Value |
| --- | --- |
| $id | `https://opendata.ndw.nu/schemas/NL/NDW/AVG/TrafficObservation` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `measurement_site_id` | `string` | `True` | Unique identifier of the NDW measurement site, from the DATEX II measurementSiteReference id attribute. | - | - | - |
| `measurement_time` | `string` | `True` | Timestamp of the measurement in ISO 8601 UTC format, from the DATEX II measurementTimeDefault element. | - | - | - |
| `average_speed` | `union` | `False` | Average vehicle speed in km/h across all lanes with valid data at this site. Null when no lane reported a valid speed. | unit=`km/h` | - | - |
| `vehicle_flow_rate` | `union` | `False` | Total vehicle flow rate in vehicles per hour, summed across all lanes at this measurement site. Null when no valid flow data was reported. | unit=`vehicles/h` | - | - |
| `number_of_lanes_with_data` | `int32` | `True` | Number of lanes that reported valid measurement data at this measurement site. | - | - | - |

#### Schema `NL.NDW.AVG.TravelTimeObservation`
<a id="schema-nlndwavgtraveltimeobservation"></a>

| Field | Value |
| --- | --- |
| Name | TravelTimeObservation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://opendata.ndw.nu/schemas/NL/NDW/AVG/TravelTimeObservation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `TravelTimeObservation`
<a id="schema-node-traveltimeobservation"></a>

Travel time observation for a road segment from the NDW DATEX II traveltime feed. Contains the actual measured travel time and the static free-flow reference time for a route measurement site.

| Field | Value |
| --- | --- |
| $id | `https://opendata.ndw.nu/schemas/NL/NDW/AVG/TravelTimeObservation` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `measurement_site_id` | `string` | `True` | Unique identifier of the NDW route measurement site, from the DATEX II measurementSiteReference id attribute. | - | - | - |
| `measurement_time` | `string` | `True` | Timestamp of the measurement in ISO 8601 UTC format, from the DATEX II measurementTimeDefault element. | - | - | - |
| `duration` | `union` | `False` | Measured travel time in seconds for the route section, from the DATEX II travelTime/duration element. Null if the upstream value was negative (invalid). | unit=`s` | - | - |
| `reference_duration` | `union` | `False` | Free-flow reference travel time in seconds for the route section, from the DATEX II basicDataReferenceValue/travelTimeData/travelTime/duration extension element. Null if not provided. | unit=`s` | - | - |
| `accuracy` | `union` | `False` | Accuracy percentage of the travel time measurement as a value between 0 and 100, from the DATEX II travelTime accuracy attribute. | unit=`%` | - | - |
| `data_quality` | `union` | `False` | Supplier-calculated data quality score as a value between 0 and 100, from the DATEX II supplierCalculatedDataQuality attribute. | unit=`%` | - | - |
| `number_of_input_values` | `union` | `False` | Number of input observations used to compute the travel time, from the DATEX II numberOfInputValuesUsed attribute. | - | - | - |

#### Schema `NL.NDW.DRIP.DripSign`
<a id="schema-nlndwdripdripsign"></a>

| Field | Value |
| --- | --- |
| Name | DripSign |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://opendata.ndw.nu/schemas/NL/NDW/DRIP/DripSign` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `DripSign`
<a id="schema-node-dripsign"></a>

Reference data for a Dynamic Route Information Panel (DRIP) sign from the NDW DATEX II dynamische_route_informatie_paneel feed. Describes the physical installation, location, and type of an individual VMS sign within a VMS controller.

| Field | Value |
| --- | --- |
| $id | `https://opendata.ndw.nu/schemas/NL/NDW/DRIP/DripSign` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `vms_controller_id` | `string` | `True` | Unique identifier of the VMS controller unit, from the DATEX II vmsUnitRecord id attribute. | - | - | - |
| `vms_index` | `string` | `True` | Index of the individual VMS sign within the controller unit, from the DATEX II vmsRecord index attribute, converted to string. | - | - | - |
| `vms_type` | `union` | `False` | DRIP sign type, from the DATEX II vmsType element. Example values: presignalling, matrixBoardTwoByTwo, matrixBoardOneByTwo. | - | - | - |
| `latitude` | `union` | `False` | WGS84 latitude of the DRIP sign location in decimal degrees. | unit=`deg` | - | - |
| `longitude` | `union` | `False` | WGS84 longitude of the DRIP sign location in decimal degrees. | unit=`deg` | - | - |
| `road_name` | `union` | `False` | Road identifier where the DRIP sign is located. Example values: A1, A10. | - | - | - |
| `description` | `union` | `False` | Human-readable description of the DRIP sign from the DATEX II description element. | - | - | - |

#### Schema `NL.NDW.DRIP.DripDisplayState`
<a id="schema-nlndwdripdripdisplaystate"></a>

| Field | Value |
| --- | --- |
| Name | DripDisplayState |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://opendata.ndw.nu/schemas/NL/NDW/DRIP/DripDisplayState` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `DripDisplayState`
<a id="schema-node-dripdisplaystate"></a>

Current display state of a Dynamic Route Information Panel (DRIP) sign from the NDW DATEX II dynamische_route_informatie_paneel feed. Captures the active text, pictogram codes, and operational state.

| Field | Value |
| --- | --- |
| $id | `https://opendata.ndw.nu/schemas/NL/NDW/DRIP/DripDisplayState` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `vms_controller_id` | `string` | `True` | Unique identifier of the VMS controller unit, from the DATEX II vmsUnitRecord id attribute. | - | - | - |
| `vms_index` | `string` | `True` | Index of the individual VMS sign within the controller unit, converted to string. | - | - | - |
| `publication_time` | `string` | `True` | ISO 8601 UTC timestamp when this display state was published, from the DATEX II publicationTime element. | - | - | - |
| `active` | `union` | `False` | Whether the DRIP sign is currently displaying content. Derived from the DATEX II vmsWorking or displayActive element. | - | - | - |
| `vms_text` | `union` | `False` | Concatenated text from all display panels of the sign, from the DATEX II displayedText/vmsText/vmsTextLine elements. | - | - | - |
| `pictogram_code` | `union` | `False` | Pictogram code displayed on the sign, from the DATEX II pictogramDisplayAreaSettings/vmsPicktogramDisplayCharacteristics/vmsPicktogramDescription element. | - | - | - |
| `state` | `union` | `False` | Operational state of the DRIP sign, from the DATEX II vmsUnitFault or operationalState element. Example values: working, fault, maintenance. | - | - | - |

#### Schema `NL.NDW.MSI.MsiSign`
<a id="schema-nlndwmsimsisign"></a>

| Field | Value |
| --- | --- |
| Name | MsiSign |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://opendata.ndw.nu/schemas/NL/NDW/MSI/MsiSign` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `MsiSign`
<a id="schema-node-msisign"></a>

Reference data for a Matrix Signal Installation (MSI) sign from the NDW DATEX II Matrixsignaalinformatie feed. Describes the physical location, lane assignment, and type of a matrix signal sign above a motorway lane.

| Field | Value |
| --- | --- |
| $id | `https://opendata.ndw.nu/schemas/NL/NDW/MSI/MsiSign` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `sign_id` | `string` | `True` | Unique identifier of the MSI sign, from the DATEX II vmsUnitRecord id attribute. | - | - | - |
| `sign_type` | `union` | `False` | MSI sign type, from the DATEX II vmsType element. Example values: matrixBoardOneByOne, matrixBoardTwoByOne. | - | - | - |
| `latitude` | `union` | `False` | WGS84 latitude of the MSI sign location in decimal degrees. | unit=`deg` | - | - |
| `longitude` | `union` | `False` | WGS84 longitude of the MSI sign location in decimal degrees. | unit=`deg` | - | - |
| `road_name` | `union` | `False` | Road identifier where the MSI sign is located. Example values: A1, A2. | - | - | - |
| `lane` | `union` | `False` | Lane designation above which the MSI sign is installed, from the DATEX II laneNumber element. | - | - | - |
| `description` | `union` | `False` | Human-readable description of the MSI sign installation from the DATEX II description element. | - | - | - |

#### Schema `NL.NDW.MSI.MsiDisplayState`
<a id="schema-nlndwmsimsidisplaystate"></a>

| Field | Value |
| --- | --- |
| Name | MsiDisplayState |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://opendata.ndw.nu/schemas/NL/NDW/MSI/MsiDisplayState` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `MsiDisplayState`
<a id="schema-node-msidisplaystate"></a>

Current display state of a Matrix Signal Installation (MSI) sign from the NDW DATEX II Matrixsignaalinformatie feed. Captures the displayed image code, operational state, and any speed limit shown.

| Field | Value |
| --- | --- |
| $id | `https://opendata.ndw.nu/schemas/NL/NDW/MSI/MsiDisplayState` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `sign_id` | `string` | `True` | Unique identifier of the MSI sign, from the DATEX II vmsUnitRecord id attribute. | - | - | - |
| `publication_time` | `string` | `True` | ISO 8601 UTC timestamp when this display state was published, from the DATEX II publicationTime element. | - | - | - |
| `image_code` | `union` | `False` | Code of the image currently displayed on the MSI sign, from the DATEX II imageCode or displayedText element. Example values: blank, closed, 70, 80, 100, arrow_left. | - | - | - |
| `state` | `union` | `False` | Operational state derived from the displayed image. Example values: open, closed, speed_limit. | - | - | - |
| `speed_limit` | `union` | `False` | Speed limit in km/h displayed on the sign when showing a speed limit image. Null when the sign is blank or shows a non-numeric image. | unit=`km/h` | - | - |

#### Schema `NL.NDW.Situations.Roadwork`
<a id="schema-nlndwsituationsroadwork"></a>

| Field | Value |
| --- | --- |
| Name | Roadwork |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://opendata.ndw.nu/schemas/NL/NDW/Situations/Roadwork` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Roadwork`
<a id="schema-node-roadwork"></a>

Road construction or maintenance work event from the NDW DATEX II planningsfeed_wegwerkzaamheden_en_evenementen feed. Represents a planned or active roadwork situation on the Dutch national road network.

| Field | Value |
| --- | --- |
| $id | `https://opendata.ndw.nu/schemas/NL/NDW/Situations/Roadwork` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `situation_record_id` | `string` | `True` | Unique identifier of the situation record, from the DATEX II situationRecord id attribute. | - | - | - |
| `version_time` | `string` | `True` | ISO 8601 UTC timestamp when this situation record version was created, from the DATEX II situationVersionTime element. | - | - | - |
| `validity_status` | `union` | `False` | Validity status of the situation record, from the DATEX II validityStatus element. Example values: active, suspended, definedByValidityTimeSpec. | - | - | - |
| `start_time` | `union` | `False` | ISO 8601 UTC timestamp when the roadwork validity period starts, from the DATEX II overallStartTime element. | - | - | - |
| `end_time` | `union` | `False` | ISO 8601 UTC timestamp when the roadwork validity period ends, from the DATEX II overallEndTime element. Null for open-ended situations. | - | - | - |
| `road_name` | `union` | `False` | Road name or identifier where the roadwork is located. | - | - | - |
| `description` | `union` | `False` | Human-readable description of the roadwork situation from the DATEX II comment or description element. | - | - | - |
| `location_description` | `union` | `False` | Human-readable description of the roadwork location from the DATEX II locationDescriptor element. | - | - | - |
| `probability` | `union` | `False` | Probability of occurrence for the roadwork, from the DATEX II probabilityOfOccurrence element. Example values: certain, probable, risk. | - | - | - |
| `severity` | `union` | `False` | Overall severity of the roadwork impact, from the DATEX II severity element. Example values: highest, high, medium, low, lowest. | - | - | - |
| `management_type` | `union` | `False` | Type of road management applied, from the DATEX II roadMaintenanceType or managementType element. Example values: laneClosures, carriagewayClosure. | - | - | - |

#### Schema `NL.NDW.Situations.BridgeOpening`
<a id="schema-nlndwsituationsbridgeopening"></a>

| Field | Value |
| --- | --- |
| Name | BridgeOpening |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://opendata.ndw.nu/schemas/NL/NDW/Situations/BridgeOpening` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `BridgeOpening`
<a id="schema-node-bridgeopening"></a>

Bridge opening event from the NDW DATEX II planningsfeed_brugopeningen feed. Represents a scheduled or active bridge opening that causes a temporary road closure on the Dutch road network.

| Field | Value |
| --- | --- |
| $id | `https://opendata.ndw.nu/schemas/NL/NDW/Situations/BridgeOpening` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `situation_record_id` | `string` | `True` | Unique identifier of the situation record, from the DATEX II situationRecord id attribute. | - | - | - |
| `version_time` | `string` | `True` | ISO 8601 UTC timestamp when this situation record version was created, from the DATEX II situationVersionTime element. | - | - | - |
| `validity_status` | `union` | `False` | Validity status of the bridge opening record from the DATEX II validityStatus element. | - | - | - |
| `start_time` | `union` | `False` | ISO 8601 UTC timestamp when the bridge opening starts. | - | - | - |
| `end_time` | `union` | `False` | ISO 8601 UTC timestamp when the bridge opening ends and the road reopens. | - | - | - |
| `bridge_name` | `union` | `False` | Name of the bridge being opened, from the DATEX II bridgeName or locationName element. | - | - | - |
| `road_name` | `union` | `False` | Road identifier that is affected by the bridge opening. | - | - | - |
| `description` | `union` | `False` | Human-readable description of the bridge opening event from the DATEX II comment or description element. | - | - | - |

#### Schema `NL.NDW.Situations.TemporaryClosure`
<a id="schema-nlndwsituationstemporaryclosure"></a>

| Field | Value |
| --- | --- |
| Name | TemporaryClosure |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://opendata.ndw.nu/schemas/NL/NDW/Situations/TemporaryClosure` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `TemporaryClosure`
<a id="schema-node-temporaryclosure"></a>

Temporary road closure from the NDW DATEX II tijdelijke_verkeersmaatregelen_afsluitingen feed. Represents a temporary closure of a road section or individual lanes on the Dutch national road network.

| Field | Value |
| --- | --- |
| $id | `https://opendata.ndw.nu/schemas/NL/NDW/Situations/TemporaryClosure` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `situation_record_id` | `string` | `True` | Unique identifier of the situation record, from the DATEX II situationRecord id attribute. | - | - | - |
| `version_time` | `string` | `True` | ISO 8601 UTC timestamp when this situation record version was created, from the DATEX II situationVersionTime element. | - | - | - |
| `validity_status` | `union` | `False` | Validity status of the temporary closure record from the DATEX II validityStatus element. | - | - | - |
| `start_time` | `union` | `False` | ISO 8601 UTC timestamp when the temporary closure starts. | - | - | - |
| `end_time` | `union` | `False` | ISO 8601 UTC timestamp when the temporary closure ends. | - | - | - |
| `road_name` | `union` | `False` | Road identifier where the temporary closure applies. | - | - | - |
| `description` | `union` | `False` | Human-readable description of the temporary closure from the DATEX II comment or description element. | - | - | - |
| `location_description` | `union` | `False` | Human-readable description of the closure location from the DATEX II locationDescriptor element. | - | - | - |
| `severity` | `union` | `False` | Overall severity of the closure impact, from the DATEX II severity element. | - | - | - |

#### Schema `NL.NDW.Situations.TemporarySpeedLimit`
<a id="schema-nlndwsituationstemporaryspeedlimit"></a>

| Field | Value |
| --- | --- |
| Name | TemporarySpeedLimit |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://opendata.ndw.nu/schemas/NL/NDW/Situations/TemporarySpeedLimit` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `TemporarySpeedLimit`
<a id="schema-node-temporaryspeedlimit"></a>

Temporary speed limit measure from the NDW DATEX II tijdelijke_verkeersmaatregelen_maximum_snelheden feed. Represents a temporary reduction in the maximum allowed speed on a section of the national road network.

| Field | Value |
| --- | --- |
| $id | `https://opendata.ndw.nu/schemas/NL/NDW/Situations/TemporarySpeedLimit` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `situation_record_id` | `string` | `True` | Unique identifier of the situation record, from the DATEX II situationRecord id attribute. | - | - | - |
| `version_time` | `string` | `True` | ISO 8601 UTC timestamp when this situation record version was created, from the DATEX II situationVersionTime element. | - | - | - |
| `validity_status` | `union` | `False` | Validity status of the temporary speed limit record from the DATEX II validityStatus element. | - | - | - |
| `start_time` | `union` | `False` | ISO 8601 UTC timestamp when the temporary speed limit starts. | - | - | - |
| `end_time` | `union` | `False` | ISO 8601 UTC timestamp when the temporary speed limit ends. | - | - | - |
| `road_name` | `union` | `False` | Road identifier where the temporary speed limit applies. | - | - | - |
| `speed_limit_kmh` | `union` | `False` | Temporary maximum speed limit in km/h, from the DATEX II speedLimit/maximumSpeedLimit element. | unit=`km/h` | - | - |
| `description` | `union` | `False` | Human-readable description of the temporary speed limit from the DATEX II comment or description element. | - | - | - |
| `location_description` | `union` | `False` | Human-readable description of the speed limit section location from the DATEX II locationDescriptor element. | - | - | - |

#### Schema `NL.NDW.Situations.SafetyRelatedMessage`
<a id="schema-nlndwsituationssafetyrelatedmessage"></a>

| Field | Value |
| --- | --- |
| Name | SafetyRelatedMessage |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://opendata.ndw.nu/schemas/NL/NDW/Situations/SafetyRelatedMessage` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `SafetyRelatedMessage`
<a id="schema-node-safetyrelatedmessage"></a>

Safety-related traffic information message from the NDW DATEX II veiligheidsgerelateerde_berichten_srti feed. Contains urgent safety alerts and hazard notifications on the national road network.

| Field | Value |
| --- | --- |
| $id | `https://opendata.ndw.nu/schemas/NL/NDW/Situations/SafetyRelatedMessage` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `situation_record_id` | `string` | `True` | Unique identifier of the situation record, from the DATEX II situationRecord id attribute. | - | - | - |
| `version_time` | `string` | `True` | ISO 8601 UTC timestamp when this situation record version was created, from the DATEX II situationVersionTime element. | - | - | - |
| `validity_status` | `union` | `False` | Validity status of the safety message record from the DATEX II validityStatus element. | - | - | - |
| `start_time` | `union` | `False` | ISO 8601 UTC timestamp when the safety-related situation starts. | - | - | - |
| `end_time` | `union` | `False` | ISO 8601 UTC timestamp when the safety-related situation ends. | - | - | - |
| `road_name` | `union` | `False` | Road identifier where the safety-related event is located. | - | - | - |
| `message_type` | `union` | `False` | Type of safety-related message, from the DATEX II xsi:type attribute on the situationRecord. Example values: RoadOrCarriagewayOrLaneManagement, VehicleObstruction, PoorRoadInfrastructure. | - | - | - |
| `description` | `union` | `False` | Human-readable description of the safety-related message from the DATEX II comment or description element. | - | - | - |
| `urgency` | `union` | `False` | Urgency level of the safety message, from the DATEX II urgency element. Example values: extremelyUrgent, urgent, normalUrgency. | - | - | - |
