# NDW Netherlands Road Traffic Bridge Events

This bridge downloads DATEX II XML data published by the Dutch NDW (Nationaal Dataportaal Wegverkeer) at `https://opendata.ndw.nu` and forwards traffic speed, travel time, and situation data to Apache Kafka, Azure Event Hubs, or Microsoft Fabric Event Streams as CloudEvents.

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

### Endpoint `NL.NDW.Traffic.Measurements.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`NL.NDW.Traffic.Measurements`](#messagegroup-nlndwtrafficmeasurements) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `ndl-traffic` |
| Kafka key | `{site_id}` |
| Deployed | False |

### Endpoint `NL.NDW.Traffic.Situations.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`NL.NDW.Traffic.Situations`](#messagegroup-nlndwtrafficsituations) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `ndl-traffic-situations` |
| Kafka key | `{situation_id}` |
| Deployed | False |

## Messagegroups

### Messagegroup `NL.NDW.Traffic.Measurements`
<a id="messagegroup-nlndwtrafficmeasurements"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `NL.NDW.Traffic.Measurements.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `NL.NDW.Traffic.TrafficSpeed`
<a id="message-nlndwtraffictrafficspeed"></a>

Aggregated traffic speed and flow measurement per road segment from the Dutch NDW DATEX II trafficspeed feed. Each record represents one measurement site with speed averaged and flow summed across all reporting lanes.

| Field | Value |
| --- | --- |
| Name | TrafficSpeed |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NL.NDW.Traffic.jstruct/schemas/NL.NDW.Traffic.TrafficSpeed`](#schema-nlndwtraffictrafficspeed) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NL.NDW.Traffic.TrafficSpeed` |
| `source` |  | `string` | `False` | `https://opendata.ndw.nu/trafficspeed.xml.gz` |
| `subject` |  | `uritemplate` | `False` | `{site_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NL.NDW.Traffic.Measurements.Kafka` | `KAFKA` | topic `ndl-traffic`; key `{site_id}` |

#### Message `NL.NDW.Traffic.TravelTime`
<a id="message-nlndwtraffictraveltime"></a>

Travel time measurement for a road segment from the Dutch NDW DATEX II traveltime feed. Each record contains the actual measured travel time and the static free-flow reference time for a measurement site.

| Field | Value |
| --- | --- |
| Name | TravelTime |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NL.NDW.Traffic.jstruct/schemas/NL.NDW.Traffic.TravelTime`](#schema-nlndwtraffictraveltime) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NL.NDW.Traffic.TravelTime` |
| `source` |  | `string` | `False` | `https://opendata.ndw.nu/traveltime.xml.gz` |
| `subject` |  | `uritemplate` | `False` | `{site_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NL.NDW.Traffic.Measurements.Kafka` | `KAFKA` | topic `ndl-traffic`; key `{site_id}` |

### Messagegroup `NL.NDW.Traffic.Situations`
<a id="messagegroup-nlndwtrafficsituations"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `NL.NDW.Traffic.Situations.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `NL.NDW.Traffic.TrafficSituation`
<a id="message-nlndwtraffictrafficsituation"></a>

Current traffic situation record from the Dutch NDW DATEX II actueel_beeld (current situation overview) feed. Includes road works, closures, lane management, and other traffic-affecting events on the Dutch road network.

| Field | Value |
| --- | --- |
| Name | TrafficSituation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NL.NDW.Traffic.jstruct/schemas/NL.NDW.Traffic.TrafficSituation`](#schema-nlndwtraffictrafficsituation) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NL.NDW.Traffic.TrafficSituation` |
| `source` |  | `string` | `False` | `https://opendata.ndw.nu/actueel_beeld.xml.gz` |
| `subject` |  | `uritemplate` | `False` | `{situation_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NL.NDW.Traffic.Situations.Kafka` | `KAFKA` | topic `ndl-traffic-situations`; key `{situation_id}` |

## Schemagroups

### Schemagroup `NL.NDW.Traffic.jstruct`
<a id="schemagroup-nlndwtrafficjstruct"></a>

#### Schema `NL.NDW.Traffic.TrafficSpeed`
<a id="schema-nlndwtraffictrafficspeed"></a>

| Field | Value |
| --- | --- |
| Name | TrafficSpeed |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/nl/ndw/traffic/TrafficSpeed` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/nl/ndw/traffic/TrafficSpeed` |
| Type | `object` |

###### Object `TrafficSpeed`
<a id="schema-node-trafficspeed"></a>

Aggregated traffic speed and flow measurement per road segment from the NDW DATEX II trafficspeed feed. Speed is averaged and flow is summed across all reporting lanes at the measurement site.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `site_id` | `string` | `True` | Unique identifier of the NDW measurement site, taken from the DATEX II measurementSiteReference id attribute. Example: PZH01_MST_0029-00. | - | - | - |
| `measurement_time` | `string` | `True` | Timestamp of the measurement in ISO 8601 format (UTC), from the DATEX II measurementTimeDefault element. | - | - | - |
| `average_speed` | `union` | `False` | Average vehicle speed in km/h across all lanes with valid data at this site. Null when no lane reported a valid speed (all lanes had speed <= 0). | unit=`km/h` | - | - |
| `vehicle_flow_rate` | `union` | `False` | Total vehicle flow rate in vehicles per hour, summed across all lanes at this measurement site. Null when no valid flow data was reported. | unit=`vehicles/h` | - | - |
| `number_of_lanes_with_data` | `int32` | `True` | Number of lanes that reported valid measurement data (speed > 0 or flow >= 0) at this measurement site. | - | - | - |

#### Schema `NL.NDW.Traffic.TravelTime`
<a id="schema-nlndwtraffictraveltime"></a>

| Field | Value |
| --- | --- |
| Name | TravelTime |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/nl/ndw/traffic/TravelTime` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/nl/ndw/traffic/TravelTime` |
| Type | `object` |

###### Object `TravelTime`
<a id="schema-node-traveltime"></a>

Travel time measurement for a road segment from the NDW DATEX II traveltime feed. Contains actual measured travel time and the static free-flow reference time.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `site_id` | `string` | `True` | Unique identifier of the NDW measurement site, taken from the DATEX II measurementSiteReference id attribute. | - | - | - |
| `measurement_time` | `string` | `True` | Timestamp of the measurement in ISO 8601 format (UTC), from the DATEX II measurementTimeDefault element. | - | - | - |
| `duration` | `union` | `False` | Actual measured travel time in seconds for this road segment. Null when the measurement has a data error (duration is -1 in the upstream). | unit=`s` | - | - |
| `reference_duration` | `union` | `False` | Static reference (free-flow) travel time in seconds for this road segment. Null when unavailable or when the measurement has a data error. | unit=`s` | - | - |
| `accuracy` | `union` | `False` | Accuracy of the travel time measurement as a percentage (0-100), indicating the quality of the sensor coverage. | - | - | - |
| `data_quality` | `union` | `False` | Supplier-calculated data quality score as a percentage (0-100). Higher values indicate more reliable measurements. | - | - | - |
| `number_of_input_values` | `union` | `False` | Number of individual vehicle travel times used to compute this aggregate travel time measurement. | - | - | - |

#### Schema `NL.NDW.Traffic.TrafficSituation`
<a id="schema-nlndwtraffictrafficsituation"></a>

| Field | Value |
| --- | --- |
| Name | TrafficSituation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/nl/ndw/traffic/TrafficSituation` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/nl/ndw/traffic/TrafficSituation` |
| Type | `object` |

###### Object `TrafficSituation`
<a id="schema-node-trafficsituation"></a>

Current traffic situation from the NDW DATEX II v3 actueel_beeld feed. Covers road works, lane closures, diversions, and other traffic-affecting events on the Dutch road network.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `situation_id` | `string` | `True` | Unique identifier of the traffic situation from the DATEX II situation id attribute. Example: RWS01_SM1117672_D2_WWA. | - | - | - |
| `version_time` | `string` | `True` | Timestamp of the latest version of this situation in ISO 8601 format (UTC), from the DATEX II situationVersionTime element. | - | - | - |
| `severity` | `union` | `False` | Overall severity of the situation. Values include: low, medium, high, highest, unknown. Null if not specified. | - | - | - |
| `record_type` | `union` | `False` | DATEX II situation record type indicating the nature of the event. Common values: RoadOrCarriagewayOrLaneManagement, MaintenanceWorks, ConstructionWorks, ReroutingManagement. Null when not available. | - | - | - |
| `cause_type` | `union` | `False` | Cause of the traffic situation. Common values: roadMaintenance, accident, congestion, roadClosed. Null when no cause is specified. | - | - | - |
| `start_time` | `union` | `False` | Start time of the situation validity period in ISO 8601 format (UTC). Null when no validity time specification is provided. | - | - | - |
| `end_time` | `union` | `False` | End time of the situation validity period in ISO 8601 format (UTC). Null when the end time is open-ended or not specified. | - | - | - |
| `information_status` | `string` | `True` | Status of the information: real (confirmed traffic data), test (test data), or exercise (drill/exercise data). | - | - | - |

### Schemagroup `NL.NDW.Traffic.avro`
<a id="schemagroup-nlndwtrafficavro"></a>

#### Schema `NL.NDW.Traffic.TrafficSpeed`
<a id="schema-nlndwtraffictrafficspeed"></a>

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
| Name | TrafficSpeed |
| Namespace | nl.ndw.traffic |
| Type | `record` |
| Doc | Aggregated traffic speed and flow measurement per road segment from the NDW DATEX II trafficspeed feed. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `site_id` | `string` | Unique identifier of the NDW measurement site. | `-` |
| `measurement_time` | `string` | Timestamp of the measurement in ISO 8601 format (UTC). | `-` |
| `average_speed` | `null` \| `double` | Average vehicle speed in km/h across all lanes with valid data. Null when no valid speed data. | `-` |
| `vehicle_flow_rate` | `null` \| `int` | Total vehicle flow rate in vehicles per hour summed across all lanes. Null when no valid flow data. | `-` |
| `number_of_lanes_with_data` | `int` | Number of lanes that reported valid measurement data. | `-` |

#### Schema `NL.NDW.Traffic.TravelTime`
<a id="schema-nlndwtraffictraveltime"></a>

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
| Name | TravelTime |
| Namespace | nl.ndw.traffic |
| Type | `record` |
| Doc | Travel time measurement for a road segment from the NDW DATEX II traveltime feed. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `site_id` | `string` | Unique identifier of the NDW measurement site. | `-` |
| `measurement_time` | `string` | Timestamp of the measurement in ISO 8601 format (UTC). | `-` |
| `duration` | `null` \| `double` | Actual measured travel time in seconds. Null when data error. | `-` |
| `reference_duration` | `null` \| `double` | Static reference (free-flow) travel time in seconds. Null when unavailable. | `-` |
| `accuracy` | `null` \| `double` | Accuracy percentage (0-100). | `-` |
| `data_quality` | `null` \| `double` | Supplier-calculated data quality percentage (0-100). | `-` |
| `number_of_input_values` | `null` \| `int` | Number of individual vehicle travel times used in the calculation. | `-` |

#### Schema `NL.NDW.Traffic.TrafficSituation`
<a id="schema-nlndwtraffictrafficsituation"></a>

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
| Name | TrafficSituation |
| Namespace | nl.ndw.traffic |
| Type | `record` |
| Doc | Current traffic situation from the NDW DATEX II v3 actueel_beeld feed. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `situation_id` | `string` | Unique identifier of the traffic situation. | `-` |
| `version_time` | `string` | Timestamp of the latest version of this situation in ISO 8601 format (UTC). | `-` |
| `severity` | `null` \| `string` | Overall severity: low, medium, high, highest, unknown. | `-` |
| `record_type` | `null` \| `string` | DATEX II situation record type. | `-` |
| `cause_type` | `null` \| `string` | Cause of the traffic situation. | `-` |
| `start_time` | `null` \| `string` | Start time of the situation validity period in ISO 8601 format. | `-` |
| `end_time` | `null` \| `string` | End time of the situation validity period in ISO 8601 format. | `-` |
| `information_status` | `string` | Status of the information: real, test, or exercise. | `-` |
