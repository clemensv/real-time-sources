# WWLLN (World Wide Lightning Location Network)

**Country/Region**: Global
**Publisher**: University of Washington, Department of Earth and Space Sciences
**API Endpoint**: N/A — academic data sharing agreement required
**Documentation**: http://wwlln.net/
**Protocol**: File-based distribution / Academic data sharing
**Auth**: Academic/research data sharing agreement
**Data Format**: ASCII text files (custom format)
**Update Frequency**: Real-time for network participants; delayed distribution for data users
**License**: Academic/research use — data sharing agreement required

## What It Provides

WWLLN is a global lightning detection network operated by the University of Washington in collaboration with ~80 universities and research institutions worldwide. It detects very low frequency (VLF) radio waves from lightning to locate strokes globally.

- **Global lightning stroke locations** — Lat/lon/time for cloud-to-ground and some intra-cloud discharges
- **~50-70 stations worldwide** — Provides global coverage
- **Detection efficiency** — ~10-30% of all strokes (lower than commercial networks but truly global)
- **Location accuracy** — Median ~5-10 km

## API Details

WWLLN does not provide a public API. Data access is through:

1. **Real-time network participation** — Institutions that host a WWLLN station receive real-time data.
2. **Data sharing agreements** — Researchers can request historical and near-real-time data for academic use.
3. **Published datasets** — Some derived products have been published in research data repositories.

Data is distributed as ASCII text files with one line per stroke:
```
date, time, lat, lon, residual, stations, energy
2024/01/15, 12:34:56.789012, -33.45, 151.23, 3.2, 8, 1234
```

## Freshness Assessment

Real-time for participating stations. Delayed (hours to days) for data-sharing recipients. Not suitable for real-time open data integration.

## Entity Model

Lightning stroke records include:
- Date and time (microsecond precision)
- Latitude, longitude
- Residual (timing fit quality, microseconds)
- Number of stations contributing to location
- Estimated energy (relative)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Real-time only for network hosts |
| Openness | 1 | Academic data sharing agreement required |
| Stability | 2 | Academic network, long-running (since 2003) |
| Structure | 1 | Simple ASCII format, no REST API |
| Identifiers | 1 | No stroke IDs, timestamp+location is key |
| Additive Value | 2 | Global VLF-based coverage, academic standard |
| **Total** | **8/18** | |

## Notes

- **Effectively dismissed for open data integration** — requires academic agreement, no public API.
- WWLLN fills an important niche in research as a consistent global lightning climatology dataset.
- Detection efficiency (~10-30%) is much lower than commercial networks (>80%) or Blitzortung (varies by region).
- The network's strength is uniform global coverage including oceanic regions where other networks have gaps.
- For open real-time lightning data, Blitzortung.org is the clear alternative.
- WWLLN data has been used extensively in published research on global lightning patterns, sprite events, and ionospheric coupling.
