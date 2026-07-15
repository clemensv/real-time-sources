# Open Charge Map Events

Transport-neutral event family for Open Charge Map charging locations (points of interest). Carries the near-real-time ChargingLocation record keyed by the stable OCM `{poi_id}` so consumers can build a temporally consistent view of each charging location.

## At a glance

- **Event types:** 10 documented event types (30 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 9 reference/catalog event types and 1 telemetry event type.
- **Identity:** `{poi_id}`, `{reference_type}/{reference_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `open-charge-map`. The record key is `{poi_id}`, `{reference_type}/{reference_id}`. Each key template is explained in the event catalog below. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['open-charge-map'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `ev-charging/open-charge-map/location/+`, `ev-charging/open-charge-map/reference/+/+`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('ev-charging/open-charge-map/location/+', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `open-charge-map`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/open-charge-map')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Charging Location

CloudEvents type: `IO.OpenChargeMap.ChargingLocation`

#### What it tells you

Near-real-time charging-location record for one Open Charge Map point of interest, keyed by the stable OCM POI id. Emitted at startup for the configured scope and thereafter whenever the record's `DateLastStatusUpdate` advances. One electric-vehicle charging location (point of interest) from the Open Charge Map v3 POI API `https://api.openchargemap.io/v3/poi/`.

#### Identity

Each event identifies the real-world resource with `{poi_id}`. `{poi_id}` is stable Open Charge Map identifier of the point of interest (charging location), from the POI `ID` field, for example `498580`. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `open-charge-map`, key `{poi_id}` |
| `MQTT/5.0` | topic `ev-charging/open-charge-map/location/{poi_id}`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/open-charge-map`, message subject `{poi_id}` |

#### Payload

`Charging Location` payloads are JSON object. Required fields: `poi_id`, `uuid`, `latitude`, `longitude`, `connections`.

- **`poi_id`** (int32, required): Stable Open Charge Map identifier of the point of interest (charging location), from the POI `ID` field, for example `498580`. It is globally unique within OCM, persists across refreshes, and forms the single component of both the CloudEvents subject and the Kafka key so every update for one charging location lands on the same partition in emission order.
- **`uuid`** (string, required): Globally unique GUID assigned to the charging location by OCM, from the POI `UUID` field, for example `82B28E8E-0E5F-4158-9DF0-AF9991E98162`. An alternate immutable identity useful for cross-referencing OCM exports; stable across the record's lifetime.
- **`data_provider_id`** (null or int32, optional): Identifier of the data provider that supplied this record, from `DataProviderID`, for example `1` (Open Charge Map Contributors). Joins to the `DataProvider` reference event and indicates the licensing and provenance of the record.
- **`operator_id`** (null or int32, optional): Identifier of the charging-network operator for this location, from `OperatorID`, for example `3296` (InstaVolt Ltd). Joins to the `Operator` reference event. Null when the operator is unknown or not recorded.
- **`operator_title`** (null or string, optional): Human-readable operator name denormalized from the inline `OperatorInfo.Title`, for example `InstaVolt Ltd` or `Tesla (Supercharger)`. Carried inline so the event is self-contained. Null when no operator is associated.
- **`usage_type_id`** (null or int32, optional): Identifier of the access/usage model for this location, from `UsageTypeID`, for example `5` (Public - Pay At Location). Joins to the `UsageType` reference event describing whether membership, an access key, or payment at the location is required.
- **`usage_type_title`** (null or string, optional): Human-readable usage-model label denormalized from the inline `UsageType.Title`, for example `Public - Pay At Location`, `Public - Membership Required`, or `Private - Restricted Access`.
- **`usage_cost`** (null or string, optional): Free-text description of the cost to use the charging location, from the `UsageCost` field, for example `£0.85/kWh`, `Free`, or `See operator app`. Deliberately free-text because tariffs vary widely and are not normalized upstream.
- **`status_type_id`** (null or int32, optional): Location-level operational-status identifier, from the POI `StatusTypeID`, for example `50` (Operational) or `75` (Partly Operational). Joins to the `StatusType` reference event.
- **`status_title`** (null or string, optional): Human-readable operational-status label denormalized from the inline `StatusType.Title`, for example `Operational`, `Planned For Future Date`, or `Temporarily Unavailable`.
- **`is_operational`** (null or boolean, optional): Convenience boolean denormalized from the inline location-level `StatusType.IsOperational`: true when the location's status is considered operational, false when it is not, null when the status carries no operational flag.
- **`submission_status_type_id`** (null or int32, optional): Editorial submission-workflow status identifier, from `SubmissionStatusTypeID`, for example `200` (Submission Published). Joins to the `SubmissionStatusType` reference event. Live POIs returned by the public feed are normally published.
- **`submission_status_title`** (null or string, optional): Human-readable submission-workflow label denormalized from the inline `SubmissionStatus.Title`, for example `Submission Published` or `Submission Under Review`.
- **`data_quality_level`** (null or int32, optional): OCM data-quality score for the record on a 1-5 scale, from `DataQualityLevel`, where 1 is the default/unverified baseline and higher values indicate more thoroughly reviewed data. Lets consumers filter to higher-confidence records. Constraints: minimum `1`, maximum `5`.
- **`number_of_points`** (null or int32, optional): Reported total number of charge points (EVSEs) at the location, from `NumberOfPoints`, for example `1` or `6`. May be supplied directly by the contributor and can differ from the summed connection `quantity`; treat as the operator-stated bay count. Constraints: minimum `0`.
- **`general_comments`** (null or string, optional): Free-text notes about the location as a whole supplied by the contributor, from `GeneralComments`, for example access restrictions or landmark hints. Usually null.
- **`is_recently_verified`** (null or boolean, optional): True when OCM considers the record to have been verified recently (within the provider's freshness window), from `IsRecentlyVerified`. A quick freshness signal complementing `date_last_verified`.
- **`date_created`** (null or datetime, optional): UTC timestamp when the record was first created in OCM, from `DateCreated` (ISO-8601, for example `2026-07-12T20:49:00Z`). Null for very old records lacking a creation timestamp.
- **`date_last_status_update`** (null or datetime, optional): UTC timestamp of the most recent change to the record, from `DateLastStatusUpdate` (ISO-8601). This is the watermark the feeder tracks: the delta poller requests records with `modifiedsince` set just past the highest observed value so only changed locations are re-emitted.
- **`date_last_verified`** (null or datetime, optional): UTC timestamp when the record was last verified by a contributor or automated check, from `DateLastVerified` (ISO-8601). Null when never explicitly verified.
- **`date_last_confirmed`** (null or datetime, optional): UTC timestamp when the location was last confirmed as still present/correct, from `DateLastConfirmed` (ISO-8601). Frequently null.
- **`date_planned`** (null or datetime, optional): UTC date on which a planned (not-yet-operational) location is expected to open, from `DatePlanned` (ISO-8601). Populated only for locations whose status is a planned/future state; otherwise null.
- **`address_id`** (null or int32, optional): Open Charge Map identifier of the address record attached to the location, from `AddressInfo.ID`. Internal to OCM; distinct from `poi_id`.
- **`address_title`** (null or string, optional): Short site name or title of the charging location, from `AddressInfo.Title`, for example `Starbucks`, `Tesco Extra`, or `Woodfield Way Car Park`. The primary human label for the location.
- **`address_line1`** (null or string, optional): First line of the street address, from `AddressInfo.AddressLine1`, for example `Woodfield Way`.
- **`address_line2`** (null or string, optional): Second line of the street address (locality, estate, or building detail), from `AddressInfo.AddressLine2`, for example `Hexthorpe`. Usually null.
- **`town`** (null or string, optional): Town or city of the charging location, from `AddressInfo.Town`, for example `Doncaster`.
- **`state_or_province`** (null or string, optional): State, province, region, or country subdivision, from `AddressInfo.StateOrProvince`, for example `England`, `California`, or `Bayern`.
- **`postcode`** (null or string, optional): Postal or ZIP code of the charging location, from `AddressInfo.Postcode`, for example `DN4 8SJ`.
- **`country_id`** (null or int32, optional): Identifier of the country the location is in, from `AddressInfo.CountryID`, for example `1` (United Kingdom). Joins to the `Country` reference event.
- **`country_iso_code`** (null or string, optional): ISO 3166-1 alpha-2 country code denormalized from the inline `AddressInfo.Country.ISOCode`, for example `GB`, `US`, or `DE`. Carried inline for convenient country-level filtering.
- **`country_title`** (null or string, optional): Human-readable country name denormalized from the inline `AddressInfo.Country.Title`, for example `United Kingdom`.
- **`latitude`** (double, required, deg (°)): WGS 84 latitude of the charging location in decimal degrees, from `AddressInfo.Latitude`, for example `53.498591581284586`. Positive north of the equator. Present on every OCM location and used directly as the map coordinate. Constraints: minimum `-90`, maximum `90`.
- **`longitude`** (double, required, deg (°)): WGS 84 longitude of the charging location in decimal degrees, from `AddressInfo.Longitude`, for example `-1.1232887704744599`. Positive east of the prime meridian. Present on every OCM location and used directly as the map coordinate. Constraints: minimum `-180`, maximum `180`.
- **`contact_telephone1`** (null or string, optional): Primary contact telephone number for the location, from `AddressInfo.ContactTelephone1`. Usually null.
- **`contact_telephone2`** (null or string, optional): Secondary contact telephone number for the location, from `AddressInfo.ContactTelephone2`. Usually null.
- **`contact_email`** (null or string, optional): Contact email address for the location, from `AddressInfo.ContactEmail`. Usually null.
- **`access_comments`** (null or string, optional): Free-text access notes for reaching or using the location, from `AddressInfo.AccessComments`, for example parking or opening-hours hints. Usually null.
- **`related_url`** (null or string, optional): Operator or venue web page related to the location, from `AddressInfo.RelatedURL`. Usually null.
- **`connections`** (array of object, required): Array of the physical charging connections (EVSE connectors) documented at the location, from the POI `Connections` array. Each element describes one connector configuration: standard, level, current type, electrical rating, status, and quantity. The bridge always emits a list, empty when the contributor has not itemized the connectors, in which case `number_of_points` may still indicate the bay count.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "poi_id": 0,
  "uuid": "string",
  "data_provider_id": 0,
  "operator_id": 0,
  "operator_title": "string",
  "usage_type_id": 0,
  "usage_type_title": "string",
  "usage_cost": "string",
  "status_type_id": 0,
  "status_title": "string",
  "is_operational": false,
  "submission_status_type_id": 0,
  "submission_status_title": "string",
  "data_quality_level": 0,
  "number_of_points": 0,
  "general_comments": "string",
  "is_recently_verified": false,
  "date_created": "2024-01-01T00:00:00Z",
  "date_last_status_update": "2024-01-01T00:00:00Z",
  "date_last_verified": "2024-01-01T00:00:00Z",
  "date_last_confirmed": "2024-01-01T00:00:00Z",
  "date_planned": "2024-01-01T00:00:00Z",
  "address_id": 0,
  "address_title": "string",
  "address_line1": "string",
  "address_line2": "string",
  "town": "string",
  "state_or_province": "string",
  "postcode": "string",
  "country_id": 0,
  "country_iso_code": "string",
  "country_title": "string",
  "latitude": 0,
  "longitude": 0,
  "contact_telephone1": "string",
  "contact_telephone2": "string",
  "contact_email": "string",
  "access_comments": "string",
  "related_url": "string",
  "connections": [
    {
      "connection_id": 0,
      "connection_type_id": 0,
      "connection_type_title": "string",
      "connection_type_formal_name": "string",
      "reference": "string",
      "status_type_id": 0,
      "is_operational": false,
      "level_id": 0,
      "level_title": "string",
      "is_fast_charge_capable": false,
      "amps": 0,
      "voltage": 0,
      "power_kw": 0,
      "current_type_id": 0,
      "current_type_title": "string",
      "quantity": 0,
      "comments": "string"
    }
  ]
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Operator

CloudEvents type: `IO.OpenChargeMap.Operator`

#### What it tells you

Open Charge Map Operator reference catalog entity, keyed by the composite `{reference_type}/{reference_id}` so all lookup entities share one identity shape on the reference topic. Emitted at startup and on the periodic reference refresh. One charging-network operator from the Open Charge Map reference data `https://api.openchargemap.io/v3/referencedata/` (`Operators` table, ~977 entries).

#### Identity

Each event identifies the real-world resource with `{reference_type}/{reference_id}`. `{reference_type}` is constant discriminator `operator` identifying this event as an operator reference entity; `{reference_id}` is open Charge Map operator identifier, from the operator `ID` field, for example `3296`. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `open-charge-map`, key `{reference_type}/{reference_id}` |
| `MQTT/5.0` | topic `ev-charging/open-charge-map/reference/{reference_type}/{reference_id}`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/open-charge-map`, message subject `{reference_type}/{reference_id}` |

#### Payload

`Operator` payloads are JSON object. Required fields: `reference_type`, `reference_id`, `title`.

- **`reference_type`** (string, required): Constant discriminator `operator` identifying this event as an operator reference entity. Forms the first segment of the `{reference_type}/{reference_id}` CloudEvents subject and Kafka key.
- **`reference_id`** (int32, required): Open Charge Map operator identifier, from the operator `ID` field, for example `3296`. Matches the `operator_id` carried on ChargingLocation and forms the second segment of the subject/key.
- **`title`** (string, required): Human-readable name of the reference entity, from its `Title` field.
- **`website_url`** (null or string, optional): Operator web site URL, from `WebsiteURL`. Null when unknown.
- **`comments`** (null or string, optional): Free-text notes about the operator, from `Comments`, for example payment or roaming details. Often null.
- **`phone_primary_contact`** (null or string, optional): Primary contact telephone number for the operator, from `PhonePrimaryContact`. Often null.
- **`phone_secondary_contact`** (null or string, optional): Secondary contact telephone number for the operator, from `PhoneSecondaryContact`. Often null.
- **`contact_email`** (null or string, optional): Contact email address for the operator, from `ContactEmail`. Often null.
- **`booking_url`** (null or string, optional): URL for booking or account sign-up with the operator, from `BookingURL`. Often null.
- **`fault_report_email`** (null or string, optional): Email address for reporting faults to the operator, from `FaultReportEmail`. Often null.
- **`is_private_individual`** (null or boolean, optional): True when the operator record represents a private individual rather than a commercial network, from `IsPrivateIndividual`.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "reference_type": "string",
  "reference_id": 0,
  "title": "string",
  "website_url": "string",
  "comments": "string",
  "phone_primary_contact": "string",
  "phone_secondary_contact": "string",
  "contact_email": "string",
  "booking_url": "string",
  "fault_report_email": "string",
  "is_private_individual": false
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Connection Type

CloudEvents type: `IO.OpenChargeMap.ConnectionType`

#### What it tells you

Open Charge Map ConnectionType reference catalog entity, keyed by the composite `{reference_type}/{reference_id}` so all lookup entities share one identity shape on the reference topic. Emitted at startup and on the periodic reference refresh. One EV connector standard from the Open Charge Map reference data (`ConnectionTypes` table, ~43 entries).

#### Identity

Each event identifies the real-world resource with `{reference_type}/{reference_id}`. `{reference_type}` is constant discriminator `connection_type` identifying this event as a connector-standard reference entity; `{reference_id}` is open Charge Map connection-type identifier, from the connection-type `ID` field, for example `33` (CCS Type 2). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `open-charge-map`, key `{reference_type}/{reference_id}` |
| `MQTT/5.0` | topic `ev-charging/open-charge-map/reference/{reference_type}/{reference_id}`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/open-charge-map`, message subject `{reference_type}/{reference_id}` |

#### Payload

`Connection Type` payloads are JSON object. Required fields: `reference_type`, `reference_id`, `title`.

- **`reference_type`** (string, required): Constant discriminator `connection_type` identifying this event as a connector-standard reference entity.
- **`reference_id`** (int32, required): Open Charge Map connection-type identifier, from the connection-type `ID` field, for example `33` (CCS Type 2). Matches the `connection_type_id` on ChargingLocation connections.
- **`title`** (string, required): Human-readable name of the reference entity, from its `Title` field.
- **`formal_name`** (null or string, optional): Formal standards designation of the connector, from `FormalName`, for example `IEC 62196-3 Configuration FF`. Null when not recorded.
- **`is_discontinued`** (null or boolean, optional): True when the connector standard has been discontinued, from `IsDiscontinued`. Discontinued types still appear on historical locations.
- **`is_obsolete`** (null or boolean, optional): True when the connector standard is considered obsolete, from `IsObsolete`.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "reference_type": "string",
  "reference_id": 0,
  "title": "string",
  "formal_name": "string",
  "is_discontinued": false,
  "is_obsolete": false
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Current Type

CloudEvents type: `IO.OpenChargeMap.CurrentType`

#### What it tells you

Open Charge Map CurrentType reference catalog entity, keyed by the composite `{reference_type}/{reference_id}` so all lookup entities share one identity shape on the reference topic. Emitted at startup and on the periodic reference refresh. One electrical current type from the Open Charge Map reference data (`CurrentTypes` table, 3 entries: AC single-phase, AC three-phase, DC).

#### Identity

Each event identifies the real-world resource with `{reference_type}/{reference_id}`. `{reference_type}` is constant discriminator `current_type` identifying this event as a current-type reference entity; `{reference_id}` is open Charge Map current-type identifier, from the current-type `ID` field: `10` (AC single-phase), `20` (AC three-phase), or `30` (DC). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `open-charge-map`, key `{reference_type}/{reference_id}` |
| `MQTT/5.0` | topic `ev-charging/open-charge-map/reference/{reference_type}/{reference_id}`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/open-charge-map`, message subject `{reference_type}/{reference_id}` |

#### Payload

`Current Type` payloads are JSON object. Required fields: `reference_type`, `reference_id`, `title`.

- **`reference_type`** (string, required): Constant discriminator `current_type` identifying this event as a current-type reference entity.
- **`reference_id`** (int32, required): Open Charge Map current-type identifier, from the current-type `ID` field: `10` (AC single-phase), `20` (AC three-phase), or `30` (DC). Matches the `current_type_id` on ChargingLocation connections.
- **`title`** (string, required): Human-readable name of the reference entity, from its `Title` field.
- **`description`** (null or string, optional): Longer description of the current type, from `Description`, for example `Direct Current`.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "reference_type": "string",
  "reference_id": 0,
  "title": "string",
  "description": "string"
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Charger Type

CloudEvents type: `IO.OpenChargeMap.ChargerType`

#### What it tells you

Open Charge Map ChargerType reference catalog entity, keyed by the composite `{reference_type}/{reference_id}` so all lookup entities share one identity shape on the reference topic. Emitted at startup and on the periodic reference refresh. One charging level (charger power class) from the Open Charge Map reference data (`ChargerTypes` table, 3 entries: Level 1 Low, Level 2 Medium, Level 3 High).

#### Identity

Each event identifies the real-world resource with `{reference_type}/{reference_id}`. `{reference_type}` is constant discriminator `charger_type` identifying this event as a charging-level reference entity; `{reference_id}` is open Charge Map charging-level identifier, from the charger-type `ID` field: `1` (Level 1, Low, under ~2 kW), `2` (Level 2, Medium, ~2-40 kW), or `3` (Level 3, High, over 40 kW). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `open-charge-map`, key `{reference_type}/{reference_id}` |
| `MQTT/5.0` | topic `ev-charging/open-charge-map/reference/{reference_type}/{reference_id}`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/open-charge-map`, message subject `{reference_type}/{reference_id}` |

#### Payload

`Charger Type` payloads are JSON object. Required fields: `reference_type`, `reference_id`, `title`.

- **`reference_type`** (string, required): Constant discriminator `charger_type` identifying this event as a charging-level reference entity.
- **`reference_id`** (int32, required): Open Charge Map charging-level identifier, from the charger-type `ID` field: `1` (Level 1, Low, under ~2 kW), `2` (Level 2, Medium, ~2-40 kW), or `3` (Level 3, High, over 40 kW). Matches the `level_id` on ChargingLocation connections.
- **`title`** (string, required): Human-readable name of the reference entity, from its `Title` field.
- **`comments`** (null or string, optional): Description of the charging level's power band, from `Comments`, for example `40KW and Higher`.
- **`is_fast_charge_capable`** (null or boolean, optional): True when this level is classed as fast charging, from `IsFastChargeCapable` (true for Level 3).
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "reference_type": "string",
  "reference_id": 0,
  "title": "string",
  "comments": "string",
  "is_fast_charge_capable": false
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Country

CloudEvents type: `IO.OpenChargeMap.Country`

#### What it tells you

Open Charge Map Country reference catalog entity, keyed by the composite `{reference_type}/{reference_id}` so all lookup entities share one identity shape on the reference topic. Emitted at startup and on the periodic reference refresh. One country from the Open Charge Map reference data (`Countries` table, ~250 entries).

#### Identity

Each event identifies the real-world resource with `{reference_type}/{reference_id}`. `{reference_type}` is constant discriminator `country` identifying this event as a country reference entity; `{reference_id}` is open Charge Map country identifier, from the country `ID` field, for example `1` (United Kingdom). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `open-charge-map`, key `{reference_type}/{reference_id}` |
| `MQTT/5.0` | topic `ev-charging/open-charge-map/reference/{reference_type}/{reference_id}`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/open-charge-map`, message subject `{reference_type}/{reference_id}` |

#### Payload

`Country` payloads are JSON object. Required fields: `reference_type`, `reference_id`, `title`.

- **`reference_type`** (string, required): Constant discriminator `country` identifying this event as a country reference entity.
- **`reference_id`** (int32, required): Open Charge Map country identifier, from the country `ID` field, for example `1` (United Kingdom). Matches the `country_id` on ChargingLocation.
- **`title`** (string, required): Human-readable name of the reference entity, from its `Title` field.
- **`iso_code`** (null or string, optional): ISO 3166-1 alpha-2 country code, from `ISOCode`, for example `GB`, `US`, or `DE`.
- **`continent_code`** (null or string, optional): Two-letter continent code, from `ContinentCode`, for example `EU`, `NA`, `AS`, `OC`, `AF`, or `SA`.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "reference_type": "string",
  "reference_id": 0,
  "title": "string",
  "iso_code": "string",
  "continent_code": "string"
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Data Provider

CloudEvents type: `IO.OpenChargeMap.DataProvider`

#### What it tells you

Open Charge Map DataProvider reference catalog entity, keyed by the composite `{reference_type}/{reference_id}` so all lookup entities share one identity shape on the reference topic. Emitted at startup and on the periodic reference refresh. One data provider from the Open Charge Map reference data (`DataProviders` table, ~56 entries).

#### Identity

Each event identifies the real-world resource with `{reference_type}/{reference_id}`. `{reference_type}` is constant discriminator `data_provider` identifying this event as a data-provider reference entity; `{reference_id}` is open Charge Map data-provider identifier, from the data-provider `ID` field, for example `1` (Open Charge Map Contributors). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `open-charge-map`, key `{reference_type}/{reference_id}` |
| `MQTT/5.0` | topic `ev-charging/open-charge-map/reference/{reference_type}/{reference_id}`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/open-charge-map`, message subject `{reference_type}/{reference_id}` |

#### Payload

`Data Provider` payloads are JSON object. Required fields: `reference_type`, `reference_id`, `title`.

- **`reference_type`** (string, required): Constant discriminator `data_provider` identifying this event as a data-provider reference entity.
- **`reference_id`** (int32, required): Open Charge Map data-provider identifier, from the data-provider `ID` field, for example `1` (Open Charge Map Contributors). Matches the `data_provider_id` on ChargingLocation.
- **`title`** (string, required): Human-readable name of the reference entity, from its `Title` field.
- **`website_url`** (null or string, optional): Data provider web site URL, from `WebsiteURL`.
- **`comments`** (null or string, optional): Free-text notes about the data provider, from `Comments`. Often null.
- **`license`** (null or string, optional): Licence under which the provider's data is published, from `License`, for example `Licensed under Creative Commons Attribution 4.0 International`. Governs reuse of the records attributed to this provider.
- **`is_open_data_licensed`** (null or boolean, optional): True when the provider's data is available under an open-data licence, from `IsOpenDataLicensed`.
- **`is_restricted_edit`** (null or boolean, optional): True when records from this provider are edit-restricted in OCM, from `IsRestrictedEdit`.
- **`is_approved_import`** (null or boolean, optional): True when the provider is an approved bulk-import source, from `IsApprovedImport`.
- **`status_title`** (null or string, optional): Human-readable provider-status label denormalized from the inline `DataProviderStatusType.Title`, for example `Manual Data Entry` or `Automated Import`.
- **`is_provider_enabled`** (null or boolean, optional): True when the provider is currently enabled as a source, denormalized from the inline `DataProviderStatusType.IsProviderEnabled`.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "reference_type": "string",
  "reference_id": 0,
  "title": "string",
  "website_url": "string",
  "comments": "string",
  "license": "string",
  "is_open_data_licensed": false,
  "is_restricted_edit": false,
  "is_approved_import": false,
  "status_title": "string",
  "is_provider_enabled": false
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Status Type

CloudEvents type: `IO.OpenChargeMap.StatusType`

#### What it tells you

Open Charge Map StatusType reference catalog entity, keyed by the composite `{reference_type}/{reference_id}` so all lookup entities share one identity shape on the reference topic. Emitted at startup and on the periodic reference refresh. One operational-status type from the Open Charge Map reference data (`StatusTypes` table, ~10 entries).

#### Identity

Each event identifies the real-world resource with `{reference_type}/{reference_id}`. `{reference_type}` is constant discriminator `status_type` identifying this event as an operational-status reference entity; `{reference_id}` is open Charge Map status-type identifier, from the status-type `ID` field, for example `50` (Operational). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `open-charge-map`, key `{reference_type}/{reference_id}` |
| `MQTT/5.0` | topic `ev-charging/open-charge-map/reference/{reference_type}/{reference_id}`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/open-charge-map`, message subject `{reference_type}/{reference_id}` |

#### Payload

`Status Type` payloads are JSON object. Required fields: `reference_type`, `reference_id`, `title`.

- **`reference_type`** (string, required): Constant discriminator `status_type` identifying this event as an operational-status reference entity.
- **`reference_id`** (int32, required): Open Charge Map status-type identifier, from the status-type `ID` field, for example `50` (Operational). Matches the `status_type_id` on ChargingLocation and its connections.
- **`title`** (string, required): Human-readable name of the reference entity, from its `Title` field.
- **`is_operational`** (null or boolean, optional): True when this status denotes operational equipment, from `IsOperational`. Null for statuses that carry no operational determination.
- **`is_user_selectable`** (null or boolean, optional): True when contributors may select this status when editing, from `IsUserSelectable`.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "reference_type": "string",
  "reference_id": 0,
  "title": "string",
  "is_operational": false,
  "is_user_selectable": false
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Usage Type

CloudEvents type: `IO.OpenChargeMap.UsageType`

#### What it tells you

Open Charge Map UsageType reference catalog entity, keyed by the composite `{reference_type}/{reference_id}` so all lookup entities share one identity shape on the reference topic. Emitted at startup and on the periodic reference refresh. One access/usage model from the Open Charge Map reference data (`UsageTypes` table, ~8 entries).

#### Identity

Each event identifies the real-world resource with `{reference_type}/{reference_id}`. `{reference_type}` is constant discriminator `usage_type` identifying this event as a usage-model reference entity; `{reference_id}` is open Charge Map usage-type identifier, from the usage-type `ID` field, for example `5` (Public - Pay At Location). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `open-charge-map`, key `{reference_type}/{reference_id}` |
| `MQTT/5.0` | topic `ev-charging/open-charge-map/reference/{reference_type}/{reference_id}`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/open-charge-map`, message subject `{reference_type}/{reference_id}` |

#### Payload

`Usage Type` payloads are JSON object. Required fields: `reference_type`, `reference_id`, `title`.

- **`reference_type`** (string, required): Constant discriminator `usage_type` identifying this event as a usage-model reference entity.
- **`reference_id`** (int32, required): Open Charge Map usage-type identifier, from the usage-type `ID` field, for example `5` (Public - Pay At Location). Matches the `usage_type_id` on ChargingLocation.
- **`title`** (string, required): Human-readable name of the reference entity, from its `Title` field.
- **`is_pay_at_location`** (null or boolean, optional): True when the user pays at the location (for example by card or coin), from `IsPayAtLocation`.
- **`is_membership_required`** (null or boolean, optional): True when network membership is required to use the location, from `IsMembershipRequired`.
- **`is_access_key_required`** (null or boolean, optional): True when a physical or digital access key (RFID card, app token) is required, from `IsAccessKeyRequired`.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "reference_type": "string",
  "reference_id": 0,
  "title": "string",
  "is_pay_at_location": false,
  "is_membership_required": false,
  "is_access_key_required": false
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Submission Status Type

CloudEvents type: `IO.OpenChargeMap.SubmissionStatusType`

#### What it tells you

Open Charge Map SubmissionStatusType reference catalog entity, keyed by the composite `{reference_type}/{reference_id}` so all lookup entities share one identity shape on the reference topic. Emitted at startup and on the periodic reference refresh. One editorial submission-workflow status from the Open Charge Map reference data (`SubmissionStatusTypes` table, ~11 entries).

#### Identity

Each event identifies the real-world resource with `{reference_type}/{reference_id}`. `{reference_type}` is constant discriminator `submission_status_type` identifying this event as a submission-workflow reference entity; `{reference_id}` is open Charge Map submission-status identifier, from the submission-status `ID` field, for example `200` (Submission Published). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `open-charge-map`, key `{reference_type}/{reference_id}` |
| `MQTT/5.0` | topic `ev-charging/open-charge-map/reference/{reference_type}/{reference_id}`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/open-charge-map`, message subject `{reference_type}/{reference_id}` |

#### Payload

`Submission Status Type` payloads are JSON object. Required fields: `reference_type`, `reference_id`, `title`.

- **`reference_type`** (string, required): Constant discriminator `submission_status_type` identifying this event as a submission-workflow reference entity.
- **`reference_id`** (int32, required): Open Charge Map submission-status identifier, from the submission-status `ID` field, for example `200` (Submission Published). Matches the `submission_status_type_id` on ChargingLocation.
- **`title`** (string, required): Human-readable name of the reference entity, from its `Title` field.
- **`is_live`** (null or boolean, optional): True when records with this submission status are publicly live/visible, from `IsLive`.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "reference_type": "string",
  "reference_id": 0,
  "title": "string",
  "is_live": false
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

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

- xRegistry manifest: [`xreg/open-charge-map.xreg.json`](xreg/open-charge-map.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- API docs: <https://openchargemap.org/site/develop/api>
