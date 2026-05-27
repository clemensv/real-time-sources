# USGS NWIS Water Quality feeder Events

USGS NWIS Water Quality publishes continuous water-quality sensor readings from the U.S. Geological Survey (USGS) Water Services API for United States water-quality monitoring sites. These events let consumers build real-time monitoring, alerting, and operational dashboards without polling the upstream API directly.

## At a glance

- **Event types:** 2 documented event types (6 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 1 reference/catalog event type and 1 telemetry event type.
- **Identity:** `{site_number}`, `{site_number}/{parameter_code}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `usgs-nwis-wq`. The record key is `{site_number}`, `{site_number}/{parameter_code}`. Each key template is explained in the event catalog below. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['usgs-nwis-wq'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `hydro/us/usgs/usgs-nwis-wq/+/+/info`, `hydro/us/usgs/usgs-nwis-wq/+/+/+/water-quality`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('hydro/us/usgs/usgs-nwis-wq/+/+/info', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `usgs-nwis-wq`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/usgs-nwis-wq')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Monitoring Site

CloudEvents type: `USGS.WaterQuality.Sites.MonitoringSite`

#### What it tells you

A reference record for one United States water-quality monitoring site published by the U.S. Geological Survey (USGS) Water Services API. It fires when the bridge publishes or refreshes the station catalog so consumers can interpret measurement events.

#### Identity

Each event identifies the real-world resource with `{site_number}`. `{site_number}` is USGS site identification number. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-nwis-wq`, key `{site_number}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-nwis-wq/{state}/{site_number}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/usgs-nwis-wq`, message subject `{site_number}`; application properties state `{state}` |

#### Payload

`Monitoring Site` payloads are JSON object. Required fields: `site_number`, `site_name`, `agency_code`.

- **`site_number`** (string, required): USGS site identification number. A unique 8-to-15-digit number assigned by the USGS to each monitoring location (e.g. '01646500').
- **`site_name`** (string, required): Official USGS station name describing the monitoring location (e.g. 'POTOMAC RIVER NEAR WASH, DC LITTLE FALLS PUMP STA').
- **`agency_code`** (string, required): Code identifying the agency responsible for the site. Typically 'USGS' for United States Geological Survey.
- **`latitude`** (double, optional): Decimal latitude of the monitoring site in the WGS84 (EPSG:4326) coordinate reference system.
- **`longitude`** (double, optional): Decimal longitude of the monitoring site in the WGS84 (EPSG:4326) coordinate reference system.
- **`site_type`** (string, optional): USGS site type code indicating the category of the monitoring location. Common values include 'ST' (stream), 'LK' (lake), 'GW' (groundwater), 'ES' (estuary).
- **`state_code`** (string, optional): Two-digit FIPS state code for the state or territory where the site is located (e.g. '24' for Maryland).
- **`county_code`** (string, optional): Five-digit FIPS county code for the county where the site is located (e.g. '24031' for Montgomery County, MD).
- **`huc_code`** (string, optional): Hydrologic Unit Code (HUC) identifying the watershed or drainage basin containing the site.
- **`state`** (string, optional): Stable routing axis used by MQTT and AMQP transport templates for usgs-nwis-wq.
- **`parameter_code`** (string, optional): Stable routing axis used by MQTT and AMQP transport templates for usgs-nwis-wq.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "site_number": "string",
  "site_name": "string",
  "agency_code": "string",
  "latitude": 0,
  "longitude": 0,
  "site_type": "string",
  "state_code": "string",
  "county_code": "string",
  "huc_code": "string",
  "state": "string",
  "parameter_code": "string"
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Water Quality Reading

CloudEvents type: `USGS.WaterQuality.Readings.WaterQualityReading`

#### What it tells you

A current measurement from the U.S. Geological Survey (USGS) Water Services API for one monitoring site. It carries continuous water-quality sensor readings when the upstream feed reports a new or refreshed value.

#### Identity

Each event identifies the real-world resource with `{site_number}/{parameter_code}`. `{site_number}` is USGS site identification number for the monitoring location that produced this reading (e.g. '01646500'); `{parameter_code}` is five-digit USGS parameter code identifying the measured quantity. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-nwis-wq`, key `{site_number}/{parameter_code}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-nwis-wq/{state}/{site_number}/{parameter_code}/water-quality`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/usgs-nwis-wq`, message subject `{site_number}/{parameter_code}`; application properties state `{state}`, parameter_code `{parameter_code}` |

#### Payload

`Water Quality Reading` payloads are JSON object. Required fields: `site_number`, `site_name`, `parameter_code`, `parameter_name`, `unit`, `date_time`.

- **`site_number`** (string, required): USGS site identification number for the monitoring location that produced this reading (e.g. '01646500').
- **`site_name`** (string, required): Official USGS station name for the monitoring location.
- **`parameter_code`** (string, required): Five-digit USGS parameter code identifying the measured quantity. Key water quality codes: 00010 (water temperature °C), 00300 (dissolved oxygen mg/L), 00400 (pH), 00095 (specific conductance µS/cm), 63680 (turbidity FNU), 99133 (nitrate+nitrite mg/L as N).
- **`parameter_name`** (string, required): Human-readable name of the measured parameter as provided in the USGS variable description (e.g. 'Temperature, water, degrees Celsius').
- **`value`** (double, optional): Numeric sensor reading for the parameter at the given date_time. Null when the sensor did not return a valid numeric value (e.g. equipment malfunction, ice-affected, or the USGS noDataValue sentinel -999999.0).
- **`unit`** (string, required): Unit of measurement for the reading as reported by the USGS (e.g. 'deg C', 'mg/l', 'uS/cm @25C', 'FNU', 'mg/l as N').
- **`qualifier`** (string, optional): USGS data qualifier code indicating the quality or status of the reading. Common values: 'P' (provisional), 'A' (approved), 'e' (estimated). Null when no qualifier is provided.
- **`date_time`** (string, required): ISO 8601 date-time string of the observation in UTC (e.g. '2024-11-15T16:45:00+00:00'). Converted from the site-local timestamp using the timezone information provided in the WaterML 2.0 response.
- **`state`** (string, optional): Stable routing axis used by MQTT and AMQP transport templates for usgs-nwis-wq.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "site_number": "string",
  "site_name": "string",
  "parameter_code": "string",
  "parameter_name": "string",
  "value": 0,
  "unit": "string",
  "qualifier": "string",
  "date_time": "string",
  "state": "string"
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

- xRegistry manifest: [`xreg/usgs_nwis_wq.xreg.json`](xreg/usgs_nwis_wq.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
