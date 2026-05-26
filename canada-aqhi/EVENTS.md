# Canada AQHI Bridge Events

Canada AQHI publishes air-quality health index observations and forecasts from Environment and Climate Change Canada (ECCC) for Canadian Air Quality Health Index communities. These events help consumers build monitoring, alerting, analytics, and dashboards without polling the upstream API directly.

## At a glance

- **Event types:** 3 documented event types (9 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 3 telemetry event types.
- **Identity:** `{province}/{community_name}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `canada-aqhi`. The record key is `{province}/{community_name}`. In plain language, `{province}/{community_name}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['canada-aqhi'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `air-quality/ca/eccc/canada-aqhi/+/+/info`, `air-quality/ca/eccc/canada-aqhi/+/+/observation`, `air-quality/ca/eccc/canada-aqhi/+/+/forecast`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('air-quality/ca/eccc/canada-aqhi/+/+/info', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `canada-aqhi`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/canada-aqhi')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Community

CloudEvents type: `ca.gc.weather.aqhi.Community`

#### What it tells you

Reference data for a Canadian Air Quality Health Index reporting community, including its stable CGNDB identifier and current upstream feed URLs.

#### Identity

Each event identifies the real-world resource with `{province}/{community_name}`. `{province}` is two-letter Canadian province or territory abbreviation resolved for the AQHI community; `{community_name}` is english AQHI community name as published by Environment and Climate Change Canada. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `canada-aqhi`, key `{province}/{community_name}` |
| `MQTT/5.0` | topic `air-quality/ca/eccc/canada-aqhi/{province}/{community_name}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/canada-aqhi`, message subject `{province}/{community_name}`; application properties province `{province}`, community_name `{community_name}` |

#### Payload

`Community` payloads are JSON object. Required fields: `province`, `community_name`, `cgndb_code`, `latitude`, `longitude`.

- **`province`** (string, required): Two-letter Canadian province or territory abbreviation resolved for the AQHI community. Constraints: pattern `^[A-Z]{2}$`.
- **`community_name`** (string, required): English AQHI community name as published by Environment and Climate Change Canada.
- **`cgndb_code`** (string, required): Five-character CGNDB community identifier published by Natural Resources Canada and referenced by ECCC AQHI feeds. Constraints: pattern `^[A-Z0-9]{5}$`.
- **`latitude`** (double, required): Latitude of the AQHI community reference point in WGS84 decimal degrees. Constraints: minimum `-90`, maximum `90`.
- **`longitude`** (double, required): Longitude of the AQHI community reference point in WGS84 decimal degrees. Constraints: minimum `-180`, maximum `180`.
- **`observation_url`** (string or null, optional): Current XML observation feed URL for the AQHI community, or null when observations are not distributed for that community.
- **`forecast_url`** (string or null, optional): Current XML forecast feed URL for the AQHI community, or null when a public forecast feed is not available.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "province": "string",
  "community_name": "string",
  "cgndb_code": "string",
  "latitude": 0,
  "longitude": 0,
  "observation_url": "string",
  "forecast_url": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Observation

CloudEvents type: `ca.gc.weather.aqhi.Observation`

#### What it tells you

Latest AQHI observation for a reporting community. Observations are published hourly and may include decimal AQHI values.

#### Identity

Each event identifies the real-world resource with `{province}/{community_name}`. `{province}` is two-letter Canadian province or territory abbreviation resolved for the AQHI community; `{community_name}` is english AQHI community name as published by Environment and Climate Change Canada. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `canada-aqhi`, key `{province}/{community_name}` |
| `MQTT/5.0` | topic `air-quality/ca/eccc/canada-aqhi/{province}/{community_name}/observation`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/canada-aqhi`, message subject `{province}/{community_name}`; application properties province `{province}`, community_name `{community_name}` |

#### Payload

`Observation` payloads are JSON object. Required fields: `province`, `community_name`, `cgndb_code`, `observation_datetime`, `aqhi_category`.

- **`province`** (string, required): Two-letter Canadian province or territory abbreviation resolved for the AQHI community. Constraints: pattern `^[A-Z]{2}$`.
- **`community_name`** (string, required): English AQHI community name as published by Environment and Climate Change Canada.
- **`cgndb_code`** (string, required): Five-character CGNDB community identifier published by Natural Resources Canada and referenced by ECCC AQHI feeds. Constraints: pattern `^[A-Z0-9]{5}$`.
- **`observation_datetime`** (string, required): UTC timestamp of the AQHI observation in ISO 8601 format.
- **`aqhi`** (double or null, optional): Observed AQHI value for the community. Observation feeds publish AQHI with decimal precision.
- **`aqhi_category`** (enum, required): Public AQHI health-risk category derived from the AQHI value.
##### `aqhi_category` values

- `Low`
- `Moderate`
- `High`
- `Very High`
- `Unknown`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "province": "string",
  "community_name": "string",
  "cgndb_code": "string",
  "observation_datetime": "string",
  "aqhi": 0,
  "aqhi_category": "Low"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Forecast

CloudEvents type: `ca.gc.weather.aqhi.Forecast`

#### What it tells you

Public AQHI forecast for one of the four standard Canadian forecast periods published for an AQHI community.

#### Identity

Each event identifies the real-world resource with `{province}/{community_name}`. `{province}` is two-letter Canadian province or territory abbreviation resolved for the AQHI community; `{community_name}` is english AQHI community name as published by Environment and Climate Change Canada. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `canada-aqhi`, key `{province}/{community_name}` |
| `MQTT/5.0` | topic `air-quality/ca/eccc/canada-aqhi/{province}/{community_name}/forecast`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/canada-aqhi`, message subject `{province}/{community_name}`; application properties province `{province}`, community_name `{community_name}` |

#### Payload

`Forecast` payloads are JSON object. Required fields: `province`, `community_name`, `cgndb_code`, `publication_datetime`, `forecast_date`, `forecast_period`, `forecast_period_label`, `aqhi_category`.

- **`province`** (string, required): Two-letter Canadian province or territory abbreviation resolved for the AQHI community. Constraints: pattern `^[A-Z]{2}$`.
- **`community_name`** (string, required): English AQHI community name as published by Environment and Climate Change Canada.
- **`cgndb_code`** (string, required): Five-character CGNDB community identifier published by Natural Resources Canada and referenced by ECCC AQHI feeds. Constraints: pattern `^[A-Z0-9]{5}$`.
- **`publication_datetime`** (string, required): UTC timestamp at which the public AQHI forecast bulletin was issued.
- **`forecast_date`** (string, required): Forecast target date expressed as YYYYMMDD. Periods 1 and 2 use the bulletin issue date; periods 3 and 4 use the following day. Constraints: pattern `^[0-9]{8}$`.
- **`forecast_period`** (enum, required): AQHI public forecast period number: 1 Today, 2 Tonight, 3 Tomorrow, 4 Tomorrow Night.
- **`forecast_period_label`** (enum, required): English public label for the AQHI forecast period.
- **`aqhi`** (integer or null, optional): Forecast AQHI value for the forecast period. Public forecasts are published as whole numbers.
- **`aqhi_category`** (enum, required): Public AQHI health-risk category derived from the forecast AQHI value.
##### `forecast_period` values

- `1`
- `2`
- `3`
- `4`
##### `forecast_period_label` values

- `Today`
- `Tonight`
- `Tomorrow`
- `Tomorrow Night`
##### `aqhi_category` values

- `Low`
- `Moderate`
- `High`
- `Very High`
- `Unknown`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "province": "string",
  "community_name": "string",
  "cgndb_code": "string",
  "publication_datetime": "string",
  "forecast_date": "string",
  "forecast_period": 1,
  "forecast_period_label": "Today",
  "aqhi": 0,
  "aqhi_category": "Low"
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

- xRegistry manifest: [`xreg/canada-aqhi.xreg.json`](xreg/canada-aqhi.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- ![Deploy AMQP Service Bus: <https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078D4?logo=microsoftazure&logoColor=white>
