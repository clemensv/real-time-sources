# ESA Swarm Geomagnetic Field (VirES API)

- **Country/Region**: Global
- **Endpoint**: `https://vires.services/api/`
- **Protocol**: REST API + Python client (viresclient)
- **Auth**: Free VirES account (email registration)
- **Format**: CSV, JSON, CDF (Common Data Format)
- **Freshness**: Near-real-time (FAST products ~3 hours latency), operational products ~2–3 days
- **Docs**: https://vires.services/, https://viresclient.readthedocs.io/
- **Score**: 13/18

## Overview

ESA's **Swarm** mission consists of three satellites measuring Earth's magnetic field with
unprecedented precision. Launched in 2013, Swarm flies in polar orbit delivering continuous
global coverage of:

- **Magnetic field vector** (VFM): 50 Hz high-resolution data
- **Plasma density** (Langmuir probe): electron density, temperature
- **Field-aligned currents** (FAC): ionospheric current systems
- **Total Electron Content** (TEC): ionospheric structure
- **Auroral oval boundaries**: high-latitude plasma boundaries

The **VirES (Virtual environments for Earth Scientists)** platform provides web GUI and API
access to Swarm data. VirES serves:

- **FAST products** — 3-hour latency near-real-time data for operational use
- **Operational products** — 2–3 day latency fully validated data
- **Historical archive** — complete mission dataset back to November 2013

Swarm data is used for:
- **Space weather monitoring** — geomagnetic storm detection
- **Ionospheric studies** — TEC, plasma bubbles, scintillation
- **Geomagnetic field modeling** — IGRF, CHAOS models
- **Aurora forecasting** — field-aligned current tracking
- **Navigation systems** — magnetic declination updates

## Endpoint Analysis

VirES provides three access methods:

1. **Web GUI** — https://vires.services/ (interactive visualization, not machine-readable)
2. **Python client** (`viresclient`) — Pythonic API wrapper
3. **HAPI server** (Heliophysics API) — https://vires.services/hapi (time-series REST protocol)

The **Python client** is the recommended integration path:

```python
from viresclient import SwarmRequest

request = SwarmRequest()
request.set_collection("SW_OPER_MAGA_LR_1B")  # Swarm A magnetometer low-res
request.set_products(
    measurements=["F", "B_NEC"],  # scalar intensity, vector components
    auxiliaries=["QDLat", "QDLon"],  # quasi-dipole coordinates
)
request.set_range_filter("Latitude", 50, 90)  # Arctic region
request.set_time_range("2026-01-15T00:00:00Z", "2026-01-15T06:00:00Z")

data = request.get_between(asynchronous=False, show_progress=False)
df = data.as_dataframe()
```

The client returns **pandas DataFrame** or **xarray Dataset** with Swarm measurements.

**HAPI server** (for tool-agnostic access):

```
GET https://vires.services/hapi/data?
  dataset=SW_OPER_MAGA_LR_1B&
  parameters=F,B_NEC&
  start=2026-01-15T00:00:00Z&
  stop=2026-01-15T06:00:00Z
```

Returns CSV with timestamp, magnetic field components, and auxiliary parameters.

**Data collections** (key products for near-real-time use):

- `SW_FAST_MAGA_LR_1B` — **Swarm A FAST** magnetic field (1 Hz), ~3-hour latency
- `SW_FAST_FACATMS_2F` — **Field-aligned currents FAST**, ~3-hour latency
- `SW_FAST_TECATMS_2F` — **Total electron content FAST**, ~3-hour latency
- `SW_OPER_MAGA_LR_1B` — Swarm A operational magnetic field (1 Hz), 2–3 day latency
- `SW_OPER_MAGA_HR_1B` — Swarm A high-res (50 Hz) magnetic field, 2–3 day latency

The **FAST products** (3-hour latency) are suitable for near-real-time space weather
monitoring. The operational products are for scientific analysis.

## Schema / Sample Payload

HAPI CSV output:

```csv
Timestamp,Latitude,Longitude,Radius,F,B_NEC_N,B_NEC_E,B_NEC_C
2026-01-15T00:00:00.000000Z,52.3,12.5,6871234.0,48567.2,22134.5,-234.1,44321.0
2026-01-15T00:00:01.000000Z,52.4,12.6,6871235.0,48568.1,22135.0,-233.9,44322.5
...
```

Fields:
- **Timestamp** — UTC, 1 Hz cadence (or 50 Hz for HR products)
- **Latitude, Longitude** — spacecraft position (degrees)
- **Radius** — geocentric distance (meters, ~6,800 km orbital altitude)
- **F** — magnetic field scalar intensity (nT, nanoTesla)
- **B_NEC** — magnetic field vector in North-East-Center frame (nT)

Additional derived parameters available:
- **QDLat, QDLon** — quasi-dipole magnetic coordinates (better for aurora/polar studies)
- **MLT** — Magnetic Local Time
- **Kp** — geomagnetic activity index (from external model)
- **FAC** — field-aligned current density (μA/m²)
- **TEC** — total electron content (TECU, 10¹⁶ electrons/m²)

Full parameter catalog: https://viresclient.readthedocs.io/en/latest/available_parameters.html

## Why Strong

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| **Value** | 3 | Swarm is the world's premier geomagnetic field mission. Critical for space weather, navigation, ionospheric research, and geophysical studies. Unique dataset unavailable elsewhere. |
| **Freshness** | 2 | FAST products: 3-hour latency (excellent for satellite data). Operational products: 2–3 days (not NRT but scientifically authoritative). |
| **Openness** | 2 | Free VirES account (email registration). No usage fees, generous quotas. Python client + HAPI REST API = easy integration. Not "no auth" but very accessible. |
| **Schema clarity** | 3 | HAPI is a formal time-series protocol. CDF/CSV output with documented units, coordinates, quality flags. Viresclient returns typed pandas/xarray. |
| **Machine-readability** | 3 | HAPI REST, Python client, CSV/CDF output. All industry-standard formats with mature library support. |
| **Repo fit** | 0 | **Satellite track data**, not station-based. Swarm orbits Earth every ~90 minutes, sweeping through different geographies. No stable "station ID" — data is keyed by time+orbit segment. Modeling as station-like events is a poor fit. |

**Total: 13/18** — Scientifically exceptional but **orbital track model** doesn't align with
repo's station/entity paradigm.

## Integration Notes

### Challenge: Orbital Track vs. Station Model

Swarm satellites trace **orbital paths**, not fixed stations. A single orbit segment might
look like:

- 00:00:00 — over Scandinavia at (60°N, 15°E)
- 00:01:00 — over Baltic Sea at (58°N, 20°E)
- 00:02:00 — over Poland at (55°N, 25°E)

Each second is a new geographic location. Treating each second as a separate CloudEvent
produces **86,400 events/day/satellite × 3 satellites = 259,200 events/day** with no
meaningful keying (lat/lon changes every second).

### Event Model Option 1: Orbit Segment Aggregates

Emit one event per **orbit** (90-minute period):

- **Subject**: `satellite/swarm/{satellite_id}/orbit/{orbit_number}`
- **Kafka key**: `{satellite_id}:{orbit_number}` (e.g., `A:45678`)
- **Payload**: Summary statistics (min/max/mean field intensity, polar crossing time, geomagnetic indices)
- **Type**: `eu.esa.swarm.orbit.complete`

Consumers fetch detailed time-series via VirES API using the orbit metadata.

### Event Model Option 2: Geomagnetic Observatory Analogy

Treat Swarm as a **moving magnetometer** and emit only when passing over pre-defined
**virtual observatories** (e.g., 100 grid cells covering Earth):

- **Subject**: `geomagnetism/{grid_cell_id}` (geohash-2 or H3-2 spatial bins)
- **Kafka key**: `{grid_cell_id}` (e.g., `u2mw` = northern Europe geohash)
- **Payload**: Swarm measurements aggregated over the ~10-second window when satellite is in that grid cell
- **Type**: `eu.esa.swarm.gridcell.observation`

This reduces event rate to ~100 cells × 16 orbits/day = 1,600 events/day, with stable keys.

### Event Model Option 3: Geomagnetic Storm Alerts

Instead of raw data, emit **derived alert events** when Swarm detects:

- **Magnetic field disturbances** — |dF/dt| > 50 nT/min (storm onset)
- **Field-aligned current spikes** — FAC > 1 μA/m² (aurora substorm)
- **Plasma density dropouts** — TEC < 5 TECU (ionospheric trough)

These are **rare, high-value events** (10–100/day globally) with clear physical significance.

- **Subject**: `spaceweather/event/{event_type}` (e.g., `spaceweather/event/fac_spike`)
- **Kafka key**: `{grid_cell}:{timestamp}` (location + time of detection)
- **Payload**: Event metadata (magnitude, duration, satellite ID, QDLat/MLT coordinates)
- **Type**: `eu.esa.swarm.spaceweather.alert`

This aligns with repo's **event stream** model better than raw orbital data.

## Limitations

- **Orbital geometry** — not station-based; satellites move ~7 km/s, sweeping different regions each orbit
- **Polar bias** — polar orbits mean Arctic/Antarctic sampled every orbit; equator sampled only 2×/day at fixed longitudes
- **Single-point measurements** — Swarm measures field at satellite altitude (~450 km), not ground level
- **3-hour FAST latency** — not real-time; operational products are 2–3 days behind
- **Account registration** — requires VirES account (free but not anonymous)
- **No WebSocket/SSE** — pull-only API (HAPI or Python client)

## Why It Matters

Swarm is revolutionizing geomagnetic science:

- **IGRF-14** (International Geomagnetic Reference Field) — Swarm data anchors the global magnetic model used in navigation
- **Geomagnetic jerks** — Swarm detected sudden field changes in 2014, 2017, 2020 tied to Earth's core dynamics
- **Space weather** — Swarm field-aligned currents track aurora substorms and ionospheric disturbances
- **Earthquake precursors** — controversial but studied: magnetic anomalies before major quakes

Bridging Swarm into Kafka enables:
- **Cross-domain fusion** — magnetic storms + aurora imagery + ionosonde TEC
- **Navigation updates** — real-time magnetic declination corrections
- **Space weather alerts** — geomagnetic storm onset detection
- **Scientific discovery** — correlate magnetic field with seismic, atmospheric, oceanic phenomena

## Alternative: Ground-based Magnetometer Networks

If Swarm's orbital model is too complex, consider ground-based **magnetometer networks**
instead:

- **INTERMAGNET** — 150 observatories, 1-second cadence, open data
- **SuperMAG** — aggregates 500+ stations
- **NOAA SWPC** — real-time magnetometers (already partially covered in repo)

Ground observatories provide **fixed station IDs**, making them trivial to key. They lack
Swarm's global coverage and ionospheric plasma measurements but fit the repo pattern perfectly.

## Verdict

⚠️ **Maybe** — World-class dataset, excellent API, but **orbital track model** is fundamentally
incompatible with the repo's station/entity keying paradigm. **Build** only if:

1. Adopting an **orbit-segment or grid-cell aggregation** event model
2. Focusing on **derived alerts** (storms, FAC spikes) rather than raw orbital tracks
3. Treating it as a **reference dataset** (S3 archive + notification events) rather than streaming

**Alternative**: Bridge **INTERMAGNET ground-based magnetometers** instead for a clean station-based
fit, or wait for Swarm to inspire a **new event pattern** for orbital/moving platform data
(applicable to future LEO constellations: Planet, Spire, etc.).
