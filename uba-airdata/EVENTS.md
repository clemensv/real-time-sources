# UBA Germany Air Quality Bridge Events

This document describes the events emitted by the UBA Germany Air Quality
bridge.

- `de.uba.airdata.Station`
- `de.uba.airdata.Measure`
- `de.uba.airdata.components.Component`

---

## Message Group: de.uba.airdata

### Message: de.uba.airdata.Station

Station reference event keyed by `station_id`.

CloudEvents attributes:

- `type`: `de.uba.airdata.Station`
- `source`: `{feedurl}`
- `subject`: `{station_id}`

Fields:

- `station_id` — stable numeric UBA station identifier
- `station_code` — official station code such as `DEBE021`
- `station_name` — station display name
- `station_city` — city or locality
- `station_synonym` — legacy short code if published
- `active_from` — activation date
- `active_to` — deactivation date, or `null` while active
- `longitude` — WGS84 longitude
- `latitude` — WGS84 latitude
- `network_id` — stable monitoring network identifier
- `network_code` — short network code such as `BE`, `BB`, or `UB`
- `network_name` — network display name
- `setting_name` — station environment label
- `setting_short` — short environment code
- `type_name` — station type such as traffic or background
- `street` — street name if published
- `street_nr` — street number if published
- `zip_code` — postal code if published

### Message: de.uba.airdata.Measure

Hourly one-hour-average measurement event keyed by `station_id`.

CloudEvents attributes:

- `type`: `de.uba.airdata.Measure`
- `source`: `{feedurl}`
- `subject`: `{station_id}`

Fields:

- `station_id` — stable numeric UBA station identifier
- `component_id` — pollutant component identifier
- `scope_id` — UBA averaging scope identifier, typically `2` for one hour
- `date_start` — start of the measurement interval
- `date_end` — end of the measurement interval
- `value` — measurement value in the unit defined by the component, or `null`
- `quality_index` — quality flag published by UBA

---

## Message Group: de.uba.airdata.components

### Message: de.uba.airdata.components.Component

Component reference event keyed by `component_id`.

CloudEvents attributes:

- `type`: `de.uba.airdata.components.Component`
- `source`: `{feedurl}`
- `subject`: `{component_id}`

Fields:

- `component_id` — stable numeric UBA component identifier
- `component_code` — short component code such as `NO2`, `O3`, or `PM10`
- `symbol` — published chemical or pollutant symbol
- `unit` — published measurement unit string
- `name` — English display name
