# Smart Citizen

**Country/Region**: Global (origin: Barcelona, Catalonia)
**Publisher**: Fab Lab Barcelona / Institute for Advanced Architecture of Catalonia
**API Endpoint**: `https://api.smartcitizen.me/v0/`
**Documentation**: https://developer.smartcitizen.me/
**Protocol**: REST (JSON)
**Auth**: None (read), OAuth2 (write)
**Data Format**: JSON
**Update Frequency**: Varies by device — active devices report every 1-5 minutes
**License**: Data is CC BY-SA 4.0; platform is open source (AGPL)

## What It Provides

Smart Citizen is an open-source citizen sensor platform built around the Smart Citizen Kit — a modular environmental monitoring device that measures air quality (PM2.5, PM10, NO2, CO), noise levels (dBA), temperature, humidity, light, and barometric pressure. Devices are deployed by citizens, schools, hackerspaces, and researchers worldwide, with particular density in European cities.

The API provides access to every device, its sensors, and its readings. You can query by location, find nearby devices, and retrieve time-series data for any sensor on any device.

## API Details

- **Devices list**: `GET /v0/devices?per_page={n}` — all devices with latest readings
- **Nearby devices**: `GET /v0/devices?near={lat},{lng}&per_page={n}` — geographic search
- **Single device**: `GET /v0/devices/{id}` — full device details including all sensors
- **Readings**: `GET /v0/devices/{id}/readings?sensor_id={sid}&rollup={interval}&from={date}&to={date}` — time-series data
- **Search**: `GET /v0/search?q={query}` — full-text search across devices
- **Pagination**: `per_page` (max 100), `page` parameters
- **No auth for reads**: All device data publicly accessible
- **Rate limit**: Not explicitly documented; API is responsive

## Freshness Assessment

Active devices post readings every 1-5 minutes. The API reflects the latest reading instantly. The `last_reading_at` field on each device shows when it last reported. Many devices are intermittent or retired, so filtering by `state=has_published` and recent `last_reading_at` is essential.

Confirmed live: Barcelona-area query returned devices with recent data.

## Entity Model

- **Device**: `id` (integer), `name`, `description`, `state`, `last_reading_at`, `owner` (user), `data` (latest readings)
- **Sensor**: `id`, `name`, `description`, `unit`, `measurement_id`
- **Reading**: `timestamp`, `value` (per sensor)
- **Location**: `latitude`, `longitude`, `city`, `country`
- **Kit**: Hardware model (Smart Citizen Kit 1.0, 1.1, 2.1, Station)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | 1-5 minutes for active devices; many are dormant |
| Openness | 3 | No auth, open API, AGPL platform, CC BY-SA data |
| Stability | 2 | Academic project; smaller scale than commercial platforms |
| Structure | 3 | Clean JSON, well-documented REST API |
| Identifiers | 3 | Integer device/sensor IDs, measurement type IDs |
| Additive Value | 2 | Multi-sensor environmental data; complements air-quality-focused platforms |
| **Total** | **15/18** | |

## Notes

- Confirmed live: API returned devices including "Parisien Sensor" with historical data.
- The platform is fully open source — firmware, hardware designs, and backend are all on GitHub.
- Device density is highest in Barcelona, but deployments span globally (schools, hackerspaces, research projects).
- The multi-sensor approach (air + noise + weather) is unique — most citizen sensor platforms focus on one measurement type.
- Noise monitoring capability (dBA) is relatively rare in citizen sensor APIs.
- Pairs well with Sensor.Community for air quality cross-validation, and with official monitoring networks for calibration.
