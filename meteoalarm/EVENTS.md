# Meteoalarm European Weather Warnings Bridge Events

MQTT/5.0 transport variant for Meteoalarm CAP weather warnings. Non-retained QoS-1 warning events route by country feed slug, native CAP severity, normalized Meteoalarm awareness type, and CAP identifier under alerts/intl/meteoalarm/meteoalarm/... The awareness_type axis is derived from the Meteoalarm awareness_type parameter label and normalized for MQTT topic safety.

## At a glance

- **Event types:** 1 documented event type (2 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0
- **Reference vs telemetry:** 0 reference/catalog event types and 1 telemetry event type.
- **Identity:** `{identifier}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `meteoalarm`. The record key is `{identifier}`. In plain language, `{identifier}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['meteoalarm'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `alerts/intl/meteoalarm/meteoalarm/+/+/+/+/warning`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('alerts/intl/meteoalarm/meteoalarm/+/+/+/+/warning', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.

## Event catalog

### Weather Warning

CloudEvents type: `Meteoalarm.WeatherWarning`

#### What it tells you

A severe weather warning from the EUMETNET Meteoalarm system, aggregating warnings from 30+ European national meteorological services. Each warning follows the CAP (Common Alerting Protocol) structure with awareness levels and hazard types. A severe weather warning from the EUMETNET Meteoalarm system.

#### Identity

Each event identifies the real-world resource with `{identifier}`. `{identifier}` is the unique CAP alert identifier assigned by the issuing national meteorological service. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `meteoalarm`, key `{identifier}` |
| `MQTT/5.0` | topic `alerts/intl/meteoalarm/meteoalarm/{country}/{severity}/{awareness_type}/{identifier}/warning`, retain `false`, QoS `1` |

#### Payload

`Weather Warning` payloads are JSON object. Required fields: `identifier`, `sender`, `sent`, `status`, `msg_type`, `scope`, `country`, `event`, `severity`, `urgency`, `certainty`, `awareness_type`, `area_desc`.

- **`identifier`** (string, required): The unique CAP alert identifier assigned by the issuing national meteorological service.
- **`sender`** (string, required): The identifier of the issuing national meteorological service (e.g., 'opendata@dwd.de').
- **`sent`** (datetime, required): The date and time when the warning was issued, in ISO-8601 format.
- **`status`** (enum, required): The CAP alert status. 'Actual' for real warnings, 'Test' for test messages.
- **`msg_type`** (enum, required): The CAP message type indicating the nature of the alert.
- **`scope`** (enum, required): The CAP scope of the alert. Typically 'Public' for weather warnings.
- **`country`** (string, required): Country feed slug where the warning applies (for example germany or france). Matches the {country} MQTT topic axis.
- **`event`** (string, required): The weather event description, typically in the national language of the issuing service (e.g., 'STURMBÖEN', 'Thunderstorm').
- **`category`** (enum, optional): The CAP alert category. 'Met' for meteorological warnings.
- **`severity`** (enum, required): Native CAP severity level (Minor, Moderate, Severe, Extreme, or Unknown). Matches the {severity} MQTT topic axis without further bucketing.
- **`urgency`** (enum, required): The CAP urgency level indicating the time-frame for protective action.
- **`certainty`** (enum, required): The CAP certainty level indicating the confidence in the forecast.
- **`headline`** (string, optional): A brief human-readable headline summarizing the warning, often in the national language.
- **`description`** (string, optional): A detailed description of the weather warning, often in the national language.
- **`instruction`** (string, optional): Recommended protective actions for the public.
- **`effective`** (datetime, optional): The date and time when the warning becomes effective, in ISO-8601 format.
- **`onset`** (datetime, optional): The expected date and time of onset of the weather event, in ISO-8601 format.
- **`expires`** (datetime, optional): The date and time when the warning expires, in ISO-8601 format.
- **`web`** (string, optional): A URL to the full warning details on the issuing service's website.
- **`contact`** (string, optional): Contact information for the issuing meteorological service.
- **`awareness_level`** (string, optional): The Meteoalarm awareness level as a string combining the numeric level and color, e.g., '2; yellow; Moderate'. Values range from '1; green' (no significant weather) to '4; red' (very dangerous).
- **`awareness_type`** (string, required): Meteoalarm awareness type label normalized to lowercase kebab-case for MQTT topic routing (for example wind, snow-ice, thunderstorm, flooding). Matches the {awareness_type} MQTT topic axis.
- **`area_desc`** (string, required): A textual description of the affected geographic area.
- **`geocodes`** (string, optional): A semicolon-separated list of geocode values (EMMA_ID or WARNCELLID) identifying the specific warning zones.
- **`language`** (string, optional): The language of the info block used to populate this event (e.g., 'de-DE', 'en-GB').
- **`awareness_type_raw`** (string, optional): Raw Meteoalarm awareness_type parameter value as provided by CAP, for example "2; Snow/Ice".
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
  "identifier": "string",
  "sender": "string",
  "sent": "2024-01-01T00:00:00Z",
  "status": "Actual",
  "msg_type": "Alert",
  "scope": "Public",
  "country": "string",
  "event": "string",
  "category": "Met",
  "severity": "Extreme",
  "urgency": "Immediate",
  "certainty": "Observed",
  "headline": "string",
  "description": "string",
  "instruction": "string",
  "effective": "2024-01-01T00:00:00Z",
  "onset": "2024-01-01T00:00:00Z",
  "expires": "2024-01-01T00:00:00Z",
  "web": "string",
  "contact": "string",
  "awareness_level": "string",
  "awareness_type": "string",
  "area_desc": "string",
  "geocodes": "string",
  "language": "string",
  "awareness_type_raw": "string"
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

- xRegistry manifest: [`xreg/meteoalarm.xreg.json`](xreg/meteoalarm.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
