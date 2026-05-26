# Energi Data Service DK feeder Events

MQTT 5.0 binary-mode CloudEvents variant of dk.energinet.energidataservice.

## At a glance

- **Event types:** 3 documented event types (9 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 3 telemetry event types.
- **Identity:** `{price_area}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `energidataservice-dk`. The record key is `{price_area}`. In plain language, `{price_area}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['energidataservice-dk'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `energy/dk/energidataservice/energidataservice-dk/+/power-system-snapshot`, `energy/dk/energidataservice/energidataservice-dk/+/spot-price`, `energy/dk/energidataservice/energidataservice-dk/+/info`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('energy/dk/energidataservice/energidataservice-dk/+/power-system-snapshot', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `energidataservice-dk`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/energidataservice-dk')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Power System Snapshot

CloudEvents type: `dk.energinet.energidataservice.PowerSystemSnapshot`

#### What it tells you

Minute-by-minute snapshot of the Danish power system from Energi Data Service (Energinet), including CO2 emission intensity, renewable generation (solar, onshore wind, offshore wind), conventional production bands, total cross-border exchange flows, per-interconnector exchange (DK1–DE, DK1–NL, DK1–GB, DK1–NO, DK1–SE, DK1–DK2, DK2–DE, DK2–SE, Bornholm–SE), automatic and manual frequency restoration reserve activation (aFRR, mFRR) per price area, and grid imbalance per price area. Minute-by-minute snapshot of the Danish power system from Energi Data Service (Energinet). Published by the PowerSystemRightNow dataset at approximately 1-minute intervals.

#### Identity

Each event identifies the real-world resource with `{price_area}`. `{price_area}` is price area code. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `energidataservice-dk`, key `{price_area}` |
| `MQTT/5.0` | topic `energy/dk/energidataservice/energidataservice-dk/{price_area}/power-system-snapshot`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/energidataservice-dk`, message subject `{price_area}` |

#### Payload

`Power System Snapshot` payloads are JSON object. Required fields: `minutes1_utc`, `minutes1_dk`, `price_area`.

- **`minutes1_utc`** (string, required): UTC timestamp of the snapshot rounded to the nearest minute, in ISO 8601 format. Sourced from the PowerSystemRightNow 'Minutes1UTC' field.
- **`minutes1_dk`** (string, required): Danish local-time timestamp of the snapshot rounded to the nearest minute, in ISO 8601 format. Sourced from the PowerSystemRightNow 'Minutes1DK' field.
- **`price_area`** (string, required): Price area code. Set to 'DK' for system-wide power system snapshots that cover the entire Danish grid (both DK1 and DK2).
- **`co2_emission`** (double or null, optional, g/kWh): CO2 emission intensity of electricity consumed in Denmark at the time of the snapshot, measured in grams of CO2 per kWh (g/kWh). Sourced from 'CO2Emission'.
- **`production_ge_100mw`** (double or null, optional, MW): Total electricity production from centralized power plants with capacity >= 100 MW, in megawatts (MW). Sourced from 'ProductionGe100MW'.
- **`production_lt_100mw`** (double or null, optional, MW): Total electricity production from decentralized power plants with capacity < 100 MW, in megawatts (MW). Sourced from 'ProductionLt100MW'.
- **`solar_power`** (double or null, optional, MW): Estimated total solar photovoltaic power production in Denmark, in megawatts (MW). Sourced from 'SolarPower'.
- **`offshore_wind_power`** (double or null, optional, MW): Total offshore wind power production in Denmark, in megawatts (MW). Sourced from 'OffshoreWindPower'.
- **`onshore_wind_power`** (double or null, optional, MW): Total onshore wind power production in Denmark, in megawatts (MW). Sourced from 'OnshoreWindPower'.
- **`exchange_sum`** (double or null, optional, MW): Net total cross-border electricity exchange for all Danish interconnectors, in megawatts (MW). Positive values indicate net import; negative values indicate net export. Sourced from 'Exchange_Sum'.
- **`exchange_dk1_de`** (double or null, optional, MW): Electricity exchange flow on the DK1–Germany interconnector, in megawatts (MW). Positive = import to DK1, negative = export from DK1. Sourced from 'Exchange_DK1_DE'.
- **`exchange_dk1_nl`** (double or null, optional, MW): Electricity exchange flow on the DK1–Netherlands (COBRAcable) interconnector, in megawatts (MW). Positive = import to DK1, negative = export from DK1. Sourced from 'Exchange_DK1_NL'.
- **`exchange_dk1_gb`** (double or null, optional, MW): Electricity exchange flow on the DK1–Great Britain (Viking Link) interconnector, in megawatts (MW). Positive = import to DK1, negative = export from DK1. Sourced from 'Exchange_DK1_GB'.
- **`exchange_dk1_no`** (double or null, optional, MW): Electricity exchange flow on the DK1–Norway (Skagerrak) interconnector, in megawatts (MW). Positive = import to DK1, negative = export from DK1. Sourced from 'Exchange_DK1_NO'.
- **`exchange_dk1_se`** (double or null, optional, MW): Electricity exchange flow on the DK1–Sweden interconnector, in megawatts (MW). Positive = import to DK1, negative = export from DK1. Sourced from 'Exchange_DK1_SE'.
- **`exchange_dk1_dk2`** (double or null, optional, MW): Electricity exchange flow on the DK1–DK2 (Great Belt) interconnector, in megawatts (MW). Positive = flow from DK1 to DK2, negative = flow from DK2 to DK1. Sourced from 'Exchange_DK1_DK2'.
- **`exchange_dk2_de`** (double or null, optional, MW): Electricity exchange flow on the DK2–Germany (Kontek) interconnector, in megawatts (MW). Positive = import to DK2, negative = export from DK2. Sourced from 'Exchange_DK2_DE'.
- **`exchange_dk2_se`** (double or null, optional, MW): Electricity exchange flow on the DK2–Sweden (Øresund) interconnector, in megawatts (MW). Positive = import to DK2, negative = export from DK2. Sourced from 'Exchange_DK2_SE'.
- **`exchange_bornholm_se`** (double or null, optional, MW): Electricity exchange flow on the Bornholm–Sweden interconnector, in megawatts (MW). Positive = import to Bornholm, negative = export from Bornholm. Sourced from 'Exchange_Bornholm_SE'.
- **`afrr_activated_dk1`** (double or null, optional, MW): Automatic Frequency Restoration Reserve (aFRR) activated in price area DK1, in megawatts (MW). Positive = upward regulation, negative = downward regulation. Sourced from 'aFRR_ActivatedDK1'.
- **`afrr_activated_dk2`** (double or null, optional, MW): Automatic Frequency Restoration Reserve (aFRR) activated in price area DK2, in megawatts (MW). Positive = upward regulation, negative = downward regulation. Sourced from 'aFRR_ActivatedDK2'.
- **`mfrr_activated_dk1`** (double or null, optional, MW): Manual Frequency Restoration Reserve (mFRR) activated in price area DK1, in megawatts (MW). Positive = upward regulation, negative = downward regulation. Sourced from 'mFRR_ActivatedDK1'.
- **`mfrr_activated_dk2`** (double or null, optional, MW): Manual Frequency Restoration Reserve (mFRR) activated in price area DK2, in megawatts (MW). Positive = upward regulation, negative = downward regulation. Sourced from 'mFRR_ActivatedDK2'.
- **`imbalance_dk1`** (double or null, optional, MW): Net power imbalance in price area DK1, in megawatts (MW). Represents the difference between scheduled and actual generation/consumption. Sourced from 'ImbalanceDK1'.
- **`imbalance_dk2`** (double or null, optional, MW): Net power imbalance in price area DK2, in megawatts (MW). Represents the difference between scheduled and actual generation/consumption. Sourced from 'ImbalanceDK2'.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "minutes1_utc": "string",
  "minutes1_dk": "string",
  "price_area": "string",
  "co2_emission": 0,
  "production_ge_100mw": 0,
  "production_lt_100mw": 0,
  "solar_power": 0,
  "offshore_wind_power": 0,
  "onshore_wind_power": 0,
  "exchange_sum": 0,
  "exchange_dk1_de": 0,
  "exchange_dk1_nl": 0,
  "exchange_dk1_gb": 0,
  "exchange_dk1_no": 0,
  "exchange_dk1_se": 0,
  "exchange_dk1_dk2": 0,
  "exchange_dk2_de": 0,
  "exchange_dk2_se": 0,
  "exchange_bornholm_se": 0,
  "afrr_activated_dk1": 0,
  "afrr_activated_dk2": 0,
  "mfrr_activated_dk1": 0,
  "mfrr_activated_dk2": 0,
  "imbalance_dk1": 0,
  "imbalance_dk2": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Spot Price

CloudEvents type: `dk.energinet.energidataservice.SpotPrice`

#### What it tells you

Day-ahead electricity spot price per bidding zone from Energi Data Service (Energinet / Nord Pool). One record per hour per price area (DK1 – Western Denmark, DK2 – Eastern Denmark). Prices are published in both DKK and EUR.

#### Identity

Each event identifies the real-world resource with `{price_area}`. `{price_area}` is nord Pool bidding zone code. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `energidataservice-dk`, key `{price_area}` |
| `MQTT/5.0` | topic `energy/dk/energidataservice/energidataservice-dk/{price_area}/spot-price`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/energidataservice-dk`, message subject `{price_area}` |

#### Payload

`Spot Price` payloads are JSON object. Required fields: `hour_utc`, `hour_dk`, `price_area`.

- **`hour_utc`** (string, required): UTC hour for which the spot price applies, in ISO 8601 format. Each price applies to the full 60-minute interval starting at this timestamp. Sourced from 'HourUTC'.
- **`hour_dk`** (string, required): Danish local-time hour for which the spot price applies, in ISO 8601 format. Sourced from 'HourDK'.
- **`price_area`** (string, required): Nord Pool bidding zone code. 'DK1' is Western Denmark (Jutland and Funen); 'DK2' is Eastern Denmark (Zealand, Lolland-Falster, and Bornholm). Sourced from 'PriceArea'.
- **`spot_price_dkk`** (double or null, optional, DKK/MWh): Day-ahead spot price in Danish Kroner per megawatt-hour (DKK/MWh). Sourced from 'SpotPriceDKK'.
- **`spot_price_eur`** (double or null, optional, EUR/MWh): Day-ahead spot price in Euros per megawatt-hour (EUR/MWh). Sourced from 'SpotPriceEUR'.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "hour_utc": "string",
  "hour_dk": "string",
  "price_area": "string",
  "spot_price_dkk": 0,
  "spot_price_eur": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Info

CloudEvents type: `dk.energinet.energidataservice.Info`

#### What it tells you

Retained reference information for MQTT/AMQP topic discovery. Reference information for the source, area, or event collection used by MQTT retained topics and AMQP consumers to discover the logical feed scope.

#### Identity

Each event identifies the real-world resource with `{price_area}`. `{price_area}` is energy market price area or bidding zone represented by this reference record, when applicable. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `energidataservice-dk`, key `{price_area}` |
| `MQTT/5.0` | topic `energy/dk/energidataservice/energidataservice-dk/{price_area}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/energidataservice-dk`, message subject `{price_area}` |

#### Payload

`Info` payloads are JSON object. Required fields: `info_id`, `name`.

- **`info_id`** (string, required): Stable identifier for the reference information record; used as the CloudEvents subject when no more specific upstream entity exists.
- **`name`** (string, required): Human-readable name for the source, area, or event collection represented by this reference information record.
- **`country`** (string or null, optional): Lower-case ISO 3166-1 alpha-2 country code or intl when the feed spans countries.
- **`city`** (string or null, optional): City segment used in civic-events topic routing, or null when not applicable.
- **`category`** (string or null, optional): Event category segment used in topic routing, or null when not applicable.
- **`price_area`** (string or null, optional): Energy market price area or bidding zone represented by this reference record, when applicable.
- **`settlement_date`** (string or null, optional): GB settlement date for Elexon retained information topics when applicable.
- **`settlement_period`** (int32 or null, optional): GB settlement period for Elexon retained information topics when applicable.
- **`area_code`** (string or null, optional): Electricity control area or utility service area code represented by this record when applicable.
- **`segment`** (string or null, optional): Ticketmaster classification segment used for wildcard topic routing, when applicable.
- **`entity_id`** (string or null, optional): Stable upstream entity identifier for reference topics, when applicable.
- **`event_id`** (string or null, optional): Stable upstream event identifier for event-scoped reference topics, when applicable.
- **`venue_id`** (string or null, optional): Stable venue identifier for venue-scoped civic event topics, when applicable.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "info_id": "string",
  "name": "string",
  "country": "string",
  "city": "string",
  "category": "string",
  "price_area": "string",
  "settlement_date": "string",
  "settlement_period": 0,
  "area_code": "string",
  "segment": "string",
  "entity_id": "string",
  "event_id": "string",
  "venue_id": "string"
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

- xRegistry manifest: [`xreg/energidataservice_dk.xreg.json`](xreg/energidataservice_dk.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- Energi Data Service API: <https://www.energidataservice.dk/>
