# AviationWeather.gov feeder Events

MQTT 5 companion message group for gov.noaa.aviationweather.

## At a glance

- **Event types:** 3 documented event types (9 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 1 reference/catalog event type and 2 telemetry event types.
- **Identity:** `{icao_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `aviationweather`. The record key is `{icao_id}`. In plain language, `{icao_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['aviationweather'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `aviation/intl/noaa/aviationweather/+/info`, `aviation/intl/noaa/aviationweather/+/metar`, `aviation/intl/noaa/aviationweather/sigmets/+/+/sigmet`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('aviation/intl/noaa/aviationweather/+/info', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `aviationweather`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/aviationweather')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Station

CloudEvents type: `gov.noaa.aviationweather.Station`

#### What it tells you

Reference record for an aviation weather reporting station. Sourced from the AviationWeather.gov station information endpoint. Fields cover ICAO, IATA, FAA, and WMO identifiers, location, elevation, and available data products.

#### Identity

Each event identifies the real-world resource with `{icao_id}`. `{icao_id}` is ICAO station identifier. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aviationweather`, key `{icao_id}` |
| `MQTT/5.0` | topic `aviation/intl/noaa/aviationweather/{icao_id}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/aviationweather`, message subject `{icao_id}` |

#### Payload

`Station` payloads are JSON object. Required fields: `icao_id`, `name`, `latitude`, `longitude`.

- **`icao_id`** (string, required): ICAO station identifier. Four-character alphanumeric code assigned by ICAO (e.g. 'KJFK' for John F. Kennedy International Airport).
- **`iata_id`** (string or null, optional): IATA airport code, a three-character code used by the airline industry (e.g. 'JFK'). May be null for non-airport stations.
- **`faa_id`** (string or null, optional): FAA location identifier. Three or four character code assigned by the FAA. May be null for non-US stations.
- **`wmo_id`** (string or null, optional): WMO station identifier. Five-digit numeric code assigned by the World Meteorological Organization. May be null.
- **`name`** (string, required): Human-readable site name from the AviationWeather station database, e.g. 'New York/JF Kennedy Intl'.
- **`latitude`** (double, required, deg (°)): Station latitude in decimal degrees north. Negative values indicate southern hemisphere.
- **`longitude`** (double, required, deg (°)): Station longitude in decimal degrees east. Negative values indicate western hemisphere.
- **`elevation`** (double or null, optional, m): Station field elevation in meters above mean sea level.
- **`state`** (string or null, optional): State or province code where the station is located (e.g. 'NY'). May be null for non-US stations.
- **`country`** (string or null, optional): Two-character ISO 3166-1 alpha-2 country code (e.g. 'US', 'GB').
- **`site_type`** (string or null, optional): Comma-separated list of data products available at this station from the siteType array (e.g. 'METAR,TAF').
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "icao_id": "string",
  "iata_id": "string",
  "faa_id": "string",
  "wmo_id": "string",
  "name": "string",
  "latitude": 0,
  "longitude": 0,
  "elevation": 0,
  "state": "string",
  "country": "string",
  "site_type": "string"
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Metar

CloudEvents type: `gov.noaa.aviationweather.Metar`

#### What it tells you

METAR aviation weather observation from the AviationWeather.gov API. Reports surface conditions including temperature, dewpoint, wind, visibility, pressure, clouds, and flight category for an ICAO reporting station.

#### Identity

Each event identifies the real-world resource with `{icao_id}`. `{icao_id}` is ICAO station identifier for the reporting station (e.g. 'KJFK'). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aviationweather`, key `{icao_id}` |
| `MQTT/5.0` | topic `aviation/intl/noaa/aviationweather/{icao_id}/metar`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/aviationweather`, message subject `{icao_id}` |

#### Payload

`Metar` payloads are JSON object. Required fields: `icao_id`, `obs_time`, `raw_ob`.

- **`icao_id`** (string, required): ICAO station identifier for the reporting station (e.g. 'KJFK').
- **`obs_time`** (datetime, required): Observation time as a Unix epoch timestamp (seconds since 1970-01-01T00:00:00Z) from the obsTime field in the API response.
- **`report_time`** (datetime or null, optional): Report time as an ISO 8601 UTC string from the reportTime field. This is the time the observation was officially reported.
- **`temp`** (double or null, optional, CEL (°C)): Air temperature at the station. Unit: degrees Celsius.
- **`dewp`** (double or null, optional, CEL (°C)): Dewpoint temperature at the station. Unit: degrees Celsius.
- **`wdir`** (int32 or null, optional, deg (°)): Wind direction in degrees true (the direction from which the wind is blowing), averaged over the observation period. Value of 0 indicates variable or calm.
- **`wspd`** (int32 or null, optional, [kn_i] (kt)): Sustained wind speed in knots.
- **`wgst`** (int32 or null, optional, [kn_i] (kt)): Wind gust speed in knots. Null if no gusts reported.
- **`visib`** (string or null, optional): Prevailing visibility as reported. Value is a string because it can contain qualifiers like '10+' (greater than 10 statute miles) or fractional values. Unit: statute miles.
- **`altim`** (double or null, optional, hPa): Altimeter setting (QNH) in hectopascals.
- **`slp`** (double or null, optional, hPa): Sea level pressure in hectopascals. May be null if not reported.
- **`qc_field`** (int32 or null, optional): Quality control flag bitmask from the qcField in the API response.
- **`wx_string`** (string or null, optional): Present weather string using standard METAR codes (e.g. '-RA' for light rain, 'BR' for mist).
- **`metar_type`** (string or null, optional): METAR report type: 'METAR' for routine, 'SPECI' for special observation.
- **`raw_ob`** (string, required): The full raw METAR observation text as received, e.g. 'METAR KJFK 061051Z 32013KT 10SM SCT050 05/M05 A3001'.
- **`latitude`** (double or null, optional, deg (°)): Station latitude in decimal degrees north from the METAR response.
- **`longitude`** (double or null, optional, deg (°)): Station longitude in decimal degrees east from the METAR response.
- **`elevation`** (double or null, optional, m): Station elevation in meters above mean sea level from the METAR response.
- **`flt_cat`** (string or null, optional): Flight category derived from ceiling and visibility: VFR, MVFR, IFR, or LIFR.
- **`clouds`** (string or null, optional): JSON-encoded array of cloud layer objects. Each object has 'cover' (string: SKC, CLR, FEW, SCT, BKN, OVC) and 'base' (integer or null: cloud base in feet AGL). Example: '[{"cover":"SCT","base":5000}]'.
- **`name`** (string or null, optional): Human-readable station name included in the METAR response (e.g. 'New York/JF Kennedy Intl, NY, US').
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "icao_id": "string",
  "obs_time": "2024-01-01T00:00:00Z",
  "report_time": "2024-01-01T00:00:00Z",
  "temp": 0,
  "dewp": 0,
  "wdir": 0,
  "wspd": 0,
  "wgst": 0,
  "visib": "string",
  "altim": 0,
  "slp": 0,
  "qc_field": 0,
  "wx_string": "string",
  "metar_type": "string",
  "raw_ob": "string",
  "latitude": 0,
  "longitude": 0,
  "elevation": 0,
  "flt_cat": "string",
  "clouds": "string",
  "name": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Sigmet

CloudEvents type: `gov.noaa.aviationweather.Sigmet`

#### What it tells you

SIGMET (Significant Meteorological Information) advisory from the AviationWeather.gov API. Covers both US domestic convective/non-convective SIGMETs and international SIGMETs. Reports hazardous weather conditions for aviation including thunderstorms, turbulence, icing, and volcanic ash.

#### Identity

Each event identifies the real-world resource with `{icao_id}`. `{icao_id}` is ICAO identifier for the issuing office (e.g. 'KKCI' for the Kansas City Aviation Weather Center) or FIR identifier for international SIGMETs. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aviationweather`, key `{icao_id}` |
| `MQTT/5.0` | topic `aviation/intl/noaa/aviationweather/sigmets/{region}/{sigmet_id}/sigmet`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/aviationweather`, message subject `{region}/{sigmet_id}` |

#### Payload

`Sigmet` payloads are JSON object. Required fields: `icao_id`, `series_id`, `valid_time_from`, `valid_time_to`.

- **`icao_id`** (string, required): ICAO identifier for the issuing office (e.g. 'KKCI' for the Kansas City Aviation Weather Center) or FIR identifier for international SIGMETs.
- **`series_id`** (string, required): SIGMET series identifier combining alphanumeric sequence (e.g. '6W' for domestic, '8' for international).
- **`valid_time_from`** (datetime, required): Start of the SIGMET validity period as a Unix epoch timestamp (seconds since 1970-01-01T00:00:00Z).
- **`valid_time_to`** (datetime, required): End of the SIGMET validity period as a Unix epoch timestamp (seconds since 1970-01-01T00:00:00Z).
- **`hazard`** (string or null, optional): Weather hazard type: 'CONVECTIVE' for US convective SIGMETs, 'TS' (thunderstorm), 'TURB' (turbulence), 'ICE' (icing), 'VA' (volcanic ash), 'MTW' (mountain wave), etc.
- **`qualifier`** (string or null, optional): Hazard qualifier for international SIGMETs (e.g. 'EMBD' for embedded, 'SEV' for severe, 'OBSC' for obscured). Null for US domestic SIGMETs.
- **`sigmet_type`** (string or null, optional): SIGMET classification: 'SIGMET' for US domestic, 'ISIGMET' for international SIGMETs.
- **`altitude_hi`** (int32 or null, optional, [ft_i] (ft)): Upper altitude limit of the hazard area in feet. From altitudeHi1 for US SIGMETs or top for international SIGMETs.
- **`altitude_low`** (int32 or null, optional, [ft_i] (ft)): Lower altitude limit of the hazard area in feet. From altitudeLow1 for US SIGMETs or base for international SIGMETs.
- **`movement_dir`** (string or null, optional): Direction of movement of the weather phenomenon. Numeric degrees for US SIGMETs, cardinal direction string (e.g. 'NE') for international.
- **`movement_spd`** (string or null, optional): Speed of movement of the weather phenomenon. Numeric knots for US SIGMETs, knots string for international.
- **`severity`** (string or null, optional): Severity level indicator from the severity field in the US SIGMET response. Higher values indicate greater severity.
- **`raw_sigmet`** (string or null, optional): Full raw SIGMET text as received from the upstream source.
- **`coords`** (string or null, optional): JSON-encoded array of coordinate objects defining the hazard area polygon. Each object has 'lat' (number) and 'lon' (number). Example: '[{"lat":41.88,"lon":-123.70},{"lat":40.00,"lon":-124.23}]'.
- **`sigmet_id`** (string, optional): Normalized routing field 'sigmet_id' added for MQTT/AMQP subscriber filtering.
- **`region`** (string, optional): Normalized routing field 'region' added for MQTT/AMQP subscriber filtering.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "icao_id": "string",
  "series_id": "string",
  "valid_time_from": "2024-01-01T00:00:00Z",
  "valid_time_to": "2024-01-01T00:00:00Z",
  "hazard": "string",
  "qualifier": "string",
  "sigmet_type": "string",
  "altitude_hi": 0,
  "altitude_low": 0,
  "movement_dir": "string",
  "movement_spd": "string",
  "severity": "string",
  "raw_sigmet": "string",
  "coords": "string",
  "sigmet_id": "string",
  "region": "string"
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

- xRegistry manifest: [`xreg/aviationweather.xreg.json`](xreg/aviationweather.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
