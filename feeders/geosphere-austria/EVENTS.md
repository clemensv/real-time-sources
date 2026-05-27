# GeoSphere Austria feeder Events

GeoSphere Austria Weather publishes weather observations from GeoSphere Austria for Austrian weather stations. These events help consumers build monitoring, alerting, analytics, and dashboards without polling the upstream API directly.

## At a glance

- **Event types:** 2 documented event types (6 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 1 reference/catalog event type and 1 telemetry event type.
- **Identity:** `{station_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `geosphere-austria-tawes`. The record key is `{station_id}`. In plain language, `{station_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['geosphere-austria-tawes'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `weather/at/geosphere/geosphere-austria/+/+/info`, `weather/at/geosphere/geosphere-austria/+/+/observation`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('weather/at/geosphere/geosphere-austria/+/+/info', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `geosphere-austria`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/geosphere-austria')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Weather Station

CloudEvents type: `at.geosphere.tawes.WeatherStation`

#### What it tells you

Reference data for a GeoSphere Austria TAWES automatic weather station, including location, elevation, and federal state.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is stable GeoSphere Austria numeric station identifier used as the Kafka key and CloudEvents subject. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `geosphere-austria-tawes`, key `{station_id}` |
| `MQTT/5.0` | topic `weather/at/geosphere/geosphere-austria/{bundesland}/{station_id}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/geosphere-austria`, message subject `{station_id}`; application properties bundesland `{bundesland}` |

#### Payload

`Weather Station` payloads are JSON object. Required fields: `station_id`, `station_name`, `latitude`, `longitude`, `altitude`, `state`.

- **`station_id`** (string, required): Stable GeoSphere Austria numeric station identifier used as the Kafka key and CloudEvents subject. Mapped from the upstream 'id' field in the station metadata. Constraints: pattern `^[0-9]+$`.
- **`station_name`** (string, required): Station name from the GeoSphere metadata, for example 'WIEN HOHE WARTE' or 'INNSBRUCK FLUGHAFEN'. Mapped from the upstream 'name' field.
- **`latitude`** (double, required, degree (°)): WGS84 latitude of the station in decimal degrees, sourced from the GeoSphere metadata 'lat' field.
- **`longitude`** (double, required, degree (°)): WGS84 longitude of the station in decimal degrees, sourced from the GeoSphere metadata 'lon' field.
- **`altitude`** (double, required, meter (m)): Station altitude above sea level in meters, sourced from the GeoSphere metadata 'altitude' field.
- **`state`** (string or null, required): Austrian federal state (Bundesland) where the station is located, for example 'Wien', 'Tirol', 'Steiermark'. Sourced from the GeoSphere metadata 'state' field. Null when the metadata does not include a state.
- **`bundesland`** (string, optional): Normalized routing field 'bundesland' added for MQTT/AMQP subscriber filtering.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "station_name": "string",
  "latitude": 0,
  "longitude": 0,
  "altitude": 0,
  "state": "string",
  "bundesland": "string"
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Weather Observation

CloudEvents type: `at.geosphere.tawes.WeatherObservation`

#### What it tells you

10-minute weather observation from a GeoSphere Austria TAWES station, including temperature, humidity, precipitation, wind, pressure, sunshine duration, and global radiation.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is geoSphere Austria numeric station identifier for the observing station. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `geosphere-austria-tawes`, key `{station_id}` |
| `MQTT/5.0` | topic `weather/at/geosphere/geosphere-austria/{bundesland}/{station_id}/observation`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/geosphere-austria`, message subject `{station_id}`; application properties bundesland `{bundesland}` |

#### Payload

`Weather Observation` payloads are JSON object. Required fields: `station_id`, `observation_time`, `temperature`, `humidity`, `precipitation`, `wind_direction`, `wind_speed`, `pressure`, `sunshine_duration`, `global_radiation`.

- **`station_id`** (string, required): GeoSphere Austria numeric station identifier for the observing station. Mapped from the upstream 'station' property in the GeoJSON features. Constraints: pattern `^[0-9]+$`.
- **`observation_time`** (string, required): Observation timestamp in UTC from the GeoSphere API 'timestamps' array, formatted as an ISO-8601 instant such as '2024-01-15T13:00:00+00:00'.
- **`temperature`** (double or null, required, degree Celsius (°C)): Air temperature (Lufttemperatur) in degrees Celsius over the 10-minute interval, from the GeoSphere TL parameter. Null when the station does not report this parameter.
- **`humidity`** (double or null, required, percent (%)): Relative humidity (Relative Feuchte) as a percentage over the 10-minute interval, from the GeoSphere RF parameter. Null when not reported.
- **`precipitation`** (double or null, required, millimeter (mm)): Precipitation (Niederschlag) in millimeters accumulated during the 10-minute interval, from the GeoSphere RR parameter. Null when not reported.
- **`wind_direction`** (double or null, required, degree (°)): Wind direction (Windrichtung) in degrees over the 10-minute interval, from the GeoSphere DD parameter. 0 indicates north, 90 east, 180 south, 270 west. Null when not reported.
- **`wind_speed`** (double or null, required, meter per second (m/s)): Wind speed (Windgeschwindigkeit) in meters per second over the 10-minute interval, from the GeoSphere FF parameter. Null when not reported.
- **`pressure`** (double or null, required, hectopascal (hPa)): Atmospheric pressure (Luftdruck) in hectopascals at station level over the 10-minute interval, from the GeoSphere P parameter. Null when not reported.
- **`sunshine_duration`** (double or null, required, second (s)): Sunshine duration (Sonnenscheindauer) in seconds during the 10-minute interval, from the GeoSphere SO parameter. Null when the station does not have a sunshine sensor (has_sunshine=false) or the value is missing.
- **`global_radiation`** (double or null, required, watt per square meter (W/m²)): Global radiation (Globalstrahlung) in watts per square meter during the 10-minute interval, from the GeoSphere GLOW parameter. Null when the station does not have a radiation sensor (has_global_radiation=false) or the value is missing.
- **`bundesland`** (string, optional): Normalized routing field 'bundesland' added for MQTT/AMQP subscriber filtering.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "observation_time": "string",
  "temperature": 0,
  "humidity": 0,
  "precipitation": 0,
  "wind_direction": 0,
  "wind_speed": 0,
  "pressure": 0,
  "sunshine_duration": 0,
  "global_radiation": 0,
  "bundesland": "string"
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

- xRegistry manifest: [`xreg/geosphere-austria.xreg.json`](xreg/geosphere-austria.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
