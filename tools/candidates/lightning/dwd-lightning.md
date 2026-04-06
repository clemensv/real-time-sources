# DWD Lightning Data (Deutscher Wetterdienst)

**Country/Region**: Germany / Central Europe
**Publisher**: Deutscher Wetterdienst (DWD) — German Meteorological Service
**API Endpoint**: `https://opendata.dwd.de/weather/lightning/`
**Documentation**: https://opendata.dwd.de/ (DWD Open Data portal)
**Protocol**: File download (HTTP)
**Auth**: None
**Data Format**: CSV-like text files
**Update Frequency**: Sub-hourly (files published in ~10-minute intervals)
**License**: DWD Open Data — free for all uses (Geodatenzugangsgesetz)

## What It Provides

DWD publishes lightning detection data from the European EUCLID (European Cooperation for Lightning Detection) network as part of its open data initiative. The data covers:

- **Lightning stroke locations** — Individual cloud-to-ground and intra-cloud discharges over Germany and surrounding regions
- **Stroke characteristics** — Peak current, polarity, type classification
- **Detection timestamps** — High temporal precision

DWD is a member of EUCLID, which operates a professional network of lightning detection sensors across Europe.

## API Details

Lightning data is published on the DWD open data server:

```
https://opendata.dwd.de/weather/lightning/
```

Files are organized in time-based directories. Each file contains lightning stroke data for a ~10-minute interval. Format is text-based with fields including:
- Timestamp
- Latitude, longitude
- Peak current (kA)
- Type (CG/IC)
- Polarity

The DWD open data server is a simple HTTP file server — no REST API, just directory listing and file download.

## Freshness Assessment

Good. Files appear in ~10-minute intervals with near-real-time stroke data. For a file-based distribution system, this is quite fresh. Not streaming, but frequent enough for many monitoring applications.

## Entity Model

Lightning stroke records include:
- Timestamp (to millisecond or microsecond)
- Geographic location (lat/lon)
- Peak current (kiloamps)
- Stroke type (cloud-to-ground, intra-cloud)
- Polarity (+/-)
- Quality metrics

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | ~10-minute file intervals, near-real-time |
| Openness | 3 | Fully open, no auth, German open data law |
| Stability | 3 | Official national met service, legally mandated open data |
| Structure | 2 | Text files, not a queryable API |
| Identifiers | 1 | No stroke IDs, timestamp+location is key |
| Additive Value | 2 | Professional-grade European lightning data, EUCLID network |
| **Total** | **13/18** | |

## Notes

- DWD's open data is among the most accessible and legally clear in Europe — mandated by German law.
- The data comes from the EUCLID network, which is a professional-grade lightning detection system (comparable in quality to Vaisala NLDN).
- Coverage is strongest in Germany and Central Europe; quality degrades with distance from sensor network.
- File-based distribution requires polling and parsing — not ideal for streaming applications but workable.
- This is one of the very few professional lightning datasets available as truly open data.
- The DWD open data server also hosts extensive weather data (radar, observations, forecasts) that could complement lightning data.
- Consider this as a higher-quality European alternative to Blitzortung for the Central European region.
