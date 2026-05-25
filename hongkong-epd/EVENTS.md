# Hong Kong EPD AQHI Bridge Events

MQTT/5.0 transport variants of the HK EPD AQHI CloudEvents, mapping each message to a retained, QoS-1 Unified Namespace topic under air-quality/hk/epd/hongkong-epd/{district}/{station_id}/... The {district} placeholder is the Hong Kong 18-district administrative area where the station is located, normalized to lowercase snake_case.

## At a glance

- **Event types:** 2 documented event types (4 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0
- **Reference vs telemetry:** 1 reference/catalog event type and 1 telemetry event type.
- **Identity:** `{station_id}` identifies the resource each event is about.
- **Operations:** The checked-in guide documents a default polling interval of 3600 seconds.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `hongkong-epd-aqhi`. The record key is `{station_id}`. In plain language, `{station_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['hongkong-epd-aqhi'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `air-quality/hk/epd/hongkong-epd/+/+/info`, `air-quality/hk/epd/hongkong-epd/+/+/aqhi`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('air-quality/hk/epd/hongkong-epd/+/+/info', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.

## Event catalog

### Station

CloudEvents type: `HK.Gov.EPD.AQHI.Station`

#### What it tells you

Reference data for a Hong Kong EPD AQHI monitoring station. The EPD operates a network of General Stations and Roadside Stations across Hong Kong. Station coordinates are derived from the EPD station map.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is stable station identifier derived from the station name in snake_case, for example central_western or mong_kok. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `hongkong-epd-aqhi`, key `{station_id}` |
| `MQTT/5.0` | topic `air-quality/hk/epd/hongkong-epd/{district}/{station_id}/info`, retain `true`, QoS `1` |

#### Payload

`Station` payloads are JSON object. Required fields: `station_id`, `station_name`, `station_type`, `district`.

- **`station_id`** (string, required): Stable station identifier derived from the station name in snake_case, for example central_western or mong_kok.
- **`station_name`** (string, required): Station name as published in the EPD AQHI feed, for example 'Central/Western' or 'Mong Kok'.
- **`station_type`** (string, required): Station classification. General Stations measure ambient background air quality and Roadside Stations are positioned near roads to capture traffic-related pollution.
- **`district`** (string, required): Hong Kong 18-district administrative area where the monitoring station is located, normalized to lowercase snake_case. Used as the {district} segment of the MQTT/UNS topic. Examples: central-and-western, wan-chai, yau-tsim-mong.
- **`latitude`** (double or null, optional, degree (°)): WGS84 latitude of the monitoring station.
- **`longitude`** (double or null, optional, degree (°)): WGS84 longitude of the monitoring station.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "station_name": "string",
  "station_type": "string",
  "district": "string",
  "latitude": 0,
  "longitude": 0
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Aqhireading

CloudEvents type: `HK.Gov.EPD.AQHI.AQHIReading`

#### What it tells you

Air Quality Health Index (AQHI) reading for a Hong Kong EPD monitoring station. AQHI quantifies health risk from air pollution on a scale of 1 to 10+ and is calculated from concentrations of nitrogen dioxide, sulphur dioxide, ozone, and PM2.5. Published hourly by the EPD.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is stable station identifier in snake_case. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `hongkong-epd-aqhi`, key `{station_id}` |
| `MQTT/5.0` | topic `air-quality/hk/epd/hongkong-epd/{district}/{station_id}/aqhi`, retain `true`, QoS `1` |

#### Payload

`Aqhireading` payloads are JSON object. Required fields: `station_id`, `station_name`, `station_type`, `district`, `reading_time`, `aqhi`.

- **`station_id`** (string, required): Stable station identifier in snake_case.
- **`station_name`** (string, required): Station name as published in the EPD AQHI feed.
- **`station_type`** (string, required): Station classification: General Stations or Roadside Stations.
- **`district`** (string, required): Hong Kong 18-district administrative area where the monitoring station is located, normalized to lowercase snake_case. Used as the {district} segment of the MQTT/UNS topic.
- **`reading_time`** (datetime, required): Observation timestamp parsed from the feed DateTime field. The XML feed publishes RFC 2822 timestamps and the bridge emits ISO 8601 values.
- **`aqhi`** (integer, required): AQHI value. Scale: 1 to 3 Low health risk, 4 to 6 Moderate, 7 High, 8 to 10 Very High, and above 10 Serious. Value 11 is used in the feed to indicate 10+ Serious. Constraints: minimum `1`.
- **`health_risk_category`** (string or null, optional): Health risk category derived from the AQHI value: Low, Moderate, High, Very High, or Serious.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "station_name": "string",
  "station_type": "string",
  "district": "string",
  "reading_time": "2024-01-01T00:00:00Z",
  "aqhi": 0,
  "health_risk_category": "string"
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

- The checked-in guide documents a default polling interval of 3600 seconds.
- The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- Reference/catalog events are documented as startup emissions, with periodic refresh when the source supports it.

## References

- xRegistry manifest: [`xreg/hongkong_epd.xreg.json`](xreg/hongkong_epd.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
