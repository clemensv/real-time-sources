# German Autobahn Traffic Bridge Events

MQTT/5.0 mirror of the DE.Autobahn CloudEvents, published into the Unified-Namespace topic tree 'traffic/de/autobahn/autobahn/{road}/{kind}/{identifier}/{state}'. {kind} (10 values) and {state} (appeared/updated/resolved) are literally baked per-message so xrcg can resolve every placeholder from schema fields. Lifecycle-event families (roadwork, short-term-roadwork, closure, entry-exit-closure, warning) are QoS-1 non-retained — they are state-change notifications, not LKV slots. Stable-object families (weight-limit-3-5, webcam, parking-lorry, electric-charging-station, strong-electric-charging-station) are QoS-1 retained so late subscribers see the current state of every known object; the bridge publishes an empty retained payload on `resolved` to clear the slot.

## At a glance

- **Event types:** 30 documented event types (60 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0
- **Reference vs telemetry:** 6 reference/catalog event types and 24 telemetry event types.
- **Identity:** `{identifier}` identifies the resource each event is about.
- **Operations:** The bridge documentation mentions ETag-aware polling, so consumers should expect unchanged upstream responses to be skipped.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `autobahn`. The record key is `{identifier}`. In plain language, `{identifier}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['autobahn'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `traffic/de/autobahn/autobahn/+/roadwork/+/appeared`, `traffic/de/autobahn/autobahn/+/roadwork/+/updated`, `traffic/de/autobahn/autobahn/+/roadwork/+/resolved`, `traffic/de/autobahn/autobahn/+/short-term-roadwork/+/appeared`, `traffic/de/autobahn/autobahn/+/short-term-roadwork/+/updated`, `traffic/de/autobahn/autobahn/+/short-term-roadwork/+/resolved`, `traffic/de/autobahn/autobahn/+/closure/+/appeared`, `traffic/de/autobahn/autobahn/+/closure/+/updated`, `traffic/de/autobahn/autobahn/+/closure/+/resolved`, `traffic/de/autobahn/autobahn/+/entry-exit-closure/+/appeared`, `traffic/de/autobahn/autobahn/+/entry-exit-closure/+/updated`, `traffic/de/autobahn/autobahn/+/entry-exit-closure/+/resolved`, `traffic/de/autobahn/autobahn/+/warning/+/appeared`, `traffic/de/autobahn/autobahn/+/warning/+/updated`, `traffic/de/autobahn/autobahn/+/warning/+/resolved`, `traffic/de/autobahn/autobahn/+/weight-limit-3-5/+/appeared`, `traffic/de/autobahn/autobahn/+/weight-limit-3-5/+/updated`, `traffic/de/autobahn/autobahn/+/weight-limit-3-5/+/resolved`, `traffic/de/autobahn/autobahn/+/webcam/+/appeared`, `traffic/de/autobahn/autobahn/+/webcam/+/updated`, `traffic/de/autobahn/autobahn/+/webcam/+/resolved`, `traffic/de/autobahn/autobahn/+/parking-lorry/+/appeared`, `traffic/de/autobahn/autobahn/+/parking-lorry/+/updated`, `traffic/de/autobahn/autobahn/+/parking-lorry/+/resolved`, `traffic/de/autobahn/autobahn/+/electric-charging-station/+/appeared`, `traffic/de/autobahn/autobahn/+/electric-charging-station/+/updated`, `traffic/de/autobahn/autobahn/+/electric-charging-station/+/resolved`, `traffic/de/autobahn/autobahn/+/strong-electric-charging-station/+/appeared`, `traffic/de/autobahn/autobahn/+/strong-electric-charging-station/+/updated`, `traffic/de/autobahn/autobahn/+/strong-electric-charging-station/+/resolved`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('traffic/de/autobahn/autobahn/+/roadwork/+/appeared', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.

## Event catalog

### Roadwork Appeared

CloudEvents type: `DE.Autobahn.RoadworkAppeared`

#### What it tells you

Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.

#### Identity

Each event identifies the real-world resource with `{identifier}`. `{identifier}` is stable Autobahn item identifier used for the CloudEvents subject and Kafka key. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `autobahn`, key `{identifier}` |
| `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/roadwork/{identifier}/appeared`, retain `false`, QoS `1` |

#### Payload

`Roadwork Appeared` payloads are JSON object. Required fields: `identifier`, `road`, `road_ids`, `event_time`, `display_type`.

- **`identifier`** (string, required): Stable Autobahn item identifier used for the CloudEvents subject and Kafka key.
- **`road`** (string, required): Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. Constraints: pattern `^[a-z0-9-]+$`.
- **`road_ids`** (array of string, required): Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families.
- **`event_time`** (datetime, required): CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp.
- **`display_type`** (enum, required): Autobahn API display_type value that identifies the road-event subtype.
- **`title`** (string or null, optional): Human-readable title from the Autobahn API item.
- **`subtitle`** (string or null, optional): Human-readable subtitle from the Autobahn API item.
- **`description_lines`** (array of string, optional): Description lines from the Autobahn API description array.
- **`future`** (boolean or null, optional): Whether the Autobahn API marks the item as a future event.
- **`is_blocked`** (boolean or null, optional): Whether the Autobahn API marks the affected road segment as blocked.
- **`icon`** (string or null, optional): Autobahn API icon identifier for the item.
- **`start_lc_position`** (integer or null, optional): Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment.
- **`start_timestamp`** (datetime or null, optional): startTimestamp value from the Autobahn API when the item includes a scheduled or known start time.
- **`extent`** (string or null, optional): Autobahn API extent text for the affected road segment.
- **`point`** (string or null, optional): Autobahn API point text that identifies the affected point on the road segment.
- **`coordinate_lat`** (double or null, optional): Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-90`, maximum `90`.
- **`coordinate_lon`** (double or null, optional): Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-180`, maximum `180`.
- **`geometry_json`** (string or null, optional): Serialized Autobahn API geometry object for the affected road segment.
- **`impact_lower`** (string or null, optional): Lower bound from the Autobahn API impact object.
- **`impact_upper`** (string or null, optional): Upper bound from the Autobahn API impact object.
- **`impact_symbols`** (array of string, optional): Impact symbols from the Autobahn API impact.symbols array.
- **`route_recommendation_json`** (string or null, optional): Serialized Autobahn API routeRecommendation object when rerouting advice is available.
- **`footer_lines`** (array of string, optional): Footer lines from the Autobahn API footer array.
##### `display_type` values

- `ROADWORKS`
- `SHORT_TERM_ROADWORKS`
- `CLOSURE`
- `CLOSURE_ENTRY_EXIT`
- `WEIGHT_LIMIT_35`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "identifier": "string",
  "road": "string",
  "road_ids": [
    "string"
  ],
  "event_time": "2024-01-01T00:00:00Z",
  "display_type": "ROADWORKS",
  "title": "string",
  "subtitle": "string",
  "description_lines": [
    "string"
  ],
  "future": false,
  "is_blocked": false,
  "icon": "string",
  "start_lc_position": 0,
  "start_timestamp": "2024-01-01T00:00:00Z",
  "extent": "string",
  "point": "string",
  "coordinate_lat": 0,
  "coordinate_lon": 0,
  "geometry_json": "string",
  "impact_lower": "string",
  "impact_upper": "string",
  "impact_symbols": [
    "string"
  ],
  "route_recommendation_json": "string",
  "footer_lines": [
    "string"
  ]
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Roadwork Updated

CloudEvents type: `DE.Autobahn.RoadworkUpdated`

#### What it tells you

Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.

#### Identity

Each event identifies the real-world resource with `{identifier}`. `{identifier}` is stable Autobahn item identifier used for the CloudEvents subject and Kafka key. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `autobahn`, key `{identifier}` |
| `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/roadwork/{identifier}/updated`, retain `false`, QoS `1` |

#### Payload

`Roadwork Updated` payloads are JSON object. Required fields: `identifier`, `road`, `road_ids`, `event_time`, `display_type`.

- **`identifier`** (string, required): Stable Autobahn item identifier used for the CloudEvents subject and Kafka key.
- **`road`** (string, required): Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. Constraints: pattern `^[a-z0-9-]+$`.
- **`road_ids`** (array of string, required): Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families.
- **`event_time`** (datetime, required): CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp.
- **`display_type`** (enum, required): Autobahn API display_type value that identifies the road-event subtype.
- **`title`** (string or null, optional): Human-readable title from the Autobahn API item.
- **`subtitle`** (string or null, optional): Human-readable subtitle from the Autobahn API item.
- **`description_lines`** (array of string, optional): Description lines from the Autobahn API description array.
- **`future`** (boolean or null, optional): Whether the Autobahn API marks the item as a future event.
- **`is_blocked`** (boolean or null, optional): Whether the Autobahn API marks the affected road segment as blocked.
- **`icon`** (string or null, optional): Autobahn API icon identifier for the item.
- **`start_lc_position`** (integer or null, optional): Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment.
- **`start_timestamp`** (datetime or null, optional): startTimestamp value from the Autobahn API when the item includes a scheduled or known start time.
- **`extent`** (string or null, optional): Autobahn API extent text for the affected road segment.
- **`point`** (string or null, optional): Autobahn API point text that identifies the affected point on the road segment.
- **`coordinate_lat`** (double or null, optional): Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-90`, maximum `90`.
- **`coordinate_lon`** (double or null, optional): Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-180`, maximum `180`.
- **`geometry_json`** (string or null, optional): Serialized Autobahn API geometry object for the affected road segment.
- **`impact_lower`** (string or null, optional): Lower bound from the Autobahn API impact object.
- **`impact_upper`** (string or null, optional): Upper bound from the Autobahn API impact object.
- **`impact_symbols`** (array of string, optional): Impact symbols from the Autobahn API impact.symbols array.
- **`route_recommendation_json`** (string or null, optional): Serialized Autobahn API routeRecommendation object when rerouting advice is available.
- **`footer_lines`** (array of string, optional): Footer lines from the Autobahn API footer array.
##### `display_type` values

- `ROADWORKS`
- `SHORT_TERM_ROADWORKS`
- `CLOSURE`
- `CLOSURE_ENTRY_EXIT`
- `WEIGHT_LIMIT_35`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "identifier": "string",
  "road": "string",
  "road_ids": [
    "string"
  ],
  "event_time": "2024-01-01T00:00:00Z",
  "display_type": "ROADWORKS",
  "title": "string",
  "subtitle": "string",
  "description_lines": [
    "string"
  ],
  "future": false,
  "is_blocked": false,
  "icon": "string",
  "start_lc_position": 0,
  "start_timestamp": "2024-01-01T00:00:00Z",
  "extent": "string",
  "point": "string",
  "coordinate_lat": 0,
  "coordinate_lon": 0,
  "geometry_json": "string",
  "impact_lower": "string",
  "impact_upper": "string",
  "impact_symbols": [
    "string"
  ],
  "route_recommendation_json": "string",
  "footer_lines": [
    "string"
  ]
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Roadwork Resolved

CloudEvents type: `DE.Autobahn.RoadworkResolved`

#### What it tells you

Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.

#### Identity

Each event identifies the real-world resource with `{identifier}`. `{identifier}` is stable Autobahn item identifier used for the CloudEvents subject and Kafka key. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `autobahn`, key `{identifier}` |
| `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/roadwork/{identifier}/resolved`, retain `false`, QoS `1` |

#### Payload

`Roadwork Resolved` payloads are JSON object. Required fields: `identifier`, `road`, `road_ids`, `event_time`, `display_type`.

- **`identifier`** (string, required): Stable Autobahn item identifier used for the CloudEvents subject and Kafka key.
- **`road`** (string, required): Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. Constraints: pattern `^[a-z0-9-]+$`.
- **`road_ids`** (array of string, required): Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families.
- **`event_time`** (datetime, required): CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp.
- **`display_type`** (enum, required): Autobahn API display_type value that identifies the road-event subtype.
- **`title`** (string or null, optional): Human-readable title from the Autobahn API item.
- **`subtitle`** (string or null, optional): Human-readable subtitle from the Autobahn API item.
- **`description_lines`** (array of string, optional): Description lines from the Autobahn API description array.
- **`future`** (boolean or null, optional): Whether the Autobahn API marks the item as a future event.
- **`is_blocked`** (boolean or null, optional): Whether the Autobahn API marks the affected road segment as blocked.
- **`icon`** (string or null, optional): Autobahn API icon identifier for the item.
- **`start_lc_position`** (integer or null, optional): Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment.
- **`start_timestamp`** (datetime or null, optional): startTimestamp value from the Autobahn API when the item includes a scheduled or known start time.
- **`extent`** (string or null, optional): Autobahn API extent text for the affected road segment.
- **`point`** (string or null, optional): Autobahn API point text that identifies the affected point on the road segment.
- **`coordinate_lat`** (double or null, optional): Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-90`, maximum `90`.
- **`coordinate_lon`** (double or null, optional): Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-180`, maximum `180`.
- **`geometry_json`** (string or null, optional): Serialized Autobahn API geometry object for the affected road segment.
- **`impact_lower`** (string or null, optional): Lower bound from the Autobahn API impact object.
- **`impact_upper`** (string or null, optional): Upper bound from the Autobahn API impact object.
- **`impact_symbols`** (array of string, optional): Impact symbols from the Autobahn API impact.symbols array.
- **`route_recommendation_json`** (string or null, optional): Serialized Autobahn API routeRecommendation object when rerouting advice is available.
- **`footer_lines`** (array of string, optional): Footer lines from the Autobahn API footer array.
##### `display_type` values

- `ROADWORKS`
- `SHORT_TERM_ROADWORKS`
- `CLOSURE`
- `CLOSURE_ENTRY_EXIT`
- `WEIGHT_LIMIT_35`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "identifier": "string",
  "road": "string",
  "road_ids": [
    "string"
  ],
  "event_time": "2024-01-01T00:00:00Z",
  "display_type": "ROADWORKS",
  "title": "string",
  "subtitle": "string",
  "description_lines": [
    "string"
  ],
  "future": false,
  "is_blocked": false,
  "icon": "string",
  "start_lc_position": 0,
  "start_timestamp": "2024-01-01T00:00:00Z",
  "extent": "string",
  "point": "string",
  "coordinate_lat": 0,
  "coordinate_lon": 0,
  "geometry_json": "string",
  "impact_lower": "string",
  "impact_upper": "string",
  "impact_symbols": [
    "string"
  ],
  "route_recommendation_json": "string",
  "footer_lines": [
    "string"
  ]
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Short Term Roadwork Appeared

CloudEvents type: `DE.Autobahn.ShortTermRoadworkAppeared`

#### What it tells you

Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.

#### Identity

Each event identifies the real-world resource with `{identifier}`. `{identifier}` is stable Autobahn item identifier used for the CloudEvents subject and Kafka key. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `autobahn`, key `{identifier}` |
| `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/short-term-roadwork/{identifier}/appeared`, retain `false`, QoS `1` |

#### Payload

`Short Term Roadwork Appeared` payloads are JSON object. Required fields: `identifier`, `road`, `road_ids`, `event_time`, `display_type`.

- **`identifier`** (string, required): Stable Autobahn item identifier used for the CloudEvents subject and Kafka key.
- **`road`** (string, required): Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. Constraints: pattern `^[a-z0-9-]+$`.
- **`road_ids`** (array of string, required): Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families.
- **`event_time`** (datetime, required): CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp.
- **`display_type`** (enum, required): Autobahn API display_type value that identifies the road-event subtype.
- **`title`** (string or null, optional): Human-readable title from the Autobahn API item.
- **`subtitle`** (string or null, optional): Human-readable subtitle from the Autobahn API item.
- **`description_lines`** (array of string, optional): Description lines from the Autobahn API description array.
- **`future`** (boolean or null, optional): Whether the Autobahn API marks the item as a future event.
- **`is_blocked`** (boolean or null, optional): Whether the Autobahn API marks the affected road segment as blocked.
- **`icon`** (string or null, optional): Autobahn API icon identifier for the item.
- **`start_lc_position`** (integer or null, optional): Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment.
- **`start_timestamp`** (datetime or null, optional): startTimestamp value from the Autobahn API when the item includes a scheduled or known start time.
- **`extent`** (string or null, optional): Autobahn API extent text for the affected road segment.
- **`point`** (string or null, optional): Autobahn API point text that identifies the affected point on the road segment.
- **`coordinate_lat`** (double or null, optional): Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-90`, maximum `90`.
- **`coordinate_lon`** (double or null, optional): Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-180`, maximum `180`.
- **`geometry_json`** (string or null, optional): Serialized Autobahn API geometry object for the affected road segment.
- **`impact_lower`** (string or null, optional): Lower bound from the Autobahn API impact object.
- **`impact_upper`** (string or null, optional): Upper bound from the Autobahn API impact object.
- **`impact_symbols`** (array of string, optional): Impact symbols from the Autobahn API impact.symbols array.
- **`route_recommendation_json`** (string or null, optional): Serialized Autobahn API routeRecommendation object when rerouting advice is available.
- **`footer_lines`** (array of string, optional): Footer lines from the Autobahn API footer array.
##### `display_type` values

- `ROADWORKS`
- `SHORT_TERM_ROADWORKS`
- `CLOSURE`
- `CLOSURE_ENTRY_EXIT`
- `WEIGHT_LIMIT_35`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "identifier": "string",
  "road": "string",
  "road_ids": [
    "string"
  ],
  "event_time": "2024-01-01T00:00:00Z",
  "display_type": "ROADWORKS",
  "title": "string",
  "subtitle": "string",
  "description_lines": [
    "string"
  ],
  "future": false,
  "is_blocked": false,
  "icon": "string",
  "start_lc_position": 0,
  "start_timestamp": "2024-01-01T00:00:00Z",
  "extent": "string",
  "point": "string",
  "coordinate_lat": 0,
  "coordinate_lon": 0,
  "geometry_json": "string",
  "impact_lower": "string",
  "impact_upper": "string",
  "impact_symbols": [
    "string"
  ],
  "route_recommendation_json": "string",
  "footer_lines": [
    "string"
  ]
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Short Term Roadwork Updated

CloudEvents type: `DE.Autobahn.ShortTermRoadworkUpdated`

#### What it tells you

Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.

#### Identity

Each event identifies the real-world resource with `{identifier}`. `{identifier}` is stable Autobahn item identifier used for the CloudEvents subject and Kafka key. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `autobahn`, key `{identifier}` |
| `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/short-term-roadwork/{identifier}/updated`, retain `false`, QoS `1` |

#### Payload

`Short Term Roadwork Updated` payloads are JSON object. Required fields: `identifier`, `road`, `road_ids`, `event_time`, `display_type`.

- **`identifier`** (string, required): Stable Autobahn item identifier used for the CloudEvents subject and Kafka key.
- **`road`** (string, required): Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. Constraints: pattern `^[a-z0-9-]+$`.
- **`road_ids`** (array of string, required): Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families.
- **`event_time`** (datetime, required): CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp.
- **`display_type`** (enum, required): Autobahn API display_type value that identifies the road-event subtype.
- **`title`** (string or null, optional): Human-readable title from the Autobahn API item.
- **`subtitle`** (string or null, optional): Human-readable subtitle from the Autobahn API item.
- **`description_lines`** (array of string, optional): Description lines from the Autobahn API description array.
- **`future`** (boolean or null, optional): Whether the Autobahn API marks the item as a future event.
- **`is_blocked`** (boolean or null, optional): Whether the Autobahn API marks the affected road segment as blocked.
- **`icon`** (string or null, optional): Autobahn API icon identifier for the item.
- **`start_lc_position`** (integer or null, optional): Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment.
- **`start_timestamp`** (datetime or null, optional): startTimestamp value from the Autobahn API when the item includes a scheduled or known start time.
- **`extent`** (string or null, optional): Autobahn API extent text for the affected road segment.
- **`point`** (string or null, optional): Autobahn API point text that identifies the affected point on the road segment.
- **`coordinate_lat`** (double or null, optional): Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-90`, maximum `90`.
- **`coordinate_lon`** (double or null, optional): Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-180`, maximum `180`.
- **`geometry_json`** (string or null, optional): Serialized Autobahn API geometry object for the affected road segment.
- **`impact_lower`** (string or null, optional): Lower bound from the Autobahn API impact object.
- **`impact_upper`** (string or null, optional): Upper bound from the Autobahn API impact object.
- **`impact_symbols`** (array of string, optional): Impact symbols from the Autobahn API impact.symbols array.
- **`route_recommendation_json`** (string or null, optional): Serialized Autobahn API routeRecommendation object when rerouting advice is available.
- **`footer_lines`** (array of string, optional): Footer lines from the Autobahn API footer array.
##### `display_type` values

- `ROADWORKS`
- `SHORT_TERM_ROADWORKS`
- `CLOSURE`
- `CLOSURE_ENTRY_EXIT`
- `WEIGHT_LIMIT_35`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "identifier": "string",
  "road": "string",
  "road_ids": [
    "string"
  ],
  "event_time": "2024-01-01T00:00:00Z",
  "display_type": "ROADWORKS",
  "title": "string",
  "subtitle": "string",
  "description_lines": [
    "string"
  ],
  "future": false,
  "is_blocked": false,
  "icon": "string",
  "start_lc_position": 0,
  "start_timestamp": "2024-01-01T00:00:00Z",
  "extent": "string",
  "point": "string",
  "coordinate_lat": 0,
  "coordinate_lon": 0,
  "geometry_json": "string",
  "impact_lower": "string",
  "impact_upper": "string",
  "impact_symbols": [
    "string"
  ],
  "route_recommendation_json": "string",
  "footer_lines": [
    "string"
  ]
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Short Term Roadwork Resolved

CloudEvents type: `DE.Autobahn.ShortTermRoadworkResolved`

#### What it tells you

Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.

#### Identity

Each event identifies the real-world resource with `{identifier}`. `{identifier}` is stable Autobahn item identifier used for the CloudEvents subject and Kafka key. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `autobahn`, key `{identifier}` |
| `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/short-term-roadwork/{identifier}/resolved`, retain `false`, QoS `1` |

#### Payload

`Short Term Roadwork Resolved` payloads are JSON object. Required fields: `identifier`, `road`, `road_ids`, `event_time`, `display_type`.

- **`identifier`** (string, required): Stable Autobahn item identifier used for the CloudEvents subject and Kafka key.
- **`road`** (string, required): Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. Constraints: pattern `^[a-z0-9-]+$`.
- **`road_ids`** (array of string, required): Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families.
- **`event_time`** (datetime, required): CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp.
- **`display_type`** (enum, required): Autobahn API display_type value that identifies the road-event subtype.
- **`title`** (string or null, optional): Human-readable title from the Autobahn API item.
- **`subtitle`** (string or null, optional): Human-readable subtitle from the Autobahn API item.
- **`description_lines`** (array of string, optional): Description lines from the Autobahn API description array.
- **`future`** (boolean or null, optional): Whether the Autobahn API marks the item as a future event.
- **`is_blocked`** (boolean or null, optional): Whether the Autobahn API marks the affected road segment as blocked.
- **`icon`** (string or null, optional): Autobahn API icon identifier for the item.
- **`start_lc_position`** (integer or null, optional): Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment.
- **`start_timestamp`** (datetime or null, optional): startTimestamp value from the Autobahn API when the item includes a scheduled or known start time.
- **`extent`** (string or null, optional): Autobahn API extent text for the affected road segment.
- **`point`** (string or null, optional): Autobahn API point text that identifies the affected point on the road segment.
- **`coordinate_lat`** (double or null, optional): Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-90`, maximum `90`.
- **`coordinate_lon`** (double or null, optional): Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-180`, maximum `180`.
- **`geometry_json`** (string or null, optional): Serialized Autobahn API geometry object for the affected road segment.
- **`impact_lower`** (string or null, optional): Lower bound from the Autobahn API impact object.
- **`impact_upper`** (string or null, optional): Upper bound from the Autobahn API impact object.
- **`impact_symbols`** (array of string, optional): Impact symbols from the Autobahn API impact.symbols array.
- **`route_recommendation_json`** (string or null, optional): Serialized Autobahn API routeRecommendation object when rerouting advice is available.
- **`footer_lines`** (array of string, optional): Footer lines from the Autobahn API footer array.
##### `display_type` values

- `ROADWORKS`
- `SHORT_TERM_ROADWORKS`
- `CLOSURE`
- `CLOSURE_ENTRY_EXIT`
- `WEIGHT_LIMIT_35`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "identifier": "string",
  "road": "string",
  "road_ids": [
    "string"
  ],
  "event_time": "2024-01-01T00:00:00Z",
  "display_type": "ROADWORKS",
  "title": "string",
  "subtitle": "string",
  "description_lines": [
    "string"
  ],
  "future": false,
  "is_blocked": false,
  "icon": "string",
  "start_lc_position": 0,
  "start_timestamp": "2024-01-01T00:00:00Z",
  "extent": "string",
  "point": "string",
  "coordinate_lat": 0,
  "coordinate_lon": 0,
  "geometry_json": "string",
  "impact_lower": "string",
  "impact_upper": "string",
  "impact_symbols": [
    "string"
  ],
  "route_recommendation_json": "string",
  "footer_lines": [
    "string"
  ]
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Warning Appeared

CloudEvents type: `DE.Autobahn.WarningAppeared`

#### What it tells you

Normalized Autobahn warning payload with delay and traffic source details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/warning.

#### Identity

Each event identifies the real-world resource with `{identifier}`. `{identifier}` is stable Autobahn warning identifier used for the CloudEvents subject and Kafka key. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `autobahn`, key `{identifier}` |
| `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/warning/{identifier}/appeared`, retain `false`, QoS `1` |

#### Payload

`Warning Appeared` payloads are JSON object. Required fields: `identifier`, `road`, `road_ids`, `event_time`, `display_type`.

- **`identifier`** (string, required): Stable Autobahn warning identifier used for the CloudEvents subject and Kafka key.
- **`road`** (string, required): Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. Constraints: pattern `^[a-z0-9-]+$`.
- **`road_ids`** (array of string, required): Autobahn road identifiers for the road query that yielded this warning item.
- **`event_time`** (datetime, required): CloudEvents event time for the emitted warning record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp.
- **`display_type`** (enum, required): Autobahn API display_type for warning items.
- **`title`** (string or null, optional): Human-readable title from the Autobahn API warning item.
- **`subtitle`** (string or null, optional): Human-readable subtitle from the Autobahn API warning item.
- **`description_lines`** (array of string, optional): Description lines from the Autobahn API description array.
- **`future`** (boolean or null, optional): Whether the Autobahn API marks the warning as a future event.
- **`is_blocked`** (boolean or null, optional): Whether the Autobahn API marks the warning segment as blocked.
- **`icon`** (string or null, optional): Autobahn API icon identifier for the warning item.
- **`start_lc_position`** (integer or null, optional): Numeric startLcPosition value emitted by the Autobahn API for the beginning of the warning segment.
- **`start_timestamp`** (datetime or null, optional): startTimestamp value from the Autobahn API when the warning includes a scheduled or known start time.
- **`extent`** (string or null, optional): Autobahn API extent text for the affected road segment.
- **`point`** (string or null, optional): Autobahn API point text that identifies the affected point on the road segment.
- **`coordinate_lat`** (double or null, optional): Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-90`, maximum `90`.
- **`coordinate_lon`** (double or null, optional): Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-180`, maximum `180`.
- **`geometry_json`** (string or null, optional): Serialized Autobahn API geometry object for the affected road segment.
- **`impact_lower`** (string or null, optional): Lower bound from the Autobahn API impact object.
- **`impact_upper`** (string or null, optional): Upper bound from the Autobahn API impact object.
- **`impact_symbols`** (array of string, optional): Impact symbols from the Autobahn API impact.symbols array.
- **`route_recommendation_json`** (string or null, optional): Serialized Autobahn API routeRecommendation object when rerouting advice is available.
- **`footer_lines`** (array of string, optional): Footer lines from the Autobahn API footer array.
- **`delay_minutes`** (integer or null, optional, min): delayTimeValue from the Autobahn warning item, expressed in minutes. Constraints: minimum `0`.
- **`average_speed_kmh`** (integer or null, optional, km/h): averageSpeed from the Autobahn warning item, expressed in kilometers per hour. Constraints: minimum `0`.
- **`abnormal_traffic_type`** (string or null, optional): abnormalTrafficType code from the Autobahn warning item.
- **`source_name`** (string or null, optional): source value from the Autobahn warning item that identifies the origin of the warning.
##### `display_type` values

- `WARNING`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "identifier": "string",
  "road": "string",
  "road_ids": [
    "string"
  ],
  "event_time": "2024-01-01T00:00:00Z",
  "display_type": "WARNING",
  "title": "string",
  "subtitle": "string",
  "description_lines": [
    "string"
  ],
  "future": false,
  "is_blocked": false,
  "icon": "string",
  "start_lc_position": 0,
  "start_timestamp": "2024-01-01T00:00:00Z",
  "extent": "string",
  "point": "string",
  "coordinate_lat": 0,
  "coordinate_lon": 0,
  "geometry_json": "string",
  "impact_lower": "string",
  "impact_upper": "string",
  "impact_symbols": [
    "string"
  ],
  "route_recommendation_json": "string",
  "footer_lines": [
    "string"
  ],
  "delay_minutes": 0,
  "average_speed_kmh": 0,
  "abnormal_traffic_type": "string",
  "source_name": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Warning Updated

CloudEvents type: `DE.Autobahn.WarningUpdated`

#### What it tells you

Normalized Autobahn warning payload with delay and traffic source details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/warning.

#### Identity

Each event identifies the real-world resource with `{identifier}`. `{identifier}` is stable Autobahn warning identifier used for the CloudEvents subject and Kafka key. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `autobahn`, key `{identifier}` |
| `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/warning/{identifier}/updated`, retain `false`, QoS `1` |

#### Payload

`Warning Updated` payloads are JSON object. Required fields: `identifier`, `road`, `road_ids`, `event_time`, `display_type`.

- **`identifier`** (string, required): Stable Autobahn warning identifier used for the CloudEvents subject and Kafka key.
- **`road`** (string, required): Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. Constraints: pattern `^[a-z0-9-]+$`.
- **`road_ids`** (array of string, required): Autobahn road identifiers for the road query that yielded this warning item.
- **`event_time`** (datetime, required): CloudEvents event time for the emitted warning record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp.
- **`display_type`** (enum, required): Autobahn API display_type for warning items.
- **`title`** (string or null, optional): Human-readable title from the Autobahn API warning item.
- **`subtitle`** (string or null, optional): Human-readable subtitle from the Autobahn API warning item.
- **`description_lines`** (array of string, optional): Description lines from the Autobahn API description array.
- **`future`** (boolean or null, optional): Whether the Autobahn API marks the warning as a future event.
- **`is_blocked`** (boolean or null, optional): Whether the Autobahn API marks the warning segment as blocked.
- **`icon`** (string or null, optional): Autobahn API icon identifier for the warning item.
- **`start_lc_position`** (integer or null, optional): Numeric startLcPosition value emitted by the Autobahn API for the beginning of the warning segment.
- **`start_timestamp`** (datetime or null, optional): startTimestamp value from the Autobahn API when the warning includes a scheduled or known start time.
- **`extent`** (string or null, optional): Autobahn API extent text for the affected road segment.
- **`point`** (string or null, optional): Autobahn API point text that identifies the affected point on the road segment.
- **`coordinate_lat`** (double or null, optional): Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-90`, maximum `90`.
- **`coordinate_lon`** (double or null, optional): Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-180`, maximum `180`.
- **`geometry_json`** (string or null, optional): Serialized Autobahn API geometry object for the affected road segment.
- **`impact_lower`** (string or null, optional): Lower bound from the Autobahn API impact object.
- **`impact_upper`** (string or null, optional): Upper bound from the Autobahn API impact object.
- **`impact_symbols`** (array of string, optional): Impact symbols from the Autobahn API impact.symbols array.
- **`route_recommendation_json`** (string or null, optional): Serialized Autobahn API routeRecommendation object when rerouting advice is available.
- **`footer_lines`** (array of string, optional): Footer lines from the Autobahn API footer array.
- **`delay_minutes`** (integer or null, optional, min): delayTimeValue from the Autobahn warning item, expressed in minutes. Constraints: minimum `0`.
- **`average_speed_kmh`** (integer or null, optional, km/h): averageSpeed from the Autobahn warning item, expressed in kilometers per hour. Constraints: minimum `0`.
- **`abnormal_traffic_type`** (string or null, optional): abnormalTrafficType code from the Autobahn warning item.
- **`source_name`** (string or null, optional): source value from the Autobahn warning item that identifies the origin of the warning.
##### `display_type` values

- `WARNING`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "identifier": "string",
  "road": "string",
  "road_ids": [
    "string"
  ],
  "event_time": "2024-01-01T00:00:00Z",
  "display_type": "WARNING",
  "title": "string",
  "subtitle": "string",
  "description_lines": [
    "string"
  ],
  "future": false,
  "is_blocked": false,
  "icon": "string",
  "start_lc_position": 0,
  "start_timestamp": "2024-01-01T00:00:00Z",
  "extent": "string",
  "point": "string",
  "coordinate_lat": 0,
  "coordinate_lon": 0,
  "geometry_json": "string",
  "impact_lower": "string",
  "impact_upper": "string",
  "impact_symbols": [
    "string"
  ],
  "route_recommendation_json": "string",
  "footer_lines": [
    "string"
  ],
  "delay_minutes": 0,
  "average_speed_kmh": 0,
  "abnormal_traffic_type": "string",
  "source_name": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Warning Resolved

CloudEvents type: `DE.Autobahn.WarningResolved`

#### What it tells you

Normalized Autobahn warning payload with delay and traffic source details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/warning.

#### Identity

Each event identifies the real-world resource with `{identifier}`. `{identifier}` is stable Autobahn warning identifier used for the CloudEvents subject and Kafka key. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `autobahn`, key `{identifier}` |
| `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/warning/{identifier}/resolved`, retain `false`, QoS `1` |

#### Payload

`Warning Resolved` payloads are JSON object. Required fields: `identifier`, `road`, `road_ids`, `event_time`, `display_type`.

- **`identifier`** (string, required): Stable Autobahn warning identifier used for the CloudEvents subject and Kafka key.
- **`road`** (string, required): Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. Constraints: pattern `^[a-z0-9-]+$`.
- **`road_ids`** (array of string, required): Autobahn road identifiers for the road query that yielded this warning item.
- **`event_time`** (datetime, required): CloudEvents event time for the emitted warning record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp.
- **`display_type`** (enum, required): Autobahn API display_type for warning items.
- **`title`** (string or null, optional): Human-readable title from the Autobahn API warning item.
- **`subtitle`** (string or null, optional): Human-readable subtitle from the Autobahn API warning item.
- **`description_lines`** (array of string, optional): Description lines from the Autobahn API description array.
- **`future`** (boolean or null, optional): Whether the Autobahn API marks the warning as a future event.
- **`is_blocked`** (boolean or null, optional): Whether the Autobahn API marks the warning segment as blocked.
- **`icon`** (string or null, optional): Autobahn API icon identifier for the warning item.
- **`start_lc_position`** (integer or null, optional): Numeric startLcPosition value emitted by the Autobahn API for the beginning of the warning segment.
- **`start_timestamp`** (datetime or null, optional): startTimestamp value from the Autobahn API when the warning includes a scheduled or known start time.
- **`extent`** (string or null, optional): Autobahn API extent text for the affected road segment.
- **`point`** (string or null, optional): Autobahn API point text that identifies the affected point on the road segment.
- **`coordinate_lat`** (double or null, optional): Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-90`, maximum `90`.
- **`coordinate_lon`** (double or null, optional): Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-180`, maximum `180`.
- **`geometry_json`** (string or null, optional): Serialized Autobahn API geometry object for the affected road segment.
- **`impact_lower`** (string or null, optional): Lower bound from the Autobahn API impact object.
- **`impact_upper`** (string or null, optional): Upper bound from the Autobahn API impact object.
- **`impact_symbols`** (array of string, optional): Impact symbols from the Autobahn API impact.symbols array.
- **`route_recommendation_json`** (string or null, optional): Serialized Autobahn API routeRecommendation object when rerouting advice is available.
- **`footer_lines`** (array of string, optional): Footer lines from the Autobahn API footer array.
- **`delay_minutes`** (integer or null, optional, min): delayTimeValue from the Autobahn warning item, expressed in minutes. Constraints: minimum `0`.
- **`average_speed_kmh`** (integer or null, optional, km/h): averageSpeed from the Autobahn warning item, expressed in kilometers per hour. Constraints: minimum `0`.
- **`abnormal_traffic_type`** (string or null, optional): abnormalTrafficType code from the Autobahn warning item.
- **`source_name`** (string or null, optional): source value from the Autobahn warning item that identifies the origin of the warning.
##### `display_type` values

- `WARNING`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "identifier": "string",
  "road": "string",
  "road_ids": [
    "string"
  ],
  "event_time": "2024-01-01T00:00:00Z",
  "display_type": "WARNING",
  "title": "string",
  "subtitle": "string",
  "description_lines": [
    "string"
  ],
  "future": false,
  "is_blocked": false,
  "icon": "string",
  "start_lc_position": 0,
  "start_timestamp": "2024-01-01T00:00:00Z",
  "extent": "string",
  "point": "string",
  "coordinate_lat": 0,
  "coordinate_lon": 0,
  "geometry_json": "string",
  "impact_lower": "string",
  "impact_upper": "string",
  "impact_symbols": [
    "string"
  ],
  "route_recommendation_json": "string",
  "footer_lines": [
    "string"
  ],
  "delay_minutes": 0,
  "average_speed_kmh": 0,
  "abnormal_traffic_type": "string",
  "source_name": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Closure Appeared

CloudEvents type: `DE.Autobahn.ClosureAppeared`

#### What it tells you

Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.

#### Identity

Each event identifies the real-world resource with `{identifier}`. `{identifier}` is stable Autobahn item identifier used for the CloudEvents subject and Kafka key. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `autobahn`, key `{identifier}` |
| `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/closure/{identifier}/appeared`, retain `false`, QoS `1` |

#### Payload

`Closure Appeared` payloads are JSON object. Required fields: `identifier`, `road`, `road_ids`, `event_time`, `display_type`.

- **`identifier`** (string, required): Stable Autobahn item identifier used for the CloudEvents subject and Kafka key.
- **`road`** (string, required): Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. Constraints: pattern `^[a-z0-9-]+$`.
- **`road_ids`** (array of string, required): Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families.
- **`event_time`** (datetime, required): CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp.
- **`display_type`** (enum, required): Autobahn API display_type value that identifies the road-event subtype.
- **`title`** (string or null, optional): Human-readable title from the Autobahn API item.
- **`subtitle`** (string or null, optional): Human-readable subtitle from the Autobahn API item.
- **`description_lines`** (array of string, optional): Description lines from the Autobahn API description array.
- **`future`** (boolean or null, optional): Whether the Autobahn API marks the item as a future event.
- **`is_blocked`** (boolean or null, optional): Whether the Autobahn API marks the affected road segment as blocked.
- **`icon`** (string or null, optional): Autobahn API icon identifier for the item.
- **`start_lc_position`** (integer or null, optional): Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment.
- **`start_timestamp`** (datetime or null, optional): startTimestamp value from the Autobahn API when the item includes a scheduled or known start time.
- **`extent`** (string or null, optional): Autobahn API extent text for the affected road segment.
- **`point`** (string or null, optional): Autobahn API point text that identifies the affected point on the road segment.
- **`coordinate_lat`** (double or null, optional): Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-90`, maximum `90`.
- **`coordinate_lon`** (double or null, optional): Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-180`, maximum `180`.
- **`geometry_json`** (string or null, optional): Serialized Autobahn API geometry object for the affected road segment.
- **`impact_lower`** (string or null, optional): Lower bound from the Autobahn API impact object.
- **`impact_upper`** (string or null, optional): Upper bound from the Autobahn API impact object.
- **`impact_symbols`** (array of string, optional): Impact symbols from the Autobahn API impact.symbols array.
- **`route_recommendation_json`** (string or null, optional): Serialized Autobahn API routeRecommendation object when rerouting advice is available.
- **`footer_lines`** (array of string, optional): Footer lines from the Autobahn API footer array.
##### `display_type` values

- `ROADWORKS`
- `SHORT_TERM_ROADWORKS`
- `CLOSURE`
- `CLOSURE_ENTRY_EXIT`
- `WEIGHT_LIMIT_35`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "identifier": "string",
  "road": "string",
  "road_ids": [
    "string"
  ],
  "event_time": "2024-01-01T00:00:00Z",
  "display_type": "ROADWORKS",
  "title": "string",
  "subtitle": "string",
  "description_lines": [
    "string"
  ],
  "future": false,
  "is_blocked": false,
  "icon": "string",
  "start_lc_position": 0,
  "start_timestamp": "2024-01-01T00:00:00Z",
  "extent": "string",
  "point": "string",
  "coordinate_lat": 0,
  "coordinate_lon": 0,
  "geometry_json": "string",
  "impact_lower": "string",
  "impact_upper": "string",
  "impact_symbols": [
    "string"
  ],
  "route_recommendation_json": "string",
  "footer_lines": [
    "string"
  ]
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Closure Updated

CloudEvents type: `DE.Autobahn.ClosureUpdated`

#### What it tells you

Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.

#### Identity

Each event identifies the real-world resource with `{identifier}`. `{identifier}` is stable Autobahn item identifier used for the CloudEvents subject and Kafka key. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `autobahn`, key `{identifier}` |
| `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/closure/{identifier}/updated`, retain `false`, QoS `1` |

#### Payload

`Closure Updated` payloads are JSON object. Required fields: `identifier`, `road`, `road_ids`, `event_time`, `display_type`.

- **`identifier`** (string, required): Stable Autobahn item identifier used for the CloudEvents subject and Kafka key.
- **`road`** (string, required): Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. Constraints: pattern `^[a-z0-9-]+$`.
- **`road_ids`** (array of string, required): Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families.
- **`event_time`** (datetime, required): CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp.
- **`display_type`** (enum, required): Autobahn API display_type value that identifies the road-event subtype.
- **`title`** (string or null, optional): Human-readable title from the Autobahn API item.
- **`subtitle`** (string or null, optional): Human-readable subtitle from the Autobahn API item.
- **`description_lines`** (array of string, optional): Description lines from the Autobahn API description array.
- **`future`** (boolean or null, optional): Whether the Autobahn API marks the item as a future event.
- **`is_blocked`** (boolean or null, optional): Whether the Autobahn API marks the affected road segment as blocked.
- **`icon`** (string or null, optional): Autobahn API icon identifier for the item.
- **`start_lc_position`** (integer or null, optional): Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment.
- **`start_timestamp`** (datetime or null, optional): startTimestamp value from the Autobahn API when the item includes a scheduled or known start time.
- **`extent`** (string or null, optional): Autobahn API extent text for the affected road segment.
- **`point`** (string or null, optional): Autobahn API point text that identifies the affected point on the road segment.
- **`coordinate_lat`** (double or null, optional): Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-90`, maximum `90`.
- **`coordinate_lon`** (double or null, optional): Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-180`, maximum `180`.
- **`geometry_json`** (string or null, optional): Serialized Autobahn API geometry object for the affected road segment.
- **`impact_lower`** (string or null, optional): Lower bound from the Autobahn API impact object.
- **`impact_upper`** (string or null, optional): Upper bound from the Autobahn API impact object.
- **`impact_symbols`** (array of string, optional): Impact symbols from the Autobahn API impact.symbols array.
- **`route_recommendation_json`** (string or null, optional): Serialized Autobahn API routeRecommendation object when rerouting advice is available.
- **`footer_lines`** (array of string, optional): Footer lines from the Autobahn API footer array.
##### `display_type` values

- `ROADWORKS`
- `SHORT_TERM_ROADWORKS`
- `CLOSURE`
- `CLOSURE_ENTRY_EXIT`
- `WEIGHT_LIMIT_35`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "identifier": "string",
  "road": "string",
  "road_ids": [
    "string"
  ],
  "event_time": "2024-01-01T00:00:00Z",
  "display_type": "ROADWORKS",
  "title": "string",
  "subtitle": "string",
  "description_lines": [
    "string"
  ],
  "future": false,
  "is_blocked": false,
  "icon": "string",
  "start_lc_position": 0,
  "start_timestamp": "2024-01-01T00:00:00Z",
  "extent": "string",
  "point": "string",
  "coordinate_lat": 0,
  "coordinate_lon": 0,
  "geometry_json": "string",
  "impact_lower": "string",
  "impact_upper": "string",
  "impact_symbols": [
    "string"
  ],
  "route_recommendation_json": "string",
  "footer_lines": [
    "string"
  ]
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Closure Resolved

CloudEvents type: `DE.Autobahn.ClosureResolved`

#### What it tells you

Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.

#### Identity

Each event identifies the real-world resource with `{identifier}`. `{identifier}` is stable Autobahn item identifier used for the CloudEvents subject and Kafka key. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `autobahn`, key `{identifier}` |
| `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/closure/{identifier}/resolved`, retain `false`, QoS `1` |

#### Payload

`Closure Resolved` payloads are JSON object. Required fields: `identifier`, `road`, `road_ids`, `event_time`, `display_type`.

- **`identifier`** (string, required): Stable Autobahn item identifier used for the CloudEvents subject and Kafka key.
- **`road`** (string, required): Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. Constraints: pattern `^[a-z0-9-]+$`.
- **`road_ids`** (array of string, required): Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families.
- **`event_time`** (datetime, required): CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp.
- **`display_type`** (enum, required): Autobahn API display_type value that identifies the road-event subtype.
- **`title`** (string or null, optional): Human-readable title from the Autobahn API item.
- **`subtitle`** (string or null, optional): Human-readable subtitle from the Autobahn API item.
- **`description_lines`** (array of string, optional): Description lines from the Autobahn API description array.
- **`future`** (boolean or null, optional): Whether the Autobahn API marks the item as a future event.
- **`is_blocked`** (boolean or null, optional): Whether the Autobahn API marks the affected road segment as blocked.
- **`icon`** (string or null, optional): Autobahn API icon identifier for the item.
- **`start_lc_position`** (integer or null, optional): Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment.
- **`start_timestamp`** (datetime or null, optional): startTimestamp value from the Autobahn API when the item includes a scheduled or known start time.
- **`extent`** (string or null, optional): Autobahn API extent text for the affected road segment.
- **`point`** (string or null, optional): Autobahn API point text that identifies the affected point on the road segment.
- **`coordinate_lat`** (double or null, optional): Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-90`, maximum `90`.
- **`coordinate_lon`** (double or null, optional): Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-180`, maximum `180`.
- **`geometry_json`** (string or null, optional): Serialized Autobahn API geometry object for the affected road segment.
- **`impact_lower`** (string or null, optional): Lower bound from the Autobahn API impact object.
- **`impact_upper`** (string or null, optional): Upper bound from the Autobahn API impact object.
- **`impact_symbols`** (array of string, optional): Impact symbols from the Autobahn API impact.symbols array.
- **`route_recommendation_json`** (string or null, optional): Serialized Autobahn API routeRecommendation object when rerouting advice is available.
- **`footer_lines`** (array of string, optional): Footer lines from the Autobahn API footer array.
##### `display_type` values

- `ROADWORKS`
- `SHORT_TERM_ROADWORKS`
- `CLOSURE`
- `CLOSURE_ENTRY_EXIT`
- `WEIGHT_LIMIT_35`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "identifier": "string",
  "road": "string",
  "road_ids": [
    "string"
  ],
  "event_time": "2024-01-01T00:00:00Z",
  "display_type": "ROADWORKS",
  "title": "string",
  "subtitle": "string",
  "description_lines": [
    "string"
  ],
  "future": false,
  "is_blocked": false,
  "icon": "string",
  "start_lc_position": 0,
  "start_timestamp": "2024-01-01T00:00:00Z",
  "extent": "string",
  "point": "string",
  "coordinate_lat": 0,
  "coordinate_lon": 0,
  "geometry_json": "string",
  "impact_lower": "string",
  "impact_upper": "string",
  "impact_symbols": [
    "string"
  ],
  "route_recommendation_json": "string",
  "footer_lines": [
    "string"
  ]
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Entry Exit Closure Appeared

CloudEvents type: `DE.Autobahn.EntryExitClosureAppeared`

#### What it tells you

Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.

#### Identity

Each event identifies the real-world resource with `{identifier}`. `{identifier}` is stable Autobahn item identifier used for the CloudEvents subject and Kafka key. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `autobahn`, key `{identifier}` |
| `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/entry-exit-closure/{identifier}/appeared`, retain `false`, QoS `1` |

#### Payload

`Entry Exit Closure Appeared` payloads are JSON object. Required fields: `identifier`, `road`, `road_ids`, `event_time`, `display_type`.

- **`identifier`** (string, required): Stable Autobahn item identifier used for the CloudEvents subject and Kafka key.
- **`road`** (string, required): Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. Constraints: pattern `^[a-z0-9-]+$`.
- **`road_ids`** (array of string, required): Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families.
- **`event_time`** (datetime, required): CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp.
- **`display_type`** (enum, required): Autobahn API display_type value that identifies the road-event subtype.
- **`title`** (string or null, optional): Human-readable title from the Autobahn API item.
- **`subtitle`** (string or null, optional): Human-readable subtitle from the Autobahn API item.
- **`description_lines`** (array of string, optional): Description lines from the Autobahn API description array.
- **`future`** (boolean or null, optional): Whether the Autobahn API marks the item as a future event.
- **`is_blocked`** (boolean or null, optional): Whether the Autobahn API marks the affected road segment as blocked.
- **`icon`** (string or null, optional): Autobahn API icon identifier for the item.
- **`start_lc_position`** (integer or null, optional): Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment.
- **`start_timestamp`** (datetime or null, optional): startTimestamp value from the Autobahn API when the item includes a scheduled or known start time.
- **`extent`** (string or null, optional): Autobahn API extent text for the affected road segment.
- **`point`** (string or null, optional): Autobahn API point text that identifies the affected point on the road segment.
- **`coordinate_lat`** (double or null, optional): Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-90`, maximum `90`.
- **`coordinate_lon`** (double or null, optional): Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-180`, maximum `180`.
- **`geometry_json`** (string or null, optional): Serialized Autobahn API geometry object for the affected road segment.
- **`impact_lower`** (string or null, optional): Lower bound from the Autobahn API impact object.
- **`impact_upper`** (string or null, optional): Upper bound from the Autobahn API impact object.
- **`impact_symbols`** (array of string, optional): Impact symbols from the Autobahn API impact.symbols array.
- **`route_recommendation_json`** (string or null, optional): Serialized Autobahn API routeRecommendation object when rerouting advice is available.
- **`footer_lines`** (array of string, optional): Footer lines from the Autobahn API footer array.
##### `display_type` values

- `ROADWORKS`
- `SHORT_TERM_ROADWORKS`
- `CLOSURE`
- `CLOSURE_ENTRY_EXIT`
- `WEIGHT_LIMIT_35`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "identifier": "string",
  "road": "string",
  "road_ids": [
    "string"
  ],
  "event_time": "2024-01-01T00:00:00Z",
  "display_type": "ROADWORKS",
  "title": "string",
  "subtitle": "string",
  "description_lines": [
    "string"
  ],
  "future": false,
  "is_blocked": false,
  "icon": "string",
  "start_lc_position": 0,
  "start_timestamp": "2024-01-01T00:00:00Z",
  "extent": "string",
  "point": "string",
  "coordinate_lat": 0,
  "coordinate_lon": 0,
  "geometry_json": "string",
  "impact_lower": "string",
  "impact_upper": "string",
  "impact_symbols": [
    "string"
  ],
  "route_recommendation_json": "string",
  "footer_lines": [
    "string"
  ]
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Entry Exit Closure Updated

CloudEvents type: `DE.Autobahn.EntryExitClosureUpdated`

#### What it tells you

Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.

#### Identity

Each event identifies the real-world resource with `{identifier}`. `{identifier}` is stable Autobahn item identifier used for the CloudEvents subject and Kafka key. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `autobahn`, key `{identifier}` |
| `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/entry-exit-closure/{identifier}/updated`, retain `false`, QoS `1` |

#### Payload

`Entry Exit Closure Updated` payloads are JSON object. Required fields: `identifier`, `road`, `road_ids`, `event_time`, `display_type`.

- **`identifier`** (string, required): Stable Autobahn item identifier used for the CloudEvents subject and Kafka key.
- **`road`** (string, required): Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. Constraints: pattern `^[a-z0-9-]+$`.
- **`road_ids`** (array of string, required): Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families.
- **`event_time`** (datetime, required): CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp.
- **`display_type`** (enum, required): Autobahn API display_type value that identifies the road-event subtype.
- **`title`** (string or null, optional): Human-readable title from the Autobahn API item.
- **`subtitle`** (string or null, optional): Human-readable subtitle from the Autobahn API item.
- **`description_lines`** (array of string, optional): Description lines from the Autobahn API description array.
- **`future`** (boolean or null, optional): Whether the Autobahn API marks the item as a future event.
- **`is_blocked`** (boolean or null, optional): Whether the Autobahn API marks the affected road segment as blocked.
- **`icon`** (string or null, optional): Autobahn API icon identifier for the item.
- **`start_lc_position`** (integer or null, optional): Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment.
- **`start_timestamp`** (datetime or null, optional): startTimestamp value from the Autobahn API when the item includes a scheduled or known start time.
- **`extent`** (string or null, optional): Autobahn API extent text for the affected road segment.
- **`point`** (string or null, optional): Autobahn API point text that identifies the affected point on the road segment.
- **`coordinate_lat`** (double or null, optional): Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-90`, maximum `90`.
- **`coordinate_lon`** (double or null, optional): Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-180`, maximum `180`.
- **`geometry_json`** (string or null, optional): Serialized Autobahn API geometry object for the affected road segment.
- **`impact_lower`** (string or null, optional): Lower bound from the Autobahn API impact object.
- **`impact_upper`** (string or null, optional): Upper bound from the Autobahn API impact object.
- **`impact_symbols`** (array of string, optional): Impact symbols from the Autobahn API impact.symbols array.
- **`route_recommendation_json`** (string or null, optional): Serialized Autobahn API routeRecommendation object when rerouting advice is available.
- **`footer_lines`** (array of string, optional): Footer lines from the Autobahn API footer array.
##### `display_type` values

- `ROADWORKS`
- `SHORT_TERM_ROADWORKS`
- `CLOSURE`
- `CLOSURE_ENTRY_EXIT`
- `WEIGHT_LIMIT_35`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "identifier": "string",
  "road": "string",
  "road_ids": [
    "string"
  ],
  "event_time": "2024-01-01T00:00:00Z",
  "display_type": "ROADWORKS",
  "title": "string",
  "subtitle": "string",
  "description_lines": [
    "string"
  ],
  "future": false,
  "is_blocked": false,
  "icon": "string",
  "start_lc_position": 0,
  "start_timestamp": "2024-01-01T00:00:00Z",
  "extent": "string",
  "point": "string",
  "coordinate_lat": 0,
  "coordinate_lon": 0,
  "geometry_json": "string",
  "impact_lower": "string",
  "impact_upper": "string",
  "impact_symbols": [
    "string"
  ],
  "route_recommendation_json": "string",
  "footer_lines": [
    "string"
  ]
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Entry Exit Closure Resolved

CloudEvents type: `DE.Autobahn.EntryExitClosureResolved`

#### What it tells you

Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.

#### Identity

Each event identifies the real-world resource with `{identifier}`. `{identifier}` is stable Autobahn item identifier used for the CloudEvents subject and Kafka key. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `autobahn`, key `{identifier}` |
| `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/entry-exit-closure/{identifier}/resolved`, retain `false`, QoS `1` |

#### Payload

`Entry Exit Closure Resolved` payloads are JSON object. Required fields: `identifier`, `road`, `road_ids`, `event_time`, `display_type`.

- **`identifier`** (string, required): Stable Autobahn item identifier used for the CloudEvents subject and Kafka key.
- **`road`** (string, required): Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. Constraints: pattern `^[a-z0-9-]+$`.
- **`road_ids`** (array of string, required): Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families.
- **`event_time`** (datetime, required): CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp.
- **`display_type`** (enum, required): Autobahn API display_type value that identifies the road-event subtype.
- **`title`** (string or null, optional): Human-readable title from the Autobahn API item.
- **`subtitle`** (string or null, optional): Human-readable subtitle from the Autobahn API item.
- **`description_lines`** (array of string, optional): Description lines from the Autobahn API description array.
- **`future`** (boolean or null, optional): Whether the Autobahn API marks the item as a future event.
- **`is_blocked`** (boolean or null, optional): Whether the Autobahn API marks the affected road segment as blocked.
- **`icon`** (string or null, optional): Autobahn API icon identifier for the item.
- **`start_lc_position`** (integer or null, optional): Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment.
- **`start_timestamp`** (datetime or null, optional): startTimestamp value from the Autobahn API when the item includes a scheduled or known start time.
- **`extent`** (string or null, optional): Autobahn API extent text for the affected road segment.
- **`point`** (string or null, optional): Autobahn API point text that identifies the affected point on the road segment.
- **`coordinate_lat`** (double or null, optional): Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-90`, maximum `90`.
- **`coordinate_lon`** (double or null, optional): Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-180`, maximum `180`.
- **`geometry_json`** (string or null, optional): Serialized Autobahn API geometry object for the affected road segment.
- **`impact_lower`** (string or null, optional): Lower bound from the Autobahn API impact object.
- **`impact_upper`** (string or null, optional): Upper bound from the Autobahn API impact object.
- **`impact_symbols`** (array of string, optional): Impact symbols from the Autobahn API impact.symbols array.
- **`route_recommendation_json`** (string or null, optional): Serialized Autobahn API routeRecommendation object when rerouting advice is available.
- **`footer_lines`** (array of string, optional): Footer lines from the Autobahn API footer array.
##### `display_type` values

- `ROADWORKS`
- `SHORT_TERM_ROADWORKS`
- `CLOSURE`
- `CLOSURE_ENTRY_EXIT`
- `WEIGHT_LIMIT_35`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "identifier": "string",
  "road": "string",
  "road_ids": [
    "string"
  ],
  "event_time": "2024-01-01T00:00:00Z",
  "display_type": "ROADWORKS",
  "title": "string",
  "subtitle": "string",
  "description_lines": [
    "string"
  ],
  "future": false,
  "is_blocked": false,
  "icon": "string",
  "start_lc_position": 0,
  "start_timestamp": "2024-01-01T00:00:00Z",
  "extent": "string",
  "point": "string",
  "coordinate_lat": 0,
  "coordinate_lon": 0,
  "geometry_json": "string",
  "impact_lower": "string",
  "impact_upper": "string",
  "impact_symbols": [
    "string"
  ],
  "route_recommendation_json": "string",
  "footer_lines": [
    "string"
  ]
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Weight Limit35 Restriction Appeared

CloudEvents type: `DE.Autobahn.WeightLimit35RestrictionAppeared`

#### What it tells you

Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.

#### Identity

Each event identifies the real-world resource with `{identifier}`. `{identifier}` is stable Autobahn item identifier used for the CloudEvents subject and Kafka key. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `autobahn`, key `{identifier}` |
| `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/weight-limit-3-5/{identifier}/appeared`, retain `true`, QoS `1` |

#### Payload

`Weight Limit35 Restriction Appeared` payloads are JSON object. Required fields: `identifier`, `road`, `road_ids`, `event_time`, `display_type`.

- **`identifier`** (string, required): Stable Autobahn item identifier used for the CloudEvents subject and Kafka key.
- **`road`** (string, required): Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. Constraints: pattern `^[a-z0-9-]+$`.
- **`road_ids`** (array of string, required): Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families.
- **`event_time`** (datetime, required): CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp.
- **`display_type`** (enum, required): Autobahn API display_type value that identifies the road-event subtype.
- **`title`** (string or null, optional): Human-readable title from the Autobahn API item.
- **`subtitle`** (string or null, optional): Human-readable subtitle from the Autobahn API item.
- **`description_lines`** (array of string, optional): Description lines from the Autobahn API description array.
- **`future`** (boolean or null, optional): Whether the Autobahn API marks the item as a future event.
- **`is_blocked`** (boolean or null, optional): Whether the Autobahn API marks the affected road segment as blocked.
- **`icon`** (string or null, optional): Autobahn API icon identifier for the item.
- **`start_lc_position`** (integer or null, optional): Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment.
- **`start_timestamp`** (datetime or null, optional): startTimestamp value from the Autobahn API when the item includes a scheduled or known start time.
- **`extent`** (string or null, optional): Autobahn API extent text for the affected road segment.
- **`point`** (string or null, optional): Autobahn API point text that identifies the affected point on the road segment.
- **`coordinate_lat`** (double or null, optional): Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-90`, maximum `90`.
- **`coordinate_lon`** (double or null, optional): Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-180`, maximum `180`.
- **`geometry_json`** (string or null, optional): Serialized Autobahn API geometry object for the affected road segment.
- **`impact_lower`** (string or null, optional): Lower bound from the Autobahn API impact object.
- **`impact_upper`** (string or null, optional): Upper bound from the Autobahn API impact object.
- **`impact_symbols`** (array of string, optional): Impact symbols from the Autobahn API impact.symbols array.
- **`route_recommendation_json`** (string or null, optional): Serialized Autobahn API routeRecommendation object when rerouting advice is available.
- **`footer_lines`** (array of string, optional): Footer lines from the Autobahn API footer array.
##### `display_type` values

- `ROADWORKS`
- `SHORT_TERM_ROADWORKS`
- `CLOSURE`
- `CLOSURE_ENTRY_EXIT`
- `WEIGHT_LIMIT_35`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "identifier": "string",
  "road": "string",
  "road_ids": [
    "string"
  ],
  "event_time": "2024-01-01T00:00:00Z",
  "display_type": "ROADWORKS",
  "title": "string",
  "subtitle": "string",
  "description_lines": [
    "string"
  ],
  "future": false,
  "is_blocked": false,
  "icon": "string",
  "start_lc_position": 0,
  "start_timestamp": "2024-01-01T00:00:00Z",
  "extent": "string",
  "point": "string",
  "coordinate_lat": 0,
  "coordinate_lon": 0,
  "geometry_json": "string",
  "impact_lower": "string",
  "impact_upper": "string",
  "impact_symbols": [
    "string"
  ],
  "route_recommendation_json": "string",
  "footer_lines": [
    "string"
  ]
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Weight Limit35 Restriction Updated

CloudEvents type: `DE.Autobahn.WeightLimit35RestrictionUpdated`

#### What it tells you

Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.

#### Identity

Each event identifies the real-world resource with `{identifier}`. `{identifier}` is stable Autobahn item identifier used for the CloudEvents subject and Kafka key. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `autobahn`, key `{identifier}` |
| `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/weight-limit-3-5/{identifier}/updated`, retain `true`, QoS `1` |

#### Payload

`Weight Limit35 Restriction Updated` payloads are JSON object. Required fields: `identifier`, `road`, `road_ids`, `event_time`, `display_type`.

- **`identifier`** (string, required): Stable Autobahn item identifier used for the CloudEvents subject and Kafka key.
- **`road`** (string, required): Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. Constraints: pattern `^[a-z0-9-]+$`.
- **`road_ids`** (array of string, required): Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families.
- **`event_time`** (datetime, required): CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp.
- **`display_type`** (enum, required): Autobahn API display_type value that identifies the road-event subtype.
- **`title`** (string or null, optional): Human-readable title from the Autobahn API item.
- **`subtitle`** (string or null, optional): Human-readable subtitle from the Autobahn API item.
- **`description_lines`** (array of string, optional): Description lines from the Autobahn API description array.
- **`future`** (boolean or null, optional): Whether the Autobahn API marks the item as a future event.
- **`is_blocked`** (boolean or null, optional): Whether the Autobahn API marks the affected road segment as blocked.
- **`icon`** (string or null, optional): Autobahn API icon identifier for the item.
- **`start_lc_position`** (integer or null, optional): Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment.
- **`start_timestamp`** (datetime or null, optional): startTimestamp value from the Autobahn API when the item includes a scheduled or known start time.
- **`extent`** (string or null, optional): Autobahn API extent text for the affected road segment.
- **`point`** (string or null, optional): Autobahn API point text that identifies the affected point on the road segment.
- **`coordinate_lat`** (double or null, optional): Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-90`, maximum `90`.
- **`coordinate_lon`** (double or null, optional): Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-180`, maximum `180`.
- **`geometry_json`** (string or null, optional): Serialized Autobahn API geometry object for the affected road segment.
- **`impact_lower`** (string or null, optional): Lower bound from the Autobahn API impact object.
- **`impact_upper`** (string or null, optional): Upper bound from the Autobahn API impact object.
- **`impact_symbols`** (array of string, optional): Impact symbols from the Autobahn API impact.symbols array.
- **`route_recommendation_json`** (string or null, optional): Serialized Autobahn API routeRecommendation object when rerouting advice is available.
- **`footer_lines`** (array of string, optional): Footer lines from the Autobahn API footer array.
##### `display_type` values

- `ROADWORKS`
- `SHORT_TERM_ROADWORKS`
- `CLOSURE`
- `CLOSURE_ENTRY_EXIT`
- `WEIGHT_LIMIT_35`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "identifier": "string",
  "road": "string",
  "road_ids": [
    "string"
  ],
  "event_time": "2024-01-01T00:00:00Z",
  "display_type": "ROADWORKS",
  "title": "string",
  "subtitle": "string",
  "description_lines": [
    "string"
  ],
  "future": false,
  "is_blocked": false,
  "icon": "string",
  "start_lc_position": 0,
  "start_timestamp": "2024-01-01T00:00:00Z",
  "extent": "string",
  "point": "string",
  "coordinate_lat": 0,
  "coordinate_lon": 0,
  "geometry_json": "string",
  "impact_lower": "string",
  "impact_upper": "string",
  "impact_symbols": [
    "string"
  ],
  "route_recommendation_json": "string",
  "footer_lines": [
    "string"
  ]
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Weight Limit35 Restriction Resolved

CloudEvents type: `DE.Autobahn.WeightLimit35RestrictionResolved`

#### What it tells you

Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.

#### Identity

Each event identifies the real-world resource with `{identifier}`. `{identifier}` is stable Autobahn item identifier used for the CloudEvents subject and Kafka key. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `autobahn`, key `{identifier}` |
| `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/weight-limit-3-5/{identifier}/resolved`, retain `true`, QoS `1` |

#### Payload

`Weight Limit35 Restriction Resolved` payloads are JSON object. Required fields: `identifier`, `road`, `road_ids`, `event_time`, `display_type`.

- **`identifier`** (string, required): Stable Autobahn item identifier used for the CloudEvents subject and Kafka key.
- **`road`** (string, required): Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. Constraints: pattern `^[a-z0-9-]+$`.
- **`road_ids`** (array of string, required): Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families.
- **`event_time`** (datetime, required): CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp.
- **`display_type`** (enum, required): Autobahn API display_type value that identifies the road-event subtype.
- **`title`** (string or null, optional): Human-readable title from the Autobahn API item.
- **`subtitle`** (string or null, optional): Human-readable subtitle from the Autobahn API item.
- **`description_lines`** (array of string, optional): Description lines from the Autobahn API description array.
- **`future`** (boolean or null, optional): Whether the Autobahn API marks the item as a future event.
- **`is_blocked`** (boolean or null, optional): Whether the Autobahn API marks the affected road segment as blocked.
- **`icon`** (string or null, optional): Autobahn API icon identifier for the item.
- **`start_lc_position`** (integer or null, optional): Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment.
- **`start_timestamp`** (datetime or null, optional): startTimestamp value from the Autobahn API when the item includes a scheduled or known start time.
- **`extent`** (string or null, optional): Autobahn API extent text for the affected road segment.
- **`point`** (string or null, optional): Autobahn API point text that identifies the affected point on the road segment.
- **`coordinate_lat`** (double or null, optional): Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-90`, maximum `90`.
- **`coordinate_lon`** (double or null, optional): Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-180`, maximum `180`.
- **`geometry_json`** (string or null, optional): Serialized Autobahn API geometry object for the affected road segment.
- **`impact_lower`** (string or null, optional): Lower bound from the Autobahn API impact object.
- **`impact_upper`** (string or null, optional): Upper bound from the Autobahn API impact object.
- **`impact_symbols`** (array of string, optional): Impact symbols from the Autobahn API impact.symbols array.
- **`route_recommendation_json`** (string or null, optional): Serialized Autobahn API routeRecommendation object when rerouting advice is available.
- **`footer_lines`** (array of string, optional): Footer lines from the Autobahn API footer array.
##### `display_type` values

- `ROADWORKS`
- `SHORT_TERM_ROADWORKS`
- `CLOSURE`
- `CLOSURE_ENTRY_EXIT`
- `WEIGHT_LIMIT_35`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "identifier": "string",
  "road": "string",
  "road_ids": [
    "string"
  ],
  "event_time": "2024-01-01T00:00:00Z",
  "display_type": "ROADWORKS",
  "title": "string",
  "subtitle": "string",
  "description_lines": [
    "string"
  ],
  "future": false,
  "is_blocked": false,
  "icon": "string",
  "start_lc_position": 0,
  "start_timestamp": "2024-01-01T00:00:00Z",
  "extent": "string",
  "point": "string",
  "coordinate_lat": 0,
  "coordinate_lon": 0,
  "geometry_json": "string",
  "impact_lower": "string",
  "impact_upper": "string",
  "impact_symbols": [
    "string"
  ],
  "route_recommendation_json": "string",
  "footer_lines": [
    "string"
  ]
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Parking Lorry Appeared

CloudEvents type: `DE.Autobahn.ParkingLorryAppeared`

#### What it tells you

Normalized Autobahn lorry parking payload with parsed amenity and space counts. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/parking_lorry.

#### Identity

Each event identifies the real-world resource with `{identifier}`. `{identifier}` is stable Autobahn parking identifier used for the CloudEvents subject and Kafka key. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `autobahn`, key `{identifier}` |
| `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/parking-lorry/{identifier}/appeared`, retain `true`, QoS `1` |

#### Payload

`Parking Lorry Appeared` payloads are JSON object. Required fields: `identifier`, `road`, `road_ids`, `event_time`, `display_type`.

- **`identifier`** (string, required): Stable Autobahn parking identifier used for the CloudEvents subject and Kafka key.
- **`road`** (string, required): Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. Constraints: pattern `^[a-z0-9-]+$`.
- **`road_ids`** (array of string, required): Autobahn road identifiers for the road query that yielded this parking item.
- **`event_time`** (datetime, required): CloudEvents event time for the emitted parking record. The bridge uses the poll timestamp because parking items do not expose startTimestamp in the normalized payload.
- **`display_type`** (enum, required): Autobahn API display_type for lorry parking items.
- **`title`** (string or null, optional): Human-readable title from the Autobahn API parking item.
- **`subtitle`** (string or null, optional): Human-readable subtitle from the Autobahn API parking item.
- **`description_lines`** (array of string, optional): Description lines from the Autobahn API description array.
- **`future`** (boolean or null, optional): Whether the Autobahn API marks the parking item as a future entry.
- **`is_blocked`** (boolean or null, optional): Whether the Autobahn API marks the parking site as blocked.
- **`icon`** (string or null, optional): Autobahn API icon identifier for the parking item.
- **`start_lc_position`** (integer or null, optional): Numeric startLcPosition value emitted by the Autobahn API for the parking site location.
- **`extent`** (string or null, optional): Autobahn API extent text for the parking site.
- **`point`** (string or null, optional): Autobahn API point text that identifies the parking site location.
- **`coordinate_lat`** (double or null, optional): Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-90`, maximum `90`.
- **`coordinate_lon`** (double or null, optional): Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-180`, maximum `180`.
- **`route_recommendation_json`** (string or null, optional): Serialized Autobahn API routeRecommendation object when rerouting advice is available for the parking location.
- **`footer_lines`** (array of string, optional): Footer lines from the Autobahn API footer array.
- **`amenity_descriptions`** (array of string, optional): Descriptions extracted from lorryParkingFeatureIcons[].description for the parking site amenities.
- **`car_space_count`** (integer or null, optional): Number of passenger-car spaces parsed from description lines that contain PKW Stellplätze. Constraints: minimum `0`.
- **`lorry_space_count`** (integer or null, optional): Number of lorry spaces parsed from description lines that contain LKW Stellplätze. Constraints: minimum `0`.
##### `display_type` values

- `PARKING`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "identifier": "string",
  "road": "string",
  "road_ids": [
    "string"
  ],
  "event_time": "2024-01-01T00:00:00Z",
  "display_type": "PARKING",
  "title": "string",
  "subtitle": "string",
  "description_lines": [
    "string"
  ],
  "future": false,
  "is_blocked": false,
  "icon": "string",
  "start_lc_position": 0,
  "extent": "string",
  "point": "string",
  "coordinate_lat": 0,
  "coordinate_lon": 0,
  "route_recommendation_json": "string",
  "footer_lines": [
    "string"
  ],
  "amenity_descriptions": [
    "string"
  ],
  "car_space_count": 0,
  "lorry_space_count": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Parking Lorry Updated

CloudEvents type: `DE.Autobahn.ParkingLorryUpdated`

#### What it tells you

Normalized Autobahn lorry parking payload with parsed amenity and space counts. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/parking_lorry.

#### Identity

Each event identifies the real-world resource with `{identifier}`. `{identifier}` is stable Autobahn parking identifier used for the CloudEvents subject and Kafka key. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `autobahn`, key `{identifier}` |
| `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/parking-lorry/{identifier}/updated`, retain `true`, QoS `1` |

#### Payload

`Parking Lorry Updated` payloads are JSON object. Required fields: `identifier`, `road`, `road_ids`, `event_time`, `display_type`.

- **`identifier`** (string, required): Stable Autobahn parking identifier used for the CloudEvents subject and Kafka key.
- **`road`** (string, required): Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. Constraints: pattern `^[a-z0-9-]+$`.
- **`road_ids`** (array of string, required): Autobahn road identifiers for the road query that yielded this parking item.
- **`event_time`** (datetime, required): CloudEvents event time for the emitted parking record. The bridge uses the poll timestamp because parking items do not expose startTimestamp in the normalized payload.
- **`display_type`** (enum, required): Autobahn API display_type for lorry parking items.
- **`title`** (string or null, optional): Human-readable title from the Autobahn API parking item.
- **`subtitle`** (string or null, optional): Human-readable subtitle from the Autobahn API parking item.
- **`description_lines`** (array of string, optional): Description lines from the Autobahn API description array.
- **`future`** (boolean or null, optional): Whether the Autobahn API marks the parking item as a future entry.
- **`is_blocked`** (boolean or null, optional): Whether the Autobahn API marks the parking site as blocked.
- **`icon`** (string or null, optional): Autobahn API icon identifier for the parking item.
- **`start_lc_position`** (integer or null, optional): Numeric startLcPosition value emitted by the Autobahn API for the parking site location.
- **`extent`** (string or null, optional): Autobahn API extent text for the parking site.
- **`point`** (string or null, optional): Autobahn API point text that identifies the parking site location.
- **`coordinate_lat`** (double or null, optional): Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-90`, maximum `90`.
- **`coordinate_lon`** (double or null, optional): Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-180`, maximum `180`.
- **`route_recommendation_json`** (string or null, optional): Serialized Autobahn API routeRecommendation object when rerouting advice is available for the parking location.
- **`footer_lines`** (array of string, optional): Footer lines from the Autobahn API footer array.
- **`amenity_descriptions`** (array of string, optional): Descriptions extracted from lorryParkingFeatureIcons[].description for the parking site amenities.
- **`car_space_count`** (integer or null, optional): Number of passenger-car spaces parsed from description lines that contain PKW Stellplätze. Constraints: minimum `0`.
- **`lorry_space_count`** (integer or null, optional): Number of lorry spaces parsed from description lines that contain LKW Stellplätze. Constraints: minimum `0`.
##### `display_type` values

- `PARKING`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "identifier": "string",
  "road": "string",
  "road_ids": [
    "string"
  ],
  "event_time": "2024-01-01T00:00:00Z",
  "display_type": "PARKING",
  "title": "string",
  "subtitle": "string",
  "description_lines": [
    "string"
  ],
  "future": false,
  "is_blocked": false,
  "icon": "string",
  "start_lc_position": 0,
  "extent": "string",
  "point": "string",
  "coordinate_lat": 0,
  "coordinate_lon": 0,
  "route_recommendation_json": "string",
  "footer_lines": [
    "string"
  ],
  "amenity_descriptions": [
    "string"
  ],
  "car_space_count": 0,
  "lorry_space_count": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Parking Lorry Resolved

CloudEvents type: `DE.Autobahn.ParkingLorryResolved`

#### What it tells you

Normalized Autobahn lorry parking payload with parsed amenity and space counts. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/parking_lorry.

#### Identity

Each event identifies the real-world resource with `{identifier}`. `{identifier}` is stable Autobahn parking identifier used for the CloudEvents subject and Kafka key. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `autobahn`, key `{identifier}` |
| `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/parking-lorry/{identifier}/resolved`, retain `true`, QoS `1` |

#### Payload

`Parking Lorry Resolved` payloads are JSON object. Required fields: `identifier`, `road`, `road_ids`, `event_time`, `display_type`.

- **`identifier`** (string, required): Stable Autobahn parking identifier used for the CloudEvents subject and Kafka key.
- **`road`** (string, required): Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. Constraints: pattern `^[a-z0-9-]+$`.
- **`road_ids`** (array of string, required): Autobahn road identifiers for the road query that yielded this parking item.
- **`event_time`** (datetime, required): CloudEvents event time for the emitted parking record. The bridge uses the poll timestamp because parking items do not expose startTimestamp in the normalized payload.
- **`display_type`** (enum, required): Autobahn API display_type for lorry parking items.
- **`title`** (string or null, optional): Human-readable title from the Autobahn API parking item.
- **`subtitle`** (string or null, optional): Human-readable subtitle from the Autobahn API parking item.
- **`description_lines`** (array of string, optional): Description lines from the Autobahn API description array.
- **`future`** (boolean or null, optional): Whether the Autobahn API marks the parking item as a future entry.
- **`is_blocked`** (boolean or null, optional): Whether the Autobahn API marks the parking site as blocked.
- **`icon`** (string or null, optional): Autobahn API icon identifier for the parking item.
- **`start_lc_position`** (integer or null, optional): Numeric startLcPosition value emitted by the Autobahn API for the parking site location.
- **`extent`** (string or null, optional): Autobahn API extent text for the parking site.
- **`point`** (string or null, optional): Autobahn API point text that identifies the parking site location.
- **`coordinate_lat`** (double or null, optional): Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-90`, maximum `90`.
- **`coordinate_lon`** (double or null, optional): Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-180`, maximum `180`.
- **`route_recommendation_json`** (string or null, optional): Serialized Autobahn API routeRecommendation object when rerouting advice is available for the parking location.
- **`footer_lines`** (array of string, optional): Footer lines from the Autobahn API footer array.
- **`amenity_descriptions`** (array of string, optional): Descriptions extracted from lorryParkingFeatureIcons[].description for the parking site amenities.
- **`car_space_count`** (integer or null, optional): Number of passenger-car spaces parsed from description lines that contain PKW Stellplätze. Constraints: minimum `0`.
- **`lorry_space_count`** (integer or null, optional): Number of lorry spaces parsed from description lines that contain LKW Stellplätze. Constraints: minimum `0`.
##### `display_type` values

- `PARKING`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "identifier": "string",
  "road": "string",
  "road_ids": [
    "string"
  ],
  "event_time": "2024-01-01T00:00:00Z",
  "display_type": "PARKING",
  "title": "string",
  "subtitle": "string",
  "description_lines": [
    "string"
  ],
  "future": false,
  "is_blocked": false,
  "icon": "string",
  "start_lc_position": 0,
  "extent": "string",
  "point": "string",
  "coordinate_lat": 0,
  "coordinate_lon": 0,
  "route_recommendation_json": "string",
  "footer_lines": [
    "string"
  ],
  "amenity_descriptions": [
    "string"
  ],
  "car_space_count": 0,
  "lorry_space_count": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Electric Charging Station Appeared

CloudEvents type: `DE.Autobahn.ElectricChargingStationAppeared`

#### What it tells you

Normalized Autobahn charging-station payload with parsed address and charging point details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/electric_charging_station.

#### Identity

Each event identifies the real-world resource with `{identifier}`. `{identifier}` is stable Autobahn charging-station identifier used for the CloudEvents subject and Kafka key. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `autobahn`, key `{identifier}` |
| `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/electric-charging-station/{identifier}/appeared`, retain `true`, QoS `1` |

#### Payload

`Electric Charging Station Appeared` payloads are JSON object. Required fields: `identifier`, `road`, `road_ids`, `event_time`, `display_type`.

- **`identifier`** (string, required): Stable Autobahn charging-station identifier used for the CloudEvents subject and Kafka key.
- **`road`** (string, required): Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. Constraints: pattern `^[a-z0-9-]+$`.
- **`road_ids`** (array of string, required): Autobahn road identifiers for the road query that yielded this charging station item.
- **`event_time`** (datetime, required): CloudEvents event time for the emitted charging-station record. The bridge uses the poll timestamp because charging station items do not expose startTimestamp in the normalized payload.
- **`display_type`** (enum, required): Autobahn API display_type for charging-station items.
- **`title`** (string or null, optional): Human-readable title from the Autobahn API charging-station item.
- **`subtitle`** (string or null, optional): Human-readable subtitle from the Autobahn API charging-station item.
- **`description_lines`** (array of string, optional): Description lines from the Autobahn API description array.
- **`future`** (boolean or null, optional): Whether the Autobahn API marks the charging station item as a future entry.
- **`is_blocked`** (boolean or null, optional): Whether the Autobahn API marks the charging station site as blocked.
- **`icon`** (string or null, optional): Autobahn API icon identifier for the charging station item.
- **`extent`** (string or null, optional): Autobahn API extent text for the charging station site.
- **`point`** (string or null, optional): Autobahn API point text that identifies the charging station site.
- **`coordinate_lat`** (double or null, optional): Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-90`, maximum `90`.
- **`coordinate_lon`** (double or null, optional): Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-180`, maximum `180`.
- **`address_line`** (string or null, optional): Address line parsed from the first Autobahn API description line for the charging station site.
- **`charging_point_count`** (integer or null, optional): Number of parsed charging point entries derived from the Autobahn API description lines. Constraints: minimum `0`.
- **`charging_points_json`** (string or null, optional): Serialized array of normalized charging point entries parsed from the Autobahn API description lines.
- **`route_recommendation_json`** (string or null, optional): Serialized Autobahn API routeRecommendation object when rerouting advice is available for the charging station site.
- **`footer_lines`** (array of string, optional): Footer lines from the Autobahn API footer array.
##### `display_type` values

- `ELECTRIC_CHARGING_STATION`
- `STRONG_ELECTRIC_CHARGING_STATION`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "identifier": "string",
  "road": "string",
  "road_ids": [
    "string"
  ],
  "event_time": "2024-01-01T00:00:00Z",
  "display_type": "ELECTRIC_CHARGING_STATION",
  "title": "string",
  "subtitle": "string",
  "description_lines": [
    "string"
  ],
  "future": false,
  "is_blocked": false,
  "icon": "string",
  "extent": "string",
  "point": "string",
  "coordinate_lat": 0,
  "coordinate_lon": 0,
  "address_line": "string",
  "charging_point_count": 0,
  "charging_points_json": "string",
  "route_recommendation_json": "string",
  "footer_lines": [
    "string"
  ]
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Electric Charging Station Updated

CloudEvents type: `DE.Autobahn.ElectricChargingStationUpdated`

#### What it tells you

Normalized Autobahn charging-station payload with parsed address and charging point details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/electric_charging_station.

#### Identity

Each event identifies the real-world resource with `{identifier}`. `{identifier}` is stable Autobahn charging-station identifier used for the CloudEvents subject and Kafka key. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `autobahn`, key `{identifier}` |
| `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/electric-charging-station/{identifier}/updated`, retain `true`, QoS `1` |

#### Payload

`Electric Charging Station Updated` payloads are JSON object. Required fields: `identifier`, `road`, `road_ids`, `event_time`, `display_type`.

- **`identifier`** (string, required): Stable Autobahn charging-station identifier used for the CloudEvents subject and Kafka key.
- **`road`** (string, required): Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. Constraints: pattern `^[a-z0-9-]+$`.
- **`road_ids`** (array of string, required): Autobahn road identifiers for the road query that yielded this charging station item.
- **`event_time`** (datetime, required): CloudEvents event time for the emitted charging-station record. The bridge uses the poll timestamp because charging station items do not expose startTimestamp in the normalized payload.
- **`display_type`** (enum, required): Autobahn API display_type for charging-station items.
- **`title`** (string or null, optional): Human-readable title from the Autobahn API charging-station item.
- **`subtitle`** (string or null, optional): Human-readable subtitle from the Autobahn API charging-station item.
- **`description_lines`** (array of string, optional): Description lines from the Autobahn API description array.
- **`future`** (boolean or null, optional): Whether the Autobahn API marks the charging station item as a future entry.
- **`is_blocked`** (boolean or null, optional): Whether the Autobahn API marks the charging station site as blocked.
- **`icon`** (string or null, optional): Autobahn API icon identifier for the charging station item.
- **`extent`** (string or null, optional): Autobahn API extent text for the charging station site.
- **`point`** (string or null, optional): Autobahn API point text that identifies the charging station site.
- **`coordinate_lat`** (double or null, optional): Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-90`, maximum `90`.
- **`coordinate_lon`** (double or null, optional): Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-180`, maximum `180`.
- **`address_line`** (string or null, optional): Address line parsed from the first Autobahn API description line for the charging station site.
- **`charging_point_count`** (integer or null, optional): Number of parsed charging point entries derived from the Autobahn API description lines. Constraints: minimum `0`.
- **`charging_points_json`** (string or null, optional): Serialized array of normalized charging point entries parsed from the Autobahn API description lines.
- **`route_recommendation_json`** (string or null, optional): Serialized Autobahn API routeRecommendation object when rerouting advice is available for the charging station site.
- **`footer_lines`** (array of string, optional): Footer lines from the Autobahn API footer array.
##### `display_type` values

- `ELECTRIC_CHARGING_STATION`
- `STRONG_ELECTRIC_CHARGING_STATION`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "identifier": "string",
  "road": "string",
  "road_ids": [
    "string"
  ],
  "event_time": "2024-01-01T00:00:00Z",
  "display_type": "ELECTRIC_CHARGING_STATION",
  "title": "string",
  "subtitle": "string",
  "description_lines": [
    "string"
  ],
  "future": false,
  "is_blocked": false,
  "icon": "string",
  "extent": "string",
  "point": "string",
  "coordinate_lat": 0,
  "coordinate_lon": 0,
  "address_line": "string",
  "charging_point_count": 0,
  "charging_points_json": "string",
  "route_recommendation_json": "string",
  "footer_lines": [
    "string"
  ]
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Electric Charging Station Resolved

CloudEvents type: `DE.Autobahn.ElectricChargingStationResolved`

#### What it tells you

Normalized Autobahn charging-station payload with parsed address and charging point details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/electric_charging_station.

#### Identity

Each event identifies the real-world resource with `{identifier}`. `{identifier}` is stable Autobahn charging-station identifier used for the CloudEvents subject and Kafka key. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `autobahn`, key `{identifier}` |
| `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/electric-charging-station/{identifier}/resolved`, retain `true`, QoS `1` |

#### Payload

`Electric Charging Station Resolved` payloads are JSON object. Required fields: `identifier`, `road`, `road_ids`, `event_time`, `display_type`.

- **`identifier`** (string, required): Stable Autobahn charging-station identifier used for the CloudEvents subject and Kafka key.
- **`road`** (string, required): Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. Constraints: pattern `^[a-z0-9-]+$`.
- **`road_ids`** (array of string, required): Autobahn road identifiers for the road query that yielded this charging station item.
- **`event_time`** (datetime, required): CloudEvents event time for the emitted charging-station record. The bridge uses the poll timestamp because charging station items do not expose startTimestamp in the normalized payload.
- **`display_type`** (enum, required): Autobahn API display_type for charging-station items.
- **`title`** (string or null, optional): Human-readable title from the Autobahn API charging-station item.
- **`subtitle`** (string or null, optional): Human-readable subtitle from the Autobahn API charging-station item.
- **`description_lines`** (array of string, optional): Description lines from the Autobahn API description array.
- **`future`** (boolean or null, optional): Whether the Autobahn API marks the charging station item as a future entry.
- **`is_blocked`** (boolean or null, optional): Whether the Autobahn API marks the charging station site as blocked.
- **`icon`** (string or null, optional): Autobahn API icon identifier for the charging station item.
- **`extent`** (string or null, optional): Autobahn API extent text for the charging station site.
- **`point`** (string or null, optional): Autobahn API point text that identifies the charging station site.
- **`coordinate_lat`** (double or null, optional): Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-90`, maximum `90`.
- **`coordinate_lon`** (double or null, optional): Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-180`, maximum `180`.
- **`address_line`** (string or null, optional): Address line parsed from the first Autobahn API description line for the charging station site.
- **`charging_point_count`** (integer or null, optional): Number of parsed charging point entries derived from the Autobahn API description lines. Constraints: minimum `0`.
- **`charging_points_json`** (string or null, optional): Serialized array of normalized charging point entries parsed from the Autobahn API description lines.
- **`route_recommendation_json`** (string or null, optional): Serialized Autobahn API routeRecommendation object when rerouting advice is available for the charging station site.
- **`footer_lines`** (array of string, optional): Footer lines from the Autobahn API footer array.
##### `display_type` values

- `ELECTRIC_CHARGING_STATION`
- `STRONG_ELECTRIC_CHARGING_STATION`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "identifier": "string",
  "road": "string",
  "road_ids": [
    "string"
  ],
  "event_time": "2024-01-01T00:00:00Z",
  "display_type": "ELECTRIC_CHARGING_STATION",
  "title": "string",
  "subtitle": "string",
  "description_lines": [
    "string"
  ],
  "future": false,
  "is_blocked": false,
  "icon": "string",
  "extent": "string",
  "point": "string",
  "coordinate_lat": 0,
  "coordinate_lon": 0,
  "address_line": "string",
  "charging_point_count": 0,
  "charging_points_json": "string",
  "route_recommendation_json": "string",
  "footer_lines": [
    "string"
  ]
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Strong Electric Charging Station Appeared

CloudEvents type: `DE.Autobahn.StrongElectricChargingStationAppeared`

#### What it tells you

Normalized Autobahn charging-station payload with parsed address and charging point details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/electric_charging_station.

#### Identity

Each event identifies the real-world resource with `{identifier}`. `{identifier}` is stable Autobahn charging-station identifier used for the CloudEvents subject and Kafka key. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `autobahn`, key `{identifier}` |
| `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/strong-electric-charging-station/{identifier}/appeared`, retain `true`, QoS `1` |

#### Payload

`Strong Electric Charging Station Appeared` payloads are JSON object. Required fields: `identifier`, `road`, `road_ids`, `event_time`, `display_type`.

- **`identifier`** (string, required): Stable Autobahn charging-station identifier used for the CloudEvents subject and Kafka key.
- **`road`** (string, required): Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. Constraints: pattern `^[a-z0-9-]+$`.
- **`road_ids`** (array of string, required): Autobahn road identifiers for the road query that yielded this charging station item.
- **`event_time`** (datetime, required): CloudEvents event time for the emitted charging-station record. The bridge uses the poll timestamp because charging station items do not expose startTimestamp in the normalized payload.
- **`display_type`** (enum, required): Autobahn API display_type for charging-station items.
- **`title`** (string or null, optional): Human-readable title from the Autobahn API charging-station item.
- **`subtitle`** (string or null, optional): Human-readable subtitle from the Autobahn API charging-station item.
- **`description_lines`** (array of string, optional): Description lines from the Autobahn API description array.
- **`future`** (boolean or null, optional): Whether the Autobahn API marks the charging station item as a future entry.
- **`is_blocked`** (boolean or null, optional): Whether the Autobahn API marks the charging station site as blocked.
- **`icon`** (string or null, optional): Autobahn API icon identifier for the charging station item.
- **`extent`** (string or null, optional): Autobahn API extent text for the charging station site.
- **`point`** (string or null, optional): Autobahn API point text that identifies the charging station site.
- **`coordinate_lat`** (double or null, optional): Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-90`, maximum `90`.
- **`coordinate_lon`** (double or null, optional): Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-180`, maximum `180`.
- **`address_line`** (string or null, optional): Address line parsed from the first Autobahn API description line for the charging station site.
- **`charging_point_count`** (integer or null, optional): Number of parsed charging point entries derived from the Autobahn API description lines. Constraints: minimum `0`.
- **`charging_points_json`** (string or null, optional): Serialized array of normalized charging point entries parsed from the Autobahn API description lines.
- **`route_recommendation_json`** (string or null, optional): Serialized Autobahn API routeRecommendation object when rerouting advice is available for the charging station site.
- **`footer_lines`** (array of string, optional): Footer lines from the Autobahn API footer array.
##### `display_type` values

- `ELECTRIC_CHARGING_STATION`
- `STRONG_ELECTRIC_CHARGING_STATION`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "identifier": "string",
  "road": "string",
  "road_ids": [
    "string"
  ],
  "event_time": "2024-01-01T00:00:00Z",
  "display_type": "ELECTRIC_CHARGING_STATION",
  "title": "string",
  "subtitle": "string",
  "description_lines": [
    "string"
  ],
  "future": false,
  "is_blocked": false,
  "icon": "string",
  "extent": "string",
  "point": "string",
  "coordinate_lat": 0,
  "coordinate_lon": 0,
  "address_line": "string",
  "charging_point_count": 0,
  "charging_points_json": "string",
  "route_recommendation_json": "string",
  "footer_lines": [
    "string"
  ]
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Strong Electric Charging Station Updated

CloudEvents type: `DE.Autobahn.StrongElectricChargingStationUpdated`

#### What it tells you

Normalized Autobahn charging-station payload with parsed address and charging point details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/electric_charging_station.

#### Identity

Each event identifies the real-world resource with `{identifier}`. `{identifier}` is stable Autobahn charging-station identifier used for the CloudEvents subject and Kafka key. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `autobahn`, key `{identifier}` |
| `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/strong-electric-charging-station/{identifier}/updated`, retain `true`, QoS `1` |

#### Payload

`Strong Electric Charging Station Updated` payloads are JSON object. Required fields: `identifier`, `road`, `road_ids`, `event_time`, `display_type`.

- **`identifier`** (string, required): Stable Autobahn charging-station identifier used for the CloudEvents subject and Kafka key.
- **`road`** (string, required): Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. Constraints: pattern `^[a-z0-9-]+$`.
- **`road_ids`** (array of string, required): Autobahn road identifiers for the road query that yielded this charging station item.
- **`event_time`** (datetime, required): CloudEvents event time for the emitted charging-station record. The bridge uses the poll timestamp because charging station items do not expose startTimestamp in the normalized payload.
- **`display_type`** (enum, required): Autobahn API display_type for charging-station items.
- **`title`** (string or null, optional): Human-readable title from the Autobahn API charging-station item.
- **`subtitle`** (string or null, optional): Human-readable subtitle from the Autobahn API charging-station item.
- **`description_lines`** (array of string, optional): Description lines from the Autobahn API description array.
- **`future`** (boolean or null, optional): Whether the Autobahn API marks the charging station item as a future entry.
- **`is_blocked`** (boolean or null, optional): Whether the Autobahn API marks the charging station site as blocked.
- **`icon`** (string or null, optional): Autobahn API icon identifier for the charging station item.
- **`extent`** (string or null, optional): Autobahn API extent text for the charging station site.
- **`point`** (string or null, optional): Autobahn API point text that identifies the charging station site.
- **`coordinate_lat`** (double or null, optional): Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-90`, maximum `90`.
- **`coordinate_lon`** (double or null, optional): Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-180`, maximum `180`.
- **`address_line`** (string or null, optional): Address line parsed from the first Autobahn API description line for the charging station site.
- **`charging_point_count`** (integer or null, optional): Number of parsed charging point entries derived from the Autobahn API description lines. Constraints: minimum `0`.
- **`charging_points_json`** (string or null, optional): Serialized array of normalized charging point entries parsed from the Autobahn API description lines.
- **`route_recommendation_json`** (string or null, optional): Serialized Autobahn API routeRecommendation object when rerouting advice is available for the charging station site.
- **`footer_lines`** (array of string, optional): Footer lines from the Autobahn API footer array.
##### `display_type` values

- `ELECTRIC_CHARGING_STATION`
- `STRONG_ELECTRIC_CHARGING_STATION`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "identifier": "string",
  "road": "string",
  "road_ids": [
    "string"
  ],
  "event_time": "2024-01-01T00:00:00Z",
  "display_type": "ELECTRIC_CHARGING_STATION",
  "title": "string",
  "subtitle": "string",
  "description_lines": [
    "string"
  ],
  "future": false,
  "is_blocked": false,
  "icon": "string",
  "extent": "string",
  "point": "string",
  "coordinate_lat": 0,
  "coordinate_lon": 0,
  "address_line": "string",
  "charging_point_count": 0,
  "charging_points_json": "string",
  "route_recommendation_json": "string",
  "footer_lines": [
    "string"
  ]
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Strong Electric Charging Station Resolved

CloudEvents type: `DE.Autobahn.StrongElectricChargingStationResolved`

#### What it tells you

Normalized Autobahn charging-station payload with parsed address and charging point details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/electric_charging_station.

#### Identity

Each event identifies the real-world resource with `{identifier}`. `{identifier}` is stable Autobahn charging-station identifier used for the CloudEvents subject and Kafka key. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `autobahn`, key `{identifier}` |
| `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/strong-electric-charging-station/{identifier}/resolved`, retain `true`, QoS `1` |

#### Payload

`Strong Electric Charging Station Resolved` payloads are JSON object. Required fields: `identifier`, `road`, `road_ids`, `event_time`, `display_type`.

- **`identifier`** (string, required): Stable Autobahn charging-station identifier used for the CloudEvents subject and Kafka key.
- **`road`** (string, required): Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. Constraints: pattern `^[a-z0-9-]+$`.
- **`road_ids`** (array of string, required): Autobahn road identifiers for the road query that yielded this charging station item.
- **`event_time`** (datetime, required): CloudEvents event time for the emitted charging-station record. The bridge uses the poll timestamp because charging station items do not expose startTimestamp in the normalized payload.
- **`display_type`** (enum, required): Autobahn API display_type for charging-station items.
- **`title`** (string or null, optional): Human-readable title from the Autobahn API charging-station item.
- **`subtitle`** (string or null, optional): Human-readable subtitle from the Autobahn API charging-station item.
- **`description_lines`** (array of string, optional): Description lines from the Autobahn API description array.
- **`future`** (boolean or null, optional): Whether the Autobahn API marks the charging station item as a future entry.
- **`is_blocked`** (boolean or null, optional): Whether the Autobahn API marks the charging station site as blocked.
- **`icon`** (string or null, optional): Autobahn API icon identifier for the charging station item.
- **`extent`** (string or null, optional): Autobahn API extent text for the charging station site.
- **`point`** (string or null, optional): Autobahn API point text that identifies the charging station site.
- **`coordinate_lat`** (double or null, optional): Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-90`, maximum `90`.
- **`coordinate_lon`** (double or null, optional): Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-180`, maximum `180`.
- **`address_line`** (string or null, optional): Address line parsed from the first Autobahn API description line for the charging station site.
- **`charging_point_count`** (integer or null, optional): Number of parsed charging point entries derived from the Autobahn API description lines. Constraints: minimum `0`.
- **`charging_points_json`** (string or null, optional): Serialized array of normalized charging point entries parsed from the Autobahn API description lines.
- **`route_recommendation_json`** (string or null, optional): Serialized Autobahn API routeRecommendation object when rerouting advice is available for the charging station site.
- **`footer_lines`** (array of string, optional): Footer lines from the Autobahn API footer array.
##### `display_type` values

- `ELECTRIC_CHARGING_STATION`
- `STRONG_ELECTRIC_CHARGING_STATION`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "identifier": "string",
  "road": "string",
  "road_ids": [
    "string"
  ],
  "event_time": "2024-01-01T00:00:00Z",
  "display_type": "ELECTRIC_CHARGING_STATION",
  "title": "string",
  "subtitle": "string",
  "description_lines": [
    "string"
  ],
  "future": false,
  "is_blocked": false,
  "icon": "string",
  "extent": "string",
  "point": "string",
  "coordinate_lat": 0,
  "coordinate_lon": 0,
  "address_line": "string",
  "charging_point_count": 0,
  "charging_points_json": "string",
  "route_recommendation_json": "string",
  "footer_lines": [
    "string"
  ]
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Webcam Appeared

CloudEvents type: `DE.Autobahn.WebcamAppeared`

#### What it tells you

Normalized Autobahn webcam payload with operator and media URLs. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/webcam.

#### Identity

Each event identifies the real-world resource with `{identifier}`. `{identifier}` is stable Autobahn webcam identifier used for the CloudEvents subject and Kafka key. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `autobahn`, key `{identifier}` |
| `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/webcam/{identifier}/appeared`, retain `true`, QoS `1` |

#### Payload

`Webcam Appeared` payloads are JSON object. Required fields: `identifier`, `road`, `road_ids`, `event_time`, `display_type`.

- **`identifier`** (string, required): Stable Autobahn webcam identifier used for the CloudEvents subject and Kafka key.
- **`road`** (string, required): Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. Constraints: pattern `^[a-z0-9-]+$`.
- **`road_ids`** (array of string, required): Autobahn road identifiers for the road query that yielded this webcam item.
- **`event_time`** (datetime, required): CloudEvents event time for the emitted webcam record. The bridge uses the poll timestamp because webcam items do not expose startTimestamp in the normalized payload.
- **`display_type`** (enum, required): Autobahn API display_type for webcam items.
- **`title`** (string or null, optional): Human-readable title from the Autobahn API webcam item.
- **`subtitle`** (string or null, optional): Human-readable subtitle from the Autobahn API webcam item.
- **`description_lines`** (array of string, optional): Description lines from the Autobahn API description array.
- **`future`** (boolean or null, optional): Whether the Autobahn API marks the webcam item as a future entry.
- **`is_blocked`** (boolean or null, optional): Whether the Autobahn API marks the webcam location as blocked.
- **`icon`** (string or null, optional): Autobahn API icon identifier for the webcam item.
- **`extent`** (string or null, optional): Autobahn API extent text for the webcam location.
- **`point`** (string or null, optional): Autobahn API point text that identifies the webcam location.
- **`coordinate_lat`** (double or null, optional): Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-90`, maximum `90`.
- **`coordinate_lon`** (double or null, optional): Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-180`, maximum `180`.
- **`route_recommendation_json`** (string or null, optional): Serialized Autobahn API routeRecommendation object when rerouting advice is available for the webcam location.
- **`footer_lines`** (array of string, optional): Footer lines from the Autobahn API footer array.
- **`operator_name`** (string or null, optional): operator value from the Autobahn API webcam item.
- **`image_url`** (uri or null, optional): imageurl value from the Autobahn API webcam item for the still image.
- **`stream_url`** (uri or null, optional): linkurl value from the Autobahn API webcam item for the linked stream or detail page.
##### `display_type` values

- `WEBCAM`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "identifier": "string",
  "road": "string",
  "road_ids": [
    "string"
  ],
  "event_time": "2024-01-01T00:00:00Z",
  "display_type": "WEBCAM",
  "title": "string",
  "subtitle": "string",
  "description_lines": [
    "string"
  ],
  "future": false,
  "is_blocked": false,
  "icon": "string",
  "extent": "string",
  "point": "string",
  "coordinate_lat": 0,
  "coordinate_lon": 0,
  "route_recommendation_json": "string",
  "footer_lines": [
    "string"
  ],
  "operator_name": "string",
  "image_url": "string",
  "stream_url": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Webcam Updated

CloudEvents type: `DE.Autobahn.WebcamUpdated`

#### What it tells you

Normalized Autobahn webcam payload with operator and media URLs. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/webcam.

#### Identity

Each event identifies the real-world resource with `{identifier}`. `{identifier}` is stable Autobahn webcam identifier used for the CloudEvents subject and Kafka key. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `autobahn`, key `{identifier}` |
| `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/webcam/{identifier}/updated`, retain `true`, QoS `1` |

#### Payload

`Webcam Updated` payloads are JSON object. Required fields: `identifier`, `road`, `road_ids`, `event_time`, `display_type`.

- **`identifier`** (string, required): Stable Autobahn webcam identifier used for the CloudEvents subject and Kafka key.
- **`road`** (string, required): Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. Constraints: pattern `^[a-z0-9-]+$`.
- **`road_ids`** (array of string, required): Autobahn road identifiers for the road query that yielded this webcam item.
- **`event_time`** (datetime, required): CloudEvents event time for the emitted webcam record. The bridge uses the poll timestamp because webcam items do not expose startTimestamp in the normalized payload.
- **`display_type`** (enum, required): Autobahn API display_type for webcam items.
- **`title`** (string or null, optional): Human-readable title from the Autobahn API webcam item.
- **`subtitle`** (string or null, optional): Human-readable subtitle from the Autobahn API webcam item.
- **`description_lines`** (array of string, optional): Description lines from the Autobahn API description array.
- **`future`** (boolean or null, optional): Whether the Autobahn API marks the webcam item as a future entry.
- **`is_blocked`** (boolean or null, optional): Whether the Autobahn API marks the webcam location as blocked.
- **`icon`** (string or null, optional): Autobahn API icon identifier for the webcam item.
- **`extent`** (string or null, optional): Autobahn API extent text for the webcam location.
- **`point`** (string or null, optional): Autobahn API point text that identifies the webcam location.
- **`coordinate_lat`** (double or null, optional): Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-90`, maximum `90`.
- **`coordinate_lon`** (double or null, optional): Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-180`, maximum `180`.
- **`route_recommendation_json`** (string or null, optional): Serialized Autobahn API routeRecommendation object when rerouting advice is available for the webcam location.
- **`footer_lines`** (array of string, optional): Footer lines from the Autobahn API footer array.
- **`operator_name`** (string or null, optional): operator value from the Autobahn API webcam item.
- **`image_url`** (uri or null, optional): imageurl value from the Autobahn API webcam item for the still image.
- **`stream_url`** (uri or null, optional): linkurl value from the Autobahn API webcam item for the linked stream or detail page.
##### `display_type` values

- `WEBCAM`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "identifier": "string",
  "road": "string",
  "road_ids": [
    "string"
  ],
  "event_time": "2024-01-01T00:00:00Z",
  "display_type": "WEBCAM",
  "title": "string",
  "subtitle": "string",
  "description_lines": [
    "string"
  ],
  "future": false,
  "is_blocked": false,
  "icon": "string",
  "extent": "string",
  "point": "string",
  "coordinate_lat": 0,
  "coordinate_lon": 0,
  "route_recommendation_json": "string",
  "footer_lines": [
    "string"
  ],
  "operator_name": "string",
  "image_url": "string",
  "stream_url": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Webcam Resolved

CloudEvents type: `DE.Autobahn.WebcamResolved`

#### What it tells you

Normalized Autobahn webcam payload with operator and media URLs. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/webcam.

#### Identity

Each event identifies the real-world resource with `{identifier}`. `{identifier}` is stable Autobahn webcam identifier used for the CloudEvents subject and Kafka key. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `autobahn`, key `{identifier}` |
| `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/webcam/{identifier}/resolved`, retain `true`, QoS `1` |

#### Payload

`Webcam Resolved` payloads are JSON object. Required fields: `identifier`, `road`, `road_ids`, `event_time`, `display_type`.

- **`identifier`** (string, required): Stable Autobahn webcam identifier used for the CloudEvents subject and Kafka key.
- **`road`** (string, required): Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. Constraints: pattern `^[a-z0-9-]+$`.
- **`road_ids`** (array of string, required): Autobahn road identifiers for the road query that yielded this webcam item.
- **`event_time`** (datetime, required): CloudEvents event time for the emitted webcam record. The bridge uses the poll timestamp because webcam items do not expose startTimestamp in the normalized payload.
- **`display_type`** (enum, required): Autobahn API display_type for webcam items.
- **`title`** (string or null, optional): Human-readable title from the Autobahn API webcam item.
- **`subtitle`** (string or null, optional): Human-readable subtitle from the Autobahn API webcam item.
- **`description_lines`** (array of string, optional): Description lines from the Autobahn API description array.
- **`future`** (boolean or null, optional): Whether the Autobahn API marks the webcam item as a future entry.
- **`is_blocked`** (boolean or null, optional): Whether the Autobahn API marks the webcam location as blocked.
- **`icon`** (string or null, optional): Autobahn API icon identifier for the webcam item.
- **`extent`** (string or null, optional): Autobahn API extent text for the webcam location.
- **`point`** (string or null, optional): Autobahn API point text that identifies the webcam location.
- **`coordinate_lat`** (double or null, optional): Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-90`, maximum `90`.
- **`coordinate_lon`** (double or null, optional): Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. Constraints: minimum `-180`, maximum `180`.
- **`route_recommendation_json`** (string or null, optional): Serialized Autobahn API routeRecommendation object when rerouting advice is available for the webcam location.
- **`footer_lines`** (array of string, optional): Footer lines from the Autobahn API footer array.
- **`operator_name`** (string or null, optional): operator value from the Autobahn API webcam item.
- **`image_url`** (uri or null, optional): imageurl value from the Autobahn API webcam item for the still image.
- **`stream_url`** (uri or null, optional): linkurl value from the Autobahn API webcam item for the linked stream or detail page.
##### `display_type` values

- `WEBCAM`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "identifier": "string",
  "road": "string",
  "road_ids": [
    "string"
  ],
  "event_time": "2024-01-01T00:00:00Z",
  "display_type": "WEBCAM",
  "title": "string",
  "subtitle": "string",
  "description_lines": [
    "string"
  ],
  "future": false,
  "is_blocked": false,
  "icon": "string",
  "extent": "string",
  "point": "string",
  "coordinate_lat": 0,
  "coordinate_lon": 0,
  "route_recommendation_json": "string",
  "footer_lines": [
    "string"
  ],
  "operator_name": "string",
  "image_url": "string",
  "stream_url": "string"
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

- The bridge documentation mentions ETag-aware polling, so consumers should expect unchanged upstream responses to be skipped.
- The MQTT variant publishes with QoS 1 and retained-message Last-Known-Value semantics where declared in the event catalog.

## References

- xRegistry manifest: [`xreg/autobahn.xreg.json`](xreg/autobahn.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
