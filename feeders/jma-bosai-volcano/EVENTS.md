# JMA Bosai Volcano feeder Events

JMA Bosai Volcano publishes volcano warnings and eruption notices from the Japan Meteorological Agency for Japanese volcano warning areas. These events help consumers monitor hazards, route notifications, and correlate public-warning updates without polling the upstream source directly.

## At a glance

- **Event types:** 3 documented event types (9 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 3 telemetry event types.
- **Identity:** `jp.jma.volcano/{volcano_code}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `jma-bosai-volcano`. The record key is `jp.jma.volcano/{volcano_code}`. In plain language, `jp.jma.volcano/{volcano_code}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['jma-bosai-volcano'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `weather/jp/jma/jma-bosai-volcano/+/+/+`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('weather/jp/jma/jma-bosai-volcano/+/+/+', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `jma-bosai-volcano`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/jma-bosai-volcano')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Volcano

CloudEvents type: `JP.JMA.Volcano.Volcano`

#### What it tells you

JMA Bosai volcano catalog reference data emitted at startup and on monthly refresh.

#### Identity

Each event identifies the real-world resource with `jp.jma.volcano/{volcano_code}`. `{volcano_code}` is three-digit JMA volcano identifier used in the Bosai volcanic warning feeds and the volcano catalog. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `jma-bosai-volcano`, key `jp.jma.volcano/{volcano_code}` |
| `MQTT/5.0` | topic `weather/jp/jma/jma-bosai-volcano/{prefecture}/{volcano_code}/{event}`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/jma-bosai-volcano`, message subject `jp.jma.volcano/{volcano_code}`; application properties prefecture `{prefecture}`, event `{event}` |

#### Payload

`Volcano` payloads are JSON object. Required fields: `volcano_code`, `name_jp`, `name_en`, `latitude`, `longitude`, `level_operation`, `prefecture`, `event`.

- **`volcano_code`** (string, required): Three-digit JMA volcano identifier used in the Bosai volcanic warning feeds and the volcano catalog. This is the stable domain key for the volcano and is used in the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{3}$`.
- **`name_jp`** (string, required): Japanese volcano name from the JMA Bosai volcano catalog. This is a display label and is not used as the stable identity because JMA warning records key volcanoes by code.
- **`name_en`** (string, required): English volcano name from the JMA Bosai volcano catalog, used as a display label for international consumers.
- **`latitude`** (double, required, degree (°)): Latitude of the volcano in WGS84 decimal degrees. The bridge converts JMA degree-and-minute coordinates when present, and otherwise forwards the Bosai catalog decimal latitude.
- **`longitude`** (double, required, degree (°)): Longitude of the volcano in WGS84 decimal degrees. The bridge converts JMA degree-and-minute coordinates when present, and otherwise forwards the Bosai catalog decimal longitude.
- **`elevation_m`** (double or null, optional, meter (m)): Volcano summit elevation in metres when supplied by the JMA catalog. Some Bosai catalog entries omit elevation, so the field is null in emitted events when JMA does not provide the value.
- **`level_operation`** (boolean, required): True when JMA marks the volcano as operating under the five-level eruption alert system. False means the volcano is represented by binary issued/not-issued volcanic warnings rather than a local five-level evacuation framework.
- **`prefecture`** (string, required): ASCII-safe Japanese prefecture or region slug used as a MQTT and AMQP routing axis. The bridge derives this from JMA station/volcano metadata when available, otherwise emits unknown. Constraints: pattern `^[a-z0-9][a-z0-9-]*$`.
- **`event`** (enum, required): Fixed topic event segment for Volcano messages.
##### `event` values

- `info`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "volcano_code": "string",
  "name_jp": "string",
  "name_en": "string",
  "latitude": 0,
  "longitude": 0,
  "elevation_m": 0,
  "level_operation": false,
  "prefecture": "string",
  "event": "info"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Volcanic Warning

CloudEvents type: `JP.JMA.Volcano.VolcanicWarning`

#### What it tells you

JMA Bosai active volcanic warning or forecast for a target volcano.

#### Identity

Each event identifies the real-world resource with `jp.jma.volcano/{volcano_code}`. `{volcano_code}` is three-digit JMA volcano identifier used in the Bosai volcanic warning feeds and the volcano catalog. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `jma-bosai-volcano`, key `jp.jma.volcano/{volcano_code}` |
| `MQTT/5.0` | topic `weather/jp/jma/jma-bosai-volcano/{prefecture}/{volcano_code}/{event}`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/jma-bosai-volcano`, message subject `jp.jma.volcano/{volcano_code}`; application properties prefecture `{prefecture}`, event `{event}` |

#### Payload

`Volcanic Warning` payloads are JSON object. Required fields: `volcano_code`, `event_id`, `report_datetime`, `report_datetime_local`, `alert_level_code`, `alert_level_name`, `condition`, `info_type_jp`, `area_codes`, `prefecture`, `event`.

- **`volcano_code`** (string, required): Three-digit JMA volcano identifier used in the Bosai volcanic warning feeds and the volcano catalog. This is the stable domain key for the volcano and is used in the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{3}$`.
- **`event_id`** (string, required): JMA eventId from the Bosai warning record. The warning feed uses this identifier with reportDatetime to identify the active report for a target volcano.
- **`report_datetime`** (datetime, required): Report issue time converted from JMA local Japan Standard Time to UTC and serialized as an RFC3339 timestamp. This is the normalized time used for cross-region analytics.
- **`report_datetime_local`** (datetime, required): Original JMA reportDatetime value in Japan Standard Time as published by the Bosai warning feed. Keeping the local timestamp preserves the official bulletin time shown by JMA.
- **`alert_level_code`** (string, required): Raw JMA volcanic warning code as published in the `code` field of warning.json, emitted verbatim as a string. JMA's volcanic warning codes form an OPEN, upstream-controlled vocabulary that changes with volcanic activity, so this field is intentionally not constrained to a closed enum; consumers should treat any unlisted code as a valid JMA code and rely on the sibling `alert_level_name` field for the human-readable label JMA publishes alongside each code. Known codes observed in the live feed and JMA eruption-alert-level guidance: `02` = Crater-area warning (火口周辺警報); `03` = Eruption warning for surrounding sea area (噴火警報（周辺海域）); `04` = Eruption forecast, warning lifted (噴火予報：警報解除); `11` = Active volcano, pay attention (活動火山であることに留意); `12` = Crater area restriction (火口周辺規制); `13` = Mountain access restriction (入山規制); `22` = Crater vicinity danger (火口周辺危険); `23` = Mountain access danger (入山危険); `36` = Surrounding waters warning for submarine or island volcanoes (周辺海域警戒); `43` = Crater-area warning, entry restrictions (火口周辺警報：入山規制等); `44` = Eruption warning for surrounding sea area, sea-area warning (噴火警報（周辺海域）：周辺海域警戒); `45` = Active volcano, pay attention (活火山であることに留意); `49` = Crater-area warning, caution around the crater (火口周辺警報：火口周辺警戒). Labels for codes 11/12/13 are from JMA eruption-alert-level guidance; the remaining labels are taken from the live warning.json item `name` fields, which the Bosai JSON feed publishes directly.
- **`alert_level_name`** (string, required): Japanese alert level or warning label from the target-volcano item, such as レベル３（入山規制）. JMA uses this text to communicate the public-facing warning level or restriction phrase.
- **`previous_level_code`** (string or null, optional): Previous JMA alert level or warning code from lastCode when the warning feed provides one. It allows consumers to determine whether the current report raised, lowered, continued, or newly issued a level.
- **`condition`** (enum, required): Normalized lifecycle condition derived from the Japanese JMA condition text. 発表 is mapped to ISSUED, 引上げ to RAISED, 引下げ to LOWERED, 継続 to CONTINUED, 切替 to SWITCHED, and 解除 to CANCELLED so downstream consumers can compare reports without parsing Japanese status labels.
- **`info_type_jp`** (string, required): Japanese volcanoInfos type label from the JMA feed. For emitted warning events the bridge uses the target-volcano section, normally 噴火警報・予報（対象火山）, because that section carries the stable volcano code identity.
- **`area_codes`** (array of string, required): List of JMA municipal or regional area codes from the outer areas field of the Bosai volcano report. JMA uses these area identifiers to indicate municipalities or regions affected by the volcanic warning or eruption information.
- **`prefecture`** (string, required): ASCII-safe Japanese prefecture or region slug used as a MQTT and AMQP routing axis. The bridge derives this from JMA station/volcano metadata when available, otherwise emits unknown. Constraints: pattern `^[a-z0-9][a-z0-9-]*$`.
- **`event`** (enum, required): Fixed topic event segment for VolcanicWarning messages.
##### `condition` values

- `ISSUED`: Provider value `ISSUED` for this coded alert field.
- `RAISED`: Provider value `RAISED` for this coded alert field.
- `LOWERED`: Provider value `LOWERED` for this coded alert field.
- `CONTINUED`: Provider value `CONTINUED` for this coded alert field.
- `SWITCHED`: Provider value `SWITCHED` for this coded alert field.
- `CANCELLED`: Provider value `CANCELLED` for this coded alert field.
##### `event` values

- `warning`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "volcano_code": "string",
  "event_id": "string",
  "report_datetime": "2024-01-01T00:00:00Z",
  "report_datetime_local": "2024-01-01T00:00:00Z",
  "alert_level_code": "string",
  "alert_level_name": "string",
  "previous_level_code": "string",
  "condition": "ISSUED",
  "info_type_jp": "string",
  "area_codes": [
    "string"
  ],
  "prefecture": "string",
  "event": "warning"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Volcanic Eruption

CloudEvents type: `JP.JMA.Volcano.VolcanicEruption`

#### What it tells you

JMA Bosai volcanic eruption observation report for a target volcano.

#### Identity

Each event identifies the real-world resource with `jp.jma.volcano/{volcano_code}`. `{volcano_code}` is three-digit JMA volcano identifier used in the Bosai volcanic warning feeds and the volcano catalog. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `jma-bosai-volcano`, key `jp.jma.volcano/{volcano_code}` |
| `MQTT/5.0` | topic `weather/jp/jma/jma-bosai-volcano/{prefecture}/{volcano_code}/{event}`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/jma-bosai-volcano`, message subject `jp.jma.volcano/{volcano_code}`; application properties prefecture `{prefecture}`, event `{event}` |

#### Payload

`Volcanic Eruption` payloads are JSON object. Required fields: `volcano_code`, `event_id`, `report_datetime`, `report_datetime_local`, `description`, `area_codes`, `prefecture`, `event`.

- **`volcano_code`** (string, required): Three-digit JMA volcano identifier used in the Bosai volcanic warning feeds and the volcano catalog. This is the stable domain key for the volcano and is used in the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{3}$`.
- **`event_id`** (string, required): JMA eventId from the Bosai eruption record. The bridge combines this identifier with reportDatetime for deduplication of eruption observations.
- **`report_datetime`** (datetime, required): Eruption report issue time converted from JMA local Japan Standard Time to UTC and serialized as an RFC3339 timestamp.
- **`report_datetime_local`** (datetime, required): Original JMA reportDatetime value in Japan Standard Time as published in eruption.json.
- **`eruption_datetime`** (datetime or null, optional): Observed eruption time converted to UTC when the eruption feed contains a structured eruption or observation datetime. The field is null when JMA publishes only report issue time or free text.
- **`eruption_datetime_local`** (datetime or null, optional): Observed eruption time in the original Japan Standard Time representation when present in a JMA eruption item. The field is null when the live payload does not expose a separate occurrence time.
- **`eruption_type`** (string or null, optional): Normalized phenomenon name from JMA eruption observation bulletins. JMA documentation says the report carries the phenomenon name, with examples including eruption and continuous-eruption state changes; null means the live JSON item did not expose a recognizable phenomenon name.
- **`crater_name`** (string or null, optional): Japanese crater name from the eruption observation report when JMA identifies the crater, such as 南岳山頂火口 in JMA bulletin examples. Null means the eruption JSON item or text did not include a crater label.
- **`colored_plume_height_m`** (double or null, optional, meter (m)): Height in metres of the colored volcanic plume above the crater, corresponding to the 有色噴煙 field in JMA eruption observation bulletins. Null means no colored-plume height was published or parsed.
- **`white_plume_height_m`** (double or null, optional, meter (m)): Height in metres of the white volcanic plume above the crater, corresponding to the 白色噴煙 field when JMA publishes it. Null means no white-plume height was published or parsed.
- **`maximum_plume_height_since_start_m`** (double or null, optional, meter (m)): Maximum plume height in metres above the crater since the eruption began, corresponding to the JMA bulletin field 噴火開始以降の最高噴煙高度. Null means JMA did not publish this field for the observation.
- **`plume_direction`** (string or null, optional): Japanese plume flow direction from the JMA 流向 field, for example 直上 or 東. Null means the eruption item did not provide a plume direction.
- **`ash_dispersal_direction`** (string or null, optional): Direction or area text for ash dispersal when the eruption observation describes ash movement separately from the plume-flow direction. Null means JMA did not publish a separate ash dispersal direction in the parsed item.
- **`pyroclastic_flow_observed`** (boolean or null, optional): True when the eruption observation text states that a pyroclastic flow (火砕流) was observed, false when the text explicitly states no pyroclastic flow, and null when the report does not mention pyroclastic-flow status.
- **`plume_amount_jp`** (string or null, optional): Japanese qualitative plume-amount label from JMA bulletin text, such as やや多量. Null means the observation did not include a plume-amount label.
- **`description`** (string, required): Japanese free-text description assembled from the JMA eruption item fields such as description, text, name, title, or content. This preserves the official observational wording when the eruption feed carries discrete eruption observations.
- **`info_type_jp`** (string or null, optional): Japanese volcanoInfos section type from eruption.json when supplied by JMA. It identifies the official section in which the eruption observation was published.
- **`area_codes`** (array of string, required): List of JMA municipal or regional area codes from the outer areas field of the Bosai volcano report. JMA uses these area identifiers to indicate municipalities or regions affected by the volcanic warning or eruption information.
- **`prefecture`** (string, required): ASCII-safe Japanese prefecture or region slug used as a MQTT and AMQP routing axis. The bridge derives this from JMA station/volcano metadata when available, otherwise emits unknown. Constraints: pattern `^[a-z0-9][a-z0-9-]*$`.
- **`event`** (enum, required): Fixed topic event segment for VolcanicEruption messages.
##### `eruption_type` values

- `ERUPTION`: Provider value `ERUPTION` for this coded alert field.
- `EXPLOSION`: Provider value `EXPLOSION` for this coded alert field.
- `CONTINUOUS_ERUPTION_CONTINUING`: Provider value `CONTINUOUS_ERUPTION_CONTINUING` for this coded alert field.
- `CONTINUOUS_ERUPTION_STOPPED`: Provider value `CONTINUOUS_ERUPTION_STOPPED` for this coded alert field.
- `UNKNOWN`: Provider value `UNKNOWN` for this coded alert field.
##### `event` values

- `eruption`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "volcano_code": "string",
  "event_id": "string",
  "report_datetime": "2024-01-01T00:00:00Z",
  "report_datetime_local": "2024-01-01T00:00:00Z",
  "eruption_datetime": "2024-01-01T00:00:00Z",
  "eruption_datetime_local": "2024-01-01T00:00:00Z",
  "eruption_type": "ERUPTION",
  "crater_name": "string",
  "colored_plume_height_m": 0,
  "white_plume_height_m": 0,
  "maximum_plume_height_since_start_m": 0,
  "plume_direction": "string",
  "ash_dispersal_direction": "string",
  "pyroclastic_flow_observed": false,
  "plume_amount_jp": "string",
  "description": "string",
  "info_type_jp": "string",
  "area_codes": [
    "string"
  ],
  "prefecture": "string",
  "event": "eruption"
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

- xRegistry manifest: [`xreg/jma-bosai-volcano.xreg.json`](xreg/jma-bosai-volcano.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
