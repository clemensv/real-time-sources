# French Road Traffic Events

Real-time traffic data from the French national non-conceded road network, published by [Bison Futé](https://www.bison-fute.gouv.fr/) via the [transport.data.gouv.fr](https://transport.data.gouv.fr/) open data portal.

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
| Schemagroups | 2 |

## Endpoints

### Endpoint `fr.gouv.transport.bison_fute.traffic_flow.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`fr.gouv.transport.bison_fute.traffic_flow`](#messagegroup-frgouvtransportbisonfutetrafficflow) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `french-road-traffic-flow` |
| Kafka key | `{site_id}` |
| Deployed | False |

### Endpoint `fr.gouv.transport.bison_fute.road_event.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`fr.gouv.transport.bison_fute.road_event`](#messagegroup-frgouvtransportbisonfuteroadevent) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `french-road-traffic-events` |
| Kafka key | `{situation_id}` |
| Deployed | False |

## Messagegroups

### Messagegroup `fr.gouv.transport.bison_fute.traffic_flow`
<a id="messagegroup-frgouvtransportbisonfutetrafficflow"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `fr.gouv.transport.bison_fute.traffic_flow.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `fr.gouv.transport.bison_fute.TrafficFlowMeasurement`
<a id="message-frgouvtransportbisonfutetrafficflowmeasurement"></a>

Real-time traffic flow and speed measurement from a DATEX II measurement site on the French national non-conceded road network. Published by Bison Futé (TIPI) as a MeasuredDataPublication snapshot every 6 minutes.

| Field | Value |
| --- | --- |
| Name | TrafficFlowMeasurement |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/fr.gouv.transport.bison_fute.jstruct/schemas/fr.gouv.transport.bison_fute.TrafficFlowMeasurement`](#schema-frgouvtransportbisonfutetrafficflowmeasurement) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `fr.gouv.transport.bison_fute.TrafficFlowMeasurement` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{site_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `fr.gouv.transport.bison_fute.traffic_flow.Kafka` | `KAFKA` | topic `french-road-traffic-flow`; key `{site_id}` |

### Messagegroup `fr.gouv.transport.bison_fute.road_event`
<a id="messagegroup-frgouvtransportbisonfuteroadevent"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `fr.gouv.transport.bison_fute.road_event.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `fr.gouv.transport.bison_fute.RoadEvent`
<a id="message-frgouvtransportbisonfuteroadevent"></a>

Real-time road situation record from the French national non-conceded road network. Published by Bison Futé (TIPI) as a SituationPublication snapshot. Each record represents a traffic incident, construction works, lane management, obstruction, or other event affecting road conditions. Record types include Accident, ConstructionWorks, MaintenanceWorks, RoadOrCarriagewayOrLaneManagement, AbnormalTraffic, EnvironmentalObstruction, GeneralObstruction, VehicleObstruction, AnimalPresenceObstruction, InfrastructureDamageObstruction, GeneralNetworkManagement, ReroutingManagement, SpeedManagement, WeatherRelatedRoadConditions, OperatorAction, GeneralInstructionOrMessageToRoadUsers, and RoadsideServiceDisruption.

| Field | Value |
| --- | --- |
| Name | RoadEvent |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/fr.gouv.transport.bison_fute.jstruct/schemas/fr.gouv.transport.bison_fute.RoadEvent`](#schema-frgouvtransportbisonfuteroadevent) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `fr.gouv.transport.bison_fute.RoadEvent` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{situation_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `fr.gouv.transport.bison_fute.road_event.Kafka` | `KAFKA` | topic `french-road-traffic-events`; key `{situation_id}` |

## Schemagroups

### Schemagroup `fr.gouv.transport.bison_fute.jstruct`
<a id="schemagroup-frgouvtransportbisonfutejstruct"></a>

#### Schema `fr.gouv.transport.bison_fute.TrafficFlowMeasurement`
<a id="schema-frgouvtransportbisonfutetrafficflowmeasurement"></a>

| Field | Value |
| --- | --- |
| Name | TrafficFlowMeasurement |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/fr/gouv/transport/bison_fute/TrafficFlowMeasurement` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/fr/gouv/transport/bison_fute/TrafficFlowMeasurement` |
| Type | `object` |

###### Object `TrafficFlowMeasurement`
<a id="schema-node-trafficflowmeasurement"></a>

Real-time traffic flow and speed measurement from a DATEX II measurement site on the French national non-conceded road network. Each record corresponds to one siteMeasurements element in the Bison Futé MeasuredDataPublication DATEX II feed, containing aggregated vehicle flow rate (vehicles per hour) and average vehicle speed (km/h) for the measurement interval.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `site_id` | `string` | `True` | Unique identifier of the DATEX II measurement site record, as declared in the measurementSiteReference element (e.g. 'MUM76.h1', 'MB631.B8'). Stable across publication snapshots. | - | - | - |
| `measurement_time` | `string` | `True` | ISO 8601 timestamp of the measurement, taken from the measurementTimeDefault element in the DATEX II siteMeasurements block. Represents the end of the aggregation interval. | - | - | - |
| `vehicle_flow_rate` | `union` | `False` | Number of vehicles per hour passing the measurement site during the aggregation interval, from the DATEX II TrafficFlow/vehicleFlowRate element. Null when flow data is not available for this site in the current snapshot. | - | - | - |
| `average_speed` | `union` | `False` | Average speed of vehicles in kilometres per hour at the measurement site during the aggregation interval, from the DATEX II TrafficSpeed/averageVehicleSpeed/speed element. Null when speed data is not available for this site in the current snapshot. | - | - | - |
| `input_values_flow` | `union` | `False` | Number of individual vehicle observations used to compute the vehicle flow rate, from the numberOfInputValuesUsed attribute on the vehicleFlow element. Null when flow data is not present. | - | - | - |
| `input_values_speed` | `union` | `False` | Number of individual vehicle observations used to compute the average speed, from the numberOfInputValuesUsed attribute on the averageVehicleSpeed element. Null when speed data is not present. | - | - | - |

#### Schema `fr.gouv.transport.bison_fute.RoadEvent`
<a id="schema-frgouvtransportbisonfuteroadevent"></a>

| Field | Value |
| --- | --- |
| Name | RoadEvent |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/fr/gouv/transport/bison_fute/RoadEvent` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/fr/gouv/transport/bison_fute/RoadEvent` |
| Type | `object` |

###### Object `RoadEvent`
<a id="schema-node-roadevent"></a>

Real-time road situation record from the French national non-conceded road network DATEX II SituationPublication feed. Each record represents one situationRecord element within a situation, describing a traffic incident, construction works, lane management, environmental obstruction, or other event affecting road conditions. Location is provided as WGS84 coordinates and road identifiers.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `situation_id` | `string` | `True` | Unique identifier of the parent DATEX II situation element (e.g. '230814-001797'). Stable across version updates of the same situation. | - | - | - |
| `record_id` | `string` | `True` | Unique identifier of this specific situation record within the parent situation (e.g. '230814-001797-1'). Each situation may contain multiple records. | - | - | - |
| `version` | `string` | `True` | Version number of the parent situation, incremented each time the situation is updated by the publisher. | - | - | - |
| `severity` | `union` | `False` | Overall severity of the parent situation as published in the overallSeverity element. Possible values include 'low', 'medium', 'high', 'highest'. Null when severity is not provided. | - | - | - |
| `record_type` | `string` | `True` | DATEX II xsi:type of the situation record, indicating the category of road event. Known values: Accident, AbnormalTraffic, ConstructionWorks, MaintenanceWorks, RoadOrCarriagewayOrLaneManagement, EnvironmentalObstruction, GeneralObstruction, VehicleObstruction, AnimalPresenceObstruction, InfrastructureDamageObstruction, GeneralNetworkManagement, ReroutingManagement, SpeedManagement, WeatherRelatedRoadConditions, OperatorAction, GeneralInstructionOrMessageToRoadUsers, RoadsideServiceDisruption. | - | - | - |
| `probability` | `union` | `False` | Probability of occurrence of the event from the probabilityOfOccurrence element. Possible values: 'certain', 'probable', 'riskOf'. Null when not specified. | - | - | - |
| `latitude` | `union` | `False` | WGS84 latitude of the event location from the DATEX II pointCoordinates element. Null when no coordinates are provided in the situation record. | - | - | - |
| `longitude` | `union` | `False` | WGS84 longitude of the event location from the DATEX II pointCoordinates element. Null when no coordinates are provided in the situation record. | - | - | - |
| `road_number` | `union` | `False` | Road identifier (e.g. 'N20', 'A10', 'D906') from the linearElement/roadNumber or tpegOtherPointDescriptor linkName element. Null when no road number is available. | - | - | - |
| `town_name` | `union` | `False` | Name of the nearest town from the tpegOtherPointDescriptor townName element. Null when no town name is provided. | - | - | - |
| `direction` | `union` | `False` | Direction of traffic affected by the event from the tpegDirection element. Possible values: 'bothWays', 'positive', 'negative'. Null when direction is not specified. | - | - | - |
| `description` | `union` | `False` | Human-readable description of the event from the generalPublicComment element with commentType 'description'. Null when no description comment is provided. | - | - | - |
| `location_description` | `union` | `False` | Human-readable description of the event location from the generalPublicComment element with commentType 'locationDescriptor'. When multiple location descriptors exist, they are concatenated with ' \\| '. Null when no location comment is provided. | - | - | - |
| `source_name` | `union` | `False` | Name of the organization or directorate that published this situation record, from the source/sourceIdentification element. Null when not specified. | - | - | - |
| `validity_status` | `union` | `False` | Validity status of the situation record from the validity/validityStatus element (e.g. 'definedByValidityTimeSpec', 'active'). Null when not provided. | - | - | - |
| `overall_start_time` | `union` | `False` | ISO 8601 start time of the event validity period from the overallStartTime element. Null when the validity period is not defined. | - | - | - |
| `overall_end_time` | `union` | `False` | ISO 8601 end time of the event validity period from the overallEndTime element. Null when the event has no defined end time (open-ended). | - | - | - |
| `creation_time` | `string` | `True` | ISO 8601 timestamp when the situation record was first created, from the situationRecordCreationTime element. | - | - | - |
| `observation_time` | `union` | `False` | ISO 8601 timestamp of the most recent observation of this situation, from the situationRecordObservationTime element. Null when not provided. | - | - | - |

### Schemagroup `fr.gouv.transport.bison_fute.avro`
<a id="schemagroup-frgouvtransportbisonfuteavro"></a>

#### Schema `fr.gouv.transport.bison_fute.TrafficFlowMeasurement`
<a id="schema-frgouvtransportbisonfutetrafficflowmeasurement"></a>

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | TrafficFlowMeasurement |
| Namespace | fr.gouv.transport.bison_fute |
| Type | `record` |
| Doc | Real-time traffic flow and speed measurement from a DATEX II measurement site on the French national non-conceded road network. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `site_id` | `string` | Unique identifier of the DATEX II measurement site record. | `-` |
| `measurement_time` | `string` | ISO 8601 timestamp of the measurement. | `-` |
| `vehicle_flow_rate` | `null` \| `int` | Number of vehicles per hour passing the measurement site. | `-` |
| `average_speed` | `null` \| `double` | Average speed of vehicles in km/h at the measurement site. | `-` |
| `input_values_flow` | `null` \| `int` | Number of vehicle observations used to compute the flow rate. | `-` |
| `input_values_speed` | `null` \| `int` | Number of vehicle observations used to compute the average speed. | `-` |

#### Schema `fr.gouv.transport.bison_fute.RoadEvent`
<a id="schema-frgouvtransportbisonfuteroadevent"></a>

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | RoadEvent |
| Namespace | fr.gouv.transport.bison_fute |
| Type | `record` |
| Doc | Real-time road situation record from the French national non-conceded road network. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `situation_id` | `string` | Unique identifier of the parent DATEX II situation. | `-` |
| `record_id` | `string` | Unique identifier of this situation record within the parent situation. | `-` |
| `version` | `string` | Version number of the parent situation. | `-` |
| `severity` | `null` \| `string` | Overall severity of the parent situation. | `-` |
| `record_type` | `string` | DATEX II xsi:type of the situation record. | `-` |
| `probability` | `null` \| `string` | Probability of occurrence of the event. | `-` |
| `latitude` | `null` \| `double` | WGS84 latitude of the event location. | `-` |
| `longitude` | `null` \| `double` | WGS84 longitude of the event location. | `-` |
| `road_number` | `null` \| `string` | Road identifier (e.g. N20, A10). | `-` |
| `town_name` | `null` \| `string` | Name of the nearest town. | `-` |
| `direction` | `null` \| `string` | Direction of traffic affected. | `-` |
| `description` | `null` \| `string` | Human-readable description of the event. | `-` |
| `location_description` | `null` \| `string` | Human-readable description of the event location. | `-` |
| `source_name` | `null` \| `string` | Name of the publishing organization. | `-` |
| `validity_status` | `null` \| `string` | Validity status of the situation record. | `-` |
| `overall_start_time` | `null` \| `string` | ISO 8601 start time of the event validity period. | `-` |
| `overall_end_time` | `null` \| `string` | ISO 8601 end time of the event validity period. | `-` |
| `creation_time` | `string` | ISO 8601 timestamp when the situation record was first created. | `-` |
| `observation_time` | `null` \| `string` | ISO 8601 timestamp of the most recent observation. | `-` |
