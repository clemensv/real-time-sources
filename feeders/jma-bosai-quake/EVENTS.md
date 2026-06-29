# JMA Bosai Quake Events

JMA Bosai Earthquake publishes earthquake reports and intensity updates from the Japan Meteorological Agency for Japanese earthquake report areas. These events help consumers monitor hazards, route notifications, and correlate public-warning updates without polling the upstream source directly.

## At a glance

- **Event types:** 1 documented event type (3 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 1 telemetry event type.
- **Identity:** `jp.jma.quake/{event_id}/{serial}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `jma-bosai-quake`. The record key is `jp.jma.quake/{event_id}/{serial}`. In plain language, `jp.jma.quake/{event_id}/{serial}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['jma-bosai-quake'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `seismic/jp/jma/jma-bosai-quake/+/+/+/+/report`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('seismic/jp/jma/jma-bosai-quake/+/+/+/+/report', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `jma-bosai-quake`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/jma-bosai-quake')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Earthquake Report

CloudEvents type: `JP.JMA.Quake.EarthquakeReport`

#### What it tells you

JMA Bosai earthquake and seismic intensity report header enriched with parsed hypocenter coordinates, prefecture and city intensity summaries, and tsunami-related comment interpretation from the detail bulletin when available.

#### Identity

Each event identifies the real-world resource with `jp.jma.quake/{event_id}/{serial}`. `{event_id}` is stable JMA earthquake event identifier copied from list.json eid and detail Head.EventID; `{serial}` is JMA report serial number parsed from list.json ser and detail Head.Serial. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `jma-bosai-quake`, key `jp.jma.quake/{event_id}/{serial}` |
| `MQTT/5.0` | topic `seismic/jp/jma/jma-bosai-quake/{prefecture}/{magnitude_bucket}/{event_id}/{serial}/report`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/jma-bosai-quake`, message subject `jp.jma.quake/{event_id}/{serial}` |

#### Payload

`Earthquake Report` payloads are JSON object. Required fields: `prefecture`, `magnitude_bucket`, `event_id`, `serial`, `report_id`, `info_type`, `report_datetime`, `report_datetime_local`, `control_datetime`, `control_datetime_local`, `origin_datetime`, `origin_datetime_local`, `title_jp`, `bulletin_type`, `detail_url`, `affected_prefectures`, `affected_cities`, `tsunami_possible`.

- **`prefecture`** (string, required): ASCII-safe Romanized prefecture slug derived from the JMA epicenter area name when available, otherwise from the first affected prefecture code. Japanese names remain in epicenter_area_jp and affected prefecture/city payload fields; MQTT topics use this ASCII axis. Constraints: pattern `^[a-z0-9][a-z0-9-]*$`.
- **`magnitude_bucket`** (string, required): MQTT routing bucket derived from the JMA magnitude. Values are magnitude-lt1, magnitude-1 through magnitude-8 for floor buckets, magnitude-9plus, or magnitude-unknown when the bulletin omits magnitude. Constraints: pattern `^magnitude-(unknown|lt1|[1-8]|9plus)$`.
- **`event_id`** (string, required): Stable JMA earthquake event identifier copied from list.json eid and detail Head.EventID. JMA uses the earthquake origin time in YYYYMMDDHHMMSS form as the event id, so multiple serial reports for the same earthquake share this value. Constraints: pattern `^[0-9]{14}$`.
- **`serial`** (integer, required): JMA report serial number parsed from list.json ser and detail Head.Serial. The serial identifies the revision sequence for bulletins sharing the same event id. Constraints: minimum `0`.
- **`report_id`** (string, required): Composite report identifier formed as event_id, an underscore, and the JMA serial number. It distinguishes initial, corrected, and subsequent bulletins for the same earthquake event.
- **`info_type`** (enum, required): Normalized information type derived from the Japanese JMA ift field: ISSUED for 発表, CORRECTED for 訂正, and CANCELLED for 取消.
- **`report_datetime`** (datetime, required): Report publication time converted from list.json rdt to an RFC3339 UTC timestamp. JMA publishes rdt with a local offset for the report release time.
- **`report_datetime_local`** (datetime, required): Original JMA report publication timestamp copied from list.json rdt, preserving the local offset supplied by the JMA Bosai feed.
- **`control_datetime`** (datetime, required): JMA control timestamp — when the bulletin was published to the JMA distribution system, distinct from `report_datetime` which is the event report time. This field converts the compact list.json ctt value from JST to an RFC3339 UTC timestamp.
- **`control_datetime_local`** (datetime, required): JMA control timestamp — when the bulletin was published to the JMA distribution system, distinct from `report_datetime` which is the event report time. This field preserves the compact list.json ctt value as an RFC3339 timestamp with the Japan Standard Time offset.
- **`origin_datetime`** (datetime, required): Earthquake origin time converted from list.json at to an RFC3339 UTC timestamp. JMA uses this time as the basis for the event id.
- **`origin_datetime_local`** (datetime, required): Original JMA earthquake origin timestamp copied from list.json at, preserving the local offset supplied by the JMA Bosai feed.
- **`title_jp`** (string, required): Japanese JMA bulletin title copied from list.json ttl, such as 震源・震度情報 for earthquake and seismic intensity information.
- **`title_en`** (string or null, optional): English bulletin title copied from list.json en_ttl when supplied by the multilingual JMA Bosai feed. Null is emitted when en_ttl is absent, including some 震度速報, 南海トラフ関連解説情報, and 顕著な地震の震源要素更新のお知らせ bulletins.
- **`epicenter_area_code`** (string or null, optional): JMA hypocenter or epicenter area code copied from list.json acd and detail Body.Earthquake.Hypocenter.Area.Code. Null is emitted when the source bulletin omits hypocenter metadata, including 震度速報, 南海トラフ関連解説情報, and 顕著な地震の震源要素更新のお知らせ bulletins.
- **`epicenter_area_jp`** (string or null, optional): Japanese epicenter area name copied from list.json anm and detail Body.Earthquake.Hypocenter.Area.Name. Null is emitted when the source bulletin omits hypocenter metadata, including 震度速報, 南海トラフ関連解説情報, and 顕著な地震の震源要素更新のお知らせ bulletins.
- **`epicenter_area_en`** (string or null, optional): English epicenter area name copied from list.json en_anm when supplied by the multilingual JMA Bosai feed. Null is emitted when the source bulletin omits hypocenter metadata, including 震度速報, 南海トラフ関連解説情報, and 顕著な地震の震源要素更新のお知らせ bulletins.
- **`latitude`** (double or null, optional, degree (°)): Hypocenter latitude in WGS84 decimal degrees parsed from the ISO 6709 coordinate string in list.json cod or detail Body.Earthquake.Hypocenter.Area.Coordinate. Null is emitted when the coordinate is absent or cannot be parsed; null is also emitted when list.json cod is absent, including 震度速報, 南海トラフ関連解説情報, and 顕著な地震の震源要素更新のお知らせ bulletins. Constraints: minimum `-90.0`, maximum `90.0`.
- **`longitude`** (double or null, optional, degree (°)): Hypocenter longitude in WGS84 decimal degrees parsed from the ISO 6709 coordinate string in list.json cod or detail Body.Earthquake.Hypocenter.Area.Coordinate. Null is emitted when the coordinate is absent or cannot be parsed; null is also emitted when list.json cod is absent, including 震度速報, 南海トラフ関連解説情報, and 顕著な地震の震源要素更新のお知らせ bulletins. Constraints: minimum `-180.0`, maximum `180.0`.
- **`depth_km`** (double or null, optional, kilometer (km)): Hypocenter depth in kilometres parsed from the third component of the ISO 6709 coordinate string. JMA encodes depth in metres with a sign in cod; this field divides the absolute metre value by 1000 so +35.0+135.5-10000/ becomes 10.0 km. Null is emitted when list.json cod is absent, including 震度速報, 南海トラフ関連解説情報, and 顕著な地震の震源要素更新のお知らせ bulletins. Constraints: minimum `0.0`, maximum `700.0`.
- **`magnitude`** (double or null, optional): Dimensionless JMA earthquake magnitude parsed from list.json mag or detail Body.Earthquake.Magnitude and expressed on the JMA magnitude scale, which is similar to Richter magnitude for shallow events. Null is emitted when the source bulletin omits magnitude, including 震度速報, 南海トラフ関連解説情報, and 顕著な地震の震源要素更新のお知らせ bulletins.
- **`max_intensity`** (string or null, optional): Maximum observed JMA seismic intensity for the report copied from list.json maxi or detail Body.Intensity.Observation.MaxInt. Null is emitted when the bulletin has no observed intensity summary, including 震度速報, 南海トラフ関連解説情報, and 顕著な地震の震源要素更新のお知らせ bulletins. Constraints: pattern `^(1|2|3|4|5-|5\+|6-|6\+|7)$`.
- **`bulletin_type`** (enum, required): JMA detail bulletin product code parsed from the detail JSON filename. Supported earthquake-related JMA Bosai codes are VXSE51 (震度速報), VXSE52 (震源に関する情報), VXSE53 (震源・震度に関する情報), VXSE5k (震源・震度情報 Bosai variant), VXSE61 (長周期地震動に関する観測情報), and VYSE52 (南海トラフ地震関連解説情報). Tsunami-specific VTSE products are deliberately not modeled by this source.
- **`detail_url`** (uri, required): Absolute URL for the full JMA Bosai earthquake detail JSON referenced by list.json json.
- **`affected_prefectures`** (array of object, required): Prefecture intensity summaries derived from list.json int[]. Each entry includes the JMA prefecture code and maximum JMA seismic intensity reported for that prefecture.
- **`affected_cities`** (array of object, required): City intensity summaries flattened from list.json int[].city[]. Each entry carries its parent prefecture code, city code, and maximum JMA seismic intensity for the city.
- **`tsunami_possible`** (boolean or null, required): Interpretation of tsunami-related text in the full detail JSON comments. True means the detail bulletin text indicates tsunami attention or possibility; false means the detail explicitly states there is no tsunami concern; null means no tsunami-related detail text was available or fetched.
##### `info_type` values

- `ISSUED`: Provider value `ISSUED` for this coded alert field.
- `CORRECTED`: Provider value `CORRECTED` for this coded alert field.
- `CANCELLED`: Provider value `CANCELLED` for this coded alert field.
##### `max_intensity` values

- `1`: Provider value `1` for this coded alert field.
- `2`: Provider value `2` for this coded alert field.
- `3`: Provider value `3` for this coded alert field.
- `4`: Provider value `4` for this coded alert field.
- `5-`: Provider value `5-` for this coded alert field.
- `5+`: Provider value `5+` for this coded alert field.
- `6-`: Provider value `6-` for this coded alert field.
- `6+`: Provider value `6+` for this coded alert field.
- `7`: Provider value `7` for this coded alert field.
##### `bulletin_type` values

- `VXSE51`: Provider value `VXSE51` for this coded alert field.
- `VXSE52`: Provider value `VXSE52` for this coded alert field.
- `VXSE53`: Provider value `VXSE53` for this coded alert field.
- `VXSE5k`: Provider value `VXSE5k` for this coded alert field.
- `VXSE61`: Provider value `VXSE61` for this coded alert field.
- `VYSE52`: Provider value `VYSE52` for this coded alert field.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "prefecture": "string",
  "magnitude_bucket": "string",
  "event_id": "string",
  "serial": 0,
  "report_id": "string",
  "info_type": "ISSUED",
  "report_datetime": "2024-01-01T00:00:00Z",
  "report_datetime_local": "2024-01-01T00:00:00Z",
  "control_datetime": "2024-01-01T00:00:00Z",
  "control_datetime_local": "2024-01-01T00:00:00Z",
  "origin_datetime": "2024-01-01T00:00:00Z",
  "origin_datetime_local": "2024-01-01T00:00:00Z",
  "title_jp": "string",
  "title_en": "string",
  "epicenter_area_code": "string",
  "epicenter_area_jp": "string",
  "epicenter_area_en": "string",
  "latitude": 0,
  "longitude": 0,
  "depth_km": 0,
  "magnitude": 0,
  "max_intensity": "1",
  "bulletin_type": "VXSE51",
  "detail_url": "string",
  "affected_prefectures": [
    {
      "code": "string",
      "max_intensity": "1"
    }
  ],
  "affected_cities": [
    {
      "prefecture_code": "string",
      "city_code": "string",
      "max_intensity": "1"
    }
  ],
  "tsunami_possible": false
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

- xRegistry manifest: [`xreg/jma-bosai-quake.xreg.json`](xreg/jma-bosai-quake.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- Azure Service Bus Standard namespace: <https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview>
