# PSMSL — Permanent Service for Mean Sea Level

**Country/Region**: Global (~1,500 stations in ~70 countries)
**Publisher**: Permanent Service for Mean Sea Level, hosted at the National Oceanography Centre (NOC), Liverpool, UK
**API Endpoint**: `https://www.psmsl.org/data/obtaining/` (download portal); station pages at `/data/obtaining/stations/{id}.php`
**Documentation**: https://www.psmsl.org/data/obtaining/
**Protocol**: HTTP file downloads (ASCII/CSV)
**Auth**: None
**Data Format**: ASCII fixed-width (RLR/Metric datasets), CSV
**Update Frequency**: Varies — annual updates for most stations; some updated more frequently
**License**: Open data; citation required (Holgate et al., 2013)

## What It Provides

The PSMSL is the global repository for long-term mean sea level data, operating since 1933. It collects, publishes, and analyses long-term sea level change information from tide gauges worldwide. This is not a real-time monitoring system — it's the authoritative archive for sea level trend analysis.

Two primary datasets:
- **RLR (Revised Local Reference)**: Quality-controlled data with a consistent datum definition. The gold standard for sea level change research. ~1,500 stations.
- **Metric**: Raw annual mean values as reported by national authorities. Broader coverage but less datum control.

Station coverage spans every continent, with records going back to the 1800s for some European stations (Amsterdam from 1700, Brest from 1807, San Francisco from 1854).

## API Details

Data access is file-based, not a REST API:

```
# Station page with metadata and data links
https://www.psmsl.org/data/obtaining/stations/{stationId}.php

# Bulk download of entire RLR dataset
https://www.psmsl.org/data/obtaining/rlr.monthly.data/rlr_monthly.zip
https://www.psmsl.org/data/obtaining/rlr.annual.data/rlr_annual.zip

# Individual station data
https://www.psmsl.org/data/obtaining/rlr.monthly.data/{stationId}.rlrdata
```

Station table on the obtaining page is sortable and includes: station name, ID, lat/lon, GLOSS ID, country, last update date.

Cross-references to GLOSS (Global Sea Level Observing System) station IDs where applicable.

## Freshness Assessment

Poor for real-time use. PSMSL is an archival service — data arrives annually from national authorities. Most stations are 1-2 years behind current date. Some update dates show "01/01/80" indicating no update since 1987. The latest updates in the verified station list show dates in 2024-2026 for actively maintained stations.

However, the historical depth is unmatched: 300+ years at Amsterdam, 200+ years at Brest, century-scale records at dozens of stations worldwide.

## Entity Model

- **Station**: PSMSL ID, name, lat/lon, coastline code, station code, country, GLOSS ID
- **RLR Record**: year (or year-month), mean sea level (mm), quality flag, datum information
- **Metric Record**: year, mean sea level (mm), missing data flag
- **Datum**: RLR datum definition linking local benchmark to a consistent reference

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 0 | Annual archival updates, 1-2 year lag — not real-time |
| Openness | 3 | Free download, no registration |
| Stability | 3 | Operating since 1933; hosted at UK NOC; internationally mandated |
| Structure | 1 | File downloads in fixed-width ASCII format; no REST API |
| Identifiers | 3 | PSMSL IDs are the global standard; cross-refs to GLOSS |
| Additive Value | 3 | The global reference dataset for sea level change; 300+ years depth |
| **Total** | **13/18** | |

## Notes

- PSMSL is not a real-time source — include it only as a reference/historical dataset for sea level trend context.
- PSMSL station IDs are the de facto global standard for identifying tide gauge locations. All other sea level datasets cross-reference to PSMSL.
- The data quality control and datum management are world-class. If you need to answer "is sea level rising at location X?", PSMSL is where you go.
- Potential use case: combine PSMSL long-term trends with real-time IOC SLSMF observations for context-aware sea level monitoring.
- The station database itself (metadata only) could be valuable as a reference gazetteer of all known tide gauge locations worldwide.
