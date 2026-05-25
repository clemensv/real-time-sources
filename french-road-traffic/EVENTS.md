# French Road Traffic Events

Real-time traffic data from the French national non-conceded road network, published by [Bison Futé](https://www.bison-fute.gouv.fr/) via the [transport.data.gouv.fr](https://transport.data.gouv.fr/) open data portal.

## At a glance

- **Event types:** 2 documented event types.
- **Transports:** KAFKA
- **Reference vs telemetry:** 0 reference/catalog event types and 2 telemetry event types.
- **Identity:** `{site_id}`, `{situation_id}` identifies the resource each event is about.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `french-road-traffic-flow`, `french-road-traffic-events`. The record key is `{site_id}`, `{situation_id}`. Each key template is explained in the event catalog below. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['french-road-traffic-flow', 'french-road-traffic-events'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.

## Event catalog

### Traffic Flow Measurement

CloudEvents type: `fr.gouv.transport.bison_fute.TrafficFlowMeasurement`

#### What it tells you

Real-time traffic flow and speed measurement from a DATEX II measurement site on the French national non-conceded road network. Published by Bison Futé (TIPI) as a MeasuredDataPublication snapshot every 6 minutes. Each record corresponds to one siteMeasurements element in the Bison Futé MeasuredDataPublication DATEX II feed, containing aggregated vehicle flow rate (vehicles per hour) and average vehicle speed (km/h) for the measurement interval.

#### Identity

Each event identifies the real-world resource with `{site_id}`. `{site_id}` is unique identifier of the DATEX II measurement site record, as declared in the measurementSiteReference element (e.g. 'MUM76.h1', 'MB631.B8'). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `french-road-traffic-flow`, key `{site_id}` |

#### Payload

`Traffic Flow Measurement` payloads are JSON object. Required fields: `site_id`, `measurement_time`.

- **`site_id`** (string, required): Unique identifier of the DATEX II measurement site record, as declared in the measurementSiteReference element (e.g. 'MUM76.h1', 'MB631.B8'). Stable across publication snapshots.
- **`measurement_time`** (string, required): ISO 8601 timestamp of the measurement, taken from the measurementTimeDefault element in the DATEX II siteMeasurements block. Represents the end of the aggregation interval.
- **`vehicle_flow_rate`** (int32 or null, optional): Number of vehicles per hour passing the measurement site during the aggregation interval, from the DATEX II TrafficFlow/vehicleFlowRate element. Null when flow data is not available for this site in the current snapshot.
- **`average_speed`** (double or null, optional): Average speed of vehicles in kilometres per hour at the measurement site during the aggregation interval, from the DATEX II TrafficSpeed/averageVehicleSpeed/speed element. Null when speed data is not available for this site in the current snapshot.
- **`input_values_flow`** (int32 or null, optional): Number of individual vehicle observations used to compute the vehicle flow rate, from the numberOfInputValuesUsed attribute on the vehicleFlow element. Null when flow data is not present.
- **`input_values_speed`** (int32 or null, optional): Number of individual vehicle observations used to compute the average speed, from the numberOfInputValuesUsed attribute on the averageVehicleSpeed element. Null when speed data is not present.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "site_id": "string",
  "measurement_time": "string",
  "vehicle_flow_rate": 0,
  "average_speed": 0,
  "input_values_flow": 0,
  "input_values_speed": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Road Event

CloudEvents type: `fr.gouv.transport.bison_fute.RoadEvent`

#### What it tells you

Real-time road situation record from the French national non-conceded road network. Published by Bison Futé (TIPI) as a SituationPublication snapshot. Each record represents a traffic incident, construction works, lane management, obstruction, or other event affecting road conditions.

#### Identity

Each event identifies the real-world resource with `{situation_id}`. `{situation_id}` is unique identifier of the parent DATEX II situation element (e.g. '230814-001797'). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `french-road-traffic-events`, key `{situation_id}` |

#### Payload

`Road Event` payloads are JSON object. Required fields: `situation_id`, `record_id`, `version`, `record_type`, `creation_time`.

- **`situation_id`** (string, required): Unique identifier of the parent DATEX II situation element (e.g. '230814-001797'). Stable across version updates of the same situation.
- **`record_id`** (string, required): Unique identifier of this specific situation record within the parent situation (e.g. '230814-001797-1'). Each situation may contain multiple records.
- **`version`** (string, required): Version number of the parent situation, incremented each time the situation is updated by the publisher.
- **`severity`** (string or null, optional): Overall severity of the parent situation as published in the overallSeverity element. Possible values include 'low', 'medium', 'high', 'highest'. Null when severity is not provided.
- **`record_type`** (string, required): DATEX II xsi:type of the situation record, indicating the category of road event. Known values: Accident, AbnormalTraffic, ConstructionWorks, MaintenanceWorks, RoadOrCarriagewayOrLaneManagement, EnvironmentalObstruction, GeneralObstruction, VehicleObstruction, AnimalPresenceObstruction, InfrastructureDamageObstruction, GeneralNetworkManagement, ReroutingManagement, SpeedManagement, WeatherRelatedRoadConditions, OperatorAction, GeneralInstructionOrMessageToRoadUsers, RoadsideServiceDisruption.
- **`probability`** (string or null, optional): Probability of occurrence of the event from the probabilityOfOccurrence element. Possible values: 'certain', 'probable', 'riskOf'. Null when not specified.
- **`latitude`** (double or null, optional): WGS84 latitude of the event location from the DATEX II pointCoordinates element. Null when no coordinates are provided in the situation record.
- **`longitude`** (double or null, optional): WGS84 longitude of the event location from the DATEX II pointCoordinates element. Null when no coordinates are provided in the situation record.
- **`road_number`** (string or null, optional): Road identifier (e.g. 'N20', 'A10', 'D906') from the linearElement/roadNumber or tpegOtherPointDescriptor linkName element. Null when no road number is available.
- **`town_name`** (string or null, optional): Name of the nearest town from the tpegOtherPointDescriptor townName element. Null when no town name is provided.
- **`direction`** (string or null, optional): Direction of traffic affected by the event from the tpegDirection element. Possible values: 'bothWays', 'positive', 'negative'. Null when direction is not specified.
- **`description`** (string or null, optional): Human-readable description of the event from the generalPublicComment element with commentType 'description'. Null when no description comment is provided.
- **`location_description`** (string or null, optional): Human-readable description of the event location from the generalPublicComment element with commentType 'locationDescriptor'. When multiple location descriptors exist, they are concatenated with ' | '. Null when no location comment is provided.
- **`source_name`** (string or null, optional): Name of the organization or directorate that published this situation record, from the source/sourceIdentification element. Null when not specified.
- **`validity_status`** (string or null, optional): Validity status of the situation record from the validity/validityStatus element (e.g. 'definedByValidityTimeSpec', 'active'). Null when not provided.
- **`overall_start_time`** (string or null, optional): ISO 8601 start time of the event validity period from the overallStartTime element. Null when the validity period is not defined.
- **`overall_end_time`** (string or null, optional): ISO 8601 end time of the event validity period from the overallEndTime element. Null when the event has no defined end time (open-ended).
- **`creation_time`** (string, required): ISO 8601 timestamp when the situation record was first created, from the situationRecordCreationTime element.
- **`observation_time`** (string or null, optional): ISO 8601 timestamp of the most recent observation of this situation, from the situationRecordObservationTime element. Null when not provided.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "situation_id": "string",
  "record_id": "string",
  "version": "string",
  "severity": "string",
  "record_type": "string",
  "probability": "string",
  "latitude": 0,
  "longitude": 0,
  "road_number": "string",
  "town_name": "string",
  "direction": "string",
  "description": "string",
  "location_description": "string",
  "source_name": "string",
  "validity_status": "string",
  "overall_start_time": "string",
  "overall_end_time": "string",
  "creation_time": "string",
  "observation_time": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

## Conventions

CloudEvents is the envelope around each JSON payload. It supplies metadata such as `specversion` (`1.0`), `type` (what kind of event this is), `source` (who produced it), `id` (the event occurrence identifier), `time`, and `subject` (the resource the event is about). For this source, `subject` is the stable routing identity described in each event above; the unique event occurrence is identified by CloudEvents `id` together with `source`. This repository convention mirrors the same identity to transport-native routing fields where available: Kafka message key (or the `partitionkey` extension when present), MQTT topic identity segments, and AMQP message `subject` or application properties. Those mirrors are application conventions, not generic CloudEvents binding rules. The AMQP link address identifies the stream as a whole, not an individual station or entity.

Transport bindings carry CloudEvents metadata differently:

| Transport | CloudEvents metadata location | Payload location |
| --- | --- | --- |
| Kafka binary mode | Kafka headers named `ce_<attribute>` for CloudEvents attributes except `datacontenttype`; `datacontenttype` maps to Kafka `content-type` | Kafka record value |
| Kafka structured mode | Inside the JSON CloudEvent envelope, with content type `application/cloudevents+json`; batched mode is not used by this generator | Kafka record value |
| MQTT 5 binary mode | MQTT 5 user properties named by the CloudEvents attribute (`id`, `source`, `type`, `subject`, ...), as defined by the CloudEvents MQTT binding; no `ce_` prefix | PUBLISH payload |
| AMQP 1.0 binary mode | Application properties named `cloudEvents:<attribute>` except `datacontenttype`; `datacontenttype` maps to AMQP `content-type` and must not be duplicated as an application property | AMQP message body |

All payloads documented here are JSON. MQTT retained messages are Last Known Value snapshots: the broker stores the most recent retained message per exact topic and delivers it to new subscribers when their subscription matches that topic. Schema evolution is additive where possible; incompatible semantic or structural changes are published as a new CloudEvents type so existing consumers can keep running.

## Operational notes

No source-specific polling cadence, rate limit, or stream characteristic is documented in the checked-in README or CONTAINER guide.

## References

- xRegistry manifest: [`xreg/french_road_traffic.xreg.json`](xreg/french_road_traffic.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
