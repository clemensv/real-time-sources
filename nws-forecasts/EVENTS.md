# NWS Forecast Zones Events

MQTT 5 variant of NWS forecast zone events with state, zone type, zone id, and event kind in the topic.

## At a glance

- **Event types:** 3 documented event types (9 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 3 telemetry event types.
- **Identity:** `{zone_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `nws-forecasts`. The record key is `{zone_id}`. In plain language, `{zone_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['nws-forecasts'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `weather/us/noaa/nws-forecasts/+/+/+/+`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('weather/us/noaa/nws-forecasts/+/+/+/+', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `nws-forecasts`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/nws-forecasts')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Forecast Zone

CloudEvents type: `Microsoft.OpenData.US.NOAA.NWS.ForecastZone`

#### What it tells you

Reference data for an NWS forecast zone selected by the bridge. The api.weather.gov /zones/forecast/{zoneId} endpoint returns both public land forecast zones such as WAZ315 and marine forecast zones such as PZZ135. The bridge emits this reference event at startup and on periodic refresh so downstream consumers can correlate forecast snapshots with stable zone metadata.

#### Identity

Each event identifies the real-world resource with `{zone_id}`. `{zone_id}` is NWS forecast zone identifier from the upstream properties.id field, such as WAZ315 for the City of Seattle public forecast zone or PZZ135 for the Puget Sound and Hood Canal marine zone. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `nws-forecasts`, key `{zone_id}` |
| `MQTT/5.0` | topic `weather/us/noaa/nws-forecasts/{state}/{zone_type}/{zone_id}/{event}`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/nws-forecasts`, message subject `{zone_id}`; application properties state `{state}`, zone_type `{zone_type}`, event `{event}` |

#### Payload

`Forecast Zone` payloads are JSON object. Required fields: `zone_id`, `zone_type`, `name`, `state`, `forecast_office_url`, `effective_date`, `expiration_date`.

- **`zone_id`** (string, required): NWS forecast zone identifier from the upstream properties.id field, such as WAZ315 for the City of Seattle public forecast zone or PZZ135 for the Puget Sound and Hood Canal marine zone. Constraints: pattern `^[A-Z]{3}[0-9]{3}$`.
- **`zone_type`** (enum, required): NWS zone category from the upstream properties.type field. Forecast-zone responses use 'public' for land forecast zones and marine-oriented values such as 'coastal', 'offshore', or 'marine' for waters forecasts.
- **`name`** (string, required): Human-readable NWS zone name from properties.name, for example 'City of Seattle' or 'Puget Sound and Hood Canal'.
- **`state`** (string, required): Two-letter state or marine area code from properties.state. Washington forecast zones use WA for public zones and PZ for Washington coastal and inland waters marine zones. Constraints: pattern `^[A-Z]{2}$`.
- **`forecast_office_url`** (string, required): Canonical api.weather.gov URL of the primary Weather Forecast Office responsible for the zone, from properties.forecastOffice.
- **`grid_identifier`** (string or null, optional): Grid identifier from properties.gridIdentifier. For Seattle forecast zones this is commonly the three-letter WFO grid identifier such as SEW. Marine zones can omit this field. Constraints: pattern `^[A-Z]{3}$`.
- **`awips_location_identifier`** (string or null, optional): AWIPS location identifier from properties.awipsLocationIdentifier when the zone has a matching AWIPS code.
- **`cwa_ids`** (array of string, optional): List of Weather Forecast Office county warning area identifiers from properties.cwa. The NWS publishes this as an array because a zone can be served by one or more CWAs.
- **`forecast_office_urls`** (array of string, optional): List of api.weather.gov office URLs from properties.forecastOffices. The public zone detail currently repeats the primary office here, but the endpoint models it as a list.
- **`time_zones`** (array of string, optional): Ordered list of IANA timezone names from properties.timeZone for the zone boundary. Most Puget Sound zones use a single entry of America/Los_Angeles.
- **`observation_station_ids`** (array of string, optional): Ordered list of observation station identifiers derived from the properties.observationStations URL array. The bridge strips the common URL prefix and emits only the terminal station identifier for compact reference data.
- **`radar_station`** (string or null, optional): Nearest NEXRAD radar station identifier from properties.radarStation, such as ATX for Seattle-area land zones, or null when the zone metadata does not declare a radar station.
- **`effective_date`** (datetime, required): Date and time at which this zone definition became effective, from properties.effectiveDate.
- **`expiration_date`** (datetime, required): Date and time at which this zone definition expires, from properties.expirationDate. NWS currently uses a far-future sentinel date for active zone definitions.
##### `zone_type` values

- `public`
- `coastal`
- `offshore`
- `marine`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "zone_id": "string",
  "zone_type": "public",
  "name": "string",
  "state": "string",
  "forecast_office_url": "string",
  "grid_identifier": "string",
  "awips_location_identifier": "string",
  "cwa_ids": [
    "string"
  ],
  "forecast_office_urls": [
    "string"
  ],
  "time_zones": [
    "string"
  ],
  "observation_station_ids": [
    "string"
  ],
  "radar_station": "string",
  "effective_date": "2024-01-01T00:00:00Z",
  "expiration_date": "2024-01-01T00:00:00Z"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Land Zone Forecast

CloudEvents type: `Microsoft.OpenData.US.NOAA.NWS.LandZoneForecast`

#### What it tells you

Public land-zone forecast snapshot from api.weather.gov /zones/forecast/{zoneId}/forecast. This endpoint returns narrative forecast periods for a land forecast zone such as Seattle or Tacoma. The bridge preserves the ordered forecast periods and emits the zone identifier as the Kafka key so each event represents the current forecast snapshot for one zone.

#### Identity

Each event identifies the real-world resource with `{zone_id}`. `{zone_id}` is forecast zone identifier for the land forecast snapshot. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `nws-forecasts`, key `{zone_id}` |
| `MQTT/5.0` | topic `weather/us/noaa/nws-forecasts/{state}/{zone_type}/{zone_id}/{event}`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/nws-forecasts`, message subject `{zone_id}`; application properties state `{state}`, zone_type `{zone_type}`, event `{event}` |

#### Payload

`Land Zone Forecast` payloads are JSON object. Required fields: `zone_id`, `updated`, `periods`.

- **`zone_id`** (string, required): Forecast zone identifier for the land forecast snapshot. This matches the configured zone identifier and the upstream properties.zone URL suffix. Constraints: pattern `^[A-Z]{3}[0-9]{3}$`.
- **`updated`** (datetime, required): Timestamp from properties.updated indicating when the NWS most recently updated this zone forecast.
- **`periods`** (array of object, required): Ordered narrative forecast periods from properties.periods. Each element represents one named daypart or day-level outlook such as Tonight, Tuesday, or Tuesday Night.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "zone_id": "string",
  "updated": "2024-01-01T00:00:00Z",
  "periods": [
    {
      "period_number": 0,
      "period_name": "string",
      "detailed_forecast": "string"
    }
  ]
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Marine Zone Forecast

CloudEvents type: `Microsoft.OpenData.US.NOAA.NWS.MarineZoneForecast`

#### What it tells you

Marine forecast bulletin snapshot parsed from the NOAA/NWS coastal waters text feed under tgftp.nws.noaa.gov/data/forecasts/marine/coastal/pz/. The upstream feed is plain text rather than structured JSON, so the bridge emits the bulletin metadata plus an ordered array of named narrative periods for the selected marine zone.

#### Identity

Each event identifies the real-world resource with `{zone_id}`. `{zone_id}` is marine forecast zone identifier parsed from the bulletin zone header line, such as PZZ135 for Puget Sound and Hood Canal. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `nws-forecasts`, key `{zone_id}` |
| `MQTT/5.0` | topic `weather/us/noaa/nws-forecasts/{state}/{zone_type}/{zone_id}/{event}`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/nws-forecasts`, message subject `{zone_id}`; application properties state `{state}`, zone_type `{zone_type}`, event `{event}` |

#### Payload

`Marine Zone Forecast` payloads are JSON object. Required fields: `zone_id`, `zone_name`, `issued_at_text`, `periods`, `bulletin_text`.

- **`zone_id`** (string, required): Marine forecast zone identifier parsed from the bulletin zone header line, such as PZZ135 for Puget Sound and Hood Canal. Constraints: pattern `^[A-Z]{3}[0-9]{3}$`.
- **`zone_name`** (string, required): Marine zone display name parsed from the zone header line immediately following the zone identifier in the text bulletin.
- **`product_title`** (string or null, optional): Bulletin title line, such as 'Coastal Waters Forecast for Washington'.
- **`office_name`** (string or null, optional): Issuing office line from the bulletin header, for example 'National Weather Service Seattle WA'.
- **`issued_at_text`** (string, required): Issue time line from the zone-specific section of the marine bulletin, preserved as the original text because the feed uses local-office time abbreviations such as PDT.
- **`expires_text`** (string or null, optional): Raw Expires header value from the bulletin preamble, preserved as text because the feed does not provide an explicit timezone annotation in ISO form.
- **`wmo_header`** (string or null, optional): WMO abbreviated heading line from the marine bulletin, for example 'FZUS56 KSEW 132142'.
- **`bulletin_awips_id`** (string or null, optional): AWIPS product identifier line from the bulletin, for example CWFSEW.
- **`synopsis`** (string or null, optional): Narrative synopsis paragraph that appears before the zone-specific section and describes the broader marine area covered by the bulletin.
- **`periods`** (array of object, required): Ordered narrative forecast periods parsed from the zone-specific section. Each element preserves the named period heading and its free-text forecast text.
- **`bulletin_text`** (string, required): Zone-specific marine bulletin body including the ordered period sections, preserved as plain text so downstream consumers can retain the original marine forecast wording.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "zone_id": "string",
  "zone_name": "string",
  "product_title": "string",
  "office_name": "string",
  "issued_at_text": "string",
  "expires_text": "string",
  "wmo_header": "string",
  "bulletin_awips_id": "string",
  "synopsis": "string",
  "periods": [
    {
      "period_name": "string",
      "forecast_text": "string"
    }
  ],
  "bulletin_text": "string"
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
- Reference/catalog events are documented as startup emissions, with periodic refresh when the source supports it.

## References

- xRegistry manifest: [`xreg/nws_forecasts.xreg.json`](xreg/nws_forecasts.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
