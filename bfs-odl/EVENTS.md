# BfS ODL Events

## Message Group: `de.bfs.odl`

### `de.bfs.odl.Station`

Station metadata for a BfS ODL gamma dose rate monitoring probe.

**CloudEvents Attributes:**
- `type`: `de.bfs.odl.Station`
- `source`: Feed URL
- `subject`: `{station_id}` (9-digit Kennziffer)

**Schema Fields:**

| Field | Type | Description |
|---|---|---|
| `station_id` | string | Nine-digit station identifier (Kennziffer) assigned by BfS |
| `station_code` | string | Short alphanumeric station code (e.g., `DEZ0305`) |
| `name` | string | Human-readable station location name |
| `postal_code` | string | German postal code (PLZ) |
| `site_status` | int32 | Numeric operational status (1 = in operation) |
| `site_status_text` | string | German status text (e.g., "in Betrieb") |
| `kid` | int32 | Numeric region identifier (Kreis-ID) |
| `height_above_sea` | double (nullable) | Elevation above sea level in meters |
| `longitude` | double | Longitude in WGS84 decimal degrees |
| `latitude` | double | Latitude in WGS84 decimal degrees |

---

### `de.bfs.odl.DoseRateMeasurement`

One-hour averaged ambient gamma dose rate measurement.

**CloudEvents Attributes:**
- `type`: `de.bfs.odl.DoseRateMeasurement`
- `source`: Feed URL
- `subject`: `{station_id}` (9-digit Kennziffer)

**Schema Fields:**

| Field | Type | Unit | Description |
|---|---|---|---|
| `station_id` | string | — | Nine-digit station identifier |
| `start_measure` | string | — | Start of measurement period (ISO 8601 UTC) |
| `end_measure` | string | — | End of measurement period (ISO 8601 UTC) |
| `value` | double (nullable) | µSv/h | Gross ambient gamma dose rate |
| `value_cosmic` | double (nullable) | µSv/h | Cosmic radiation component |
| `value_terrestrial` | double (nullable) | µSv/h | Terrestrial radiation component |
| `validated` | int32 | — | Validation flag (1 = validated, 0 = preliminary) |
| `nuclide` | string | — | Nuclide identifier (always `Gamma-ODL-Brutto`) |
