# Australian Wildfires feeder Events

Australia Wildfires publishes bushfire incident status updates from Australian emergency-services incident feeds for Australian wildfire incidents. These events help consumers monitor hazards, route notifications, and correlate public-warning updates without polling the upstream source directly.

## At a glance

- **Event types:** 1 documented event type (3 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 1 telemetry event type.
- **Identity:** `{state}/{incident_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `australia-wildfires`. The record key is `{state}/{incident_id}`. In plain language, `{state}/{incident_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['australia-wildfires'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `wildfire/au/+/+/+/incident`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('wildfire/au/+/+/+/incident', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `australia-wildfires`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/australia-wildfires')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Fire Incident

CloudEvents type: `AU.Gov.Emergency.Wildfires.FireIncident`

#### What it tells you

An incident update from Australian emergency-services incident feeds. It reports the current status, location, and classification for a wildfire or emergency incident.

#### Identity

Each event identifies the real-world resource with `{state}/{incident_id}`. `{state}` is australian state abbreviation indicating which emergency service reported this incident; `{incident_id}` is stable identifier for the fire incident, derived from the source system. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `australia-wildfires`, key `{state}/{incident_id}` |
| `MQTT/5.0` | topic `wildfire/au/{state}/{status}/{incident_id}/incident`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/australia-wildfires`, message subject `{state}/{incident_id}` |

#### Payload

`Fire Incident` payloads are JSON object. Required fields: `incident_id`, `state`, `title`, `alert_level`, `status`, `updated`, `source_url`.

- **`incident_id`** (string, required): Stable identifier for the fire incident, derived from the source system. NSW: numeric incident ID extracted from the RFS GUID URL. VIC: numeric sourceId from the VicEmergency feed. QLD: alphanumeric UniqueID from the QFD feed (e.g. 'IF39-5661721').
- **`state`** (string, required): Australian state abbreviation indicating which emergency service reported this incident. One of 'NSW' (New South Wales Rural Fire Service), 'VIC' (VicEmergency / Country Fire Authority / Fire Rescue Victoria), or 'QLD' (Queensland Fire Department).
- **`title`** (string, required): Human-readable title or headline for the incident as provided by the source agency. NSW: location-based title from the RFS feed (e.g. '(GWYDIR HWY), MATHESON'). VIC: warning name or sourceTitle from VicEmergency. QLD: WarningTitle from the QFD feed.
- **`alert_level`** (string, required): Fire danger alert level as classified by the issuing agency. Common values across states: 'Advice' (fire is under control or low threat), 'Watch and Act' (conditions are changing, prepare to leave), 'Emergency Warning' (immediate danger, take action now). NSW uses 'category' field, VIC uses 'action' or category1, QLD uses 'WarningLevel'.
- **`status`** (string, required): Topic-safe lowercase-kebab operational status for the incident (e.g. under-control, being-controlled, out-of-control, unknown). The MQTT feeder maps missing upstream status values to unknown so the {status} topic segment is never null or empty. Constraints: pattern `^[a-z0-9][a-z0-9-]*$`.
- **`location`** (string or null, optional): Human-readable location description for the incident. NSW: full location string extracted from the HTML description (e.g. 'B76 (GWYDIR HWY), MATHESON 2370'). VIC: locality names from the location field. QLD: derived from the WarningTitle or Header text.
- **`latitude`** (double or null, optional, degree (\u00b0)): Latitude of the incident centroid in decimal degrees (WGS84). Extracted from the GeoJSON Point geometry where available, or computed as the centroid of a Polygon geometry. Negative values indicate Southern Hemisphere.
- **`longitude`** (double or null, optional, degree (\u00b0)): Longitude of the incident centroid in decimal degrees (WGS84). Extracted from the GeoJSON Point geometry where available, or computed as the centroid of a Polygon geometry.
- **`size_hectares`** (double or null, optional, hectare (ha)): Estimated area of the fire in hectares as reported by the source agency. NSW: extracted from the SIZE field in the HTML description. VIC: parsed from sizeFmt if available. QLD: not typically provided, may be null.
- **`type`** (string or null, optional): Classification of the fire type as reported by the source agency. NSW: extracted from the TYPE field in the HTML description (e.g. 'Bush Fire', 'Grass Fire', 'Hazard Reduction'). VIC: event field from the CAP envelope (e.g. 'Grass Fire', 'Scrub Fire', 'Bush Fire'). QLD: derived from CallToAction text.
- **`responsible_agency`** (string or null, optional): Name of the fire-fighting agency responsible for the incident. NSW: extracted from RESPONSIBLE AGENCY in the HTML description (e.g. 'Rural Fire Service', 'Fire and Rescue NSW'). VIC: senderName from the CAP envelope (e.g. 'Country Fire Authority', 'Fire Rescue Victoria'). QLD: defaults to 'Queensland Fire Department'.
- **`updated`** (datetime, required): Timestamp when the incident record was last updated by the source agency, in ISO 8601 format with UTC timezone. NSW: parsed from the UPDATED field in the HTML description or pubDate. VIC: 'updated' field from the VicEmergency feed. QLD: parsed from the WarningTitle date reference or current fetch time.
- **`source_url`** (string, required): URL pointing to the original incident details or the source feed. NSW: GUID permalink from the RFS feed (e.g. 'https://incidents.rfs.nsw.gov.au/api/v1/incidents/653509'). VIC: constructed URL to the VicEmergency warning page. QLD: static URL of the QFD bushfire alert feed.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "incident_id": "string",
  "state": "string",
  "title": "string",
  "alert_level": "string",
  "status": "string",
  "location": "string",
  "latitude": 0,
  "longitude": 0,
  "size_hectares": 0,
  "type": "string",
  "responsible_agency": "string",
  "updated": "2024-01-01T00:00:00Z",
  "source_url": "string"
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

## References

- xRegistry manifest: [`xreg/australia_wildfires.xreg.json`](xreg/australia_wildfires.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
