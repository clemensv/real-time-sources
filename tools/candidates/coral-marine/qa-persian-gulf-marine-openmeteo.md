# Qatar Marine Conditions (Open-Meteo Copernicus Marine)

- **Country/Region**: Qatar (Persian Gulf)
- **Endpoint**: `https://marine-api.open-meteo.com/v1/marine?latitude=25.28&longitude=51.52&current=wave_height,wave_direction,wave_period,wind_wave_height,swell_wave_height&hourly=wave_height,wave_direction,ocean_current_velocity,ocean_current_direction`
- **Protocol**: REST / JSON
- **Auth**: None
- **Format**: JSON
- **Freshness**: Current block updates every ~15 minutes; hourly forecasts
- **Docs**: https://open-meteo.com/en/docs/marine-weather-api
- **Score**: 14/18

## Overview

Open-Meteo provides free access to **Copernicus Marine Service (CMEMS)** wave and ocean
current forecasts for any coastal or offshore location worldwide. For Qatar, this covers the
**Persian Gulf** (also called Arabian Gulf), a semi-enclosed sea with shallow depths (avg 50m,
max 90m) and complex wave dynamics.

Qatar has ~560 km of coastline. Marine conditions are relevant for:
- **Hamad Port** (Mesaieed) — Qatar's primary deepwater container/RoRo terminal
- **Ras Laffan** — LNG export terminal (largest in the world, ~80 MTPA capacity)
- **Fishing and recreation**: Pearl diving heritage, dhow sailing, sport fishing
- **Offshore oil/gas platforms**: North Field (world's largest non-associated gas field,
  shared with Iran as South Pars)
- **Desalination intake**: Qatar depends on desalinated seawater; wave/current conditions
  affect intake efficiency

The model provides:
- **Total wave height** (wind waves + swell)
- **Wave direction** and **period** (dominant wave characteristics)
- **Wind wave height** (locally generated waves from current wind)
- **Swell wave height** (long-period waves propagating from distant storms)
- **Ocean current velocity and direction** (surface currents)
- **Sea surface temperature** (also available, not shown in example endpoint)

## Endpoint Analysis

**Live test successful** — API returned current marine conditions off Doha coast:

```json
{
  "latitude": 25.28,
  "longitude": 51.52,
  "generationtime_ms": 0.089,
  "utc_offset_seconds": 10800,
  "timezone": "Asia/Qatar",
  "current_units": {
    "time": "iso8601",
    "wave_height": "m",
    "wave_direction": "°",
    "wave_period": "s",
    "wind_wave_height": "m",
    "swell_wave_height": "m"
  },
  "current": {
    "time": "2025-05-22T15:00",
    "wave_height": 0.90,
    "wave_direction": 356,
    "wave_period": 4.15,
    "wind_wave_height": 0.88,
    "swell_wave_height": 0.02
  },
  "hourly_units": {
    "time": "iso8601",
    "wave_height": "m",
    "wave_direction": "°"
  },
  "hourly": {
    "time": ["2025-05-22T00:00", "2025-05-22T01:00", ...],
    "wave_height": [0.85, 0.87, 0.92, 0.95, ...],
    "wave_direction": [358, 357, 356, 355, ...]
  }
}
```

**Interpretation**:
- **Wave height**: 0.90 m (moderate, typical for Persian Gulf in spring)
- **Wave direction**: 356° (from the north, consistent with shamal wind)
- **Wave period**: 4.15 s (short period = locally generated wind waves, not oceanic swell)
- **Wind wave vs swell**: Wind wave = 0.88 m, swell = 0.02 m → **almost entirely wind-driven**,
  typical for enclosed seas
- **Implication**: The Persian Gulf has minimal swell because it's too small for oceanic swell
  to develop. Waves are dominated by local wind (shamal from the north/northwest).

**Additional parameters** available:
- `sea_surface_temperature` (SST, critical for coral health and desalination efficiency)
- `ocean_current_velocity`, `ocean_current_direction` (surface currents)
- `significant_wave_height` (H_s, statistical measure of wave height)

**7-day forecast**: Hourly predictions for the next 168 hours.

**Multi-location**: Can request coastal grid points along Qatar's entire coastline.

## Integration Notes

- **Polling interval**: 60 minutes for hourly data; 15 minutes if using `current` block only
- **CloudEvents subject**: `marine/{location}` → `marine/doha` or `marine/hamad-port`
- **Kafka key**: Location identifier (e.g., `doha`, `ras-laffan`, or lat/lon grid cell)
- **Entity model**: Coastal grid point time series
- **Data source**: Copernicus Marine Service (CMEMS), operated by Mercator Ocean International
  for the European Commission
- **Model**: GLORYS12 (global ocean reanalysis) + real-time forecast models
- **License**: CC BY 4.0
- **Overlap check**: The repo does not currently have a marine/wave conditions bridge.
  **NOAA NDBC** covers US buoys (wave height, SST, wind, pressure) but is geographic-specific
  to US waters. A global marine bridge using CMEMS would be a **new capability**.
- **Qatar-specific relevance**:
  - LNG shipping from Ras Laffan requires wave height forecasts for tanker navigation
  - Hamad Port container operations depend on wave conditions for safe berthing
  - Offshore platform access (helicopter, crew boat) requires wave/wind forecasts
  - Recreational boating safety

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Current block updates every ~15 min; hourly forecasts |
| Openness | 3 | No auth, free tier, CC BY 4.0, documented API |
| Stability | 3 | Open-Meteo + CMEMS operational service |
| Structure | 2 | Typed JSON with units metadata |
| Identifiers | 2 | Lat/lon grid points (stable but not named buoy IDs) |
| Additive value | 2 | New domain (marine/wave) for non-US locations |

**Verdict**: Recommended as a **global marine-conditions bridge** using Open-Meteo's CMEMS
backend. Qatar (Persian Gulf coastal points) would be the initial configuration, but the
bridge could cover any ocean/sea location worldwide. This fills a gap in the repo's coverage —
currently only US coastal buoys (NOAA NDBC) have wave data.

**Use cases**:
- Marine safety warnings for Qatar's 560 km coastline
- Port operations planning (Hamad Port, Ras Laffan)
- Offshore energy sector (platform access weather windows)
- Desalination plant intake efficiency (SST, current velocity)
- Coral reef monitoring (SST anomalies trigger bleaching)
- Recreational boating / fishing forecasts

**Comparison with buoy networks**: Qatar does not operate a public real-time coastal buoy
network (unlike NOAA NDBC in the US or MIRAMAR in France). CMEMS model output is the **best
available free real-time source** for Persian Gulf marine conditions.

**Persian Gulf specifics**: The Gulf is shallow, warm (SST 15–35°C seasonal range), and
hypersaline (salinity 40-45 ppt vs 35 ppt global avg). Wave climate is dominated by shamal
winds (north/northwest, especially June-July). CMEMS models are calibrated for the Gulf's
unique characteristics.
