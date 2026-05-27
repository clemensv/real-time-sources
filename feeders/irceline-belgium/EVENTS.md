# IRCELINE Belgium feeder Events

IRCELINE Belgium Air Quality publishes pollutant concentration and air-quality measurements from Belgium's IRCELINE interregional environment agency for Belgian air-quality monitoring stations. These events help consumers build monitoring, alerting, analytics, and dashboards without polling the upstream API directly.

## At a glance

- **Event types:** 3 documented event types (9 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 3 telemetry event types.
- **Identity:** `{station_id}`, `{timeseries_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `irceline-belgium`. The record key is `{station_id}`, `{timeseries_id}`. Each key template is explained in the event catalog below. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['irceline-belgium'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `air-quality/be/irceline/irceline-belgium/+/+/info`, `air-quality/be/irceline/irceline-belgium/+/+/+/timeseries`, `air-quality/be/irceline/irceline-belgium/+/+/+/observation`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('air-quality/be/irceline/irceline-belgium/+/+/info', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `irceline-belgium`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/irceline-belgium')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Station

CloudEvents type: `be.irceline.Station`

#### What it tells you

A reference record published by Belgium's IRCELINE interregional environment agency. It lets consumers label, group, and route the live measurement or forecast events.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is stable numeric station identifier from station.properties.id in the IRCELINE stations GeoJSON feed. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `irceline-belgium`, key `{station_id}` |
| `MQTT/5.0` | topic `air-quality/be/irceline/irceline-belgium/{region}/{station_id}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/irceline-belgium`, message subject `{station_id}`; application properties region `{region}`, pollutant `{pollutant}` |

#### Payload

`Station` payloads are JSON object. Required fields: `station_id`, `label`, `latitude`, `longitude`.

- **`station_id`** (string, required): Stable numeric station identifier from station.properties.id in the IRCELINE stations GeoJSON feed. The bridge converts the upstream integer identifier to a string because this value is also used as the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]+$`.
- **`label`** (string, required): Human-readable station label from station.properties.label, typically formatted as '{station code} - {municipality}' such as '40AL02 - Beveren'. This is the display name published by IRCELINE for the monitoring site.
- **`latitude`** (double, required, deg (°)): Station latitude in decimal degrees north, derived from the second element of station.geometry.coordinates in the upstream GeoJSON Point geometry. The upstream array follows GeoJSON order [longitude, latitude, elevation].
- **`longitude`** (double, required, deg (°)): Station longitude in decimal degrees east, derived from the first element of station.geometry.coordinates in the upstream GeoJSON Point geometry. The third element is the literal string 'NaN' in live payloads and is ignored.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "label": "string",
  "latitude": 0,
  "longitude": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Timeseries

CloudEvents type: `be.irceline.Timeseries`

#### What it tells you

A current environmental measurement from Belgium's IRCELINE interregional environment agency. It carries pollutant concentration and air-quality measurements when the upstream feed reports a new or refreshed value.

#### Identity

Each event identifies the real-world resource with `{timeseries_id}`. `{timeseries_id}` is stable numeric identifier of the IRCELINE timeseries from the root id property on GET /timeseries results. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `irceline-belgium`, key `{timeseries_id}` |
| `MQTT/5.0` | topic `air-quality/be/irceline/irceline-belgium/{region}/{station_id}/{pollutant}/timeseries`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/irceline-belgium`, message subject `{timeseries_id}`; application properties region `{region}`, station_id `{station_id}`, pollutant `{pollutant}` |

#### Payload

`Timeseries` payloads are JSON object. Required fields: `timeseries_id`, `label`, `uom`, `station_id`, `station_label`.

- **`timeseries_id`** (string, required): Stable numeric identifier of the IRCELINE timeseries from the root id property on GET /timeseries results. The bridge converts the upstream value to a string because this identifier is the Kafka key and CloudEvents subject for both reference and observation events. Constraints: pattern `^[0-9]+$`.
- **`label`** (string, required): Descriptive timeseries label from the upstream label property, combining phenomenon name, timeseries identifier, procedure label, and station label. Example: 'Particulate Matter < 10 µm 6152 - DAILY CORRECTION TEOM - procedure, 40AL01 - Linkeroever'.
- **`uom`** (string, required): Published unit of measurement from the upstream uom property, such as 'µg/m³'. IRCELINE returns this literal display unit on both collection and expanded timeseries responses.
- **`station_id`** (string, required): Numeric station identifier linked to the timeseries, mapped from station.properties.id on the embedded station feature. This is the stable identifier of the monitoring site that hosts the timeseries. Constraints: pattern `^[0-9]+$`.
- **`station_label`** (string, required): Human-readable station label linked to the timeseries, mapped from station.properties.label on the embedded station feature.
- **`latitude`** (double or null, optional, deg (°)): Station latitude in decimal degrees north, derived from station.geometry.coordinates[1] when the embedded station feature includes a GeoJSON Point geometry.
- **`longitude`** (double or null, optional, deg (°)): Station longitude in decimal degrees east, derived from station.geometry.coordinates[0] when the embedded station feature includes a GeoJSON Point geometry.
- **`phenomenon_id`** (string or null, optional): Identifier of the measured phenomenon from parameters.phenomenon.id on expanded timeseries metadata, for example '5' for particulate matter under 10 micrometers.
- **`phenomenon_label`** (string or null, optional): Human-readable phenomenon label from parameters.phenomenon.label on expanded timeseries metadata, for example 'Nitrogen dioxide' or 'Ozone'.
- **`category_id`** (string or null, optional): Identifier of the IRCELINE category linked to the timeseries from parameters.category.id. In the live API this currently mirrors the phenomenon identifier for air-quality pollutants.
- **`category_label`** (string or null, optional): Human-readable IRCELINE category label from parameters.category.label. In the live API this currently mirrors the phenomenon label for air-quality pollutants.
- **`status_intervals`** (array of object, optional): Optional ordered array of status interval bands from the upstream statusIntervals expansion. Each entry describes a lower and upper threshold, a display label, and a color used by IRCELINE for BelAQI-style interpretation of the timeseries values.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "timeseries_id": "string",
  "label": "string",
  "uom": "string",
  "station_id": "string",
  "station_label": "string",
  "latitude": 0,
  "longitude": 0,
  "phenomenon_id": "string",
  "phenomenon_label": "string",
  "category_id": "string",
  "category_label": "string",
  "status_intervals": [
    {
      "lower": "string",
      "upper": "string",
      "name": "string",
      "color": "string"
    }
  ]
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Observation

CloudEvents type: `be.irceline.Observation`

#### What it tells you

A current environmental measurement from Belgium's IRCELINE interregional environment agency. It carries pollutant concentration and air-quality measurements when the upstream feed reports a new or refreshed value.

#### Identity

Each event identifies the real-world resource with `{timeseries_id}`. `{timeseries_id}` is stable numeric timeseries identifier of the measurement source. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `irceline-belgium`, key `{timeseries_id}` |
| `MQTT/5.0` | topic `air-quality/be/irceline/irceline-belgium/{region}/{station_id}/{pollutant}/observation`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/irceline-belgium`, message subject `{timeseries_id}`; application properties region `{region}`, station_id `{station_id}`, pollutant `{pollutant}` |

#### Payload

`Observation` payloads are JSON object. Required fields: `timeseries_id`, `timestamp`, `uom`.

- **`timeseries_id`** (string, required): Stable numeric timeseries identifier of the measurement source. This is copied from the parent timeseries metadata and matches the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]+$`.
- **`timestamp`** (string, required): Observation timestamp in ISO 8601 UTC form produced by converting the upstream Unix millisecond timestamp from values[].timestamp, for example '2025-04-08T09:00:00Z'. Constraints: pattern `^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]{3})?Z$`.
- **`value`** (double or null, optional): Measured numeric value from values[].value. IRCELINE can publish null when a data point exists without a numeric value, so the schema explicitly allows null.
- **`uom`** (string, required): Unit of measurement carried over from the parent timeseries uom field, such as 'µg/m³'. This keeps each observation self-describing without requiring a separate metadata lookup.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "timeseries_id": "string",
  "timestamp": "string",
  "value": 0,
  "uom": "string"
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

- xRegistry manifest: [`xreg/irceline_belgium.xreg.json`](xreg/irceline_belgium.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
