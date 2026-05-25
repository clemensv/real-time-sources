# Digitraffic Marine Bridge Usage Guide Events

Digitraffic Maritime publishes maritime traffic and fairway updates from Fintraffic Digitraffic for Finnish maritime fairways and vessels. These events help consumers monitor mobility operations, passenger information, and traffic conditions without polling the upstream source directly.

## At a glance

- **Event types:** 5 documented event types.
- **Transports:** KAFKA
- **Reference vs telemetry:** 0 reference/catalog event types and 5 telemetry event types.
- **Identity:** `{mmsi}`, `{port_call_id}`, `{vessel_id}`, `{locode}` identifies the resource each event is about.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `digitraffic-maritime`. The record key is `{mmsi}`, `{port_call_id}`, `{vessel_id}`, `{locode}`. Each key template is explained in the event catalog below. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['digitraffic-maritime'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.

## Event catalog

### Vessel Location

CloudEvents type: `fi.digitraffic.marine.ais.VesselLocation`

#### What it tells you

A reference record from Fintraffic Digitraffic for a station, stop, route, site, or other transport resource. It gives consumers stable identifiers and labels needed to interpret realtime updates.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is provider field for mmsi in this record. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `digitraffic-maritime`, key `{mmsi}` |

#### Payload

`Vessel Location` payloads are JSON object. Required fields: `time`, `sog`, `cog`, `navStat`, `rot`, `posAcc`, `raim`, `heading`, `lon`, `lat`.

- **`mmsi`** (int32, optional): Provider field for mmsi in this record.
- **`time`** (int32, required): Time when the provider recorded or published the update.
- **`sog`** (double, required): Provider field for sog in this record.
- **`cog`** (double, required): Provider field for cog in this record.
- **`navStat`** (int32, required): Provider field for nav stat in this record.
- **`rot`** (int32, required): Provider field for rot in this record.
- **`posAcc`** (boolean, required): Provider field for pos acc in this record.
- **`raim`** (boolean, required): Provider field for raim in this record.
- **`heading`** (int32, required): Provider field for heading in this record.
- **`lon`** (double, required): Provider field for lon in this record.
- **`lat`** (double, required): Provider field for lat in this record.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "mmsi": 0,
  "time": 0,
  "sog": 0,
  "cog": 0,
  "navStat": 0,
  "rot": 0,
  "posAcc": false,
  "raim": false,
  "heading": 0,
  "lon": 0,
  "lat": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Vessel Metadata

CloudEvents type: `fi.digitraffic.marine.ais.VesselMetadata`

#### What it tells you

A vehicle or vessel update from Fintraffic Digitraffic. It reports the latest position, movement, identity, or voyage information available from the upstream feed.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is provider field for mmsi in this record. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `digitraffic-maritime`, key `{mmsi}` |

#### Payload

`Vessel Metadata` payloads are JSON object. Required fields: `timestamp`.

- **`mmsi`** (int32, optional): Provider field for mmsi in this record.
- **`timestamp`** (int32, required): Time when the provider recorded or published the update.
- **`name`** (string, optional): Human-readable name of the resource.
- **`callSign`** (string, optional): Provider field for call sign in this record.
- **`imo`** (int32, optional): Provider field for imo in this record.
- **`type`** (int32, optional): Provider field for type in this record.
- **`draught`** (int32, optional): Provider field for draught in this record.
- **`eta`** (int32, optional): Provider field for eta in this record.
- **`destination`** (string, optional): Provider field for destination in this record.
- **`posType`** (int32, optional): Provider field for pos type in this record.
- **`refA`** (int32, optional): Provider field for ref a in this record.
- **`refB`** (int32, optional): Provider field for ref b in this record.
- **`refC`** (int32, optional): Provider field for ref c in this record.
- **`refD`** (int32, optional): Provider field for ref d in this record.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "mmsi": 0,
  "timestamp": 0,
  "name": "string",
  "callSign": "string",
  "imo": 0,
  "type": 0,
  "draught": 0,
  "eta": 0,
  "destination": "string",
  "posType": 0,
  "refA": 0,
  "refB": 0,
  "refC": 0,
  "refD": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Port Call

CloudEvents type: `fi.digitraffic.marine.portcall.PortCall`

#### What it tells you

A transport update from Fintraffic Digitraffic. It carries maritime traffic and fairway updates for Finnish maritime fairways and vessels.

#### Identity

Each event identifies the real-world resource with `{port_call_id}`. `{port_call_id}` is digitraffic port call identifier for this Portnet vessel visit record. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `digitraffic-maritime`, key `{port_call_id}` |

#### Payload

`Port Call` payloads are JSON object. Required fields: `port_call_id`, `updated_at`, `port_to_visit`, `vessel_name`, `domestic_traffic_arrival`, `domestic_traffic_departure`, `arrival_with_cargo`, `not_loading`, `agents`, `port_areas`.

- **`port_call_id`** (int32, required): Digitraffic port call identifier for this Portnet vessel visit record.
- **`updated_at`** (datetime, required): Timestamp when this port call record was last updated in Digitraffic, from the portCallTimestamp field.
- **`customs_reference`** (string or null, optional): Customs reference string carried with the port call when available.
- **`port_to_visit`** (string, required): UN/LOCODE of the destination port that this call is scheduled to visit.
- **`previous_port`** (string or null, optional): UN/LOCODE of the vessel's previous port when reported by Portnet.
- **`next_port`** (string or null, optional): UN/LOCODE of the vessel's next announced port when reported by Portnet.
- **`mmsi`** (int32 or null, optional): Maritime Mobile Service Identity associated with the visiting vessel, when available.
- **`imo_lloyds`** (int32 or null, optional): IMO or Lloyd's vessel number carried with the port call when available.
- **`vessel_name`** (string, required): Reported vessel name for the visit.
- **`vessel_name_prefix`** (string or null, optional): Reported vessel name prefix such as 'ms' or 'mt' when present.
- **`radio_call_sign`** (string or null, optional): Radio call sign for the visiting vessel when reported by Portnet.
- **`nationality`** (string or null, optional): Flag or nationality code reported for the vessel.
- **`vessel_type_code`** (int32 or null, optional): Digitraffic vessel type code for the visiting vessel.
- **`domestic_traffic_arrival`** (boolean, required): True when the arrival leg is domestic traffic.
- **`domestic_traffic_departure`** (boolean, required): True when the departure leg is domestic traffic.
- **`arrival_with_cargo`** (boolean, required): True when the vessel is reported as arriving with cargo.
- **`not_loading`** (boolean, required): True when the vessel is reported as not loading cargo at the call.
- **`discharge`** (int32 or null, optional): Digitraffic discharge indicator value for the call when reported.
- **`current_security_level`** (int32 or null, optional): Current ISPS security level reported for the vessel at this call.
- **`agents`** (array of object, required): Agent and manager organizations attached to the port call.
- **`port_areas`** (array of object, required): Planned or actual berth and port-area timing details associated with the call.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "port_call_id": 0,
  "updated_at": "2024-01-01T00:00:00Z",
  "customs_reference": "string",
  "port_to_visit": "string",
  "previous_port": "string",
  "next_port": "string",
  "mmsi": 0,
  "imo_lloyds": 0,
  "vessel_name": "string",
  "vessel_name_prefix": "string",
  "radio_call_sign": "string",
  "nationality": "string",
  "vessel_type_code": 0,
  "domestic_traffic_arrival": false,
  "domestic_traffic_departure": false,
  "arrival_with_cargo": false,
  "not_loading": false,
  "discharge": 0,
  "current_security_level": 0,
  "agents": [
    {
      "name": "string",
      "port_call_direction": "string",
      "role": 0
    }
  ],
  "port_areas": [
    {
      "port_area_code": "string",
      "port_area_name": "string",
      "berth_code": "string",
      "berth_name": "string",
      "eta": "2024-01-01T00:00:00Z",
      "eta_source": "string",
      "etd": "2024-01-01T00:00:00Z",
      "etd_source": "string",
      "ata": "2024-01-01T00:00:00Z",
      "ata_source": "string",
      "atd": "2024-01-01T00:00:00Z",
      "atd_source": "string",
      "arrival_draught": 0,
      "departure_draught": 0
    }
  ]
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Vessel Details

CloudEvents type: `fi.digitraffic.marine.portcall.VesselDetails`

#### What it tells you

A vehicle or vessel update from Fintraffic Digitraffic. It reports the latest position, movement, identity, or voyage information available from the upstream feed.

#### Identity

Each event identifies the real-world resource with `{vessel_id}`. `{vessel_id}` is digitraffic vessel identifier from the vesselId field. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `digitraffic-maritime`, key `{vessel_id}` |

#### Payload

`Vessel Details` payloads are JSON object. Required fields: `vessel_id`, `updated_at`.

- **`vessel_id`** (integer, required): Digitraffic vessel identifier from the vesselId field. This is the stable identifier used as the CloudEvents subject and Kafka record key for vessel reference events.
- **`updated_at`** (datetime, required): Timestamp when Digitraffic last updated the vessel metadata record, from the updateTimestamp field.
- **`mmsi`** (int32 or null, optional): Maritime Mobile Service Identity associated with this vessel when available.
- **`name`** (string or null, optional): Reported vessel name.
- **`name_prefix`** (string or null, optional): Reported vessel-name prefix such as ms when available.
- **`imo_lloyds`** (int32 or null, optional): IMO or Lloyd's number associated with the vessel when available.
- **`radio_call_sign`** (string or null, optional): Radio call sign associated with the vessel when available.
- **`radio_call_sign_type`** (string or null, optional): Type of radio call sign reported by Digitraffic, for example REAL.
- **`data_source`** (string or null, optional): Upstream data source reported by Digitraffic for the vessel metadata, for example Portnet.
- **`vessel_construction`** (object, optional): Construction and classification attributes for the vessel. See [VesselConstruction](#payload-fi-digitraffic-marine-portcall-vesseldetails-vesselconstruction).
- **`vessel_dimensions`** (object, optional): Tonnage and dimensional attributes for the vessel. See [VesselDimensions](#payload-fi-digitraffic-marine-portcall-vesseldetails-vesseldimensions).
- **`vessel_registration`** (object, optional): Registry and nationality details for the vessel. See [VesselRegistration](#payload-fi-digitraffic-marine-portcall-vesseldetails-vesselregistration).
- **`vessel_system`** (object, optional): System and contact details carried with the vessel metadata. See [VesselSystem](#payload-fi-digitraffic-marine-portcall-vesseldetails-vesselsystem).
##### VesselConstruction
<a id="payload-fi-digitraffic-marine-portcall-vesseldetails-vesselconstruction"></a>

Construction and classification attributes for the vessel.

- **`vessel_type_code`** (int32 or null, optional): Digitraffic vessel type code from vesselConstruction.vesselTypeCode when available.
- **`vessel_type_name`** (string or null, optional): Human-readable vessel type name from vesselConstruction.vesselTypeName when available.
- **`ice_class_code`** (string or null, optional): Ice class code reported for the vessel when available.
- **`ice_class_issue_date`** (datetime or null, optional): Date when the current ice-class endorsement was issued, when available.
- **`ice_class_issue_place`** (string or null, optional): Place where the ice-class endorsement was issued when available.
- **`ice_class_end_date`** (datetime or null, optional): Date when the current ice-class endorsement ends, when available.
- **`double_bottom`** (boolean or null, optional): True when the vessel is reported as having a double bottom.
- **`inert_gas_system`** (boolean or null, optional): True when the vessel is reported as having an inert gas system.
- **`ballast_tank`** (boolean or null, optional): True when the vessel is reported as having a ballast tank.
##### VesselDimensions
<a id="payload-fi-digitraffic-marine-portcall-vesseldetails-vesseldimensions"></a>

Tonnage and dimensional attributes for the vessel.

- **`tonnage_certificate_issuer`** (string or null, optional): Issuer of the vessel tonnage certificate when available.
- **`date_of_issue`** (datetime or null, optional): Date when the tonnage certificate was issued when available.
- **`gross_tonnage`** (int32 or null, optional): Gross tonnage reported for the vessel when available.
- **`net_tonnage`** (int32 or null, optional): Net tonnage reported for the vessel when available.
- **`dead_weight`** (int32 or null, optional): Deadweight reported for the vessel from the deathWeight field when available.
- **`length`** (double or null, optional, m): Reported vessel length in meters when available.
- **`overall_length`** (double or null, optional, m): Reported vessel overall length in meters when available.
- **`height`** (double or null, optional, m): Reported vessel height in meters when available.
- **`breadth`** (double or null, optional, m): Reported vessel breadth in meters when available.
- **`draught`** (double or null, optional, m): Reported vessel draught in meters when available.
- **`max_speed`** (double or null, optional, kn): Reported maximum vessel speed in knots when available.
- **`engine_power`** (string or null, optional): Engine power value as reported by Digitraffic when available.
##### VesselRegistration
<a id="payload-fi-digitraffic-marine-portcall-vesseldetails-vesselregistration"></a>

Registry and nationality details for the vessel.

- **`nationality`** (string or null, optional): Reported nationality or flag state for the vessel when available.
- **`port_of_registry`** (string or null, optional): Reported port of registry or home port for the vessel when available.
##### VesselSystem
<a id="payload-fi-digitraffic-marine-portcall-vesseldetails-vesselsystem"></a>

System and contact details carried with the vessel metadata.

- **`ship_owner`** (string or null, optional): Reported ship owner name when available.
- **`ship_telephone_1`** (string or null, optional): Primary ship telephone number when available.
- **`ship_email`** (string or null, optional): Ship email address when available.
- **`ship_verifier`** (string or null, optional): Verifier or registry authority code carried with the vessel system record when available.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "vessel_id": 0,
  "updated_at": "2024-01-01T00:00:00Z",
  "mmsi": 0,
  "name": "string",
  "name_prefix": "string",
  "imo_lloyds": 0,
  "radio_call_sign": "string",
  "radio_call_sign_type": "string",
  "data_source": "string",
  "vessel_construction": {
    "vessel_type_code": 0,
    "vessel_type_name": "string",
    "ice_class_code": "string",
    "ice_class_issue_date": "2024-01-01T00:00:00Z",
    "ice_class_issue_place": "string",
    "ice_class_end_date": "2024-01-01T00:00:00Z",
    "double_bottom": false,
    "inert_gas_system": false,
    "ballast_tank": false
  },
  "vessel_dimensions": {
    "tonnage_certificate_issuer": "string",
    "date_of_issue": "2024-01-01T00:00:00Z",
    "gross_tonnage": 0,
    "net_tonnage": 0,
    "dead_weight": 0,
    "length": 0,
    "overall_length": 0,
    "height": 0,
    "breadth": 0,
    "draught": 0,
    "max_speed": 0,
    "engine_power": "string"
  },
  "vessel_registration": {
    "nationality": "string",
    "port_of_registry": "string"
  },
  "vessel_system": {
    "ship_owner": "string",
    "ship_telephone_1": "string",
    "ship_email": "string",
    "ship_verifier": "string"
  }
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Port Location

CloudEvents type: `fi.digitraffic.marine.portcall.PortLocation`

#### What it tells you

A reference record from Fintraffic Digitraffic for a station, stop, route, site, or other transport resource. It gives consumers stable identifiers and labels needed to interpret realtime updates.

#### Identity

Each event identifies the real-world resource with `{locode}`. `{locode}` is UN/LOCODE identifying the port location. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `digitraffic-maritime`, key `{locode}` |

#### Payload

`Port Location` payloads are JSON object. Required fields: `locode`, `data_updated_time`, `location_name`, `country`, `port_areas`, `berths`.

- **`locode`** (string, required): UN/LOCODE identifying the port location. This value is used as the CloudEvents subject and Kafka record key for port-location reference events.
- **`data_updated_time`** (datetime, required): Timestamp when the ports snapshot used for this location was last updated in Digitraffic.
- **`location_name`** (string, required): Human-readable port or location name from the ssnLocations feature properties.
- **`country`** (string, required): Country name reported for the location in the ssnLocations feature properties.
- **`longitude`** (double or null, optional, deg): Longitude of the port location point in decimal degrees east when the upstream feature includes geometry.
- **`latitude`** (double or null, optional, deg): Latitude of the port location point in decimal degrees north when the upstream feature includes geometry.
- **`port_areas`** (array of object, required): Port areas associated with this location from the portAreas feature collection.
- **`berths`** (array of object, required): Berth catalog entries associated with this location from the berths collection.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "locode": "string",
  "data_updated_time": "2024-01-01T00:00:00Z",
  "location_name": "string",
  "country": "string",
  "longitude": 0,
  "latitude": 0,
  "port_areas": [
    {
      "port_area_code": "string",
      "port_area_name": "string",
      "longitude": 0,
      "latitude": 0
    }
  ],
  "berths": [
    {
      "port_area_code": "string",
      "berth_code": "string",
      "berth_name": "string"
    }
  ]
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

- xRegistry manifest: [`xreg/digitraffic_maritime.xreg.json`](xreg/digitraffic_maritime.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
