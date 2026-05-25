# Wallonia ISSeP Events

Wallonia ISSeP Air Quality publishes pollutant concentration measurements from Wallonia's Institut Scientifique de Service Public (ISSeP) for Walloon air-quality monitoring stations. These events help consumers build monitoring, alerting, analytics, and dashboards without polling the upstream API directly.

## At a glance

- **Event types:** 2 documented event types (6 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 2 telemetry event types.
- **Identity:** `{configuration_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `wallonia-issep`. The record key is `{configuration_id}`. In plain language, `{configuration_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['wallonia-issep'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `air-quality/be/issep/wallonia-issep/+/+/info`, `air-quality/be/issep/wallonia-issep/+/+/observation`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('air-quality/be/issep/wallonia-issep/+/+/info', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `wallonia-issep`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/wallonia-issep')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Sensor Configuration

CloudEvents type: `be.issep.airquality.SensorConfiguration`

#### What it tells you

A current environmental measurement from Wallonia's Institut Scientifique de Service Public (ISSeP). It carries pollutant concentration measurements when the upstream feed reports a new or refreshed value.

#### Identity

Each event identifies the real-world resource with `{configuration_id}`. `{configuration_id}` is stable numeric identifier of the sensor configuration from the upstream id_configuration field. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `wallonia-issep`, key `{configuration_id}` |
| `MQTT/5.0` | topic `air-quality/be/issep/wallonia-issep/{province}/{configuration_id}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/wallonia-issep`, message subject `{configuration_id}`; application properties province `{province}` |

#### Payload

`Sensor Configuration` payloads are JSON object. Required fields: `configuration_id`, `province`.

- **`configuration_id`** (string, required): Stable numeric identifier of the sensor configuration from the upstream id_configuration field. Converted to string because it serves as the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]+$`.
- **`province`** (string, required): Slug of the Walloon province where the sensor is located (e.g. brabant-wallon, hainaut, liege, luxembourg, namur, or "unknown" sentinel if location is not yet mapped). Matches the {province} MQTT topic axis.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "configuration_id": "string",
  "province": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Observation

CloudEvents type: `be.issep.airquality.Observation`

#### What it tells you

A current environmental measurement from Wallonia's Institut Scientifique de Service Public (ISSeP). It carries pollutant concentration measurements when the upstream feed reports a new or refreshed value.

#### Identity

Each event identifies the real-world resource with `{configuration_id}`. `{configuration_id}` is stable numeric sensor configuration identifier from id_configuration. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `wallonia-issep`, key `{configuration_id}` |
| `MQTT/5.0` | topic `air-quality/be/issep/wallonia-issep/{province}/{configuration_id}/observation`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/wallonia-issep`, message subject `{configuration_id}`; application properties province `{province}` |

#### Payload

`Observation` payloads are JSON object. Required fields: `configuration_id`, `province`, `moment`.

- **`configuration_id`** (string, required): Stable numeric sensor configuration identifier from id_configuration. Matches the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]+$`.
- **`province`** (string, required): Slug of the Walloon province where the sensor is located (e.g. brabant-wallon, hainaut, liege, luxembourg, namur, or "unknown" sentinel if location is not yet mapped). Matches the {province} MQTT topic axis.
- **`moment`** (string, required): ISO 8601 observation timestamp from the upstream moment field, e.g. '2026-04-08T09:09:13+02:00'. Preserved as-is from the API response.
- **`co`** (int32 or null, optional): Raw carbon monoxide electrochemical sensor reading in internal units.
- **`no`** (int32 or null, optional): Raw nitric oxide electrochemical sensor reading in internal units.
- **`no2`** (int32 or null, optional): Raw nitrogen dioxide electrochemical sensor reading in internal units. Negative values are valid.
- **`o3no2`** (int32 or null, optional): Raw combined ozone and nitrogen dioxide electrochemical sensor reading in internal units. Negative values are valid.
- **`ppbno`** (double or null, optional, ppb): Calibrated nitric oxide concentration in parts per billion (ppb).
- **`ppbno_statut`** (int32 or null, optional): Quality status flag for ppbno. 100 indicates valid, 0 indicates invalid or unavailable.
- **`ppbno2`** (double or null, optional, ppb): Calibrated nitrogen dioxide concentration in parts per billion (ppb).
- **`ppbno2_statut`** (int32 or null, optional): Quality status flag for ppbno2. 100 indicates valid, 0 indicates invalid or unavailable.
- **`ppbo3`** (double or null, optional, ppb): Calibrated ozone concentration in parts per billion (ppb).
- **`ppbo3_statut`** (int32 or null, optional): Quality status flag for ppbo3. 100 indicates valid, 0 indicates invalid or unavailable.
- **`ugpcmno`** (double or null, optional, µg/m³): Calibrated nitric oxide concentration in micrograms per cubic meter (µg/m³).
- **`ugpcmno_statut`** (int32 or null, optional): Quality status flag for ugpcmno. 100 indicates valid, 0 indicates invalid or unavailable.
- **`ugpcmno2`** (double or null, optional, µg/m³): Calibrated nitrogen dioxide concentration in micrograms per cubic meter (µg/m³).
- **`ugpcmno2_statut`** (int32 or null, optional): Quality status flag for ugpcmno2. 100 indicates valid, 0 indicates invalid or unavailable.
- **`ugpcmo3`** (double or null, optional, µg/m³): Calibrated ozone concentration in micrograms per cubic meter (µg/m³).
- **`ugpcmo3_statut`** (int32 or null, optional): Quality status flag for ugpcmo3. 100 indicates valid, 0 indicates invalid or unavailable.
- **`bme_t`** (double or null, optional, °C): Temperature reading from the BME280 environmental sensor in degrees Celsius.
- **`bme_t_statut`** (int32 or null, optional): Quality status flag for bme_t. 100 indicates valid, 0 indicates invalid or unavailable.
- **`bme_pres`** (int32 or null, optional, Pa): Atmospheric pressure reading from the BME280 sensor in Pascals.
- **`bme_pres_statut`** (int32 or null, optional): Quality status flag for bme_pres. 100 indicates valid, 0 indicates invalid or unavailable.
- **`bme_rh`** (double or null, optional, %): Relative humidity reading from the BME280 sensor as a percentage.
- **`bme_rh_statut`** (int32 or null, optional): Quality status flag for bme_rh. 100 indicates valid, 0 indicates invalid or unavailable.
- **`pm1`** (double or null, optional, µg/m³): Particulate matter concentration for particles under 1 micrometer in µg/m³.
- **`pm1_statut`** (int32 or null, optional): Quality status flag for pm1. 100 indicates valid, 0 indicates invalid or unavailable.
- **`pm25`** (double or null, optional, µg/m³): Particulate matter concentration for particles under 2.5 micrometers in µg/m³.
- **`pm25_statut`** (int32 or null, optional): Quality status flag for pm25. 100 indicates valid, 0 indicates invalid or unavailable.
- **`pm4`** (double or null, optional, µg/m³): Particulate matter concentration for particles under 4 micrometers in µg/m³.
- **`pm4_statut`** (int32 or null, optional): Quality status flag for pm4. 100 indicates valid, 0 indicates invalid or unavailable.
- **`pm10`** (double or null, optional, µg/m³): Particulate matter concentration for particles under 10 micrometers in µg/m³.
- **`pm10_statut`** (int32 or null, optional): Quality status flag for pm10. 100 indicates valid, 0 indicates invalid or unavailable.
- **`vbat`** (double or null, optional, V): Battery voltage of the sensor unit in Volts.
- **`vbat_statut`** (int32 or null, optional): Quality status flag for vbat. 100 indicates valid, 0 indicates invalid or unavailable.
- **`mwh_bat`** (double or null, optional, mWh): Battery energy level in milliwatt-hours. Negative values indicate discharge.
- **`mwh_pv`** (double or null, optional, mWh): Photovoltaic energy generation in milliwatt-hours.
- **`co_rf`** (double or null, optional): Carbon monoxide reference station comparison value.
- **`no_rf`** (double or null, optional): Nitric oxide reference station comparison value.
- **`no2_rf`** (double or null, optional): Nitrogen dioxide reference station comparison value.
- **`o3no2_rf`** (double or null, optional): Combined ozone and nitrogen dioxide reference station comparison value.
- **`o3_rf`** (double or null, optional): Ozone reference station comparison value.
- **`pm10_rf`** (double or null, optional): PM10 reference station comparison value.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "configuration_id": "string",
  "province": "string",
  "moment": "string",
  "co": 0,
  "no": 0,
  "no2": 0,
  "o3no2": 0,
  "ppbno": 0,
  "ppbno_statut": 0,
  "ppbno2": 0,
  "ppbno2_statut": 0,
  "ppbo3": 0,
  "ppbo3_statut": 0,
  "ugpcmno": 0,
  "ugpcmno_statut": 0,
  "ugpcmno2": 0,
  "ugpcmno2_statut": 0,
  "ugpcmo3": 0,
  "ugpcmo3_statut": 0,
  "bme_t": 0,
  "bme_t_statut": 0,
  "bme_pres": 0,
  "bme_pres_statut": 0,
  "bme_rh": 0,
  "bme_rh_statut": 0,
  "pm1": 0,
  "pm1_statut": 0,
  "pm25": 0,
  "pm25_statut": 0,
  "pm4": 0,
  "pm4_statut": 0,
  "pm10": 0,
  "pm10_statut": 0,
  "vbat": 0,
  "vbat_statut": 0,
  "mwh_bat": 0,
  "mwh_pv": 0,
  "co_rf": 0,
  "no_rf": 0,
  "no2_rf": 0,
  "o3no2_rf": 0,
  "o3_rf": 0,
  "pm10_rf": 0
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

- xRegistry manifest: [`xreg/wallonia_issep.xreg.json`](xreg/wallonia_issep.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
