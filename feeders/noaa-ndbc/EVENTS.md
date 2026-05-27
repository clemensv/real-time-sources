# NOAA NDBC feeder Events

MQTT 5 variant of noaa-ndbc events with UNS topics for wildcard subscribers.

## At a glance

- **Event types:** 9 documented event types (27 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 1 reference/catalog event type and 8 telemetry event types.
- **Identity:** `{station_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `noaa-ndbc`. The record key is `{station_id}`. In plain language, `{station_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['noaa-ndbc'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `maritime/us/noaa/noaa-ndbc/+/+/observation`, `maritime/us/noaa/noaa-ndbc/+/+/info`, `maritime/us/noaa/noaa-ndbc/+/+/solar-radiation`, `maritime/us/noaa/noaa-ndbc/+/+/oceanographic`, `maritime/us/noaa/noaa-ndbc/+/+/dart-measurement`, `maritime/us/noaa/noaa-ndbc/+/+/continuous-wind`, `maritime/us/noaa/noaa-ndbc/+/+/supplemental`, `maritime/us/noaa/noaa-ndbc/+/+/detailed-wave-summary`, `maritime/us/noaa/noaa-ndbc/+/+/hourly-rain`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('maritime/us/noaa/noaa-ndbc/+/+/observation', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `noaa-ndbc`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/noaa-ndbc')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Buoy Observation

CloudEvents type: `Microsoft.OpenData.US.NOAA.NDBC.BuoyObservation`

#### What it tells you

Real-time standard meteorological and oceanographic observation from an NDBC buoy, C-MAN station, or partner platform. Sourced from the NDBC latest_obs.txt composite file which is updated every five minutes. Fields cover wind, waves, pressure, temperature, dewpoint, pressure tendency, visibility, and tide.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is NDBC station identifier. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-ndbc`, key `{station_id}` |
| `MQTT/5.0` | topic `maritime/us/noaa/noaa-ndbc/{region}/{station_id}/observation`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/noaa-ndbc`, message subject `{station_id}`; application properties region `{region}` |

#### Payload

`Buoy Observation` payloads are JSON object. Required fields: `station_id`, `latitude`, `longitude`, `timestamp`.

- **`station_id`** (string, required): NDBC station identifier. Five-character alphanumeric code assigned by NDBC (e.g. '41001' for deep-ocean buoys, 'BURL1' for C-MAN stations).
- **`latitude`** (double, required): Latitude of the observing platform in decimal degrees north. Negative values indicate southern hemisphere.
- **`longitude`** (double, required): Longitude of the observing platform in decimal degrees east. Negative values indicate western hemisphere.
- **`timestamp`** (datetime, required): Observation timestamp in UTC, constructed from the YYYY MM DD hh mm columns in the NDBC data.
- **`wind_direction`** (double or null, optional, deg (°)): Wind direction (the direction the wind is coming from) averaged over an 8-minute period for buoys or a 2-minute period for land stations. Unit: degrees true.
- **`wind_speed`** (double or null, optional, m/s): Average wind speed during the observation period: 8 minutes for buoys, 2 minutes for land stations. Unit: meters per second.
- **`gust`** (double or null, optional, m/s): Peak 5-second or 8-second gust speed during the observation period. Unit: meters per second.
- **`wave_height`** (double or null, optional, m): Significant wave height — the average of the highest one-third of all wave heights during a 20-minute sampling period. Unit: meters.
- **`dominant_wave_period`** (double or null, optional, s): Dominant wave period — the period (in seconds) of the wave band with the maximum energy in the spectral wave analysis. Unit: seconds.
- **`average_wave_period`** (double or null, optional, s): Average wave period of all waves during the 20-minute sampling period. Unit: seconds.
- **`mean_wave_direction`** (double or null, optional, deg (°)): Mean wave direction corresponding to the energy at the dominant wave period (DPD). Unit: degrees true.
- **`pressure`** (double or null, optional, hPa): Sea-level pressure reduced using the standard atmosphere from the station elevation. Unit: hectopascals.
- **`air_temperature`** (double or null, optional, CEL (°C)): Air temperature measured at the station. Unit: degrees Celsius.
- **`water_temperature`** (double or null, optional, CEL (°C)): Sea surface temperature. For buoys, measured by a hull-contact sensor near the waterline. Unit: degrees Celsius.
- **`dewpoint`** (double or null, optional, CEL (°C)): Dewpoint temperature computed from air temperature and relative humidity. Unit: degrees Celsius.
- **`pressure_tendency`** (double or null, optional, hPa): Pressure tendency — the signed change in sea-level pressure over the preceding 3 hours. A negative value indicates falling pressure; a positive value indicates rising pressure. Unit: hectopascals.
- **`visibility`** (double or null, optional, [nmi_i] (nmi)): Station visibility as reported by the observing platform. Buoy visibility sensors have a range of 0 to 1.6 nautical miles and are generally only available on C-MAN stations. Unit: nautical miles.
- **`tide`** (double or null, optional, [ft_i] (ft)): Water level above or below Mean Lower Low Water (MLLW) at coastal and C-MAN stations. Unit: feet.
- **`region`** (string, optional): Stable routing axis used by MQTT and AMQP transport templates for noaa-ndbc.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "latitude": 0,
  "longitude": 0,
  "timestamp": "2024-01-01T00:00:00Z",
  "wind_direction": 0,
  "wind_speed": 0,
  "gust": 0,
  "wave_height": 0,
  "dominant_wave_period": 0,
  "average_wave_period": 0,
  "mean_wave_direction": 0,
  "pressure": 0,
  "air_temperature": 0,
  "water_temperature": 0,
  "dewpoint": 0,
  "pressure_tendency": 0,
  "visibility": 0,
  "tide": 0,
  "region": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Buoy Station

CloudEvents type: `Microsoft.OpenData.US.NOAA.NDBC.BuoyStation`

#### What it tells you

Reference record from the NDBC station table describing the owning agency, platform type, hull class, canonical station name, parsed location, and time-zone code for an observing platform.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is NDBC station identifier. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-ndbc`, key `{station_id}` |
| `MQTT/5.0` | topic `maritime/us/noaa/noaa-ndbc/{region}/{station_id}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/noaa-ndbc`, message subject `{station_id}`; application properties region `{region}` |

#### Payload

`Buoy Station` payloads are JSON object. Required fields: `station_id`, `name`.

- **`station_id`** (string, required): NDBC station identifier. Five-character alphanumeric code assigned by NDBC and reused across the station table, latest observations, and realtime2 products.
- **`owner`** (string or null, optional): Owning organization as listed in the NDBC station table, such as NDBC, NOS, or another partner agency.
- **`station_type`** (string or null, optional): Platform type from the station table, such as Weather Buoy or C-MAN Station.
- **`hull`** (string or null, optional): Hull or platform class reported in the station table, for example DISCUS or 3-meter.
- **`name`** (string, required): Human-readable station name from the NDBC station table.
- **`latitude`** (double or null, optional, deg): Station latitude in decimal degrees north parsed from the station table LOCATION field. Negative values indicate southern hemisphere.
- **`longitude`** (double or null, optional, deg): Station longitude in decimal degrees east parsed from the station table LOCATION field. Negative values indicate western hemisphere.
- **`timezone`** (string or null, optional): Single-letter time-zone code carried in the NDBC station table for display and forecast products.
- **`region`** (string, optional): Stable routing axis used by MQTT and AMQP transport templates for noaa-ndbc.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "owner": "string",
  "station_type": "string",
  "hull": "string",
  "name": "string",
  "latitude": 0,
  "longitude": 0,
  "timezone": "string",
  "region": "string"
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Buoy Solar Radiation Observation

CloudEvents type: `Microsoft.OpenData.US.NOAA.NDBC.BuoySolarRadiationObservation`

#### What it tells you

Hourly solar radiation observation from the NDBC .srad realtime2 product. The file reports LI-COR shortwave radiation, Eppley shortwave radiation, and downwelling longwave radiation when those sensors are installed on a station.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is NDBC station identifier. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-ndbc`, key `{station_id}` |
| `MQTT/5.0` | topic `maritime/us/noaa/noaa-ndbc/{region}/{station_id}/solar-radiation`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/noaa-ndbc`, message subject `{station_id}`; application properties region `{region}` |

#### Payload

`Buoy Solar Radiation Observation` payloads are JSON object. Required fields: `station_id`, `timestamp`.

- **`station_id`** (string, required): NDBC station identifier. The .srad realtime2 file is published per station and keyed by this identifier.
- **`timestamp`** (datetime, required): Observation timestamp in UTC, constructed from the YYYY MM DD hh mm columns in the NDBC .srad realtime2 file.
- **`shortwave_radiation_licor`** (double or null, optional, W/m2): Average shortwave radiation over the preceding hour from a LI-COR LI-200 pyranometer when the SRAD1 column is present. Unit: watts per square meter.
- **`shortwave_radiation_eppley`** (double or null, optional, W/m2): Average shortwave radiation over the preceding hour from an Eppley PSP Precision Spectral Pyranometer when the SWRAD column is present. Unit: watts per square meter.
- **`longwave_radiation`** (double or null, optional, W/m2): Average downwelling longwave radiation over the preceding hour from an Eppley PIR Precision Infrared Radiometer when the LWRAD column is present. Unit: watts per square meter.
- **`region`** (string, optional): Stable routing axis used by MQTT and AMQP transport templates for noaa-ndbc.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "timestamp": "2024-01-01T00:00:00Z",
  "shortwave_radiation_licor": 0,
  "shortwave_radiation_eppley": 0,
  "longwave_radiation": 0,
  "region": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Buoy Oceanographic Observation

CloudEvents type: `Microsoft.OpenData.US.NOAA.NDBC.BuoyOceanographicObservation`

#### What it tells you

Oceanographic observation from the NDBC .ocean realtime2 product. Each record reports the measurement depth together with direct ocean temperature, conductivity, salinity, dissolved oxygen, chlorophyll, turbidity, pH, and redox potential for one station and timestamp.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is NDBC station identifier. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-ndbc`, key `{station_id}` |
| `MQTT/5.0` | topic `maritime/us/noaa/noaa-ndbc/{region}/{station_id}/oceanographic`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/noaa-ndbc`, message subject `{station_id}`; application properties region `{region}` |

#### Payload

`Buoy Oceanographic Observation` payloads are JSON object. Required fields: `station_id`, `timestamp`, `depth`.

- **`station_id`** (string, required): NDBC station identifier. The .ocean realtime2 file is published per station and keyed by this identifier.
- **`timestamp`** (datetime, required): Observation timestamp in UTC, constructed from the YYYY MM DD hh mm columns in the NDBC .ocean realtime2 file.
- **`depth`** (double, required, m): Depth in meters at which the oceanographic measurements in this record were taken.
- **`ocean_temperature`** (double or null, optional, CEL (degC)): Direct ocean temperature measurement from the OTMP column. Unit: degrees Celsius.
- **`conductivity`** (double or null, optional, mS/cm): Electrical conductivity of seawater from the COND column. Unit: millisiemens per centimeter.
- **`salinity`** (double or null, optional, psu): Practical salinity computed from conductivity, temperature, and pressure using the Practical Salinity Scale of 1978. Unit: practical salinity units.
- **`oxygen_saturation`** (double or null, optional, %): Dissolved oxygen saturation percentage from the O2% column.
- **`oxygen_concentration`** (double or null, optional, ppm): Dissolved oxygen concentration from the O2PPM column. Unit: parts per million.
- **`chlorophyll_concentration`** (double or null, optional, ug/L): Chlorophyll concentration from the CLCON column. Unit: micrograms per liter.
- **`turbidity`** (double or null, optional, FTU): Turbidity from the TURB column. Unit: Formazin Turbidity Units.
- **`ph`** (double or null, optional): Acidity or alkalinity of the seawater sample from the PH column. This is dimensionless.
- **`redox_potential`** (double or null, optional, mV): Oxidation-reduction potential of seawater from the EH column. Unit: millivolts.
- **`region`** (string, optional): Stable routing axis used by MQTT and AMQP transport templates for noaa-ndbc.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "timestamp": "2024-01-01T00:00:00Z",
  "depth": 0,
  "ocean_temperature": 0,
  "conductivity": 0,
  "salinity": 0,
  "oxygen_saturation": 0,
  "oxygen_concentration": 0,
  "chlorophyll_concentration": 0,
  "turbidity": 0,
  "ph": 0,
  "redox_potential": 0,
  "region": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Buoy Dart Measurement

CloudEvents type: `Microsoft.OpenData.US.NOAA.NDBC.BuoyDartMeasurement`

#### What it tells you

Realtime DART tsunameter measurement from the NDBC .dart product. Each record contains a second-resolution timestamp, the documented NDBC measurement type code, and the measured water-column height for a DART station.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is NDBC station identifier for the DART tsunameter site publishing the .dart realtime2 file. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-ndbc`, key `{station_id}` |
| `MQTT/5.0` | topic `maritime/us/noaa/noaa-ndbc/{region}/{station_id}/dart-measurement`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/noaa-ndbc`, message subject `{station_id}`; application properties region `{region}` |

#### Payload

`Buoy Dart Measurement` payloads are JSON object. Required fields: `station_id`, `timestamp`, `measurement_type_code`, `water_column_height`.

- **`station_id`** (string, required): NDBC station identifier for the DART tsunameter site publishing the .dart realtime2 file.
- **`timestamp`** (datetime, required): Observation timestamp in UTC, constructed from the YYYY MM DD hh mm ss columns in the NDBC .dart realtime2 file.
- **`measurement_type_code`** (integer, required): Measurement type code from the T column in the DART file. NDBC documents 1 as a 15-minute measurement, 2 as a 1-minute measurement, and 3 as a 15-second measurement.
- **`water_column_height`** (double, required, m): Height of the measured water column from the HEIGHT column in the DART file. Unit: meters.
- **`region`** (string, optional): Stable routing axis used by MQTT and AMQP transport templates for noaa-ndbc.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "timestamp": "2024-01-01T00:00:00Z",
  "measurement_type_code": 0,
  "water_column_height": 0,
  "region": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Buoy Continuous Wind Observation

CloudEvents type: `Microsoft.OpenData.US.NOAA.NDBC.BuoyContinuousWindObservation`

#### What it tells you

Continuous-wind measurement from the NDBC .cwind realtime2 product. Each record reports the latest ten-minute wind average together with the strongest gust observed during the surrounding hourly window and the HHMM code describing when that gust occurred.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is NDBC station identifier for the station publishing the .cwind realtime2 file. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-ndbc`, key `{station_id}` |
| `MQTT/5.0` | topic `maritime/us/noaa/noaa-ndbc/{region}/{station_id}/continuous-wind`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/noaa-ndbc`, message subject `{station_id}`; application properties region `{region}` |

#### Payload

`Buoy Continuous Wind Observation` payloads are JSON object. Required fields: `station_id`, `timestamp`.

- **`station_id`** (string, required): NDBC station identifier for the station publishing the .cwind realtime2 file.
- **`timestamp`** (datetime, required): Observation timestamp in UTC, constructed from the YYYY MM DD hh mm columns in the NDBC .cwind realtime2 file.
- **`wind_direction`** (double or null, optional, deg (°)): Ten-minute average wind direction from the WDIR column, measured clockwise from true north. Unit: degrees true.
- **`wind_speed`** (double or null, optional, m/s): Ten-minute average wind speed from the WSPD column. Unit: meters per second.
- **`gust_direction`** (double or null, optional, deg (°)): Direction of the hourly peak gust from the GDR column, measured clockwise from true north. Unit: degrees true.
- **`gust`** (double or null, optional, m/s): Maximum 5-second peak gust from the GST column during the measurement hour. Unit: meters per second.
- **`gust_time_code`** (string or null, optional): HHMM UTC time code from the GTIME column indicating when the reported gust occurred within the surrounding hourly window. Around midnight the code can refer to the previous UTC day. Constraints: pattern `^[0-9]{4}$`.
- **`region`** (string, optional): Stable routing axis used by MQTT and AMQP transport templates for noaa-ndbc.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "timestamp": "2024-01-01T00:00:00Z",
  "wind_direction": 0,
  "wind_speed": 0,
  "gust_direction": 0,
  "gust": 0,
  "gust_time_code": "string",
  "region": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Buoy Supplemental Measurement

CloudEvents type: `Microsoft.OpenData.US.NOAA.NDBC.BuoySupplementalMeasurement`

#### What it tells you

Supplemental hourly extrema from the NDBC .supl realtime2 product. Each record reports the lowest one-minute pressure recorded during the hour and the highest one-minute wind speed with its direction and HHMM occurrence times.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is NDBC station identifier for the station publishing the .supl realtime2 file. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-ndbc`, key `{station_id}` |
| `MQTT/5.0` | topic `maritime/us/noaa/noaa-ndbc/{region}/{station_id}/supplemental`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/noaa-ndbc`, message subject `{station_id}`; application properties region `{region}` |

#### Payload

`Buoy Supplemental Measurement` payloads are JSON object. Required fields: `station_id`, `timestamp`.

- **`station_id`** (string, required): NDBC station identifier for the station publishing the .supl realtime2 file.
- **`timestamp`** (datetime, required): Observation timestamp in UTC, constructed from the YYYY MM DD hh mm columns in the NDBC .supl realtime2 file.
- **`lowest_pressure`** (double or null, optional, hPa): Lowest one-minute atmospheric pressure recorded during the hour from the PRES column. Unit: hectopascals.
- **`lowest_pressure_time_code`** (string or null, optional): HHMM UTC time code from the PTIME column indicating when the lowest one-minute pressure occurred during the surrounding hourly window. Around midnight the code can refer to the previous UTC day. Constraints: pattern `^[0-9]{4}$`.
- **`highest_wind_speed`** (double or null, optional, m/s): Highest one-minute wind speed recorded during the hour from the WSPD column. Unit: meters per second.
- **`highest_wind_direction`** (double or null, optional, deg (°)): Direction associated with the highest one-minute wind speed from the WDIR column, measured clockwise from true north. Unit: degrees true.
- **`highest_wind_time_code`** (string or null, optional): HHMM UTC time code from the WTIME column indicating when the highest one-minute wind speed occurred during the surrounding hourly window. Around midnight the code can refer to the previous UTC day. Constraints: pattern `^[0-9]{4}$`.
- **`region`** (string, optional): Stable routing axis used by MQTT and AMQP transport templates for noaa-ndbc.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "timestamp": "2024-01-01T00:00:00Z",
  "lowest_pressure": 0,
  "lowest_pressure_time_code": "string",
  "highest_wind_speed": 0,
  "highest_wind_direction": 0,
  "highest_wind_time_code": "string",
  "region": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Buoy Detailed Wave Summary

CloudEvents type: `Microsoft.OpenData.US.NOAA.NDBC.BuoyDetailedWaveSummary`

#### What it tells you

Detailed wave-summary record from the NDBC .spec realtime2 product. Each record summarizes significant wave height together with swell and wind-wave components, qualitative steepness, and mean wave direction for one station timestamp.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is NDBC station identifier for the station publishing the .spec realtime2 file. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-ndbc`, key `{station_id}` |
| `MQTT/5.0` | topic `maritime/us/noaa/noaa-ndbc/{region}/{station_id}/detailed-wave-summary`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/noaa-ndbc`, message subject `{station_id}`; application properties region `{region}` |

#### Payload

`Buoy Detailed Wave Summary` payloads are JSON object. Required fields: `station_id`, `timestamp`.

- **`station_id`** (string, required): NDBC station identifier for the station publishing the .spec realtime2 file.
- **`timestamp`** (datetime, required): Observation timestamp in UTC, constructed from the YYYY MM DD hh mm columns in the NDBC .spec realtime2 file.
- **`significant_wave_height`** (double or null, optional, m): Significant wave height from the WVHT column, representing the average height of the highest one-third of waves during the sampling period. Unit: meters.
- **`swell_height`** (double or null, optional, m): Swell-wave height from the SwH column. Unit: meters.
- **`swell_period`** (double or null, optional, s): Swell-wave period from the SwP column. Unit: seconds.
- **`wind_wave_height`** (double or null, optional, m): Wind-wave height from the WWH column. Unit: meters.
- **`wind_wave_period`** (double or null, optional, s): Wind-wave period from the WWP column. Unit: seconds.
- **`swell_direction`** (string or null, optional): Swell direction from the SwD column. Live NDBC .spec files currently publish this field as a compass code such as E, SE, or ESE rather than a numeric degree value.
- **`wind_wave_direction`** (string or null, optional): Wind-wave direction from the WWD column. Live NDBC .spec files currently publish this field as a compass code such as E, SE, or ESE rather than a numeric degree value.
- **`steepness`** (string or null, optional): Wave steepness category from the STEEPNESS column, for example SWELL, AVERAGE, or VERY_STEEP.
- **`average_wave_period`** (double or null, optional, s): Average wave period from the APD column. Unit: seconds.
- **`mean_wave_direction`** (double or null, optional, deg (°)): Mean wave direction from the MWD column, measured clockwise from true north. Unit: degrees true.
- **`region`** (string, optional): Stable routing axis used by MQTT and AMQP transport templates for noaa-ndbc.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "timestamp": "2024-01-01T00:00:00Z",
  "significant_wave_height": 0,
  "swell_height": 0,
  "swell_period": 0,
  "wind_wave_height": 0,
  "wind_wave_period": 0,
  "swell_direction": "string",
  "wind_wave_direction": "string",
  "steepness": "string",
  "average_wave_period": 0,
  "mean_wave_direction": 0,
  "region": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Buoy Hourly Rain Measurement

CloudEvents type: `Microsoft.OpenData.US.NOAA.NDBC.BuoyHourlyRainMeasurement`

#### What it tells you

Hourly precipitation total from the NDBC .rain realtime2 product. Each record reports the one-hour rain accumulation for a station timestamp.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is NDBC station identifier for the station publishing the .rain realtime2 file. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-ndbc`, key `{station_id}` |
| `MQTT/5.0` | topic `maritime/us/noaa/noaa-ndbc/{region}/{station_id}/hourly-rain`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/noaa-ndbc`, message subject `{station_id}`; application properties region `{region}` |

#### Payload

`Buoy Hourly Rain Measurement` payloads are JSON object. Required fields: `station_id`, `timestamp`.

- **`station_id`** (string, required): NDBC station identifier for the station publishing the .rain realtime2 file.
- **`timestamp`** (datetime, required): Observation timestamp in UTC, constructed from the YYYY MM DD hh mm columns in the NDBC .rain realtime2 file.
- **`accumulation`** (double or null, optional, mm): Hourly rain accumulation from the ACCUM column. This is the total precipitation accumulated during the 60-minute period ending at the reported timestamp. Unit: millimeters.
- **`region`** (string, optional): Stable routing axis used by MQTT and AMQP transport templates for noaa-ndbc.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "timestamp": "2024-01-01T00:00:00Z",
  "accumulation": 0,
  "region": "string"
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

- xRegistry manifest: [`xreg/noaa_ndbc.xreg.json`](xreg/noaa_ndbc.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
