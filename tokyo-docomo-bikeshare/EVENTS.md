# Tokyo Docomo Bikeshare Events

Real-time bikeshare data for **Tokyo Docomo Bikeshare** (ドコモ・バイクシェア), Japan's largest bikeshare network with 1,794 dock-based stations across the central wards of Tokyo (Chiyoda, Minato, Shibuya, Shinjuku, and others).

## Table of Contents

- [Registry](#registry)
- [Endpoints](#endpoints)
- [Messagegroups](#messagegroups)
- [Schemagroups](#schemagroups)

---

## Registry

| Field | Value |
| --- | --- |
| Endpoints | 2 |
| Messagegroups | 2 |
| Schemagroups | 1 |

## Endpoints

### Endpoint `JP.ODPT.DocomoBikeshare.System.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`JP.ODPT.DocomoBikeshare.System`](#messagegroup-jpodptdocomobikesharesystem) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `tokyo-docomo-bikeshare` |
| Kafka key | `{system_id}` |
| Deployed | False |

### Endpoint `JP.ODPT.DocomoBikeshare.Stations.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`JP.ODPT.DocomoBikeshare.Stations`](#messagegroup-jpodptdocomobikesharestations) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `tokyo-docomo-bikeshare` |
| Kafka key | `{system_id}/{station_id}` |
| Deployed | False |

## Messagegroups

### Messagegroup `JP.ODPT.DocomoBikeshare.System`
<a id="messagegroup-jpodptdocomobikesharesystem"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `JP.ODPT.DocomoBikeshare.System.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `JP.ODPT.DocomoBikeshare.BikeshareSystem`
<a id="message-jpodptdocomobikesharebikesharesystem"></a>

| Field | Value |
| --- | --- |
| Name | BikeshareSystem |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/JP.ODPT.DocomoBikeshare.jstruct/schemas/JP.ODPT.DocomoBikeshare.BikeshareSystem`](#schema-jpodptdocomobikesharebikesharesystem) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `JP.ODPT.DocomoBikeshare.BikeshareSystem` |
| `source` |  | `string` | `False` | `https://api-public.odpt.org/api/v4/gbfs/docomo-cycle-tokyo` |
| `subject` |  | `uritemplate` | `False` | `{system_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `JP.ODPT.DocomoBikeshare.System.Kafka` | `KAFKA` | topic `tokyo-docomo-bikeshare`; key `{system_id}` |

### Messagegroup `JP.ODPT.DocomoBikeshare.Stations`
<a id="messagegroup-jpodptdocomobikesharestations"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `JP.ODPT.DocomoBikeshare.Stations.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `JP.ODPT.DocomoBikeshare.BikeshareStation`
<a id="message-jpodptdocomobikesharebikesharestation"></a>

| Field | Value |
| --- | --- |
| Name | BikeshareStation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/JP.ODPT.DocomoBikeshare.jstruct/schemas/JP.ODPT.DocomoBikeshare.BikeshareStation`](#schema-jpodptdocomobikesharebikesharestation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `JP.ODPT.DocomoBikeshare.BikeshareStation` |
| `source` |  | `string` | `False` | `https://api-public.odpt.org/api/v4/gbfs/docomo-cycle-tokyo` |
| `subject` |  | `uritemplate` | `False` | `{system_id}/{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `JP.ODPT.DocomoBikeshare.Stations.Kafka` | `KAFKA` | topic `tokyo-docomo-bikeshare`; key `{system_id}/{station_id}` |

#### Message `JP.ODPT.DocomoBikeshare.BikeshareStationStatus`
<a id="message-jpodptdocomobikesharebikesharestationstatus"></a>

| Field | Value |
| --- | --- |
| Name | BikeshareStationStatus |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/JP.ODPT.DocomoBikeshare.jstruct/schemas/JP.ODPT.DocomoBikeshare.BikeshareStationStatus`](#schema-jpodptdocomobikesharebikesharestationstatus) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `JP.ODPT.DocomoBikeshare.BikeshareStationStatus` |
| `source` |  | `string` | `False` | `https://api-public.odpt.org/api/v4/gbfs/docomo-cycle-tokyo` |
| `subject` |  | `uritemplate` | `False` | `{system_id}/{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `JP.ODPT.DocomoBikeshare.Stations.Kafka` | `KAFKA` | topic `tokyo-docomo-bikeshare`; key `{system_id}/{station_id}` |

## Schemagroups

### Schemagroup `JP.ODPT.DocomoBikeshare.jstruct`
<a id="schemagroup-jpodptdocomobikesharejstruct"></a>

#### Schema `JP.ODPT.DocomoBikeshare.BikeshareSystem`
<a id="schema-jpodptdocomobikesharebikesharesystem"></a>

| Field | Value |
| --- | --- |
| Name | BikeshareSystem |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://real-time-sources.2030.io/schemas/jp/odpt/docomobikeshare/BikeshareSystem` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `BikeshareSystem`
<a id="schema-node-bikesharesystem"></a>

Metadata describing the Tokyo Docomo Bikeshare system, sourced from the GBFS 2.3 system_information.json feed published by the Open Data Platform for Transportation (ODPT).

| Field | Value |
| --- | --- |
| $id | `https://real-time-sources.2030.io/schemas/jp/odpt/docomobikeshare/BikeshareSystem` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `system_id` | `string` | `True` | Unique identifier for this bikeshare system. A short, URL-friendly identifier that does not contain spaces, for example 'docomo-cycle-tokyo'. This value is stable and matches the GBFS feed directory name on the ODPT platform. | - | - | - |
| `language` | `string` | `True` | A single IETF BCP 47 language identifier representing the primary language used in this feed, for example 'ja' for Japanese or 'en' for English. | - | - | - |
| `name` | `string` | `True` | Full name of the bikeshare system as displayed to customers, for example 'ドコモ・バイクシェア' or 'Docomo Bikeshare'. | - | - | - |
| `short_name` | `union` | `False` | Optional abbreviation or short form of the system name, for example 'DocomoBike'. | - | - | - |
| `operator` | `union` | `False` | Name of the company or organization that operates the bikeshare system, for example 'NTT Docomo, Inc.'. | - | - | - |
| `url` | `union` | `False` | URL of the bikeshare system or operator website for end users, for example 'https://docomo-cycle.jp/'. | - | - | - |
| `purchase_url` | `union` | `False` | URL where a customer can purchase a membership or learn about purchasing memberships for this bikeshare system. | - | - | - |
| `start_date` | `union` | `False` | Date that the bikeshare system began operations, formatted as YYYY-MM-DD in accordance with ISO 8601. | - | - | - |
| `phone_number` | `union` | `False` | A single voice telephone number for the customer service department of this bikeshare system, including country and area code. | - | - | - |
| `email` | `union` | `False` | A single contact email address actively monitored by the operator's customer service department. | - | - | - |
| `feed_contact_email` | `union` | `False` | A single contact email address for the purpose of reporting issues with the GBFS feed for this system. | - | - | - |
| `timezone` | `string` | `True` | The IANA time zone database name for the time zone where the system is located, for example 'Asia/Tokyo'. | - | - | - |
| `license_url` | `union` | `False` | A fully qualified URL of a page that defines the license terms for the GBFS data published by this system. | - | - | - |

#### Schema `JP.ODPT.DocomoBikeshare.BikeshareStation`
<a id="schema-jpodptdocomobikesharebikesharestation"></a>

| Field | Value |
| --- | --- |
| Name | BikeshareStation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://real-time-sources.2030.io/schemas/jp/odpt/docomobikeshare/BikeshareStation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `BikeshareStation`
<a id="schema-node-bikesharestation"></a>

Physical location and static attributes of a single Tokyo Docomo Bikeshare docking station, sourced from the GBFS 2.3 station_information.json feed published by the Open Data Platform for Transportation (ODPT).

| Field | Value |
| --- | --- |
| $id | `https://real-time-sources.2030.io/schemas/jp/odpt/docomobikeshare/BikeshareStation` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `system_id` | `string` | `True` | Identifier of the bikeshare system this station belongs to, for example 'docomo-cycle-tokyo'. Included in the payload so that the composite Kafka key {system_id}/{station_id} can be resolved from the event data. | - | - | - |
| `station_id` | `string` | `True` | Unique identifier of the station within the GBFS feed, for example '00010137'. Stable across feed updates; used as the second component of the Kafka key. | - | - | - |
| `name` | `string` | `True` | Public name of the station as displayed to customers. Tokyo Docomo Bikeshare publishes bilingual names in the format 'Japanese / English', for example 'A4-01.東京駅八重洲口 / Tokyo Station Yaesu'. | - | - | - |
| `short_name` | `union` | `False` | Short name or other operator-assigned identifier for the station, if provided. | - | - | - |
| `lat` | `double` | `True` | WGS 84 latitude of the station in decimal degrees. Positive values indicate north of the equator. | unit=`deg` symbol=`°` | - | - |
| `lon` | `double` | `True` | WGS 84 longitude of the station in decimal degrees. Positive values indicate east of the prime meridian. | unit=`deg` symbol=`°` | - | - |
| `address` | `union` | `False` | Street address of the station, if provided by the operator. | - | - | - |
| `cross_street` | `union` | `False` | Cross street or nearby landmark of the station location, if provided. | - | - | - |
| `region_id` | `union` | `False` | Identifier of the district or region where the station is located, as defined in the GBFS system_regions.json feed. | - | - | - |
| `post_code` | `union` | `False` | Postal code of the station location, if provided. | - | - | - |
| `capacity` | `union` | `False` | Total number of docking points installed at the station, including those that are temporarily disabled. Reflects the physical capacity of the station. | - | - | - |
| `is_virtual_station` | `union` | `False` | If true, the station is a virtual station (i.e., a parking zone without physical docks) rather than a docked station. If absent or false, the station has physical docking points. | - | - | - |

#### Schema `JP.ODPT.DocomoBikeshare.BikeshareStationStatus`
<a id="schema-jpodptdocomobikesharebikesharestationstatus"></a>

| Field | Value |
| --- | --- |
| Name | BikeshareStationStatus |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://real-time-sources.2030.io/schemas/jp/odpt/docomobikeshare/BikeshareStationStatus` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `BikeshareStationStatus`
<a id="schema-node-bikesharestationstatus"></a>

Real-time availability and operational status of a single Tokyo Docomo Bikeshare docking station, sourced from the GBFS 2.3 station_status.json feed published by the Open Data Platform for Transportation (ODPT). Updates on a 60-second TTL.

| Field | Value |
| --- | --- |
| $id | `https://real-time-sources.2030.io/schemas/jp/odpt/docomobikeshare/BikeshareStationStatus` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `system_id` | `string` | `True` | Identifier of the bikeshare system this station belongs to, for example 'docomo-cycle-tokyo'. Included in the payload so that the composite Kafka key {system_id}/{station_id} can be resolved from the event data. | - | - | - |
| `station_id` | `string` | `True` | Unique identifier of the station within the GBFS feed, for example '00010137'. Matches the station_id in the corresponding BikeshareStation event. | - | - | - |
| `num_bikes_available` | `int32` | `True` | Number of functional vehicles (bicycles) physically available for rental at this station at the time of the last update. | - | - | - |
| `num_bikes_disabled` | `union` | `False` | Number of disabled or broken vehicles at the station that are not available for rental. Absent if the operator does not publish this value. | - | - | - |
| `num_docks_available` | `union` | `False` | Number of empty and functional docking points at the station where a customer can return a vehicle. Absent if the operator does not publish this value. | - | - | - |
| `num_docks_disabled` | `union` | `False` | Number of broken or disabled docking points at the station that cannot accept vehicle returns. Absent if the operator does not publish this value. | - | - | - |
| `is_installed` | `boolean` | `True` | Indicates whether the station infrastructure is installed on-street and operational. A value of false means the station is temporarily or permanently removed from service. | - | - | - |
| `is_renting` | `boolean` | `True` | Indicates whether the station is currently allowing vehicle rentals. May be false even when bikes are present, for example during a system outage. | - | - | - |
| `is_returning` | `boolean` | `True` | Indicates whether the station is currently accepting vehicle returns. May be false even when docks are empty, for example during a system outage. | - | - | - |
| `last_reported` | `union` | `False` | Unix timestamp in seconds (UTC) indicating the last time this station's status was updated by the operator's system. Absent if the operator does not publish this value. | - | - | - |
