# Canada AQHI Bridge Events

This bridge emits three CloudEvents types in the `ca.gc.weather.aqhi` message
group. All three use the same Kafka key and CloudEvents subject:

- `subject`: `{province}/{community_name}`
- Kafka key: `{province}/{community_name}`

## `ca.gc.weather.aqhi.Community`

Reference data for an AQHI reporting community.

| Field | Type | Description |
|---|---|---|
| `province` | `string` | Two-letter Canadian province or territory code. |
| `community_name` | `string` | AQHI community name as published by ECCC. |
| `cgndb_code` | `string` | Five-character CGNDB community identifier. |
| `latitude` | `double` | Community latitude in WGS84 decimal degrees. |
| `longitude` | `double` | Community longitude in WGS84 decimal degrees. |
| `observation_url` | `string \| null` | Current XML observation feed URL for the community. |
| `forecast_url` | `string \| null` | Current XML forecast feed URL for the community. |

## `ca.gc.weather.aqhi.Observation`

Latest AQHI observation for a community.

| Field | Type | Description |
|---|---|---|
| `province` | `string` | Two-letter Canadian province or territory code. |
| `community_name` | `string` | AQHI community name as published by ECCC. |
| `cgndb_code` | `string` | Five-character CGNDB community identifier. |
| `observation_datetime` | `string` | Observation timestamp in ISO 8601 UTC form. |
| `aqhi` | `double \| null` | AQHI value from the upstream observation feed. |
| `aqhi_category` | `string` | `Low`, `Moderate`, `High`, `Very High`, or `Unknown`. |

## `ca.gc.weather.aqhi.Forecast`

Public AQHI forecast for one of the four standard forecast periods.

| Field | Type | Description |
|---|---|---|
| `province` | `string` | Two-letter Canadian province or territory code. |
| `community_name` | `string` | AQHI community name as published by ECCC. |
| `cgndb_code` | `string` | Five-character CGNDB community identifier. |
| `publication_datetime` | `string` | Forecast bulletin issue timestamp in ISO 8601 UTC form. |
| `forecast_date` | `string` | Forecast target date in `YYYYMMDD` format. |
| `forecast_period` | `integer` | `1` Today, `2` Tonight, `3` Tomorrow, `4` Tomorrow Night. |
| `forecast_period_label` | `string` | English label for the forecast period. |
| `aqhi` | `integer \| null` | Forecast AQHI value for the public period. |
| `aqhi_category` | `string` | `Low`, `Moderate`, `High`, `Very High`, or `Unknown`. |
