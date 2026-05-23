# Table of Contents

- [NO.Kystverket.AIS](#message-group-nokystverketais)
  - [NO.Kystverket.AIS.PositionReportClassA](#message-nokystverketaispositionreportclassa)
  - [NO.Kystverket.AIS.StaticVoyageData](#message-nokystverketaisstaticvoyagedata)
  - [NO.Kystverket.AIS.PositionReportClassB](#message-nokystverketaispositionreportclassb)
  - [NO.Kystverket.AIS.StaticDataClassB](#message-nokystverketaisstaticdataclassb)
  - [NO.Kystverket.AIS.AidToNavigation](#message-nokystverketaisaidtonavigation)
- [NO.Kystverket.AIS.mqtt](#message-group-nokystverketaismqtt)
  - [NO.Kystverket.AIS.mqtt.PositionReport](#message-nokystverketaismqttpositionreport)
  - [NO.Kystverket.AIS.mqtt.ShipStatic](#message-nokystverketaismqttshipstatic)
  - [NO.Kystverket.AIS.mqtt.AidToNavigation](#message-nokystverketaismqttaidtonavigation)

---

## Message Group: NO.Kystverket.AIS
---
### Message: NO.Kystverket.AIS.PositionReportClassA
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `NO.Kystverket.AIS.PositionReportClassA` |
| `source` |  | `` | `False` | `urn:ais:kystverket:tcp` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

#### Schema:
##### Object: PositionReportClassA
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `mmsi` | *int32* | - | `True` |  |
| `navigation_status` | *int32* | - | `False` |  |
| `rate_of_turn` | *double* | - | `False` |  |
| `speed_over_ground` | *double* | - | `False` |  |
| `position_accuracy` | *int32* | - | `False` |  |
| `longitude` | *double* | - | `True` |  |
| `latitude` | *double* | - | `True` |  |
| `course_over_ground` | *double* | - | `False` |  |
| `true_heading` | *int32* | - | `False` |  |
| `timestamp` | *string* | - | `True` |  |
| `station_id` | *string* | - | `False` |  |
| `msg_type` | *int32* | - | `False` |  |
---
### Message: NO.Kystverket.AIS.StaticVoyageData
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `NO.Kystverket.AIS.StaticVoyageData` |
| `source` |  | `` | `False` | `urn:ais:kystverket:tcp` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

#### Schema:
##### Object: StaticVoyageData
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `mmsi` | *int32* | - | `True` |  |
| `imo_number` | *int32* | - | `False` |  |
| `callsign` | *string* | - | `False` |  |
| `ship_name` | *string* | - | `False` |  |
| `ship_type` | *int32* | - | `False` |  |
| `dimension_to_bow` | *int32* | - | `False` |  |
| `dimension_to_stern` | *int32* | - | `False` |  |
| `dimension_to_port` | *int32* | - | `False` |  |
| `dimension_to_starboard` | *int32* | - | `False` |  |
| `draught` | *double* | - | `False` |  |
| `destination` | *string* | - | `False` |  |
| `eta_month` | *int32* | - | `False` |  |
| `eta_day` | *int32* | - | `False` |  |
| `eta_hour` | *int32* | - | `False` |  |
| `eta_minute` | *int32* | - | `False` |  |
| `timestamp` | *string* | - | `True` |  |
| `station_id` | *string* | - | `False` |  |
---
### Message: NO.Kystverket.AIS.PositionReportClassB
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `NO.Kystverket.AIS.PositionReportClassB` |
| `source` |  | `` | `False` | `urn:ais:kystverket:tcp` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

#### Schema:
##### Object: PositionReportClassB
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `mmsi` | *int32* | - | `True` |  |
| `speed_over_ground` | *double* | - | `False` |  |
| `position_accuracy` | *int32* | - | `False` |  |
| `longitude` | *double* | - | `True` |  |
| `latitude` | *double* | - | `True` |  |
| `course_over_ground` | *double* | - | `False` |  |
| `true_heading` | *int32* | - | `False` |  |
| `timestamp` | *string* | - | `True` |  |
| `station_id` | *string* | - | `False` |  |
| `msg_type` | *int32* | - | `False` |  |
---
### Message: NO.Kystverket.AIS.StaticDataClassB
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `NO.Kystverket.AIS.StaticDataClassB` |
| `source` |  | `` | `False` | `urn:ais:kystverket:tcp` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

#### Schema:
##### Object: StaticDataClassB
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `mmsi` | *int32* | - | `True` |  |
| `part_number` | *int32* | - | `False` |  |
| `ship_name` | *string* | - | `False` |  |
| `ship_type` | *int32* | - | `False` |  |
| `callsign` | *string* | - | `False` |  |
| `dimension_to_bow` | *int32* | - | `False` |  |
| `dimension_to_stern` | *int32* | - | `False` |  |
| `dimension_to_port` | *int32* | - | `False` |  |
| `dimension_to_starboard` | *int32* | - | `False` |  |
| `timestamp` | *string* | - | `True` |  |
| `station_id` | *string* | - | `False` |  |
---
### Message: NO.Kystverket.AIS.AidToNavigation
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `NO.Kystverket.AIS.AidToNavigation` |
| `source` |  | `` | `False` | `urn:ais:kystverket:tcp` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

#### Schema:
##### Object: AidToNavigation
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `mmsi` | *int32* | - | `True` |  |
| `aid_type` | *int32* | - | `False` |  |
| `name` | *string* | - | `False` |  |
| `position_accuracy` | *int32* | - | `False` |  |
| `longitude` | *double* | - | `True` |  |
| `latitude` | *double* | - | `True` |  |
| `timestamp` | *string* | - | `True` |  |
| `station_id` | *string* | - | `False` |  |
## Message Group: NO.Kystverket.AIS.mqtt
---
### Message: NO.Kystverket.AIS.mqtt.PositionReport
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `NO.Kystverket.AIS.mqtt.PositionReport` |
| `source` |  | `` | `False` | `tcp://153.44.253.27:5631` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

#### Schema:
##### Object: PositionReport
*AIS position report (Type 1/2/3/18/19) projected onto the UNS axes.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `mmsi` | *string* | - | `True` | Source MMSI as a 9-digit ASCII string (padded with leading zeros). Used as the UNS topic '{mmsi}' placeholder and as the CloudEvents subject. |
| `flag` | *string* | - | `True` | ISO-3166-1 alpha-2 country code (lower-case) derived from the first three digits of the MMSI via the ITU MID (Maritime Identification Digit) registry. 'xx' is used for MIDs that do not map to a country. |
| `ship_type` | *string* | - | `True` | Kebab-case ship-type bucket derived from the ITU-R M.1371 ShipType code. For static reports it is derived from the broadcast Type-5/24 ShipType field; for position reports it is looked up from an in-process ship-type cache keyed by MMSI. 'unknown' if no static report has been observed yet. |
| `geohash5` | *string* | - | `True` | 5-character geohash of the reported (latitude, longitude). Approx. 4.9 km x 4.9 km cells at the equator. For messages without a position, filled from the most recently observed position for the MMSI, falling back to '00000'. |
| `msg_type` | *string* | - | `True` | Kebab-case event family used as the trailing UNS topic segment. Always equals the segment baked into the message's MQTT topic template. |
| `latitude` | *double* | - | `True` | Reported latitude in WGS-84 decimal degrees. |
| `longitude` | *double* | - | `True` | Reported longitude in WGS-84 decimal degrees. |
| `speed_over_ground` | *double* | - | `False` | Speed over ground in knots. |
| `course_over_ground` | *double* | - | `False` | Course over ground in degrees (0..359.9). |
| `true_heading` | *int32* | - | `False` | True heading in degrees (0..359, 511 = not available). |
| `navigation_status` | *int32* | - | `False` | ITU navigation status code (0..15). 0 for Class-B. |
| `rate_of_turn` | *double* | - | `False` | Rate of turn in AIS-encoded units. 0 for Class-B. |
| `position_accuracy` | *int32* | - | `False` | 1 if high-accuracy (DGPS), else 0. |
| `timestamp` | *string* | - | `False` | ISO-8601 receive time as supplied by the upstream NMEA tag. |
| `station_id` | *string* | - | `False` | Kystverket base-station identifier from the NMEA tag block. |
| `ais_msg_type` | *int32* | - | `True` | Original ITU-R M.1371 message ID (1, 2, 3, 18, or 19). |
---
### Message: NO.Kystverket.AIS.mqtt.ShipStatic
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `NO.Kystverket.AIS.mqtt.ShipStatic` |
| `source` |  | `` | `False` | `tcp://153.44.253.27:5631` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

#### Schema:
##### Object: ShipStatic
*AIS static and voyage-related data (Type 5 / Type 24) projected onto the UNS axes.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `mmsi` | *string* | - | `True` | Source MMSI as a 9-digit ASCII string (padded with leading zeros). Used as the UNS topic '{mmsi}' placeholder and as the CloudEvents subject. |
| `flag` | *string* | - | `True` | ISO-3166-1 alpha-2 country code (lower-case) derived from the first three digits of the MMSI via the ITU MID (Maritime Identification Digit) registry. 'xx' is used for MIDs that do not map to a country. |
| `ship_type` | *string* | - | `True` | Kebab-case ship-type bucket derived from the ITU-R M.1371 ShipType code. For static reports it is derived from the broadcast Type-5/24 ShipType field; for position reports it is looked up from an in-process ship-type cache keyed by MMSI. 'unknown' if no static report has been observed yet. |
| `geohash5` | *string* | - | `True` | 5-character geohash of the reported (latitude, longitude). Approx. 4.9 km x 4.9 km cells at the equator. For messages without a position, filled from the most recently observed position for the MMSI, falling back to '00000'. |
| `msg_type` | *string* | - | `True` | Kebab-case event family used as the trailing UNS topic segment. Always equals the segment baked into the message's MQTT topic template. |
| `ship_name` | *string* | - | `False` | Vessel name as broadcast (max 20 chars, trimmed). |
| `callsign` | *string* | - | `False` | Radio call sign as broadcast (max 7 chars). |
| `imo_number` | *int32* | - | `False` | IMO number (7-digit). 0 if not assigned or for Class-B. |
| `ship_type_code` | *int32* | - | `True` | Raw ITU-R M.1371 ship type code (0..99). |
| `destination` | *string* | - | `False` | Voyage destination string (max 20 chars). Empty for Type 24. |
| `eta` | *string* | - | `False` | Voyage ETA as ISO-8601 string. Empty if absent (Type 24). |
| `draught` | *double* | - | `False` | Maximum present static draught in metres. 0.0 if absent. |
| `dim_to_bow` | *int32* | - | `False` | Distance from reference point to bow in metres. |
| `dim_to_stern` | *int32* | - | `False` | Distance from reference point to stern in metres. |
| `dim_to_port` | *int32* | - | `False` | Distance from reference point to port side in metres. |
| `dim_to_starboard` | *int32* | - | `False` | Distance from reference point to starboard side in metres. |
| `timestamp` | *string* | - | `False` | ISO-8601 receive time as supplied by the upstream NMEA tag. |
| `station_id` | *string* | - | `False` | Kystverket base-station identifier. |
| `ais_msg_type` | *int32* | - | `True` | Original ITU-R M.1371 message ID (5 or 24). |
---
### Message: NO.Kystverket.AIS.mqtt.AidToNavigation
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `NO.Kystverket.AIS.mqtt.AidToNavigation` |
| `source` |  | `` | `False` | `tcp://153.44.253.27:5631` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

#### Schema:
##### Object: AidToNavigation
*Aid-to-Navigation report (Type 21) projected onto the UNS axes.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `mmsi` | *string* | - | `True` | Source MMSI as a 9-digit ASCII string (padded with leading zeros). Used as the UNS topic '{mmsi}' placeholder and as the CloudEvents subject. |
| `flag` | *string* | - | `True` | ISO-3166-1 alpha-2 country code (lower-case) derived from the first three digits of the MMSI via the ITU MID (Maritime Identification Digit) registry. 'xx' is used for MIDs that do not map to a country. |
| `ship_type` | *string* | - | `True` | Kebab-case ship-type bucket derived from the ITU-R M.1371 ShipType code. For static reports it is derived from the broadcast Type-5/24 ShipType field; for position reports it is looked up from an in-process ship-type cache keyed by MMSI. 'unknown' if no static report has been observed yet. |
| `geohash5` | *string* | - | `True` | 5-character geohash of the reported (latitude, longitude). Approx. 4.9 km x 4.9 km cells at the equator. For messages without a position, filled from the most recently observed position for the MMSI, falling back to '00000'. |
| `msg_type` | *string* | - | `True` | Kebab-case event family used as the trailing UNS topic segment. Always equals the segment baked into the message's MQTT topic template. |
| `name` | *string* | - | `False` | Aid-to-Navigation name as broadcast. |
| `aid_type` | *int32* | - | `True` | AtoN type code (0..31) per ITU-R M.1371. |
| `latitude` | *double* | - | `True` | Reported latitude in WGS-84 decimal degrees. |
| `longitude` | *double* | - | `True` | Reported longitude in WGS-84 decimal degrees. |
| `position_accuracy` | *int32* | - | `False` | 1 if high-accuracy (DGPS), else 0. |
| `timestamp` | *string* | - | `False` | ISO-8601 receive time as supplied by the upstream NMEA tag. |
| `station_id` | *string* | - | `False` | Kystverket base-station identifier. |
| `ais_msg_type` | *int32* | - | `True` | Original ITU-R M.1371 message ID (21). |
