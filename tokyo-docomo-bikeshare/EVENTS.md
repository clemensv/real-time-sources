# Tokyo Docomo Bikeshare Bridge Events

This document describes the events emitted by the Tokyo Docomo Bikeshare bridge.

- [JP.ODPT.DocomoBikeshare.System](#message-group-jpopdtdocombikesharesystem)
  - [JP.ODPT.DocomoBikeshare.BikeshareSystem](#message-jpopdtdocombikesharebikesharesystem)
- [JP.ODPT.DocomoBikeshare.Stations](#message-group-jpopdtdocombikesharestations)
  - [JP.ODPT.DocomoBikeshare.BikeshareStation](#message-jpopdtdocombikesharebikesharestation)
  - [JP.ODPT.DocomoBikeshare.BikeshareStationStatus](#message-jpopdtdocombikesharebikesharestationstatus)

---

## Message Group: JP.ODPT.DocomoBikeshare.System

Kafka endpoint: topic `tokyo-docomo-bikeshare`, key `{system_id}`

---
### Message: JP.ODPT.DocomoBikeshare.BikeshareSystem

#### CloudEvents Attributes:
| **Name** | **Description** | **Type** | **Required** | **Value** |
|---|---|---|---|---|
| `type` | | `` | `False` | `JP.ODPT.DocomoBikeshare.BikeshareSystem` |
| `source` | | `` | `False` | `https://api-public.odpt.org/api/v4/gbfs/docomo-cycle-tokyo` |
| `subject` | | `uritemplate` | `False` | `{system_id}` |

#### Schema:
##### Object: BikeshareSystem
*Metadata describing the Tokyo Docomo Bikeshare system, sourced from the GBFS 2.3 system_information.json feed published by the Open Data Platform for Transportation (ODPT).*

| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|---|---|---|---|---|
| `system_id` | *string* | - | `True` | Unique identifier for this bikeshare system. A short, URL-friendly identifier that does not contain spaces, for example 'docomo-cycle-tokyo'. This value is stable and matches the GBFS feed directory name on the ODPT platform. |
| `language` | *string* | - | `True` | A single IETF BCP 47 language identifier representing the primary language used in this feed, for example 'ja' for Japanese or 'en' for English. |
| `name` | *string* | - | `True` | Full name of the bikeshare system as displayed to customers, for example 'ドコモ・バイクシェア' or 'Docomo Bikeshare'. |
| `short_name` | *string* (optional) | - | `False` | Optional abbreviation or short form of the system name, for example 'DocomoBike'. |
| `operator` | *string* (optional) | - | `False` | Name of the company or organization that operates the bikeshare system, for example 'NTT Docomo, Inc.'. |
| `url` | *string* (optional) | - | `False` | URL of the bikeshare system or operator website for end users, for example 'https://docomo-cycle.jp/'. |
| `purchase_url` | *string* (optional) | - | `False` | URL where a customer can purchase a membership or learn about purchasing memberships for this bikeshare system. |
| `start_date` | *string* (optional) | - | `False` | Date that the bikeshare system began operations, formatted as YYYY-MM-DD in accordance with ISO 8601. |
| `phone_number` | *string* (optional) | - | `False` | A single voice telephone number for the customer service department of this bikeshare system, including country and area code. |
| `email` | *string* (optional) | - | `False` | A single contact email address actively monitored by the operator's customer service department. |
| `feed_contact_email` | *string* (optional) | - | `False` | A single contact email address for the purpose of reporting issues with the GBFS feed for this system. |
| `timezone` | *string* | - | `True` | The IANA time zone database name for the time zone where the system is located, for example 'Asia/Tokyo'. |
| `license_url` | *string* (optional) | - | `False` | A fully qualified URL of a page that defines the license terms for the GBFS data published by this system. |

---

## Message Group: JP.ODPT.DocomoBikeshare.Stations

Kafka endpoint: topic `tokyo-docomo-bikeshare`, key `{system_id}/{station_id}`

---
### Message: JP.ODPT.DocomoBikeshare.BikeshareStation

#### CloudEvents Attributes:
| **Name** | **Description** | **Type** | **Required** | **Value** |
|---|---|---|---|---|
| `type` | | `` | `False` | `JP.ODPT.DocomoBikeshare.BikeshareStation` |
| `source` | | `` | `False` | `https://api-public.odpt.org/api/v4/gbfs/docomo-cycle-tokyo` |
| `subject` | | `uritemplate` | `False` | `{system_id}/{station_id}` |

#### Schema:
##### Object: BikeshareStation
*Physical location and static attributes of a single Tokyo Docomo Bikeshare docking station, sourced from the GBFS 2.3 station_information.json feed published by the Open Data Platform for Transportation (ODPT).*

| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|---|---|---|---|---|
| `system_id` | *string* | - | `True` | Identifier of the bikeshare system this station belongs to, for example 'docomo-cycle-tokyo'. Included in the payload so that the composite Kafka key {system_id}/{station_id} can be resolved from the event data. |
| `station_id` | *string* | - | `True` | Unique identifier of the station within the GBFS feed, for example '00010137'. Stable across feed updates; used as the second component of the Kafka key. |
| `name` | *string* | - | `True` | Public name of the station as displayed to customers. Tokyo Docomo Bikeshare publishes bilingual names in the format 'Japanese / English', for example 'A4-01.東京駅八重洲口 / Tokyo Station Yaesu'. |
| `short_name` | *string* (optional) | - | `False` | Short name or other operator-assigned identifier for the station, if provided. |
| `lat` | *double* | deg (°) | `True` | WGS 84 latitude of the station in decimal degrees. Positive values indicate north of the equator. |
| `lon` | *double* | deg (°) | `True` | WGS 84 longitude of the station in decimal degrees. Positive values indicate east of the prime meridian. |
| `address` | *string* (optional) | - | `False` | Street address of the station, if provided by the operator. |
| `cross_street` | *string* (optional) | - | `False` | Cross street or nearby landmark of the station location, if provided. |
| `region_id` | *string* (optional) | - | `False` | Identifier of the district or region where the station is located, as defined in the GBFS system_regions.json feed. |
| `post_code` | *string* (optional) | - | `False` | Postal code of the station location, if provided. |
| `capacity` | *int32* (optional) | - | `False` | Total number of docking points installed at the station, including those that are temporarily disabled. Reflects the physical capacity of the station. |
| `is_virtual_station` | *bool* (optional) | - | `False` | If true, the station is a virtual station (i.e., a parking zone without physical docks) rather than a docked station. If absent or false, the station has physical docking points. |

---
### Message: JP.ODPT.DocomoBikeshare.BikeshareStationStatus

#### CloudEvents Attributes:
| **Name** | **Description** | **Type** | **Required** | **Value** |
|---|---|---|---|---|
| `type` | | `` | `False` | `JP.ODPT.DocomoBikeshare.BikeshareStationStatus` |
| `source` | | `` | `False` | `https://api-public.odpt.org/api/v4/gbfs/docomo-cycle-tokyo` |
| `subject` | | `uritemplate` | `False` | `{system_id}/{station_id}` |

#### Schema:
##### Object: BikeshareStationStatus
*Real-time availability and operational status of a single Tokyo Docomo Bikeshare docking station, sourced from the GBFS 2.3 station_status.json feed published by the Open Data Platform for Transportation (ODPT). Updates on a 60-second TTL.*

| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|---|---|---|---|---|
| `system_id` | *string* | - | `True` | Identifier of the bikeshare system this station belongs to, for example 'docomo-cycle-tokyo'. Included in the payload so that the composite Kafka key {system_id}/{station_id} can be resolved from the event data. |
| `station_id` | *string* | - | `True` | Unique identifier of the station within the GBFS feed, for example '00010137'. Matches the station_id in the corresponding BikeshareStation event. |
| `num_bikes_available` | *int32* | - | `True` | Number of functional vehicles (bicycles) physically available for rental at this station at the time of the last update. |
| `num_bikes_disabled` | *int32* (optional) | - | `False` | Number of disabled or broken vehicles at the station that are not available for rental. Absent if the operator does not publish this value. |
| `num_docks_available` | *int32* (optional) | - | `False` | Number of empty and functional docking points at the station where a customer can return a vehicle. Absent if the operator does not publish this value. |
| `num_docks_disabled` | *int32* (optional) | - | `False` | Number of broken or disabled docking points at the station that cannot accept vehicle returns. Absent if the operator does not publish this value. |
| `is_installed` | *bool* | - | `True` | Indicates whether the station infrastructure is installed on-street and operational. A value of false means the station is temporarily or permanently removed from service. |
| `is_renting` | *bool* | - | `True` | Indicates whether the station is currently allowing vehicle rentals. May be false even when bikes are present, for example during a system outage. |
| `is_returning` | *bool* | - | `True` | Indicates whether the station is currently accepting vehicle returns. May be false even when docks are empty, for example during a system outage. |
| `last_reported` | *int64* (optional) | - | `False` | Unix timestamp in seconds (UTC) indicating the last time this station's status was updated by the operator's system. Absent if the operator does not publish this value. |
