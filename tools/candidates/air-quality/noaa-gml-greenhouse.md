# NOAA Global Monitoring Laboratory (GML) — Greenhouse Gases

**Country/Region**: Global
**Publisher**: NOAA (National Oceanic and Atmospheric Administration) / GML (Global Monitoring Laboratory)
**API Endpoint**: `https://gml.noaa.gov/webdata/ccgg/trends/` (data files) and `https://gml.noaa.gov/ccgg/obspack/`
**Documentation**: https://gml.noaa.gov/ccgg/trends/
**Protocol**: HTTP file distribution
**Auth**: None
**Data Format**: CSV, TXT (fixed-format)
**Update Frequency**: Monthly (trends), hourly/daily (individual stations)
**License**: US Government public domain

## What It Provides

NOAA's Global Monitoring Laboratory (GML) is the world's reference network for atmospheric greenhouse gas monitoring. It provides the definitive Mauna Loa CO₂ record (the "Keeling Curve"), global CO₂ and CH₄ trends, and measurements from ~100 sampling locations worldwide including surface observatories, tall towers, aircraft profiles, and flask sampling networks. Key products include:

- **CO₂ trends**: Global and Mauna Loa monthly means (the most-cited climate dataset in the world)
- **CH₄ (methane) trends**: Global mean and growth rate
- **N₂O (nitrous oxide) trends**: Global mean
- **SF₆ trends**: Global mean (industrial tracer)
- **Station data**: Continuous and flask measurements from global network
- **ObsPack**: Compiled observation packages for modelling

## API Details

- **CO₂ Global Trend**: `https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_gl.txt`
  - Monthly mean global CO₂ (ppm) since 1979
- **CO₂ Mauna Loa**: `https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_mlo.txt`
  - Monthly mean Mauna Loa CO₂ (ppm) since 1958
- **CH₄ Global Trend**: `https://gml.noaa.gov/webdata/ccgg/trends/ch4/ch4_mm_gl.txt`
  - Monthly mean global CH₄ (ppb)
- **N₂O Global Trend**: `https://gml.noaa.gov/webdata/ccgg/trends/n2o/n2o_mm_gl.txt`
- **File Format**: Fixed-width text with comment headers (# lines); columns: year, month, decimal date, average, trend, uncertainty
- **ObsPack**: Bundled observation files for modelling use — registration required

## Freshness Assessment

Global trend files are updated monthly with ~2-month lag. Individual station data may be updated more frequently. This is reference-grade, quality-controlled data — not real-time. The Mauna Loa record is the gold standard for climate monitoring.

## Entity Model

- **Trend** → gas (CO₂, CH₄, N₂O, SF₆) × scope (global, Mauna Loa) × month → value (ppm/ppb)
- **Station** → name, coordinates, elevation, network (surface, tower, aircraft)
- **Measurement** → station × gas × datetime → mixing ratio (ppm/ppb)
- **ObsPack** → compiled observation package for models

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 1 | Monthly trends with ~2-month lag; not real-time |
| Openness | 3 | US public domain; no auth for trend files |
| Stability | 3 | NOAA — most authoritative atmospheric monitoring agency |
| Structure | 2 | Fixed-width text files; parseable but not JSON/REST |
| Identifiers | 2 | Gas names, station codes (e.g., MLO for Mauna Loa) |
| Additive Value | 3 | Globally unique reference data; the Keeling Curve |
| **Total** | **14/18** | |

## Notes

- This is *not* real-time air quality data — it's reference-grade greenhouse gas monitoring with monthly update cadence. Include it for climate monitoring, not urban air quality.
- The Mauna Loa CO₂ record (since 1958) is arguably the single most important dataset in climate science.
- Fixed-width text format requires custom parsing — lines starting with `#` are headers/comments.
- For near-real-time greenhouse gas monitoring, Copernicus CAMS (satellite-derived) provides more frequent updates.
- NOAA GML also operates the HATS (Halocarbons and other Atmospheric Trace Species) network for ozone-depleting substances.
- ObsPack data bundles are designed for atmospheric transport modelling and require registration.
- The trend files are small (< 100 KB) and trivially easy to fetch — ideal for "current atmospheric CO₂" dashboards.
