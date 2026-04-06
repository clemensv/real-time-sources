# German Autobahn Traffic Events

The bridge emits CloudEvents in structured JSON format to Kafka-compatible
endpoints.

## Event Metadata

- `source`: `https://verkehr.autobahn.de/o/autobahn`
- `subject`: `{identifier}`
- Kafka key: `{identifier}`

## Event Families

The upstream API exposes multiple resource-specific payload shapes and uses
`display_type` to distinguish important subtypes. The bridge preserves those
families in the emitted event contract.

| Event type prefix | Payload schema | Trigger |
|---|---|---|
| `DE.Autobahn.Roadwork*` | `DE.Autobahn.RoadEvent` | `roadworks` items with `display_type=ROADWORKS` |
| `DE.Autobahn.ShortTermRoadwork*` | `DE.Autobahn.RoadEvent` | `roadworks` items with `display_type=SHORT_TERM_ROADWORKS` |
| `DE.Autobahn.Warning*` | `DE.Autobahn.WarningEvent` | `warning` items |
| `DE.Autobahn.Closure*` | `DE.Autobahn.RoadEvent` | `closure` items with `display_type=CLOSURE` |
| `DE.Autobahn.EntryExitClosure*` | `DE.Autobahn.RoadEvent` | `closure` items with `display_type=CLOSURE_ENTRY_EXIT` |
| `DE.Autobahn.WeightLimit35Restriction*` | `DE.Autobahn.RoadEvent` | `closure` items with `display_type=WEIGHT_LIMIT_35` |
| `DE.Autobahn.ParkingLorry*` | `DE.Autobahn.ParkingLorry` | `parking_lorry` items |
| `DE.Autobahn.ElectricChargingStation*` | `DE.Autobahn.ChargingStation` | charging items with `display_type=ELECTRIC_CHARGING_STATION` |
| `DE.Autobahn.StrongElectricChargingStation*` | `DE.Autobahn.ChargingStation` | charging items with `display_type=STRONG_ELECTRIC_CHARGING_STATION` |
| `DE.Autobahn.Webcam*` | `DE.Autobahn.Webcam` | `webcam` items |

Each family emits the lifecycle triplet `Appeared`, `Updated`, and `Resolved`.

## Payload Shapes

`DE.Autobahn.RoadEvent` includes the shared road-event fields used by
roadworks and closure-like items: identifiers, aggregated `road_ids`, route
text, lane or blockage metadata, optional geometry, impact ranges, and footer
text.

`DE.Autobahn.WarningEvent` extends the road-event shape with warning-specific
traffic metadata such as `delay_minutes`, `average_speed_kmh`,
`abnormal_traffic_type`, and `source_name`.

`DE.Autobahn.ParkingLorry` contains parking-site metadata plus parsed
`amenity_descriptions`, `car_space_count`, and `lorry_space_count`.

`DE.Autobahn.ChargingStation` contains charging-site metadata plus parsed
`address_line`, `charging_point_count`, and `charging_points_json`.

`DE.Autobahn.Webcam` contains webcam metadata plus `operator_name`,
`image_url`, and `stream_url`.