# Madrid Real-Time Traffic (Informo) Events

Madrid Traffic publishes traffic intensity and occupancy measurements from Madrid open traffic sensor feeds for Madrid traffic sensors. These events help consumers monitor mobility operations, passenger information, and traffic conditions without polling the upstream source directly.

## At a glance

- **Event types:** 2 documented event types (6 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 2 telemetry event types.
- **Identity:** `{sensor_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `madrid-traffic`. The record key is `{sensor_id}`. In plain language, `{sensor_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['madrid-traffic'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `traffic/es/madrid/madrid-traffic/+/+/info`, `traffic/es/madrid/madrid-traffic/+/+/reading`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('traffic/es/madrid/madrid-traffic/+/+/info', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `broker-configured address`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/events')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Measurement Point

CloudEvents type: `es.madrid.informo.MeasurementPoint`

#### What it tells you

A current transport measurement or status update from Madrid open traffic sensor feeds. It carries traffic intensity and occupancy measurements when the upstream feed reports a new or refreshed value.

#### Identity

Each event identifies the real-world resource with `{sensor_id}`. `{sensor_id}` is unique sensor identifier from the Madrid Informo system. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `madrid-traffic`, key `{sensor_id}` |
| `MQTT/5.0` | topic `traffic/es/madrid/madrid-traffic/{district}/{sensor_id}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `broker-configured node`, message subject `{sensor_id}` |

#### Payload

`Measurement Point` payloads are JSON object. Required fields: `sensor_id`, `description`.

- **`sensor_id`** (string, required): Unique sensor identifier from the Madrid Informo system. Corresponds to the 'idelem' field in the upstream XML. Numeric code assigned by the Madrid traffic management center to each measurement point.
- **`description`** (string, required): Human-readable description of the road segment where this sensor is installed. Typically includes the street name, direction, and bounding cross-streets. Corresponds to 'descripcion' in the upstream XML. Text is in Spanish.
- **`element_type`** (string or null, optional): Classification of the measurement point within Madrid's traffic network. Derived from the 'accesoAsociado' field prefix in the upstream XML. Common values include 'URB' for urban streets and 'M30' for the M-30 ring motorway.
- **`subarea`** (string or null, optional): Traffic management zone code for this sensor. Corresponds to 'subarea' in the upstream XML. Used by Madrid's traffic management center for geographic grouping of sensors.
- **`longitude`** (double or null, optional, deg (°)): Longitude of the sensor in decimal degrees (WGS84, EPSG:4326). Converted from the UTM easting in 'st_x' in the upstream XML, which uses European comma decimal separators.
- **`latitude`** (double or null, optional, deg (°)): Latitude of the sensor in decimal degrees (WGS84, EPSG:4326). Converted from the UTM northing in 'st_y' in the upstream XML, which uses European comma decimal separators.
- **`saturation_intensity`** (integer or null, optional, 1/h (veh/h)): Maximum traffic intensity that the road segment can handle, expressed in vehicles per hour. Corresponds to 'intensidadSat' in the upstream XML. Used as the denominator for computing load and saturation ratios.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "sensor_id": "string",
  "description": "string",
  "element_type": "string",
  "subarea": "string",
  "longitude": 0,
  "latitude": 0,
  "saturation_intensity": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Traffic Reading

CloudEvents type: `es.madrid.informo.TrafficReading`

#### What it tells you

A current transport measurement or status update from Madrid open traffic sensor feeds. It carries traffic intensity and occupancy measurements when the upstream feed reports a new or refreshed value.

#### Identity

Each event identifies the real-world resource with `{sensor_id}`. `{sensor_id}` is unique sensor identifier from the Madrid Informo system. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `madrid-traffic`, key `{sensor_id}` |
| `MQTT/5.0` | topic `traffic/es/madrid/madrid-traffic/{district}/{sensor_id}/reading`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `broker-configured node`, message subject `{sensor_id}` |

#### Payload

`Traffic Reading` payloads are JSON object. Required fields: `sensor_id`, `timestamp`.

- **`sensor_id`** (string, required): Unique sensor identifier from the Madrid Informo system. Corresponds to 'idelem' in the upstream XML. Used as the key for correlating readings with measurement point reference data.
- **`intensity`** (integer or null, optional, 1/h (veh/h)): Current traffic intensity measured by the sensor, expressed in vehicles per hour. Corresponds to 'intensidad' in the upstream XML. A value of 0 may indicate no traffic or a sensor in standby mode.
- **`occupancy`** (integer or null, optional, %): Percentage of time the sensor detects a vehicle presence. Corresponds to 'ocupacion' in the upstream XML. Range is 0 to 100.
- **`load`** (integer or null, optional, %): Load percentage representing the ratio of current intensity to saturation intensity. Corresponds to 'carga' in the upstream XML. Range is typically 0 to 100.
- **`service_level`** (integer or null, optional): Traffic service level reported by the sensor. Corresponds to 'nivelServicio' in the upstream XML. Values: 0 = fluid/free flow, 1 = moderate/dense, 2 = congested, 3 = severely congested.
- **`error_flag`** (string or null, optional): Error status flag for this reading. Corresponds to 'error' in the upstream XML. 'N' indicates a normal reading, 'S' or 'Y' indicates the sensor is reporting an error and the data may be unreliable.
- **`timestamp`** (datetime, required): Timestamp of the traffic reading in UTC. Since the upstream XML does not include per-sensor timestamps, this is derived from the poll time rounded to the nearest 5-minute interval, reflecting the upstream update cadence.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "sensor_id": "string",
  "intensity": 0,
  "occupancy": 0,
  "load": 0,
  "service_level": 0,
  "error_flag": "string",
  "timestamp": "2024-01-01T00:00:00Z"
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

- xRegistry manifest: [`xreg/madrid_traffic.xreg.json`](xreg/madrid_traffic.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
