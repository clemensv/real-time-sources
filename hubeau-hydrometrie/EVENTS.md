# Hub'Eau Hydrométrie API Bridge Events

This project bridges the [Hub'Eau Hydrométrie API](https://hubeau.eaufrance.fr/page/api-hydrometrie) to Apache Kafka, Azure Event Hubs, or Microsoft Fabric Event Streams. It provides real-time water level (height) and flow (discharge) data from approximately 6,300 monitoring stations across France.

## At a glance

- **Event types:** 2 documented event types.
- **Transports:** KAFKA
- **Reference vs telemetry:** 1 reference/catalog event type and 1 telemetry event type.
- **Identity:** `{code_station}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `hubeau-hydrometrie`. The record key is `{code_station}`. In plain language, `{code_station}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['hubeau-hydrometrie'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.

## Event catalog

### Station

CloudEvents type: `FR.Gov.Eaufrance.HubEau.Hydrometrie.Station`

#### What it tells you

This event carries station data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{code_station}`. `{code_station}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `hubeau-hydrometrie`, key `{code_station}` |

#### Payload

`Station` payloads are JSON object. Required fields: `code_station`, `libelle_station`, `longitude_station`, `latitude_station`.

- **`code_station`** (string, required): No description provided.
- **`libelle_station`** (string, required): No description provided.
- **`code_site`** (string or null, optional): No description provided.
- **`longitude_station`** (double, required): No description provided.
- **`latitude_station`** (double, required): No description provided.
- **`libelle_cours_eau`** (string or null, optional): No description provided.
- **`libelle_commune`** (string or null, optional): No description provided.
- **`code_departement`** (string or null, optional): No description provided.
- **`en_service`** (boolean or null, optional): No description provided.
- **`date_ouverture_station`** (string or null, optional): No description provided.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "code_station": "string",
  "libelle_station": "string",
  "code_site": "string",
  "longitude_station": 0,
  "latitude_station": 0,
  "libelle_cours_eau": "string",
  "libelle_commune": "string",
  "code_departement": "string",
  "en_service": false,
  "date_ouverture_station": "string"
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity.

### Observation

CloudEvents type: `FR.Gov.Eaufrance.HubEau.Hydrometrie.Observation`

#### What it tells you

This event carries observation data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{code_station}`. `{code_station}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `hubeau-hydrometrie`, key `{code_station}` |

#### Payload

`Observation` payloads are JSON object. Required fields: `code_station`, `date_obs`, `resultat_obs`, `grandeur_hydro`.

- **`code_station`** (string, required): No description provided.
- **`date_obs`** (datetime, required): No description provided.
- **`resultat_obs`** (double, required): No description provided.
- **`grandeur_hydro`** (string, required): No description provided.
- **`libelle_methode_obs`** (string or null, optional): No description provided.
- **`libelle_qualification_obs`** (string or null, optional): No description provided.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "code_station": "string",
  "date_obs": "2024-01-01T00:00:00Z",
  "resultat_obs": 0,
  "grandeur_hydro": "string",
  "libelle_methode_obs": "string",
  "libelle_qualification_obs": "string"
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

- xRegistry manifest: [`xreg/hubeau_hydrometrie.xreg.json`](xreg/hubeau_hydrometrie.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- Hub'Eau Hydrométrie
API: <https://hubeau.eaufrance.fr/page/api-hydrometrie>
