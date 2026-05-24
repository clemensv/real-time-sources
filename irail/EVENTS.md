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

## MQTT/UNS topic tree

The MQTT feeder publishes MQTT 5.0 binary-mode CloudEvents under the Unified Namespace root `transit/be/irail/irail`.

| Event | Topic | Retain | QoS | Notes |
|---|---|---:|---:|---|
| `be.irail.Station` | `transit/be/irail/irail/{station_id}/info` | true | 1 | Station reference snapshot. |
| `be.irail.StationBoard` | `transit/be/irail/irail/{station_id}/station-board` | true | 1 | Departure-board state snapshot; retained publish expires after 900 seconds. |
| `be.irail.ArrivalBoard` | `transit/be/irail/irail/{station_id}/arrival-board` | true | 1 | Arrival-board state snapshot; retained publish expires after 900 seconds. |

`{station_id}` is a required, non-null 9-digit NMBS/SNCB station identifier and is the same value used by the Kafka key and CloudEvents subject.

### Subscription patterns

| Use case | Subscription |
|---|---|
| One station, all iRail state | `transit/be/irail/irail/008814001/#` |
| Station reference data for every station | `transit/be/irail/irail/+/info` |
| Departure boards for every station | `transit/be/irail/irail/+/station-board` |
| Arrival boards for every station | `transit/be/irail/irail/+/arrival-board` |
| Entire iRail tree | `transit/be/irail/irail/#` |
