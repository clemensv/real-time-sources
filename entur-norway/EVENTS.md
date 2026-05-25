# Entur Norway SIRI Bridge Events

Message group for dated service journey reference data and real-time journey telemetry (ET and VM). All messages in this group share the journeys/{operating_day}/{service_journey_id} Kafka key.

## At a glance

- **Event types:** 4 documented event types (7 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0
- **Reference vs telemetry:** 0 reference/catalog event types and 4 telemetry event types.
- **Identity:** `journeys/{operating_day}/{service_journey_id}`, `situations/{situation_number}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `entur-norway`. The record key is `journeys/{operating_day}/{service_journey_id}`, `situations/{situation_number}`. Each key template is explained in the event catalog below. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['entur-norway'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `transit/no/entur/entur-norway/et/+/+/+/estimated-vehicle-journey`, `transit/no/entur/entur-norway/vm/+/+/+/monitored-vehicle-journey`, `transit/no/entur/entur-norway/sx/+/+/situation`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('transit/no/entur/entur-norway/et/+/+/+/estimated-vehicle-journey', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.

## Event catalog

### Dated Service Journey

CloudEvents type: `no.entur.DatedServiceJourney`

#### What it tells you

Reference data for a dated service journey in the Norwegian public transport network. A DatedServiceJourney is a specific vehicle journey operating on a particular operating day, identified by its NeTEx ServiceJourney reference and operating day. This reference event is emitted at bridge startup from the SIRI-ET feed and refreshed periodically to provide downstream consumers with the timetable context for subsequent telemetry events.

#### Identity

Each event identifies the real-world resource with `journeys/{operating_day}/{service_journey_id}`. `{operating_day}` is ISO 8601 calendar date string representing the operating day on which this journey runs, extracted from FramedVehicleJourneyRef/DataFrameRef; `{service_journey_id}` is neTEx ServiceJourney identifier extracted from FramedVehicleJourneyRef/DatedVehicleJourneyRef. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `entur-norway`, key `journeys/{operating_day}/{service_journey_id}` |

#### Payload

`Dated Service Journey` payloads are JSON object. Required fields: `service_journey_id`, `operating_day`, `line_ref`, `operator_ref`.

- **`service_journey_id`** (string, required): NeTEx ServiceJourney identifier extracted from FramedVehicleJourneyRef/DatedVehicleJourneyRef. Uniquely identifies the planned vehicle journey within the NeTEx codespace. Example: RUT:ServiceJourney:1-1234.
- **`operating_day`** (string, required): ISO 8601 calendar date string representing the operating day on which this journey runs, extracted from FramedVehicleJourneyRef/DataFrameRef. Example: 2024-01-01. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`line_ref`** (string, required): NeTEx Line reference identifying the line this journey belongs to. Example: RUT:Line:1.
- **`operator_ref`** (string, required): NeTEx Operator or codespace reference identifying the operator responsible for this journey. Example: RUT.
- **`direction_ref`** (string or null, optional): Direction reference for this journey leg, e.g. Outbound or Inbound, or a NeTEx DirectionType value.
- **`vehicle_mode`** (string or null, optional): SIRI VehicleMode describing the mode of transport for this journey. Known values: bus, tram, rail, ferry, metro, water, air, coach, taxi.
- **`route_ref`** (string or null, optional): NeTEx Route reference for this journey, if available.
- **`published_line_name`** (string or null, optional): Public-facing line number or name displayed to passengers on signs and in apps. Example: 31.
- **`external_line_ref`** (string or null, optional): External line reference, typically the same value as line_ref, used for cross-system reconciliation.
- **`origin_name`** (string or null, optional): Human-readable name of the origin stop or place for this journey.
- **`destination_name`** (string or null, optional): Human-readable name of the destination stop or place for this journey.
- **`data_source`** (string or null, optional): Operator codespace originating this data record, as reported in the SIRI DataSource element. Example: RUT.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "service_journey_id": "string",
  "operating_day": "string",
  "line_ref": "string",
  "operator_ref": "string",
  "direction_ref": "string",
  "vehicle_mode": "string",
  "route_ref": "string",
  "published_line_name": "string",
  "external_line_ref": "string",
  "origin_name": "string",
  "destination_name": "string",
  "data_source": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Estimated Vehicle Journey

CloudEvents type: `no.entur.EstimatedVehicleJourney`

#### What it tells you

Real-time estimated timetable update for a vehicle journey from the Entur SIRI-ET feed (GET /realtime/v1/rest/et). Contains updated arrival and departure times for each stop along the journey, cancellation flags, and extra journey markers. Uses incremental requestorId polling to receive only changed journeys since the last poll.

#### Identity

Each event identifies the real-world resource with `journeys/{operating_day}/{service_journey_id}`. `{operating_day}` is ISO 8601 calendar date string representing the operating day on which this journey runs, extracted from FramedVehicleJourneyRef/DataFrameRef; `{service_journey_id}` is neTEx ServiceJourney identifier extracted from FramedVehicleJourneyRef/DatedVehicleJourneyRef. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `entur-norway`, key `journeys/{operating_day}/{service_journey_id}` |
| `MQTT/5.0` | topic `transit/no/entur/entur-norway/et/{operator_ref}/{line_ref}/{service_journey_id}/estimated-vehicle-journey`, retain `false`, QoS `1` |

#### Payload

`Estimated Vehicle Journey` payloads are JSON object. Required fields: `service_journey_id`, `operating_day`, `line_ref`, `operator_ref`, `is_cancellation`, `estimated_calls`.

- **`service_journey_id`** (string, required): NeTEx ServiceJourney identifier extracted from FramedVehicleJourneyRef/DatedVehicleJourneyRef. Uniquely identifies the planned vehicle journey within the NeTEx codespace. Example: RUT:ServiceJourney:1-1234.
- **`operating_day`** (string, required): ISO 8601 calendar date string representing the operating day on which this journey runs, extracted from FramedVehicleJourneyRef/DataFrameRef. Example: 2024-01-01. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`line_ref`** (string, required): NeTEx Line reference identifying the line this journey belongs to. Example: RUT:Line:1.
- **`operator_ref`** (string, required): NeTEx Operator or codespace reference identifying the operator responsible for this journey. Example: RUT.
- **`direction_ref`** (string or null, optional): Direction reference for this journey, e.g. Outbound or Inbound.
- **`vehicle_mode`** (string or null, optional): SIRI VehicleMode describing the mode of transport. Known values: bus, tram, rail, ferry, metro, water, air, coach, taxi.
- **`published_line_name`** (string or null, optional): Public-facing line number or name displayed to passengers. Example: 31.
- **`route_ref`** (string or null, optional): NeTEx Route reference for this journey, if available.
- **`origin_name`** (string or null, optional): Human-readable name of the origin stop or place for this journey.
- **`destination_name`** (string or null, optional): Human-readable name of the destination stop or place for this journey.
- **`is_cancellation`** (boolean, required): True if the entire journey is cancelled. Corresponds to the SIRI Cancellation element on the EstimatedVehicleJourney. Defaults to false.
- **`is_extra_journey`** (boolean or null, optional): True if this is an extra journey added outside the planned timetable (SIRI ExtraJourney).
- **`is_complete_stop_sequence`** (boolean or null, optional): True if the EstimatedCalls list covers all stops in the journey sequence (SIRI IsCompleteStopSequence). False means the list is a partial update.
- **`monitored`** (boolean or null, optional): True if this journey is being actively tracked by an AVL system.
- **`data_source`** (string or null, optional): Operator codespace originating this data record, from the SIRI DataSource element. Example: RUT.
- **`recorded_at_time`** (datetime or null, optional): ISO 8601 UTC timestamp when this update was recorded by the source system (SIRI RecordedAtTime).
- **`estimated_calls`** (array of object, required): Ordered list of estimated arrival and departure times for each stop along the journey. May be a partial list if is_complete_stop_sequence is false.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "service_journey_id": "string",
  "operating_day": "string",
  "line_ref": "string",
  "operator_ref": "string",
  "direction_ref": "string",
  "vehicle_mode": "string",
  "published_line_name": "string",
  "route_ref": "string",
  "origin_name": "string",
  "destination_name": "string",
  "is_cancellation": false,
  "is_extra_journey": false,
  "is_complete_stop_sequence": false,
  "monitored": false,
  "data_source": "string",
  "recorded_at_time": "2024-01-01T00:00:00Z",
  "estimated_calls": [
    {
      "stop_point_ref": "string",
      "order": 0,
      "stop_point_name": "string",
      "aimed_arrival_time": "2024-01-01T00:00:00Z",
      "expected_arrival_time": "2024-01-01T00:00:00Z",
      "aimed_departure_time": "2024-01-01T00:00:00Z",
      "expected_departure_time": "2024-01-01T00:00:00Z",
      "arrival_status": "string",
      "departure_status": "string",
      "departure_platform_name": "string",
      "arrival_boarding_activity": "string",
      "departure_boarding_activity": "string",
      "is_cancellation": false,
      "is_extra_stop": false
    }
  ]
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Monitored Vehicle Journey

CloudEvents type: `no.entur.MonitoredVehicleJourney`

#### What it tells you

Real-time vehicle monitoring update from the Entur SIRI-VM feed (GET /realtime/v1/rest/vm). Contains the current geographic position of a vehicle, its bearing, delay, occupancy status, and the next monitored call. Uses incremental requestorId polling for efficient change delivery.

#### Identity

Each event identifies the real-world resource with `journeys/{operating_day}/{service_journey_id}`. `{operating_day}` is ISO 8601 calendar date string for the operating day of this journey, from FramedVehicleJourneyRef/DataFrameRef; `{service_journey_id}` is neTEx ServiceJourney identifier extracted from FramedVehicleJourneyRef/DatedVehicleJourneyRef. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `entur-norway`, key `journeys/{operating_day}/{service_journey_id}` |
| `MQTT/5.0` | topic `transit/no/entur/entur-norway/vm/{operator_ref}/{line_ref}/{service_journey_id}/monitored-vehicle-journey`, retain `false`, QoS `1` |

#### Payload

`Monitored Vehicle Journey` payloads are JSON object. Required fields: `service_journey_id`, `operating_day`, `recorded_at_time`, `line_ref`, `operator_ref`, `monitored`.

- **`service_journey_id`** (string, required): NeTEx ServiceJourney identifier extracted from FramedVehicleJourneyRef/DatedVehicleJourneyRef. Uniquely identifies the planned vehicle journey. Example: RUT:ServiceJourney:1-1234.
- **`operating_day`** (string, required): ISO 8601 calendar date string for the operating day of this journey, from FramedVehicleJourneyRef/DataFrameRef. Example: 2024-01-01. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`recorded_at_time`** (datetime, required): ISO 8601 UTC timestamp from the parent VehicleActivity/RecordedAtTime element indicating when this position was recorded.
- **`line_ref`** (string, required): NeTEx Line reference identifying the line this journey belongs to. Example: RUT:Line:1.
- **`operator_ref`** (string, required): NeTEx Operator or codespace reference for the operator running this journey. Example: RUT.
- **`direction_ref`** (string or null, optional): Direction reference for this journey, e.g. Outbound or Inbound.
- **`vehicle_mode`** (string or null, optional): SIRI VehicleMode describing the mode of transport. Known values: bus, tram, rail, ferry, metro, water, air, coach, taxi.
- **`published_line_name`** (string or null, optional): Public-facing line number or name displayed to passengers. Example: 31.
- **`origin_name`** (string or null, optional): Human-readable name of the origin stop or place for this journey.
- **`destination_name`** (string or null, optional): Human-readable name of the destination stop or place for this journey.
- **`vehicle_ref`** (string or null, optional): Vehicle identifier from the SIRI VehicleRef element. Identifies the physical vehicle (e.g. bus number), not the journey. Not used as a Kafka key.
- **`latitude`** (double or null, optional, degrees): WGS84 latitude of the vehicle's current position in decimal degrees, from VehicleLocation/Latitude. Constraints: minimum `-90.0`, maximum `90.0`.
- **`longitude`** (double or null, optional, degrees): WGS84 longitude of the vehicle's current position in decimal degrees, from VehicleLocation/Longitude. Constraints: minimum `-180.0`, maximum `180.0`.
- **`bearing`** (double or null, optional, degrees): Compass bearing in degrees (0-360) indicating the direction of travel, from the SIRI Bearing element. Constraints: minimum `0.0`, maximum `360.0`.
- **`delay_seconds`** (int32 or null, optional, s): Current delay in integer seconds, parsed from the ISO 8601 Duration value in the SIRI Delay element. Positive values indicate lateness; negative values indicate running early.
- **`occupancy_status`** (string or null, optional): Passenger occupancy status of the vehicle from the SIRI OccupancyStatus element.
- **`progress_status`** (string or null, optional): Journey progress status from the SIRI ProgressStatus element indicating whether the journey is running normally or has been cancelled/skipped.
- **`monitored`** (boolean, required): True if this journey is being actively tracked by an AVL system, from the SIRI Monitored element.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "service_journey_id": "string",
  "operating_day": "string",
  "recorded_at_time": "2024-01-01T00:00:00Z",
  "line_ref": "string",
  "operator_ref": "string",
  "direction_ref": "string",
  "vehicle_mode": "string",
  "published_line_name": "string",
  "origin_name": "string",
  "destination_name": "string",
  "vehicle_ref": "string",
  "latitude": 0,
  "longitude": 0,
  "bearing": 0,
  "delay_seconds": 0,
  "occupancy_status": "string",
  "progress_status": "string",
  "monitored": false
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Pt Situation Element

CloudEvents type: `no.entur.PtSituationElement`

#### What it tells you

Real-time transit disruption or service alert from the Entur SIRI-SX feed (GET /realtime/v1/rest/sx). Represents a published situation element describing a service disruption, delay cause, or passenger information notice. Includes affected lines, stops, severity level, and validity periods.

#### Identity

Each event identifies the real-world resource with `situations/{situation_number}`. `{situation_number}` is unique situation identifier from the SIRI SituationNumber element. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `entur-norway`, key `situations/{situation_number}` |
| `MQTT/5.0` | topic `transit/no/entur/entur-norway/sx/{severity}/{situation_number}/situation`, retain `false`, QoS `1` |

#### Payload

`Pt Situation Element` payloads are JSON object. Required fields: `situation_number`, `creation_time`, `severity`.

- **`situation_number`** (string, required): Unique situation identifier from the SIRI SituationNumber element. Used as the Kafka key. Example: RUT:SituationNumber:12345.
- **`version`** (string or null, optional): Version number of this situation record, from the SIRI Version element. Increments with each update to the same situation.
- **`creation_time`** (datetime, required): ISO 8601 UTC timestamp when this situation was first created, from the SIRI CreationTime element.
- **`source_type`** (string or null, optional): Type of the originating source system from the SIRI Source/SourceType element.
- **`source_name`** (string or null, optional): Name of the originating source organisation from the SIRI Source/Name element.
- **`progress`** (string or null, optional): Publication progress state of this situation from the SIRI Progress element.
- **`severity`** (string, required): SIRI Severity classification of the impact of this situation on passenger services, or 'unknown' when absent.
- **`keywords`** (string or null, optional): Space-separated list of classification keywords from the SIRI Keywords element, used to categorise the situation type.
- **`summary`** (string or null, optional): Short public-facing summary text in Norwegian or English describing the situation, from the SIRI Summary element.
- **`description`** (string or null, optional): Full public-facing descriptive text in Norwegian or English providing details about the situation, from the SIRI Description element.
- **`affects_line_refs`** (array of string, optional): List of NeTEx LineRef values identifying the lines affected by this situation, extracted from Affects/Networks/AffectedNetwork/AffectedLine/LineRef elements.
- **`affects_stop_point_refs`** (array of string, optional): List of NSR StopPointRef values identifying the stop points affected by this situation, extracted from Affects/StopPoints/AffectedStopPoint/StopPointRef elements.
- **`validity_periods`** (array of object, optional): One or more time windows during which this situation is active, from the SIRI ValidityPeriod elements.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "situation_number": "string",
  "version": "string",
  "creation_time": "2024-01-01T00:00:00Z",
  "source_type": "string",
  "source_name": "string",
  "progress": "string",
  "severity": "string",
  "keywords": "string",
  "summary": "string",
  "description": "string",
  "affects_line_refs": [
    "string"
  ],
  "affects_stop_point_refs": [
    "string"
  ],
  "validity_periods": [
    {
      "start_time": "2024-01-01T00:00:00Z",
      "end_time": "2024-01-01T00:00:00Z"
    }
  ]
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

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

- The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- The MQTT variant publishes with QoS 1 and retained-message Last-Known-Value semantics where declared in the event catalog.
- Reference/catalog events are documented as startup emissions, with periodic refresh when the source supports it.

## References

- xRegistry manifest: [`xreg/entur-norway.xreg.json`](xreg/entur-norway.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
