# EPA UV Bridge Events

MQTT/5.0 transport variants for EPA UV Index forecasts. Topics are retained QoS-1 UV forecast leaves under uv/us/epa/epa-uv/{state}/{city_slug}/{location_id}/..., where {state} is lowercase US state, {city_slug} is lowercase kebab-case city, and {location_id} preserves the existing Kafka/CloudEvents entity id intentionally for subject/key compatibility even though it is derivable from state+city. Hourly slots use topic-safe {forecast_hour}=YYYYMMDDTHH; daily slots use {forecast_date}=YYYY-MM-DD. Message expiry bounds retained forecast slots so stale forecasts age out.

## At a glance

- **Event types:** 2 documented event types (4 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0
- **Reference vs telemetry:** 0 reference/catalog event types and 2 telemetry event types.
- **Identity:** `{location_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `epa-uv`. The record key is `{location_id}`. In plain language, `{location_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['epa-uv'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `uv/us/epa/epa-uv/+/+/+/hourly/+`, `uv/us/epa/epa-uv/+/+/+/daily/+`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('uv/us/epa/epa-uv/+/+/+/hourly/+', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.

## Event catalog

### Hourly Forecast

CloudEvents type: `US.EPA.UVIndex.HourlyForecast`

#### What it tells you

Hourly UV Index forecast for a configured city and state from the EPA Envirofacts UV hourly service.

#### Identity

Each event identifies the real-world resource with `{location_id}`. `{location_id}` is stable slug derived from the configured city and state. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `epa-uv`, key `{location_id}` |
| `MQTT/5.0` | topic `uv/us/epa/epa-uv/{state}/{city_slug}/{location_id}/hourly/{forecast_hour}`, retain `true`, QoS `1` |

#### Payload

`Hourly Forecast` payloads are JSON object. Required fields: `location_id`, `city`, `state`, `forecast_datetime`, `uv_index`, `city_slug`, `forecast_hour`.

- **`location_id`** (string, required): Stable slug derived from the configured city and state.
- **`city`** (string, required): City for which the hourly UV forecast was requested.
- **`state`** (string, required): Lowercase two-letter US state segment used for MQTT/UNS routing; display/input state is normalized by the bridge.
- **`forecast_datetime`** (string, required): Forecast timestamp normalized to ISO local datetime form without an explicit UTC offset. Used as the retained MQTT hourly slot with message expiry.
- **`uv_index`** (integer, required): Hourly UV Index forecast value.
- **`city_slug`** (string, required): Lowercase kebab-case city segment used for MQTT/UNS routing; derived from city without the state suffix.
- **`forecast_hour`** (string, required): Topic-safe retained forecast slot in YYYYMMDDTHH form, derived from forecast_datetime with zero padding and no offset, colon, slash, plus, or hash characters.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "location_id": "string",
  "city": "string",
  "state": "string",
  "forecast_datetime": "string",
  "uv_index": 0,
  "city_slug": "string",
  "forecast_hour": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Daily Forecast

CloudEvents type: `US.EPA.UVIndex.DailyForecast`

#### What it tells you

Daily UV Index forecast and alert flag for a configured city and state from the EPA Envirofacts UV daily service.

#### Identity

Each event identifies the real-world resource with `{location_id}`. `{location_id}` is stable slug derived from the configured city and state. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `epa-uv`, key `{location_id}` |
| `MQTT/5.0` | topic `uv/us/epa/epa-uv/{state}/{city_slug}/{location_id}/daily/{forecast_date}`, retain `true`, QoS `1` |

#### Payload

`Daily Forecast` payloads are JSON object. Required fields: `location_id`, `city`, `state`, `forecast_date`, `uv_index`, `uv_alert`, `city_slug`.

- **`location_id`** (string, required): Stable slug derived from the configured city and state.
- **`city`** (string, required): City for which the daily UV forecast was requested.
- **`state`** (string, required): Lowercase two-letter US state segment used for MQTT/UNS routing; display/input state is normalized by the bridge.
- **`forecast_date`** (string, required): Topic-safe forecast date normalized to YYYY-MM-DD. Used as the retained MQTT daily slot with message expiry.
- **`uv_index`** (integer, required): Daily UV Index forecast value.
- **`uv_alert`** (string, required): Character flag indicating whether a UV alert is issued for the forecast day.
- **`city_slug`** (string, required): Lowercase kebab-case city segment used for MQTT/UNS routing; derived from city without the state suffix.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "location_id": "string",
  "city": "string",
  "state": "string",
  "forecast_date": "string",
  "uv_index": 0,
  "uv_alert": "string",
  "city_slug": "string"
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
- The MQTT variant publishes with QoS 1 and retained-message Last-Known-Value semantics where declared in the event catalog.

## References

- xRegistry manifest: [`xreg/epa_uv.xreg.json`](xreg/epa_uv.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
