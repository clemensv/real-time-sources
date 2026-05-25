# EAWS ALBINA Avalanche Bulletin Bridge Events

MQTT/5.0 transport variant for EAWS ALBINA avalanche bulletins. Non-retained QoS-1 bulletin events route by country, region, and danger level under alerts/at/eaws/eaws-albina/...

## At a glance

- **Event types:** 2 documented event types (3 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0
- **Reference vs telemetry:** 0 reference/catalog event types and 2 telemetry event types.
- **Identity:** `{region_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `eaws-albina`. The record key is `{region_id}`. In plain language, `{region_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['eaws-albina'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `alerts/at/eaws/eaws-albina/+/+/+/bulletin`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('alerts/at/eaws/eaws-albina/+/+/+/bulletin', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.

## Event catalog

### Avalanche Region

CloudEvents type: `org.EAWS.ALBINA.AvalancheRegion`

#### What it tells you

Reference event describing an EAWS region (or super-region) that the bridge is configured to observe. Emitted at bridge startup and whenever the configured region set changes. Acts as the catalog backbone for downstream consumers, ensuring the regional context is available even outside the avalanche season when no bulletins are being published.

#### Identity

Each event identifies the real-world resource with `{region_id}`. `{region_id}` is EAWS region identifier (country prefix plus warning service code), e.g. AT-07 for Tirol, IT-32-BZ for South Tyrol. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `eaws-albina`, key `{region_id}` |

#### Payload

`Avalanche Region` payloads are JSON object. Required fields: `region_id`, `lang`, `configured_at`.

- **`region_id`** (string, required): EAWS region identifier (country prefix plus warning service code), e.g. AT-07 for Tirol, IT-32-BZ for South Tyrol. Matches the regionID used in CAAMLv6 bulletins.
- **`lang`** (string, required): ISO 639-1 language code used by the bridge when requesting bulletins for this region (de, en, it, fr, etc.).
- **`configured_at`** (datetime, required): ISO 8601 UTC timestamp when this region was registered in the bridge configuration. Updated whenever the bridge starts and re-emits its catalog.
- **`bulletin_base_url`** (string or null, optional): Base URL used by the bridge to fetch CAAMLv6 bulletins for this region (typically https://avalanche.report/albina_files). Null when not provided.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "region_id": "string",
  "lang": "string",
  "configured_at": "2024-01-01T00:00:00Z",
  "bulletin_base_url": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Avalanche Bulletin

CloudEvents type: `org.EAWS.ALBINA.AvalancheBulletin`

#### What it tells you

This event carries avalanche bulletin data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{region_id}`. `{region_id}` is EAWS micro-region identifier from the CAAMLv6 regions array, e.g. AT-07-04-02 for Karwendel Mountains East. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `eaws-albina`, key `{region_id}` |
| `MQTT/5.0` | topic `alerts/at/eaws/eaws-albina/{country}/{region_id}/{danger_level}/bulletin`, retain `false`, QoS `1` |

#### Payload

`Avalanche Bulletin` payloads are JSON object. Required fields: `region_id`, `region_name`, `bulletin_id`, `publication_time`, `valid_time_start`, `valid_time_end`, `lang`, `danger_ratings_json`, `avalanche_problems_json`, `country`, `danger_level`.

- **`region_id`** (string, required): EAWS micro-region identifier from the CAAMLv6 regions array, e.g. AT-07-04-02 for Karwendel Mountains East.
- **`region_name`** (string, required): Human-readable name of the EAWS micro-region, e.g. 'Karwendel Mountains East'.
- **`bulletin_id`** (string, required): Unique UUID assigned to this bulletin by the ALBINA system, from the CAAMLv6 bulletinID field.
- **`publication_time`** (datetime, required): ISO 8601 timestamp when this bulletin was published by the avalanche warning service.
- **`valid_time_start`** (datetime, required): ISO 8601 start of the validity period for this bulletin.
- **`valid_time_end`** (datetime, required): ISO 8601 end of the validity period for this bulletin.
- **`lang`** (string, required): ISO 639-1 language code of the bulletin text, e.g. 'en', 'de', 'it'.
- **`max_danger_rating`** (string or null, optional): Highest EAWS danger rating across all elevation bands and time periods in this bulletin. One of: low, moderate, considerable, high, very_high, or null if no ratings are present.
- **`max_danger_rating_value`** (int32 or null, optional): Numeric value (1-5) of the highest EAWS danger rating: 1=low, 2=moderate, 3=considerable, 4=high, 5=very_high. Null if no ratings are present.
- **`danger_ratings_json`** (string, required): JSON-encoded array of CAAMLv6 dangerRatings objects, each with mainValue (string), optional elevation (object with upperBound/lowerBound), and validTimePeriod (string: all_day, earlier, later).
- **`avalanche_problems_json`** (string, required): JSON-encoded array of CAAMLv6 avalancheProblems objects, each with problemType (e.g. wet_snow, persistent_weak_layers, wind_slab, new_snow, gliding_snow), snowpackStability, frequency, avalancheSize (1-5), aspects array, and optional elevation bounds.
- **`tendency_type`** (string or null, optional): Overall tendency of avalanche danger from the first tendency entry: decreasing, steady, or increasing. Null if no tendency data is present.
- **`danger_patterns_json`** (string or null, optional): JSON-encoded array of LWD Tyrol danger pattern codes from customData.LWD_Tyrol.dangerPatterns, e.g. ["DP10","DP4"]. Null if not present (non-Tyrol regions).
- **`avalanche_activity_highlights`** (string or null, optional): Summary of current avalanche activity conditions from avalancheActivity.highlights. May contain HTML markup. Null if not provided.
- **`snowpack_structure_comment`** (string or null, optional): Description of current snowpack structure and layering from snowpackStructure.comment. May contain HTML markup. Null if not provided.
- **`country`** (string, required): Lowercase ISO 3166-1 alpha-2 country code derived from the CAAML region_id prefix, e.g. at or it.
- **`danger_level`** (string, required): Topic-safe EAWS danger level derived from the highest danger rating, or 'unknown' when no rating is present.
##### `max_danger_rating` values

- `low`
- `moderate`
- `considerable`
- `high`
- `very_high`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "region_id": "string",
  "region_name": "string",
  "bulletin_id": "string",
  "publication_time": "2024-01-01T00:00:00Z",
  "valid_time_start": "2024-01-01T00:00:00Z",
  "valid_time_end": "2024-01-01T00:00:00Z",
  "lang": "string",
  "max_danger_rating": "low",
  "max_danger_rating_value": 0,
  "danger_ratings_json": "string",
  "avalanche_problems_json": "string",
  "tendency_type": "string",
  "danger_patterns_json": "string",
  "avalanche_activity_highlights": "string",
  "snowpack_structure_comment": "string",
  "country": "string",
  "danger_level": "string"
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

- xRegistry manifest: [`xreg/eaws_albina.xreg.json`](xreg/eaws_albina.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
