# Sensor.Community (Luftdaten.info) - UAE Citizen Air Quality Sensors

- **Country/Region**: United Arab Emirates (crowdsourced deployments)
- **Endpoint**: `https://data.sensor.community/airrohr/v1/filter/country=AE`
- **Protocol**: REST API (JSON)
- **Auth**: None
- **Format**: JSON
- **Freshness**: Real-time (sensors report every 2.5 minutes)
- **Docs**: https://sensor.community/en/, https://github.com/opendata-stuttgart/meta/wiki/APIs
- **Score**: **12–13/18** (if UAE has sensors; 0/18 if none deployed)

## Overview

**Sensor.Community** (formerly Luftdaten.info) is a global citizen science air quality network where volunteers build and deploy low-cost PM2.5/PM10 sensors (based on SDS011, PMS5003, or similar). The network has ~15,000 active sensors worldwide.

**How it works**:
- DIY sensor kits (~€30–50): Particulate sensor + ESP8266 WiFi + power supply
- Sensor reports to Sensor.Community API every 2.5 minutes
- Data includes: PM2.5, PM10, temperature, humidity, location (lat/lon)
- Open API: No auth, public JSON feeds

**Why citizen sensors matter**:
- **Spatial density**: Citizen networks achieve 100x higher spatial resolution than regulatory networks
- **Hyperlocal**: Track pollution hotspots (traffic intersections, construction sites, industrial areas)
- **Complementary**: Fill gaps where official monitoring is sparse
- **Community engagement**: Empowers residents to monitor their own air quality

## UAE Deployment Status (Unknown)

**Sensor.Community does NOT have a country-level dashboard**. To check UAE coverage:

```
GET https://data.sensor.community/airrohr/v1/filter/country=AE
```

**Expected outcomes**:
1. **If sensors exist**: API returns sensor list with locations and latest readings
2. **If no sensors**: API returns empty array `[]`

**Manual check** (browser):
- Visit https://maps.sensor.community/
- Zoom to UAE (Dubai, Abu Dhabi, Sharjah)
- Look for sensor dots

**As of this discovery**: Unknown whether UAE has active Sensor.Community deployments. The UAE has a high expatriate population with environmental awareness (especially European expats familiar with Luftdaten), so deployment is plausible.

## Why UAE Citizen Sensors Would Be Valuable

**If UAE has sensors**:

1. **Complements official networks**: EAD, Dubai Municipality, NCM air quality stations are sparse (20–30 stations per city). Citizen sensors could add 100+.
2. **Dust storm hyperlocal tracking**: Official stations show city-wide averages; citizen sensors reveal neighborhood-level variations during haboobs.
3. **Construction pollution**: Dubai/Abu Dhabi have massive construction activity (mega-projects, Expo 2020 legacy sites). Citizen sensors near sites track PM spikes.
4. **Traffic pollution**: Sensors near Sheikh Zayed Road, E11 highway, or Jebel Ali Port reveal vehicle/shipping emissions.
5. **Indoor-outdoor**: Some users deploy sensors inside homes to track indoor air quality (AC filter effectiveness, cooking emissions).

## API Analysis

**Sensor.Community API** (verified working globally):

**Get all UAE sensors**:
```
GET https://data.sensor.community/airrohr/v1/filter/country=AE
```

**Returns** (if sensors exist):
```json
[
  {
    "sensor": {
      "id": 123456,
      "sensor_type": {
        "name": "SDS011"
      }
    },
    "location": {
      "latitude": "25.2048",
      "longitude": "55.2708",
      "altitude": "10.0",
      "country": "AE",
      "indoor": 0
    },
    "sensordatavalues": [
      {"value_type": "P1", "value": "12.34"},  // PM10
      {"value_type": "P2", "value": "8.56"},   // PM2.5
      {"value_type": "temperature", "value": "38.2"},
      {"value_type": "humidity", "value": "45.0"}
    ],
    "timestamp": "2025-01-23T10:15:00"
  }
]
```

**Update frequency**: Every 2.5 minutes per sensor (145 seconds)

## Scoring (If UAE Has Sensors)

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 2.5-minute updates (real-time) |
| Openness | 3 | No auth, fully open API |
| Stability | 2 | Community network; sensors can go offline without notice |
| Structure | 3 | JSON REST API, well-documented |
| Identifiers | 3 | Sensor IDs are stable (assigned when sensor registers) |
| Additive value | 1–2 | Air quality domain exists; citizen sensors add spatial density but quality is lower than regulatory sensors |

**Total**: 15/18 (if sensors exist and are active)

**If UAE has NO sensors**: Score = 0 (no data source)

## Key Model

**Sensor-keyed** (`sensor_id`)

**Event families**:
- Reference: sensor metadata (location, sensor type, indoor/outdoor, owner metadata)
- Telemetry: measurements (PM2.5, PM10, temperature, humidity, timestamp)

**CloudEvents subject**: `ae/air-quality/citizen/sensors/{sensor_id}`

## Integration Notes

- **Bridge would be global**: Sensor.Community covers 80+ countries. A bridge would poll all countries, not just UAE. UAE would be a **geographic filter** in post-processing.
- **Repo sibling**: The repo does not have a citizen sensor source yet. This would establish the **citizen science sensor domain**.
- **Data quality**: Citizen sensors are less accurate than regulatory monitors (±15–30% error typical). Include data quality flags in schema.
- **Sensor churn**: Sensors go offline frequently (power outages, WiFi issues, owner relocates). Bridge needs to handle dynamic sensor lists.

## Verdict

**IF UAE has active Sensor.Community sensors**: **Build** (score 13–15/18, depending on sensor count and stability)

**IF UAE has NO sensors**: **Skip** (no data source exists)

**Action required**: 
1. **Query Sensor.Community API** for UAE (1 minute):
   ```
   curl "https://data.sensor.community/airrohr/v1/filter/country=AE"
   ```
2. **Check map** at maps.sensor.community (zoom to UAE)

**If sensors found**:
- Count active sensors (need at least 5–10 for viable dataset)
- Check last update times (sensors reporting within last 24 hours = active)
- Proceed to **Build** (global Sensor.Community bridge with UAE coverage documented)

**If no sensors found**:
- **Skip** but document as a **potential future source** (advocate for Sensor.Community deployment in UAE)
- Contact UAE environmental groups, maker communities, expat forums to encourage sensor builds

**Priority**: Low-to-Medium (contingent on sensor existence). If sensors exist, this is a **quick win** (API is trivial to integrate). If not, it's a dead end.
