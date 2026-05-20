# DWD Open Data Bridge Events

This document describes the events emitted by the DWD Open Data bridge.

- [DE.DWD.CDC](#message-group-dedwdcdc)
  - [DE.DWD.CDC.StationMetadata](#message-dedwdcdcstationmetadata)
  - [DE.DWD.CDC.AirTemperature10Min](#message-dedwdcdcairtemperature10min)
  - [DE.DWD.CDC.Precipitation10Min](#message-dedwdcdcprecipitation10min)
  - [DE.DWD.CDC.Wind10Min](#message-dedwdcdcwind10min)
  - [DE.DWD.CDC.Solar10Min](#message-dedwdcdcsolar10min)
  - [DE.DWD.CDC.HourlyObservation](#message-dedwdcdchourlyobservation)
  - [DE.DWD.Weather.Alert](#message-dedwdweatheralert)
- [DE.DWD.IconD2](#message-group-dedwdicond2)
  - [DE.DWD.IconD2.Grid](#message-dedwdicond2grid)

---

## Message Group: DE.DWD.CDC

---

### Message: DE.DWD.CDC.StationMetadata

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.DWD.CDC.StationMetadata` |
| `source` |  | `` | `False` | `https://opendata.dwd.de` |

#### Schema:

##### Record: None

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
---

### Message: DE.DWD.CDC.AirTemperature10Min

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.DWD.CDC.AirTemperature10Min` |
| `source` |  | `` | `False` | `https://opendata.dwd.de` |

#### Schema:

##### Record: None

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
---

### Message: DE.DWD.CDC.Precipitation10Min

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.DWD.CDC.Precipitation10Min` |
| `source` |  | `` | `False` | `https://opendata.dwd.de` |

#### Schema:

##### Record: None

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
---

### Message: DE.DWD.CDC.Wind10Min

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.DWD.CDC.Wind10Min` |
| `source` |  | `` | `False` | `https://opendata.dwd.de` |

#### Schema:

##### Record: None

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
---

### Message: DE.DWD.CDC.Solar10Min

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.DWD.CDC.Solar10Min` |
| `source` |  | `` | `False` | `https://opendata.dwd.de` |

#### Schema:

##### Record: None

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
---

### Message: DE.DWD.CDC.HourlyObservation

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.DWD.CDC.HourlyObservation` |
| `source` |  | `` | `False` | `https://opendata.dwd.de` |

#### Schema:

##### Record: None

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
---

### Message: DE.DWD.Weather.Alert

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.DWD.Weather.Alert` |
| `source` |  | `` | `False` | `https://opendata.dwd.de` |

#### Schema:

##### Record: None

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|

---

## Message Group: DE.DWD.IconD2

ICON-D2 numerical weather prediction grids (DWD short-range, ~2.2 km native resolution). One event per `(run_id, parameter, lead_hour)` carries the full forecast field aggregated to a regular 0.1 deg lat/lon grid as parallel `lats` / `lons` / `values` arrays.

---

### Message: DE.DWD.IconD2.Grid

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type`      | CloudEvents type | `string`    | `True`       | `DE.DWD.IconD2.Grid` |
| `source`    | Origin URL       | `string`    | `True`       | `https://opendata.dwd.de` |
| `subject`   | Identity key     | `uritemplate` | `True`     | `{run_id}/{parameter}/{lead_hour}` |

Kafka partition key uses the same template as the subject: `{run_id}/{parameter}/{lead_hour}`.

#### Schema:

##### Record: Grid

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `run_id` | `string` | Model run identifier, `YYYYMMDDHH`. |
| `run_time` | `datetime` | UTC timestamp of the model run. |
| `parameter` | `string` | ICON-D2 parameter short name (e.g. `t_2m`, `tot_prec`, `vmax_10m`, `clct`, `cape_ml`, `dbz_cmax`, `pmsl`, `h_snow`). |
| `unit` | `string` | Physical unit of `values` (e.g. `degC`, `mm`, `m/s`, `hPa`). |
| `lead_hour` | `int` | Forecast lead hour, 0..48. |
| `valid_time` | `datetime` | UTC timestamp this forecast field is valid for (`run_time + lead_hour`). |
| `produced_at` | `datetime` | UTC timestamp the bridge produced this event. |
| `source_url` | `string` | Anonymous HTTPS URL of the original GRIB2.bz2 file on opendata.dwd.de. |
| `resolution_deg` | `number` | Aggregation grid spacing in degrees (typically 0.1). |
| `bbox_min_lon` / `bbox_min_lat` / `bbox_max_lon` / `bbox_max_lat` | `number` | Bounding box of the aggregation grid (lon/lat order). |
| `lats` | `number[]` | Latitudes of populated cell centres (parallel to `lons` and `values`). |
| `lons` | `number[]` | Longitudes of populated cell centres. |
| `values` | `number[]` | Forecast values, indexed parallel to `lats`/`lons`. Missing-value sentinels are filtered at the source; `dbz_cmax` clear-air rows are filtered at the KQL update policy. |
