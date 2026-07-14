# Taipei YouBike 2.0 Events

Transport-neutral event family for Taiwan's YouBike 2.0 public bicycle-sharing system (branded YouBike 2.0 / 微笑單車, operated island-wide by YouBike Co., Ltd. under contract to Taiwanese municipalities). Both the slowly-changing docking-station reference event and the near-real-time availability event are keyed by the stable YouBike station number `{station_id}` so consumers can build temporally consistent views of one docking station.

## At a glance

- **Event types:** 2 documented event types (8 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 1 reference/catalog event type and 1 telemetry event type.
- **Identity:** `{station_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `taipei-youbike`. The record key is `{station_id}`. In plain language, `{station_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['taipei-youbike'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `mobility/taipei-youbike/+/info`, `mobility/taipei-youbike/+/status`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('mobility/taipei-youbike/+/info', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `taipei-youbike`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/taipei-youbike')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Station Information

CloudEvents type: `TW.YouBike.StationInformation`

#### What it tells you

Reference data describing one Taiwan YouBike 2.0 docking station, sourced from the YouBike public station feed at `https://apis.youbike.com.tw/json/station-yb2.json`. Carries the stable station number, the bilingual (Traditional Chinese and English) station name, district and street address, WGS 84 coordinates, the nominal docking capacity, the station type, and the administrative region codes. Emitted at bridge startup and on periodic reference refresh so consumers can join StationStatus availability records against stable station metadata.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is stable YouBike station number from the `station_no` field of the upstream record, for example `500101001`. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `taipei-youbike`, key `{station_id}` |
| `MQTT/5.0` | topic `mobility/taipei-youbike/{station_id}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/taipei-youbike`, message subject `{station_id}` |

#### Payload

`Station Information` payloads are JSON object. Required fields: `station_id`, `name_tw`, `lat`, `lon`.

- **`station_id`** (string, required): Stable YouBike station number from the `station_no` field of the upstream record, for example `500101001`. It is unique within the YouBike 2.0 network, persists across feed refreshes, and forms the single component of both the CloudEvents subject and the Kafka key. The leading digits encode the operating city and administrative area.
- **`name_tw`** (string, required): Traditional Chinese (zh-Hant-TW) customer-facing station name from the `name_tw` field, for example `捷運科技大樓站` (MRT Technology Building Station). This is the primary display name shown in the YouBike app and on station signage.
- **`name_en`** (null or string, optional): English station name from the `name_en` field, for example `MRT Technology Bldg. Sta.`. Intended for maps, screens, and accessibility tooling; the bridge emits null when the upstream value is absent or an empty string.
- **`name_cn`** (null or string, optional): Simplified Chinese (zh-Hans) station name from the `name_cn` field. This localization slot is present in the upstream schema but is currently returned as an empty string for every station; the bridge normalizes the empty string to null.
- **`district_tw`** (null or string, optional): Traditional Chinese administrative district (行政區) in which the station is located, from the `district_tw` field, for example `大安區` (Da'an District). The bridge emits null when absent or empty.
- **`district_en`** (null or string, optional): English administrative district name from the `district_en` field, for example `Daan Dist.`. Useful for district-level grouping and filtering; the bridge emits null when absent or empty.
- **`district_cn`** (null or string, optional): Simplified Chinese administrative district name from the `district_cn` field. Present in the upstream schema but currently returned as an empty string for every station; the bridge normalizes the empty string to null.
- **`address_tw`** (null or string, optional): Traditional Chinese street address of the station from the `address_tw` field, for example `復興南路二段235號前` (in front of No. 235, Section 2, Fuxing South Road). The bridge emits null when absent or empty.
- **`address_en`** (null or string, optional): English street address of the station from the `address_en` field, for example `No.235, Sec. 2, Fuxing S. Rd.`. The bridge emits null when absent or empty.
- **`address_cn`** (null or string, optional): Simplified Chinese street address from the `address_cn` field. Present in the upstream schema but currently returned as an empty string for every station; the bridge normalizes the empty string to null.
- **`lat`** (double, required, deg (°)): WGS 84 latitude of the docking station in decimal degrees, parsed from the string-valued `lat` field of the upstream record (for example `"25.02605"`). Positive values are north of the equator; all YouBike stations are in Taiwan, roughly between 22 and 25.3 degrees north. Constraints: minimum `-90`, maximum `90`.
- **`lon`** (double, required, deg (°)): WGS 84 longitude of the docking station in decimal degrees, parsed from the string-valued `lng` field of the upstream record (for example `"121.5436"`). Positive values are east of the prime meridian; all YouBike stations are in Taiwan, roughly between 120 and 122 degrees east. Constraints: minimum `-180`, maximum `180`.
- **`capacity`** (null or int32, optional): Nominal number of physical docking points at the station, from the `parking_spaces` field. Represents the configured physical size of the docking station; it is not necessarily equal to the live sum of available bikes, empty docks, and out-of-service docks. The bridge emits null when the value is absent. Constraints: minimum `0`.
- **`station_type`** (null or int32, optional): YouBike station generation code from the `type` field. The value `2` denotes a YouBike 2.0 station (the lightweight docking generation that carries its lock and payment terminal on the bike rather than the dock). This feed exposes only YouBike 2.0 stations, so the value is `2` for every record. Constraints: minimum `0`.
- **`country_code`** (null or string, optional): YouBike internal country code from the `country_code` field. Currently `00` for every station (Taiwan). Reserved by the operator for future multi-country deployments; the bridge emits null when absent.
- **`area_code`** (null or string, optional): YouBike internal administrative-area code from the `area_code` field, a two-character hexadecimal code such as `00` (Taipei City), `05` (New Taipei City), `07` (Taoyuan), `01` (Taichung), `12` (Kaohsiung), `13` (Tainan), or `0A` (Miaoli County) that groups stations by operating city / service area across the 14 YouBike regions of Taiwan. The operator publishes no official code-to-city table; the mapping is established empirically by correlating the code with `district_tw` and the station coordinates. The bridge emits null when absent.
- **`img`** (null or string, optional): Relative URL path of the station photograph on the YouBike web site from the `img` field, for example `/images/station/default.jpg`. Resolve against `https://apis.youbike.com.tw` to obtain the absolute image URL; the bridge emits null when absent.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "name_tw": "string",
  "name_en": "string",
  "name_cn": "string",
  "district_tw": "string",
  "district_en": "string",
  "district_cn": "string",
  "address_tw": "string",
  "address_en": "string",
  "address_cn": "string",
  "lat": 0,
  "lon": 0,
  "capacity": 0,
  "station_type": 0,
  "country_code": "string",
  "area_code": "string",
  "img": "string"
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Station Status

CloudEvents type: `TW.YouBike.StationStatus`

#### What it tells you

Near-real-time availability telemetry for one Taiwan YouBike 2.0 docking station, derived from the YouBike public station feed at `https://apis.youbike.com.tw/json/station-yb2.json`. Reports the current count of rentable bikes (broken down by YouBike 1.0, YouBike 2.0, and electric YouBike), empty docks available for returns, out-of-service docks, the discrete availability gauge level, the station service status, and the upstream data-update timestamps. Near-real-time availability record for one Taiwan YouBike 2.0 docking station, from the YouBike public station feed `https://apis.youbike.com.tw/json/station-yb2.json`.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is stable YouBike station number from the `station_no` field of the upstream record, for example `500101001`. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `taipei-youbike`, key `{station_id}` |
| `MQTT/5.0` | topic `mobility/taipei-youbike/{station_id}/status`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/taipei-youbike`, message subject `{station_id}` |

#### Payload

`Station Status` payloads are JSON object. Required fields: `station_id`, `num_bikes_available`, `num_empty_docks`, `service_status`, `updated_at`.

- **`station_id`** (string, required): Stable YouBike station number from the `station_no` field of the upstream record, for example `500101001`. Matches the `station_id` of the corresponding `StationInformation` event and forms the CloudEvents subject and Kafka key.
- **`num_bikes_available`** (int32, required): Total number of rentable bikes currently docked and available at the station, from the `available_spaces` field. Equals the sum of `num_bikes_yb1`, `num_bikes_yb2`, and `num_ebikes_available`. Constraints: minimum `0`.
- **`num_bikes_yb1`** (null or int32, optional): Number of first-generation YouBike 1.0 mechanical bikes currently available at the station, from the `yb1` key of the upstream `available_spaces_detail` object. This is a legacy field retained from when YouBike 1.0 and 2.0 coexisted; YouBike 1.0 has been fully retired and the value is `0` for every station in the current island-wide feed (the companion `station-yb1.json` endpoint returns an empty document). The bridge emits null when the breakdown is absent. Constraints: minimum `0`.
- **`num_bikes_yb2`** (null or int32, optional): Number of second-generation YouBike 2.0 mechanical bikes currently available at the station, from the `yb2` key of the upstream `available_spaces_detail` object. The bridge emits null when the breakdown is absent. Constraints: minimum `0`.
- **`num_ebikes_available`** (null or int32, optional): Number of electric YouBike (YouBike 2.0E, electrically assisted) bikes currently available at the station, from the `eyb` key of the upstream `available_spaces_detail` object. The bridge emits null when the breakdown is absent. Constraints: minimum `0`.
- **`num_empty_docks`** (int32, required): Number of empty docking points currently available for returning a bike at the station, from the `empty_spaces` field. Constraints: minimum `0`.
- **`num_forbidden_docks`** (null or int32, optional): Number of docking points currently disabled or out of service (故障/禁用車位, for example a broken dock that can neither release nor accept a bike), from the `forbidden_spaces` field. The bridge emits null when absent. Constraints: minimum `0`.
- **`availability_level`** (null or int32, optional): Discrete availability gauge level from the `available_spaces_level` field, taking one of the values 0, 20, 40, 60, 80, or 100 (a six-step / 0-to-5-bar signal indicator the YouBike app renders, 0 = empty, 100 = plentiful). It tracks standard YouBike 2.0 (`num_bikes_yb2`) availability: the level is 0 whenever no standard bikes are docked, even if electric bikes are present. It is a coarse presentation rather than an exact percentage, and the exact bucketing thresholds are proprietary to the operator. The bridge emits null when absent. Constraints: minimum `0`, maximum `100`.
- **`service_status`** (int32, required): Station service status from the `status` field, aligned with the TDX (Taiwan Transport Data eXchange) `ServiceStatus` enumeration. `1` indicates normal operation (正常營運); `2` indicates the station is temporarily suspended (暫停營運) — observed suspended stations have every dock forbidden (`num_forbidden_docks` equals `capacity`), zero available bikes and empty docks, and a frozen timestamp. `0` (停止營運, ceased) denotes a permanently closed station and is not observed in the current feed because closed stations are dropped from the document rather than flagged. Constraints: minimum `0`.
- **`updated_at`** (datetime, required): Timestamp at which the YouBike backend last wrote this station's record, in ISO 8601 / RFC 3339 UTC. It is the operator's record-update time and runs a few tens of seconds after `snapshot_time` (the underlying sensor reading). The upstream `updated_at` field is a naive local time string in the Asia/Taipei time zone (UTC+8), for example `2026-07-15 01:30:34`; the bridge converts it to an absolute UTC instant.
- **`snapshot_time`** (null or datetime, optional): Timestamp at which the station hardware (the on-site IoT module) collected the occupancy reading, in ISO 8601 / RFC 3339 UTC. This is the source sensor time (the Taipei open-data mirror labels the equivalent field `infoTime` / `mday`) and is typically a few tens of seconds earlier than `updated_at`. The upstream `time` field is a naive local time string in the Asia/Taipei time zone (UTC+8), for example `2026-07-15 01:30:04`; the bridge converts it to an absolute UTC instant and emits null when absent.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "num_bikes_available": 0,
  "num_bikes_yb1": 0,
  "num_bikes_yb2": 0,
  "num_ebikes_available": 0,
  "num_empty_docks": 0,
  "num_forbidden_docks": 0,
  "availability_level": 0,
  "service_status": 0,
  "updated_at": "2024-01-01T00:00:00Z",
  "snapshot_time": "2024-01-01T00:00:00Z"
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
- Reference/catalog events are documented as startup emissions, with periodic refresh when the source supports it.

## References

- xRegistry manifest: [`xreg/taipei-youbike.xreg.json`](xreg/taipei-youbike.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- Azure Service Bus emulator: <https://learn.microsoft.com/azure/service-bus-messaging/test-locally-with-service-bus-emulator>
