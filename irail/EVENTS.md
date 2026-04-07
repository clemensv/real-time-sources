# iRail Events

## Message Group: `be.irail`

### `be.irail.Station`

Station metadata for a Belgian railway station in the NMBS/SNCB network.

**CloudEvents Attributes:**
- `type`: `be.irail.Station`
- `source`: Feed URL
- `subject`: `{station_id}` (9-digit UIC-derived NMBS station code)

**Schema Fields:**

| Field | Type | Description |
|---|---|---|
| `station_id` | string | Nine-digit UIC-derived numeric station identifier |
| `name` | string | Default display name of the station |
| `standard_name` | string | Consistent official station name |
| `longitude` | double | Longitude in WGS84 decimal degrees |
| `latitude` | double | Latitude in WGS84 decimal degrees |
| `uri` | string | Stable linked-data URI identifying this station |

---

### `be.irail.StationBoard`

Real-time departure board for a Belgian railway station.

**CloudEvents Attributes:**
- `type`: `be.irail.StationBoard`
- `source`: Feed URL
- `subject`: `{station_id}` (9-digit UIC-derived NMBS station code)

**Schema Fields:**

| Field | Type | Description |
|---|---|---|
| `station_id` | string | Nine-digit UIC-derived station identifier |
| `station_name` | string | Display name of the station |
| `retrieved_at` | string | ISO 8601 UTC timestamp when board was retrieved |
| `departure_count` | int32 | Number of departures in this board snapshot |
| `departures` | array of Departure | Departure entries on the board |

**Departure (nested object):**

| Field | Type | Description |
|---|---|---|
| `destination_station_id` | string | Nine-digit identifier of the destination station |
| `destination_name` | string | Display name of the destination station |
| `scheduled_time` | string | Scheduled departure time in ISO 8601 UTC |
| `delay_seconds` | int32 | Current delay in seconds (0 = on time) |
| `is_canceled` | boolean | True if departure has been canceled |
| `has_left` | boolean | True if the train has already departed |
| `is_extra_stop` | boolean | True if stop added by traffic control |
| `vehicle_id` | string | Full iRail vehicle identifier (e.g., `BE.NMBS.IC2117`) |
| `vehicle_short_name` | string | Short name (e.g., `IC 2117`) |
| `vehicle_type` | string | Service type: IC, S, L, P, THA, EUR, EXT |
| `vehicle_number` | string | Numeric part of the vehicle identifier |
| `platform` | string (nullable) | Platform number. Null if not assigned |
| `is_normal_platform` | boolean | True if platform is the normally scheduled one |
| `occupancy` | string | Occupancy estimate: low, medium, high, unknown |
| `departure_connection_uri` | string | Stable URI uniquely identifying this departure |
