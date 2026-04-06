# NEON — National Ecological Observatory Network Water Quality

**Country/Region**: USA (34 aquatic sites across 20 ecoclimatic domains)
**Publisher**: National Ecological Observatory Network (NEON), managed by Battelle for NSF
**API Endpoint**: `https://data.neonscience.org/api/v0/`
**Documentation**: https://data.neonscience.org/data-api
**Protocol**: REST API (JSON)
**Auth**: Optional API token for higher rate limits (free registration)
**Data Format**: JSON (metadata); CSV in ZIP bundles (data)
**Update Frequency**: Continuous in-situ sensors (1-min for streams, 5-min for lakes/rivers); data released monthly
**License**: CC0 / NEON Data Use Policy (open, attribution requested)

## What It Provides

NEON operates a continental-scale ecological observation network with 34 aquatic sites (streams, rivers, lakes) continuously monitoring water quality parameters:

- **Specific conductance** (µS/cm)
- **Dissolved oxygen** (mg/L)
- **pH**
- **Turbidity** (NTU)
- **Fluorescent dissolved organic matter** (fDOM) — QSU
- **Chlorophyll-a** (µg/L)
- **Water temperature** (°C)

Data product `DP1.20288.001` is the in-situ water quality dataset. Wadeable stream sites record at 1-minute intervals; lake and river sites at 5-minute intervals. Sites span from Alaska to Puerto Rico, covering every major US biome.

Verified API probe: the `/api/v0/sites?type=AQUATIC` endpoint returns 34 aquatic sites with metadata including coordinates, domain, and available data products.

## API Details

Two-step data access pattern:

```
# Step 1: Find available data for a product at a site
GET https://data.neonscience.org/api/v0/data/DP1.20288.001/{siteCode}/{YYYY-MM}

# Step 2: Download data files from URLs in the response
# Returns ZIP bundles with CSV files

# List all aquatic sites
GET https://data.neonscience.org/api/v0/sites?type=AQUATIC

# Product metadata
GET https://data.neonscience.org/api/v0/products/DP1.20288.001
```

The API returns JSON with data file URLs and metadata. Actual measurements are in CSV files within ZIP archives. Rate limiting applies — API tokens available for heavier use.

Sites include: ARIK (Colorado), BARC (Florida), BIGC (California), BLWA (Alabama), COMO (Colorado), CRAM (Wisconsin), HOPB (Massachusetts), KING (Colorado), LECO (Tennessee), LEWI (Virginia), MART (California), MAYF (Alabama), MCDI (Mississippi), OKSR (Alaska), POSE (Maryland), PRIN (Texas), PRLA (Wisconsin), PRPO (Wisconsin), SUGG (Florida), TOMB (Arizona), TOOK (Alaska), WALK (Virginia), WLOU (Colorado), and more.

## Freshness Assessment

Moderate for real-time use. Sensors record continuously at 1-5 minute intervals, but data is packaged and released monthly. Provisional data is available within weeks. The API provides the latest released data, not a live stream. NEON's focus is ecological research, not operational monitoring.

## Entity Model

- **Site**: siteCode, siteName, siteType, latitude, longitude, stateCode, domainCode, domainName
- **Data Product**: productCode (DP1.20288.001), productName, description
- **Data File**: fileName, url, size, md5 checksum
- **Measurement**: startDateTime, endDateTime, conductance, dissolvedOxygen, pH, turbidity, fDOM, chlorophyll, temperature, quality flags

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Continuous sensors but monthly data release cycle; not truly real-time |
| Openness | 3 | Open data; API available; CC0 license |
| Stability | 3 | NSF-funded 30-year project (2012–2042); institutional backing |
| Structure | 2 | REST API for metadata; data delivery via ZIP/CSV bundles; not streaming |
| Identifiers | 3 | Site codes, product codes, domain codes — all well-defined |
| Additive Value | 3 | Continental-scale ecological monitoring; unique multi-parameter WQ; 30-year design life |
| **Total** | **15/18** | |

## Notes

- NEON is designed for 30 years of continuous ecological observation — unmatched long-term commitment for water quality monitoring.
- The data is research-grade with extensive QC flags, calibration records, and uncertainty estimates.
- Not suitable for real-time alerting, but excellent for trend analysis and ecological research.
- The multi-parameter continuous monitoring (7 WQ parameters simultaneously) is richer than most operational networks.
- NEON's aquatic sites are co-located with terrestrial instrumentation — enables watershed-scale analysis.
- An R package (`neonUtilities`) and Python SDK exist for programmatic data access, simplifying integration.
