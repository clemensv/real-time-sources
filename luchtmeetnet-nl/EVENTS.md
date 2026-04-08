# Luchtmeetnet Netherlands Events

The bridge emits structured JSON CloudEvents whose payloads are defined by the
checked-in xRegistry contract in `xreg/luchtmeetnet_nl.xreg.json`.

| Event type | Description | Subject template | Schema summary |
|---|---|---|---|
| `nl.rivm.luchtmeetnet.Station` | Station reference data with operator, classification, coordinates, and measured formulas. | `{station_number}` | `Station` contains `station_number`, `location`, `type`, `organisation`, nullable `municipality` and `province`, WGS84 `longitude` and `latitude`, `year_start`, and the `components` list. |
| `nl.rivm.luchtmeetnet.Measurement` | Hourly measurement for one station and one component formula. | `{station_number}` | `Measurement` contains `station_number`, `formula`, numeric `value`, and ISO 8601 `timestamp_measured`. |
| `nl.rivm.luchtmeetnet.LKI` | Hourly Dutch national air quality index for one station. | `{station_number}` | `LKI` contains `station_number`, integer `value` on the 1-11 scale, and ISO 8601 `timestamp_measured`. |
| `nl.rivm.luchtmeetnet.components.Component` | Component reference data with Dutch and English names for a formula code. | `{formula}` | `Component` contains `formula`, `name_nl`, and `name_en`. |
