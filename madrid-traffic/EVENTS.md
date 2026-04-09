# Events for `es.madrid.informo`

## MeasurementPoint

- **Type:** `es.madrid.informo.MeasurementPoint`
- **Source:** `https://informo.madrid.es/informo/tmadrid/pm.xml`
- **Subject:** `{sensor_id}`

Reference data for a traffic measurement point (sensor) in Madrid's Informo system.

| Field | Type | Required | Description |
|---|---|---|---|
| `sensor_id` | string | Yes | Unique sensor identifier (upstream: `idelem`) |
| `description` | string | Yes | Road segment description in Spanish (upstream: `descripcion`) |
| `element_type` | string or null | No | Classification: URB (urban), M30 (ring motorway), etc. |
| `subarea` | string or null | No | Traffic management zone code (upstream: `subarea`) |
| `longitude` | double or null | No | Longitude in decimal degrees WGS84 (upstream: `st_x`) |
| `latitude` | double or null | No | Latitude in decimal degrees WGS84 (upstream: `st_y`) |
| `saturation_intensity` | integer or null | No | Max capacity in vehicles/hour (upstream: `intensidadSat`) |

## TrafficReading

- **Type:** `es.madrid.informo.TrafficReading`
- **Source:** `https://informo.madrid.es/informo/tmadrid/pm.xml`
- **Subject:** `{sensor_id}`

Real-time traffic reading from a measurement point, updated every ~5 minutes.

| Field | Type | Required | Description |
|---|---|---|---|
| `sensor_id` | string | Yes | Unique sensor identifier (upstream: `idelem`) |
| `intensity` | integer or null | No | Traffic intensity in vehicles/hour (upstream: `intensidad`) |
| `occupancy` | integer or null | No | Road occupancy 0–100% (upstream: `ocupacion`) |
| `load` | integer or null | No | Load percentage (upstream: `carga`) |
| `service_level` | integer or null | No | 0=free flow, 1=moderate, 2=congested, 3=severe (upstream: `nivelServicio`) |
| `error_flag` | string or null | No | N=normal, S/Y=error (upstream: `error`) |
| `timestamp` | datetime | Yes | UTC timestamp (poll time rounded to 5-min interval) |
