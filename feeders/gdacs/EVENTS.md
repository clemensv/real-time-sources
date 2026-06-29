# GDACS Events

GDACS publishes disaster alerts and impact updates from the Global Disaster Alert and Coordination System for global natural-hazard events. These events help consumers monitor hazards, route notifications, and correlate public-warning updates without polling the upstream source directly.

## At a glance

- **Event types:** 1 documented event type (3 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 1 telemetry event type.
- **Identity:** `{event_type}/{event_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `gdacs`. The record key is `{event_type}/{event_id}`. In plain language, `{event_type}/{event_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['gdacs'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `alerts/intl/gdacs/gdacs/+/+/+/+/alert`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('alerts/intl/gdacs/gdacs/+/+/+/+/alert', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `gdacs`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/gdacs')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Disaster Alert

CloudEvents type: `GDACS.DisasterAlert`

#### What it tells you

A disaster alert from the Global Disaster Alert and Coordination System (GDACS), covering earthquakes, tropical cyclones, floods, volcanoes, forest fires, and droughts worldwide.

#### Identity

Each event identifies the real-world resource with `{event_type}/{event_id}`. `{event_type}` is the type of natural disaster reported by GDACS; `{event_id}` is the unique numeric identifier assigned to the disaster event by GDACS, stable across all episodes and updates for the same event. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gdacs`, key `{event_type}/{event_id}` |
| `MQTT/5.0` | topic `alerts/intl/gdacs/gdacs/{event_type}/{alert_color}/{country}/{event_id}/alert`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `amqp://localhost:5672/gdacs`, message subject `{event_type}/{event_id}` |

#### Payload

`Disaster Alert` payloads are JSON object. Required fields: `event_type`, `event_id`, `alert_level`, `severity_value`, `severity_unit`, `country`, `latitude`, `longitude`, `from_date`, `alert_color`.

- **`event_type`** (enum, required): The type of natural disaster reported by GDACS. EQ = Earthquake, TC = Tropical Cyclone, FL = Flood, VO = Volcano, FF = Forest Fire, DR = Drought.
- **`event_id`** (string, required): The unique numeric identifier assigned to the disaster event by GDACS, stable across all episodes and updates for the same event.
- **`episode_id`** (string, optional): The unique numeric identifier for a specific episode within an event. Events such as tropical cyclones may have multiple episodes as they evolve over time.
- **`alert_level`** (enum, required): The overall GDACS alert level for the event, indicating the expected humanitarian impact. Green = low impact, Orange = moderate impact, Red = high impact requiring international response.
- **`alert_score`** (double, optional): A numeric score (0.0–3.0) representing the overall alert severity. Higher values indicate greater expected impact. Derived from severity, population exposure, and vulnerability.
- **`episode_alert_level`** (string, optional): The GDACS alert level specific to this episode, which may differ from the overall event alert level as conditions evolve.
- **`episode_alert_score`** (double, optional): A numeric score (0.0–3.0) representing the alert severity for this specific episode.
- **`event_name`** (string, optional): The human-readable name assigned to the event by GDACS, such as a cyclone name or descriptive location label.
- **`severity_value`** (double, required): The numeric severity measure for the event. The meaning depends on the event type: magnitude for earthquakes, wind speed for cyclones, water level for floods, VEI for volcanoes.
- **`severity_unit`** (string, required): The unit of measurement for the severity value. Examples: 'M' (Richter magnitude), 'km/h' (wind speed), 'm' (water level), 'VEI' (Volcanic Explosivity Index).
- **`severity_text`** (string, optional): A human-readable text description of the severity, as provided in the GDACS RSS feed severity element text content.
- **`country`** (string, required): Affected country name or normalized unknown sentinel when GDACS omits the country. Matches the {country} MQTT topic axis.
- **`iso3`** (string, optional): The ISO 3166-1 alpha-3 country code(s) for the affected country or countries.
- **`latitude`** (double, required): The latitude of the disaster event epicenter or centroid in decimal degrees (WGS84).
- **`longitude`** (double, required): The longitude of the disaster event epicenter or centroid in decimal degrees (WGS84).
- **`from_date`** (datetime, required): The date and time when the disaster event was first detected or began, in ISO-8601 format.
- **`to_date`** (datetime, optional): The date and time when the disaster event ended or was last observed, in ISO-8601 format. May be absent for ongoing events.
- **`population_value`** (double, optional): The estimated number of people exposed to or affected by the disaster event, as calculated by GDACS impact models.
- **`population_unit`** (string, optional): The unit for the population value, typically 'Pop' (population count) or a radius-based exposure descriptor.
- **`vulnerability`** (double, optional): A GDACS-calculated vulnerability score (0.0–3.0) that reflects the affected region's capacity to cope with the disaster, factoring in infrastructure, governance, and socioeconomic conditions.
- **`bbox_min_lon`** (double, optional): The minimum longitude of the bounding box that encloses the affected area, in decimal degrees.
- **`bbox_max_lon`** (double, optional): The maximum longitude of the bounding box that encloses the affected area, in decimal degrees.
- **`bbox_min_lat`** (double, optional): The minimum latitude of the bounding box that encloses the affected area, in decimal degrees.
- **`bbox_max_lat`** (double, optional): The maximum latitude of the bounding box that encloses the affected area, in decimal degrees.
- **`is_current`** (boolean, optional): Whether this disaster event is currently ongoing according to GDACS. True if the event is still active, false if it has concluded.
- **`version`** (int32, optional): The version number of this event record in GDACS. Incremented each time the event data is updated or revised.
- **`description`** (string, optional): The RSS item description text, typically a brief HTML or plain-text summary of the disaster event with key impact details.
- **`link`** (string, optional): The URL linking to the full GDACS event report page for this disaster event.
- **`pub_date`** (datetime, optional): The date and time when this RSS item was published or last updated, in ISO-8601 format.
- **`alert_color`** (enum, required): Lowercase GDACS alert color derived from alert_level (green, orange, or red). Matches the {alert_color} MQTT topic axis.
##### `event_type` values

- `EQ`: Provider value `EQ` for this coded alert field.
- `TC`: Provider value `TC` for this coded alert field.
- `FL`: Provider value `FL` for this coded alert field.
- `VO`: Provider value `VO` for this coded alert field.
- `FF`: Provider value `FF` for this coded alert field.
- `DR`: Provider value `DR` for this coded alert field.
##### `alert_level` values

- `Green`: Provider value `Green` for this coded alert field.
- `Orange`: Provider value `Orange` for this coded alert field.
- `Red`: Provider value `Red` for this coded alert field.
##### `alert_color` values

- `green`: Provider value `green` for this coded alert field.
- `orange`: Provider value `orange` for this coded alert field.
- `red`: Provider value `red` for this coded alert field.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "event_type": "EQ",
  "event_id": "string",
  "episode_id": "string",
  "alert_level": "Green",
  "alert_score": 0,
  "episode_alert_level": "string",
  "episode_alert_score": 0,
  "event_name": "string",
  "severity_value": 0,
  "severity_unit": "string",
  "severity_text": "string",
  "country": "string",
  "iso3": "string",
  "latitude": 0,
  "longitude": 0,
  "from_date": "2024-01-01T00:00:00Z",
  "to_date": "2024-01-01T00:00:00Z",
  "population_value": 0,
  "population_unit": "string",
  "vulnerability": 0,
  "bbox_min_lon": 0,
  "bbox_max_lon": 0,
  "bbox_min_lat": 0,
  "bbox_max_lat": 0,
  "is_current": false,
  "version": 0,
  "description": "string",
  "link": "string",
  "pub_date": "2024-01-01T00:00:00Z",
  "alert_color": "green"
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
- The MQTT variant publishes with QoS 1 and retained-message Last-Known-Value semantics where declared in the event catalog.

## References

- xRegistry manifest: [`xreg/gdacs.xreg.json`](xreg/gdacs.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- Azure Service Bus Standard namespace: <https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview>
