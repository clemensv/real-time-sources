# OpenStreetMap Minutely Diffs Bridge Events

MQTT/5.0 UNS variants of the Wikimedia OSM Diffs CloudEvents. The minutely diff stream is split into three non-retained firehose families (node, way, relation) under osm/intl/wikimedia/wikimedia-osm-diffs/<family>/{geohash5}/{element_id}/change with QoS 0 and retain=false, and one retained side-channel snapshot for the OSM replication sequence published to osm/intl/wikimedia/wikimedia-osm-diffs/replication-state/replication-state with retain=true so late subscribers can see the most recent processed sequence number on connect.

## At a glance

- **Event types:** 2 documented event types (8 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 2 telemetry event types.
- **Identity:** `{element_type}/{element_id}`, `replication_state` identifies the resource each event is about.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `wikimedia-osm-diffs`. The record key is `{element_type}/{element_id}`, `replication_state`. Each key template is explained in the event catalog below. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['wikimedia-osm-diffs'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `osm/intl/wikimedia/wikimedia-osm-diffs/node/+/+/change`, `osm/intl/wikimedia/wikimedia-osm-diffs/way/+/+/change`, `osm/intl/wikimedia/wikimedia-osm-diffs/relation/+/+/change`, `osm/intl/wikimedia/wikimedia-osm-diffs/replication-state/replication-state`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('osm/intl/wikimedia/wikimedia-osm-diffs/node/+/+/change', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `wikimedia-osm-diffs`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/wikimedia-osm-diffs')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Map Change

CloudEvents type: `Org.OpenStreetMap.Diffs.MapChange`

#### What it tells you

An individual element change from the OpenStreetMap minutely replication diff feed. Each event represents a single create, modify, or delete operation on a node, way, or relation in the OSM database. The diff files are OsmChange XML documents published every 60 seconds at https://planet.openstreetmap.org/replication/minute/.

#### Identity

Each event identifies the real-world resource with `{element_type}/{element_id}`. `{element_type}` is the OSM element type: node, way, or relation; `{element_id}` is the unique numeric identifier of the OSM element within its element type namespace. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `wikimedia-osm-diffs`, key `{element_type}/{element_id}` |
| `MQTT/5.0` | topic `osm/intl/wikimedia/wikimedia-osm-diffs/node/{geohash5}/{element_id}/change`, retain `false`, QoS `0` |
| `MQTT/5.0` | topic `osm/intl/wikimedia/wikimedia-osm-diffs/way/{geohash5}/{element_id}/change`, retain `false`, QoS `0` |
| `MQTT/5.0` | topic `osm/intl/wikimedia/wikimedia-osm-diffs/relation/{geohash5}/{element_id}/change`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/wikimedia-osm-diffs`, message subject `{element_type}/{element_id}` |

#### Payload

`Map Change` payloads are JSON object. Required fields: `change_type`, `element_type`, `element_id`, `geohash5`, `version`, `timestamp`, `changeset_id`, `tags`, `sequence_number`.

- **`change_type`** (string, required): The type of change applied to the element in this replication diff: create, modify, or delete, corresponding to the OsmChange XML sections.
- **`element_type`** (string, required): The OSM element type: node, way, or relation. Nodes carry geographic coordinates; ways and relations reference other elements.
- **`element_id`** (int64, required): The unique numeric identifier of the OSM element within its element type namespace. Combined with element_type, this forms the globally unique OSM element identity.
- **`geohash5`** (string, required): Five-character base32 geohash of the element's representative coordinate. For nodes, derived from latitude/longitude; for ways and relations, derived from the centroid of any embedded bbox. The sentinel 'nogeo' is emitted for elements with no resolvable coordinate (most relation deletes, member-only edits, etc.) so the UNS topic placeholder always resolves to a fixed-shape lowercase ASCII segment.
- **`version`** (int32, required): The version number of this element. Each edit to an element increments the version by one.
- **`timestamp`** (datetime, required): The UTC timestamp when this element version was created or last modified in the OSM database, as recorded in the OsmChange XML.
- **`changeset_id`** (int64, required): The numeric identifier of the OSM changeset that contains this element change. A changeset groups related edits by a single user.
- **`user_name`** (string or null, optional): The display name of the OSM user who made this edit. May be null for redacted or anonymous edits.
- **`user_id`** (int64 or null, optional): The numeric user identifier of the OSM contributor. May be null for redacted or anonymous edits.
- **`latitude`** (double or null, optional): The WGS-84 latitude of the node in decimal degrees. Present only when element_type is node; null for ways and relations.
- **`longitude`** (double or null, optional): The WGS-84 longitude of the node in decimal degrees. Present only when element_type is node; null for ways and relations.
- **`tags`** (string, required): JSON-encoded object of key-value tag pairs attached to this element. Tags describe the element's real-world features such as name, highway type, or building classification. Encoded as a JSON string because xreg does not natively support map types.
- **`sequence_number`** (int64, required): The replication sequence number of the minutely diff file that contained this change. Useful for correlating changes back to specific replication state.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "change_type": "string",
  "element_type": "string",
  "element_id": 0,
  "geohash5": "string",
  "version": 0,
  "timestamp": "2024-01-01T00:00:00Z",
  "changeset_id": 0,
  "user_name": "string",
  "user_id": 0,
  "latitude": 0,
  "longitude": 0,
  "tags": "string",
  "sequence_number": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Replication State

CloudEvents type: `Org.OpenStreetMap.Diffs.ReplicationState`

#### What it tells you

Current replication state from the OpenStreetMap minutely diff feed. Emitted once per poll cycle to record which replication sequence was just processed. The state is read from https://planet.openstreetmap.org/replication/minute/state.txt.

#### Identity

Each event identifies the real-world resource with `replication_state`. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `wikimedia-osm-diffs`, key `replication_state` |
| `MQTT/5.0` | topic `osm/intl/wikimedia/wikimedia-osm-diffs/replication-state/replication-state`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/wikimedia-osm-diffs`, message subject `replication_state` |

#### Payload

`Replication State` payloads are JSON object. Required fields: `sequence_number`, `timestamp`.

- **`sequence_number`** (int64, required): The monotonically increasing sequence number of the latest processed minutely diff file. Each diff file corresponds to exactly one sequence number.
- **`timestamp`** (datetime, required): The UTC timestamp associated with the replication state, indicating the point in time up to which the diff file covers OSM edits.
- **`source_url`** (string or null, optional): The replication state document URL from which this snapshot was parsed. Useful so subscribers can re-derive the diff file URL or compare across mirror feeds. Null when the bridge does not record the URL.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "sequence_number": 0,
  "timestamp": "2024-01-01T00:00:00Z",
  "source_url": "string"
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

- xRegistry manifest: [`xreg/wikimedia_osm_diffs.xreg.json`](xreg/wikimedia_osm_diffs.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
