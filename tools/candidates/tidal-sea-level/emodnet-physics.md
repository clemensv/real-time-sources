# EMODnet Physics — European Marine Observation ERDDAP

**Country/Region**: Europe (pan-European marine observations network)
**Publisher**: EMODnet (European Marine Observation and Data Network), funded by EU DG MARE
**API Endpoint**: `https://erddap.emodnet-physics.eu/erddap/`
**Documentation**: https://erddap.emodnet-physics.eu/erddap/information.html
**Protocol**: ERDDAP (OPeNDAP, WMS, REST subsets)
**Auth**: None
**Data Format**: JSON, CSV, .nc (NetCDF), .mat, .kml, HTML table, and many more
**Update Frequency**: Near real-time (aggregated from national providers; varies by source)
**License**: Open data (EMODnet open access policy)

## What It Provides

EMODnet Physics is the EU's marine observation data aggregation platform, collecting and standardizing oceanographic data from national providers across Europe. The ERDDAP server provides unified access to:

- **Sea level / tide gauge data** from European coastal stations
- **Wave height and period** from buoys
- **Sea temperature and salinity** profiles
- **Current measurements**
- **Atmospheric parameters** from marine platforms

The ERDDAP installation acts as a middleware layer — it ingests data from national sources (like SMHI, DMI, BODC, Puertos del Estado, etc.) and serves it through a standardized interface. This means a single API call pattern works for data from dozens of countries.

## API Details

ERDDAP provides multiple access patterns:

```
# Search for datasets
https://erddap.emodnet-physics.eu/erddap/search/index.html?searchFor=sea+level

# Grid datasets (griddap)
https://erddap.emodnet-physics.eu/erddap/griddap/{datasetId}.json?{variable}[{constraints}]

# Tabular datasets (tabledap)
https://erddap.emodnet-physics.eu/erddap/tabledap/{datasetId}.json?{variables}&{constraints}

# OPeNDAP access
https://erddap.emodnet-physics.eu/erddap/griddap/{datasetId}.opendap
```

ERDDAP supports output in ~15 formats: .json, .csv, .nc, .mat, .kml, .html, .tsv, .xhtml, .pdf (graphs), .png (maps), and more.

All timestamps standardized to ISO 8601 / seconds since 1970-01-01T00:00:00Z.

## Freshness Assessment

Good. Near real-time for many datasets, but latency varies by national provider. Some feeds are hours behind; some are days behind. The aggregation adds value through standardization but introduces latency compared to going directly to national APIs.

## Entity Model

- **Dataset**: datasetId, title, institution, time range, geographic bounding box
- **Station/Platform**: platform code, lat/lon, deployment type
- **Variable**: name, units, standard_name (CF conventions)
- **Observation**: time, position, value, quality flag

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Near-real-time but aggregation adds latency vs. direct national sources |
| Openness | 3 | No auth, open access |
| Stability | 2 | EU-funded project (DG MARE); depends on continued EU funding cycles |
| Structure | 3 | ERDDAP is one of the best-designed scientific data servers; RESTful; multi-format |
| Identifiers | 2 | Dataset IDs; platform codes vary by source |
| Additive Value | 3 | Single point of access for all European marine data; standardized formats |
| **Total** | **15/18** | |

## Notes

- EMODnet Physics is the "one-stop shop" for European marine observations — if you don't want to integrate 30+ national APIs, this is the shortcut.
- The ERDDAP platform is developed by NOAA and used worldwide by scientific data centers. It's well-tested and extremely capable.
- The trade-off vs. direct national APIs: EMODnet adds standardization and multi-format output at the cost of some latency and potential gaps in station-level metadata.
- Dataset discovery can be challenging — the search functionality is basic and dataset naming conventions vary.
- Particularly valuable for cross-border analysis (e.g., North Sea basin, Mediterranean) where national APIs would need to be combined manually.
- The underlying infrastructure has changed URLs in the past (was at a different domain) — monitor for URL stability.
