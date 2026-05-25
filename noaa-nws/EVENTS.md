# NOAA NWS Weather Alerts Poller Events

**NOAA NWS Weather Alerts Poller** polls the National Weather Service (NWS) Weather Alerts API for active weather alerts across the United States and sends them to a Kafka topic as CloudEvents. The tool tracks previously seen alert IDs to avoid sending duplicates.

## At a glance

- **Event types:** 4 documented event types.
- **Transports:** KAFKA
- **Reference vs telemetry:** 0 reference/catalog event types and 4 telemetry event types.
- **Identity:** `{alert_id}`, `{zone_id}`, `{station_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `noaa-nws`. The record key is `{alert_id}`, `{zone_id}`, `{station_id}`. Each key template is explained in the event catalog below. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['noaa-nws'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.

## Event catalog

### Weather Alert

CloudEvents type: `Microsoft.OpenData.US.NOAA.NWS.WeatherAlert`

#### What it tells you

Active weather alert from the NWS Common Alerting Protocol (CAP) feed. Alerts cover severe weather warnings, watches, advisories, and statements issued by NWS Weather Forecast Offices.

#### Identity

Each event identifies the real-world resource with `{alert_id}`. `{alert_id}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-nws`, key `{alert_id}` |

#### Payload

`Weather Alert` payloads are JSON object. Required fields: `alert_id`, `area_desc`, `sent`, `effective`, `expires`, `status`, `message_type`, `severity`, `certainty`, `urgency`, `event`.

- **`alert_id`** (string, required): No description provided.
- **`area_desc`** (string, required): No description provided.
- **`sent`** (datetime, required): No description provided.
- **`effective`** (datetime, required): No description provided.
- **`expires`** (datetime, required): No description provided.
- **`status`** (enum, required): No description provided.
- **`message_type`** (enum, required): No description provided.
- **`category`** (enum, optional): No description provided.
- **`severity`** (enum, required): No description provided.
- **`certainty`** (enum, required): No description provided.
- **`urgency`** (enum, required): No description provided.
- **`event`** (string, required): No description provided.
- **`sender_name`** (string, optional): No description provided.
- **`headline`** (string or null, optional): No description provided.
- **`description`** (string, optional): No description provided.
##### `status` values

- `Actual`
- `Exercise`
- `System`
- `Test`
- `Draft`
##### `message_type` values

- `Alert`
- `Update`
- `Cancel`
##### `category` values

- `Met`
- `Geo`
- `Safety`
- `Security`
- `Rescue`
- `Fire`
- `Health`
- `Env`
- `Transport`
- `Infra`
- `CBRNE`
- `Other`
##### `severity` values

- `Extreme`
- `Severe`
- `Moderate`
- `Minor`
- `Unknown`
##### `certainty` values

- `Observed`
- `Likely`
- `Possible`
- `Unlikely`
- `Unknown`
##### `urgency` values

- `Immediate`
- `Expected`
- `Future`
- `Past`
- `Unknown`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "alert_id": "string",
  "area_desc": "string",
  "sent": "2024-01-01T00:00:00Z",
  "effective": "2024-01-01T00:00:00Z",
  "expires": "2024-01-01T00:00:00Z",
  "status": "Actual",
  "message_type": "Alert",
  "category": "Met",
  "severity": "Extreme",
  "certainty": "Observed",
  "urgency": "Immediate",
  "event": "string",
  "sender_name": "string",
  "headline": "string",
  "description": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Zone

CloudEvents type: `Microsoft.OpenData.US.NOAA.NWS.Zone`

#### What it tells you

NWS forecast zone reference data. Zones partition the US into geographic areas for which forecasts and warnings are issued.

#### Identity

Each event identifies the real-world resource with `{zone_id}`. `{zone_id}` is NWS zone identifier, e.g. 'NYZ072' for New York City. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-nws`, key `{zone_id}` |

#### Payload

`Zone` payloads are JSON object. Required fields: `zone_id`, `name`, `state`.

- **`zone_id`** (string, required): NWS zone identifier, e.g. 'NYZ072' for New York City.
- **`name`** (string, required): Human-readable zone name.
- **`type`** (string, optional): Zone type: 'forecast', 'county', 'fire', 'coastal', or 'offshore'.
- **`state`** (string, required): Two-letter US state or territory abbreviation.
- **`forecast_office`** (string, optional): NWS Weather Forecast Office (WFO) responsible for this zone, e.g. 'OKX'.
- **`timezone`** (string, optional): IANA timezone name for the zone, e.g. 'America/New_York'.
- **`radar_station`** (string or null, optional): Nearest NEXRAD radar station identifier, or null if none assigned.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "zone_id": "string",
  "name": "string",
  "type": "string",
  "state": "string",
  "forecast_office": "string",
  "timezone": "string",
  "radar_station": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Observation Station

CloudEvents type: `Microsoft.OpenData.US.NOAA.NWS.ObservationStation`

#### What it tells you

NWS surface weather observation station reference data from the api.weather.gov /stations endpoint. Each station represents a fixed automated or manual observing site in the US.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is station identifier, typically a 4-character ICAO code such as 'KJFK' or a cooperative observer ID. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-nws`, key `{station_id}` |

#### Payload

`Observation Station` payloads are JSON object. Required fields: `station_id`, `name`.

- **`station_id`** (string, required): Station identifier, typically a 4-character ICAO code such as 'KJFK' or a cooperative observer ID.
- **`name`** (string, required): Human-readable station name, e.g. 'New York, Kennedy International Airport'.
- **`elevation_m`** (double or null, optional, m): Station elevation above mean sea level.
- **`time_zone`** (string or null, optional): IANA timezone of the station, e.g. 'America/New_York'.
- **`forecast_zone`** (string or null, optional): NWS forecast zone identifier associated with this station.
- **`county`** (string or null, optional): NWS county zone identifier for the station's location.
- **`fire_weather_zone`** (string or null, optional): NWS fire weather zone identifier for the station's location.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "name": "string",
  "elevation_m": 0,
  "time_zone": "string",
  "forecast_zone": "string",
  "county": "string",
  "fire_weather_zone": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Weather Observation

CloudEvents type: `Microsoft.OpenData.US.NOAA.NWS.WeatherObservation`

#### What it tells you

Latest weather observation from a NWS surface station. Observations are fetched from the api.weather.gov /stations/{stationId}/observations/latest endpoint. Measurement values are extracted from NWS quantity objects (unitCode + value + qualityControl).

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is ICAO or cooperative observer station identifier. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `noaa-nws`, key `{station_id}` |

#### Payload

`Weather Observation` payloads are JSON object. Required fields: `station_id`, `timestamp`.

- **`station_id`** (string, required): ICAO or cooperative observer station identifier.
- **`timestamp`** (datetime, required): UTC timestamp of the observation.
- **`text_description`** (string or null, optional): Brief text summary of current conditions, e.g. 'Clear', 'Mostly Cloudy', 'Rain'.
- **`temperature`** (double or null, optional, Cel (°C)): Air temperature at the time of observation.
- **`dewpoint`** (double or null, optional, Cel (°C)): Dew point temperature.
- **`wind_direction`** (double or null, optional, degree (°)): Wind direction in degrees from which the wind is blowing.
- **`wind_speed`** (double or null, optional, km/h): Sustained wind speed.
- **`wind_gust`** (double or null, optional, km/h): Peak wind gust speed, null if no gusts observed.
- **`barometric_pressure`** (double or null, optional, Pa): Station barometric pressure (not reduced to sea level).
- **`sea_level_pressure`** (double or null, optional, Pa): Atmospheric pressure reduced to mean sea level.
- **`visibility`** (double or null, optional, m): Horizontal visibility.
- **`relative_humidity`** (double or null, optional, percent (%)): Relative humidity percentage.
- **`wind_chill`** (double or null, optional, Cel (°C)): Calculated wind chill temperature, null when conditions do not warrant it.
- **`heat_index`** (double or null, optional, Cel (°C)): Calculated heat index temperature, null when conditions do not warrant it.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "timestamp": "2024-01-01T00:00:00Z",
  "text_description": "string",
  "temperature": 0,
  "dewpoint": 0,
  "wind_direction": 0,
  "wind_speed": 0,
  "wind_gust": 0,
  "barometric_pressure": 0,
  "sea_level_pressure": 0,
  "visibility": 0,
  "relative_humidity": 0,
  "wind_chill": 0,
  "heat_index": 0
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

- xRegistry manifest: [`xreg/noaa_nws.xreg.json`](xreg/noaa_nws.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
