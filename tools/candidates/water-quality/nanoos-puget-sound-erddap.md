# NANOOS / ORCA Puget Sound ERDDAP

**Country/Region**: US — Puget Sound / Pacific Northwest
**Publisher**: NANOOS (Northwest Association of Networked Ocean Observing Systems) with NW Environmental Moorings / University of Washington Applied Physics Laboratory
**API Endpoint**: `https://erddap.nanoos.org/erddap/` and `https://nwem.apl.uw.edu/erddap/`
**Documentation**: https://erddap.nanoos.org/erddap/index.html and https://nwem.apl.uw.edu/
**Protocol**: ERDDAP (REST-like tabledap/griddap)
**Auth**: None
**Data Format**: JSON, CSV, NetCDF, XML, HTML and other ERDDAP outputs
**Update Frequency**: Near-real-time
**License**: Open scientific data with dataset-specific citation requirements

## What It Provides

This is the most interesting Puget Sound-specific environmental candidate I found. NANOOS and the University of Washington's Northwest Environmental Moorings publish near-real-time marine observations from ORCA and related moorings across Puget Sound. The datasets include:

- **Dissolved oxygen**
- **Salinity / conductivity**
- **Water temperature**
- **Chlorophyll**
- **Turbidity**
- Additional physical and meteorological observations for some platforms

These data are exactly the kind of station-keyed environmental telemetry that fit the repository well. Unlike general USGS freshwater feeds, this source captures the marine and estuarine dynamics that make Puget Sound unique.

## API Details

The ERDDAP installation supports the standard ERDDAP access patterns:

- `tabledap` — subset table-oriented buoy/mooring observations
- `griddap` — gridded products where applicable
- RESTful search and metadata services
- Dataset discovery through `allDatasets` and categorized metadata

The NANOOS ERDDAP homepage advertises:

- dataset search across more than 100 datasets
- machine-oriented RESTful services
- multiple output formats
- an "out-of-date datasets" status page for near-real-time monitoring
- subscription hooks for dataset changes

The ORCA/NWEM datasets are especially attractive because they expose named mooring datasets for Puget Sound locations and are already being served through a mature scientific data platform.

## Freshness Assessment

Good. This is near-real-time marine observing data, not annual or batch publication. The ERDDAP server itself has tooling specifically for monitoring near-real-time dataset staleness, which is a strong signal that the platform is designed for continuously refreshed observations. Exact cadence varies by mooring and dataset.

## Entity Model

- **Mooring / station** — named observing site with location and metadata
- **Dataset** — ERDDAP dataset ID representing an observation stream or profile family
- **Observation** — timestamped measured value, sometimes depth-resolved
- **Variable** — dissolved oxygen, salinity, temperature, chlorophyll, turbidity, meteorological context

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Near-real-time, but exact per-dataset cadence varies |
| Openness | 3 | No auth required |
| Stability | 3 | NANOOS / IOOS / UW institutional backing |
| Structure | 3 | ERDDAP is one of the best scientific data access patterns available |
| Identifiers | 2 | Dataset IDs and mooring names are usable, but identity design needs care |
| Additive Value | 3 | Unique Puget Sound marine water-quality telemetry |
| **Total** | **16/18** | |

## Notes

- This is a very good candidate if we want a **marine water quality** bridge instead of another river-gauge or general weather feed.
- ERDDAP is already represented elsewhere in the candidate inventory, which lowers implementation risk because the protocol pattern is known.
- The most important design choice would be whether to model one source around a curated set of Puget Sound moorings, or a broader ERDDAP-backed marine observation family.
- Dataset-level citation requirements should be preserved in documentation even if the runtime only needs open access.
