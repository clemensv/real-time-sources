# AirQo — Kampala/Uganda Air Quality Network

- **Country/Region**: Uganda (Kampala and expanding)
- **Endpoint**: `https://api.airqo.net/api/v2/devices/measurements`
- **Protocol**: REST
- **Auth**: API key (free registration)
- **Format**: JSON
- **Freshness**: Near real-time (hourly or better)
- **Docs**: https://docs.airqo.net/
- **Score**: 13/18

## Overview

AirQo is a remarkable African-born air quality monitoring network, developed by Makerere
University in Kampala, Uganda. It operates 100+ low-cost air quality sensors primarily
in Kampala, with expansion to other Ugandan cities and East African countries.

What makes AirQo special:
- **African-designed**: Built by African researchers for African conditions
- **Dense urban coverage**: 100+ sensors in Kampala alone — more granular than most
  European city networks
- **Machine learning calibration**: Uses ML to improve low-cost sensor accuracy
- **Open data commitment**: API access available for researchers and developers
- **Expanding footprint**: Growing into Nairobi, Dar es Salaam, and other cities

AirQo represents the future of African environmental monitoring — locally developed,
mobile-first, sensor-dense, and API-accessible.

## Endpoint Analysis

The AirQo API is documented at `https://docs.airqo.net/` with the following structure:

```
# Get latest measurements
GET /api/v2/devices/measurements?tenant=airqo&recent=yes

# Get device list
GET /api/v2/devices?tenant=airqo

# Get measurements for specific device
GET /api/v2/devices/measurements?device_id={id}&startTime={ISO}&endTime={ISO}

# Get site information
GET /api/v2/sites?tenant=airqo
```

Expected response:
```json
{
  "success": true,
  "measurements": [
    {
      "device": "aq_01",
      "site_id": "site_001",
      "pm2_5": {"value": 45.2, "calibratedValue": 38.1},
      "pm10": {"value": 67.8},
      "temperature": {"value": 24.5},
      "humidity": {"value": 72.0},
      "time": "2026-04-06T18:00:00Z",
      "location": {"latitude": 0.3476, "longitude": 32.5825}
    }
  ]
}
```

## Integration Notes

- **API key registration**: Register at https://platform.airqo.net/ for API access.
  The platform includes a dashboard, analytics tools, and API documentation.
- **Calibrated vs raw**: AirQo provides both raw and ML-calibrated PM2.5 values.
  Use calibrated values for CloudEvents — they account for humidity interference
  and sensor drift common in tropical environments.
- **Kampala focus**: The densest coverage is in Kampala. For other Ugandan cities
  and expansion areas, check device availability first.
- **OpenAQ integration**: AirQo feeds data into OpenAQ. But the AirQo API provides
  more detail (calibrated values, device metadata, site context).
- **African success story**: Highlight this as an example of Africa building its own
  environmental monitoring infrastructure — not waiting for imported solutions.
- **Event enrichment**: Combine with weather data to explain pollution spikes (dust
  storms, biomass burning, stagnant air).

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Hourly or better |
| Openness | 2 | Free API key required |
| Stability | 2 | University-backed, growing |
| Structure | 2 | JSON API, documentation improving |
| Identifiers | 2 | Device IDs, site IDs |
| Richness | 2 | PM2.5, PM10, temp, humidity, calibrated values |
