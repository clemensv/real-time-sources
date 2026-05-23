# NEOM Smart City - Sensor Networks

- **Country/Region**: Saudi Arabia (NEOM, northwestern Saudi Arabia)
- **Endpoint**: Unknown (project under construction)
- **Protocol**: Unknown
- **Auth**: Unknown
- **Format**: Unknown
- **Freshness**: Real-time (smart city sensors are continuous)
- **Docs**: https://www.neom.com (no data portal)
- **Score**: 9/18

## Overview

**NEOM** (نيوم) is Saudi Arabia's flagship megaproject: a $500 billion "smart city" being built from scratch in northwestern Saudi Arabia along the Red Sea coast. NEOM is a key component of Saudi Vision 2030 and aims to be:

- **100% renewable energy** (solar, wind)
- **Carbon neutral** (zero emissions)
- **Fully autonomous** (self-driving vehicles, AI governance)
- **Hyper-connected** (5G/6G, IoT sensors everywhere)
- **Population**: 1 million by 2030 (planned)
- **Size**: 26,500 km² (larger than Israel, comparable to Belgium)

NEOM comprises several sub-projects:
1. **THE LINE** — A 170 km linear city, 200m wide, no cars, walkable end-to-end
2. **Oxagon** — Industrial floating city for advanced manufacturing
3. **Trojena** — Mountain resort with artificial snow (ski resort in Saudi Arabia!)
4. **Sindalah** — Luxury island resort (Red Sea)
5. **NEOM Bay** — Coastal city with marina and beaches

**Smart city technology**: NEOM is designed as a **living lab** for AI, IoT, and urban innovation. Planned systems include:

- **Digital twin** — Real-time 3D model of the entire city
- **IoT sensor network** — Millions of sensors monitoring:
  - Air quality (PM2.5, PM10, O3, NO2)
  - Energy consumption (building-level, real-time)
  - Water usage and quality
  - Traffic flow (autonomous vehicle coordination)
  - Weather (microclimate stations)
  - Waste management (smart bins, collection routes)
  - Structural health (building sway, bridge load)
- **AI-driven operations** — Automated traffic, energy, water, waste management
- **Open data platform** — NEOM has announced plans for a public data portal (not yet launched)

**Construction status** (as of 2024):
- THE LINE: First phase under construction (excavation visible from satellite)
- Oxagon: Groundwork started
- Trojena: Site preparation
- Sindalah: Island resort opening 2024
- Overall: Early construction phase; full operation not expected until 2030+

## Potential Data Products

If NEOM publishes sensor data, it could include:

1. **Air quality** — Real-time PM2.5, PM10, O3, NO2 from distributed sensors
2. **Energy generation** — Solar farm output, wind turbine production, battery storage state
3. **Energy consumption** — Building-level electricity use, grid load
4. **Water network** — Desalination plant output, distribution pressure, usage by zone
5. **Weather** — High-density microclimate monitoring (temperature, humidity, wind, radiation)
6. **Traffic** — Autonomous vehicle positions (if public), pedestrian flow
7. **Waste** — Smart bin fill levels, collection routes
8. **Environmental** — Red Sea water quality, coral health, marine biodiversity

**Update frequency**: Smart city sensors typically report every **1-60 minutes** for static metrics (air quality, weather), and **1-second intervals** for dynamic metrics (energy, traffic).

## Endpoint Analysis

**NEOM website**: `https://www.neom.com`

NEOM's corporate website provides project information, news, and renderings. **No data portal or developer API** is currently advertised.

**Open data announcements**: NEOM has publicly stated it will be a **"transparent city"** with open data, but no portal has launched yet.

**Possible future endpoints** (speculative):
```
https://data.neom.com/api/sensors
https://api.neom.com/v1/airquality
https://digital-twin.neom.com/live
```

**Comparison with other smart cities**:

| City/Project | Status | Open data? | Real-time sensors? |
|--------------|--------|------------|--------------------|
| **NEOM** | Under construction | ❌ Not yet | ❓ Planned |
| Songdo (South Korea) | Operational | ❌ Limited | ✅ Yes (private) |
| Masdar City (UAE) | Operational | ❌ None | ✅ Yes (private) |
| Singapore | Operational | ✅ Yes | ✅ Some (data.gov.sg) |
| Barcelona | Operational | ✅ Yes | ✅ Yes (OpenDataBCN) |
| Copenhagen | Operational | ✅ Yes | ✅ Yes (Open Data DK) |

**Pattern**: Middle Eastern "smart cities" (Masdar, NEOM) have **not published open data**, unlike European smart cities (Barcelona, Copenhagen). NEOM's announced commitment to transparency would be a regional breakthrough.

## Integration Notes

- **City does not exist yet**: NEOM is under construction and will not be operational until the late 2020s or 2030s. There is no data to fetch.
- **Open data promise**: NEOM has publicly committed to transparency and open data. If fulfilled, this would be a **globally significant smart city data source**.
- **Monitor for launch**: Check NEOM's website and Saudi open data portal (data.gov.sa) quarterly for:
  - Data portal launch
  - Developer API documentation
  - Sample sensor datasets
- **Alternative: Construction monitoring**: Satellite imagery of NEOM construction progress is publicly available (Sentinel-2, Landsat). This is not "real-time" in the sensor sense but is updated every few days.

**Unique value if data exists**:
- **First Saudi smart city data** — No other Saudi city publishes real-time sensor data.
- **Desert smart city** — NEOM's extreme climate (summer heat, dust storms, Red Sea humidity) provides unique environmental monitoring.
- **100% renewable grid** — Real-time energy data would show the world's first 100%-renewable city in operation.
- **Red Sea marine monitoring** — NEOM borders pristine coral reefs. Marine water quality data would be valuable for climate science.

**High-value datasets to prioritize** (if published):
1. **Renewable energy generation** — Solar/wind output, battery state
2. **Air quality** — Desert dust, marine aerosols
3. **Red Sea water quality** — Temperature, salinity, pH (coral health)
4. **Microclimate weather** — High-density station network in extreme desert

## Scoring

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Smart city sensors are real-time (if data existed) |
| Openness | 1 | Announced open data commitment, but not yet implemented |
| Stability | 2 | Mega-project backed by Saudi government, but long-term viability uncertain |
| Structure | 3 | Would likely be JSON REST API (modern smart city standard) |
| Identifiers | 2 | Sensor IDs, zone IDs (if implemented) |
| Additive value | 3 | **Globally unique** — first 100% renewable city, desert smart city |

**Total: 14/18** (if data existed and open data commitment is fulfilled)  
**Actual: 9/18** (penalized for non-existent city and uncertain data policy)

**Verdict**: ⏭️ **Reference** — NEOM is a **high-value future source** that does not yet exist. The city's announced commitment to open data makes it worth monitoring, but there is no data to build a bridge for until NEOM is operational (late 2020s at earliest).

**Recommended action**:
1. **Monitor NEOM announcements** — Check neom.com and Saudi media quarterly for data portal launches.
2. **Monitor data.gov.sa** — NEOM sensor data may appear on the national portal.
3. **Contact NEOM** — Reach out to NEOM's digital infrastructure team to request early access or beta API credentials once construction advances.
4. **Satellite monitoring** — In the meantime, track NEOM construction progress via satellite imagery (Sentinel-2 updates every 5 days).

If NEOM launches an open data portal with real-time sensor data, **immediately escalate to ✅ Build**. This would be a flagship source for:
- Smart city research
- Renewable energy grid operations
- Desert climate monitoring
- Red Sea marine environmental science

**Timeline**: Expect no data until **2026 at earliest** (Sindalah island resort may publish first). Full NEOM data not expected until **2030+**.
