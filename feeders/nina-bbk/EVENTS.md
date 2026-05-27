# NINA/BBK feeder Events

NINA BBK publishes civil-protection warnings from Germany's Federal Office of Civil Protection and Disaster Assistance (BBK) for German warning areas. These events help consumers monitor hazards, route notifications, and correlate public-warning updates without polling the upstream source directly.

## At a glance

- **Event types:** 1 documented event type (3 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 1 telemetry event type.
- **Identity:** `{warning_id}` identifies the resource each event is about.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `nina-bbk`. The record key is `{warning_id}`. In plain language, `{warning_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['nina-bbk'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `alerts/de/nina/nina-bbk/+/+/+/warning`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('alerts/de/nina/nina-bbk/+/+/+/warning', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `nina-bbk`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/nina-bbk')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Civil Warning

CloudEvents type: `NINA.CivilWarning`

#### What it tells you

A civil protection warning from Germany's NINA/BBK warning system. Aggregates warnings from MOWAS (federal), KATWARN (municipal), BIWAPP (municipal), DWD (weather service), LHP (flood centers), and police services. Each warning follows the CAP (Common Alerting Protocol) structure with multi-language support.

#### Identity

Each event identifies the real-world resource with `{warning_id}`. `{warning_id}` is the unique warning identifier assigned by the NINA/BBK system (e.g., 'mow.DE-HE-DA-W184-20240723-000'). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `nina-bbk`, key `{warning_id}` |
| `MQTT/5.0` | topic `alerts/de/nina/nina-bbk/{state}/{severity}/{warning_id}/warning`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `amqp://localhost:5672/nina-bbk`, message subject `{warning_id}`; application properties state `{state}`, severity `{severity}` |

#### Payload

`Civil Warning` payloads are JSON object. Required fields: `warning_id`, `provider`, `sender`, `sent`, `status`, `msg_type`, `scope`, `event`, `severity`, `urgency`, `certainty`, `state`.

- **`warning_id`** (string, required): The unique warning identifier assigned by the NINA/BBK system (e.g., 'mow.DE-HE-DA-W184-20240723-000').
- **`provider`** (enum, required): The NINA provider that issued the warning.
- **`version`** (integer, optional): The version number of this warning, incremented with each update.
- **`sender`** (string, required): The identifier of the issuing authority (e.g., 'DE-HE-DA-W184').
- **`sender_name`** (string, optional): The human-readable long name of the issuing authority (e.g., 'Integrierte Leitstelle Stadt Darmstadt').
- **`sent`** (datetime, required): The date and time when the warning was issued, in ISO-8601 format.
- **`status`** (enum, required): The CAP alert status.
- **`msg_type`** (enum, required): The CAP message type indicating the nature of the warning.
- **`scope`** (enum, required): The CAP scope of the warning. Typically 'Public'.
- **`references`** (string, optional): CAP references to prior related warnings, in the format 'sender,identifier,sent'.
- **`event`** (string, required): The event type description (e.g., 'Gefahreninformation', 'Hochwasserinformation').
- **`event_code`** (string, optional): The BBK event code identifying the hazard type (e.g., 'BBK-EVC-067' for animal disease, 'BBK-EVC-045' for flood).
- **`category`** (enum, optional): The CAP alert category.
- **`severity`** (enum, required): Native CAP severity level (Minor, Moderate, Severe, Extreme, or Unknown). Matches the {severity} MQTT topic axis without further bucketing.
- **`urgency`** (enum, required): The CAP urgency level.
- **`certainty`** (enum, required): The CAP certainty level.
- **`headline`** (string, optional): A brief human-readable headline summarizing the warning.
- **`description`** (string, optional): A detailed description of the warning situation.
- **`instruction`** (string, optional): Recommended protective actions for the public.
- **`web`** (string, optional): A URL to further information about the warning.
- **`contact`** (string, optional): Contact information for the issuing authority.
- **`area_desc`** (string, optional): A textual description of the affected geographic area.
- **`verwaltungsbereiche`** (string, optional): Comma-separated German administrative area codes (Amtliche Gemeindeschlüssel) affected by the warning.
- **`language`** (string, optional): The language of the info block used to populate this event (e.g., 'de', 'EN').
- **`state`** (string, required): German federal-state slug derived from CAP area administrative codes (warnVerwaltungsbereiche), with sender-code fallback. Matches the {state} MQTT topic axis.
##### `provider` values

- `mowas`: Provider value `mowas` for this coded alert field.
- `katwarn`: Provider value `katwarn` for this coded alert field.
- `biwapp`: Provider value `biwapp` for this coded alert field.
- `dwd`: Provider value `dwd` for this coded alert field.
- `lhp`: Provider value `lhp` for this coded alert field.
- `police`: Provider value `police` for this coded alert field.
##### `status` values

- `Actual`: Provider value `Actual` for this coded alert field.
- `Exercise`: Provider value `Exercise` for this coded alert field.
- `System`: Provider value `System` for this coded alert field.
- `Test`: Provider value `Test` for this coded alert field.
- `Draft`: Provider value `Draft` for this coded alert field.
##### `msg_type` values

- `Alert`: Provider value `Alert` for this coded alert field.
- `Update`: Provider value `Update` for this coded alert field.
- `Cancel`: Provider value `Cancel` for this coded alert field.
- `Ack`: Provider value `Ack` for this coded alert field.
- `Error`: Provider value `Error` for this coded alert field.
##### `scope` values

- `Public`: Provider value `Public` for this coded alert field.
- `Restricted`: Provider value `Restricted` for this coded alert field.
- `Private`: Provider value `Private` for this coded alert field.
##### `category` values

- `Met`: Provider value `Met` for this coded alert field.
- `Geo`: Provider value `Geo` for this coded alert field.
- `Safety`: Provider value `Safety` for this coded alert field.
- `Security`: Provider value `Security` for this coded alert field.
- `Rescue`: Provider value `Rescue` for this coded alert field.
- `Fire`: Provider value `Fire` for this coded alert field.
- `Health`: Provider value `Health` for this coded alert field.
- `Env`: Provider value `Env` for this coded alert field.
- `Transport`: Provider value `Transport` for this coded alert field.
- `Infra`: Provider value `Infra` for this coded alert field.
- `CBRNE`: Provider value `CBRNE` for this coded alert field.
- `Other`: Provider value `Other` for this coded alert field.
##### `severity` values

- `Extreme`: Provider value `Extreme` for this coded alert field.
- `Severe`: Provider value `Severe` for this coded alert field.
- `Moderate`: Provider value `Moderate` for this coded alert field.
- `Minor`: Provider value `Minor` for this coded alert field.
- `Unknown`: Provider value `Unknown` for this coded alert field.
##### `urgency` values

- `Immediate`: Provider value `Immediate` for this coded alert field.
- `Expected`: Provider value `Expected` for this coded alert field.
- `Future`: Provider value `Future` for this coded alert field.
- `Past`: Provider value `Past` for this coded alert field.
- `Unknown`: Provider value `Unknown` for this coded alert field.
##### `certainty` values

- `Observed`: Provider value `Observed` for this coded alert field.
- `Likely`: Provider value `Likely` for this coded alert field.
- `Possible`: Provider value `Possible` for this coded alert field.
- `Unlikely`: Provider value `Unlikely` for this coded alert field.
- `Unknown`: Provider value `Unknown` for this coded alert field.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "warning_id": "string",
  "provider": "mowas",
  "version": 0,
  "sender": "string",
  "sender_name": "string",
  "sent": "2024-01-01T00:00:00Z",
  "status": "Actual",
  "msg_type": "Alert",
  "scope": "Public",
  "references": "string",
  "event": "string",
  "event_code": "string",
  "category": "Met",
  "severity": "Extreme",
  "urgency": "Immediate",
  "certainty": "Observed",
  "headline": "string",
  "description": "string",
  "instruction": "string",
  "web": "string",
  "contact": "string",
  "area_desc": "string",
  "verwaltungsbereiche": "string",
  "language": "string",
  "state": "string"
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

No source-specific polling cadence, rate limit, or stream characteristic is documented in the checked-in README or CONTAINER guide.

## References

- xRegistry manifest: [`xreg/nina_bbk.xreg.json`](xreg/nina_bbk.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
