# Sensor.Community (formerly Luftdaten.info)

**Country/Region**: Global (crowdsourced; heaviest in Europe)
**Publisher**: Sensor.Community / Open Knowledge Foundation / OK Lab Stuttgart
**API Endpoint**: `https://data.sensor.community/airrohr/v1/`
**Documentation**: https://github.com/opendata-stuttgart/meta/wiki/EN-APIs
**Protocol**: REST
**Auth**: None
**Data Format**: JSON
**Update Frequency**: Real-time (~2.5 minute intervals per sensor)
**License**: Open Data Commons Database License (ODbL)

## What It Provides

Sensor.Community is the world's largest citizen science air quality network, with 15,000+ low-cost sensors deployed globally (concentrated in Germany and Europe). Sensors measure PM2.5, PM10 (SDS011, SPS30), temperature, humidity, and pressure (BME280, DHT22). The API provides real-time readings from all sensors with no authentication required.

## API Details

- **Base URL**: `https://data.sensor.community/airrohr/v1/`
- **Key Endpoints**:
  - `GET /filter/type=SDS011` — all current readings from SDS011 PM sensors
  - `GET /filter/type=BME280` — all current readings from BME280 temp/humidity sensors
  - `GET /filter/area=lat,lon,dist` — sensors within radius of coordinates
  - `GET /filter/country=DE` — sensors in a country
  - `GET /sensor/{id}/` — readings from a specific sensor
  - `GET /push-sensor-data/` — endpoint for sensors to push data
- **Response Fields**: location (lat/lon/country/altitude/indoor), sensor (type, id), timestamp, sensordatavalues (P1=PM10, P2=PM2.5)
- **Data Volume**: Very large — `filter/type=SDS011` returns thousands of readings in a single response
- **Sample**: `{"location":{"longitude":"25.62","country":"BG","latitude":"42.42"},"sensor":{"sensor_type":{"name":"SDS011"},"id":36083},"timestamp":"2026-04-06 10:24:02","sensordatavalues":[{"value":"5.00","value_type":"P1"},{"value":"3.33","value_type":"P2"}]}`

## Freshness Assessment

Sensors report every ~2.5 minutes. The API returns the most recent reading from each sensor. Data is as fresh as it gets for citizen science — true near-real-time. No historical API; historical data is available as daily CSV archives.

## Entity Model

- **Sensor** → id, sensor_type (SDS011, BME280, etc.), pin
- **Location** → id, lat/lon, country, altitude, indoor flag
- **SensorDataValues** → value, value_type (P1=PM10, P2=PM2.5, temperature, humidity, pressure)
- Sensors push data; API serves latest snapshot

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | ~2.5 min intervals, true real-time |
| Openness | 3 | No auth, ODbL license |
| Stability | 2 | Community-run project; API has returned 403 errors during testing |
| Structure | 2 | Simple flat JSON, but large bulk responses |
| Identifiers | 2 | Sensor IDs stable; location IDs present |
| Additive Value | 3 | Massive citizen science network; unique granularity |
| **Total** | **15/18** | |

## Notes

- The API occasionally returns 403 errors on the `/v1/now/` endpoint. The `/airrohr/v1/filter/` endpoints are more reliable.
- Response sizes can be very large (tens of MB for all SDS011 sensors globally). Use country or area filters.
- Data quality varies — these are low-cost sensors in uncontrolled environments. Not regulatory-grade.
- Already ingested by OpenAQ, but direct access gives real-time per-sensor granularity.
- Historical data: daily CSV archives at `https://archive.sensor.community/` organized by date.
- The push API (`push-sensor-data`) could enable real-time streaming integration.
