# DATEX II feeder Events

DATEX II publishes traffic situations, traffic measurements, and measurement-site reference records from configurable European road-traffic XML endpoints.

## Measurement Site

CloudEvents type: `org.datex2.measured.MeasurementSite`

Subject and Kafka key template: `{supplier_id}/{measurement_site_id}`

Reference measurement-site record from a DATEX II MeasurementSiteTablePublication.

Reference event describing a DATEX II MeasurementSiteTablePublication measurement site. It contextualizes MeasuredDataPublication traffic observations with site identity, location, equipment, and lane metadata.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `supplier_id` | `string` | yes | Stable endpoint registry identifier assigned to the DATEX II supplier/operator configuration. It scopes upstream identifiers that are only guaranteed unique within one publisher. |
| `measurement_site_id` | `string` | yes | Stable DATEX II measurement site identifier from measurementSiteReference/@id or measurementSiteRecord/@id. It is the stable identity for fixed traffic measurement equipment and route measurement sites. |
| `feed_url` | `uri` | yes | Canonical URL of the DATEX II endpoint configuration from which this normalized event was acquired. Used as the CloudEvents source value. |
| `country_code` | `string` | yes | ISO 3166-1 alpha-2 country code from the endpoint registry, used for regional routing and filtering when the upstream feed covers a national road authority. Required for MQTT topic routing and retained in the payload for consumers. |
| `operator_id` | `string` | yes | operator or road authority code from the endpoint registry, such as NDW, Bison Futé, Trafikverket, National Highways, Statens vegvesen, or CITA. Required for MQTT topic routing and retained in the payload for consumers. |
| `name` | `string / null` | no | Human-readable measurement site name from measurementSiteName or an equivalent DATEX II location label. It is descriptive only and never used as a key. |
| `measurement_site_type` | `string / null` | no | DATEX II equipment or measurement-site type such as inductionLoop, microwave, floatingCar, Bluetooth, or routeSection. Values come from measurementEquipmentTypeUsed or the site table profile. |
| `period_seconds` | `int32 / null` | no | Nominal aggregation period in seconds from measurementSpecificCharacteristics/period. Consumers use it to interpret flow, speed, and occupancy observations. |
| `latitude` | `double / null` | no | WGS84 latitude in decimal degrees from pointByCoordinates/pointCoordinates/latitude. Null when the site table omits coordinates. |
| `longitude` | `double / null` | no | WGS84 longitude in decimal degrees from pointByCoordinates/pointCoordinates/longitude. Null when the site table omits coordinates. |
| `road_number` | `string / null` | no | Road or route identifier from roadInformation/roadName, roadNumber, or a TPEG linkName descriptor, for example A10, N205, M25, or E411. |
| `carriageway` | `string / null` | no | DATEX II carriageway classification affected or measured, such as mainCarriageway, entrySlipRoad, exitSlipRoad, or connectingCarriageway. |
| `lane` | `string / null` | no | DATEX II lane classification when a measurement site is lane-specific, such as lane1, lane2, busLane, hardShoulder, or allLanesCompleteCarriageway. |
| `specific_measurements` | `string / null` | no | Compact JSON/text summary of measurementSpecificCharacteristics entries when the upstream site table exposes multiple per-lane or per-vehicle-class measurements. Preserved so bespoke NDW measurement-site detail can be represented without dropping profile-specific metadata. |

## Traffic Measurement

CloudEvents type: `org.datex2.measured.TrafficMeasurement`

Subject and Kafka key template: `{supplier_id}/{measurement_site_id}`

Traffic speed, flow, occupancy, or travel-time observation from a DATEX II MeasuredDataPublication.

Normalized traffic measurement from a DATEX II MeasuredDataPublication. The schema covers point and route observations emitted by NDW and Bison Futé including speed, flow, occupancy, and travel time.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `supplier_id` | `string` | yes | Stable endpoint registry identifier assigned to the DATEX II supplier/operator configuration. It scopes upstream identifiers that are only guaranteed unique within one publisher. |
| `measurement_site_id` | `string` | yes | Stable DATEX II measurement site identifier from measurementSiteReference/@id or measurementSiteRecord/@id. It is the stable identity for fixed traffic measurement equipment and route measurement sites. |
| `feed_url` | `uri` | yes | Canonical URL of the DATEX II endpoint configuration from which this normalized event was acquired. Used as the CloudEvents source value. |
| `measurement_time` | `datetime` | yes | ISO 8601 timestamp from measurementTimeDefault or the measuredValue time override. It marks the end or reference instant of the aggregation interval in a MeasuredDataPublication. |
| `measurement_time_key` | `string` | yes | Key-safe timestamp token derived from measurement_time by replacing characters that are awkward in transport subjects. It preserves the DATEX II measured-time identity component for consumers that need per-sample addressing. |
| `country_code` | `string` | yes | country code inherited from the endpoint registry. Required for MQTT topic routing and retained in the payload for consumers. |
| `operator_id` | `string` | yes | operator code inherited from the endpoint registry. Required for MQTT topic routing and retained in the payload for consumers. |
| `road_number` | `string / null` | no | Road identifier associated with the measurement site, copied from the reference table when available. |
| `average_speed_kmh` | `double / null` | no | Average vehicle speed in kilometres per hour from TrafficSpeed/averageVehicleSpeed/speed. Null when the site reports flow or occupancy but not speed. |
| `vehicle_flow_rate_veh_per_hour` | `int32 / null` | no | Vehicle flow rate in vehicles per hour from TrafficFlow/vehicleFlowRate. Null when no flow observation is present for this site in the current publication. |
| `occupancy_percent` | `double / null` | no | Traffic occupancy percentage from TrafficConcentration/occupancy or profile-specific occupancy elements. Null when the upstream publication omits occupancy. |
| `travel_time_seconds` | `double / null` | no | Measured travel time over a route section in seconds from TravelTimeData/travelTime or equivalent route measurement. Null for point sensors. |
| `free_flow_travel_time_seconds` | `double / null` | no | Reference or free-flow travel time in seconds for route measurements when supplied by the DATEX II profile. Consumers compare measured travel_time_seconds with this value to derive delay. |
| `input_value_count` | `int32 / null` | no | Number of input samples used to compute the aggregate, from numberOfInputValuesUsed. Null when the profile does not disclose sample count. |
| `quality_status` | `string / null` | no | DATEX II or supplier-specific quality flag for the measurement value, such as reliable, unreliable, invalid, suspect, or unavailable. |
| `vehicle_type` | `string / null` | no | Vehicle class to which the measurement applies when the upstream profile splits values by vehicle type; null means all vehicles or unspecified. |
| `lane` | `string / null` | no | Lane or carriageway qualifier to which the measured value applies when the feed reports lane-specific measurements. |
| `raw_measurements` | `string / null` | no | Compact JSON/text preservation of additional measuredValue entries not normalized into the common speed, flow, occupancy, or travel-time fields. Used to remain lossless for DATEX II profile variations while keeping the primary analytics columns stable. |

## Situation Record

CloudEvents type: `org.datex2.situation.SituationRecord`

Subject and Kafka key template: `{supplier_id}/{situation_record_id}`

Incident, roadwork, obstruction, abnormal traffic, weather, or management record from a DATEX II SituationPublication.

Normalized situation record from a DATEX II SituationPublication. It represents incidents, accidents, roadworks, abnormal traffic, obstructions, weather impacts, and network-management measures with stable situation and record identifiers.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `supplier_id` | `string` | yes | Stable endpoint registry identifier assigned to the DATEX II supplier/operator configuration. It scopes upstream identifiers that are only guaranteed unique within one publisher. |
| `situation_id` | `string` | yes | Stable DATEX II situation identifier from situation/@id. Multiple situation records can belong to the same situation container. |
| `situation_record_id` | `string` | yes | Stable DATEX II situationRecord identifier from situationRecord/@id. It identifies the specific incident, roadwork, obstruction, or network-management record across publication updates. |
| `feed_url` | `uri` | yes | Canonical URL of the DATEX II endpoint configuration from which this normalized event was acquired. Used as the CloudEvents source value. |
| `version` | `string / null` | no | DATEX II version of the situation or situationRecord from @version. Re-emission happens when this value or the record update timestamp changes. |
| `record_type` | `string` | yes | DATEX II situation record xsi:type or element local name, such as Accident, AbnormalTraffic, ConstructionWorks, MaintenanceWorks, EnvironmentalObstruction, GeneralObstruction, VehicleObstruction, RoadOrCarriagewayOrLaneManagement, GeneralNetworkManagement, ReroutingManagement, SpeedManagement, or WeatherRelatedRoadConditions. |
| `severity` | `string / null` | no | Overall severity or impact from overallSeverity. Documented DATEX II values include low, medium, high, highest, and unknown depending on profile version. |
| `probability` | `string / null` | no | Probability of occurrence from probabilityOfOccurrence, such as certain, probable, or riskOf. |
| `validity_status` | `string / null` | no | Validity status from validity/validityStatus, for example active, suspended, definedByValidityTimeSpec, or planned. |
| `creation_time` | `datetime / null` | no | ISO 8601 creation timestamp from situationRecordCreationTime. It identifies when the supplier first created this situation record. |
| `observation_time` | `datetime / null` | no | ISO 8601 observation or last-update timestamp from situationRecordObservationTime or equivalent profile fields. |
| `overall_start_time` | `datetime / null` | no | ISO 8601 validity start time from overallStartTime or validityTimeSpecification/overallStartTime. |
| `overall_end_time` | `datetime / null` | no | ISO 8601 validity end time from overallEndTime. Null for open-ended, active, or not-yet-estimated situations. |
| `latitude` | `double / null` | no | WGS84 latitude in decimal degrees from pointCoordinates/latitude when the situation has a point location. |
| `longitude` | `double / null` | no | WGS84 longitude in decimal degrees from pointCoordinates/longitude when the situation has a point location. |
| `road_number` | `string / null` | no | Road identifier from linearElement/roadNumber, roadName, or TPEG linkName descriptors. |
| `direction` | `string / null` | no | Affected direction from tpegDirection, directionBound, or profile-specific direction values such as positive, negative, bothWays, clockwise, or anticlockwise. |
| `location_description` | `string / null` | no | Human-readable location text from generalPublicComment with locationDescriptor, AlertC descriptors, TPEG descriptors, or supplier-specific comments. |
| `description` | `string / null` | no | Human-readable public description/comment for the situation record. This is useful for operator displays but is not stable identity. |
| `source_name` | `string / null` | no | Supplier or source organization name from source/sourceIdentification, sourceName, or the endpoint registry. |
| `cause` | `string / null` | no | DATEX II cause, causeType, or profile-specific cause label associated with the situation, when supplied. |
| `management_type` | `string / null` | no | Network-management action for management records such as temporary closure, speed management, lane management, rerouting, roadworks, or operator action. |
| `raw_record` | `string / null` | no | Compact XML/text snapshot of selected additional DATEX II fields that are not part of the common normalized situation shape. This preserves profile-specific details during the first generalized feeder build without losing bespoke NDW/French data. |
| `country_code` | `string` | yes | ISO 3166-1 alpha-2 country code from the endpoint registry, used in MQTT UNS topics and regional filtering. Required for MQTT topic routing and retained in the payload for consumers. |
| `operator_id` | `string` | yes | Operator or road authority code from the endpoint registry, such as NDW, Bison Futé, Trafikverket, National Highways, Statens vegvesen, or CITA. Required for MQTT topic routing and retained in the payload for consumers. |
