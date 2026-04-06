# Dublin City Noise Monitoring (Sonitus)
**Country/Region**: Ireland (Dublin)
**Publisher**: Dublin City Council / Smart Dublin / Sonitus Systems
**API Endpoint**: `https://data.smartdublin.ie/sonitus-api` (portal) — sensor data via Sonitus API
**Documentation**: https://data.smartdublin.ie/ (Smart Dublin Open Data)
**Protocol**: REST
**Auth**: API Key (via Smart Dublin registration)
**Data Format**: JSON
**Update Frequency**: Near real-time (continuous monitoring, typically 1-minute or 15-minute intervals)
**License**: Creative Commons Attribution 4.0 (CC BY 4.0)

## What It Provides
Dublin City's noise monitoring network (operated by Sonitus Systems) provides continuous environmental noise data from fixed monitoring stations across Dublin:
- **LAeq** — A-weighted equivalent continuous sound level
- **LA10, LA90** — statistical noise levels (10th and 90th percentiles)
- **LAmax, LAmin** — maximum and minimum levels
- **Octave/third-octave band spectra** (at some stations)
- **Weather data** (co-located at some stations: wind, rain, temperature)
- Station locations and metadata

## API Details
- **Smart Dublin portal**: `https://data.smartdublin.ie/` — datasets listed with Sonitus noise data
- **Sonitus API**: Sensor data available through the Sonitus Systems platform
- **Typical endpoints**: Location listing, real-time readings, historical data queries
- **Data resolution**: Typically LAeq measurements at 1-second, 1-minute, and 15-minute intervals
- **Stations**: Multiple fixed monitoring sites across Dublin city, including near construction sites, entertainment venues, and transport corridors
- **IoT Sensor Catalogue**: `https://iotsensorcatalogue.smartdublin.ie/` — browse available sensors

## Freshness Assessment
Good. Sonitus monitors report continuously, with data typically available at 1-minute to 15-minute resolution. The Smart Dublin platform provides open data access, though the exact API mechanics may require registration. The noise monitoring network is actively maintained.

## Entity Model
- **Location** (station ID, name, lat/lon, description, installation date)
- **Measurement** (timestamp, LAeq, LA10, LA90, LAmax, LAmin, frequency spectra)
- **Metadata** (sensor type, calibration date, measurement standard)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Continuous monitoring, near real-time |
| Openness | 2 | Open data, but may require API key |
| Stability | 2 | Smart Dublin platform, active but niche |
| Structure | 2 | JSON via API, exact schema needs exploration |
| Identifiers | 2 | Station IDs, but limited public documentation |
| Additive Value | 3 | Unique real-time urban noise data |
| **Total** | **14/18** | |

## Notes
- Sonitus Systems is a commercial environmental monitoring company — their API may have usage restrictions
- The Smart Dublin platform is the open data gateway
- Dublin's noise monitoring is part of the EU Environmental Noise Directive compliance
- Worth exploring the IoT Sensor Catalogue for additional sensor types
- Noise data is inherently real-time and high-frequency, making it a good candidate for streaming
