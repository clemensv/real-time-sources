# UBA AirData feeder Events

UBA Airdata publishes pollutant concentration measurements from the Austrian Umweltbundesamt air-quality data service for Austrian air-quality monitoring stations. These events help consumers build monitoring, alerting, analytics, and dashboards without polling the upstream API directly.

## At a glance

- **Event types:** 3 documented event types (9 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 1 reference/catalog event type and 2 telemetry event types.
- **Identity:** `{station_id}`, `{component_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `uba-airdata`. The record key is `{station_id}`, `{component_id}`. Each key template is explained in the event catalog below. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['uba-airdata'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `air-quality/at/uba/uba-airdata/+/+/+/info`, `air-quality/at/uba/uba-airdata/+/+/+/measure`, `air-quality/at/uba/uba-airdata/+/+/+/component`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('air-quality/at/uba/uba-airdata/+/+/+/info', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `uba-airdata`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/uba-airdata')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Station

CloudEvents type: `de.uba.airdata.Station`

#### What it tells you

Reference data for a UBA air quality monitoring station, including geographic position, station environment, and the denormalized monitoring network metadata published by the UBA air_data/v3 station catalog.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is stable numeric UBA station identifier from the 'station id' column. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `uba-airdata`, key `{station_id}` |
| `MQTT/5.0` | topic `air-quality/at/uba/uba-airdata/{bundesland}/{station_id}/{component_id}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/uba-airdata`, message subject `{station_id}`; application properties bundesland `{bundesland}`, component_id `{component_id}` |

#### Payload

`Station` payloads are JSON object. Required fields: `station_id`, `station_code`, `station_name`, `station_city`, `station_synonym`, `active_from`, `active_to`, `longitude`, `latitude`, `network_id`, `network_code`, `network_name`, `setting_name`, `setting_short`, `type_name`, `street`, `street_nr`, `zip_code`.

- **`station_id`** (int32, required): Stable numeric UBA station identifier from the 'station id' column. This is the station key used for CloudEvents subject and Kafka key.
- **`station_code`** (string, required): Official station code from the 'station code' column, typically the European Environment Agency style identifier such as 'DEBE021' or 'DEBB003'.
- **`station_name`** (string, required): Human-readable station name from the 'station name' column as published by UBA.
- **`station_city`** (string, required): City or locality from the 'station city' column where the monitoring station is located.
- **`station_synonym`** (string or null, required): Legacy or alternate station short code from the 'station synonym' column. UBA may publish an empty value when no synonym exists.
- **`active_from`** (string, required): Station activation date from the 'station active from' column in ISO date form 'YYYY-MM-DD'.
- **`active_to`** (string or null, required): Station deactivation date from the 'station active to' column in ISO date form 'YYYY-MM-DD'. Null means the station is still active.
- **`longitude`** (double, required): Station longitude from the 'station longitude' column in WGS84 decimal degrees.
- **`latitude`** (double, required): Station latitude from the 'station latitude' column in WGS84 decimal degrees.
- **`network_id`** (int32, required): Stable numeric monitoring network identifier from the 'network id' column. This maps to the federal state or the UBA-operated network.
- **`network_code`** (string, required): Short network code from the 'network code' column, usually a two-letter German state code such as 'BE' or 'BB', or 'UB' for UBA.
- **`network_name`** (string, required): Monitoring network name from the 'network name' column, typically the English federal state name such as 'Berlin' or 'Brandenburg'.
- **`setting_name`** (string, required): Station environment description from the 'station setting name' column, for example 'urban area'.
- **`setting_short`** (string, required): Short station environment code from the 'station setting short name' column, for example 'urban'.
- **`type_name`** (string, required): Station type classification from the 'station type name' column, for example 'traffic', 'background', or 'industrial'.
- **`street`** (string or null, required): Street name from the 'station street' column. Null is used when UBA does not publish a street value.
- **`street_nr`** (string or null, required): Street number from the 'station street nr' column. Null is used when the source publishes an empty value.
- **`zip_code`** (string or null, required): Postal code from the 'station zip code' column. Null is used when the source publishes an empty value.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": 0,
  "station_code": "string",
  "station_name": "string",
  "station_city": "string",
  "station_synonym": "string",
  "active_from": "string",
  "active_to": "string",
  "longitude": 0,
  "latitude": 0,
  "network_id": 0,
  "network_code": "string",
  "network_name": "string",
  "setting_name": "string",
  "setting_short": "string",
  "type_name": "string",
  "street": "string",
  "street_nr": "string",
  "zip_code": "string"
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Measure

CloudEvents type: `de.uba.airdata.Measure`

#### What it tells you

Hourly one-hour-average air quality measurement for a UBA monitoring station and pollutant component as returned by the air_data/v3 measures endpoint.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is stable numeric UBA station identifier for the station that reported the measurement. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `uba-airdata`, key `{station_id}` |
| `MQTT/5.0` | topic `air-quality/at/uba/uba-airdata/{bundesland}/{station_id}/{component_id}/measure`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/uba-airdata`, message subject `{station_id}`; application properties bundesland `{bundesland}`, component_id `{component_id}` |

#### Payload

`Measure` payloads are JSON object. Required fields: `station_id`, `component_id`, `scope_id`, `date_start`, `date_end`, `value`, `quality_index`.

- **`station_id`** (int32, required): Stable numeric UBA station identifier for the station that reported the measurement.
- **`component_id`** (int32, required): Stable numeric UBA pollutant component identifier from the first element of the measure value array, for example 5 for NO₂.
- **`scope_id`** (int32, required): Stable numeric UBA averaging scope identifier from the second element of the measure value array. Scope 2 represents the one-hour average used by this bridge.
- **`date_start`** (string, required): Measurement period start timestamp from the nested measures object key, using the UBA local datetime format 'YYYY-MM-DD HH:MM:SS'.
- **`date_end`** (string, required): Measurement period end timestamp from the fourth element of the measure value array, using the UBA local datetime format 'YYYY-MM-DD HH:MM:SS'.
- **`value`** (double or null, required): Measured pollutant value from the third element of the measure value array, expressed in the unit defined by the referenced component. Null means the source returned no numeric measurement value.
- **`quality_index`** (string, required): UBA quality or confidence flag from the fifth element of the measure value array. The published documentation commonly references 0 valid, 1 provisional, and 2 estimated; live payloads have also been observed with the code 3.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": 0,
  "component_id": 0,
  "scope_id": 0,
  "date_start": "string",
  "date_end": "string",
  "value": 0,
  "quality_index": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Component

CloudEvents type: `de.uba.airdata.components.Component`

#### What it tells you

Reference data for an air pollutant component published by the UBA air_data/v3 components catalog, including the stable numeric component identifier, code, symbol, unit, and English display name.

#### Identity

Each event identifies the real-world resource with `{component_id}`. `{component_id}` is stable numeric UBA component identifier from the 'component id' column. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `uba-airdata`, key `{component_id}` |
| `MQTT/5.0` | topic `air-quality/at/uba/uba-airdata/{bundesland}/{station_id}/{component_id}/component`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/uba-airdata`, message subject `{component_id}`; application properties bundesland `{bundesland}`, station_id `{station_id}` |

#### Payload

`Component` payloads are JSON object. Required fields: `component_id`, `component_code`, `symbol`, `unit`, `name`.

- **`component_id`** (int32, required): Stable numeric UBA component identifier from the 'component id' column. This is the CloudEvents subject and Kafka key for component events.
- **`component_code`** (string, required): Short UBA component code from the 'component code' column, such as 'PM10', 'NO2', 'O3', or 'PM2'.
- **`symbol`** (string, required): Published component symbol from the 'component symbol' column. This may include Unicode subscripts, for example 'PM₁₀' or 'NO₂'.
- **`unit`** (string, required): Published measurement unit string from the 'component unit' column, such as 'µg/m³', 'mg/m³', or 'ng/m³'.
- **`name`** (string, required): English component display name from the 'component name' column, such as 'Particulate matter' or 'Nitrogen dioxide'.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "component_id": 0,
  "component_code": "string",
  "symbol": "string",
  "unit": "string",
  "name": "string"
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

- xRegistry manifest: [`xreg/uba_airdata.xreg.json`](xreg/uba_airdata.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
