# Defra AURN Bridge Events

This document describes the events emitted by the Defra AURN bridge.

- [uk.gov.defra.aurn.Stations](#message-group-ukgovdefraaurnstations)
  - [uk.gov.defra.aurn.Station](#message-ukgovdefraaurnstation)
- [uk.gov.defra.aurn.Timeseries](#message-group-ukgovdefraaurntimeseries)
  - [uk.gov.defra.aurn.Timeseries](#message-ukgovdefraaurntimeseries)
  - [uk.gov.defra.aurn.Observation](#message-ukgovdefraaurnobservation)

---

## Message Group: uk.gov.defra.aurn.Stations

---

### Message: uk.gov.defra.aurn.Station

*Reference metadata for a Defra AURN monitoring station entry as published by the 52°North SOS Timeseries API stations collection.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `uk.gov.defra.aurn.Station` |
| `source` |  | `` | `False` | `https://uk-air.defra.gov.uk/sos-ukair/api/v1/stations` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:

##### Record: Station

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
## Message Group: uk.gov.defra.aurn.Timeseries

---

### Message: uk.gov.defra.aurn.Timeseries

*Reference metadata for a Defra AURN station and pollutant timeseries combination, including linked station coordinates and pollutant taxonomy identifiers.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `uk.gov.defra.aurn.Timeseries` |
| `source` |  | `` | `False` | `https://uk-air.defra.gov.uk/sos-ukair/api/v1/timeseries` |
| `subject` |  | `uritemplate` | `False` | `{timeseries_id}` |

#### Schema:

##### Record: Timeseries

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
---

### Message: uk.gov.defra.aurn.Observation

*Hourly or near-hourly Defra AURN observation value for a single timeseries, emitted from the getData endpoint for the most recent two-hour polling window.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `uk.gov.defra.aurn.Observation` |
| `source` |  | `` | `False` | `https://uk-air.defra.gov.uk/sos-ukair/api/v1/timeseries` |
| `subject` |  | `uritemplate` | `False` | `{timeseries_id}` |

#### Schema:

##### Record: Observation

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
