# BOM Australia feeder Events

MQTT 5 companion message group for AU.Gov.BOM.Weather.

## At a glance

- **Event types:** 3 documented event types (9 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 1 reference/catalog event type and 2 telemetry event types.
- **Identity:** `{station_wmo}`, `{warning_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `bom-australia`. The record key is `{station_wmo}`, `{warning_id}`. Each key template is explained in the event catalog below. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['bom-australia'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `weather/au/bom/bom-australia/+/+/info`, `weather/au/bom/bom-australia/+/+/observation`, `alerts/au/bom/bom-australia/+/+/+/warning`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('weather/au/bom/bom-australia/+/+/info', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `bom-australia`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/bom-australia')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Station

CloudEvents type: `AU.Gov.BOM.Weather.Station`

#### What it tells you

Reference metadata for a BOM weather observation station identified by its WMO station number. Stations report half-hourly surface observations covering temperature, wind, pressure, rainfall, humidity, cloud, and visibility.

#### Identity

Each event identifies the real-world resource with `{station_wmo}`. `{station_wmo}` is WMO station number assigned by the World Meteorological Organization, used as the stable identity for this station across all BOM products. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `bom-australia`, key `{station_wmo}` |
| `MQTT/5.0` | topic `weather/au/bom/bom-australia/{state}/{station_wmo}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/bom-australia`, message subject `{station_wmo}`; application properties state `{state}` |

#### Payload

`Station` payloads are JSON object. Required fields: `station_wmo`, `name`, `latitude`, `longitude`.

- **`station_wmo`** (string, required): WMO station number assigned by the World Meteorological Organization, used as the stable identity for this station across all BOM products.
- **`name`** (string, required): Human-readable station name as assigned by the Bureau of Meteorology, e.g. 'Sydney Airport' or 'Melbourne Airport'.
- **`product_id`** (string, optional): BOM product code identifying the observation product this station belongs to, e.g. 'IDN60901' for NSW capital city observations.
- **`state`** (string, optional): Australian state or territory the station is located in, as reported by BOM, e.g. 'New South Wales', 'Victoria'.
- **`time_zone`** (string, optional): Abbreviation of the local time zone for the station, e.g. 'EST' for Eastern Standard Time, 'CST' for Central Standard Time.
- **`latitude`** (double, required, degree (°)): Geographic latitude of the station in decimal degrees (negative for Southern Hemisphere).
- **`longitude`** (double, required, degree (°)): Geographic longitude of the station in decimal degrees.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_wmo": "string",
  "name": "string",
  "product_id": "string",
  "state": "string",
  "time_zone": "string",
  "latitude": 0,
  "longitude": 0
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Weather Observation

CloudEvents type: `AU.Gov.BOM.Weather.WeatherObservation`

#### What it tells you

Half-hourly surface weather observation from a BOM automatic weather station. Each record contains temperature, wind, pressure, humidity, rainfall, cloud, and visibility measurements as reported in the station's 72-hour observation product.

#### Identity

Each event identifies the real-world resource with `{station_wmo}`. `{station_wmo}` is WMO station number identifying the reporting station. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `bom-australia`, key `{station_wmo}` |
| `MQTT/5.0` | topic `weather/au/bom/bom-australia/{state}/{station_wmo}/observation`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/bom-australia`, message subject `{station_wmo}`; application properties state `{state}` |

#### Payload

`Weather Observation` payloads are JSON object. Required fields: `station_wmo`, `station_name`, `observation_time_utc`.

- **`station_wmo`** (string, required): WMO station number identifying the reporting station.
- **`station_name`** (string, required): Human-readable name of the reporting station.
- **`observation_time_utc`** (datetime, required): Timestamp of the observation in UTC, derived from the BOM 'aifstime_utc' field in YYYYMMDDHHmmss format.
- **`local_time`** (string, optional): Local date and time string as provided by BOM in 'local_date_time_full' format (YYYYMMDDHHmmss).
- **`air_temp`** (double or null, optional, Cel (°C)): Air temperature measured at the station.
- **`apparent_temp`** (double or null, optional, Cel (°C)): Apparent (feels-like) temperature combining air temperature, humidity, and wind chill effects.
- **`dewpt`** (double or null, optional, Cel (°C)): Dew point temperature at the station.
- **`rel_hum`** (int32 or null, optional, percent (%)): Relative humidity as a percentage.
- **`delta_t`** (double or null, optional, Cel (°C)): Wet bulb depression (difference between dry and wet bulb temperatures), used for bushfire danger calculations.
- **`wind_dir`** (string or null, optional): Compass direction the wind is blowing from, e.g. 'N', 'NNE', 'SSW', 'CALM'.
- **`wind_spd_kmh`** (int32 or null, optional, km/h): Sustained wind speed in kilometres per hour.
- **`wind_spd_kt`** (int32 or null, optional, knot (kt)): Sustained wind speed in knots (nautical miles per hour).
- **`gust_kmh`** (int32 or null, optional, km/h): Maximum wind gust speed recorded in the observation period in kilometres per hour.
- **`gust_kt`** (int32 or null, optional, knot (kt)): Maximum wind gust speed recorded in the observation period in knots.
- **`press`** (double or null, optional, hPa): Atmospheric pressure at station level.
- **`press_qnh`** (double or null, optional, hPa): QNH pressure — atmospheric pressure adjusted to mean sea level using the International Standard Atmosphere, used in aviation altimetry.
- **`press_msl`** (double or null, optional, hPa): Mean sea level pressure — station pressure reduced to sea level, used for synoptic weather analysis.
- **`press_tend`** (string or null, optional): Pressure tendency description indicating whether pressure is rising, falling, or steady over the past 3 hours. May be a numeric code or textual description.
- **`rain_trace`** (string or null, optional): Rainfall since 9am local time as reported by BOM. Value is a string that may be '0.0', a numeric amount in mm, or 'Trace' for very small amounts.
- **`cloud`** (string or null, optional): Textual cloud cover description, e.g. 'Partly cloudy', 'Clear', 'Overcast'.
- **`cloud_oktas`** (int32 or null, optional): Cloud cover in oktas (eighths of sky covered), ranging from 0 (clear) to 8 (overcast).
- **`cloud_base_m`** (int32 or null, optional, m): Height of the lowest cloud base above ground level.
- **`cloud_type`** (string or null, optional): Cloud type classification as reported by the station, e.g. 'Cu', 'Cb', 'St'. May be '-' when not reported.
- **`vis_km`** (string or null, optional): Horizontal visibility in kilometres. Reported as a string as BOM may include qualifiers.
- **`weather`** (string or null, optional): Present weather description, e.g. 'Rain', 'Fog', 'Thunderstorm'. May be '-' when no significant weather.
- **`sea_state`** (string or null, optional): Sea state description for coastal stations, e.g. 'Smooth', 'Slight', 'Moderate'.
- **`swell_dir_worded`** (string or null, optional): Dominant swell direction as a compass bearing word for coastal stations.
- **`swell_height`** (double or null, optional, m): Dominant swell height for coastal stations.
- **`swell_period`** (double or null, optional, s): Dominant swell period for coastal stations.
- **`latitude`** (double, optional, degree (°)): Latitude of the station at observation time.
- **`longitude`** (double, optional, degree (°)): Longitude of the station at observation time.
- **`state`** (string, optional): Normalized routing field 'state' added for MQTT/AMQP subscriber filtering.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_wmo": "string",
  "station_name": "string",
  "observation_time_utc": "2024-01-01T00:00:00Z",
  "local_time": "string",
  "air_temp": 0,
  "apparent_temp": 0,
  "dewpt": 0,
  "rel_hum": 0,
  "delta_t": 0,
  "wind_dir": "string",
  "wind_spd_kmh": 0,
  "wind_spd_kt": 0,
  "gust_kmh": 0,
  "gust_kt": 0,
  "press": 0,
  "press_qnh": 0,
  "press_msl": 0,
  "press_tend": "string",
  "rain_trace": "string",
  "cloud": "string",
  "cloud_oktas": 0,
  "cloud_base_m": 0,
  "cloud_type": "string",
  "vis_km": "string",
  "weather": "string",
  "sea_state": "string",
  "swell_dir_worded": "string",
  "swell_height": 0,
  "swell_period": 0,
  "latitude": 0,
  "longitude": 0,
  "state": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Warning Bulletin

CloudEvents type: `AU.Gov.BOM.Warning.WarningBulletin`

#### What it tells you

Current weather warning bulletin item from a Bureau of Meteorology RSS warnings feed. Each item points to the published warning product page and carries the update timestamp and headline text from the feed.

#### Identity

Each event identifies the real-world resource with `{warning_id}`. `{warning_id}` is stable BOM warning product identifier derived from the linked product page path, for example 'IDN21037'. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `bom-australia`, key `{warning_id}` |
| `MQTT/5.0` | topic `alerts/au/bom/bom-australia/{state}/{severity}/{warning_id}/warning`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/bom-australia`, message subject `{state}/{severity}/{warning_id}` |

#### Payload

`Warning Bulletin` payloads are JSON object. Required fields: `warning_id`, `warning_url`, `feed_url`, `feed_title`, `title`, `published_at`.

- **`warning_id`** (string, required): Stable BOM warning product identifier derived from the linked product page path, for example 'IDN21037'.
- **`warning_url`** (string, required): Absolute BOM URL of the warning product page linked from the RSS item.
- **`feed_url`** (string, required): Absolute BOM RSS feed URL that published this warning item.
- **`feed_title`** (string, required): Title of the RSS feed channel publishing this warning bulletin.
- **`title`** (string, required): Normalized warning headline text from the RSS item title with line breaks collapsed to spaces.
- **`published_at`** (datetime, required): UTC timestamp when the RSS item was created or updated, taken from the item's pubDate field.
- **`issued_local_time_text`** (string or null, optional): Local issuance time prefix embedded in the RSS headline, for example '08/16:29 EST', when present.
- **`warning_type`** (string or null, optional): Warning headline extracted from the RSS title before the trailing affected-area clause, for example 'Severe Weather Warning'.
- **`affected_area_text`** (string or null, optional): Affected area clause extracted from the RSS title after the word 'for', for example 'parts of Snowy Mountains Forecast District.'.
- **`severity`** (string, optional): Normalized routing field 'severity' added for MQTT/AMQP subscriber filtering.
- **`state`** (string, optional): Normalized routing field 'state' added for MQTT/AMQP subscriber filtering.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "warning_id": "string",
  "warning_url": "string",
  "feed_url": "string",
  "feed_title": "string",
  "title": "string",
  "published_at": "2024-01-01T00:00:00Z",
  "issued_local_time_text": "string",
  "warning_type": "string",
  "affected_area_text": "string",
  "severity": "string",
  "state": "string"
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

- xRegistry manifest: [`xreg/bom_australia.xreg.json`](xreg/bom_australia.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
