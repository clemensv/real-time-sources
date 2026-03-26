# SMHI Hydrological Data Bridge Events

This document describes the events that are emitted by the SMHI Hydrological Data Bridge.

- [SE.Gov.SMHI.Hydro](#message-group-segovsmhihydro)
  - [SE.Gov.SMHI.Hydro.Station](#message-segovsmhihydrostation)
  - [SE.Gov.SMHI.Hydro.DischargeObservation](#message-segovsmhihydrodischargeobservation)

---

## Message Group: SE.Gov.SMHI.Hydro

---

### Message: SE.Gov.SMHI.Hydro.Station

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `SE.Gov.SMHI.Hydro.Station` |
| `source` | Source Feed URL | `uritemplate` | `True` | `https://opendata-download-hydroobs.smhi.se` |

#### Schema:

##### Record: Station

*A hydrological station from SMHI.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `station_id` | *string* | Unique station identifier |
| `name` | *string* | Station name |
| `owner` | *string* | Station owner (e.g. SMHI) |
| `measuring_stations` | *string* | Station type (CORE or ADDITIONAL) |
| `region` | *integer* | Region number |
| `catchment_name` | *string* | Catchment area name (river/watercourse) |
| `catchment_number` | *integer* | Catchment area number |
| `catchment_size` | *number* | Catchment area size in km² |
| `latitude` | *number* | Latitude in WGS84 |
| `longitude` | *number* | Longitude in WGS84 |

---

### Message: SE.Gov.SMHI.Hydro.DischargeObservation

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `SE.Gov.SMHI.Hydro.DischargeObservation` |
| `source` | Source Feed URL | `uritemplate` | `True` | `https://opendata-download-hydroobs.smhi.se` |

#### Schema:

##### Record: DischargeObservation

*A discharge observation from SMHI.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `station_id` | *string* | Station identifier |
| `station_name` | *string* | Station name |
| `catchment_name` | *string* | Catchment area name (river/watercourse) |
| `timestamp` | *string* | Measurement timestamp (ISO 8601) |
| `discharge` | *number* | Discharge (flow rate) in m³/s |
| `quality` | *string* | Data quality flag (e.g. O = original) |
