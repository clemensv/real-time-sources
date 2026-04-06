# ARPANSA — Australian Environmental Radiation Monitoring

**Country/Region**: Australia
**Publisher**: Australian Radiation Protection and Nuclear Safety Agency (ARPANSA)
**UV Data API**: `https://data.gov.au/data/api/3/action/package_search?fq=organization:australian-radiation-protection-and-nuclear-safety-agency-arpansa`
**Portal**: `https://www.arpansa.gov.au/`
**Protocol**: CKAN REST (data.gov.au) for UV data; web portal for ionizing radiation
**Auth**: None for data.gov.au
**Data Format**: CSV (UV data via data.gov.au)
**Update Frequency**: UV data: 1-minute resolution, published yearly; ionizing radiation: real-time on website (if accessible)
**License**: CC BY 2.5 AU (data.gov.au datasets)

## What It Provides

ARPANSA operates an Australian Environmental Radiation Monitoring Network covering ionizing radiation (gamma dose rates) at multiple locations across the country. However, only UV (non-ionizing) radiation data is published on the open data portal.

### Available on data.gov.au (UV Radiation)

13 datasets published via CKAN:

| Dataset | Location |
|---|---|
| UV Index (1-min) | Sydney, Melbourne, Perth, Brisbane, Adelaide, Darwin, Townsville, Newcastle, Gold Coast, Canberra, Alice Springs, Casey (Antarctica) |
| UV Radiation Summary | National |

Format: CSV (yearly files, e.g., `UV-Sydney-2024.csv`), 1-minute resolution.

### Not Available Programmatically (Ionizing Radiation)

The ionizing radiation monitoring data (gamma dose rates, gamma spectrometry) is displayed on the ARPANSA website dashboard, but no REST API, CSV download, or WFS service was discovered. The main arpansa.gov.au domain timed out consistently during probing — possibly geo-blocked from non-Australian networks.

## API Details

### CKAN Search (UV data)

```
GET https://data.gov.au/data/api/3/action/package_search?fq=organization:australian-radiation-protection-and-nuclear-safety-agency-arpansa&rows=20
```

Returns JSON with 13 UV radiation datasets.

### Ionizing Radiation

No endpoints found. The ARPANSA website (`www.arpansa.gov.au`) was unreachable during all probing attempts (30–45 second timeouts). The ionizing radiation monitoring data appears to exist only as an interactive web dashboard.

## Freshness Assessment

UV data: yearly CSV publications with 1-minute resolution data — high temporal resolution but batch-published. Ionizing radiation: claimed real-time on website but inaccessible for verification.

## Entity Model

- **UV Station** — named by city, 1-minute UV index readings in CSV format
- **Ionizing Radiation Station** — exists on website but no structured data available

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 2 | UV data is 1-minute resolution but yearly publication |
| Openness | 2 | UV data open on data.gov.au; ionizing data locked in portal |
| Stability | 3 | Australian government infrastructure |
| Structure | 2 | UV CSVs are clean; no ionizing radiation data structure available |
| Identifiers | 1 | City names only, no station codes |
| Additive Value | 1 | UV data is niche; ionizing data would be valuable but inaccessible |
| **Total** | **11/18** | |

## Notes

- ARPANSA's ionizing radiation data would be highly valuable — Australia is not part of EURDEP and has unique nuclear facilities (Lucas Heights reactor, uranium mining operations).
- The main website's inaccessibility may be due to geo-blocking or infrastructure issues; re-testing from an Australian network would be worthwhile.
- The UV Index data, while not ionizing radiation, could be useful for a broader environmental monitoring system.
- Australia's DEA (Digital Earth Australia) Hotspots service is excellent for wildfire data but does not include radiation monitoring.
- Contact ARPANSA directly for ionizing radiation API access.
