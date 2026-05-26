# Ireland OPW Water Level feeder Events

Ireland OPW waterlevel.ie publishes water level, temperature, and sensor voltage observations from Ireland's Office of Public Works (OPW) for Irish hydrometric stations. These events let consumers build real-time monitoring, alerting, and operational dashboards without polling the upstream API directly.

## At a glance

- **Event types:** 2 documented event types (6 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 1 reference/catalog event type and 1 telemetry event type.
- **Identity:** `{station_ref}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `ireland-opw-waterlevel`. The record key is `{station_ref}`. In plain language, `{station_ref}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['ireland-opw-waterlevel'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `hydro/ie/opw/ireland-opw-waterlevel/+/+/info`, `hydro/ie/opw/ireland-opw-waterlevel/+/+/water-level`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('hydro/ie/opw/ireland-opw-waterlevel/+/+/info', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `ireland-opw-waterlevel`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/ireland-opw-waterlevel')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Station

CloudEvents type: `ie.gov.opw.waterlevel.Station`

#### What it tells you

A reference record for one Irish hydrometric station published by Ireland's Office of Public Works (OPW). It fires when the bridge publishes or refreshes the station catalog so consumers can interpret measurement events. Reference data for an OPW hydrometric station in Ireland, including location and region.

#### Identity

Each event identifies the real-world resource with `{station_ref}`. `{station_ref}` is zero-padded 10-digit station reference code uniquely identifying the hydrometric station (e.g. '0000001041'). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `ireland-opw-waterlevel`, key `{station_ref}` |
| `MQTT/5.0` | topic `hydro/ie/opw/ireland-opw-waterlevel/{basin}/{station_ref}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/ireland-opw-waterlevel`, message subject `{station_ref}`; application properties basin `{basin}` |

#### Payload

`Station` payloads are JSON object. Required fields: `station_ref`, `station_name`, `region_id`, `longitude`, `latitude`.

- **`station_ref`** (string, required): Zero-padded 10-digit station reference code uniquely identifying the hydrometric station (e.g. '0000001041').
- **`station_name`** (string, required): Human-readable name of the hydrometric station (e.g. 'Sandy Mills').
- **`region_id`** (int32, required): Integer identifier of the OPW hydrometric region the station belongs to.
- **`longitude`** (double, required): Longitude of the station location in WGS84 decimal degrees.
- **`latitude`** (double, required): Latitude of the station location in WGS84 decimal degrees.
- **`basin`** (string, optional): Stable routing axis used by MQTT and AMQP transport templates for ireland-opw-waterlevel.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_ref": "string",
  "station_name": "string",
  "region_id": 0,
  "longitude": 0,
  "latitude": 0,
  "basin": "string"
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Water Level Reading

CloudEvents type: `ie.gov.opw.waterlevel.WaterLevelReading`

#### What it tells you

A current measurement from Ireland's Office of Public Works (OPW) for one monitoring site. It carries water level, temperature, and sensor voltage observations when the upstream feed reports a new or refreshed value. A sensor reading from an OPW hydrometric station, covering water level, temperature, voltage, or Ordnance Datum.

#### Identity

Each event identifies the real-world resource with `{station_ref}`. `{station_ref}` is zero-padded 10-digit station reference code uniquely identifying the hydrometric station (e.g. '0000001041'). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `ireland-opw-waterlevel`, key `{station_ref}` |
| `MQTT/5.0` | topic `hydro/ie/opw/ireland-opw-waterlevel/{basin}/{station_ref}/water-level`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/ireland-opw-waterlevel`, message subject `{station_ref}`; application properties basin `{basin}` |

#### Payload

`Water Level Reading` payloads are JSON object. Required fields: `station_ref`, `station_name`, `sensor_ref`, `value`, `datetime`, `err_code`.

- **`station_ref`** (string, required): Zero-padded 10-digit station reference code uniquely identifying the hydrometric station (e.g. '0000001041').
- **`station_name`** (string, required): Human-readable name of the hydrometric station (e.g. 'Sandy Mills').
- **`sensor_ref`** (string, required): Sensor reference code identifying the measurement type: '0001' for water level (metres), '0002' for temperature (degrees Celsius), '0003' for voltage (volts), 'OD' for Ordnance Datum level (metres).
- **`value`** (double or null, required): Numeric sensor reading value. Units depend on sensor_ref: metres for water level ('0001') and OD ('OD'), degrees Celsius for temperature ('0002'), volts for voltage ('0003'). Null if the value could not be parsed from the upstream string representation.
- **`datetime`** (string, required): ISO 8601 timestamp of the sensor reading as provided by the upstream API (e.g. '2024-01-15T12:00:00Z').
- **`err_code`** (int32, required): Upstream error code for the reading. A value of 99 indicates the reading is valid (OK). Other values indicate various error conditions.
- **`basin`** (string, optional): Stable routing axis used by MQTT and AMQP transport templates for ireland-opw-waterlevel.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_ref": "string",
  "station_name": "string",
  "sensor_ref": "string",
  "value": 0,
  "datetime": "string",
  "err_code": 0,
  "basin": "string"
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

- xRegistry manifest: [`xreg/ireland_opw_waterlevel.xreg.json`](xreg/ireland_opw_waterlevel.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
