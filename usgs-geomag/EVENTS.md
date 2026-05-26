# USGS Geomag feeder Events

MQTT/5.0 transport variants for USGS geomagnetic observatory reference data and one-minute readings. Topics are retained QoS-1 leaves under space-weather/us/usgs/usgs-geomag/{iaga_code}/..., where {iaga_code} in the topic is the lowercased IAGA observatory code; the payload field may carry the canonical upstream code. Producers MUST lowercase {iaga_code} for the topic and consumers MUST treat topic filters as case-sensitive. The info leaf is retained reference metadata with no expiry. The reading leaf is a latched current 1-minute observation with Message Expiry Interval 7200 seconds; if the retained value expires, interpret the empty topic as observatory or bridge silence for at least two hours, not a zero magnetic-field reading. The iaga_code is the join key between retained info and readings.

## At a glance

- **Event types:** 2 documented event types (6 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 2 telemetry event types.
- **Identity:** `{iaga_code}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `usgs-geomag`. The record key is `{iaga_code}`. In plain language, `{iaga_code}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['usgs-geomag'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `space-weather/us/usgs/usgs-geomag/+/info`, `space-weather/us/usgs/usgs-geomag/+/reading`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('space-weather/us/usgs/usgs-geomag/+/info', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `usgs-geomag`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/usgs-geomag')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Observatory

CloudEvents type: `gov.usgs.geomag.Observatory`

#### What it tells you

Reference data for a USGS Geomagnetism Program observatory, sourced from the INTERMAGNET-compatible observatories GeoJSON endpoint at https://geomag.usgs.gov/ws/observatories/. Each feature represents a ground-based magnetometer station that continuously records geomagnetic field variations.

#### Identity

Each event identifies the real-world resource with `{iaga_code}`. `{iaga_code}` is IAGA (International Association of Geomagnetism and Aeronomy) three- or four-character observatory code, e.g. BOU for Boulder, BRW for Barrow. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-geomag`, key `{iaga_code}` |
| `MQTT/5.0` | topic `space-weather/us/usgs/usgs-geomag/{iaga_code}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/usgs-geomag`, message subject `{iaga_code}` |

#### Payload

`Observatory` payloads are JSON object. Required fields: `iaga_code`, `name`.

- **`iaga_code`** (string, required): IAGA (International Association of Geomagnetism and Aeronomy) three- or four-character observatory code, e.g. BOU for Boulder, BRW for Barrow. This is the primary stable identifier for an observatory.
- **`name`** (string, required): Human-readable name of the observatory, e.g. 'Boulder', 'Barrow', 'College'.
- **`agency`** (string or null, optional): Short identifier of the operating agency, e.g. 'USGS' for United States Geological Survey.
- **`agency_name`** (string or null, optional): Full name of the operating agency, e.g. 'United States Geological Survey (USGS)'.
- **`latitude`** (double or null, optional, deg (°)): Geodetic latitude of the observatory in decimal degrees. Positive values indicate north of the equator.
- **`longitude`** (double or null, optional, deg (°)): Geodetic longitude of the observatory in decimal degrees east. Values above 180 represent west longitudes expressed as 360 minus the west longitude (e.g. 254.763 = -105.237 W).
- **`elevation`** (double or null, optional, m): Elevation of the observatory above mean sea level in meters.
- **`sensor_orientation`** (string or null, optional): Orientation of the magnetometer sensor, e.g. 'HDZ' indicating sensors measure horizontal intensity (H), declination (D), and vertical intensity (Z).
- **`sensor_sampling_rate`** (double or null, optional, Hz): Native sampling rate of the magnetometer sensor in hertz.
- **`declination_base`** (double or null, optional): Declination baseline value in minutes of arc. Used as a reference for variation measurements of the D element.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "iaga_code": "string",
  "name": "string",
  "agency": "string",
  "agency_name": "string",
  "latitude": 0,
  "longitude": 0,
  "elevation": 0,
  "sensor_orientation": "string",
  "sensor_sampling_rate": 0,
  "declination_base": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Magnetic Field Reading

CloudEvents type: `gov.usgs.geomag.MagneticFieldReading`

#### What it tells you

One-minute resolution geomagnetic field variation reading from a USGS Geomagnetism Program observatory, sourced from the timeseries web-service at https://geomag.usgs.gov/ws/data/. The H, D, Z, and F elements correspond to the four standard INTERMAGNET variation data components. The timeseries API returns parallel arrays (times + per-element value arrays) which the bridge transforms into individual timestamped events.

#### Identity

Each event identifies the real-world resource with `{iaga_code}`. `{iaga_code}` is IAGA observatory code identifying the station that produced this reading, e.g. BOU, BRW, FRN. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-geomag`, key `{iaga_code}` |
| `MQTT/5.0` | topic `space-weather/us/usgs/usgs-geomag/{iaga_code}/reading`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/usgs-geomag`, message subject `{iaga_code}` |

#### Payload

`Magnetic Field Reading` payloads are JSON object. Required fields: `iaga_code`, `timestamp`.

- **`iaga_code`** (string, required): IAGA observatory code identifying the station that produced this reading, e.g. BOU, BRW, FRN.
- **`timestamp`** (datetime, required): UTC timestamp of the 1-minute magnetic field sample, in ISO 8601 format. Derived from the 'times' array in the USGS Geomagnetism web-service timeseries response.
- **`h`** (double or null, optional, nT): Horizontal intensity component of the geomagnetic field vector. Represents the magnitude of the horizontal projection of the total field vector. Null when the observatory does not report this element or the value is missing for this minute.
- **`d`** (double or null, optional, ' (′)): Declination angle — the angular difference between magnetic north and geographic north. Positive values indicate east declination. Null when the observatory does not report this element or the value is missing for this minute.
- **`z`** (double or null, optional, nT): Vertical intensity component of the geomagnetic field vector. Positive values indicate downward (into the Earth in the northern hemisphere). Null when the observatory does not report this element or the value is missing for this minute.
- **`f`** (double or null, optional, nT): Total field intensity — the scalar magnitude of the full geomagnetic field vector. Measured by an independent proton or Overhauser magnetometer. Null when the observatory does not report this element or the value is missing for this minute.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "iaga_code": "string",
  "timestamp": "2024-01-01T00:00:00Z",
  "h": 0,
  "d": 0,
  "z": 0,
  "f": 0
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

- xRegistry manifest: [`xreg/usgs_geomag.xreg.json`](xreg/usgs_geomag.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
