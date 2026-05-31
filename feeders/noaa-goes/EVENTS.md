# NOAA GOES / SWPC feeder Events

MQTT 5 variant of NOAA GOES space-weather telemetry, alerts, and flares.

## At a glance

- **Event types:** 10 documented event types (22 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 10 telemetry event types.
- **Identity:** `{product_id}`, `{observation_time}`, `{satellite}/{energy}/{time_tag}`, `{satellite}/{time_tag}`, `{satellite}/{begin_time}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `noaa-goes`. The record key is `{product_id}`, `{observation_time}`, `{satellite}/{energy}/{time_tag}`, `{satellite}/{time_tag}`, `{satellite}/{begin_time}`. Each key template is explained in the event catalog below. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['noaa-goes'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `space-weather/us/noaa/noaa-goes/+/xrs/+`, `space-weather/us/noaa/noaa-goes/+/sgps/+`, `space-weather/us/noaa/noaa-goes/+/exis/+`, `space-weather/us/noaa/noaa-goes/+/magnetometer/+`, `space-weather/us/noaa/noaa-goes/alerts/+/alert`, `space-weather/us/noaa/noaa-goes/flares/+/+/flare`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('space-weather/us/noaa/noaa-goes/+/xrs/+', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `noaa-goes`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/noaa-goes')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Space Weather Alert

CloudEvents type: `Microsoft.OpenData.US.NOAA.SWPC.SpaceWeatherAlert`

#### What it tells you

NOAA Space Weather Prediction Center alert, watch, or warning bulletin. Alerts are issued for observed or expected space weather conditions that may affect technology systems on Earth or in space, including geomagnetic storms (ALTK/WARK), solar radiation storms (ALTPC/WARPC), and radio blackouts (ALTXR/SUM).

#### Identity

Each event identifies the real-world resource with `{product_id}`. `{product_id}` is unique SWPC product identifier for this alert bulletin, combining the alert type code and serial number or date (e.g., 'ALTK04-20240101'). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-goes`, key `{product_id}` |
| `MQTT/5.0` | topic `space-weather/us/noaa/noaa-goes/alerts/{product_id}/alert`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/noaa-goes`, message subject `{product_id}` |

#### Payload

`Space Weather Alert` payloads are JSON object. Required fields: `product_id`, `issue_datetime`, `message`.

- **`product_id`** (string, required): Unique SWPC product identifier for this alert bulletin, combining the alert type code and serial number or date (e.g., 'ALTK04-20240101'). Used as the Kafka message key.
- **`issue_datetime`** (string, required): Date and time the alert was issued by SWPC, formatted as 'YYYY Mon DD HHMM UTC' (e.g., '2024 Jan 01 0030 UTC').
- **`message`** (string, required): Full text body of the SWPC alert bulletin, including the message code, serial number, issue time, IP code, validity period, and detailed description of the observed or expected space weather condition with numerical thresholds.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "product_id": "string",
  "issue_datetime": "string",
  "message": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Planetary Kindex

CloudEvents type: `Microsoft.OpenData.US.NOAA.SWPC.PlanetaryKIndex`

#### What it tells you

Planetary K-index (Kp) observation from the NOAA Space Weather Prediction Center. The Kp index quantifies disturbances in the horizontal component of Earth's magnetic field on a 0-9 quasi-logarithmic scale, derived from 3-hour standardized K values at a global network of ground magnetometer stations. Values of Kp >= 5 indicate geomagnetic storm conditions (G1-G5 on the NOAA scale).

#### Identity

Each event identifies the real-world resource with `{observation_time}`. `{observation_time}` is UTC date-time marking the start of the 3-hour Kp observation period, in 'YYYY-MM-DD HH:MM:SS.fff' format from the SWPC noaa-planetary-k-index endpoint. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-goes`, key `{observation_time}` |

#### Payload

`Planetary Kindex` payloads are JSON object. Required fields: `observation_time`, `kp`, `a_running`, `station_count`.

- **`observation_time`** (string, required): UTC date-time marking the start of the 3-hour Kp observation period, in 'YYYY-MM-DD HH:MM:SS.fff' format from the SWPC noaa-planetary-k-index endpoint.
- **`kp`** (double, required): Planetary K-index value for this 3-hour period, ranging from 0.00 (quiet) to 9.00 (extreme storm). Each unit increase corresponds to roughly a doubling of geomagnetic disturbance amplitude. Storm thresholds: G1 (Kp=5), G2 (Kp=6), G3 (Kp=7), G4 (Kp=8), G5 (Kp=9). Constraints: minimum `0`, maximum `9`.
- **`a_running`** (double, required, nT): Running daily planetary A-index (Ap), a linear measure of geomagnetic activity derived from the eight 3-hour Kp values via a standard conversion table. Ap is measured in units of 2 nT.
- **`station_count`** (integer, required): Number of ground magnetometer stations contributing data to this Kp determination. Typical station count is 8-13; fewer stations may reduce measurement confidence.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "observation_time": "string",
  "kp": 0,
  "a_running": 0,
  "station_count": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Solar Wind Summary

CloudEvents type: `Microsoft.OpenData.US.NOAA.SWPC.SolarWindSummary`

#### What it tells you

Latest solar wind conditions summary from the DSCOVR satellite at the L1 Lagrange point (~1.5 million km sunward of Earth), combining proton bulk speed from the summary/solar-wind-speed endpoint and interplanetary magnetic field from the summary/solar-wind-mag-field endpoint. Provides a single snapshot of current conditions, updated approximately every minute.

#### Identity

Each event identifies the real-world resource with `{observation_time}`. `{observation_time}` is UTC date-time of the solar wind measurement from DSCOVR, in ISO 8601 format. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-goes`, key `{observation_time}` |

#### Payload

`Solar Wind Summary` payloads are JSON object. Required fields: `observation_time`, `wind_speed`, `bt`, `bz`.

- **`observation_time`** (string, required): UTC date-time of the solar wind measurement from DSCOVR, in ISO 8601 format.
- **`wind_speed`** (double, required, km/s): Solar wind proton bulk speed measured by DSCOVR at L1. Typical slow-wind values are 300-400 km/s; fast streams and CME passages can reach 500-1000+ km/s.
- **`bt`** (double, required, nT): Interplanetary magnetic field total magnitude (Bt) measured by the DSCOVR magnetometer at L1. Quiet-time values are typically 3-6 nT; values above 20 nT indicate strong solar wind driving.
- **`bz`** (double, required, nT): Interplanetary magnetic field north-south component in Geocentric Solar Magnetospheric (GSM) coordinates (Bz GSM). Sustained negative (southward) Bz is the primary driver of geomagnetic storms via magnetic reconnection at Earth's magnetopause.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "observation_time": "string",
  "wind_speed": 0,
  "bt": 0,
  "bz": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Solar Wind Plasma

CloudEvents type: `Microsoft.OpenData.US.NOAA.SWPC.SolarWindPlasma`

#### What it tells you

One-minute resolution solar wind plasma measurement from the DSCOVR satellite Faraday Cup instrument at the L1 Lagrange point, as reported by the SWPC solar-wind/plasma-7-day endpoint. Includes proton density, bulk speed, and ion temperature. DSCOVR provides approximately 15-45 minutes of advance warning before solar wind structures reach Earth's magnetosphere.

#### Identity

Each event identifies the real-world resource with `{observation_time}`. `{observation_time}` is UTC date-time of the plasma measurement, in 'YYYY-MM-DD HH:MM:SS.fff' format. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-goes`, key `{observation_time}` |

#### Payload

`Solar Wind Plasma` payloads are JSON object. Required fields: `observation_time`.

- **`observation_time`** (string, required): UTC date-time of the plasma measurement, in 'YYYY-MM-DD HH:MM:SS.fff' format.
- **`density`** (double or null, optional, n/cm³): Solar wind proton number density measured by the DSCOVR Faraday Cup. Typical quiet-time values are 3-10 n/cm³; values above 20 n/cm³ may indicate a coronal mass ejection passage or a compressed solar wind region.
- **`speed`** (double or null, optional, km/s): Solar wind proton bulk speed measured by DSCOVR. Typical quiet-time values are 300-400 km/s (slow wind); high-speed streams reach 500-800 km/s and CME-driven shocks can exceed 1000 km/s.
- **`temperature`** (double or null, optional, K): Solar wind ion temperature measured by DSCOVR. Typical values are 10,000-200,000 K; elevated temperatures often accompany high-speed streams and interplanetary shock passages.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "observation_time": "string",
  "density": 0,
  "speed": 0,
  "temperature": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Solar Wind Mag Field

CloudEvents type: `Microsoft.OpenData.US.NOAA.SWPC.SolarWindMagField`

#### What it tells you

One-minute resolution interplanetary magnetic field (IMF) vector measurement from the DSCOVR satellite magnetometer at the L1 Lagrange point, as reported by the SWPC solar-wind/mag-7-day endpoint. Provides the full magnetic field vector in Geocentric Solar Magnetospheric (GSM) coordinates plus total magnitude. The Bz GSM component is the primary indicator of geomagnetic storm potential.

#### Identity

Each event identifies the real-world resource with `{observation_time}`. `{observation_time}` is UTC date-time of the magnetic field measurement, in 'YYYY-MM-DD HH:MM:SS.fff' format. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-goes`, key `{observation_time}` |

#### Payload

`Solar Wind Mag Field` payloads are JSON object. Required fields: `observation_time`.

- **`observation_time`** (string, required): UTC date-time of the magnetic field measurement, in 'YYYY-MM-DD HH:MM:SS.fff' format.
- **`bx_gsm`** (double or null, optional, nT): IMF X-component in GSM coordinates, directed from Earth toward the Sun along the Earth-Sun line.
- **`by_gsm`** (double or null, optional, nT): IMF Y-component in GSM coordinates, perpendicular to the Earth-Sun line in the magnetic equatorial plane. Influences the dawn-dusk electric field in the magnetosphere.
- **`bz_gsm`** (double or null, optional, nT): IMF Z-component in GSM coordinates (north-south). Sustained negative (southward) Bz is the primary driver of geomagnetic storms through magnetic reconnection at the dayside magnetopause. Values below -10 nT can produce G2+ storms.
- **`lon_gsm`** (double or null, optional, degrees (°)): IMF longitude angle in GSM coordinates, measured in the GSM X-Y plane from the Earth-Sun line.
- **`lat_gsm`** (double or null, optional, degrees (°)): IMF latitude angle in GSM coordinates, measured from the GSM X-Y plane toward the Z-axis.
- **`bt`** (double or null, optional, nT): Total interplanetary magnetic field magnitude, computed as the vector sum sqrt(Bx² + By² + Bz²). Typical quiet-time values are 3-6 nT; values above 20 nT indicate strong solar wind magnetic driving.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "observation_time": "string",
  "bx_gsm": 0,
  "by_gsm": 0,
  "bz_gsm": 0,
  "lon_gsm": 0,
  "lat_gsm": 0,
  "bt": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Goes Xray Flux

CloudEvents type: `Microsoft.OpenData.US.NOAA.SWPC.GoesXrayFlux`

#### What it tells you

One-minute resolution full-disk solar X-ray flux measurement from the GOES primary satellite XRS (X-Ray Sensor) instrument, as reported by the SWPC goes/primary/xrays-7-day endpoint. Two energy bands are reported: 0.05-0.4 nm (short, harder X-rays) and 0.1-0.8 nm (long, softer X-rays). The 0.1-0.8 nm band is used for the official solar flare classification scale (A < B < C < M < X).

#### Identity

Each event identifies the real-world resource with `{satellite}/{energy}/{time_tag}`. `{satellite}` is GOES satellite number providing the measurement (e.g., 18 for GOES-18, 19 for GOES-19); `{energy}` is x-ray energy band identifier: '0.05-0.4nm' (short wavelength, harder X-rays) or '0.1-0.8nm' (long wavelength, softer X-rays used for flare classification); `{time_tag}` is UTC date-time of the X-ray flux measurement from the GOES XRS instrument, in ISO 8601 format (e.g., '2024-01-01T00:00:00Z'). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-goes`, key `{satellite}/{energy}/{time_tag}` |
| `MQTT/5.0` | topic `space-weather/us/noaa/noaa-goes/{satellite}/xrs/{event}`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/noaa-goes`, message subject `{satellite}/{energy}/{time_tag}`; application properties event `{event}` |

#### Payload

`Goes Xray Flux` payloads are JSON object. Required fields: `time_tag`, `satellite`, `flux`, `energy`.

- **`time_tag`** (string, required): UTC date-time of the X-ray flux measurement from the GOES XRS instrument, in ISO 8601 format (e.g., '2024-01-01T00:00:00Z').
- **`satellite`** (integer, required): GOES satellite number providing the measurement (e.g., 18 for GOES-18, 19 for GOES-19). The primary operational GOES satellite changes when new spacecraft are commissioned.
- **`flux`** (double, required, W/m²): Solar X-ray irradiance in the specified energy band. Flare classification thresholds for the 0.1-0.8 nm band: A (< 1e-7), B (1e-7 to 1e-6), C (1e-6 to 1e-5), M (1e-5 to 1e-4), X (>= 1e-4). Background is typically A1-B1 level during solar minimum.
- **`energy`** (string, required): X-ray energy band identifier: '0.05-0.4nm' (short wavelength, harder X-rays) or '0.1-0.8nm' (long wavelength, softer X-rays used for flare classification).
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "time_tag": "string",
  "satellite": 0,
  "flux": 0,
  "energy": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Goes Proton Flux

CloudEvents type: `Microsoft.OpenData.US.NOAA.SWPC.GoesProtonFlux`

#### What it tells you

Five-minute resolution integral proton flux measurement from the GOES primary satellite SEISS/SGPS (Space Environment In-Situ Suite / Solar and Galactic Proton Sensor) instrument, as reported by the SWPC goes/primary/integral-protons-7-day endpoint. Four energy thresholds are reported. The >= 10 MeV channel is used for the official NOAA S-scale solar radiation storm classification (S1-S5).

#### Identity

Each event identifies the real-world resource with `{satellite}/{energy}/{time_tag}`. `{satellite}` is GOES satellite number providing the measurement (e.g., 19 for GOES-19); `{energy}` is proton energy threshold identifier: '>=10 MeV' (NOAA S-scale metric), '>=50 MeV', '>=100 MeV', or '>=500 MeV'; `{time_tag}` is UTC date-time of the proton flux measurement in ISO 8601 format. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-goes`, key `{satellite}/{energy}/{time_tag}` |
| `MQTT/5.0` | topic `space-weather/us/noaa/noaa-goes/{satellite}/sgps/{event}`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/noaa-goes`, message subject `{satellite}/{energy}/{time_tag}`; application properties event `{event}` |

#### Payload

`Goes Proton Flux` payloads are JSON object. Required fields: `time_tag`, `satellite`, `flux`, `energy`.

- **`time_tag`** (string, required): UTC date-time of the proton flux measurement in ISO 8601 format.
- **`satellite`** (integer, required): GOES satellite number providing the measurement (e.g., 19 for GOES-19).
- **`flux`** (double, required, pfu): Integral proton flux above the specified energy threshold, in particle flux units (pfu = protons/cm²/sr/s). An S1 minor radiation storm is declared when >= 10 MeV flux exceeds 10 pfu. S5 extreme: >= 100,000 pfu.
- **`energy`** (string, required): Proton energy threshold identifier: '>=10 MeV' (NOAA S-scale metric), '>=50 MeV', '>=100 MeV', or '>=500 MeV'. Higher thresholds indicate more energetic and penetrating radiation.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "time_tag": "string",
  "satellite": 0,
  "flux": 0,
  "energy": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Goes Electron Flux

CloudEvents type: `Microsoft.OpenData.US.NOAA.SWPC.GoesElectronFlux`

#### What it tells you

Five-minute resolution integral electron flux measurement from the GOES primary satellite SEISS/SGPS instrument, as reported by the SWPC goes/primary/integral-electrons-3-day endpoint. The >= 2 MeV channel is monitored for deep dielectric charging risk to geosynchronous spacecraft. Elevated fluxes (> 1000 e/cm²/sr/s) sustained for several days can cause internal charging failures in satellite electronics.

#### Identity

Each event identifies the real-world resource with `{satellite}/{energy}/{time_tag}`. `{satellite}` is GOES satellite number providing the measurement (e.g., 19 for GOES-19); `{energy}` is electron energy threshold identifier, currently '>=2 MeV'; `{time_tag}` is UTC date-time of the electron flux measurement in ISO 8601 format. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-goes`, key `{satellite}/{energy}/{time_tag}` |
| `MQTT/5.0` | topic `space-weather/us/noaa/noaa-goes/{satellite}/exis/{event}`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/noaa-goes`, message subject `{satellite}/{energy}/{time_tag}`; application properties event `{event}` |

#### Payload

`Goes Electron Flux` payloads are JSON object. Required fields: `time_tag`, `satellite`, `flux`, `energy`.

- **`time_tag`** (string, required): UTC date-time of the electron flux measurement in ISO 8601 format.
- **`satellite`** (integer, required): GOES satellite number providing the measurement (e.g., 19 for GOES-19).
- **`flux`** (double, required, e/(cm²·sr·s)): Integral electron flux above the specified energy threshold, in electrons per cm² per steradian per second. Values above 1000 indicate elevated deep dielectric charging risk for geosynchronous satellites.
- **`energy`** (string, required): Electron energy threshold identifier, currently '>=2 MeV'. This channel is monitored for spacecraft internal charging hazard assessment.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "time_tag": "string",
  "satellite": 0,
  "flux": 0,
  "energy": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Goes Magnetometer

CloudEvents type: `Microsoft.OpenData.US.NOAA.SWPC.GoesMagnetometer`

#### What it tells you

One-minute resolution magnetic field measurement from the GOES primary satellite magnetometer at geostationary orbit (~6.6 Earth radii), as reported by the SWPC goes/primary/magnetometers-7-day endpoint. The field is measured in the spacecraft-centered HEN coordinate system where Hp is parallel to Earth's rotation axis, He is perpendicular in the east-west direction, and Hn is radially earthward. During geomagnetic storms, Hp can drop dramatically or even become negative, indicating magnetopause compression.

#### Identity

Each event identifies the real-world resource with `{satellite}/{time_tag}`. `{satellite}` is GOES satellite number providing the measurement (e.g., 19 for GOES-19); `{time_tag}` is UTC date-time of the magnetic field measurement in ISO 8601 format. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-goes`, key `{satellite}/{time_tag}` |
| `MQTT/5.0` | topic `space-weather/us/noaa/noaa-goes/{satellite}/magnetometer/{event}`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/noaa-goes`, message subject `{satellite}/{time_tag}`; application properties event `{event}` |

#### Payload

`Goes Magnetometer` payloads are JSON object. Required fields: `time_tag`, `satellite`.

- **`time_tag`** (string, required): UTC date-time of the magnetic field measurement in ISO 8601 format.
- **`satellite`** (integer, required): GOES satellite number providing the measurement (e.g., 19 for GOES-19).
- **`he`** (double or null, optional, nT): Magnetic field He component: perpendicular to the satellite-Earth direction and the dipole axis, positive eastward. Measures the east-west distortion of the geomagnetic field at geostationary orbit.
- **`hp`** (double or null, optional, nT): Magnetic field Hp component: parallel to Earth's dipole axis, positive northward. During quiet times Hp is typically 80-120 nT; during intense geomagnetic storms (G4-G5) it can drop below zero, indicating the magnetopause has been compressed inside geostationary orbit.
- **`hn`** (double or null, optional, nT): Magnetic field Hn component: along the satellite-Earth direction, positive radially earthward.
- **`total`** (double or null, optional, nT): Total magnetic field magnitude at geostationary orbit, computed as sqrt(He² + Hp² + Hn²). Typical quiet-time values are 100-120 nT.
- **`arcjet_flag`** (boolean or null, optional): When true, the satellite's electric propulsion (arcjet) thrusters are firing, which causes magnetic field contamination. Magnetometer readings during arcjet events should be treated with caution as they may not reflect the ambient geomagnetic field.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "time_tag": "string",
  "satellite": 0,
  "he": 0,
  "hp": 0,
  "hn": 0,
  "total": 0,
  "arcjet_flag": false
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Xray Flare

CloudEvents type: `Microsoft.OpenData.US.NOAA.SWPC.XrayFlare`

#### What it tells you

Individual solar X-ray flare event detected by the GOES primary satellite XRS instrument, as reported by the SWPC goes/primary/xray-flares-7-day endpoint. Each record represents a discrete flare event with onset, peak, and end times plus X-ray classifications on the standard A/B/C/M/X logarithmic scale. The flare classification is based on peak 0.1-0.8 nm X-ray flux: C-class (1e-6 W/m²), M-class (1e-5), X-class (1e-4).

#### Identity

Each event identifies the real-world resource with `{satellite}/{begin_time}`. `{satellite}` is GOES satellite number that detected this flare event (e.g., 18 for GOES-18, 19 for GOES-19); `{begin_time}` is UTC date-time of the flare onset (start of the X-ray flux rise above background), in ISO 8601 format. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-goes`, key `{satellite}/{begin_time}` |
| `MQTT/5.0` | topic `space-weather/us/noaa/noaa-goes/flares/{flare_class}/{begin_time}/flare`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/noaa-goes`, message subject `{satellite}/{begin_time}`; application properties flare_class `{flare_class}` |

#### Payload

`Xray Flare` payloads are JSON object. Required fields: `time_tag`, `begin_time`, `satellite`.

- **`time_tag`** (string, required): UTC date-time when this flare record was reported/filed by SWPC, in ISO 8601 format.
- **`begin_time`** (string, required): UTC date-time of the flare onset (start of the X-ray flux rise above background), in ISO 8601 format. Used as part of the Kafka key to uniquely identify each flare event.
- **`begin_class`** (string or null, optional): X-ray classification at flare onset, e.g., 'B6.9' or 'C1.0'. Format is a letter (A/B/C/M/X) followed by a decimal multiplier within that decade of flux.
- **`max_time`** (string or null, optional): UTC date-time of the peak X-ray flux during the flare, in ISO 8601 format.
- **`max_class`** (string or null, optional): X-ray classification at flare peak, e.g., 'C1.2', 'M5.3', 'X1.0'. This is the official flare magnitude used in space weather bulletins.
- **`max_xrlong`** (double or null, optional, W/m²): Peak X-ray flux in the 0.1-0.8 nm (long wavelength) band at the time of maximum.
- **`max_ratio`** (double or null, optional): Ratio of 0.05-0.4 nm (short) to 0.1-0.8 nm (long) X-ray flux at flare maximum. Higher ratios indicate a spectrally harder (more energetic) flare, which correlates with stronger ionospheric effects.
- **`max_ratio_time`** (string or null, optional): UTC date-time of the maximum short/long flux ratio, in ISO 8601 format. May differ from max_time.
- **`current_int_xrlong`** (double or null, optional, J/m²): Current time-integrated X-ray flux in the 0.1-0.8 nm band since flare onset, representing total X-ray energy delivered.
- **`end_time`** (string or null, optional): UTC date-time when the flare X-ray flux returned to half the peak value above background, in ISO 8601 format. Null if the flare is still in progress.
- **`end_class`** (string or null, optional): X-ray classification at the declared end of the flare event.
- **`satellite`** (integer, required): GOES satellite number that detected this flare event (e.g., 18 for GOES-18, 19 for GOES-19).
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "time_tag": "string",
  "begin_time": "string",
  "begin_class": "string",
  "max_time": "string",
  "max_class": "string",
  "max_xrlong": 0,
  "max_ratio": 0,
  "max_ratio_time": "string",
  "current_int_xrlong": 0,
  "end_time": "string",
  "end_class": "string",
  "satellite": 0
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

- xRegistry manifest: [`xreg/noaa-goes.xreg.json`](xreg/noaa-goes.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
