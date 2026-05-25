# NOAA Data Poller Usage Guide Events

**NOAA Data Poller** is a tool designed to interact with the NOAA (National Oceanic and Atmospheric Administration) API to fetch real-time environmental data from various NOAA stations. The tool can retrieve data such as water levels, air temperature, wind, and predictions, and send this data to a Kafka topic using SASL PLAIN authentication, making it suitable for integration with systems like Microsoft Event Hubs or Microsoft Fabric Event Streams.

## At a glance

- **Event types:** 13 documented event types.
- **Transports:** KAFKA
- **Reference vs telemetry:** 1 reference/catalog event type and 12 telemetry event types.
- **Identity:** `{station_id}` identifies the resource each event is about.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `noaa-tides-currents`. The record key is `{station_id}`. In plain language, `{station_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['noaa-tides-currents'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.

## Event catalog

### Water Level

CloudEvents type: `Microsoft.OpenData.US.NOAA.WaterLevel`

#### What it tells you

This event carries water level data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is {"description": "7 character station ID, or a currents station ID."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-tides-currents`, key `{station_id}` |

#### Payload

`Water Level` payloads are JSON object. Required fields: `station_id`, `timestamp`, `value`, `stddev`, `outside_sigma_band`, `flat_tolerance_limit`, `rate_of_change_limit`, `max_min_expected_height`, `quality`.

- **`station_id`** (string, required): {"description": "7 character station ID, or a currents station ID."}
- **`timestamp`** (string, required): {"description": "Timestamp of the water level measurement"}
- **`value`** (double, required): {"description": "Value of the water level"}
- **`stddev`** (double, required): {"description": "Standard deviation of 1-second samples used to compute the water level height"}
- **`outside_sigma_band`** (boolean, required): {"description": "Flag indicating if the water level is outside a 3-sigma band. Possible values: 'false' (not outside), 'true' (outside)."}
- **`flat_tolerance_limit`** (boolean, required): {"description": "Flag indicating if the flat tolerance limit is exceeded. Possible values: 'false' (not exceeded), 'true' (exceeded)."}
- **`rate_of_change_limit`** (boolean, required): {"description": "Flag indicating if the rate of change tolerance limit is exceeded. Possible values: 'false' (not exceeded), 'true' (exceeded)."}
- **`max_min_expected_height`** (boolean, required): {"description": "Flag indicating if the max/min expected water level height is exceeded. Possible values: 'false' (not exceeded), 'true' (exceeded)."}
- **`quality`** (enum, required): Quality Assurance/Quality Control level
##### `quality` values

- `Preliminary`
- `Verified`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "timestamp": "string",
  "value": 0,
  "stddev": 0,
  "outside_sigma_band": false,
  "flat_tolerance_limit": false,
  "rate_of_change_limit": false,
  "max_min_expected_height": false,
  "quality": "Preliminary"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Predictions

CloudEvents type: `Microsoft.OpenData.US.NOAA.Predictions`

#### What it tells you

This event carries predictions data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is {"description": "7 character station ID, or a currents station ID."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-tides-currents`, key `{station_id}` |

#### Payload

`Predictions` payloads are JSON object. Required fields: `station_id`, `timestamp`, `value`.

- **`station_id`** (string, required): {"description": "7 character station ID, or a currents station ID."}
- **`timestamp`** (string, required): {"description": "Timestamp of the prediction"}
- **`value`** (double, required): {"description": "Value of the prediction"}
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "timestamp": "string",
  "value": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Air Pressure

CloudEvents type: `Microsoft.OpenData.US.NOAA.AirPressure`

#### What it tells you

This event carries air pressure data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is {"description": "7 character station ID, or a currents station ID."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-tides-currents`, key `{station_id}` |

#### Payload

`Air Pressure` payloads are JSON object. Required fields: `station_id`, `timestamp`, `value`, `max_pressure_exceeded`, `min_pressure_exceeded`, `rate_of_change_exceeded`.

- **`station_id`** (string, required): {"description": "7 character station ID, or a currents station ID."}
- **`timestamp`** (string, required): {"description": "Timestamp of the air pressure measurement"}
- **`value`** (double, required): {"description": "Value of the air pressure"}
- **`max_pressure_exceeded`** (boolean, required): Flag indicating if the maximum expected air pressure was exceeded
- **`min_pressure_exceeded`** (boolean, required): Flag indicating if the minimum expected air pressure was exceeded
- **`rate_of_change_exceeded`** (boolean, required): Flag indicating if the rate of change tolerance limit was exceeded
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "timestamp": "string",
  "value": 0,
  "max_pressure_exceeded": false,
  "min_pressure_exceeded": false,
  "rate_of_change_exceeded": false
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Air Temperature

CloudEvents type: `Microsoft.OpenData.US.NOAA.AirTemperature`

#### What it tells you

This event carries air temperature data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is {"description": "7 character station ID, or a currents station ID."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-tides-currents`, key `{station_id}` |

#### Payload

`Air Temperature` payloads are JSON object. Required fields: `station_id`, `timestamp`, `value`, `max_temp_exceeded`, `min_temp_exceeded`, `rate_of_change_exceeded`.

- **`station_id`** (string, required): {"description": "7 character station ID, or a currents station ID."}
- **`timestamp`** (string, required): {"description": "Timestamp of the air temperature measurement"}
- **`value`** (double, required): {"description": "Value of the air temperature"}
- **`max_temp_exceeded`** (boolean, required): Flag indicating if the maximum expected air temperature was exceeded
- **`min_temp_exceeded`** (boolean, required): Flag indicating if the minimum expected air temperature was exceeded
- **`rate_of_change_exceeded`** (boolean, required): Flag indicating if the rate of change tolerance limit was exceeded
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "timestamp": "string",
  "value": 0,
  "max_temp_exceeded": false,
  "min_temp_exceeded": false,
  "rate_of_change_exceeded": false
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Water Temperature

CloudEvents type: `Microsoft.OpenData.US.NOAA.WaterTemperature`

#### What it tells you

This event carries water temperature data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is {"description": "7 character station ID, or a currents station ID."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-tides-currents`, key `{station_id}` |

#### Payload

`Water Temperature` payloads are JSON object. Required fields: `station_id`, `timestamp`, `value`, `max_temp_exceeded`, `min_temp_exceeded`, `rate_of_change_exceeded`.

- **`station_id`** (string, required): {"description": "7 character station ID, or a currents station ID."}
- **`timestamp`** (string, required): {"description": "Timestamp of the water temperature measurement"}
- **`value`** (double, required): {"description": "Value of the water temperature"}
- **`max_temp_exceeded`** (boolean, required): Flag indicating if the maximum expected water temperature was exceeded
- **`min_temp_exceeded`** (boolean, required): Flag indicating if the minimum expected water temperature was exceeded
- **`rate_of_change_exceeded`** (boolean, required): Flag indicating if the rate of change tolerance limit was exceeded
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "timestamp": "string",
  "value": 0,
  "max_temp_exceeded": false,
  "min_temp_exceeded": false,
  "rate_of_change_exceeded": false
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Wind

CloudEvents type: `Microsoft.OpenData.US.NOAA.Wind`

#### What it tells you

This event carries wind data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is {"description": "7 character station ID, or a currents station ID."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-tides-currents`, key `{station_id}` |

#### Payload

`Wind` payloads are JSON object. Required fields: `station_id`, `timestamp`, `speed`, `direction_degrees`, `direction_text`, `gusts`, `max_wind_speed_exceeded`, `rate_of_change_exceeded`.

- **`station_id`** (string, required): {"description": "7 character station ID, or a currents station ID."}
- **`timestamp`** (string, required): {"description": "Timestamp of the wind measurement"}
- **`speed`** (double, required): {"description": "Wind speed"}
- **`direction_degrees`** (string, required): {"description": "Wind direction"}
- **`direction_text`** (string, required): {"description": "Direction - wind direction in text."}
- **`gusts`** (double, required): {"description": "Wind gust speed"}
- **`max_wind_speed_exceeded`** (boolean, required): Flag indicating if the maximum wind speed was exceeded
- **`rate_of_change_exceeded`** (boolean, required): Flag indicating if the rate of change tolerance limit was exceeded
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "timestamp": "string",
  "speed": 0,
  "direction_degrees": "string",
  "direction_text": "string",
  "gusts": 0,
  "max_wind_speed_exceeded": false,
  "rate_of_change_exceeded": false
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Humidity

CloudEvents type: `Microsoft.OpenData.US.NOAA.Humidity`

#### What it tells you

This event carries humidity data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is {"description": "7 character station ID, or a currents station ID."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-tides-currents`, key `{station_id}` |

#### Payload

`Humidity` payloads are JSON object. Required fields: `station_id`, `timestamp`, `value`, `max_humidity_exceeded`, `min_humidity_exceeded`, `rate_of_change_exceeded`.

- **`station_id`** (string, required): {"description": "7 character station ID, or a currents station ID."}
- **`timestamp`** (string, required): {"description": "Timestamp of the humidity measurement"}
- **`value`** (double, required): {"description": "Value of the humidity"}
- **`max_humidity_exceeded`** (boolean, required): Flag indicating if the maximum expected humidity was exceeded
- **`min_humidity_exceeded`** (boolean, required): Flag indicating if the minimum expected humidity was exceeded
- **`rate_of_change_exceeded`** (boolean, required): Flag indicating if the rate of change tolerance limit was exceeded
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "timestamp": "string",
  "value": 0,
  "max_humidity_exceeded": false,
  "min_humidity_exceeded": false,
  "rate_of_change_exceeded": false
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Conductivity

CloudEvents type: `Microsoft.OpenData.US.NOAA.Conductivity`

#### What it tells you

This event carries conductivity data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is {"description": "7 character station ID, or a currents station ID."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-tides-currents`, key `{station_id}` |

#### Payload

`Conductivity` payloads are JSON object. Required fields: `station_id`, `timestamp`, `value`, `max_conductivity_exceeded`, `min_conductivity_exceeded`, `rate_of_change_exceeded`.

- **`station_id`** (string, required): {"description": "7 character station ID, or a currents station ID."}
- **`timestamp`** (string, required): {"description": "Timestamp of the conductivity measurement"}
- **`value`** (double, required): {"description": "Value of the conductivity"}
- **`max_conductivity_exceeded`** (boolean, required): Flag indicating if the maximum expected conductivity was exceeded
- **`min_conductivity_exceeded`** (boolean, required): Flag indicating if the minimum expected conductivity was exceeded
- **`rate_of_change_exceeded`** (boolean, required): Flag indicating if the rate of change tolerance limit was exceeded
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "timestamp": "string",
  "value": 0,
  "max_conductivity_exceeded": false,
  "min_conductivity_exceeded": false,
  "rate_of_change_exceeded": false
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Salinity

CloudEvents type: `Microsoft.OpenData.US.NOAA.Salinity`

#### What it tells you

This event carries salinity data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is {"description": "7 character station ID, or a currents station ID."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-tides-currents`, key `{station_id}` |

#### Payload

`Salinity` payloads are JSON object. Required fields: `station_id`, `timestamp`, `salinity`, `grams_per_kg`.

- **`station_id`** (string, required): {"description": "7 character station ID, or a currents station ID."}
- **`timestamp`** (string, required): {"description": "Timestamp of the salinity measurement"}
- **`salinity`** (double, required): {"description": "Value of the salinity"}
- **`grams_per_kg`** (double, required): {"description": "Grams of salt per kilogram of water"}
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "timestamp": "string",
  "salinity": 0,
  "grams_per_kg": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Station

CloudEvents type: `Microsoft.OpenData.US.NOAA.Station`

#### What it tells you

This event carries station data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is {"description": "Unique identifier for the station."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-tides-currents`, key `{station_id}` |

#### Payload

`Station` payloads are JSON object. Required fields: `tidal`, `greatlakes`, `shefcode`, `details`, `sensors`, `floodlevels`, `datums`, `supersededdatums`, `harmonicConstituents`, `benchmarks`, `tidePredOffsets`, `ofsMapOffsets`, `state`, `timezone`, `timezonecorr`, `observedst`, `stormsurge`, `nearby`, `forecast`, `outlook`, `HTFhistorical`, `nonNavigational`, `station_id`, `name`, `lat`, `lng`, `affiliations`, `portscode`, `products`, `disclaimers`, `notices`, `self`, `expand`, `tideType`.

- **`tidal`** (boolean, required): {"description": "Indicates whether the station measures tidal data."}
- **`greatlakes`** (boolean, required): {"description": "Indicates whether the station is located in the Great Lakes region."}
- **`shefcode`** (string, required): {"description": "Standard Hydrologic Exchange Format code for the station."}
- **`details`** (object, required): No description provided. See [details](#payload-microsoft-opendata-us-noaa-station-details).
- **`sensors`** (object, required): No description provided. See [sensors](#payload-microsoft-opendata-us-noaa-station-sensors).
- **`floodlevels`** (object, required): No description provided. See [floodlevels](#payload-microsoft-opendata-us-noaa-station-floodlevels).
- **`datums`** (object, required): No description provided. See [datums](#payload-microsoft-opendata-us-noaa-station-datums).
- **`supersededdatums`** (object, required): No description provided. See [supersededdatums](#payload-microsoft-opendata-us-noaa-station-supersededdatums).
- **`harmonicConstituents`** (object, required): No description provided. See [harmonicConstituents](#payload-microsoft-opendata-us-noaa-station-harmonicconstituents).
- **`benchmarks`** (object, required): No description provided. See [benchmarks](#payload-microsoft-opendata-us-noaa-station-benchmarks).
- **`tidePredOffsets`** (object, required): No description provided. See [tidePredOffsets](#payload-microsoft-opendata-us-noaa-station-tidepredoffsets).
- **`ofsMapOffsets`** (object, required): No description provided. See [ofsMapOffsets](#payload-microsoft-opendata-us-noaa-station-ofsmapoffsets).
- **`state`** (string, required): {"description": "State where the station is located."}
- **`timezone`** (string, required): {"description": "Timezone of the station."}
- **`timezonecorr`** (int32, required): {"description": "Timezone correction in minutes for the station."}
- **`observedst`** (boolean, required): {"description": "Indicates whether the station observes Daylight Saving Time."}
- **`stormsurge`** (boolean, required): {"description": "Indicates whether the station measures storm surge data."}
- **`nearby`** (object, required): No description provided. See [nearby](#payload-microsoft-opendata-us-noaa-station-nearby).
- **`forecast`** (boolean, required): {"description": "Indicates whether the station provides forecast data."}
- **`outlook`** (boolean, required): {"description": "Indicates whether the station provides outlook data."}
- **`HTFhistorical`** (boolean, required): {"description": "Indicates whether the station has historical High Tide Flooding data."}
- **`nonNavigational`** (boolean, required): {"description": "Indicates whether the station is non-navigational."}
- **`station_id`** (string, required): {"description": "Unique identifier for the station."}
- **`name`** (string, required): {"description": "Name of the station."}
- **`lat`** (double, required): {"description": "Latitude of the station."}
- **`lng`** (double, required): {"description": "Longitude of the station."}
- **`affiliations`** (string, required): {"description": "Affiliations of the station."}
- **`portscode`** (string, required): {"description": "PORTS code for the station."}
- **`products`** (object, required): No description provided. See [products](#payload-microsoft-opendata-us-noaa-station-products).
- **`disclaimers`** (object, required): No description provided. See [disclaimers](#payload-microsoft-opendata-us-noaa-station-disclaimers).
- **`notices`** (object, required): No description provided. See [notices](#payload-microsoft-opendata-us-noaa-station-notices).
- **`self`** (string, required): {"description": "URL to the station's data."}
- **`expand`** (string, required): {"description": "URL to expanded information about the station."}
- **`tideType`** (string, required): {"description": "Type of tide measured by the station."}
##### details
<a id="payload-microsoft-opendata-us-noaa-station-details"></a>

Nested record.

- **`self`** (string, required): No description provided.
##### sensors
<a id="payload-microsoft-opendata-us-noaa-station-sensors"></a>

Nested record.

- **`self`** (string, required): No description provided.
##### floodlevels
<a id="payload-microsoft-opendata-us-noaa-station-floodlevels"></a>

Nested record.

- **`self`** (string, required): No description provided.
##### datums
<a id="payload-microsoft-opendata-us-noaa-station-datums"></a>

Nested record.

- **`self`** (string, required): No description provided.
##### supersededdatums
<a id="payload-microsoft-opendata-us-noaa-station-supersededdatums"></a>

Nested record.

- **`self`** (string, required): No description provided.
##### harmonicConstituents
<a id="payload-microsoft-opendata-us-noaa-station-harmonicconstituents"></a>

Nested record.

- **`self`** (string, required): No description provided.
##### benchmarks
<a id="payload-microsoft-opendata-us-noaa-station-benchmarks"></a>

Nested record.

- **`self`** (string, required): No description provided.
##### tidePredOffsets
<a id="payload-microsoft-opendata-us-noaa-station-tidepredoffsets"></a>

Nested record.

- **`self`** (string, required): No description provided.
##### ofsMapOffsets
<a id="payload-microsoft-opendata-us-noaa-station-ofsmapoffsets"></a>

Nested record.

- **`self`** (string, required): No description provided.
##### nearby
<a id="payload-microsoft-opendata-us-noaa-station-nearby"></a>

Nested record.

- **`self`** (string, required): No description provided.
##### products
<a id="payload-microsoft-opendata-us-noaa-station-products"></a>

Nested record.

- **`self`** (string, required): No description provided.
##### disclaimers
<a id="payload-microsoft-opendata-us-noaa-station-disclaimers"></a>

Nested record.

- **`self`** (string, required): No description provided.
##### notices
<a id="payload-microsoft-opendata-us-noaa-station-notices"></a>

Nested record.

- **`self`** (string, required): No description provided.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "tidal": false,
  "greatlakes": false,
  "shefcode": "string",
  "details": {
    "self": "string"
  },
  "sensors": {
    "self": "string"
  },
  "floodlevels": {
    "self": "string"
  },
  "datums": {
    "self": "string"
  },
  "supersededdatums": {
    "self": "string"
  },
  "harmonicConstituents": {
    "self": "string"
  },
  "benchmarks": {
    "self": "string"
  },
  "tidePredOffsets": {
    "self": "string"
  },
  "ofsMapOffsets": {
    "self": "string"
  },
  "state": "string",
  "timezone": "string",
  "timezonecorr": 0,
  "observedst": false,
  "stormsurge": false,
  "nearby": {
    "self": "string"
  },
  "forecast": false,
  "outlook": false,
  "HTFhistorical": false,
  "nonNavigational": false,
  "station_id": "string",
  "name": "string",
  "lat": 0,
  "lng": 0,
  "affiliations": "string",
  "portscode": "string",
  "products": {
    "self": "string"
  },
  "disclaimers": {
    "self": "string"
  },
  "notices": {
    "self": "string"
  },
  "self": "string",
  "expand": "string",
  "tideType": "string"
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity.

### Visibility

CloudEvents type: `Microsoft.OpenData.US.NOAA.Visibility`

#### What it tells you

This event carries visibility data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-tides-currents`, key `{station_id}` |

#### Payload

`Visibility` payloads are JSON object. Required fields: `timestamp`, `value`, `max_visibility_exceeded`, `min_visibility_exceeded`, `rate_of_change_exceeded`, `station_id`.

- **`timestamp`** (string, required): {"description": "Timestamp of the visibility measurement"}
- **`value`** (double, required): {"description": "Value of the visibility"}
- **`max_visibility_exceeded`** (boolean, required): A flag that indicates whether the maximum expected visibility was exceeded
- **`min_visibility_exceeded`** (boolean, required): A flag that indicates whether the minimum expected visibility was exceeded
- **`rate_of_change_exceeded`** (boolean, required): A flag that indicates whether the rate of change tolerance limit was exceeded
- **`station_id`** (string, required): No description provided.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "timestamp": "string",
  "value": 0,
  "max_visibility_exceeded": false,
  "min_visibility_exceeded": false,
  "rate_of_change_exceeded": false,
  "station_id": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Currents

CloudEvents type: `Microsoft.OpenData.US.NOAA.Currents`

#### What it tells you

This event carries currents data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is {"description": "7 character station ID, or a currents station ID."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-tides-currents`, key `{station_id}` |

#### Payload

`Currents` payloads are JSON object. Required fields: `station_id`, `timestamp`, `speed`, `direction_degrees`, `bin`.

- **`station_id`** (string, required): {"description": "7 character station ID, or a currents station ID."}
- **`timestamp`** (string, required): {"description": "Timestamp of the currents measurement"}
- **`speed`** (double, required): {"description": "Current speed"}
- **`direction_degrees`** (double, required): {"description": "Current direction in degrees"}
- **`bin`** (string, required): {"description": "Bin number"}
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "timestamp": "string",
  "speed": 0,
  "direction_degrees": 0,
  "bin": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Current Predictions

CloudEvents type: `Microsoft.OpenData.US.NOAA.CurrentPredictions`

#### What it tells you

This event carries current predictions data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is {"description": "7 character station ID, or a currents station ID."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-tides-currents`, key `{station_id}` |

#### Payload

`Current Predictions` payloads are JSON object. Required fields: `station_id`, `timestamp`, `velocity_major`, `mean_flood_dir`, `mean_ebb_dir`, `depth`, `bin`.

- **`station_id`** (string, required): {"description": "7 character station ID, or a currents station ID."}
- **`timestamp`** (string, required): {"description": "Timestamp of the current prediction"}
- **`velocity_major`** (double, required): {"description": "Major axis velocity"}
- **`mean_flood_dir`** (double, required): {"description": "Mean flood direction in degrees"}
- **`mean_ebb_dir`** (double, required): {"description": "Mean ebb direction in degrees"}
- **`depth`** (double, required): {"description": "Depth of measurement"}
- **`bin`** (string, required): {"description": "Bin number"}
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "timestamp": "string",
  "velocity_major": 0,
  "mean_flood_dir": 0,
  "mean_ebb_dir": 0,
  "depth": 0,
  "bin": "string"
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

No source-specific polling cadence, rate limit, or stream characteristic is documented in the checked-in README or CONTAINER guide.

## References

- xRegistry manifest: [`xreg/noaa.xreg.json`](xreg/noaa.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
