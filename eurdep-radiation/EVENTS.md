# EURDEP Radiation Events

## Message Group: `eu.jrc.eurdep`

### `eu.jrc.eurdep.Station`

Reference metadata for a EURDEP gamma dose rate monitoring station.

**CloudEvents Attributes:**
- `type`: `eu.jrc.eurdep.Station`
- `source`: Feed URL
- `subject`: `{station_id}` (e.g. `AT0001`)

**Schema Fields:**

| Field | Type | Description |
|---|---|---|
| `station_id` | string | Alphanumeric station identifier with country prefix (e.g. `AT0001`) |
| `name` | string | Human-readable station location name |
| `country_code` | string | ISO 3166-1 alpha-2 country code (first 2 chars of station_id) |
| `latitude` | double | Latitude in WGS84 decimal degrees |
| `longitude` | double | Longitude in WGS84 decimal degrees |
| `height_above_sea` | double (nullable) | Elevation above sea level in meters |
| `site_status` | int32 | Numeric operational status (1 = active) |
| `site_status_text` | string | Human-readable status text |

---

### `eu.jrc.eurdep.DoseRateReading`

Ambient gamma dose rate reading from a EURDEP monitoring station.

**CloudEvents Attributes:**
- `type`: `eu.jrc.eurdep.DoseRateReading`
- `source`: Feed URL
- `subject`: `{station_id}` (e.g. `AT0001`)

**Schema Fields:**

| Field | Type | Unit | Description |
|---|---|---|---|
| `station_id` | string | — | Alphanumeric station identifier |
| `name` | string | — | Station location name |
| `value` | double (nullable) | µSv/h | Gross ambient gamma dose rate |
| `unit` | string | — | Unit as reported by upstream (typically `µSv/h`) |
| `start_measure` | string | — | Start of measurement period (ISO 8601 UTC) |
| `end_measure` | string | — | End of measurement period (ISO 8601 UTC) |
| `nuclide` | string | — | Nuclide identifier (e.g. `Gamma-ODL-Brutto`) |
| `duration` | string | — | Measurement integration period (e.g. `1h`) |
| `validated` | int32 | — | Validation flag (0 = not validated, 1 = national, 2 = EURDEP) |
