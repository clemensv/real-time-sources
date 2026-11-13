# NOAA SWPC L1 Events

<sub>L1 propagated solar wind (DSCOVR/ACE), 1-min cadence, 30–60 min Earth-impact lead time · Kafka · MQTT · AMQP · <a href="https://www.swpc.noaa.gov/">upstream</a> · <a href="https://services.swpc.noaa.gov/">API docs</a></sub>

## At a glance

- **Event types:** 1 documented event type (12 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 1 telemetry event type.
- **Identity:** `{spacecraft}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `noaa-swpc-l1`. The record key is `{spacecraft}`. In plain language, `{spacecraft}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['noaa-swpc-l1'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `space-weather/us/noaa-swpc/l1/+/propagated-solar-wind`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('space-weather/us/noaa-swpc/l1/+/propagated-solar-wind', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `noaa-swpc-l1`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/noaa-swpc-l1')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Propagated Solar Wind

CloudEvents type: `gov.noaa.swpc.l1.PropagatedSolarWind`

#### What it tells you

One minute-resolution solar-wind observation at L1 with forward-propagated Earth-arrival timestamp. Fuses plasma (speed/density/temperature), magnetic field (Bx/By/Bz/Bt in GSM), and bulk velocity vector (Vx/Vy/Vz in GSM) into a single row per `time_tag`. The `propagated_time_tag` field is the upstream's predicted Earth arrival time for the solar-wind parcel observed at L1 at `time_tag`.

#### Identity

Each event identifies the real-world resource with `{spacecraft}`. `{spacecraft}` is stable channel identifier for the source spacecraft at L1. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-swpc-l1`, key `{spacecraft}` |
| `MQTT/5.0` | topic `space-weather/us/noaa-swpc/l1/{spacecraft}/propagated-solar-wind`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/noaa-swpc-l1`, message subject `{spacecraft}` |

#### Payload

`Propagated Solar Wind` payloads are JSON object. Required fields: `spacecraft`, `time_tag`, `propagated_time_tag`.

- **`spacecraft`** (enum, required): Stable channel identifier for the source spacecraft at L1. **Synthesized by the bridge — not present in the upstream payload.** Set to `dscovr` for the operational primary, `ace` for the backup. Used as the CloudEvent `subject`, the Kafka partition key, the MQTT topic `{spacecraft}` segment, the AMQP message subject, and the AMQP `x-opt-partition-key` message annotation. SWPC does not currently disclose source spacecraft per row in the propagated-solar-wind feed; the bridge sets `dscovr` by default and exposes a configuration override for operators who know the active spacecraft has switched.
- **`time_tag`** (datetime, required): Wall-clock time the upstream observation was taken at L1, in ISO 8601 / RFC 3339 with explicit UTC offset. Upstream emits this in `YYYY-MM-DD HH:MM:SS.fff` form with implicit UTC; the bridge normalises to RFC 3339 with explicit `Z`. Minute-aligned. Strictly monotonic across the 7-day rolling window.
- **`propagated_time_tag`** (datetime, required): Predicted wall-clock time at which the solar-wind parcel observed at L1 at `time_tag` is expected to reach Earth's magnetopause, computed by SWPC from the observed bulk speed and the L1-to-Earth distance. Typically 30-60 minutes after `time_tag` — always `propagated_time_tag > time_tag`. This lead time is the operational value of the propagated product: downstream geomagnetic-storm forecasts trigger from `propagated_time_tag`, not `time_tag`. RFC 3339 with explicit `Z`.
- **`speed`** (double or null, optional, km/s): Bulk solar-wind speed measured at L1 by the spacecraft's Faraday cup / plasma instrument. Quiet solar wind is 300-500 km/s; high-speed streams from coronal holes can reach 800 km/s; coronal-mass-ejection (CME) shock fronts have been observed above 2000 km/s. Null when the upstream plasma instrument has no valid measurement for that minute. Unit: kilometres per second. Constraints: minimum `0`, maximum `3000`.
- **`density`** (double or null, optional, cm⁻³): Proton number density measured at L1. Quiet solar wind is 1-10 p/cm³; CME sheath / heliospheric current sheet crossings can reach 50-100 p/cm³ briefly. Null when the upstream plasma instrument has no valid measurement. Unit: particles (protons) per cubic centimetre. Constraints: minimum `0`, maximum `1000`.
- **`temperature`** (double or null, optional, K): Proton temperature at L1 in kelvin. Quiet solar wind is ~10^5 K; high-speed streams are hotter (~5×10^5 K); CME interiors are usually cooler than the ambient solar wind, while shocked sheath plasma can exceed 10^6 K. Null when the upstream plasma instrument has no valid measurement. Unit: kelvin. Constraints: minimum `0`, maximum `10000000`.
- **`bx`** (double or null, optional, nT): Bx component of the interplanetary magnetic field at L1 in Geocentric Solar Magnetospheric (GSM) coordinates — the component pointing from Earth toward the Sun. Quiet solar wind: |Bx| typically 1-5 nT; CME magnetic clouds: up to 50 nT. Wire values are nanotesla (nT); the JsonStructure `unit` is `nT` (not the SI base unit T). Null when the upstream magnetometer has no valid measurement (DSCOVR magnetometer experiences routine gaps). Constraints: minimum `-100`, maximum `100`.
- **`by`** (double or null, optional, nT): By component of the interplanetary magnetic field at L1 in GSM coordinates — the component pointing in the direction of Earth's orbital motion projected onto the magnetic equator. Quiet solar wind: |By| 1-5 nT. Wire values are nanotesla (nT); JsonStructure `unit` is `nT`. Null on magnetometer gaps. Constraints: minimum `-100`, maximum `100`.
- **`bz`** (double or null, optional, nT): Bz component of the interplanetary magnetic field at L1 in GSM coordinates — the component perpendicular to Earth's orbital plane, positive northward. **The single most operationally important field in this schema**: sustained southward Bz (negative values, especially Bz < -10 nT for ≥ 30 minutes) couples solar-wind energy into Earth's magnetosphere via dayside magnetic reconnection and drives geomagnetic storms. Bz is the principal input to the Dst, Kp, and Ap forecast models downstream of this feed. Wire values are nanotesla (nT); JsonStructure `unit` is `nT`. Null on magnetometer gaps — null Bz means no forecasting signal for that minute, not a quiet condition. Constraints: minimum `-100`, maximum `100`.
- **`bt`** (double or null, optional, nT): Total magnetic-field magnitude at L1: Bt = sqrt(Bx² + By² + Bz²). Always non-negative. Quiet solar wind: 3-8 nT; CME magnetic clouds: 20-50 nT. Wire values are nanotesla (nT); JsonStructure `unit` is `nT`. Null when any of Bx/By/Bz is null. Constraints: minimum `0`, maximum `200`.
- **`vx`** (double or null, optional, km/s): Vx component of the solar-wind bulk velocity at L1 in GSM coordinates — the radial (Sun-Earth) component. The dominant component of solar-wind flow; almost equal to -`speed` because the flow is nearly radially outward from the Sun (negative in GSM because GSM Vx points sunward while the wind flows anti-sunward). **DSCOVR typically does not measure this component reliably**; the upstream emits null for Vx/Vy/Vz on the majority of rows. Unit: kilometres per second. Constraints: minimum `-3000`, maximum `3000`.
- **`vy`** (double or null, optional, km/s): Vy component of the solar-wind bulk velocity at L1 in GSM coordinates — the dawn-dusk component. Typically small (|Vy| ≲ 100 km/s). DSCOVR usually emits null; treat as optional. Unit: kilometres per second. Constraints: minimum `-3000`, maximum `3000`.
- **`vz`** (double or null, optional, km/s): Vz component of the solar-wind bulk velocity at L1 in GSM coordinates — the north-south component. Typically small (|Vz| ≲ 100 km/s). DSCOVR usually emits null; treat as optional. Unit: kilometres per second. Constraints: minimum `-3000`, maximum `3000`.
##### `spacecraft` values

- `dscovr` — NOAA Deep Space Climate Observatory — the operational primary L1 solar-wind monitor since 2016.
- `ace` — NASA Advanced Composition Explorer — the operational backup L1 monitor; engaged when DSCOVR is unavailable.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "spacecraft": "dscovr",
  "time_tag": "2024-01-01T00:00:00Z",
  "propagated_time_tag": "2024-01-01T00:00:00Z",
  "speed": 0,
  "density": 0,
  "temperature": 0,
  "bx": 0,
  "by": 0,
  "bz": 0,
  "bt": 0,
  "vx": 0,
  "vy": 0,
  "vz": 0
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

The default payload remains JSON with a JSON Structure schema. The manifest also declares inherited `.avro` groups with Avro schemas and unchanged `application/json` payloads, and `.avro.binary` groups with `application/vnd.apache.org.avro+avro` payloads. These encoding variants retain the same event identities and transport routing. Binary Avro bytes inside structured JSON CloudEvents belong in `data_base64`; payload encoding is independent of the CloudEvents envelope mode.

Binary Avro is declared by the contract but is not yet a supported feeder output. [xregistry/codegen#670](https://github.com/xregistry/codegen/issues/670) tracks the producer-generation defect. The checked-in feeders continue to use their existing JSON producers. Avro schemas preserve RFC3339 strings as strings where no native timestamp mapping was already declared; optional JSON properties without a declared default use null defaults in Avro records.

MQTT retained messages are Last Known Value snapshots: the broker stores the most recent retained message per exact topic and delivers it to new subscribers when their subscription matches that topic. Schema evolution is additive where possible; incompatible semantic or structural changes are published as a new CloudEvents type so existing consumers can keep running.

## Operational notes

- The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- The MQTT variant publishes with QoS 1 and retained-message Last-Known-Value semantics where declared in the event catalog.

## References

- xRegistry manifest: [`xreg/noaa_swpc_l1.xreg.json`](xreg/noaa_swpc_l1.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- Azure Service Bus Standard namespace: <https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview>
