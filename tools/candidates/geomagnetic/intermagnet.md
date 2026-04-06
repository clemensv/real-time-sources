# INTERMAGNET

**Country/Region**: Global (150+ observatories in 40+ countries)
**Publisher**: INTERMAGNET consortium (GFZ, BGS, USGS, NRCan, IPGP, and others)
**API Endpoint**: `https://imag-data.bgs.ac.uk/GIN_V1/hapi/`
**Documentation**: https://intermagnet.github.io/, https://imag-data.bgs.ac.uk/GIN_V1/
**Protocol**: HAPI (Heliophysics Data Application Programmer's Interface) — REST-based
**Auth**: None (HAPI endpoint is public)
**Data Format**: JSON, CSV, binary (via HAPI); historical data in IAGA-2002 and CDF formats
**Update Frequency**: Preliminary data: minutes to hours; Definitive: annual publication
**License**: CC BY-NC 4.0 (default); some observatories have broader licenses

## What It Provides

INTERMAGNET is the global network of magnetic observatories operating to common standards. It provides continuous recordings of Earth's magnetic field at 150+ locations worldwide, with data at 1-second and 1-minute cadences. The measurements capture the three components of the geomagnetic field (typically X, Y, Z or H, D, Z, plus total field F) in nanotesla.

The HAPI endpoint at BGS was confirmed operational — HAPI v3.1, supporting CSV, JSON, and binary output formats. The catalog lists hundreds of datasets organized by observatory code, data grade (definitive/quasi-def/provisional/variation), cadence (PT1M/PT1S), and coordinate system (native/xyzf/hdzf/diff).

## API Details

- **HAPI Base URL**: `https://imag-data.bgs.ac.uk/GIN_V1/hapi/`
- **Capabilities**: `GET /hapi/capabilities` → output formats: csv, json, binary
- **Catalog**: `GET /hapi/catalog` → list of all available datasets
- **Dataset info**: `GET /hapi/info?id={dataset_id}` → parameters, time range, cadence
- **Data**: `GET /hapi/data?id={dataset_id}&time.min={start}&time.max={end}&format={csv|json|binary}`
- **Dataset ID format**: `{iaga_code}/{grade}/{cadence}/{orientation}` (e.g., `aae/definitive/PT1M/xyzf`)
- **Grades**: `definitive` (highest quality, annual), `quasi-def`, `provisional`, `variation` (near-real-time)
- **Cadences**: `PT1M` (1-minute), `PT1S` (1-second)
- **Orientations**: `native` (as measured), `xyzf` (geographic), `hdzf` (horizontal/declination/vertical), `diff` (differences)
- **HAPI specification**: https://hapi-server.org/ — standardized API for time-series data in heliophysics

## Freshness Assessment

Near-real-time "variation" data is available from some observatories with delays of minutes to hours. "Provisional" data appears within days. "Quasi-definitive" within 1-3 months. "Definitive" data is published annually as a DOI-referenced dataset. For real-time space weather applications, the variation data grade is the relevant one, but availability depends on individual observatories.

## Entity Model

- **Observatory**: IAGA code (3-letter, e.g., AAE = Addis Ababa), country, operating institute, coordinates
- **Dataset**: Observatory + grade + cadence + orientation → unique dataset ID
- **Time Series**: Timestamp + field components (X/Y/Z or H/D/Z + F) in nanotesla
- **Parameter**: Geomagnetic field component with units, fill value, and description

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Variation data in near-real-time; most data is delayed |
| Openness | 2 | No auth for HAPI; CC BY-NC limits commercial use |
| Stability | 3 | Global consortium running since 1991; BGS-hosted infrastructure |
| Structure | 3 | HAPI standard provides excellent structure and discoverability |
| Identifiers | 3 | IAGA observatory codes are the global standard |
| Additive Value | 3 | The global reference network for geomagnetic measurements |
| **Total** | **16/18** | |

## Notes

- HAPI is a well-designed standard for heliophysics time-series data — worth exploring as a generic data access pattern.
- The CC BY-NC license limits commercial use; individual observatories may have different terms.
- INTERMAGNET data is used by the aviation industry for compass calibration, by the oil/gas industry for directional drilling, and by space weather services.
- Definitive data published as DOIs (https://doi.org/10.5880/INTERMAGNET.1991.2020) — excellent for reproducibility.
- 1-second data is available from many observatories, providing high-resolution geomagnetic field variations.
