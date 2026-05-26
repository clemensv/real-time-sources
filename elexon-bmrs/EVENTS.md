# Elexon BMRS (GB Electricity Market) Poller Events

MQTT 5.0 binary-mode CloudEvents variant of UK.Co.Elexon.BMRS.

## At a glance

- **Event types:** 3 documented event types (9 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 3 telemetry event types.
- **Identity:** `{settlement_period}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `elexon-bmrs`. The record key is `{settlement_period}`. In plain language, `{settlement_period}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['elexon-bmrs'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `energy/gb/elexon/elexon-bmrs/gb/+/+/generation-mix`, `energy/gb/elexon/elexon-bmrs/gb/+/+/demand-outturn`, `energy/gb/elexon/elexon-bmrs/gb/+/+/info`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('energy/gb/elexon/elexon-bmrs/gb/+/+/generation-mix', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `elexon-bmrs`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/elexon-bmrs')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Generation Mix

CloudEvents type: `UK.Co.Elexon.BMRS.GenerationMix`

#### What it tells you

Half-hourly generation outturn summary for the GB electricity system from the Elexon BMRS API. Each record represents one settlement period and contains the generation output in megawatts (MW) broken down by fuel type, including domestic generation (biomass, CCGT, coal, nuclear, wind, OCGT, oil, hydro, pumped storage) and interconnector imports (France IFA, France IFA2, Netherlands BritNed, Belgium Nemo, Ireland EWIC, Norway NSL, Denmark Viking Link). Sourced from the BMRS /generation/outturn/summary endpoint.

#### Identity

Each event identifies the real-world resource with `{settlement_period}`. `{settlement_period}` is GB electricity settlement period number (1-50). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `elexon-bmrs`, key `{settlement_period}` |
| `MQTT/5.0` | topic `energy/gb/elexon/elexon-bmrs/gb/{settlement_date}/{settlement_period}/generation-mix`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/elexon-bmrs`, message subject `{settlement_period}` |

#### Payload

`Generation Mix` payloads are JSON object. Required fields: `settlement_period`, `start_time`.

- **`settlement_period`** (int32, required): GB electricity settlement period number (1-50). Each settlement period is 30 minutes long, starting at midnight UTC. Period 1 covers 00:00-00:30, period 2 covers 00:30-01:00, and so on.
- **`start_time`** (datetime, required): UTC start time of the settlement period as reported by the BMRS generation outturn summary endpoint.
- **`biomass_mw`** (double or null, optional, MW): Generation output from biomass-fuelled power stations in megawatts (MW). Biomass includes dedicated biomass plants and biomass co-firing units.
- **`ccgt_mw`** (double or null, optional, MW): Generation output from combined cycle gas turbine (CCGT) power stations in megawatts (MW). CCGT is the primary gas-fired generation technology in GB.
- **`coal_mw`** (double or null, optional, MW): Generation output from coal-fired power stations in megawatts (MW).
- **`nuclear_mw`** (double or null, optional, MW): Generation output from nuclear power stations in megawatts (MW).
- **`wind_mw`** (double or null, optional, MW): Generation output from wind farms (onshore and offshore combined) in megawatts (MW).
- **`ocgt_mw`** (double or null, optional, MW): Generation output from open cycle gas turbine (OCGT) power stations in megawatts (MW). OCGT units are typically used for peaking and reserve.
- **`oil_mw`** (double or null, optional, MW): Generation output from oil-fired power stations in megawatts (MW).
- **`npshyd_mw`** (double or null, optional, MW): Generation output from non-pumped-storage hydroelectric power stations in megawatts (MW).
- **`ps_mw`** (double or null, optional, MW): Generation output from pumped storage hydroelectric power stations in megawatts (MW). PS units can act as both generation and demand.
- **`intfr_mw`** (double or null, optional, MW): Net import via the France interconnector (IFA) in megawatts (MW). Positive values indicate import to GB.
- **`intned_mw`** (double or null, optional, MW): Net import via the Netherlands interconnector (BritNed) in megawatts (MW). Positive values indicate import to GB.
- **`intnem_mw`** (double or null, optional, MW): Net import via the Belgium interconnector (Nemo Link) in megawatts (MW). Positive values indicate import to GB.
- **`intelec_mw`** (double or null, optional, MW): Net import via the East-West Interconnector (EWIC) to Ireland in megawatts (MW). Positive values indicate import to GB.
- **`intifa2_mw`** (double or null, optional, MW): Net import via the IFA2 interconnector to France in megawatts (MW). Positive values indicate import to GB.
- **`intnsl_mw`** (double or null, optional, MW): Net import via the North Sea Link interconnector to Norway in megawatts (MW). Positive values indicate import to GB.
- **`intvkl_mw`** (double or null, optional, MW): Net import via the Viking Link interconnector to Denmark in megawatts (MW). Positive values indicate import to GB.
- **`other_mw`** (double or null, optional, MW): Generation output from other fuel types not individually categorised in megawatts (MW).
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "settlement_period": 0,
  "start_time": "2024-01-01T00:00:00Z",
  "biomass_mw": 0,
  "ccgt_mw": 0,
  "coal_mw": 0,
  "nuclear_mw": 0,
  "wind_mw": 0,
  "ocgt_mw": 0,
  "oil_mw": 0,
  "npshyd_mw": 0,
  "ps_mw": 0,
  "intfr_mw": 0,
  "intned_mw": 0,
  "intnem_mw": 0,
  "intelec_mw": 0,
  "intifa2_mw": 0,
  "intnsl_mw": 0,
  "intvkl_mw": 0,
  "other_mw": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Demand Outturn

CloudEvents type: `UK.Co.Elexon.BMRS.DemandOutturn`

#### What it tells you

Half-hourly demand outturn for the GB electricity transmission system from the Elexon BMRS API. Each record represents one settlement period and contains the initial national demand outturn (INDO) and initial transmission system demand outturn (ITSDO) in megawatts (MW). Sourced from the BMRS /demand/outturn endpoint.

#### Identity

Each event identifies the real-world resource with `{settlement_period}`. `{settlement_period}` is GB electricity settlement period number (1-50). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `elexon-bmrs`, key `{settlement_period}` |
| `MQTT/5.0` | topic `energy/gb/elexon/elexon-bmrs/gb/{settlement_date}/{settlement_period}/demand-outturn`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/elexon-bmrs`, message subject `{settlement_period}` |

#### Payload

`Demand Outturn` payloads are JSON object. Required fields: `settlement_period`, `settlement_date`, `start_time`.

- **`settlement_period`** (int32, required): GB electricity settlement period number (1-50). Each settlement period is 30 minutes long, starting at midnight UTC.
- **`settlement_date`** (string, required): Settlement date in ISO 8601 format (YYYY-MM-DD) as reported by the BMRS demand outturn endpoint.
- **`start_time`** (datetime, required): UTC start time of the settlement period as reported by the BMRS demand outturn endpoint.
- **`publish_time`** (datetime, optional): UTC timestamp when the demand outturn data was published by Elexon.
- **`initial_demand_outturn_mw`** (double or null, optional, MW): Initial national demand outturn (INDO) in megawatts (MW). This is the metered generation output less station transformer, unit transformer, and pumped storage demand, measured at the Grid Supply Point (GSP).
- **`initial_transmission_system_demand_outturn_mw`** (double or null, optional, MW): Initial transmission system demand outturn (ITSDO) in megawatts (MW). This represents the national demand plus station demand, pumping, and interconnector exports.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "settlement_period": 0,
  "settlement_date": "string",
  "start_time": "2024-01-01T00:00:00Z",
  "publish_time": "2024-01-01T00:00:00Z",
  "initial_demand_outturn_mw": 0,
  "initial_transmission_system_demand_outturn_mw": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Info

CloudEvents type: `UK.Co.Elexon.BMRS.Info`

#### What it tells you

Retained reference information for MQTT/AMQP topic discovery. Reference information for the source, area, or event collection used by MQTT retained topics and AMQP consumers to discover the logical feed scope.

#### Identity

Each event identifies the real-world resource with `{settlement_period}`. `{settlement_period}` is GB settlement period for Elexon retained information topics when applicable. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `elexon-bmrs`, key `{settlement_period}` |
| `MQTT/5.0` | topic `energy/gb/elexon/elexon-bmrs/gb/{settlement_date}/{settlement_period}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/elexon-bmrs`, message subject `{settlement_period}` |

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

- xRegistry manifest: [`xreg/elexon_bmrs.xreg.json`](xreg/elexon_bmrs.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
