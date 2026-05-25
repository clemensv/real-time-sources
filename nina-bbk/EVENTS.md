# NINA/BBK German Civil Protection Warnings Bridge Events

MQTT/5.0 transport variant for Germany NINA/BBK CAP warnings. Non-retained QoS-1 warning events route by German federal state, native CAP severity, and warning id under alerts/de/nina/nina-bbk/... The state axis is derived from CAP area administrative codes (warnVerwaltungsbereiche) with sender-code fallback.

## At a glance

- **Event types:** 1 documented event type (2 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0
- **Reference vs telemetry:** 0 reference/catalog event types and 1 telemetry event type.
- **Identity:** `{warning_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
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

- `mowas`
- `katwarn`
- `biwapp`
- `dwd`
- `lhp`
- `police`
##### `status` values

- `Actual`
- `Exercise`
- `System`
- `Test`
- `Draft`
##### `msg_type` values

- `Alert`
- `Update`
- `Cancel`
- `Ack`
- `Error`
##### `scope` values

- `Public`
- `Restricted`
- `Private`
##### `category` values

- `Met`
- `Geo`
- `Safety`
- `Security`
- `Rescue`
- `Fire`
- `Health`
- `Env`
- `Transport`
- `Infra`
- `CBRNE`
- `Other`
##### `severity` values

- `Extreme`
- `Severe`
- `Moderate`
- `Minor`
- `Unknown`
##### `urgency` values

- `Immediate`
- `Expected`
- `Future`
- `Past`
- `Unknown`
##### `certainty` values

- `Observed`
- `Likely`
- `Possible`
- `Unlikely`
- `Unknown`
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

- The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- The MQTT variant publishes with QoS 1 and retained-message Last-Known-Value semantics where declared in the event catalog.

## References

- xRegistry manifest: [`xreg/nina_bbk.xreg.json`](xreg/nina_bbk.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
