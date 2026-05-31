# NASA FIRMS Events

The NASA FIRMS bridge turns NASA Fire Information for Resource Management System active-fire data into a real-time CloudEvents stream for global active-fire monitoring and OSINT situational awareness.

## At a glance

- **Event types:** 2 documented event types (6 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 2 telemetry event types.
- **Identity:** `{source}/{record_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `nasa-firms`. The record key is `{source}/{record_id}`. In plain language, `{source}/{record_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['nasa-firms'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `geo/fire/firms/+/+/+/detection`, `geo/fire/firms/+/availability`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('geo/fire/firms/+/+/+/detection', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `nasa-firms`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/nasa-firms')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Fire Detection

CloudEvents type: `NASA.FIRMS.FireDetection`

#### What it tells you

A single active-fire / thermal-anomaly pixel detection from a NASA FIRMS satellite product (VIIRS or MODIS), normalised across sensors. Each event is one detection in one satellite overpass; the brightness fields populated depend on `instrument`.

#### Identity

Each event identifies the real-world resource with `{source}/{record_id}`. `{source}` is FIRMS product source identifier for the satellite/sensor that produced this detection, e.g. `VIIRS_SNPP_NRT`, `VIIRS_NOAA20_NRT`, `VIIRS_NOAA21_NRT`, `MODIS_NRT` (and the `*_SP` standard-processing variants); `{record_id}` is deterministic detection identifier — second segment of the identity key `{source}/{record_id}`. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `nasa-firms`, key `{source}/{record_id}` |
| `MQTT/5.0` | topic `geo/fire/firms/{source}/{confidence_level}/{tile}/detection`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/nasa-firms`, message subject `{source}/{record_id}` |

#### Payload

`Fire Detection` payloads are JSON object. Required fields: `source`, `record_id`, `latitude`, `longitude`, `acq_date`, `acq_time`, `acq_datetime`, `satellite`, `instrument`, `confidence_level`, `tile`.

- **`source`** (string, required): FIRMS product source identifier for the satellite/sensor that produced this detection, e.g. `VIIRS_SNPP_NRT`, `VIIRS_NOAA20_NRT`, `VIIRS_NOAA21_NRT`, `MODIS_NRT` (and the `*_SP` standard-processing variants). First segment of the stable identity key `{source}/{record_id}` and the leading MQTT topic level. Populated by the bridge from the requested FIRMS Area API source, not from a CSV column.
- **`record_id`** (string, required): Deterministic detection identifier — second segment of the identity key `{source}/{record_id}`. Computed by the bridge as a stable 16-hex-character SHA-1 digest over the immutable detection tuple (source, latitude, longitude, acq_date, acq_time, satellite). Stable across polling cycles so the same fire pixel re-detected in overlapping day-range windows resolves to the same key and is de-duplicated downstream.
- **`latitude`** (double, required, deg (°)): Latitude of the centre of the nominal ~375 m (VIIRS) or ~1 km (MODIS) fire pixel, in decimal degrees (WGS84, positive north). Note this is the pixel centroid, not the precise location of the thermal anomaly within the pixel. Constraints: minimum `-90`, maximum `90`.
- **`longitude`** (double, required, deg (°)): Longitude of the centre of the nominal fire pixel, in decimal degrees (WGS84, positive east). Pixel centroid, not the precise anomaly location. Constraints: minimum `-180`, maximum `180`.
- **`brightness`** (null or double, optional, K): MODIS only: brightness temperature of the fire pixel measured in MODIS channel 21/22 (~4 µm), in Kelvin. Null for VIIRS detections (which report `bright_ti4`/`bright_ti5` instead). Sourced from the MODIS CSV `brightness` column.
- **`bright_t31`** (null or double, optional, K): MODIS only: brightness temperature of the fire pixel measured in MODIS channel 31 (~11 µm), in Kelvin. Used with `brightness` to characterise fire intensity and screen false alarms. Null for VIIRS detections. Sourced from the MODIS CSV `bright_t31` column.
- **`bright_ti4`** (null or double, optional, K): VIIRS only: brightness temperature of the fire pixel measured in VIIRS I-4 channel (~3.74 µm), in Kelvin. Primary fire channel for VIIRS. Null for MODIS detections (which report `brightness` instead). Sourced from the VIIRS CSV `bright_ti4` column.
- **`bright_ti5`** (null or double, optional, K): VIIRS only: brightness temperature of the fire pixel measured in VIIRS I-5 channel (~11.45 µm), in Kelvin. Background/context channel paired with `bright_ti4`. Null for MODIS detections. Sourced from the VIIRS CSV `bright_ti5` column.
- **`scan`** (null or double, optional, km): Along-scan ground dimension of the detected pixel, in kilometres. Grows from nadir toward the swath edge; combined with `track` it gives the actual ground footprint (375 m / 1 km is the nominal nadir resolution only). Sourced from the CSV `scan` column.
- **`track`** (null or double, optional, km): Along-track ground dimension of the detected pixel, in kilometres. Combined with `scan` it gives the actual ground footprint of the detection. Sourced from the CSV `track` column.
- **`acq_date`** (date, required): UTC acquisition date of the satellite overpass that produced the detection, formatted `YYYY-MM-DD`. Sourced from the CSV `acq_date` column.
- **`acq_time`** (string, required): UTC acquisition time of the satellite overpass, formatted as a zero-padded `HHMM` string (e.g. `0218` = 02:18 UTC). Sourced from the CSV `acq_time` column. Constraints: pattern `^([01][0-9]|2[0-3])[0-5][0-9]$`.
- **`acq_datetime`** (datetime, required): UTC acquisition timestamp combining `acq_date` and `acq_time` into an ISO-8601 instant (`YYYY-MM-DDTHH:MM:00Z`). Derived by the bridge.
- **`satellite`** (string, required): Short platform code of the acquiring satellite as reported by FIRMS, e.g. `N` (Suomi-NPP), `1` (NOAA-20/JPSS-1), `2` (NOAA-21/JPSS-2) for VIIRS, and `T` (Terra) / `A` (Aqua) for MODIS. Sourced from the CSV `satellite` column.
- **`instrument`** (enum, required): Sensor that produced the detection: `VIIRS` or `MODIS`. Discriminates which of the brightness fields are populated. Sourced from the CSV `instrument` column.
- **`confidence`** (null or string, optional): Raw upstream detection confidence exactly as delivered by FIRMS, kept verbatim for fidelity. For VIIRS this is a class letter `l` (low), `n` (nominal) or `h` (high); for MODIS it is an integer 0–100 (percent) rendered as a string. Use the normalised `confidence_level` for filtering across sensors. Sourced from the CSV `confidence` column.
- **`confidence_level`** (enum, required): Sensor-normalised detection confidence as a routing-safe class: `low`, `nominal`, or `high`. Derived by the bridge: VIIRS `l`/`n`/`h` map directly; MODIS integer maps <30 → `low`, 30–80 → `nominal`, >80 → `high`. Used as an MQTT topic level so consumers can subscribe by confidence.
- **`version`** (null or string, optional): Collection and source-processing version of the detection, e.g. `2.0NRT` (Collection 2, near-real-time) or `2.0` (standard processing). Sourced from the CSV `version` column.
- **`frp`** (null or double, optional, MW): Fire Radiative Power in megawatts — the radiative energy release rate of the detected fire within the pixel, a proxy for combustion intensity and a key OSINT discriminator (a multi-hundred-MW spike differs sharply from routine agricultural burning). Sourced from the CSV `frp` column.
- **`daynight`** (null or string, optional): Day/Night flag for the overpass: `D` (daytime) or `N` (nighttime), based on solar elevation at the pixel. Night detections are less prone to solar false alarms. Sourced from the CSV `daynight` column.
- **`tile`** (string, required): Coarse 10° × 10° geographic tile label of the form `lat<LL>_lon<LL>` (south-west corner, e.g. `lat30_lon-120`) covering the detection. Derived by the bridge purely as an MQTT topic level so consumers can geofence a region of interest without per-message coordinate parsing.
##### `instrument` values

- `VIIRS`
- `MODIS`
##### `confidence_level` values

- `low`
- `nominal`
- `high`
##### `daynight` values

- `D`
- `N`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "source": "string",
  "record_id": "string",
  "latitude": 0,
  "longitude": 0,
  "brightness": 0,
  "bright_t31": 0,
  "bright_ti4": 0,
  "bright_ti5": 0,
  "scan": 0,
  "track": 0,
  "acq_date": null,
  "acq_time": "string",
  "acq_datetime": "2024-01-01T00:00:00Z",
  "satellite": "string",
  "instrument": "VIIRS",
  "confidence": "string",
  "confidence_level": "low",
  "version": "string",
  "frp": 0,
  "daynight": "D",
  "tile": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Data Availability

CloudEvents type: `NASA.FIRMS.DataAvailability`

#### What it tells you

Reference record describing one FIRMS product source: its current data-availability window (min/max date), sensor family, platform, and nominal resolution. Emitted at bridge startup and refreshed periodically so consumers can interpret detection freshness and coverage on the same topic as the telemetry.

#### Identity

Each event identifies the real-world resource with `{source}/{record_id}`. `{source}` is FIRMS product source identifier this coverage record describes, e.g. `VIIRS_SNPP_NRT`, `VIIRS_NOAA20_NRT`, `VIIRS_NOAA21_NRT`, `MODIS_NRT`; `{record_id}` is constant literal `coverage` — the second identity-key segment for the single reference record per source (`{source}/coverage`). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `nasa-firms`, key `{source}/{record_id}` |
| `MQTT/5.0` | topic `geo/fire/firms/{source}/availability`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/nasa-firms`, message subject `{source}/{record_id}` |

#### Payload

`Data Availability` payloads are JSON object. Required fields: `source`, `record_id`, `retrieved_at`.

- **`source`** (string, required): FIRMS product source identifier this coverage record describes, e.g. `VIIRS_SNPP_NRT`, `VIIRS_NOAA20_NRT`, `VIIRS_NOAA21_NRT`, `MODIS_NRT`. First segment of the identity key `{source}/{record_id}`; joins to `FireDetection.source`.
- **`record_id`** (string, required): Constant literal `coverage` — the second identity-key segment for the single reference record per source (`{source}/coverage`). Keeps the reference family on the same `{source}/{record_id}` shape and topic as telemetry while remaining a stable, idempotent per-source key.
- **`data_id`** (null or string, optional): Raw FIRMS data-availability product identifier as returned by the `/api/data_availability` endpoint (the CSV `data_id` column), e.g. `VIIRS_SNPP_NRT`. Usually equal to `source`; preserved verbatim.
- **`min_date`** (null or date, optional): Earliest UTC date (`YYYY-MM-DD`) for which this FIRMS source currently has data available via the Area API, from the `min_date` column of the data-availability response.
- **`max_date`** (null or date, optional): Most recent UTC date (`YYYY-MM-DD`) for which this FIRMS source currently has data available — the effective freshness horizon of the source, from the `max_date` column.
- **`instrument`** (null or string, optional): Sensor family of the source: `VIIRS` or `MODIS`. Derived by the bridge from the source identifier.
- **`satellite`** (null or string, optional): Human-readable platform name(s) carried by the source, e.g. `Suomi-NPP`, `NOAA-20`, `NOAA-21`, `Terra`, `Aqua`. Derived by the bridge from the source identifier.
- **`resolution_m`** (null or double, optional, m): Nominal nadir spatial resolution of the source sensor in metres (375 for VIIRS I-band fire product, 1000 for MODIS). Static sensor fact supplied by the bridge for downstream scaling/symbology.
- **`retrieved_at`** (datetime, required): UTC ISO-8601 timestamp at which the bridge fetched this availability record.
##### `instrument` values

- `VIIRS`
- `MODIS`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "source": "string",
  "record_id": "string",
  "data_id": "string",
  "min_date": null,
  "max_date": null,
  "instrument": "VIIRS",
  "satellite": "string",
  "resolution_m": 0,
  "retrieved_at": "2024-01-01T00:00:00Z"
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

- xRegistry manifest: [`xreg/nasa_firms.xreg.json`](xreg/nasa_firms.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- Azure Service Bus Standard namespace: <https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview>
- Azure Service Bus emulator: <https://learn.microsoft.com/azure/service-bus-messaging/test-locally-with-service-bus-emulator>
