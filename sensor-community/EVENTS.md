# Sensor.Community Events

Sensor.Community, formerly Luftdaten.info, is a large citizen-science sensor network that publishes near-real-time environmental measurements from thousands of community-operated stations. This source polls the public Airrohr API and republishes selected sensor metadata and readings as CloudEvents into Kafka.

## At a glance

- **Event types:** 2 documented event types.
- **Transports:** KAFKA
- **Reference vs telemetry:** 0 reference/catalog event types and 2 telemetry event types.
- **Identity:** `{sensor_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `sensor-community`. The record key is `{sensor_id}`. In plain language, `{sensor_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['sensor-community'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.

## Event catalog

### Sensor Info

CloudEvents type: `io.sensor.community.SensorInfo`

#### What it tells you

Reference data for a Sensor.Community sensor node including its hardware type and last known location metadata. Schema for Sensor.Community sensor reference data, capturing the stable sensor identifier, hardware type, and latest known location metadata published in the Airrohr API payload.

#### Identity

Each event identifies the real-world resource with `{sensor_id}`. `{sensor_id}` is stable integer identifier of the Sensor.Community sensor device. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `sensor-community`, key `{sensor_id}` |

#### Payload

`Sensor Info` payloads are JSON object. Required fields: `sensor_id`, `sensor_type_id`, `sensor_type_name`, `sensor_type_manufacturer`, `pin`, `location_id`, `latitude`, `longitude`, `altitude`, `country`, `indoor`.

- **`sensor_id`** (integer, required): Stable integer identifier of the Sensor.Community sensor device. This value is used as the CloudEvents subject and Kafka key.
- **`sensor_type_id`** (integer, required): Numeric upstream identifier for the sensor hardware type, such as the Sensor.Community type id for SDS011 or BME280.
- **`sensor_type_name`** (string, required): Upstream sensor hardware type name published under sensor.sensor_type.name, for example SDS011, SPS30, BME280, or DHT22.
- **`sensor_type_manufacturer`** (string, required): Manufacturer name published by Sensor.Community for the sensor hardware type, taken from sensor.sensor_type.manufacturer.
- **`pin`** (string, required): Sensor pin designation reported by the upstream payload under sensor.pin.
- **`location_id`** (integer, required): Stable integer identifier of the Sensor.Community location object associated with the reading.
- **`latitude`** (double, required): Latitude of the sensor location in WGS84 decimal degrees.
- **`longitude`** (double, required): Longitude of the sensor location in WGS84 decimal degrees.
- **`altitude`** (double or null, required, m): Altitude of the sensor location in meters above sea level when supplied by the upstream payload.
- **`country`** (string, required): ISO 3166-1 alpha-2 country code published in the Sensor.Community location record. Constraints: minLength `2`, maxLength `2`.
- **`indoor`** (boolean, required): True when the upstream location.indoor flag marks the sensor as indoor; false when the sensor is marked as outdoor.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "sensor_id": 0,
  "sensor_type_id": 0,
  "sensor_type_name": "string",
  "sensor_type_manufacturer": "string",
  "pin": "string",
  "location_id": 0,
  "latitude": 0,
  "longitude": 0,
  "altitude": 0,
  "country": "string",
  "indoor": false
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Sensor Reading

CloudEvents type: `io.sensor.community.SensorReading`

#### What it tells you

Latest Sensor.Community telemetry reading for one sensor at a specific timestamp, normalized across particulate, climate, pressure, and noise measurements. Schema for the latest normalized Sensor.Community telemetry reading for a single sensor and timestamp, covering particulate matter, temperature, humidity, pressure, and supported noise measurements.

#### Identity

Each event identifies the real-world resource with `{sensor_id}`. `{sensor_id}` is stable integer identifier of the Sensor.Community sensor device. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `sensor-community`, key `{sensor_id}` |

#### Payload

`Sensor Reading` payloads are JSON object. Required fields: `sensor_id`, `timestamp`, `sensor_type_name`, `pm10_ug_m3`, `pm2_5_ug_m3`, `pm1_0_ug_m3`, `pm4_0_ug_m3`, `temperature_celsius`, `humidity_percent`, `pressure_pa`, `pressure_sealevel_pa`, `noise_laeq_db`, `noise_la_min_db`, `noise_la_max_db`.

- **`sensor_id`** (integer, required): Stable integer identifier of the Sensor.Community sensor device. This value is used as the CloudEvents subject and Kafka key.
- **`timestamp`** (string, required): UTC timestamp published by Sensor.Community for the reading in the format YYYY-MM-DD HH:mm:ss.
- **`sensor_type_name`** (string, required): Upstream sensor hardware type name published under sensor.sensor_type.name for the device that emitted the reading.
- **`pm10_ug_m3`** (double or null, required, µg/m³): Particulate matter mass concentration for PM10 in micrograms per cubic meter when the upstream feed publishes value type P1.
- **`pm2_5_ug_m3`** (double or null, required, µg/m³): Particulate matter mass concentration for PM2.5 in micrograms per cubic meter when the upstream feed publishes value type P2.
- **`pm1_0_ug_m3`** (double or null, required, µg/m³): Particulate matter mass concentration for PM1.0 in micrograms per cubic meter when the upstream feed publishes value type P0, typically for SPS30-family sensors.
- **`pm4_0_ug_m3`** (double or null, required, µg/m³): Particulate matter mass concentration for PM4.0 in micrograms per cubic meter when the upstream feed publishes value type P4, typically for SPS30-family sensors.
- **`temperature_celsius`** (double or null, required, °C): Ambient temperature measurement in degrees Celsius when the upstream feed publishes value type temperature.
- **`humidity_percent`** (double or null, required, %): Relative humidity in percent when the upstream feed publishes value type humidity.
- **`pressure_pa`** (double or null, required, Pa): Atmospheric pressure in pascals when the upstream feed publishes value type pressure.
- **`pressure_sealevel_pa`** (double or null, required, Pa): Atmospheric pressure reduced to sea level in pascals when the upstream feed publishes value type pressure_at_sealevel.
- **`noise_laeq_db`** (double or null, required, dB(A)): Equivalent continuous sound level in A-weighted decibels when the upstream feed publishes value type noise_LAeq.
- **`noise_la_min_db`** (double or null, required, dB(A)): Minimum A-weighted sound level in decibels when the upstream feed publishes value type noise_LA_min.
- **`noise_la_max_db`** (double or null, required, dB(A)): Maximum A-weighted sound level in decibels when the upstream feed publishes value type noise_LA_max.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "sensor_id": 0,
  "timestamp": "string",
  "sensor_type_name": "string",
  "pm10_ug_m3": 0,
  "pm2_5_ug_m3": 0,
  "pm1_0_ug_m3": 0,
  "pm4_0_ug_m3": 0,
  "temperature_celsius": 0,
  "humidity_percent": 0,
  "pressure_pa": 0,
  "pressure_sealevel_pa": 0,
  "noise_laeq_db": 0,
  "noise_la_min_db": 0,
  "noise_la_max_db": 0
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

- xRegistry manifest: [`xreg/sensor-community.xreg.json`](xreg/sensor-community.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
