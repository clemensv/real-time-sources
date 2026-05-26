# UK Environment Agency Flood Monitoring API Bridge Events

UK Environment Agency Flood Monitoring publishes water level and flow observations from the Environment Agency flood-monitoring API for monitoring stations across England. These events let consumers build real-time monitoring, alerting, and operational dashboards without polling the upstream API directly.

## At a glance

- **Event types:** 2 documented event types (6 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 1 reference/catalog event type and 1 telemetry event type.
- **Identity:** `{station_reference}` identifies the resource each event is about.
- **Operations:** Reference/catalog events are documented as startup emissions, with periodic refresh when the source supports it.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `uk-ea-flood-monitoring`. The record key is `{station_reference}`. In plain language, `{station_reference}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['uk-ea-flood-monitoring'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `hydro/gb/ea/uk-ea-flood-monitoring/+/+/info`, `hydro/gb/ea/uk-ea-flood-monitoring/+/+/reading`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('hydro/gb/ea/uk-ea-flood-monitoring/+/+/info', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `uk-ea-flood-monitoring`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/uk-ea-flood-monitoring')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Station

CloudEvents type: `UK.Gov.Environment.EA.FloodMonitoring.Station`

#### What it tells you

A reference record for one monitoring stations across England published by the Environment Agency flood-monitoring API. It fires when the bridge publishes or refreshes the station catalog so consumers can interpret measurement events. Reference details for one monitoring station or site in the UK Environment Agency Flood Monitoring source.

#### Identity

Each event identifies the real-world resource with `{station_reference}`. `{station_reference}` is provider-supplied station reference value for this record. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `uk-ea-flood-monitoring`, key `{station_reference}` |
| `MQTT/5.0` | topic `hydro/gb/ea/uk-ea-flood-monitoring/{river}/{station_reference}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/uk-ea-flood-monitoring`, message subject `{station_reference}`; application properties river `{river}` |

#### Payload

`Station` payloads are JSON object. Required fields: `station_reference`, `label`, `lat`, `long`, `notation`.

- **`station_reference`** (string, required): Provider-supplied station reference value for this record.
- **`label`** (string, required): Provider-supplied label value for this record.
- **`river_name`** (string or null, optional): Name of the river or watercourse observed at the station.
- **`catchment_name`** (string or null, optional): Human-readable name of the catchment.
- **`town`** (string or null, optional): Provider-supplied town value for this record.
- **`lat`** (double, required): Provider-supplied lat value for this record.
- **`long`** (double, required): Provider-supplied long value for this record.
- **`notation`** (string, required): Provider-supplied notation value for this record.
- **`status`** (string or null, optional): Provider status value for the station, measurement, or alert.
- **`date_opened`** (string or null, optional): Provider-supplied date opened value for this record.
- **`river`** (string, optional): Stable routing axis used by MQTT and AMQP transport templates for uk-ea-flood-monitoring.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_reference": "string",
  "label": "string",
  "river_name": "string",
  "catchment_name": "string",
  "town": "string",
  "lat": 0,
  "long": 0,
  "notation": "string",
  "status": "string",
  "date_opened": "string",
  "river": "string"
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Reading

CloudEvents type: `UK.Gov.Environment.EA.FloodMonitoring.Reading`

#### What it tells you

A reading event from the Environment Agency flood-monitoring API. It represents source data for monitoring stations across England as published by the upstream feed. Payload record for reading events in the UK Environment Agency Flood Monitoring source.

#### Identity

Each event identifies the real-world resource with `{station_reference}`. `{station_reference}` is provider-supplied station reference value for this record. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `uk-ea-flood-monitoring`, key `{station_reference}` |
| `MQTT/5.0` | topic `hydro/gb/ea/uk-ea-flood-monitoring/{river}/{station_reference}/reading`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/uk-ea-flood-monitoring`, message subject `{station_reference}`; application properties river `{river}` |

#### Payload

`Reading` payloads are JSON object. Required fields: `station_reference`, `date_time`, `measure`, `value`.

- **`station_reference`** (string, required): Provider-supplied station reference value for this record.
- **`date_time`** (datetime, required): Time associated with the date time value.
- **`measure`** (string, required): Provider-supplied measure value for this record.
- **`value`** (double, required): Measured value reported by the upstream provider.
- **`river`** (string, optional): Stable routing axis used by MQTT and AMQP transport templates for uk-ea-flood-monitoring.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_reference": "string",
  "date_time": "2024-01-01T00:00:00Z",
  "measure": "string",
  "value": 0,
  "river": "string"
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

- Reference/catalog events are documented as startup emissions, with periodic refresh when the source supports it.

## References

- xRegistry manifest: [`xreg/uk_ea_flood_monitoring.xreg.json`](xreg/uk_ea_flood_monitoring.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- UK Environment Agency Flood Monitoring
API: <https://environment.data.gov.uk/flood-monitoring/doc/reference>
