# JMA Bosai Warning & Tsunami Events

JMA Bosai Warnings publishes weather warnings and advisories from the Japan Meteorological Agency for Japanese weather-warning areas. These events help consumers monitor hazards, route notifications, and correlate public-warning updates without polling the upstream source directly.

## At a glance

- **Event types:** 3 documented event types (9 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 3 telemetry event types.
- **Identity:** `jp.jma.warning/{office_code}/{area_code}`, `jp.jma.tsunami/{event_id}/{serial}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `jma-bosai-warning`, `jma-bosai-tsunami`. The record key is `jp.jma.warning/{office_code}/{area_code}`, `jp.jma.tsunami/{event_id}/{serial}`. Each key template is explained in the event catalog below. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['jma-bosai-warning', 'jma-bosai-tsunami'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `alerts/jp/jma/jma-bosai-warning/+/+/+/+/+`, `alerts/jp/jma/jma-bosai-warning/+/+/+/+/tsunami`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('alerts/jp/jma/jma-bosai-warning/+/+/+/+/+', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `jma-bosai-warning`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/jma-bosai-warning')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Office

CloudEvents type: `JP.JMA.Warning.Office`

#### What it tells you

JMA Bosai warning office reference data from area.json offices.

#### Identity

Each event identifies the real-world resource with `jp.jma.warning/{office_code}/{area_code}`. `{office_code}` is six-digit JMA Bosai office code from area.json offices; `{area_code}` is six-digit JMA Bosai office code repeated as the area component for office reference events so reference records use the same numeric warning subject and key shape as area warning telemetry. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `jma-bosai-warning`, key `jp.jma.warning/{office_code}/{area_code}` |
| `MQTT/5.0` | topic `alerts/jp/jma/jma-bosai-warning/{prefecture}/{severity}/{office_code}/{area_code}/{event}`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/jma-bosai-warning`, message subject `jp.jma.warning/{office_code}/{area_code}` |

#### Payload

`Office` payloads are JSON object. Required fields: `office_code`, `area_code`, `name_jp`, `name_en`, `parent_office_code`, `office_type`, `prefecture`, `severity`, `event`.

- **`office_code`** (string, required): Six-digit JMA Bosai office code from area.json offices. This is the first stable key component for warning reference and telemetry events. Constraints: pattern `^[0-9]{6}$`.
- **`area_code`** (string, required): Six-digit JMA Bosai office code repeated as the area component for office reference events so reference records use the same numeric warning subject and key shape as area warning telemetry. Constraints: pattern `^[0-9]{6,7}$`.
- **`name_jp`** (string, required): Japanese office or warning-region name from area.json offices[].name, such as 東京都 or 宗谷地方.
- **`name_en`** (string, required): English office or warning-region name from area.json offices[].enName, such as Tokyo or Soya.
- **`parent_office_code`** (string or null, required): Parent JMA regional center code from area.json offices[].parent. Null is emitted only if the upstream catalog omits a parent. Constraints: pattern `^[0-9]{6}$`.
- **`office_type`** (enum, required): Normalized office class. PREFECTURE is used for standard prefectural offices, SUBREGION for Hokkaido/Okinawa-style regional warning offices, and OFFICE for other JMA issuing-office catalog entries.
- **`prefecture`** (string, required): ASCII-safe Romanized prefecture or JMA warning subregion slug derived from the JMA office code/name for MQTT topic routing. Japanese administrative names are preserved separately in name_jp/area_name. Constraints: pattern `^[a-z0-9][a-z0-9-]*$`.
- **`severity`** (enum, required): Japan-native severity axis for JMA warning MQTT topics: info for office reference records, advisory for 注意報-level notices and cancellations, warning for 警報-level warnings, and emergency for 特別警報/special-warning category codes.
- **`event`** (enum, required): Fixed MQTT topic event segment for retained office reference records.
##### `office_type` values

- `PREFECTURE`: Provider value `PREFECTURE` for this coded alert field.
- `SUBREGION`: Provider value `SUBREGION` for this coded alert field.
- `OFFICE`: Provider value `OFFICE` for this coded alert field.
##### `severity` values

- `info`: Reference-information routing value used by retained JMA office records.
- `advisory`: Normalized advisory/cancellation value for 注意報-level or cleared JMA warning items.
- `warning`: Normalized warning value for 警報-level JMA warning items.
- `emergency`: Normalized emergency value for 特別警報 or special-warning category codes 32-38.
##### `event` values

- `info`: Provider value `info` for retained office reference records.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "office_code": "string",
  "area_code": "string",
  "name_jp": "string",
  "name_en": "string",
  "parent_office_code": "string",
  "office_type": "PREFECTURE",
  "prefecture": "string",
  "severity": "info",
  "event": "info"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Weather Warning

CloudEvents type: `JP.JMA.Warning.WeatherWarning`

#### What it tells you

JMA Bosai weather warning/advisory telemetry for one forecast area within an office bulletin.

#### Identity

Each event identifies the real-world resource with `jp.jma.warning/{office_code}/{area_code}`. `{office_code}` is six-digit JMA Bosai office targetArea code used in the warning/{office_code}.json endpoint; `{area_code}` is JMA inner forecast-area code from timeSeries areas[].code. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `jma-bosai-warning`, key `jp.jma.warning/{office_code}/{area_code}` |
| `MQTT/5.0` | topic `alerts/jp/jma/jma-bosai-warning/{prefecture}/{severity}/{office_code}/{area_code}/{event}`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/jma-bosai-warning`, message subject `jp.jma.warning/{office_code}/{area_code}` |

#### Payload

`Weather Warning` payloads are JSON object. Required fields: `prefecture`, `severity`, `office_code`, `area_code`, `event`, `area_name`, `report_datetime`, `report_datetime_local`, `headline_text`, `warnings`, `time_defines`.

- **`prefecture`** (string, required): ASCII-safe Romanized prefecture or JMA warning subregion slug derived from the JMA office code/name for MQTT topic routing. Japanese administrative names are preserved separately in name_jp/area_name. Constraints: pattern `^[a-z0-9][a-z0-9-]*$`.
- **`severity`** (enum, required): Japan-native severity axis for JMA warning MQTT topics: info for office reference records, advisory for 注意報-level notices and cancellations, warning for 警報-level warnings, and emergency for 特別警報/special-warning category codes.
- **`office_code`** (string, required): Six-digit JMA Bosai office targetArea code used in the warning/{office_code}.json endpoint. This is the first stable key component. Constraints: pattern `^[0-9]{6}$`.
- **`area_code`** (string, required): JMA inner forecast-area code from timeSeries areas[].code. This is the second stable key component for weather warning telemetry. Constraints: pattern `^[0-9]{6,7}$`.
- **`event`** (enum, required): Fixed MQTT topic event segment for JMA Bosai weather warning state records.
- **`area_name`** (string, required): Japanese inner forecast-area name from the warning payload when present or from area.json class catalogs when the payload only carries a code.
- **`report_datetime`** (datetime, required): JMA report publication time converted to an RFC3339 UTC timestamp. JMA publishes reportDatetime with a local Japan time offset.
- **`report_datetime_local`** (datetime, required): Original JMA reportDatetime timestamp preserving the upstream local offset, normally Japan Standard Time (+09:00).
- **`headline_text`** (string or null, required): Japanese free-text headline from headlineText summarizing areas and hazards requiring attention. Null is emitted when JMA omits the headline.
- **`warnings`** (array of object, required): All JMA warning/advisory items published for the inner area in this bulletin. WarningItem is intentionally defined inline to avoid duplicate schema definitions during Avro and producer generation.
- **`time_defines`** (array of datetime, required): Time definition values from the warning timeSeries converted to RFC3339 UTC timestamps. The original JMA array describes the valid or forecast times associated with the warning area block.
##### `severity` values

- `info`: Reference-information routing value used by retained JMA office records.
- `advisory`: Normalized advisory/cancellation value for 注意報-level or cleared JMA warning items.
- `warning`: Normalized warning value for 警報-level JMA warning items.
- `emergency`: Normalized emergency value for 特別警報 or special-warning category codes 32-38.
##### `event` values

- `warning`: Provider value `warning` for JMA weather warning state records.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "prefecture": "string",
  "severity": "info",
  "office_code": "string",
  "area_code": "string",
  "event": "warning",
  "area_name": "string",
  "report_datetime": "2024-01-01T00:00:00Z",
  "report_datetime_local": "2024-01-01T00:00:00Z",
  "headline_text": "string",
  "warnings": [
    {
      "code": "string",
      "code_description_jp": "string",
      "code_description_en": "string",
      "status": "ISSUED",
      "severity": "advisory"
    }
  ],
  "time_defines": [
    "2024-01-01T00:00:00Z"
  ]
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Tsunami Alert

CloudEvents type: `JP.JMA.Tsunami.TsunamiAlert`

#### What it tells you

JMA Bosai active tsunami alert telemetry from list.json enriched with detail bulletin coastal forecasts.

#### Identity

Each event identifies the real-world resource with `jp.jma.tsunami/{event_id}/{serial}`. `{event_id}` is stable JMA tsunami event identifier copied from list.json eid and corresponding detail Head.EventID; `{serial}` is JMA tsunami bulletin serial parsed from list.json ser or detail Head.Serial. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `jma-bosai-tsunami`, key `jp.jma.tsunami/{event_id}/{serial}` |
| `MQTT/5.0` | topic `alerts/jp/jma/jma-bosai-warning/{prefecture}/{severity}/{event_id}/{serial}/tsunami`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/jma-bosai-warning`, message subject `jp.jma.tsunami/{event_id}/{serial}` |

#### Payload

`Tsunami Alert` payloads are JSON object. Required fields: `event_id`, `serial`, `info_type`, `report_datetime`, `report_datetime_local`, `title_jp`, `title_en`, `bulletin_type`, `detail_url`, `affected_coastal_regions`, `observations`, `prefecture`, `severity`.

- **`event_id`** (string, required): Stable JMA tsunami event identifier copied from list.json eid and corresponding detail Head.EventID. This is the first stable key component. Constraints: pattern `^[0-9]{14}$`.
- **`serial`** (integer, required): JMA tsunami bulletin serial parsed from list.json ser or detail Head.Serial. This is the second stable key component. Constraints: minimum `0`.
- **`info_type`** (enum, required): Normalized information type derived from JMA ift text: ISSUED for 発表, CORRECTED for 訂正, and CANCELLED for 取消.
- **`report_datetime`** (datetime, required): JMA tsunami report publication time converted from list.json rdt to RFC3339 UTC.
- **`report_datetime_local`** (datetime, required): Original JMA tsunami report publication timestamp from list.json rdt preserving the local offset.
- **`title_jp`** (string, required): Japanese JMA tsunami bulletin title copied from list.json ttl.
- **`title_en`** (string, required): English tsunami title generated from the known JMA title class when no English list title is present.
- **`bulletin_type`** (string, required): JMA tsunami product code parsed from the detail JSON filename, such as VTSE41, VTSE51, or VTSE52.
- **`detail_url`** (uri, required): Absolute URL for the JMA Bosai tsunami detail JSON referenced by list.json json.
- **`affected_coastal_regions`** (array of object, required): Coastal forecast regions and expected wave/arrival data parsed from VTSE41 tsunami detail bulletins. AffectedCoastalRegion is defined inline to avoid duplicate schema definitions during Avro and producer generation.
- **`observations`** (array of object, required): Observed tsunami station readings parsed from VTSE51/VTSE52 observed-wave detail bulletins. The bridge emits an empty array for forecast-only bulletins or when no station observations are present.
- **`prefecture`** (string, required): ASCII-safe Japan region routing axis for tsunami MQTT/AMQP topics. Constraints: pattern `^[a-z0-9][a-z0-9-]*$`.
- **`severity`** (enum, required): Japan-native tsunami warning severity axis: advisory, warning, or emergency.
##### `info_type` values

- `ISSUED`: Provider value `ISSUED` for this coded alert field.
- `CORRECTED`: Provider value `CORRECTED` for this coded alert field.
- `CANCELLED`: Provider value `CANCELLED` for this coded alert field.
##### `severity` values

- `advisory`: Tsunami advisory or forecast-level routing severity.
- `warning`: Tsunami warning routing severity.
- `emergency`: Major tsunami warning routing severity.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "event_id": "string",
  "serial": 0,
  "info_type": "ISSUED",
  "report_datetime": "2024-01-01T00:00:00Z",
  "report_datetime_local": "2024-01-01T00:00:00Z",
  "title_jp": "string",
  "title_en": "string",
  "bulletin_type": "string",
  "detail_url": "string",
  "affected_coastal_regions": [
    {
      "code": "string",
      "name": "string",
      "category": "MAJOR_WARNING",
      "expected_max_wave_height_m": 0,
      "expected_arrival_datetime": "2024-01-01T00:00:00Z",
      "expected_arrival_datetime_local": "2024-01-01T00:00:00Z"
    }
  ],
  "observations": [
    {
      "station_code": "string",
      "station_name_jp": "string",
      "station_name_en": "string",
      "observed_max_wave_height_m": 0,
      "observed_at": "2024-01-01T00:00:00Z",
      "observed_at_local": "2024-01-01T00:00:00Z",
      "arrival_status": "ESTIMATED"
    }
  ],
  "prefecture": "string",
  "severity": "advisory"
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

- xRegistry manifest: [`xreg/jma-bosai-warning.xreg.json`](xreg/jma-bosai-warning.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- Azure Service Bus Standard namespace: <https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview>
