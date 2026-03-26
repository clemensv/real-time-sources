# UK EA Flood Monitoring API Bridge Events

This document describes the events that are emitted by the UK EA Flood Monitoring API Bridge.

- [UK.Gov.Environment.EA.FloodMonitoring](#message-group-ukgovenvironmenteafloodmonitoring)
  - [UK.Gov.Environment.EA.FloodMonitoring.Station](#message-ukgovenvironmenteafloodmonitoringstation)
  - [UK.Gov.Environment.EA.FloodMonitoring.Reading](#message-ukgovenvironmenteafloodmonitoringreading)

---

## Message Group: UK.Gov.Environment.EA.FloodMonitoring

---

### Message: UK.Gov.Environment.EA.FloodMonitoring.Station

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `UK.Gov.Environment.EA.FloodMonitoring.Station` |
| `source` | Source Feed URL | `string` | `True` | `https://environment.data.gov.uk/flood-monitoring` |

#### Schema:

##### Record: Station

*Monitoring station metadata with location and river information.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `station_reference` | *string* | Unique station reference identifier |
| `label` | *string* | Station name |
| `river_name` | *string* | Name of the river at the station |
| `catchment_name` | *string* | Name of the catchment area |
| `town` | *string* | Nearest town to the station |
| `lat` | *number* | Latitude of the station in WGS84 |
| `long` | *number* | Longitude of the station in WGS84 |
| `notation` | *string* | Station notation identifier |
| `status` | *string* | Station status URI |
| `date_opened` | *string* | Date the station was opened |

---

### Message: UK.Gov.Environment.EA.FloodMonitoring.Reading

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `UK.Gov.Environment.EA.FloodMonitoring.Reading` |
| `source` | Source Feed URL | `string` | `True` | `https://environment.data.gov.uk/flood-monitoring` |

#### Schema:

##### Record: Reading

*A water level or flow reading from a monitoring station.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `station_reference` | *string* | Station reference for this reading |
| `date_time` | *string* | Timestamp of the reading in ISO 8601 format |
| `measure` | *string* | Measure identifier URI |
| `value` | *number* | Reading value |
