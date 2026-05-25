# TfL Road Traffic Events

TfL Road Traffic publishes road disruption and traffic status updates from Transport for London for London roads and disruption areas. These events help consumers monitor mobility operations, passenger information, and traffic conditions without polling the upstream source directly.

## At a glance

- **Event types:** 3 documented event types (19 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 1 reference/catalog event type and 2 telemetry event types.
- **Identity:** `roads/{road_id}`, `disruptions/{road_id}/{severity}/{disruption_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `tfl-road-traffic`. The record key is `roads/{road_id}`, `disruptions/{road_id}/{severity}/{disruption_id}`. Each key template is explained in the event catalog below. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['tfl-road-traffic'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `traffic/gb/tfl/tfl-road-traffic/roads/+/corridor`, `traffic/gb/tfl/tfl-road-traffic/roads/+/status`, `traffic/gb/tfl/tfl-road-traffic/disruptions/+/serious/+`, `traffic/gb/tfl/tfl-road-traffic/disruptions/+/severe/+`, `traffic/gb/tfl/tfl-road-traffic/disruptions/+/moderate/+`, `traffic/gb/tfl/tfl-road-traffic/disruptions/+/minor/+`, `traffic/gb/tfl/tfl-road-traffic/disruptions/+/information/+`, `traffic/gb/tfl/tfl-road-traffic/disruptions/+/closure/+`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('traffic/gb/tfl/tfl-road-traffic/roads/+/corridor', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `tfl-road-traffic`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/tfl-road-traffic')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Road Corridor

CloudEvents type: `uk.gov.tfl.road.RoadCorridor`

#### What it tells you

Reference record for a TfL managed road corridor fetched from GET /Road.

#### Identity

Each event identifies the real-world resource with `roads/{road_id}`. `{road_id}` is unique identifier for the road corridor as used by the TfL Unified API. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `tfl-road-traffic`, key `roads/{road_id}` |
| `MQTT/5.0` | topic `traffic/gb/tfl/tfl-road-traffic/roads/{road_id}/corridor`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqp://localhost:5672/tfl-road-traffic`, message subject `roads/{road_id}`; application properties road_id `{road_id}` |

#### Payload

`Road Corridor` payloads are JSON object. Required fields: `road_id`, `display_name`.

- **`road_id`** (string, required): Unique identifier for the road corridor as used by the TfL Unified API. Corresponds to 'id' in the upstream response. Examples: 'a2', 'a12', 'm25'. Used as the stable domain key.
- **`display_name`** (string, required): Human-readable display name for the road corridor as reported by TfL. Corresponds to 'displayName' in the upstream response. Examples: 'A2', 'A12', 'M25'.
- **`status_severity`** (string or null, optional): Current aggregate status severity for this corridor as assessed by TfL. Corresponds to 'statusSeverity' in the upstream response. Common values: 'Good', 'Moderate', 'Serious', 'Severe', 'NoDisruptions'.
- **`status_severity_description`** (string or null, optional): Human-readable description of the current status severity. Corresponds to 'statusSeverityDescription' in the upstream response. Example: 'Serious Delays'.
- **`bounds`** (string or null, optional): Bounding box for the road corridor as a JSON array string. Corresponds to 'bounds' in the upstream response. Format: '[[lon_sw,lat_sw],[lon_ne,lat_ne]]' in WGS84 decimal degrees.
- **`envelope`** (string or null, optional): GeoJSON envelope polygon for the road corridor geometry. Corresponds to 'envelope' in the upstream response.
- **`url`** (string or null, optional): URL to the TfL Unified API detail page for this corridor. Corresponds to 'url' in the upstream response.
- **`status_aggregation_start_date`** (datetime or null, optional): Start date of the current status aggregation period reported by TfL. Corresponds to 'statusAggregationStartDate' in the upstream response.
- **`status_aggregation_end_date`** (datetime or null, optional): End date of the current status aggregation period reported by TfL. Corresponds to 'statusAggregationEndDate' in the upstream response.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "road_id": "string",
  "display_name": "string",
  "status_severity": "string",
  "status_severity_description": "string",
  "bounds": "string",
  "envelope": "string",
  "url": "string",
  "status_aggregation_start_date": "2024-01-01T00:00:00Z",
  "status_aggregation_end_date": "2024-01-01T00:00:00Z"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Road Status

CloudEvents type: `uk.gov.tfl.road.RoadStatus`

#### What it tells you

Real-time status snapshot for a TfL managed road corridor fetched from GET /Road/all/Status.

#### Identity

Each event identifies the real-world resource with `roads/{road_id}`. `{road_id}` is unique identifier for the road corridor as used by the TfL Unified API. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `tfl-road-traffic`, key `roads/{road_id}` |
| `MQTT/5.0` | topic `traffic/gb/tfl/tfl-road-traffic/roads/{road_id}/status`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqp://localhost:5672/tfl-road-traffic`, message subject `roads/{road_id}`; application properties road_id `{road_id}` |

#### Payload

`Road Status` payloads are JSON object. Required fields: `road_id`, `display_name`.

- **`road_id`** (string, required): Unique identifier for the road corridor as used by the TfL Unified API. Corresponds to 'id' in the upstream response. Examples: 'a2', 'a12', 'm25'. Used as the stable domain key.
- **`display_name`** (string, required): Human-readable display name for the road corridor as reported by TfL. Corresponds to 'displayName' in the upstream response. Examples: 'A2', 'A12', 'M25'.
- **`status_severity`** (string or null, optional): Current aggregate status severity for this corridor as assessed by TfL. Corresponds to 'statusSeverity' in the upstream response. Common values: 'Good', 'Moderate', 'Serious', 'Severe', 'NoDisruptions'.
- **`status_severity_description`** (string or null, optional): Human-readable description of the current status severity. Corresponds to 'statusSeverityDescription' in the upstream response. Example: 'Serious Delays'.
- **`bounds`** (string or null, optional): Bounding box for the road corridor as a JSON array string. Corresponds to 'bounds' in the upstream response. Format: '[[lon_sw,lat_sw],[lon_ne,lat_ne]]' in WGS84 decimal degrees.
- **`envelope`** (string or null, optional): GeoJSON envelope polygon for the road corridor geometry. Corresponds to 'envelope' in the upstream response.
- **`url`** (string or null, optional): URL to the TfL Unified API detail page for this corridor. Corresponds to 'url' in the upstream response.
- **`status_aggregation_start_date`** (datetime or null, optional): Start date of the current status aggregation period reported by TfL. Corresponds to 'statusAggregationStartDate' in the upstream response.
- **`status_aggregation_end_date`** (datetime or null, optional): End date of the current status aggregation period reported by TfL. Corresponds to 'statusAggregationEndDate' in the upstream response.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "road_id": "string",
  "display_name": "string",
  "status_severity": "string",
  "status_severity_description": "string",
  "bounds": "string",
  "envelope": "string",
  "url": "string",
  "status_aggregation_start_date": "2024-01-01T00:00:00Z",
  "status_aggregation_end_date": "2024-01-01T00:00:00Z"
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Road Disruption

CloudEvents type: `uk.gov.tfl.road.RoadDisruption`

#### What it tells you

Real-time road disruption event on the TfL road network fetched from GET /Road/all/Disruption.

#### Identity

Each event identifies the real-world resource with `disruptions/{road_id}/{severity}/{disruption_id}`. `{road_id}` is primary affected TfL road corridor identifier used by MQTT/UNS topics; `{severity}` is normalized TfL-native severity for MQTT partitioning; `{disruption_id}` is unique identifier for the disruption assigned by the TfL Traffic Information Management System (TIMS). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `tfl-road-traffic`, key `disruptions/{road_id}/{severity}/{disruption_id}` |
| `MQTT/5.0` | topic `traffic/gb/tfl/tfl-road-traffic/disruptions/{road_id}/serious/{disruption_id}`, retain `false`, QoS `1` |
| `MQTT/5.0` | topic `traffic/gb/tfl/tfl-road-traffic/disruptions/{road_id}/severe/{disruption_id}`, retain `false`, QoS `1` |
| `MQTT/5.0` | topic `traffic/gb/tfl/tfl-road-traffic/disruptions/{road_id}/moderate/{disruption_id}`, retain `false`, QoS `1` |
| `MQTT/5.0` | topic `traffic/gb/tfl/tfl-road-traffic/disruptions/{road_id}/minor/{disruption_id}`, retain `false`, QoS `1` |
| `MQTT/5.0` | topic `traffic/gb/tfl/tfl-road-traffic/disruptions/{road_id}/information/{disruption_id}`, retain `false`, QoS `1` |
| `MQTT/5.0` | topic `traffic/gb/tfl/tfl-road-traffic/disruptions/{road_id}/closure/{disruption_id}`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `amqp://localhost:5672/tfl-road-traffic`, message subject `disruptions/{road_id}/{severity}/{disruption_id}`; application properties road_id `{road_id}`, severity `{severity}`, disruption_id `{disruption_id}` |

#### Payload

`Road Disruption` payloads are JSON object. Required fields: `road_id`, `disruption_id`, `severity`.

- **`road_id`** (string, required): Primary affected TfL road corridor identifier used by MQTT/UNS topics. Derived from the first upstream corridorIds entry when present, otherwise 'unknown'.
- **`disruption_id`** (string, required): Unique identifier for the disruption assigned by the TfL Traffic Information Management System (TIMS). Corresponds to 'id' in the upstream response. Format: 'TIMS-NNNNN' or similar TIMS prefix.
- **`category`** (string or null, optional): Top-level category of the disruption. Corresponds to 'category' in the upstream response. Common values: 'RealTime' for live incidents, 'PlannedWork' for scheduled roadworks.
- **`sub_category`** (string or null, optional): More detailed sub-category of the disruption. Corresponds to 'subCategory' in the upstream response. Examples: 'TfL planned works', 'Utility works', 'Incident', 'Traffic signal failure'.
- **`severity`** (string, required): Normalized TfL-native severity for MQTT partitioning. Values: serious, severe, moderate, minor, information, closure. Upstream values are normalized to lowercase-kebab.
- **`ordinal`** (int32 or null, optional): Ordinal rank of this disruption used for ordering within a severity level. Corresponds to 'ordinal' in the upstream response.
- **`url`** (string or null, optional): URL to the TfL Unified API detail page for this disruption. Corresponds to 'url' in the upstream response.
- **`point`** (string or null, optional): Representative point location of the disruption as a WKT or coordinate string. Corresponds to 'point' in the upstream response.
- **`comments`** (string or null, optional): Free-text comments describing the disruption context. Corresponds to 'comments' in the upstream response. May include street names, junction descriptions, or operational notes.
- **`current_update`** (string or null, optional): Latest operational update text for this disruption. Corresponds to 'currentUpdate' in the upstream response. Updated by TfL operators as the situation evolves.
- **`current_update_datetime`** (datetime or null, optional): Timestamp when the current update text was last modified. Corresponds to 'currentUpdateDateTime' in the upstream response.
- **`corridor_ids`** (array of string, optional): Array of road corridor identifiers affected by this disruption. Corresponds to 'corridorIds' in the upstream response. Examples: ['a2', 'a12']. May be empty or null for disruptions not associated with a specific named corridor.
- **`start_datetime`** (datetime or null, optional): Scheduled or actual start date and time of the disruption. Corresponds to 'startDateTime' in the upstream response.
- **`end_datetime`** (datetime or null, optional): Scheduled or actual end date and time of the disruption. Corresponds to 'endDateTime' in the upstream response. May be null for open-ended incidents.
- **`last_modified_time`** (datetime or null, optional): Timestamp when this disruption record was last modified in the TfL system. Corresponds to 'lastModifiedTime' in the upstream response. Used for deduplication: disruptions are re-emitted only when this value changes.
- **`level_of_interest`** (string or null, optional): TfL classification of the level of public interest for this disruption. Corresponds to 'levelOfInterest' in the upstream response. Examples: 'Low', 'Medium', 'High'.
- **`location`** (string or null, optional): Free-text textual description of the disruption location. Corresponds to 'location' in the upstream response.
- **`is_provisional`** (boolean or null, optional): Whether the disruption timing or details are provisional and subject to change. Corresponds to 'isProvisional' in the upstream response.
- **`has_closures`** (boolean or null, optional): Whether this disruption includes full or partial road closures. Corresponds to 'hasClosures' in the upstream response.
- **`streets`** (array of object, optional): Array of street segments affected by this disruption. Corresponds to 'streets' in the upstream response. Each entry describes an individual street with its closure type, affected directions, and geometry.
- **`geography`** (string or null, optional): GeoJSON geometry of the disruption area as a JSON string. Corresponds to 'geography' in the upstream response. May be a Point, LineString, or Polygon representing the spatial extent of the disruption.
- **`geometry`** (string or null, optional): Secondary geometry field from the TfL database as a JSON string. Corresponds to 'geometry' in the upstream response. May contain database geometry in an alternate representation.
- **`status`** (string or null, optional): Current lifecycle status of the disruption. Corresponds to 'status' in the upstream response.
- **`is_active`** (boolean or null, optional): Whether this disruption is currently active. Corresponds to 'isActive' in the upstream response.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "road_id": "string",
  "disruption_id": "string",
  "category": "string",
  "sub_category": "string",
  "severity": "string",
  "ordinal": 0,
  "url": "string",
  "point": "string",
  "comments": "string",
  "current_update": "string",
  "current_update_datetime": "2024-01-01T00:00:00Z",
  "corridor_ids": [
    "string"
  ],
  "start_datetime": "2024-01-01T00:00:00Z",
  "end_datetime": "2024-01-01T00:00:00Z",
  "last_modified_time": "2024-01-01T00:00:00Z",
  "level_of_interest": "string",
  "location": "string",
  "is_provisional": false,
  "has_closures": false,
  "streets": [
    {
      "name": "string",
      "closure": "string",
      "directions": "string",
      "source_system_id": "string",
      "source_system_key": "string"
    }
  ],
  "geography": "string",
  "geometry": "string",
  "status": "string",
  "is_active": false
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

- xRegistry manifest: [`xreg/tfl_road_traffic.xreg.json`](xreg/tfl_road_traffic.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- Transport for London (TfL) Unified API: <https://api.tfl.gov.uk/>
- Road API documentation: <https://api.tfl.gov.uk/swagger/ui/index.html#!/Road>
