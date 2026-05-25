# JMA Bosai Volcanic Warnings and Eruptions Events

This source bridges the Japan Meteorological Agency (JMA) Bosai volcano feeds to Kafka-compatible endpoints as structured CloudEvents. It polls public, unauthenticated JMA endpoints for active volcanic warnings, eruption observations, and the volcano reference catalog.

## At a glance

- **Event types:** 3 documented event types.
- **Transports:** KAFKA
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

## Event catalog

### Volcano

CloudEvents type: `JP.JMA.Volcano.Volcano`

#### What it tells you

JMA Bosai volcano catalog reference data emitted at startup and on monthly refresh. Reference record for one volcano in the JMA Bosai volcano catalog. JMA publishes the catalog to provide volcano names, coordinates, and whether the five-level eruption alert system operates for that volcano.

#### Identity

Each event identifies the real-world resource with `jp.jma.volcano/{volcano_code}`. `{volcano_code}` is three-digit JMA volcano identifier used in the Bosai volcanic warning feeds and the volcano catalog. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `jma-bosai-volcano`, key `jp.jma.volcano/{volcano_code}` |

#### Payload

`Volcano` payloads are JSON object. Required fields: `volcano_code`, `name_jp`, `name_en`, `latitude`, `longitude`, `level_operation`.

- **`volcano_code`** (string, required): Three-digit JMA volcano identifier used in the Bosai volcanic warning feeds and the volcano catalog. This is the stable domain key for the volcano and is used in the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{3}$`.
- **`name_jp`** (string, required): Japanese volcano name from the JMA Bosai volcano catalog. This is a display label and is not used as the stable identity because JMA warning records key volcanoes by code.
- **`name_en`** (string, required): English volcano name from the JMA Bosai volcano catalog, used as a display label for international consumers.
- **`latitude`** (double, required, degree (°)): Latitude of the volcano in WGS84 decimal degrees. The bridge converts JMA degree-and-minute coordinates when present, and otherwise forwards the Bosai catalog decimal latitude.
- **`longitude`** (double, required, degree (°)): Longitude of the volcano in WGS84 decimal degrees. The bridge converts JMA degree-and-minute coordinates when present, and otherwise forwards the Bosai catalog decimal longitude.
- **`elevation_m`** (double or null, optional, meter (m)): Volcano summit elevation in metres when supplied by the JMA catalog. Some Bosai catalog entries omit elevation, so the field is null in emitted events when JMA does not provide the value.
- **`level_operation`** (boolean, required): True when JMA marks the volcano as operating under the five-level eruption alert system. False means the volcano is represented by binary issued/not-issued volcanic warnings rather than a local five-level evacuation framework.
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
  "level_operation": false
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Volcanic Warning

CloudEvents type: `JP.JMA.Volcano.VolcanicWarning`

#### What it tells you

JMA Bosai active volcanic warning or forecast for a target volcano. Active JMA Bosai volcanic warning or forecast for the target volcano. JMA eruption alert levels express the volcanic activity state, area needing caution, and expected disaster-prevention actions.

#### Identity

Each event identifies the real-world resource with `jp.jma.volcano/{volcano_code}`. `{volcano_code}` is three-digit JMA volcano identifier used in the Bosai volcanic warning feeds and the volcano catalog. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `jma-bosai-volcano`, key `jp.jma.volcano/{volcano_code}` |

#### Payload

`Volcanic Warning` payloads are JSON object. Required fields: `volcano_code`, `event_id`, `report_datetime`, `report_datetime_local`, `alert_level_code`, `alert_level_name`, `condition`, `info_type_jp`, `area_codes`.

- **`volcano_code`** (string, required): Three-digit JMA volcano identifier used in the Bosai volcanic warning feeds and the volcano catalog. This is the stable domain key for the volcano and is used in the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{3}$`.
- **`event_id`** (string, required): JMA eventId from the Bosai warning record. The warning feed uses this identifier with reportDatetime to identify the active report for a target volcano.
- **`report_datetime`** (datetime, required): Report issue time converted from JMA local Japan Standard Time to UTC and serialized as an RFC3339 timestamp. This is the normalized time used for cross-region analytics.
- **`report_datetime_local`** (datetime, required): Original JMA reportDatetime value in Japan Standard Time as published by the Bosai warning feed. Keeping the local timestamp preserves the official bulletin time shown by JMA.
- **`alert_level_code`** (enum, required): JMA volcanic warning code from warning.json. Enum symbols CODE_02, CODE_03, CODE_04, CODE_11, CODE_12, CODE_13, CODE_22, CODE_23, CODE_36, CODE_43, CODE_44, CODE_45, and CODE_49 correspond via altenums.json to observed live JMA wire codes 02, 03, 04, 11, 12, 13, 22, 23, 36, 43, 44, 45, and 49. JMA explains eruption alert levels as indicators combining volcanic activity state, area requiring caution, and expected disaster-prevention actions. Labels for CODE_11/CODE_12/CODE_13 are from JMA eruption alert level guidance; CODE_22/CODE_23/CODE_36 are target-volcano warning labels observed in live warning.json; CODE_02/CODE_03/CODE_04/CODE_43/CODE_44/CODE_45/CODE_49 labels are taken from live warning.json item name fields because the Bosai JSON feed publishes those public JMA labels directly.
- **`alert_level_name`** (string, required): Japanese alert level or warning label from the target-volcano item, such as レベル３（入山規制）. JMA uses this text to communicate the public-facing warning level or restriction phrase.
- **`previous_level_code`** (string or null, optional): Previous JMA alert level or warning code from lastCode when the warning feed provides one. It allows consumers to determine whether the current report raised, lowered, continued, or newly issued a level.
- **`condition`** (enum, required): Normalized lifecycle condition derived from the Japanese JMA condition text. 発表 is mapped to ISSUED, 引上げ to RAISED, 引下げ to LOWERED, 継続 to CONTINUED, 切替 to SWITCHED, and 解除 to CANCELLED so downstream consumers can compare reports without parsing Japanese status labels.
- **`info_type_jp`** (string, required): Japanese volcanoInfos type label from the JMA feed. For emitted warning events the bridge uses the target-volcano section, normally 噴火警報・予報（対象火山）, because that section carries the stable volcano code identity.
- **`area_codes`** (array of string, required): List of JMA municipal or regional area codes from the outer areas field of the Bosai volcano report. JMA uses these area identifiers to indicate municipalities or regions affected by the volcanic warning or eruption information.
##### `alert_level_code` values

- `CODE_02` — Crater-area warning
- `CODE_03` — Eruption warning for surrounding sea area
- `CODE_04` — Eruption forecast: warning lifted
- `CODE_11` — Active volcano; pay attention
- `CODE_12` — Crater area restriction
- `CODE_13` — Mountain access restriction
- `CODE_22` — Crater vicinity danger
- `CODE_23` — Mountain access danger
- `CODE_36` — Surrounding waters warning for submarine or island volcanoes
- `CODE_43` — Crater-area warning: entry restrictions and similar measures
- `CODE_44` — Eruption warning for surrounding sea area: surrounding sea area warning
- `CODE_45` — Active volcano; pay attention
- `CODE_49` — Crater-area warning: caution around the crater
##### `condition` values

- `ISSUED`
- `RAISED`
- `LOWERED`
- `CONTINUED`
- `SWITCHED`
- `CANCELLED`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "volcano_code": "string",
  "event_id": "string",
  "report_datetime": "2024-01-01T00:00:00Z",
  "report_datetime_local": "2024-01-01T00:00:00Z",
  "alert_level_code": "CODE_02",
  "alert_level_name": "string",
  "previous_level_code": "string",
  "condition": "ISSUED",
  "info_type_jp": "string",
  "area_codes": [
    "string"
  ]
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Volcanic Eruption

CloudEvents type: `JP.JMA.Volcano.VolcanicEruption`

#### What it tells you

JMA Bosai volcanic eruption observation report for a target volcano. Discrete JMA Bosai volcanic eruption observation report for a target volcano. The live eruption.json endpoint was empty when reviewed, so structured eruption observation fields are based on JMA documentation for 噴火に関する火山観測報, which states that reports include eruption occurrence time, plume height, plume direction, and volcanic phenomena observed with the eruption; field names also align with observed JMA HTML bulletin examples.

#### Identity

Each event identifies the real-world resource with `jp.jma.volcano/{volcano_code}`. `{volcano_code}` is three-digit JMA volcano identifier used in the Bosai volcanic warning feeds and the volcano catalog. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `jma-bosai-volcano`, key `jp.jma.volcano/{volcano_code}` |

#### Payload

`Volcanic Eruption` payloads are JSON object. Required fields: `volcano_code`, `event_id`, `report_datetime`, `report_datetime_local`, `description`, `area_codes`.

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
##### `eruption_type` values

- `ERUPTION`
- `EXPLOSION`
- `CONTINUOUS_ERUPTION_CONTINUING`
- `CONTINUOUS_ERUPTION_STOPPED`
- `UNKNOWN`
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
  ]
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
