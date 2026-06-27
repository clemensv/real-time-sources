# CAP Alerts Events

Generalized CAP 1.2 alert feeder for key-less public weather and emergency alert feeds. It supports configurable CAP XML/Atom/JSON sources and emits lossless alert and zone-reference CloudEvents over Kafka, MQTT, and AMQP.

## At a glance

- **Event types:** 2 documented event types (8 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 2 telemetry event types.
- **Identity:** `{cap_source_id}/{identifier}`, `{cap_source_id}/{zone_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `cap-alerts`. The record key is `{cap_source_id}/{identifier}`, `{cap_source_id}/{zone_id}`. Each key template is explained in the event catalog below. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['cap-alerts'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `alerts/cap/+/+/alert`, `alerts/cap/+/zones/+/info`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('alerts/cap/+/+/alert', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `cap-alerts`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/cap-alerts')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Cap Alert

CloudEvents type: `org.oasis.cap.alerts.CapAlert`

#### What it tells you

Generalized Common Alerting Protocol (CAP) 1.2 alert message. It preserves the full alert -> info[] -> area[]/resource[] CAP hierarchy plus standardized CAP extension arrays (eventCode, parameter, geocode) so national weather and emergency alert feeds can be represented losslessly. Convenience fields mirror typed fields emitted by existing DWD, MeteoAlarm, NOAA NWS, and NWS Alerts bespoke feeders while keeping the original CAP name/value pairs.

#### Identity

Each event identifies the real-world resource with `{cap_source_id}/{identifier}`. `{cap_source_id}` is configuration-assigned stable source identifier qualifying CAP alert identifiers across agencies; `{identifier}` is CAP identifier assigned by the sender to this alert message. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `cap-alerts`, key `{cap_source_id}/{identifier}` |
| `MQTT/5.0` | topic `alerts/cap/{cap_source_id}/{identifier_segment}/alert`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/cap-alerts`, message subject `{cap_source_id}/{identifier}` |

#### Payload

`Cap Alert` payloads are JSON object. Required fields: `cap_source_id`, `identifier`, `sender`, `sent`, `status`, `msg_type`, `scope`, `info`, `provider_url`.

- **`cap_source_id`** (string, required): Configuration-assigned stable source identifier qualifying CAP alert identifiers across agencies. Examples: nws-us, meteoalarm-belgium, dwd-germany. This value is the first segment of the CloudEvent subject and Kafka key.
- **`identifier`** (string, required): CAP identifier assigned by the sender to this alert message. Unique only within the sender/source, so the feeder qualifies it with cap_source_id for keys. Updates and cancellations use their own identifier; the CAP references field points to prior messages.
- **`sender`** (string, required): CAP sender identifier for the originating alerting authority, such as w-nws.webmaster@noaa.gov or opendata@dwd.de.
- **`sent`** (datetime, required): CAP sent timestamp when the message was issued by the sender, parsed as an ISO 8601 datetime.
- **`status`** (enum, required): CAP status for operational state of this message.
- **`msg_type`** (enum, required): CAP msgType indicating whether this message is an alert, update, cancellation, acknowledgement, or error.
- **`source`** (null or string, optional): CAP source: particular source of this alert message when supplied separately from sender. Null when omitted.
- **`scope`** (enum, required): CAP scope indicating intended distribution: Public, Restricted, or Private.
- **`restriction`** (null or string, optional): CAP restriction text describing distribution limits for Restricted scope messages. Null when not applicable.
- **`addresses`** (array of string, optional): CAP addresses list for Private messages, split into individual address tokens. Empty for Public and most Restricted alerts.
- **`code`** (array of object, optional): CAP code elements and code-like provider values preserved as name/value pairs. Used for source-specific routing or profile markers.
- **`note`** (null or string, optional): CAP note: message note intended for alert handling, not necessarily public display. Null when omitted.
- **`references`** (array of string, optional): CAP references entries identifying related prior messages that this message updates or cancels. Preserved as strings; not used as the CloudEvent key.
- **`incidents`** (array of string, optional): CAP incidents identifiers listing incident(s) this alert message concerns. Empty when omitted.
- **`info`** (array of object, required): All CAP info blocks attached to the alert. Multiple blocks are common for multilingual or multi-instruction alerts and are preserved losslessly.
- **`provider_url`** (uri, required): URL of the configured feed or detail resource from which this alert was acquired. Used as CloudEvent source template and for traceability.
- **`raw_cap_xml`** (null or string, optional): Original CAP XML document text when the source supplied XML. Null for JSON-only sources such as api.weather.gov active alerts unless a raw CAP detail URL was fetched.
- **`area_desc`** (null or string, optional): Convenience copy of the first info/area/areaDesc or NWS areaDesc used by existing bespoke feeders. The complete area list is still preserved under info[].area[].
- **`same_codes`** (array of string, optional): Convenience extraction of NWS SAME geocodes from CAP geocode/parameter pairs. The original values are also preserved in generic geocode[] or parameter[] arrays.
- **`ugc_codes`** (array of string, optional): Convenience extraction of NWS UGC zone codes from CAP geocode/parameter pairs. The original values are also preserved in generic geocode[] or parameter[] arrays.
- **`vtec`** (array of string, optional): Convenience extraction of NWS VTEC tracking strings from CAP parameters. The original VTEC values are also present in info[].parameter[].
- **`awareness_level`** (null or string, optional): Convenience extraction of MeteoAlarm awareness_level CAP parameter. The original name/value pair is also preserved in info[].parameter[].
- **`awareness_type`** (null or string, optional): Convenience extraction of MeteoAlarm awareness_type CAP parameter. The original name/value pair is also preserved in info[].parameter[].
- **`event_type`** (null or string, optional): Normalized lower-case event or hazard token for routing and legacy feeder compatibility, derived from CAP info.event when available.
- **`state`** (null or string, optional): Provider-specific state, territory, country, or administrative routing token when present in the upstream feed. Null when not derivable.
- **`affected_zones`** (array of uri, optional): NWS API affectedZones URI list and equivalent zone references from JSON CAP-equivalent sources. CAP XML feeds generally express the same information as area/geocode entries; this array preserves JSON-native zone URI references for lossless future folds.
- **`raw_source_json`** (null or string, optional): Raw upstream JSON object serialized as compact JSON when the source is a CAP-equivalent JSON API such as api.weather.gov. Null for native CAP XML feeds; retained as an escape hatch so future bespoke folds can prove no source-specific field was lost.
##### `status` values

- `Actual`: CAP 1.2 `Actual` value: CAP status for operational state of this message.
- `Exercise`: CAP 1.2 `Exercise` value: CAP status for operational state of this message.
- `System`: CAP 1.2 `System` value: CAP status for operational state of this message.
- `Test`: CAP 1.2 `Test` value: CAP status for operational state of this message.
- `Draft`: CAP 1.2 `Draft` value: CAP status for operational state of this message.
##### `msg_type` values

- `Alert`: CAP 1.2 `Alert` value: CAP msgType indicating whether this message is an alert, update, cancellation, acknowledgement, or error.
- `Update`: CAP 1.2 `Update` value: CAP msgType indicating whether this message is an alert, update, cancellation, acknowledgement, or error.
- `Cancel`: CAP 1.2 `Cancel` value: CAP msgType indicating whether this message is an alert, update, cancellation, acknowledgement, or error.
- `Ack`: CAP 1.2 `Ack` value: CAP msgType indicating whether this message is an alert, update, cancellation, acknowledgement, or error.
- `Error`: CAP 1.2 `Error` value: CAP msgType indicating whether this message is an alert, update, cancellation, acknowledgement, or error.
##### `scope` values

- `Public`: CAP 1.2 `Public` value: CAP scope indicating intended distribution: Public, Restricted, or Private.
- `Restricted`: CAP 1.2 `Restricted` value: CAP scope indicating intended distribution: Public, Restricted, or Private.
- `Private`: CAP 1.2 `Private` value: CAP scope indicating intended distribution: Public, Restricted, or Private.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "cap_source_id": "string",
  "identifier": "string",
  "sender": "string",
  "sent": "2024-01-01T00:00:00Z",
  "status": "Actual",
  "msg_type": "Alert",
  "source": "string",
  "scope": "Public",
  "restriction": "string",
  "addresses": [
    "string"
  ],
  "code": [
    {
      "value_name": "string",
      "value": "string"
    }
  ],
  "note": "string",
  "references": [
    "string"
  ],
  "incidents": [
    "string"
  ],
  "info": [
    {
      "language": "string",
      "category": [
        "Geo"
      ],
      "event": "string",
      "response_type": [
        "Shelter"
      ],
      "urgency": "Immediate",
      "severity": "Extreme",
      "certainty": "Observed",
      "audience": "string",
      "event_code": [
        {
          "value_name": "string",
          "value": "string"
        }
      ],
      "effective": "2024-01-01T00:00:00Z",
      "onset": "2024-01-01T00:00:00Z",
      "expires": "2024-01-01T00:00:00Z",
      "sender_name": "string",
      "headline": "string",
      "description": "string",
      "instruction": "string",
      "web": "string",
      "contact": "string",
      "parameter": [
        {
          "value_name": "string",
          "value": "string"
        }
      ],
      "resource": [
        {
          "resource_desc": "string",
          "mime_type": "string",
          "size": 0,
          "uri": "string",
          "deref_uri": null,
          "digest": "string"
        }
      ],
      "area": [
        {
          "area_desc": "string",
          "polygon": [
            "string"
          ],
          "circle": [
            "string"
          ],
          "geocode": [
            {
              "value_name": "string",
              "value": "string"
            }
          ],
          "altitude": 0,
          "ceiling": 0
        }
      ],
      "ends": "2024-01-01T00:00:00Z"
    }
  ],
  "provider_url": "string",
  "raw_cap_xml": "string",
  "area_desc": "string",
  "same_codes": [
    "string"
  ],
  "ugc_codes": [
    "string"
  ],
  "vtec": [
    "string"
  ],
  "awareness_level": "string",
  "awareness_type": "string",
  "event_type": "string",
  "state": "string",
  "affected_zones": [
    "string"
  ],
  "raw_source_json": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Cap Zone

CloudEvents type: `org.oasis.cap.alerts.CapZone`

#### What it tells you

Reference event for an alerting zone, forecast zone, MeteoAlarm region, or other area catalog entry exposed by a configured CAP source. The feeder emits zone reference data before alerts when the source exposes metadata such as api.weather.gov /zones, enabling consumers to interpret alert geocodes temporally.

#### Identity

Each event identifies the real-world resource with `{cap_source_id}/{zone_id}`. `{cap_source_id}` is configuration-assigned stable source identifier qualifying zone identifiers across agencies and used as the first subject/key segment; `{zone_id}` is stable upstream zone or region identifier, such as an NWS UGC zone code, county zone id, MeteoAlarm region code, or DWD area code. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `cap-alerts`, key `{cap_source_id}/{zone_id}` |
| `MQTT/5.0` | topic `alerts/cap/{cap_source_id}/zones/{zone_id_segment}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/cap-alerts`, message subject `{cap_source_id}/{zone_id}` |

#### Payload

`Cap Zone` payloads are JSON object. Required fields: `cap_source_id`, `zone_id`, `provider_url`.

- **`cap_source_id`** (string, required): Configuration-assigned stable source identifier qualifying zone identifiers across agencies and used as the first subject/key segment.
- **`zone_id`** (string, required): Stable upstream zone or region identifier, such as an NWS UGC zone code, county zone id, MeteoAlarm region code, or DWD area code.
- **`name`** (null or string, optional): Human-readable zone or region name supplied by the source metadata endpoint. Null when the source exposes only codes.
- **`zone_type`** (null or string, optional): Provider zone type or category, for example NWS public, marine, county, fire, forecast, or MeteoAlarm region class.
- **`state`** (null or string, optional): State, country, or regional routing token associated with the zone, if supplied by the metadata endpoint.
- **`forecast_office`** (null or string, optional): Responsible office or authority URL/code for this zone, such as an NWS Weather Forecast Office. Null when not supplied.
- **`time_zones`** (array of string, optional): IANA time-zone names associated with the zone when supplied by the metadata endpoint.
- **`geometry`** (null or string, optional): GeoJSON geometry serialized as compact JSON text when supplied by the metadata endpoint. Null when no geometry is published or when disabled for payload-size reasons.
- **`provider_url`** (uri, required): Metadata endpoint URL from which this zone reference was acquired. Used as CloudEvent source template and traceability link.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "cap_source_id": "string",
  "zone_id": "string",
  "name": "string",
  "zone_type": "string",
  "state": "string",
  "forecast_office": "string",
  "time_zones": [
    "string"
  ],
  "geometry": "string",
  "provider_url": "string"
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

- xRegistry manifest: [`xreg/cap-alerts.xreg.json`](xreg/cap-alerts.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
