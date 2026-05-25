# Blitzortung live lightning bridge Events

MQTT/5.0 non-retained UNS variant of the Blitzortung LightningStroke CloudEvent. Topic carries the source-scoped stroke id plus geohash5 (~5 km) and geohash7 (~150 m) cells so subscribers can wildcard by location at two zoom levels. QoS 0, retain=false — no LKV slot for a firehose.

## At a glance

- **Event types:** 1 documented event type (2 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0
- **Reference vs telemetry:** 0 reference/catalog event types and 1 telemetry event type.
- **Identity:** `{source_id}/{stroke_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `blitzortung`. The record key is `{source_id}/{stroke_id}`. In plain language, `{source_id}/{stroke_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['blitzortung'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `weather/intl/blitzortung/blitzortung/+/+/+/stroke`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('weather/intl/blitzortung/blitzortung/+/+/+/stroke', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.

## Event catalog

### Lightning Stroke

CloudEvents type: `Blitzortung.Lightning.LightningStroke`

#### What it tells you

Live lightning-stroke event from the public LightningMaps / Blitzortung websocket feed. Each event represents one source-scoped stroke identifier with its observation time, coordinates, upstream delay and accuracy values, and optionally the detector participation flags carried in the public sta object. One located lightning stroke from the public LightningMaps / Blitzortung live websocket feed.

#### Identity

Each event identifies the real-world resource with `{source_id}/{stroke_id}`. `{source_id}` is upstream live-source identifier from the src field; `{stroke_id}` is source-scoped stroke identifier from the upstream id field, stringified so the Kafka key and CloudEvents subject can be resolved directly from the payload. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `blitzortung`, key `{source_id}/{stroke_id}` |
| `MQTT/5.0` | topic `weather/intl/blitzortung/blitzortung/{geohash5}/{geohash7}/{stroke_id}/stroke`, retain `false`, QoS `0` |

#### Payload

`Lightning Stroke` payloads are JSON object. Required fields: `source_id`, `stroke_id`, `event_time`, `event_timestamp_ms`, `latitude`, `longitude`, `detector_participations`, `geohash5`, `geohash7`.

- **`source_id`** (int32, required): Upstream live-source identifier from the src field. The public LightningMaps websocket treats stroke ids as source-scoped, so this field is part of the stable event identity. Constraints: minimum `0`.
- **`stroke_id`** (string, required): Source-scoped stroke identifier from the upstream id field, stringified so the Kafka key and CloudEvents subject can be resolved directly from the payload.
- **`event_time`** (string, required): ISO-8601 UTC timestamp derived from the upstream time field, which the public live websocket emits in Unix epoch milliseconds.
- **`event_timestamp_ms`** (int64, required): Original upstream time value in Unix epoch milliseconds from the public live websocket. Constraints: minimum `0`.
- **`latitude`** (double, required): Latitude of the located lightning stroke in decimal degrees from the upstream lat field. Constraints: minimum `-90.0`, maximum `90.0`.
- **`longitude`** (double, required): Longitude of the located lightning stroke in decimal degrees from the upstream lon field. Constraints: minimum `-180.0`, maximum `180.0`.
- **`server_id`** (int32 or null, optional): Upstream server identifier from the srv field that produced the current live batch. The public documentation reviewed during implementation does not publish a stable human-readable enumeration for these ids. Constraints: minimum `0`.
- **`server_delay_ms`** (int32 or null, optional, millisecond (ms)): Delay between the upstream server receiving or computing the stroke and sending it to the live client, in milliseconds, from the public del field. Constraints: minimum `0`.
- **`accuracy_diameter_m`** (double or null, optional, meter (m)): Estimated accuracy diameter in meters from the upstream dev field. The public LightningMaps client renders an accuracy circle with radius dev/2, which indicates the value is expressed as a diameter rather than a raw algorithm score. Constraints: minimum `0.0`.
- **`detector_participations`** (array of object, required): Detector participation entries expanded from the upstream sta object when the client asks the public live feed to include station details. An empty array means the upstream batch did not include detector participation details for this stroke.
- **`geohash5`** (string, required): 5-character geohash of the located stroke (~40 km cell at the equator), derived in the bridge from latitude and longitude. Used as the {geohash5} MQTT topic segment for geographic wildcards. Constraints: pattern `^[0-9b-hjkmnp-z]{5}$`.
- **`geohash7`** (string, required): 7-character geohash of the located stroke (~153 m cell), derived from latitude and longitude. Used as the {geohash7} MQTT topic segment for fine-grained geographic wildcards. Constraints: pattern `^[0-9b-hjkmnp-z]{7}$`.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "source_id": 0,
  "stroke_id": "string",
  "event_time": "string",
  "event_timestamp_ms": 0,
  "latitude": 0,
  "longitude": 0,
  "server_id": 0,
  "server_delay_ms": 0,
  "accuracy_diameter_m": 0,
  "detector_participations": [
    {
      "station_id": 0,
      "status": 0
    }
  ],
  "geohash5": "string",
  "geohash7": "string"
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

- The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.

## References

- xRegistry manifest: [`xreg/blitzortung.xreg.json`](xreg/blitzortung.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
