# NWS CAP Alerts Events

NWS Alerts publishes CAP weather watches, warnings, advisories, and updates from the U.S. National Weather Service for U.S. weather alert areas. These events help consumers monitor hazards, route notifications, and correlate public-warning updates without polling the upstream source directly.

## At a glance

- **Event types:** 1 documented event type (6 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 1 telemetry event type.
- **Identity:** `{alert_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `nws-alerts`. The record key is `{alert_id}`. In plain language, `{alert_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['nws-alerts'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `alerts/us/noaa/nws-alerts/+/minor/+/+/alert`, `alerts/us/noaa/nws-alerts/+/moderate/+/+/alert`, `alerts/us/noaa/nws-alerts/+/severe/+/+/alert`, `alerts/us/noaa/nws-alerts/+/extreme/+/+/alert`, `alerts/us/noaa/nws-alerts/+/unknown/+/+/alert`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('alerts/us/noaa/nws-alerts/+/minor/+/+/alert', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `nws-alerts`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/nws-alerts')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Weather Alert

CloudEvents type: `NWS.WeatherAlert`

#### What it tells you

A weather or non-weather alert from the US National Weather Service, distributed through the Integrated Public Alert and Warning System (IPAWS). Follows the CAP (Common Alerting Protocol) standard.

#### Identity

Each event identifies the real-world resource with `{alert_id}`. `{alert_id}` is the unique URN-based identifier for the alert (e.g., 'urn:oid:2.49.0.1.840.0.xxx'). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `nws-alerts`, key `{alert_id}` |
| `AMQP/1.0` | source address `amqp://localhost:5672/nws-alerts`, message subject `{alert_id}` |
| `MQTT/5.0` | topic `alerts/us/noaa/nws-alerts/{state}/minor/{event_type}/{alert_id}/alert`, retain `false`, QoS `1` |
| `MQTT/5.0` | topic `alerts/us/noaa/nws-alerts/{state}/moderate/{event_type}/{alert_id}/alert`, retain `false`, QoS `1` |
| `MQTT/5.0` | topic `alerts/us/noaa/nws-alerts/{state}/severe/{event_type}/{alert_id}/alert`, retain `false`, QoS `1` |
| `MQTT/5.0` | topic `alerts/us/noaa/nws-alerts/{state}/extreme/{event_type}/{alert_id}/alert`, retain `false`, QoS `1` |
| `MQTT/5.0` | topic `alerts/us/noaa/nws-alerts/{state}/unknown/{event_type}/{alert_id}/alert`, retain `false`, QoS `1` |

#### Payload

`Weather Alert` payloads are JSON object. Required fields: `alert_id`, `sent`, `status`, `message_type`, `severity`, `certainty`, `urgency`, `event`, `state`, `event_type`.

- **`alert_id`** (string, required): The unique URN-based identifier for the alert (e.g., 'urn:oid:2.49.0.1.840.0.xxx'). Stable across the lifecycle of the alert.
- **`area_desc`** (string, optional): A textual description of the affected geographic area (e.g., county names).
- **`same_codes`** (string, optional): Semicolon-separated SAME (Specific Area Message Encoding) codes identifying affected counties/zones. Used by the Emergency Alert System (EAS).
- **`ugc_codes`** (string, optional): Semicolon-separated UGC (Universal Geographic Code) zone identifiers (e.g., 'MDC031', 'TXZ001').
- **`sent`** (datetime, required): The date and time when the alert was sent, in ISO-8601 format.
- **`effective`** (datetime, optional): The date and time when the alert becomes effective.
- **`onset`** (datetime, optional): The expected date and time of onset of the weather event.
- **`expires`** (datetime, optional): The date and time when the alert expires.
- **`ends`** (datetime, optional): The expected end time of the weather event.
- **`status`** (enum, required): The CAP alert status.
- **`message_type`** (enum, required): The CAP message type.
- **`category`** (string, optional): The CAP alert category (e.g., 'Met' for meteorological).
- **`severity`** (enum, required): The CAP severity level.
- **`certainty`** (enum, required): The CAP certainty level.
- **`urgency`** (enum, required): The CAP urgency level.
- **`event`** (string, required): The type of weather event (e.g., 'Tornado Warning', 'Flood Watch', 'Heat Advisory').
- **`sender`** (string, optional): The email address or identifier of the alert sender.
- **`sender_name`** (string, optional): The human-readable name of the sender (e.g., 'NWS Tulsa OK').
- **`headline`** (string, optional): A brief headline summarizing the alert.
- **`description`** (string, optional): The full textual description of the alert.
- **`instruction`** (string, optional): Recommended protective actions.
- **`response`** (string, optional): The recommended response type (e.g., 'Shelter', 'Evacuate', 'None').
- **`scope`** (string, optional): The CAP scope of the alert.
- **`code`** (string, optional): The IPAWS code (e.g., 'IPAWSv1.0').
- **`nws_headline`** (string, optional): The NWS-specific headline from the parameters block.
- **`vtec`** (string, optional): The P-VTEC (Valid Time Event Code) string for NWS event tracking.
- **`web`** (string, optional): A URL to the full alert details.
- **`state`** (string, required): Lowercase USPS state or territory code enriched by the bridge from NWS UGC/SAME zone identifiers; nostate when no state can be resolved.
- **`event_type`** (string, required): Lowercase kebab-case slug derived from the CAP event field for topic partitioning.
##### `status` values

- `Actual`: Provider value `Actual` for this coded alert field.
- `Exercise`: Provider value `Exercise` for this coded alert field.
- `System`: Provider value `System` for this coded alert field.
- `Test`: Provider value `Test` for this coded alert field.
- `Draft`: Provider value `Draft` for this coded alert field.
##### `message_type` values

- `Alert`: Provider value `Alert` for this coded alert field.
- `Update`: Provider value `Update` for this coded alert field.
- `Cancel`: Provider value `Cancel` for this coded alert field.
- `Ack`: Provider value `Ack` for this coded alert field.
- `Error`: Provider value `Error` for this coded alert field.
##### `severity` values

- `Extreme`: Provider value `Extreme` for this coded alert field.
- `Severe`: Provider value `Severe` for this coded alert field.
- `Moderate`: Provider value `Moderate` for this coded alert field.
- `Minor`: Provider value `Minor` for this coded alert field.
- `Unknown`: Provider value `Unknown` for this coded alert field.
##### `certainty` values

- `Observed`: Provider value `Observed` for this coded alert field.
- `Likely`: Provider value `Likely` for this coded alert field.
- `Possible`: Provider value `Possible` for this coded alert field.
- `Unlikely`: Provider value `Unlikely` for this coded alert field.
- `Unknown`: Provider value `Unknown` for this coded alert field.
##### `urgency` values

- `Immediate`: Provider value `Immediate` for this coded alert field.
- `Expected`: Provider value `Expected` for this coded alert field.
- `Future`: Provider value `Future` for this coded alert field.
- `Past`: Provider value `Past` for this coded alert field.
- `Unknown`: Provider value `Unknown` for this coded alert field.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "alert_id": "string",
  "area_desc": "string",
  "same_codes": "string",
  "ugc_codes": "string",
  "sent": "2024-01-01T00:00:00Z",
  "effective": "2024-01-01T00:00:00Z",
  "onset": "2024-01-01T00:00:00Z",
  "expires": "2024-01-01T00:00:00Z",
  "ends": "2024-01-01T00:00:00Z",
  "status": "Actual",
  "message_type": "Alert",
  "category": "string",
  "severity": "Extreme",
  "certainty": "Observed",
  "urgency": "Immediate",
  "event": "string",
  "sender": "string",
  "sender_name": "string",
  "headline": "string",
  "description": "string",
  "instruction": "string",
  "response": "string",
  "scope": "string",
  "code": "string",
  "nws_headline": "string",
  "vtec": "string",
  "web": "string",
  "state": "string",
  "event_type": "string"
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

- xRegistry manifest: [`xreg/nws-alerts.xreg.json`](xreg/nws-alerts.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- Azure Service Bus Standard namespace: <https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview>
