# Netherlands NDL EV Charging Events

The bridge emits CloudEvents in structured JSON format to Kafka-compatible
endpoints.

## Topics and Keys

| Topic | Key template | Message group | Event types |
|---|---|---|---|
| `ndl-charging` | `{location_id}` | `NL.NDW.Charging.Locations` | `ChargingLocation` |
| `ndl-charging` | `{location_id}/{evse_uid}` | `NL.NDW.Charging.Evse` | `EvseStatus` |
| `ndl-charging-tariffs` | `{tariff_id}` | `NL.NDW.Charging.Tariffs` | `ChargingTariff` |

## Event Metadata

All events share:

- `source`: `https://opendata.ndw.nu`
- `time`: OCPI `last_updated` timestamp from the upstream object

## Event Types

### NL.NDW.Charging.ChargingLocation

Reference data for an EV charging location. Emitted for every location on the
first poll. Contains the static OCPI v2.2 Location properties:

- `location_id` — OCPI Location.id (key)
- `country_code` — ISO-3166 alpha-2 CPO country
- `party_id` — CPO party identifier
- `publish` — whether the location is publicly visible
- `name`, `address`, `city`, `postal_code`, `state`, `country`
- `latitude`, `longitude` — WGS 84 coordinates
- `parking_type` — ON_STREET, PARKING_LOT, PARKING_GARAGE, etc.
- `operator_name`, `operator_website`, `suboperator_name`, `owner_name`
- `facilities` — list of facility types (SUPERMARKET, WIFI, etc.)
- `time_zone` — IANA TZ value
- `opening_times_twentyfourseven`, `charging_when_closed`
- `energy_mix_is_green_energy`, `energy_mix_supplier_name`
- `evse_count`, `connector_count` — aggregate counts
- `last_updated`

### NL.NDW.Charging.EvseStatus

Telemetry event for EVSE status changes. Emitted on every poll for EVSEs whose
`status` has changed. The subject and Kafka key is `{location_id}/{evse_uid}`.

- `location_id`, `evse_uid` — composite identity
- `evse_id` — human-readable eMI3 identifier
- `status` — AVAILABLE, BLOCKED, CHARGING, INOPERATIVE, OUTOFORDER, PLANNED,
  REMOVED, RESERVED, UNKNOWN
- `capabilities` — RFID_READER, REMOTE_START_STOP_CAPABLE, etc.
- `floor_level`, `latitude`, `longitude`, `physical_reference`
- `parking_restrictions` — CUSTOMERS, DISABLED, EV_ONLY, etc.
- `connectors` — array of connector summaries, each with:
  - `connector_id`, `standard`, `format`, `power_type`
  - `max_voltage`, `max_amperage`, `max_electric_power`
  - `tariff_ids` — references to ChargingTariff events
- `last_updated`

### NL.NDW.Charging.ChargingTariff

Reference data for charging tariffs. Emitted for every tariff on the first
poll. Contains the OCPI v2.2 Tariff structure:

- `tariff_id` — OCPI Tariff.id (key)
- `country_code`, `party_id`, `currency`
- `tariff_type` — AD_HOC_PAYMENT, PROFILE_CHEAP, PROFILE_FAST, etc.
- `tariff_alt_text`, `tariff_alt_url`
- `min_price_excl_vat`, `min_price_incl_vat`
- `max_price_excl_vat`, `max_price_incl_vat`
- `elements` — array of tariff elements, each with:
  - `price_components` — array of {type, price, vat, step_size}
  - `restrictions` — optional conditions (time of day, day of week, power, etc.)
- `start_date_time`, `end_date_time`
- `energy_mix_is_green_energy`
- `last_updated`

## Data Source

All data is sourced from the Nationale Databank Laadinfrastructuur (NDL),
published by the Dutch National Data Warehouse for Traffic Information (NDW):

- Locations: `https://opendata.ndw.nu/charging_point_locations_ocpi.json.gz`
- Tariffs: `https://opendata.ndw.nu/charging_point_tariffs_ocpi.json.gz`

The data uses the OCPI v2.2 (Open Charge Point Interface) standard with a
three-level hierarchy: Location → EVSE → Connector. Updates are published
every few minutes.
