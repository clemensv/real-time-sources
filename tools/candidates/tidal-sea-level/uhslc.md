# University of Hawaii Sea Level Center (UHSLC)

**Country/Region**: Global (approximately 500 stations, strong Pacific/tropical coverage)
**Publisher**: University of Hawaii at Manoa, School of Ocean and Earth Science and Technology (SOEST)
**API Endpoint**: `https://uhslc.soest.hawaii.edu/opendap/` (OPeNDAP/THREDDS)
**Documentation**: https://uhslc.soest.hawaii.edu/data/
**Protocol**: OPeNDAP / THREDDS / direct file download (NetCDF, CSV)
**Auth**: None (open access; some datasets have attribution requirements)
**Data Format**: NetCDF, CSV, ASCII
**Update Frequency**: Fast-delivery data updated within 1–2 months of collection; research-quality data on annual cycle
**License**: Open; some stations require attribution (e.g., South Africa SANHO)

## What It Provides

The UHSLC is a major GLOSS data center that collects, quality-controls, and distributes tide gauge data from around the world. It focuses particularly on Pacific island nations and developing countries that lack their own data infrastructure. Two primary products:

- **Fast-Delivery (FD)**: Hourly sea level data available within weeks of collection, preliminary QC. Approximately 500 stations.
- **Research Quality (RQ)**: Fully quality-controlled hourly data with careful datum control, released annually. ~900 station-years.

The UHSLC also maintains a joint archive with the National Centers for Environmental Information (NCEI) for long-term archival.

## API Details

Data access via OPeNDAP (Hyrax 1.17.0) at `https://uhslc.soest.hawaii.edu/opendap/`:

- `/fast/` — Fast-delivery hourly data (NetCDF)
- `/rqds/` — Research-quality daily/hourly data (NetCDF)
- `/bulk/` — Bulk download packages

OPeNDAP supports programmatic subsetting — clients can request specific variables, time ranges, and spatial subsets without downloading entire files.

Direct file downloads also available at:
- `https://uhslc.soest.hawaii.edu/data/netcdf/fast/hourly/` (individual station files)
- `https://uhslc.soest.hawaii.edu/data/csv/fast/hourly/` (CSV format)

Station identifiers: UHSLC station numbers (e.g., `h001` for Pago Pago).

## Freshness Assessment

Good for a research-grade dataset. Fast-delivery data is typically 1–4 weeks behind real-time. This is not a real-time feed in the strict operational sense — the IOC SLSMF covers the same stations with lower latency. However, UHSLC's QC is significantly more thorough than raw GTS feeds, and the fast-delivery product bridges the gap between raw real-time and full research quality.

## Entity Model

- **Station**: UHSLC number, name, country, latitude, longitude, GLOSS ID
- **TimeSeries**: hourly sea level (mm), datum reference, time span
- **Dataset**: fast-delivery vs. research-quality, version, QC level

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Fast-delivery is weeks behind; not real-time |
| Openness | 3 | Fully open, no auth required |
| Stability | 3 | Operational since 1980s, NOAA/university-funded |
| Structure | 2 | OPeNDAP/NetCDF is well-structured but requires specialized clients |
| Identifiers | 3 | UHSLC numbers cross-referenced to GLOSS, PSMSL, national IDs |
| Additive Value | 2 | Overlaps heavily with IOC SLSMF but offers superior QC |
| **Total** | **14/18** | |

## Notes

- The UHSLC is the definitive source for quality-controlled Pacific island tide gauge data. Many small island developing states (SIDS) have their only tide gauge data curated here.
- Not a real-time service — use IOC SLSMF for operational/real-time needs, UHSLC for research-grade archives.
- OPeNDAP access requires NetCDF-aware clients (e.g., `xarray` in Python, `ncdf4` in R).
- The BOM Pacific Sea Level Monitoring Project (see separate entry) provides faster updates for some of the same Pacific stations.
- Some data providers (e.g., South Africa SANHO) require explicit permission for use — check per-station attribution requirements.
