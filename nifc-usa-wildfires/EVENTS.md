# NIFC USA Wildfires - Active Wildfire Incident Feed Events

NIFC USA Wildfires publishes wildfire incident status records from the U.S. National Interagency Fire Center for U.S. wildfire incidents. These events help consumers monitor hazards, route notifications, and correlate public-warning updates without polling the upstream source directly.

## At a glance

- **Event types:** 1 documented event type.
- **Transports:** KAFKA
- **Reference vs telemetry:** 0 reference/catalog event types and 1 telemetry event type.
- **Identity:** `{irwin_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `nifc-usa-wildfires`. The record key is `{irwin_id}`. In plain language, `{irwin_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['nifc-usa-wildfires'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.

## Event catalog

### Wildfire Incident

CloudEvents type: `Gov.NIFC.Wildfires.WildfireIncident`

#### What it tells you

Active wildfire incident data from the National Interagency Fire Center (NIFC) IRWIN system, published via ArcGIS Feature Service.

#### Identity

Each event identifies the real-world resource with `{irwin_id}`. `{irwin_id}` is IRWIN incident identifier, a globally unique GUID assigned by the Integrated Reporting of Wildland-Fire Information (IRWIN) system. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `nifc-usa-wildfires`, key `{irwin_id}` |

#### Payload

`Wildfire Incident` payloads are JSON object. Required fields: `irwin_id`, `incident_name`, `modified_on_datetime`.

- **`irwin_id`** (string, required): IRWIN incident identifier, a globally unique GUID assigned by the Integrated Reporting of Wildland-Fire Information (IRWIN) system. Primary key for wildfire incidents.
- **`incident_name`** (string, required): The name assigned to the wildfire incident (e.g. 'Pinnacle', 'Backbone').
- **`unique_fire_identifier`** (string or null, optional): Unique fire identifier string assigned by the dispatching agency (e.g. '2025-ORRSF-000389'). May be null for incidents not yet assigned.
- **`incident_type_category`** (string or null, optional): Category of the incident type: WF (Wildfire), RX (Prescribed Fire), or other NWCG-defined categories.
- **`incident_type_kind`** (string or null, optional): Kind of incident from NWCG classification (e.g. 'FI' for Fire).
- **`fire_discovery_datetime`** (string or null, optional): Date and time when the fire was first discovered, in ISO 8601 format. Converted from ArcGIS epoch milliseconds.
- **`daily_acres`** (double or null, optional): Most recently reported fire size in acres from the daily situation report.
- **`calculated_acres`** (double or null, optional): GIS-calculated fire area in acres, derived from perimeter mapping when available.
- **`discovery_acres`** (double or null, optional): Size of the fire in acres at the time of initial discovery.
- **`percent_contained`** (double or null, optional): Percentage of the fire perimeter that is contained (0-100). Null if not reported.
- **`poo_state`** (string or null, optional): US state or territory where the point of origin is located, as a two-letter code prefixed with 'US-' (e.g. 'US-OR', 'US-CA').
- **`poo_county`** (string or null, optional): County where the point of origin of the fire is located (e.g. 'Curry', 'Kings').
- **`latitude`** (double or null, optional): Latitude of the fire incident point of origin in decimal degrees (WGS 84).
- **`longitude`** (double or null, optional): Longitude of the fire incident point of origin in decimal degrees (WGS 84).
- **`fire_cause`** (string or null, optional): General cause of the fire (e.g. 'Natural', 'Human', 'Undetermined').
- **`fire_cause_general`** (string or null, optional): Specific fire cause category when known (e.g. 'Lightning', 'Arson', 'Equipment Use').
- **`gacc`** (string or null, optional): Geographic Area Coordination Center responsible for the incident (e.g. 'NWCC', 'OSCC', 'EACC'). GACCs coordinate wildfire management resources across regions.
- **`total_incident_personnel`** (int32 or null, optional): Total number of personnel assigned to the incident including all resources.
- **`incident_management_organization`** (string or null, optional): Name or type of the incident management organization or team managing the fire.
- **`fire_mgmt_complexity`** (string or null, optional): Complexity level of the fire management effort, typically a Type designation (e.g. 'Type 1' for the most complex).
- **`residences_destroyed`** (int32 or null, optional): Number of residential structures destroyed by the fire.
- **`other_structures_destroyed`** (int32 or null, optional): Number of non-residential structures (outbuildings, commercial, etc.) destroyed by the fire.
- **`injuries`** (int32 or null, optional): Number of injuries reported in connection with the incident.
- **`fatalities`** (int32 or null, optional): Number of fatalities reported in connection with the incident.
- **`containment_datetime`** (string or null, optional): Date and time the fire was fully contained, in ISO 8601 format. Null if not yet contained.
- **`control_datetime`** (string or null, optional): Date and time the fire was declared under control, in ISO 8601 format. Null if not yet controlled.
- **`fire_out_datetime`** (string or null, optional): Date and time the fire was declared out, in ISO 8601 format. Null if the fire is still active.
- **`final_acres`** (double or null, optional): Final fire size in acres after the fire is declared out.
- **`modified_on_datetime`** (string, required): Date and time when the incident record was last modified in the IRWIN system, in ISO 8601 format.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "irwin_id": "string",
  "incident_name": "string",
  "unique_fire_identifier": "string",
  "incident_type_category": "string",
  "incident_type_kind": "string",
  "fire_discovery_datetime": "string",
  "daily_acres": 0,
  "calculated_acres": 0,
  "discovery_acres": 0,
  "percent_contained": 0,
  "poo_state": "string",
  "poo_county": "string",
  "latitude": 0,
  "longitude": 0,
  "fire_cause": "string",
  "fire_cause_general": "string",
  "gacc": "string",
  "total_incident_personnel": 0,
  "incident_management_organization": "string",
  "fire_mgmt_complexity": "string",
  "residences_destroyed": 0,
  "other_structures_destroyed": 0,
  "injuries": 0,
  "fatalities": 0,
  "containment_datetime": "string",
  "control_datetime": "string",
  "fire_out_datetime": "string",
  "final_acres": 0,
  "modified_on_datetime": "string"
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

- xRegistry manifest: [`xreg/nifc_usa_wildfires.xreg.json`](xreg/nifc_usa_wildfires.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
