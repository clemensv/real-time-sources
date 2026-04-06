# Sensor.Community (formerly Luftdaten.info)

**Country/Region**: Global (strongest in Europe, especially Germany)
**Publisher**: Sensor.Community / OK Lab Stuttgart
**API Endpoint**: `https://data.sensor.community/static/v2/data.json`
**Documentation**: https://github.com/opendata-stuttgart/meta/wiki/EN-APIs
**Protocol**: REST (static JSON snapshots, updated every ~5 minutes)
**Auth**: None
**Data Format**: JSON
**Update Frequency**: ~5 minutes (rolling snapshot of last 5 minutes' data)
**License**: Open Data (DbCL 1.0 — Database Contents License)

## What It Provides

Sensor.Community operates one of the world's largest citizen-run sensor networks — over 15,000 active sensors worldwide measuring air quality (PM2.5, PM10), temperature, humidity, barometric pressure, and noise levels. The API serves a complete snapshot of all sensor readings from the last 5 minutes as a single JSON array.

Live probe confirmed active data: readings from sensors in Germany (Stuttgart area) with SDS011 (particulate), DHT22 (temperature/humidity), BME280 (temp/humidity/pressure), and PPD42NS sensors. Timestamps show data from within the last 2 minutes.

## API Details

- **Full snapshot**: `https://data.sensor.community/static/v2/data.json` — all sensors, last 5 minutes (~60-80 MB JSON)
- **Per-sensor type**: `https://data.sensor.community/static/v2/data.1.json` (type 1 = PPD42NS), `data.14.json` (SDS011), etc.
- **Per-sensor**: `https://data.sensor.community/airrohr/v1/sensor/{sensor_id}/`
- **CSV archive**: `https://archive.sensor.community/` — historical daily CSV files
- **Fields per reading**: `id`, `timestamp`, `location` (id, lat, lon, altitude, country, exact_location, indoor), `sensor` (id, pin, sensor_type with id/name/manufacturer), `sensordatavalues` (array of value/value_type pairs)
- **Value types**: `P1` (PM10), `P2` (PM2.5), `temperature`, `humidity`, `pressure`, `noise_LAeq` (noise sensors)
- **No authentication, no rate limiting on static endpoints**

## Freshness Assessment

The static JSON endpoint is regenerated every ~5 minutes. Individual sensor readings are typically 2-5 minutes old. For a citizen sensor network this is excellent freshness. The archive endpoint provides historical data with daily granularity.

## Entity Model

- **Location**: `id`, geographic coordinates, country, altitude, indoor/outdoor flag
- **Sensor**: `id`, `pin` (physical connection), `sensor_type` (id, name, manufacturer)
- **Reading**: `id` (unique), `timestamp`, array of sensor data values
- **Sensor Data Value**: `id`, `value` (string-encoded number), `value_type` (P1, P2, temperature, etc.)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | 5-minute snapshots; good for citizen sensor data |
| Openness | 3 | No auth, no rate limits, open license |
| Stability | 3 | Running since 2015, large active community |
| Structure | 3 | Clean JSON with consistent schema |
| Identifiers | 2 | Sensor and location IDs are stable; no formal URN scheme |
| Additive Value | 3 | Massive global citizen sensor network; unique dataset |
| **Total** | **16/18** | |

## Notes

- The full `data.json` endpoint is very large (~60-80 MB). Filter by sensor type for smaller payloads.
- Per-sensor endpoints are more efficient for targeted queries but there's no bulk "changed since" API.
- Sensor types span a wide range: SDS011, PMS5003, BME280, DHT22, SPS30, PPD42NS, BMP180, DNMS (noise).
- The network is predominantly European but growing globally (India, Brazil, Japan, etc.).
- Data quality varies — citizen sensors are not calibrated to reference standards but correlate well in aggregate.
