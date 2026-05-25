# Entur Norway SIRI Bridge Events

Message group for dated service journey reference data and real-time journey telemetry (ET and VM). All messages in this group share the journeys/{operating_day}/{service_journey_id} Kafka key.

## Table of Contents

- [Registry](#registry)
- [Endpoints](#endpoints)
- [Messagegroups](#messagegroups)
- [Schemagroups](#schemagroups)

---

## Registry

| Field | Value |
| --- | --- |
| Endpoints | 3 |
| Messagegroups | 3 |
| Schemagroups | 2 |

## Endpoints

### Endpoint `no.entur.journeys.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`no.entur.journeys`](#messagegroup-noenturjourneys) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `entur-norway` |
| Kafka key | `journeys/{operating_day}/{service_journey_id}` |
| Deployed | False |

### Endpoint `no.entur.situations.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`no.entur.situations`](#messagegroup-noentursituations) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `entur-norway` |
| Kafka key | `situations/{situation_number}` |
| Deployed | False |

### Endpoint `no.entur.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`no.entur.mqtt`](#messagegroup-noenturmqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

## Messagegroups

### Messagegroup `no.entur.journeys`
<a id="messagegroup-noenturjourneys"></a>

| Field | Value |
| --- | --- |
| Name | Entur Journey Events |
| Description | Message group for dated service journey reference data and real-time journey telemetry (ET and VM). All messages in this group share the journeys/{operating_day}/{service_journey_id} Kafka key. |
| Transport bindings | `no.entur.journeys.Kafka` (KAFKA) |
| Messages | 3 |

#### Message `no.entur.DatedServiceJourney`
<a id="message-noenturdatedservicejourney"></a>

Reference data for a dated service journey in the Norwegian public transport network. A DatedServiceJourney is a specific vehicle journey operating on a particular operating day, identified by its NeTEx ServiceJourney reference and operating day. This reference event is emitted at bridge startup from the SIRI-ET feed and refreshed periodically to provide downstream consumers with the timetable context for subsequent telemetry events.

| Field | Value |
| --- | --- |
| Name | DatedServiceJourney |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/no.entur.jstruct/schemas/no.entur.DatedServiceJourney`](#schema-noenturdatedservicejourney) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `no.entur.DatedServiceJourney` |
| `source` |  | `string` | `False` | `https://api.entur.io/realtime/v1/rest/et` |
| `subject` |  | `uritemplate` | `False` | `journeys/{operating_day}/{service_journey_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `no.entur.journeys.Kafka` | `KAFKA` | topic `entur-norway`; key `journeys/{operating_day}/{service_journey_id}` |

#### Message `no.entur.EstimatedVehicleJourney`
<a id="message-noenturestimatedvehiclejourney"></a>

Real-time estimated timetable update for a vehicle journey from the Entur SIRI-ET feed (GET /realtime/v1/rest/et). Contains updated arrival and departure times for each stop along the journey, cancellation flags, and extra journey markers. Uses incremental requestorId polling to receive only changed journeys since the last poll.

| Field | Value |
| --- | --- |
| Name | EstimatedVehicleJourney |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/no.entur.jstruct/schemas/no.entur.EstimatedVehicleJourney`](#schema-noenturestimatedvehiclejourney) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `no.entur.EstimatedVehicleJourney` |
| `source` |  | `string` | `False` | `https://api.entur.io/realtime/v1/rest/et` |
| `subject` |  | `uritemplate` | `False` | `journeys/{operating_day}/{service_journey_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `no.entur.journeys.Kafka` | `KAFKA` | topic `entur-norway`; key `journeys/{operating_day}/{service_journey_id}` |

#### Message `no.entur.MonitoredVehicleJourney`
<a id="message-noenturmonitoredvehiclejourney"></a>

Real-time vehicle monitoring update from the Entur SIRI-VM feed (GET /realtime/v1/rest/vm). Contains the current geographic position of a vehicle, its bearing, delay, occupancy status, and the next monitored call. Uses incremental requestorId polling for efficient change delivery.

| Field | Value |
| --- | --- |
| Name | MonitoredVehicleJourney |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/no.entur.jstruct/schemas/no.entur.MonitoredVehicleJourney`](#schema-noenturmonitoredvehiclejourney) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `no.entur.MonitoredVehicleJourney` |
| `source` |  | `string` | `False` | `https://api.entur.io/realtime/v1/rest/vm` |
| `subject` |  | `uritemplate` | `False` | `journeys/{operating_day}/{service_journey_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `no.entur.journeys.Kafka` | `KAFKA` | topic `entur-norway`; key `journeys/{operating_day}/{service_journey_id}` |

### Messagegroup `no.entur.situations`
<a id="messagegroup-noentursituations"></a>

| Field | Value |
| --- | --- |
| Name | Entur Situation Events |
| Description | Message group for SIRI-SX transit disruption and service alert events. All messages in this group share the situations/{situation_number} Kafka key. |
| Transport bindings | `no.entur.situations.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `no.entur.PtSituationElement`
<a id="message-noenturptsituationelement"></a>

Real-time transit disruption or service alert from the Entur SIRI-SX feed (GET /realtime/v1/rest/sx). Represents a published situation element describing a service disruption, delay cause, or passenger information notice. Includes affected lines, stops, severity level, and validity periods.

| Field | Value |
| --- | --- |
| Name | PtSituationElement |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/no.entur.jstruct/schemas/no.entur.PtSituationElement`](#schema-noenturptsituationelement) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `no.entur.PtSituationElement` |
| `source` |  | `string` | `False` | `https://api.entur.io/realtime/v1/rest/sx` |
| `subject` |  | `uritemplate` | `False` | `situations/{situation_number}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `no.entur.situations.Kafka` | `KAFKA` | topic `entur-norway`; key `situations/{situation_number}` |

### Messagegroup `no.entur.mqtt`
<a id="messagegroup-noenturmqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 transport variant for Entur Norway SIRI real-time feeds. Non-retained QoS-1 streams route Estimated Timetable, Vehicle Monitoring, and Situation Exchange payloads by raw SIRI identifiers under transit/no/entur/entur-norway/... Missing routing fields are emitted as the literal unknown by the bridge. |
| Transport bindings | `no.entur.Mqtt` (MQTT/5.0) |
| Messages | 3 |

#### Message `no.entur.mqtt.EstimatedVehicleJourney`
<a id="message-noenturmqttestimatedvehiclejourney"></a>

Real-time estimated timetable update for a vehicle journey from the Entur SIRI-ET feed (GET /realtime/v1/rest/et). Contains updated arrival and departure times for each stop along the journey, cancellation flags, and extra journey markers. Uses incremental requestorId polling to receive only changed journeys since the last poll.

| Field | Value |
| --- | --- |
| Name | EstimatedVehicleJourney |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/no.entur.jstruct/schemas/no.entur.EstimatedVehicleJourney`](#schema-noenturestimatedvehiclejourney) |
| Base message chain | `/messagegroups/no.entur.journeys/messages/no.entur.EstimatedVehicleJourney` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `no.entur.EstimatedVehicleJourney` |
| `source` |  | `string` | `False` | `https://api.entur.io/realtime/v1/rest/et` |
| `subject` |  | `uritemplate` | `False` | `journeys/{operating_day}/{service_journey_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `no.entur.Mqtt` | `MQTT/5.0` | topic `transit/no/entur/entur-norway/et/{operator_ref}/{line_ref}/{service_journey_id}/estimated-vehicle-journey` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `transit/no/entur/entur-norway/et/{operator_ref}/{line_ref}/{service_journey_id}/estimated-vehicle-journey` |
| QoS | 1 |
| Retain | False |

#### Message `no.entur.mqtt.MonitoredVehicleJourney`
<a id="message-noenturmqttmonitoredvehiclejourney"></a>

Real-time vehicle monitoring update from the Entur SIRI-VM feed (GET /realtime/v1/rest/vm). Contains the current geographic position of a vehicle, its bearing, delay, occupancy status, and the next monitored call. Uses incremental requestorId polling for efficient change delivery.

| Field | Value |
| --- | --- |
| Name | MonitoredVehicleJourney |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/no.entur.jstruct/schemas/no.entur.MonitoredVehicleJourney`](#schema-noenturmonitoredvehiclejourney) |
| Base message chain | `/messagegroups/no.entur.journeys/messages/no.entur.MonitoredVehicleJourney` |
| Transport override | `MQTT/5.0` |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `no.entur.MonitoredVehicleJourney` |
| `source` |  | `string` | `False` | `https://api.entur.io/realtime/v1/rest/vm` |
| `subject` |  | `uritemplate` | `False` | `journeys/{operating_day}/{service_journey_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `no.entur.Mqtt` | `MQTT/5.0` | topic `transit/no/entur/entur-norway/vm/{operator_ref}/{line_ref}/{service_journey_id}/monitored-vehicle-journey` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `transit/no/entur/entur-norway/vm/{operator_ref}/{line_ref}/{service_journey_id}/monitored-vehicle-journey` |
| QoS | 1 |
| Retain | False |

#### Message `no.entur.mqtt.PtSituationElement`
<a id="message-noenturmqttptsituationelement"></a>

Real-time transit disruption or service alert from the Entur SIRI-SX feed (GET /realtime/v1/rest/sx). Represents a published situation element describing a service disruption, delay cause, or passenger information notice. Includes affected lines, stops, severity level, and validity periods.

| Field | Value |
| --- | --- |
| Name | PtSituationElement |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/no.entur.jstruct/schemas/no.entur.PtSituationElement`](#schema-noenturptsituationelement) |
| Base message chain | `/messagegroups/no.entur.situations/messages/no.entur.PtSituationElement` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `no.entur.PtSituationElement` |
| `source` |  | `string` | `False` | `https://api.entur.io/realtime/v1/rest/sx` |
| `subject` |  | `uritemplate` | `False` | `situations/{situation_number}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `no.entur.Mqtt` | `MQTT/5.0` | topic `transit/no/entur/entur-norway/sx/{severity}/{situation_number}/situation` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `transit/no/entur/entur-norway/sx/{severity}/{situation_number}/situation` |
| QoS | 1 |
| Retain | False |

## Schemagroups

### Schemagroup `no.entur.jstruct`
<a id="schemagroup-noenturjstruct"></a>

#### Schema `no.entur.DatedServiceJourney`
<a id="schema-noenturdatedservicejourney"></a>

| Field | Value |
| --- | --- |
| Name | DatedServiceJourney |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://real-time-sources.2030.io/schemas/no/entur/DatedServiceJourney` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/no/entur/DatedServiceJourney` |
| Type | `object` |

###### Object `DatedServiceJourney`
<a id="schema-node-datedservicejourney"></a>

Reference data for a dated service journey in the Norwegian public transport network. A DatedServiceJourney is a specific vehicle journey operating on a particular operating day, identified by its NeTEx ServiceJourney reference (DatedVehicleJourneyRef) and operating day (DataFrameRef). This reference record is extracted from the SIRI-ET feed and published at startup and refresh intervals.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `service_journey_id` | `string` | `True` | NeTEx ServiceJourney identifier extracted from FramedVehicleJourneyRef/DatedVehicleJourneyRef. Uniquely identifies the planned vehicle journey within the NeTEx codespace. Example: RUT:ServiceJourney:1-1234. | altnames=`{"xml": "DatedVehicleJourneyRef"}` | - | - |
| `operating_day` | `string` | `True` | ISO 8601 calendar date string representing the operating day on which this journey runs, extracted from FramedVehicleJourneyRef/DataFrameRef. Example: 2024-01-01. | altnames=`{"xml": "DataFrameRef"}` | pattern=`^\d{4}-\d{2}-\d{2}$` | - |
| `line_ref` | `string` | `True` | NeTEx Line reference identifying the line this journey belongs to. Example: RUT:Line:1. | altnames=`{"xml": "LineRef"}` | - | - |
| `operator_ref` | `string` | `True` | NeTEx Operator or codespace reference identifying the operator responsible for this journey. Example: RUT. | altnames=`{"xml": "OperatorRef"}` | - | - |
| `direction_ref` | `union` | `False` | Direction reference for this journey leg, e.g. Outbound or Inbound, or a NeTEx DirectionType value. | altnames=`{"xml": "DirectionRef"}` | - | - |
| `vehicle_mode` | `union` | `False` | SIRI VehicleMode describing the mode of transport for this journey. Known values: bus, tram, rail, ferry, metro, water, air, coach, taxi. | altnames=`{"xml": "VehicleMode"}`<br>altenums=`["bus", "tram", "rail", "ferry", "metro", "water", "air", "coach", "taxi"]` | - | - |
| `route_ref` | `union` | `False` | NeTEx Route reference for this journey, if available. | altnames=`{"xml": "RouteRef"}` | - | - |
| `published_line_name` | `union` | `False` | Public-facing line number or name displayed to passengers on signs and in apps. Example: 31. | altnames=`{"xml": "PublishedLineName"}` | - | - |
| `external_line_ref` | `union` | `False` | External line reference, typically the same value as line_ref, used for cross-system reconciliation. | altnames=`{"xml": "ExternalLineRef"}` | - | - |
| `origin_name` | `union` | `False` | Human-readable name of the origin stop or place for this journey. | altnames=`{"xml": "OriginName"}` | - | - |
| `destination_name` | `union` | `False` | Human-readable name of the destination stop or place for this journey. | altnames=`{"xml": "DestinationName"}` | - | - |
| `data_source` | `union` | `False` | Operator codespace originating this data record, as reported in the SIRI DataSource element. Example: RUT. | altnames=`{"xml": "DataSource"}` | - | - |

#### Schema `no.entur.EstimatedVehicleJourney`
<a id="schema-noenturestimatedvehiclejourney"></a>

| Field | Value |
| --- | --- |
| Name | EstimatedVehicleJourney |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://real-time-sources.2030.io/schemas/no/entur/EstimatedVehicleJourney` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/no/entur/EstimatedVehicleJourney` |
| Type | `object` |

###### Object `EstimatedVehicleJourney`
<a id="schema-node-estimatedvehiclejourney"></a>

Real-time estimated timetable update for a vehicle journey from the Entur SIRI-ET feed. Contains per-stop arrival and departure predictions, journey-level cancellation and extra-journey flags, and monitoring status. Sourced from GET /realtime/v1/rest/et using incremental requestorId polling.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `service_journey_id` | `string` | `True` | NeTEx ServiceJourney identifier extracted from FramedVehicleJourneyRef/DatedVehicleJourneyRef. Uniquely identifies the planned vehicle journey within the NeTEx codespace. Example: RUT:ServiceJourney:1-1234. | altnames=`{"xml": "DatedVehicleJourneyRef"}` | - | - |
| `operating_day` | `string` | `True` | ISO 8601 calendar date string representing the operating day on which this journey runs, extracted from FramedVehicleJourneyRef/DataFrameRef. Example: 2024-01-01. | altnames=`{"xml": "DataFrameRef"}` | pattern=`^\d{4}-\d{2}-\d{2}$` | - |
| `line_ref` | `string` | `True` | NeTEx Line reference identifying the line this journey belongs to. Example: RUT:Line:1. | altnames=`{"xml": "LineRef"}` | - | - |
| `operator_ref` | `string` | `True` | NeTEx Operator or codespace reference identifying the operator responsible for this journey. Example: RUT. | altnames=`{"xml": "OperatorRef"}` | - | - |
| `direction_ref` | `union` | `False` | Direction reference for this journey, e.g. Outbound or Inbound. | altnames=`{"xml": "DirectionRef"}` | - | - |
| `vehicle_mode` | `union` | `False` | SIRI VehicleMode describing the mode of transport. Known values: bus, tram, rail, ferry, metro, water, air, coach, taxi. | altnames=`{"xml": "VehicleMode"}`<br>altenums=`["bus", "tram", "rail", "ferry", "metro", "water", "air", "coach", "taxi"]` | - | - |
| `published_line_name` | `union` | `False` | Public-facing line number or name displayed to passengers. Example: 31. | altnames=`{"xml": "PublishedLineName"}` | - | - |
| `route_ref` | `union` | `False` | NeTEx Route reference for this journey, if available. | altnames=`{"xml": "RouteRef"}` | - | - |
| `origin_name` | `union` | `False` | Human-readable name of the origin stop or place for this journey. | altnames=`{"xml": "OriginName"}` | - | - |
| `destination_name` | `union` | `False` | Human-readable name of the destination stop or place for this journey. | altnames=`{"xml": "DestinationName"}` | - | - |
| `is_cancellation` | `boolean` | `True` | True if the entire journey is cancelled. Corresponds to the SIRI Cancellation element on the EstimatedVehicleJourney. Defaults to false. | altnames=`{"xml": "Cancellation"}` | default=`False` | default=`False` |
| `is_extra_journey` | `union` | `False` | True if this is an extra journey added outside the planned timetable (SIRI ExtraJourney). | altnames=`{"xml": "ExtraJourney"}` | - | - |
| `is_complete_stop_sequence` | `union` | `False` | True if the EstimatedCalls list covers all stops in the journey sequence (SIRI IsCompleteStopSequence). False means the list is a partial update. | altnames=`{"xml": "IsCompleteStopSequence"}` | - | - |
| `monitored` | `union` | `False` | True if this journey is being actively tracked by an AVL system. | altnames=`{"xml": "Monitored"}` | - | - |
| `data_source` | `union` | `False` | Operator codespace originating this data record, from the SIRI DataSource element. Example: RUT. | altnames=`{"xml": "DataSource"}` | - | - |
| `recorded_at_time` | `union` | `False` | ISO 8601 UTC timestamp when this update was recorded by the source system (SIRI RecordedAtTime). | altnames=`{"xml": "RecordedAtTime"}` | - | - |
| `estimated_calls` | array of [`EstimatedCall`](#schema-node-estimatedcall) | `True` | Ordered list of estimated arrival and departure times for each stop along the journey. May be a partial list if is_complete_stop_sequence is false. | - | - | - |

###### Object `EstimatedCall`
<a id="schema-node-estimatedcall"></a>

A single estimated call at a stop within an EstimatedVehicleJourney. Contains real-time arrival and departure time predictions alongside timetabled times, stop cancellation flags, and boarding activity for a specific stop point in the journey.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `stop_point_ref` | `string` | `True` | NSR Quay or StopPoint identifier for this call, from the SIRI StopPointRef element. Example: NSR:Quay:1234. | altnames=`{"xml": "StopPointRef"}` | - | - |
| `order` | `int32` | `True` | 1-based sequence order of this call within the journey, from the SIRI Order element. | altnames=`{"xml": "Order"}` | minimum=`1` | - |
| `stop_point_name` | `union` | `False` | Public-facing stop name displayed to passengers, from StopPointName. | altnames=`{"xml": "StopPointName"}` | - | - |
| `aimed_arrival_time` | `union` | `False` | Timetabled (aimed) arrival time at this stop in ISO 8601 format, from AimedArrivalTime. | altnames=`{"xml": "AimedArrivalTime"}` | - | - |
| `expected_arrival_time` | `union` | `False` | Real-time expected arrival time at this stop in ISO 8601 format, from ExpectedArrivalTime. | altnames=`{"xml": "ExpectedArrivalTime"}` | - | - |
| `aimed_departure_time` | `union` | `False` | Timetabled (aimed) departure time at this stop in ISO 8601 format, from AimedDepartureTime. | altnames=`{"xml": "AimedDepartureTime"}` | - | - |
| `expected_departure_time` | `union` | `False` | Real-time expected departure time at this stop in ISO 8601 format, from ExpectedDepartureTime. | altnames=`{"xml": "ExpectedDepartureTime"}` | - | - |
| `arrival_status` | `union` | `False` | SIRI ArrivalStatus describing the current arrival state at this stop. | altnames=`{"xml": "ArrivalStatus"}`<br>altenums=`["onTime", "early", "delayed", "cancelled", "arrived", "noReport"]` | - | - |
| `departure_status` | `union` | `False` | SIRI DepartureStatus describing the current departure state at this stop. | altnames=`{"xml": "DepartureStatus"}`<br>altenums=`["onTime", "early", "delayed", "cancelled", "departed", "noReport"]` | - | - |
| `departure_platform_name` | `union` | `False` | Platform or track identifier for the departure at this stop, from DeparturePlatformName. | altnames=`{"xml": "DeparturePlatformName"}` | - | - |
| `arrival_boarding_activity` | `union` | `False` | SIRI ArrivalBoardingActivity indicating whether passengers may board at arrival. | altnames=`{"xml": "ArrivalBoardingActivity"}`<br>altenums=`["boarding", "noBoarding", "passthru"]` | - | - |
| `departure_boarding_activity` | `union` | `False` | SIRI DepartureBoardingActivity indicating whether passengers may board at departure. | altnames=`{"xml": "DepartureBoardingActivity"}`<br>altenums=`["boarding", "noBoarding", "passthru"]` | - | - |
| `is_cancellation` | `union` | `False` | True if this individual stop call is cancelled. Corresponds to the SIRI Cancellation element on the EstimatedCall. | altnames=`{"xml": "Cancellation"}` | - | - |
| `is_extra_stop` | `union` | `False` | True if this stop was added outside the planned timetable, i.e. an extra call (SIRI ExtraCall). | altnames=`{"xml": "ExtraCall"}` | - | - |

#### Schema `no.entur.MonitoredVehicleJourney`
<a id="schema-noenturmonitoredvehiclejourney"></a>

| Field | Value |
| --- | --- |
| Name | MonitoredVehicleJourney |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://real-time-sources.2030.io/schemas/no/entur/MonitoredVehicleJourney` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/no/entur/MonitoredVehicleJourney` |
| Type | `object` |

###### Object `MonitoredVehicleJourney`
<a id="schema-node-monitoredvehiclejourney"></a>

Real-time vehicle monitoring update from the Entur SIRI-VM feed. Contains the current geographic position, bearing, delay, and occupancy of a vehicle operating a specific dated service journey. Sourced from GET /realtime/v1/rest/vm using incremental requestorId polling.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `service_journey_id` | `string` | `True` | NeTEx ServiceJourney identifier extracted from FramedVehicleJourneyRef/DatedVehicleJourneyRef. Uniquely identifies the planned vehicle journey. Example: RUT:ServiceJourney:1-1234. | altnames=`{"xml": "DatedVehicleJourneyRef"}` | - | - |
| `operating_day` | `string` | `True` | ISO 8601 calendar date string for the operating day of this journey, from FramedVehicleJourneyRef/DataFrameRef. Example: 2024-01-01. | altnames=`{"xml": "DataFrameRef"}` | pattern=`^\d{4}-\d{2}-\d{2}$` | - |
| `recorded_at_time` | `datetime` | `True` | ISO 8601 UTC timestamp from the parent VehicleActivity/RecordedAtTime element indicating when this position was recorded. | altnames=`{"xml": "RecordedAtTime"}` | - | - |
| `line_ref` | `string` | `True` | NeTEx Line reference identifying the line this journey belongs to. Example: RUT:Line:1. | altnames=`{"xml": "LineRef"}` | - | - |
| `operator_ref` | `string` | `True` | NeTEx Operator or codespace reference for the operator running this journey. Example: RUT. | altnames=`{"xml": "OperatorRef"}` | - | - |
| `direction_ref` | `union` | `False` | Direction reference for this journey, e.g. Outbound or Inbound. | altnames=`{"xml": "DirectionRef"}` | - | - |
| `vehicle_mode` | `union` | `False` | SIRI VehicleMode describing the mode of transport. Known values: bus, tram, rail, ferry, metro, water, air, coach, taxi. | altnames=`{"xml": "VehicleMode"}`<br>altenums=`["bus", "tram", "rail", "ferry", "metro", "water", "air", "coach", "taxi"]` | - | - |
| `published_line_name` | `union` | `False` | Public-facing line number or name displayed to passengers. Example: 31. | altnames=`{"xml": "PublishedLineName"}` | - | - |
| `origin_name` | `union` | `False` | Human-readable name of the origin stop or place for this journey. | altnames=`{"xml": "OriginName"}` | - | - |
| `destination_name` | `union` | `False` | Human-readable name of the destination stop or place for this journey. | altnames=`{"xml": "DestinationName"}` | - | - |
| `vehicle_ref` | `union` | `False` | Vehicle identifier from the SIRI VehicleRef element. Identifies the physical vehicle (e.g. bus number), not the journey. Not used as a Kafka key. | altnames=`{"xml": "VehicleRef"}` | - | - |
| `latitude` | `union` | `False` | WGS84 latitude of the vehicle's current position in decimal degrees, from VehicleLocation/Latitude. | unit=`degrees`<br>altnames=`{"xml": "Latitude"}` | maximum=`90.0`<br>minimum=`-90.0` | - |
| `longitude` | `union` | `False` | WGS84 longitude of the vehicle's current position in decimal degrees, from VehicleLocation/Longitude. | unit=`degrees`<br>altnames=`{"xml": "Longitude"}` | maximum=`180.0`<br>minimum=`-180.0` | - |
| `bearing` | `union` | `False` | Compass bearing in degrees (0-360) indicating the direction of travel, from the SIRI Bearing element. | unit=`degrees`<br>altnames=`{"xml": "Bearing"}` | maximum=`360.0`<br>minimum=`0.0` | - |
| `delay_seconds` | `union` | `False` | Current delay in integer seconds, parsed from the ISO 8601 Duration value in the SIRI Delay element. Positive values indicate lateness; negative values indicate running early. | unit=`s`<br>altnames=`{"xml": "Delay"}` | - | - |
| `occupancy_status` | `union` | `False` | Passenger occupancy status of the vehicle from the SIRI OccupancyStatus element. | altnames=`{"xml": "OccupancyStatus"}`<br>altenums=`["full", "standingRoomOnly", "passengerCapacityLimitReached", "seatsAvailable", "empty", "notAcceptingPassengers"]` | - | - |
| `progress_status` | `union` | `False` | Journey progress status from the SIRI ProgressStatus element indicating whether the journey is running normally or has been cancelled/skipped. | altnames=`{"xml": "ProgressStatus"}`<br>altenums=`["inProgress", "notExpected", "notRun", "cancelled"]` | - | - |
| `monitored` | `boolean` | `True` | True if this journey is being actively tracked by an AVL system, from the SIRI Monitored element. | altnames=`{"xml": "Monitored"}` | - | - |

#### Schema `no.entur.PtSituationElement`
<a id="schema-noenturptsituationelement"></a>

| Field | Value |
| --- | --- |
| Name | PtSituationElement |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://real-time-sources.2030.io/schemas/no/entur/PtSituationElement` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/no/entur/PtSituationElement` |
| Type | `object` |

###### Object `PtSituationElement`
<a id="schema-node-ptsituationelement"></a>

Real-time transit disruption or service alert from the Entur SIRI-SX feed. Describes a published situation element such as a service disruption, delay cause, planned engineering work, or passenger information notice. Includes affected network elements, severity, textual descriptions, and validity periods. Sourced from GET /realtime/v1/rest/sx.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `situation_number` | `string` | `True` | Unique situation identifier from the SIRI SituationNumber element. Used as the Kafka key. Example: RUT:SituationNumber:12345. | altnames=`{"xml": "SituationNumber"}` | - | - |
| `version` | `union` | `False` | Version number of this situation record, from the SIRI Version element. Increments with each update to the same situation. | altnames=`{"xml": "Version"}` | - | - |
| `creation_time` | `datetime` | `True` | ISO 8601 UTC timestamp when this situation was first created, from the SIRI CreationTime element. | altnames=`{"xml": "CreationTime"}` | - | - |
| `source_type` | `union` | `False` | Type of the originating source system from the SIRI Source/SourceType element. | altnames=`{"xml": "SourceType"}`<br>altenums=`["directReport", "email", "phone", "post", "feed", "radio", "tv", "web", "pager", "text", "other"]` | - | - |
| `source_name` | `union` | `False` | Name of the originating source organisation from the SIRI Source/Name element. | altnames=`{"xml": "Name"}` | - | - |
| `progress` | `union` | `False` | Publication progress state of this situation from the SIRI Progress element. | altnames=`{"xml": "Progress"}`<br>altenums=`["open", "published", "closing", "closed"]` | - | - |
| `severity` | `string` | `True` | SIRI Severity classification of the impact of this situation on passenger services, or 'unknown' when absent. | altnames=`{"xml": "Severity"}`<br>altenums=`["unknown", "noImpact", "verySlight", "slight", "normal", "severe", "verySevere", "undefined"]` | - | - |
| `keywords` | `union` | `False` | Space-separated list of classification keywords from the SIRI Keywords element, used to categorise the situation type. | altnames=`{"xml": "Keywords"}` | - | - |
| `summary` | `union` | `False` | Short public-facing summary text in Norwegian or English describing the situation, from the SIRI Summary element. | altnames=`{"xml": "Summary"}` | - | - |
| `description` | `union` | `False` | Full public-facing descriptive text in Norwegian or English providing details about the situation, from the SIRI Description element. | altnames=`{"xml": "Description"}` | - | - |
| `affects_line_refs` | array of `string` | `False` | List of NeTEx LineRef values identifying the lines affected by this situation, extracted from Affects/Networks/AffectedNetwork/AffectedLine/LineRef elements. | - | - | - |
| `affects_stop_point_refs` | array of `string` | `False` | List of NSR StopPointRef values identifying the stop points affected by this situation, extracted from Affects/StopPoints/AffectedStopPoint/StopPointRef elements. | - | - | - |
| `validity_periods` | array of [`ValidityPeriod`](#schema-node-validityperiod) | `False` | One or more time windows during which this situation is active, from the SIRI ValidityPeriod elements. | - | - | - |

###### Object `ValidityPeriod`
<a id="schema-node-validityperiod"></a>

A time window during which a PtSituationElement is active and applicable. A situation may have multiple validity periods covering separate intervals. Sourced from the SIRI ValidityPeriod element.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `start_time` | `datetime` | `True` | ISO 8601 UTC start time of this validity window, from ValidityPeriod/StartTime. | altnames=`{"xml": "StartTime"}` | - | - |
| `end_time` | `union` | `False` | ISO 8601 UTC end time of this validity window, from ValidityPeriod/EndTime. Null if the validity period is open-ended. | altnames=`{"xml": "EndTime"}` | - | - |

### Schemagroup `no.entur.avro`
<a id="schemagroup-noenturavro"></a>

#### Schema `no.entur.DatedServiceJourney`
<a id="schema-noenturdatedservicejourney"></a>

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | DatedServiceJourney |
| Namespace | no.entur |
| Type | `record` |
| Doc | Reference data for a dated service journey in the Norwegian public transport network. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `service_journey_id` | `string` | NeTEx ServiceJourney identifier from DatedVehicleJourneyRef. Example: RUT:ServiceJourney:1-1234. | `-` |
| `operating_day` | `string` | ISO 8601 date string for the operating day from DataFrameRef. Example: 2024-01-01. | `-` |
| `line_ref` | `string` | NeTEx Line reference. Example: RUT:Line:1. | `-` |
| `operator_ref` | `string` | NeTEx Operator or codespace reference. Example: RUT. | `-` |
| `direction_ref` | `null` \| `string` | Direction reference, e.g. Outbound or Inbound. | `-` |
| `vehicle_mode` | `null` \| `string` | SIRI VehicleMode: bus, tram, rail, ferry, metro, water, air, coach, taxi. | `-` |
| `route_ref` | `null` \| `string` | NeTEx Route reference. | `-` |
| `published_line_name` | `null` \| `string` | Public-facing line number or name displayed to passengers. | `-` |
| `external_line_ref` | `null` \| `string` | External line reference. | `-` |
| `origin_name` | `null` \| `string` | Origin stop or place name for this journey. | `-` |
| `destination_name` | `null` \| `string` | Destination stop or place name for this journey. | `-` |
| `data_source` | `null` \| `string` | Operator codespace originating this data record. | `-` |

#### Schema `no.entur.EstimatedVehicleJourney`
<a id="schema-noenturestimatedvehiclejourney"></a>

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | EstimatedVehicleJourney |
| Namespace | no.entur |
| Type | `record` |
| Doc | Real-time estimated timetable update from the Entur SIRI-ET feed. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `service_journey_id` | `string` | NeTEx ServiceJourney identifier from FramedVehicleJourneyRef/DatedVehicleJourneyRef. | `-` |
| `operating_day` | `string` | ISO 8601 date string from FramedVehicleJourneyRef/DataFrameRef. | `-` |
| `line_ref` | `string` | NeTEx Line reference. | `-` |
| `operator_ref` | `string` | Operator codespace. | `-` |
| `direction_ref` | `null` \| `string` | Direction reference. | `-` |
| `vehicle_mode` | `null` \| `string` | Transport mode. | `-` |
| `published_line_name` | `null` \| `string` | Public-facing line name. | `-` |
| `route_ref` | `null` \| `string` | NeTEx Route reference. | `-` |
| `origin_name` | `null` \| `string` | Origin stop name. | `-` |
| `destination_name` | `null` \| `string` | Destination stop name. | `-` |
| `is_cancellation` | `boolean` | True if the entire journey is cancelled. | `-` |
| `is_extra_journey` | `null` \| `boolean` | True if this is an extra journey not in the timetable. | `-` |
| `is_complete_stop_sequence` | `null` \| `boolean` | True if EstimatedCalls covers all stops. | `-` |
| `monitored` | `null` \| `boolean` | True if this journey is actively monitored. | `-` |
| `data_source` | `null` \| `string` | DataSource codespace. | `-` |
| `recorded_at_time` | `null` \| `string` | ISO 8601 UTC timestamp when this update was recorded. | `-` |
| `estimated_calls` | array of record `EstimatedCall` | Ordered list of estimated arrival and departure times for each stop. | `-` |

#### Schema `no.entur.MonitoredVehicleJourney`
<a id="schema-noenturmonitoredvehiclejourney"></a>

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | MonitoredVehicleJourney |
| Namespace | no.entur |
| Type | `record` |
| Doc | Real-time vehicle monitoring update from the Entur SIRI-VM feed. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `service_journey_id` | `string` | NeTEx ServiceJourney identifier from FramedVehicleJourneyRef/DatedVehicleJourneyRef. | `-` |
| `operating_day` | `string` | ISO 8601 date string from FramedVehicleJourneyRef/DataFrameRef. | `-` |
| `recorded_at_time` | `string` | ISO 8601 UTC timestamp from VehicleActivity/RecordedAtTime. | `-` |
| `line_ref` | `string` | NeTEx Line reference. | `-` |
| `operator_ref` | `string` | Operator codespace. | `-` |
| `direction_ref` | `null` \| `string` | Direction reference. | `-` |
| `vehicle_mode` | `null` \| `string` | Transport mode. | `-` |
| `published_line_name` | `null` \| `string` | Public-facing line name. | `-` |
| `origin_name` | `null` \| `string` | Origin stop name. | `-` |
| `destination_name` | `null` \| `string` | Destination stop name. | `-` |
| `vehicle_ref` | `null` \| `string` | VehicleRef identifier. This is payload data, not the Kafka key. | `-` |
| `latitude` | `null` \| `double` | WGS84 latitude from VehicleLocation. | `-` |
| `longitude` | `null` \| `double` | WGS84 longitude from VehicleLocation. | `-` |
| `bearing` | `null` \| `double` | Compass bearing in degrees (0-360). | `-` |
| `delay_seconds` | `null` \| `int` | Current delay in seconds, parsed from SIRI Delay ISO 8601 duration. | `-` |
| `occupancy_status` | `null` \| `string` | OccupancyStatus: full, standingRoomOnly, seatsAvailable, empty, etc. | `-` |
| `progress_status` | `null` \| `string` | ProgressStatus: inProgress, notExpected, notRun, cancelled. | `-` |
| `monitored` | `boolean` | True if this journey is actively monitored by an AVL system. | `-` |

#### Schema `no.entur.PtSituationElement`
<a id="schema-noenturptsituationelement"></a>

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | PtSituationElement |
| Namespace | no.entur |
| Type | `record` |
| Doc | Real-time transit disruption or service alert from the Entur SIRI-SX feed. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `situation_number` | `string` | Unique situation identifier (SituationNumber). Example: RUT:SituationNumber:12345. | `-` |
| `version` | `null` \| `string` | Situation version number. | `-` |
| `creation_time` | `string` | ISO 8601 UTC creation time (CreationTime). | `-` |
| `source_type` | `null` \| `string` | Source type: directReport, email, phone, post, feed, radio, tv, web, pager, text, other. | `-` |
| `source_name` | `null` \| `string` | Name of originating source or organisation. | `-` |
| `progress` | `null` \| `string` | Publication progress: open, published, closing, closed. | `-` |
| `severity` | `string` | SIRI Severity classification, or 'unknown' when absent. | `-` |
| `keywords` | `null` \| `string` | Space-separated keywords from the SIRI Keywords element. | `-` |
| `summary` | `null` \| `string` | Short public summary text from Summary element. | `-` |
| `description` | `null` \| `string` | Full public description text from Description element. | `-` |
| `validity_periods` | array of record `ValidityPeriod` | One or more active validity windows for this situation. | `-` |
| `affects_line_refs` | array of `string` | LineRef values from AffectedLine elements. | `-` |
| `affects_stop_point_refs` | array of `string` | StopPointRef values from AffectedStopPoint elements. | `-` |
