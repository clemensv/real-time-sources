# PegelOnline API Bridge Events

This document describes the events that are emitted by the PegelOnline API Bridge.

- [de.wsv.pegelonline](#message-group-dewsvpegelonline)
  - [de.wsv.pegelonline.Station](#message-dewsvpegelonlinestation)
  - [de.wsv.pegelonline.CurrentMeasurement](#message-dewsvpegelonlinecurrentmeasurement)

---

## Message Group: de.wsv.pegelonline

### Message: de.wsv.pegelonline.Station

**ID**: de.wsv.pegelonline.Station
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro
**Created At**: 2024-09-10T15:02:55.573631
**Modified At**: 2024-09-10T15:02:55.573631

#### Metadata:

- **specversion**: CloudEvents version
  - Type: *string*
  - Required: *True*
  - Value: `1.0`

- **type**: Event type
  - Type: *string*
  - Required: *True*
  - Value: `de.wsv.pegelonline.Station`

- **source**: Source Feed URL
  - Type: *uritemplate*
  - Required: *True*
  - Value: `{feedurl}`

- **subject**: Station
  - Type: *uritemplate*
  - Required: *False*
  - Value: `{station_id}`

#### Schema:

##### Record: Station

*Schema representing a PEGELONLINE station with location and water body information.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `uuid` | *string* | Unique immutable identifier of the station. |
| `number` | *string* | Station number representing the unique code of the station. |
| `shortname` | *string* | Short name of the station (maximum 40 characters). |
| `longname` | *string* | Full name of the station (maximum 255 characters). |
| `km` | *double* | River kilometer marking of the station location. |
| `agency` | *string* | Waterways and Shipping Office responsible for the station. |
| `longitude` | *double* | Longitude coordinate of the station in WGS84 decimal notation. |
| `latitude` | *double* | Latitude coordinate of the station in WGS84 decimal notation. |
| `water` | [Record Water](#record-water) |  |

---

##### Record: Water

*Details of the water body associated with the station.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `shortname` | *string* | Short name of the water body (maximum 40 characters). |
| `longname` | *string* | Full name of the water body (maximum 255 characters). |
### Message: de.wsv.pegelonline.CurrentMeasurement

**ID**: de.wsv.pegelonline.CurrentMeasurement
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro
**Created At**: 2024-09-10T15:02:58.776148
**Modified At**: 2024-09-10T15:02:58.776148

#### Metadata:

- **specversion**: CloudEvents version
  - Type: *string*
  - Required: *True*
  - Value: `1.0`

- **type**: Event type
  - Type: *string*
  - Required: *True*
  - Value: `de.wsv.pegelonline.CurrentMeasurement`

- **source**: Source Feed URL
  - Type: *uritemplate*
  - Required: *True*
  - Value: `{feedurl}`

- **subject**: Station
  - Type: *uritemplate*
  - Required: *False*
  - Value: `{station_id}`

#### Schema:

##### Record: CurrentMeasurement

*Schema representing the current measurement for a PEGELONLINE station.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `station_uuid` | *string* | Unique immutable identifier of the station. |
| `timestamp` | *string* | Timestamp of the current measurement encoded in ISO_8601 format. |
| `value` | *double* | Current measured value as a decimal number in the unit defined by the station's timeseries. |
| `stateMnwMhw` | *string* |  |
| `stateNswHsw` | *string* |  |
