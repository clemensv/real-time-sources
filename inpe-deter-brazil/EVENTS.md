# INPE DETER Brazil - Deforestation Alerts Events

MQTT/5.0 transport variants for INPE DETER Brazil deforestation and related land-disturbance alerts. The UNS topic tree is deforestation/br/inpe/inpe-deter-brazil/{biome}/{state_slug}/{class_slug}/{alert_id}/alert. Payloads are JSON binary-mode CloudEvents. QoS 1 is used for at-least-once alert delivery; consumers MUST deduplicate by alert_id. retain=false is used because DETER alerts are immutable historical events and retaining each alert_id topic would create an unbounded retained-message graveyard. A Message Expiry Interval of 604800 seconds bounds queued delivery for offline durable subscribers. The state_slug axis is a lowercased Brazilian UF code or unknown when INPE omits or publishes an unsupported UF; class_slug is a supported topic-safe lowercase-kebab DETER class or unknown.

## At a glance

- **Event types:** 1 documented event type (2 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0
- **Reference vs telemetry:** 0 reference/catalog event types and 1 telemetry event type.
- **Identity:** `{biome}/{alert_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `inpe-deter-brazil`. The record key is `{biome}/{alert_id}`. In plain language, `{biome}/{alert_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['inpe-deter-brazil'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `deforestation/br/inpe/inpe-deter-brazil/+/+/+/+/alert`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('deforestation/br/inpe/inpe-deter-brazil/+/+/+/+/alert', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.

## Event catalog

### Deforestation Alert

CloudEvents type: `BR.INPE.DETER.DeforestationAlert`

#### What it tells you

INPE DETER deforestation alert for Amazon and Cerrado biomes.

#### Identity

Each event identifies the real-world resource with `{biome}/{alert_id}`. `{biome}` is biome of the alert: amazon or cerrado; `{alert_id}` is stable reference ID from INPE (gid). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `inpe-deter-brazil`, key `{biome}/{alert_id}` |
| `MQTT/5.0` | topic `deforestation/br/inpe/inpe-deter-brazil/{biome}/{state_slug}/{class_slug}/{alert_id}/alert`, retain `false`, QoS `1` |

#### Payload

`Deforestation Alert` payloads are JSON object. Required fields: `alert_id`, `biome`, `classname`, `view_date`, `satellite`, `sensor`, `area_km2`, `centroid_latitude`, `centroid_longitude`.

- **`alert_id`** (string, required): Stable reference ID from INPE (gid).
- **`biome`** (enum, required): Biome of the alert: amazon or cerrado.
- **`classname`** (string, required): Deforestation class: DESMATAMENTO_CR, DEGRADACAO, MINERACAO, CS_DESORDENADO, etc.
- **`view_date`** (string, required): Observation date in YYYY-MM-DD format.
- **`satellite`** (string, required): Satellite name (CBERS-4, Amazonia-1, etc.).
- **`sensor`** (string, required): Sensor name (AWFI, WFI, MSI).
- **`area_km2`** (double, required): Area of the deforestation polygon in square kilometers.
- **`municipality`** (string or null, optional): Municipality name.
- **`state_code`** (string or null, optional): Brazilian state code (UF), e.g. PA, MT, when provided by INPE; null when omitted. The topic-safe state_slug field is used for MQTT routing.
- **`path_row`** (string or null, optional): Satellite path/row identifier.
- **`publish_month`** (string or null, optional): Publication month in YYYY-MM-DD format.
- **`centroid_latitude`** (double, required): Latitude of the polygon centroid in decimal degrees.
- **`centroid_longitude`** (double, required): Longitude of the polygon centroid in decimal degrees.
- **`state_slug`** (string, optional): Lowercased Brazilian state code (UF), e.g. pa, mt, used as a topic-safe MQTT routing axis; unknown when INPE omits the UF. Constraints: pattern `^([a-z]{2}|unknown)$`.
- **`class_slug`** (enum, optional): Lowercase-kebab normalized DETER class used as a topic-safe MQTT routing axis, e.g. desmatamento-cr, degradacao, mineracao. Constraints: pattern `^[a-z0-9][a-z0-9-]*$`.
##### `biome` values

- `amazon`
- `cerrado`
##### `class_slug` values

- `desmatamento-cr`
- `desmatamento-veg`
- `degradacao`
- `mineracao`
- `cs-desordenado`
- `cs-geometrico`
- `cicatriz-de-queimada`
- `corte-seletivo`
- `unknown`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "alert_id": "string",
  "biome": "amazon",
  "classname": "string",
  "view_date": "string",
  "satellite": "string",
  "sensor": "string",
  "area_km2": 0,
  "municipality": "string",
  "state_code": "string",
  "path_row": "string",
  "publish_month": "string",
  "centroid_latitude": 0,
  "centroid_longitude": 0,
  "state_slug": "string",
  "class_slug": "desmatamento-cr"
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
- The MQTT variant publishes with QoS 1 and retained-message Last-Known-Value semantics where declared in the event catalog.

## References

- xRegistry manifest: [`xreg/inpe_deter_brazil.xreg.json`](xreg/inpe_deter_brazil.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
