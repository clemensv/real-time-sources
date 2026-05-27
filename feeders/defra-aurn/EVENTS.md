# Defra AURN feeder Events

DEFRA AURN publishes pollutant concentration measurements from the UK Department for Environment, Food and Rural Affairs Automatic Urban and Rural Network for UK air-quality monitoring stations. These events help consumers build monitoring, alerting, analytics, and dashboards without polling the upstream API directly.

## At a glance

- **Event types:** 3 documented event types (9 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 1 reference/catalog event type and 2 telemetry event types.
- **Identity:** `{station_id}`, `{timeseries_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `defra-aurn`. The record key is `{station_id}`, `{timeseries_id}`. Each key template is explained in the event catalog below. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['defra-aurn'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `air-quality/gb/defra/defra-aurn/+/+/info`, `air-quality/gb/defra/defra-aurn/+/+/+/timeseries`, `air-quality/gb/defra/defra-aurn/+/+/+/observation`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('air-quality/gb/defra/defra-aurn/+/+/info', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `defra-aurn`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/defra-aurn')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Station

CloudEvents type: `uk.gov.defra.aurn.Station`

#### What it tells you

Reference metadata for a Defra AURN monitoring station entry as published by the 52°North SOS Timeseries API stations collection.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is stable numeric monitoring station identifier from the GeoJSON feature properties.id field returned by GET /stations. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `defra-aurn`, key `{station_id}` |
| `MQTT/5.0` | topic `air-quality/gb/defra/defra-aurn/{region}/{station_id}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/defra-aurn`, message subject `{station_id}`; application properties region `{region}`, pollutant `{pollutant}` |

#### Payload

`Station` payloads are JSON object. Required fields: `station_id`, `label`, `latitude`, `longitude`.

- **`station_id`** (string, required): Stable numeric monitoring station identifier from the GeoJSON feature properties.id field returned by GET /stations. The bridge converts the numeric API value to a string so it can be used consistently as the Kafka key and CloudEvents subject. Constraints: pattern `^[0-9]+$`.
- **`label`** (string, required): Upstream station label from properties.label in GET /stations. In this API the label includes both the site name and the monitored pollutant description, for example 'Camden Kerbside-Particulate matter less than 10 micro m (aerosol)'.
- **`latitude`** (double, required, degree (°)): WGS84 latitude in decimal degrees taken from geometry.coordinates[0] in the Defra SOS GeoJSON feature. The upstream API uses latitude-first coordinate ordering rather than GeoJSON's usual longitude-first convention. Constraints: minimum `-90`, maximum `90`.
- **`longitude`** (double, required, degree (°)): WGS84 longitude in decimal degrees taken from geometry.coordinates[1] in the Defra SOS GeoJSON feature. The bridge ignores the third coordinate array member because the upstream API returns a string 'NaN' elevation value there. Constraints: minimum `-180`, maximum `180`.
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

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Timeseries

CloudEvents type: `uk.gov.defra.aurn.Timeseries`

#### What it tells you

Reference metadata for a Defra AURN station and pollutant timeseries combination, including linked station coordinates and pollutant taxonomy identifiers.

#### Identity

Each event identifies the real-world resource with `{timeseries_id}`. `{timeseries_id}` is stable numeric timeseries identifier from the id field returned by GET /timeseries and GET /timeseries/{id}?expanded=true. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `defra-aurn`, key `{timeseries_id}` |
| `MQTT/5.0` | topic `air-quality/gb/defra/defra-aurn/{region}/{station_id}/{pollutant}/timeseries`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/defra-aurn`, message subject `{timeseries_id}`; application properties region `{region}`, station_id `{station_id}`, pollutant `{pollutant}` |

#### Payload

`Timeseries` payloads are JSON object. Required fields: `timeseries_id`, `label`, `uom`, `station_id`, `station_label`.

- **`timeseries_id`** (string, required): Stable numeric timeseries identifier from the id field returned by GET /timeseries and GET /timeseries/{id}?expanded=true. Each timeseries represents one station and one pollutant combination. Constraints: pattern `^[0-9]+$`.
- **`label`** (string, required): Descriptive label from the timeseries label field. In the live API this string combines the EIONet pollutant URI, the station identifier, and the station display label.
- **`uom`** (string, required): Unit of measurement string from the timeseries uom field, for example 'ug.m-3'. The bridge republishes the upstream unit token unchanged so consumers can interpret observation values correctly.
- **`station_id`** (string, required): Stable station identifier from station.properties.id inside the expanded timeseries response. This is the identifier of the monitoring site associated with the timeseries. Constraints: pattern `^[0-9]+$`.
- **`station_label`** (string, required): Station display label from station.properties.label inside the expanded timeseries response. In this API the label already includes the pollutant name, so it is unique per station and pollutant combination.
- **`latitude`** (double or null, optional, degree (°)): WGS84 latitude in decimal degrees derived from station.geometry.coordinates[0] in the expanded timeseries response. The field is nullable because the bridge will emit null if the upstream omits coordinates. Constraints: minimum `-90`, maximum `90`.
- **`longitude`** (double or null, optional, degree (°)): WGS84 longitude in decimal degrees derived from station.geometry.coordinates[1] in the expanded timeseries response. The field is nullable because the bridge will emit null if the upstream omits coordinates. Constraints: minimum `-180`, maximum `180`.
- **`phenomenon_id`** (string or null, optional): Pollutant phenomenon identifier from parameters.phenomenon.id in the expanded timeseries response. The API models pollutants through EIONet vocabulary identifiers and numeric ids. Constraints: pattern `^[0-9]+$`.
- **`phenomenon_label`** (string or null, optional): Pollutant label from parameters.phenomenon.label in the expanded timeseries response. In the live API this is typically an EIONet pollutant URI such as 'http://dd.eionet.europa.eu/vocabulary/aq/pollutant/5'.
- **`category_id`** (string or null, optional): Category identifier from parameters.category.id in the expanded timeseries response. In this API the category collection currently mirrors the phenomenon collection, but it is still carried through explicitly because it is part of the published timeseries metadata. Constraints: pattern `^[0-9]+$`.
- **`category_label`** (string or null, optional): Category label from parameters.category.label in the expanded timeseries response. In the live API this is the same EIONet URI string as the phenomenon label for the same pollutant.
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
  "category_label": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Observation

CloudEvents type: `uk.gov.defra.aurn.Observation`

#### What it tells you

Hourly or near-hourly Defra AURN observation value for a single timeseries, emitted from the getData endpoint for the most recent two-hour polling window.

#### Identity

Each event identifies the real-world resource with `{timeseries_id}`. `{timeseries_id}` is stable numeric timeseries identifier for the series that produced this observation. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `defra-aurn`, key `{timeseries_id}` |
| `MQTT/5.0` | topic `air-quality/gb/defra/defra-aurn/{region}/{station_id}/{pollutant}/observation`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/defra-aurn`, message subject `{timeseries_id}`; application properties region `{region}`, station_id `{station_id}`, pollutant `{pollutant}` |

#### Payload

`Observation` payloads are JSON object. Required fields: `timeseries_id`, `timestamp`, `value`, `uom`.

- **`timeseries_id`** (string, required): Stable numeric timeseries identifier for the series that produced this observation. This field is the Kafka key and CloudEvents subject for both the reference timeseries event and the observation event. Constraints: pattern `^[0-9]+$`.
- **`timestamp`** (datetime, required): Observation timestamp encoded as an ISO 8601 UTC string. The bridge converts the upstream GET /timeseries/{id}/getData values[].timestamp Unix millisecond value with datetime.fromtimestamp(timestamp/1000, tz=timezone.utc).isoformat().
- **`value`** (double or null, required): Measured pollutant concentration or other reported numeric reading from values[].value in GET /timeseries/{id}/getData. The field is nullable because the API can represent missing or flagged values with null.
- **`uom`** (string, required): Unit of measurement for the observation, copied from the parent timeseries uom field so each telemetry event remains self-describing.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "timeseries_id": "string",
  "timestamp": "2024-01-01T00:00:00Z",
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

- xRegistry manifest: [`xreg/defra_aurn.xreg.json`](xreg/defra_aurn.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
