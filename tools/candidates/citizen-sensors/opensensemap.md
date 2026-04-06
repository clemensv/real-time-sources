# openSenseMap

**Country/Region**: Global (strongest in Germany/Europe)
**Publisher**: Institute for Geoinformatics (ifgi), University of Münster
**API Endpoint**: `https://api.opensensemap.org/boxes`
**Documentation**: https://docs.opensensemap.org/
**Protocol**: REST
**Auth**: None (read access)
**Data Format**: JSON
**Update Frequency**: Continuous (sensor-dependent, typically 1-10 minutes)
**License**: Open Data (PDDL for data, MIT for code)

## What It Provides

openSenseMap is a citizen sensor platform from the University of Münster where anyone can register a "senseBox" (sensor station) and publish environmental data. The network covers temperature, humidity, air pressure, light intensity, UV, noise, PM2.5/PM10, and more. Each "box" is a sensor station with multiple sensors, registered with metadata including location, exposure type, and sensor configuration.

Live probe confirmed active API: returned boxes like "LeKa Berlin" with sensors for Helligkeit (light), Schall (sound), Luftdruck (pressure), Luftfeuchtigkeit (humidity), Temperatur (temperature). Sensor types include GL5528, LM386, BMP085, DHT11.

## API Details

- **List boxes**: `GET /boxes?limit={n}&format=json` — sensor stations with metadata
- **Single box**: `GET /boxes/{boxId}` — full station detail with sensor array
- **Measurements**: `GET /boxes/{boxId}/sensors/{sensorId}` — time-series for one sensor
- **Bulk data**: `GET /boxes/data?bbox={west,south,east,north}&phenomenon={name}` — spatial query
- **Statistics**: `GET /statistics/descriptive?boxId={id}&sensorId={id}&from_date={}&to_date={}`
- **Fields**: `_id`, `name`, `sensors[]` (id, sensorType, title, unit, lastMeasurement), `exposure` (indoor/outdoor/mobile/unknown), `model`, `currentLocation` (GeoJSON Point), `lastMeasurementAt`, `createdAt`, `grouptag`
- **MQTT**: Boxes can publish via MQTT; API serves the aggregated data via REST
- **No authentication for read access**

## Freshness Assessment

Freshness varies by box. Active boxes report every 1-10 minutes. Some boxes have been inactive for years (the probe showed last measurements in 2014-2024 range across different boxes). The API reflects the latest data per sensor. No streaming interface — polling required.

## Entity Model

- **Box (senseBox)**: Station with id, name, location (GeoJSON), exposure type, model, creation date
- **Sensor**: Attached to a box; has id, type, title, unit, last measurement reference
- **Measurement**: Value + timestamp for a specific sensor
- **Phenomenon**: What's being measured (temperature, PM2.5, etc.) — encoded in sensor title/type

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Active boxes report every 1-10 minutes; many inactive boxes |
| Openness | 3 | No auth, PDDL license, open API |
| Stability | 2 | University-backed; running since 2015 |
| Structure | 3 | Well-structured REST API with GeoJSON support |
| Identifiers | 2 | MongoDB ObjectIDs as identifiers |
| Additive Value | 2 | Overlaps with Sensor.Community; platform is more flexible |
| **Total** | **14/18** | |

## Notes

- openSenseMap is more of a platform than a network — it aggregates data from diverse hardware including senseBox kits, custom Arduino setups, and commercial sensors.
- The data heterogeneity is both a strength (flexibility) and weakness (inconsistent coverage).
- Many registered boxes are inactive or test installations — active filtering is important.
- The senseBox hardware kit is widely used in German schools for STEM education.
- MQTT ingestion means the platform can accept data from IoT devices natively.
