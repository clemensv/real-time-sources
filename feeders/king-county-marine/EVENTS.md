# King County Marine feeder Events

King County Marine publishes marine transit schedule and status updates from King County Metro marine feeds for King County water-taxi routes and sailings. These events help consumers monitor mobility operations, passenger information, and traffic conditions without polling the upstream source directly.

## At a glance

- **Event types:** 2 documented event types (6 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 1 reference/catalog event type and 1 telemetry event type.
- **Identity:** `{station_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `king-county-marine`. The record key is `{station_id}`. In plain language, `{station_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['king-county-marine'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `maritime/us/wa/king-county/king-county-marine/+/info`, `maritime/us/wa/king-county/king-county-marine/+/water-quality`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('maritime/us/wa/king-county/king-county-marine/+/info', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `king-county-marine`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/king-county-marine')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Station

CloudEvents type: `US.WA.KingCounty.Marine.Station`

#### What it tells you

A reference record from King County Metro marine feeds for a station, stop, route, site, or other transport resource. It gives consumers stable identifiers and labels needed to interpret realtime updates.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is stable bridge identifier for the buoy or mooring dataset. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `king-county-marine`, key `{station_id}` |
| `MQTT/5.0` | topic `maritime/us/wa/king-county/king-county-marine/{station_id}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/king-county-marine`, message subject `{station_id}` |

#### Payload

`Station` payloads are JSON object. Required fields: `station_id`, `station_name`, `dataset_id`, `dataset_name`, `dataset_url`, `sensor_level`.

- **`station_id`** (string, required): Stable bridge identifier for the buoy or mooring dataset.
- **`station_name`** (string, required): Human-readable station name derived from the dataset title.
- **`dataset_id`** (string, required): Socrata dataset identifier for the source dataset.
- **`dataset_name`** (string, required): Original King County dataset title.
- **`dataset_url`** (string, required): Dataset page URL on data.kingcounty.gov.
- **`sensor_level`** (string, required): Sensor position classification inferred from the dataset title, such as surface, bottom, or water-column.
- **`latitude`** (double or null, optional): Station latitude in decimal degrees north, parsed from the dataset description.
- **`longitude`** (double or null, optional): Station longitude in decimal degrees east of Greenwich; King County locations are negative because they lie west of Greenwich.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "station_name": "string",
  "dataset_id": "string",
  "dataset_name": "string",
  "dataset_url": "string",
  "sensor_level": "string",
  "latitude": 0,
  "longitude": 0
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Water Quality Reading

CloudEvents type: `US.WA.KingCounty.Marine.WaterQualityReading`

#### What it tells you

A transport update from King County Metro marine feeds. It carries marine transit schedule and status updates for King County water-taxi routes and sailings.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is stable bridge identifier for the buoy or mooring dataset. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `king-county-marine`, key `{station_id}` |
| `MQTT/5.0` | topic `maritime/us/wa/king-county/king-county-marine/{station_id}/water-quality`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/king-county-marine`, message subject `{station_id}` |

#### Payload

`Water Quality Reading` payloads are JSON object. Required fields: `station_id`, `station_name`, `observation_time`.

- **`station_id`** (string, required): Stable bridge identifier for the buoy or mooring dataset.
- **`station_name`** (string, required): Human-readable station name derived from the dataset title.
- **`observation_time`** (string, required): Observation timestamp normalized to UTC ISO 8601 form.
- **`water_temperature_c`** (double or null, optional, Cel (°C)): Water temperature in degrees Celsius.
- **`conductivity_s_m`** (double or null, optional, S/m): Electrical conductivity in siemens per meter.
- **`pressure_dbar`** (double or null, optional, dbar): Water pressure in decibar as published by the raw datasets.
- **`dissolved_oxygen_mg_l`** (double or null, optional, mg/L): Dissolved oxygen concentration in milligrams per liter.
- **`ph`** (double or null, optional): Measured pH value.
- **`chlorophyll_ug_l`** (double or null, optional, ug/L (µg/L)): Chlorophyll fluorescence or chlorophyll concentration in micrograms per liter.
- **`turbidity_ntu`** (double or null, optional, NTU): Turbidity in nephelometric turbidity units.
- **`chlorophyll_stddev_ug_l`** (double or null, optional, ug/L (µg/L)): Standard deviation of chlorophyll fluorescence in micrograms per liter.
- **`turbidity_stddev_ntu`** (double or null, optional, NTU): Standard deviation of turbidity in nephelometric turbidity units.
- **`salinity_psu`** (double or null, optional, PSU): Salinity in practical salinity units.
- **`specific_conductivity_s_m`** (double or null, optional, S/m): Specific conductivity in siemens per meter.
- **`dissolved_oxygen_saturation_pct`** (double or null, optional, P1 (%)): Dissolved oxygen saturation as a percentage.
- **`nitrate_umol`** (double or null, optional, umol (µmol)): Nitrate or nitrate-plus-nitrite concentration in micromoles.
- **`nitrate_mg_l`** (double or null, optional, mg/L): Nitrate or nitrate-plus-nitrite concentration in milligrams per liter.
- **`wind_direction_deg`** (double or null, optional, deg (°)): Wind direction in degrees at the buoy surface.
- **`wind_speed_m_s`** (double or null, optional, m/s): Wind speed in meters per second at the buoy surface.
- **`photosynthetically_active_radiation_umol_s_m2`** (double or null, optional, umol/s/m2 (µmol/s/m²)): Photosynthetically active radiation in micromoles per second per square meter.
- **`air_temperature_f`** (double or null, optional, [degF] (°F)): Air temperature in degrees Fahrenheit.
- **`air_humidity_pct`** (double or null, optional, P1 (%)): Relative humidity percentage.
- **`air_pressure_in_hg`** (double or null, optional, [in_i'Hg] (inHg)): Air pressure in inches of mercury.
- **`system_battery_v`** (double or null, optional, V): System battery voltage in volts.
- **`sensor_battery_v`** (double or null, optional, V): Sensor or sonde battery voltage in volts.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "station_name": "string",
  "observation_time": "string",
  "water_temperature_c": 0,
  "conductivity_s_m": 0,
  "pressure_dbar": 0,
  "dissolved_oxygen_mg_l": 0,
  "ph": 0,
  "chlorophyll_ug_l": 0,
  "turbidity_ntu": 0,
  "chlorophyll_stddev_ug_l": 0,
  "turbidity_stddev_ntu": 0,
  "salinity_psu": 0,
  "specific_conductivity_s_m": 0,
  "dissolved_oxygen_saturation_pct": 0,
  "nitrate_umol": 0,
  "nitrate_mg_l": 0,
  "wind_direction_deg": 0,
  "wind_speed_m_s": 0,
  "photosynthetically_active_radiation_umol_s_m2": 0,
  "air_temperature_f": 0,
  "air_humidity_pct": 0,
  "air_pressure_in_hg": 0,
  "system_battery_v": 0,
  "sensor_battery_v": 0
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

- xRegistry manifest: [`xreg/king_county_marine.xreg.json`](xreg/king_county_marine.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
