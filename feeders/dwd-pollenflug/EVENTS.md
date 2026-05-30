# DWD Pollenflug Events

DWD Pollenflug publishes pollen exposure forecasts by region and plant type from Germany's Deutscher Wetterdienst (DWD) for German pollen forecast regions. These events help consumers build monitoring, alerting, analytics, and dashboards without polling the upstream API directly.

## At a glance

- **Event types:** 2 documented event types (6 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 2 telemetry event types.
- **Identity:** `{region_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `dwd-pollenflug`. The record key is `{region_id}`. In plain language, `{region_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['dwd-pollenflug'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `air-quality/de/dwd/dwd-pollenflug/+/info`, `air-quality/de/dwd/dwd-pollenflug/+/+/pollen-forecast`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('air-quality/de/dwd/dwd-pollenflug/+/info', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `dwd-pollenflug`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/dwd-pollenflug')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Region

CloudEvents type: `DE.DWD.Pollenflug.Region`

#### What it tells you

A reference record published by Germany's Deutscher Wetterdienst (DWD). It lets consumers label, group, and route the live measurement or forecast events.

#### Identity

Each event identifies the real-world resource with `{region_id}`. `{region_id}` is unique numeric identifier for the forecast area. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `dwd-pollenflug`, key `{region_id}` |
| `MQTT/5.0` | topic `air-quality/de/dwd/dwd-pollenflug/{region_id}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/dwd-pollenflug`, message subject `{region_id}` |

#### Payload

`Region` payloads are JSON object. Required fields: `region_id`, `region_name`.

- **`region_id`** (string, required): Unique numeric identifier for the forecast area. For regions without sub-regions this is the main region_id (e.g. 20 for Mecklenburg-Vorpommern). For sub-regions it is the partregion_id (e.g. 11 for 'Inseln und Marschen' within Schleswig-Holstein). Derived from the DWD JSON fields region_id and partregion_id.
- **`region_name`** (string, required): Name of the main geographic region as published by DWD (e.g. 'Schleswig-Holstein und Hamburg', 'Bayern'). Sourced from the 'region_name' field in the DWD API response.
- **`partregion_id`** (int32 or null, optional): Numeric identifier of the sub-region within the parent region. Set to -1 by DWD when the region has no sub-divisions; the bridge emits null in that case. Sourced from the 'partregion_id' field in the DWD API response.
- **`partregion_name`** (string or null, optional): Name of the sub-region (e.g. 'Inseln und Marschen', 'Geest,Schleswig-Holstein und Hamburg'). Empty string in the DWD response when the region has no sub-divisions; the bridge emits null in that case. Sourced from the 'partregion_name' field in the DWD API response.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "region_id": "string",
  "region_name": "string",
  "partregion_id": 0,
  "partregion_name": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Pollen Forecast

CloudEvents type: `DE.DWD.Pollenflug.PollenForecast`

#### What it tells you

A forecast from Germany's Deutscher Wetterdienst (DWD) for one area or station. It carries pollen exposure forecasts by region and plant type for the period published by the upstream source.

#### Identity

Each event identifies the real-world resource with `{region_id}`. `{region_id}` is unique numeric identifier for the forecast area. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `dwd-pollenflug`, key `{region_id}` |
| `MQTT/5.0` | topic `air-quality/de/dwd/dwd-pollenflug/{region_id}/{pollen_type}/pollen-forecast`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/dwd-pollenflug`, message subject `{region_id}/{pollen_type}` |

#### Payload

`Pollen Forecast` payloads are JSON object. Required fields: `region_id`, `region_name`, `last_update`, `next_update`.

- **`region_id`** (string, required): Unique numeric identifier for the forecast area. Same identity model as Region: uses partregion_id when the area is a sub-region, otherwise uses the main region_id.
- **`region_name`** (string, required): Display name of the forecast area. Uses partregion_name when available, otherwise region_name.
- **`last_update`** (string, required): Timestamp of the last forecast update as published by DWD, e.g. '2025-04-08 11:00 Uhr'. Retained as a string because the upstream format includes the German suffix 'Uhr'.
- **`next_update`** (string, required): Timestamp of the next expected forecast update as published by DWD, e.g. '2025-04-09 11:00 Uhr'.
- **`sender`** (string or null, optional): Issuing organization as stated in the DWD API response, typically 'Deutscher Wetterdienst - Medizin-Meteorologie'.
- **`hazel_today`** (string or null, optional): Pollen intensity for Hasel (hazel) today. Values: '0' (none), '0-1' (none to low), '1' (low), '1-2' (low to medium), '2' (medium), '2-3' (medium to high), '3' (high).
- **`hazel_tomorrow`** (string or null, optional): Pollen intensity for Hasel (hazel) tomorrow.
- **`hazel_dayafter_to`** (string or null, optional): Pollen intensity for Hasel (hazel) the day after tomorrow.
- **`alder_today`** (string or null, optional): Pollen intensity for Erle (alder) today.
- **`alder_tomorrow`** (string or null, optional): Pollen intensity for Erle (alder) tomorrow.
- **`alder_dayafter_to`** (string or null, optional): Pollen intensity for Erle (alder) the day after tomorrow.
- **`birch_today`** (string or null, optional): Pollen intensity for Birke (birch) today.
- **`birch_tomorrow`** (string or null, optional): Pollen intensity for Birke (birch) tomorrow.
- **`birch_dayafter_to`** (string or null, optional): Pollen intensity for Birke (birch) the day after tomorrow.
- **`ash_today`** (string or null, optional): Pollen intensity for Esche (ash) today.
- **`ash_tomorrow`** (string or null, optional): Pollen intensity for Esche (ash) tomorrow.
- **`ash_dayafter_to`** (string or null, optional): Pollen intensity for Esche (ash) the day after tomorrow.
- **`grasses_today`** (string or null, optional): Pollen intensity for Gräser (grasses) today. In the upstream API this field is named 'Graeser'.
- **`grasses_tomorrow`** (string or null, optional): Pollen intensity for Gräser (grasses) tomorrow.
- **`grasses_dayafter_to`** (string or null, optional): Pollen intensity for Gräser (grasses) the day after tomorrow.
- **`rye_today`** (string or null, optional): Pollen intensity for Roggen (rye) today.
- **`rye_tomorrow`** (string or null, optional): Pollen intensity for Roggen (rye) tomorrow.
- **`rye_dayafter_to`** (string or null, optional): Pollen intensity for Roggen (rye) the day after tomorrow.
- **`mugwort_today`** (string or null, optional): Pollen intensity for Beifuß (mugwort) today. In the upstream API this field is named 'Beifuss'.
- **`mugwort_tomorrow`** (string or null, optional): Pollen intensity for Beifuß (mugwort) tomorrow.
- **`mugwort_dayafter_to`** (string or null, optional): Pollen intensity for Beifuß (mugwort) the day after tomorrow.
- **`ragweed_today`** (string or null, optional): Pollen intensity for Ambrosia (ragweed) today.
- **`ragweed_tomorrow`** (string or null, optional): Pollen intensity for Ambrosia (ragweed) tomorrow.
- **`ragweed_dayafter_to`** (string or null, optional): Pollen intensity for Ambrosia (ragweed) the day after tomorrow.
- **`pollen_type`** (null or string, optional): Normalized routing field 'pollen_type' added for MQTT/AMQP subscriber filtering.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "region_id": "string",
  "region_name": "string",
  "last_update": "string",
  "next_update": "string",
  "sender": "string",
  "hazel_today": "string",
  "hazel_tomorrow": "string",
  "hazel_dayafter_to": "string",
  "alder_today": "string",
  "alder_tomorrow": "string",
  "alder_dayafter_to": "string",
  "birch_today": "string",
  "birch_tomorrow": "string",
  "birch_dayafter_to": "string",
  "ash_today": "string",
  "ash_tomorrow": "string",
  "ash_dayafter_to": "string",
  "grasses_today": "string",
  "grasses_tomorrow": "string",
  "grasses_dayafter_to": "string",
  "rye_today": "string",
  "rye_tomorrow": "string",
  "rye_dayafter_to": "string",
  "mugwort_today": "string",
  "mugwort_tomorrow": "string",
  "mugwort_dayafter_to": "string",
  "ragweed_today": "string",
  "ragweed_tomorrow": "string",
  "ragweed_dayafter_to": "string",
  "pollen_type": "string"
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

## References

- xRegistry manifest: [`xreg/dwd_pollenflug.xreg.json`](xreg/dwd_pollenflug.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- Azure Service Bus Standard namespace: <https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview>
