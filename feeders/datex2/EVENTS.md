# DATEX II real-time traffic feeder Events

DATEX II MeasuredDataPublication telemetry and MeasurementSiteTablePublication reference data.

## At a glance

- **Event types:** 3 documented event types (9 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 3 telemetry event types.
- **Identity:** `{supplier_id}/{measurement_site_id}`, `{supplier_id}/{situation_record_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `datex2`. The record key is `{supplier_id}/{measurement_site_id}`, `{supplier_id}/{situation_record_id}`. Each key template is explained in the event catalog below. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['datex2'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `traffic/+/+/datex2/measured/+/+/site`, `traffic/+/+/datex2/measured/+/+/measurement`, `traffic/+/+/datex2/situations/+/+/record`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('traffic/+/+/datex2/measured/+/+/site', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `broker-configured address`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/events')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Measurement Site

CloudEvents type: `org.datex2.measured.MeasurementSite`

#### What it tells you

Reference measurement-site record from a DATEX II MeasurementSiteTablePublication. Reference event describing a DATEX II MeasurementSiteTablePublication measurement site. It contextualizes MeasuredDataPublication traffic observations with site identity, location, equipment, and lane metadata.

#### Identity

Each event identifies the real-world resource with `{supplier_id}/{measurement_site_id}`. `{supplier_id}` is stable endpoint registry identifier assigned to the DATEX II supplier/operator configuration; `{measurement_site_id}` is stable DATEX II measurement site identifier from measurementSiteReference/@id or measurementSiteRecord/@id. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `datex2`, key `{supplier_id}/{measurement_site_id}` |
| `MQTT/5.0` | topic `traffic/{country_code}/{operator_id}/datex2/measured/{supplier_id}/{measurement_site_id}/site`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `broker-configured node`, message subject `{supplier_id}/{measurement_site_id}` |

#### Payload

`Measurement Site` payloads are JSON object. Required fields: `supplier_id`, `measurement_site_id`, `feed_url`, `country_code`, `operator_id`.

- **`supplier_id`** (string, required): Stable endpoint registry identifier assigned to the DATEX II supplier/operator configuration. It scopes upstream identifiers that are only guaranteed unique within one publisher.
- **`measurement_site_id`** (string, required): Stable DATEX II measurement site identifier from measurementSiteReference/@id or measurementSiteRecord/@id. It is the stable identity for fixed traffic measurement equipment and route measurement sites.
- **`feed_url`** (uri, required): Canonical URL of the DATEX II endpoint configuration from which this normalized event was acquired. Used as the CloudEvents source value.
- **`country_code`** (string, required): ISO 3166-1 alpha-2 country code from the endpoint registry, used for regional routing and filtering when the upstream feed covers a national road authority. Required for MQTT topic routing and retained in the payload for consumers.
- **`operator_id`** (string, required): operator or road authority code from the endpoint registry, such as NDW, Bison Futé, Trafikverket, National Highways, Statens vegvesen, or CITA. Required for MQTT topic routing and retained in the payload for consumers.
- **`name`** (string or null, optional): Human-readable measurement site name from measurementSiteName or an equivalent DATEX II location label. It is descriptive only and never used as a key.
- **`measurement_site_type`** (string or null, optional): DATEX II equipment or measurement-site type such as inductionLoop, microwave, floatingCar, Bluetooth, or routeSection. Values come from measurementEquipmentTypeUsed or the site table profile.
- **`period_seconds`** (int32 or null, optional): Nominal aggregation period in seconds from measurementSpecificCharacteristics/period. Consumers use it to interpret flow, speed, and occupancy observations.
- **`latitude`** (double or null, optional): WGS84 latitude in decimal degrees from pointByCoordinates/pointCoordinates/latitude. Null when the site table omits coordinates.
- **`longitude`** (double or null, optional): WGS84 longitude in decimal degrees from pointByCoordinates/pointCoordinates/longitude. Null when the site table omits coordinates.
- **`road_number`** (string or null, optional): Road or route identifier from roadInformation/roadName, roadNumber, or a TPEG linkName descriptor, for example A10, N205, M25, or E411.
- **`carriageway`** (string or null, optional): DATEX II carriageway classification affected or measured, such as mainCarriageway, entrySlipRoad, exitSlipRoad, or connectingCarriageway.
- **`lane`** (string or null, optional): DATEX II lane classification when a measurement site is lane-specific, such as lane1, lane2, busLane, hardShoulder, or allLanesCompleteCarriageway.
- **`specific_measurements`** (string or null, optional): Compact JSON/text summary of measurementSpecificCharacteristics entries when the upstream site table exposes multiple per-lane or per-vehicle-class measurements. Preserved so bespoke NDW measurement-site detail can be represented without dropping profile-specific metadata.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "supplier_id": "string",
  "measurement_site_id": "string",
  "feed_url": "string",
  "country_code": "string",
  "operator_id": "string",
  "name": "string",
  "measurement_site_type": "string",
  "period_seconds": 0,
  "latitude": 0,
  "longitude": 0,
  "road_number": "string",
  "carriageway": "string",
  "lane": "string",
  "specific_measurements": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Traffic Measurement

CloudEvents type: `org.datex2.measured.TrafficMeasurement`

#### What it tells you

Traffic speed, flow, occupancy, or travel-time observation from a DATEX II MeasuredDataPublication. Normalized traffic measurement from a DATEX II MeasuredDataPublication. The schema covers point and route observations emitted by NDW and Bison Futé including speed, flow, occupancy, and travel time.

#### Identity

Each event identifies the real-world resource with `{supplier_id}/{measurement_site_id}`. `{supplier_id}` is stable endpoint registry identifier assigned to the DATEX II supplier/operator configuration; `{measurement_site_id}` is stable DATEX II measurement site identifier from measurementSiteReference/@id or measurementSiteRecord/@id. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `datex2`, key `{supplier_id}/{measurement_site_id}` |
| `MQTT/5.0` | topic `traffic/{country_code}/{operator_id}/datex2/measured/{supplier_id}/{measurement_site_id}/measurement`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `broker-configured node`, message subject `{supplier_id}/{measurement_site_id}` |

#### Payload

`Traffic Measurement` payloads are JSON object. Required fields: `supplier_id`, `measurement_site_id`, `feed_url`, `measurement_time`, `measurement_time_key`, `country_code`, `operator_id`.

- **`supplier_id`** (string, required): Stable endpoint registry identifier assigned to the DATEX II supplier/operator configuration. It scopes upstream identifiers that are only guaranteed unique within one publisher.
- **`measurement_site_id`** (string, required): Stable DATEX II measurement site identifier from measurementSiteReference/@id or measurementSiteRecord/@id. It is the stable identity for fixed traffic measurement equipment and route measurement sites.
- **`feed_url`** (uri, required): Canonical URL of the DATEX II endpoint configuration from which this normalized event was acquired. Used as the CloudEvents source value.
- **`measurement_time`** (datetime, required): ISO 8601 timestamp from measurementTimeDefault or the measuredValue time override. It marks the end or reference instant of the aggregation interval in a MeasuredDataPublication.
- **`measurement_time_key`** (string, required): Key-safe timestamp token derived from measurement_time by replacing characters that are awkward in transport subjects. It preserves the DATEX II measured-time identity component for consumers that need per-sample addressing.
- **`country_code`** (string, required): country code inherited from the endpoint registry. Required for MQTT topic routing and retained in the payload for consumers.
- **`operator_id`** (string, required): operator code inherited from the endpoint registry. Required for MQTT topic routing and retained in the payload for consumers.
- **`road_number`** (string or null, optional): Road identifier associated with the measurement site, copied from the reference table when available.
- **`average_speed_kmh`** (double or null, optional): Average vehicle speed in kilometres per hour from TrafficSpeed/averageVehicleSpeed/speed. Null when the site reports flow or occupancy but not speed.
- **`vehicle_flow_rate_veh_per_hour`** (int32 or null, optional): Vehicle flow rate in vehicles per hour from TrafficFlow/vehicleFlowRate. Null when no flow observation is present for this site in the current publication.
- **`occupancy_percent`** (double or null, optional): Traffic occupancy percentage from TrafficConcentration/occupancy or profile-specific occupancy elements. Null when the upstream publication omits occupancy.
- **`travel_time_seconds`** (double or null, optional): Measured travel time over a route section in seconds from TravelTimeData/travelTime or equivalent route measurement. Null for point sensors.
- **`free_flow_travel_time_seconds`** (double or null, optional): Reference or free-flow travel time in seconds for route measurements when supplied by the DATEX II profile. Consumers compare measured travel_time_seconds with this value to derive delay.
- **`input_value_count`** (int32 or null, optional): Number of input samples used to compute the aggregate, from numberOfInputValuesUsed. Null when the profile does not disclose sample count.
- **`quality_status`** (string or null, optional): DATEX II or supplier-specific quality flag for the measurement value, such as reliable, unreliable, invalid, suspect, or unavailable.
- **`vehicle_type`** (string or null, optional): Vehicle class to which the measurement applies when the upstream profile splits values by vehicle type; null means all vehicles or unspecified.
- **`lane`** (string or null, optional): Lane or carriageway qualifier to which the measured value applies when the feed reports lane-specific measurements.
- **`raw_measurements`** (string or null, optional): Compact JSON/text preservation of additional measuredValue entries not normalized into the common speed, flow, occupancy, or travel-time fields. Used to remain lossless for DATEX II profile variations while keeping the primary analytics columns stable.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "supplier_id": "string",
  "measurement_site_id": "string",
  "feed_url": "string",
  "measurement_time": "2024-01-01T00:00:00Z",
  "measurement_time_key": "string",
  "country_code": "string",
  "operator_id": "string",
  "road_number": "string",
  "average_speed_kmh": 0,
  "vehicle_flow_rate_veh_per_hour": 0,
  "occupancy_percent": 0,
  "travel_time_seconds": 0,
  "free_flow_travel_time_seconds": 0,
  "input_value_count": 0,
  "quality_status": "string",
  "vehicle_type": "string",
  "lane": "string",
  "raw_measurements": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Situation Record

CloudEvents type: `org.datex2.situation.SituationRecord`

#### What it tells you

Incident, roadwork, obstruction, abnormal traffic, weather, or management record from a DATEX II SituationPublication. Normalized situation record from a DATEX II SituationPublication. It represents incidents, accidents, roadworks, abnormal traffic, obstructions, weather impacts, and network-management measures with stable situation and record identifiers.

#### Identity

Each event identifies the real-world resource with `{supplier_id}/{situation_record_id}`. `{supplier_id}` is stable endpoint registry identifier assigned to the DATEX II supplier/operator configuration; `{situation_record_id}` is stable DATEX II situationRecord identifier from situationRecord/@id. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `datex2`, key `{supplier_id}/{situation_record_id}` |
| `MQTT/5.0` | topic `traffic/{country_code}/{operator_id}/datex2/situations/{supplier_id}/{situation_record_id}/record`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `broker-configured node`, message subject `{supplier_id}/{situation_record_id}` |

#### Payload

`Situation Record` payloads are JSON object. Required fields: `supplier_id`, `situation_id`, `situation_record_id`, `feed_url`, `record_type`, `country_code`, `operator_id`.

- **`supplier_id`** (string, required): Stable endpoint registry identifier assigned to the DATEX II supplier/operator configuration. It scopes upstream identifiers that are only guaranteed unique within one publisher.
- **`situation_id`** (string, required): Stable DATEX II situation identifier from situation/@id. Multiple situation records can belong to the same situation container.
- **`situation_record_id`** (string, required): Stable DATEX II situationRecord identifier from situationRecord/@id. It identifies the specific incident, roadwork, obstruction, or network-management record across publication updates.
- **`feed_url`** (uri, required): Canonical URL of the DATEX II endpoint configuration from which this normalized event was acquired. Used as the CloudEvents source value.
- **`version`** (string or null, optional): DATEX II version of the situation or situationRecord from @version. Re-emission happens when this value or the record update timestamp changes.
- **`record_type`** (string, required): DATEX II situation record xsi:type or element local name, such as Accident, AbnormalTraffic, ConstructionWorks, MaintenanceWorks, EnvironmentalObstruction, GeneralObstruction, VehicleObstruction, RoadOrCarriagewayOrLaneManagement, GeneralNetworkManagement, ReroutingManagement, SpeedManagement, or WeatherRelatedRoadConditions.
- **`severity`** (string or null, optional): Overall severity or impact from overallSeverity. Documented DATEX II values include low, medium, high, highest, and unknown depending on profile version.
- **`probability`** (string or null, optional): Probability of occurrence from probabilityOfOccurrence, such as certain, probable, or riskOf.
- **`validity_status`** (string or null, optional): Validity status from validity/validityStatus, for example active, suspended, definedByValidityTimeSpec, or planned.
- **`creation_time`** (datetime or null, optional): ISO 8601 creation timestamp from situationRecordCreationTime. It identifies when the supplier first created this situation record.
- **`observation_time`** (datetime or null, optional): ISO 8601 observation or last-update timestamp from situationRecordObservationTime or equivalent profile fields.
- **`overall_start_time`** (datetime or null, optional): ISO 8601 validity start time from overallStartTime or validityTimeSpecification/overallStartTime.
- **`overall_end_time`** (datetime or null, optional): ISO 8601 validity end time from overallEndTime. Null for open-ended, active, or not-yet-estimated situations.
- **`latitude`** (double or null, optional): WGS84 latitude in decimal degrees from pointCoordinates/latitude when the situation has a point location.
- **`longitude`** (double or null, optional): WGS84 longitude in decimal degrees from pointCoordinates/longitude when the situation has a point location.
- **`road_number`** (string or null, optional): Road identifier from linearElement/roadNumber, roadName, or TPEG linkName descriptors.
- **`direction`** (string or null, optional): Affected direction from tpegDirection, directionBound, or profile-specific direction values such as positive, negative, bothWays, clockwise, or anticlockwise.
- **`location_description`** (string or null, optional): Human-readable location text from generalPublicComment with locationDescriptor, AlertC descriptors, TPEG descriptors, or supplier-specific comments.
- **`description`** (string or null, optional): Human-readable public description/comment for the situation record. This is useful for operator displays but is not stable identity.
- **`source_name`** (string or null, optional): Supplier or source organization name from source/sourceIdentification, sourceName, or the endpoint registry.
- **`cause`** (string or null, optional): DATEX II cause, causeType, or profile-specific cause label associated with the situation, when supplied.
- **`management_type`** (string or null, optional): Network-management action for management records such as temporary closure, speed management, lane management, rerouting, roadworks, or operator action.
- **`raw_record`** (string or null, optional): Compact XML/text snapshot of selected additional DATEX II fields that are not part of the common normalized situation shape. This preserves profile-specific details during the first generalized feeder build without losing bespoke NDW/French data.
- **`country_code`** (string, required): ISO 3166-1 alpha-2 country code from the endpoint registry, used in MQTT UNS topics and regional filtering. Required for MQTT topic routing and retained in the payload for consumers.
- **`operator_id`** (string, required): Operator or road authority code from the endpoint registry, such as NDW, Bison Futé, Trafikverket, National Highways, Statens vegvesen, or CITA. Required for MQTT topic routing and retained in the payload for consumers.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "supplier_id": "string",
  "situation_id": "string",
  "situation_record_id": "string",
  "feed_url": "string",
  "version": "string",
  "record_type": "string",
  "severity": "string",
  "probability": "string",
  "validity_status": "string",
  "creation_time": "2024-01-01T00:00:00Z",
  "observation_time": "2024-01-01T00:00:00Z",
  "overall_start_time": "2024-01-01T00:00:00Z",
  "overall_end_time": "2024-01-01T00:00:00Z",
  "latitude": 0,
  "longitude": 0,
  "road_number": "string",
  "direction": "string",
  "location_description": "string",
  "description": "string",
  "source_name": "string",
  "cause": "string",
  "management_type": "string",
  "raw_record": "string",
  "country_code": "string",
  "operator_id": "string"
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

- xRegistry manifest: [`xreg/datex2.xreg.json`](xreg/datex2.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- ![Deploy Service Bus AMQP: <https://aka.ms/deploytoazurebutton>
