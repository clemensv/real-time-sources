# Malaysia MetMalaysia — Malaysian Meteorological Department

**Country/Region**: Malaysia
**Publisher**: Malaysian Meteorological Department (MetMalaysia)
**API Endpoint**: `https://www.met.gov.my/` (web portal — connection failed)
**Documentation**: https://www.met.gov.my/
**Protocol**: Web portal; FWIS (Forecasting and Warning Information System)
**Auth**: N/A
**Data Format**: HTML
**Update Frequency**: Hourly observations; warnings in real-time
**License**: Malaysian government data

## What It Provides

MetMalaysia monitors weather for a tropical Southeast Asian country spanning the Malay Peninsula and Borneo (33M people), facing:

- **Monsoon flooding**: Northeast monsoon (November-March) brings devastating floods to east coast states
- **Transboundary haze**: Indonesian fire smoke (annual crisis)
- **Tropical thunderstorms**: Year-round severe convection
- **Marine weather**: Strait of Malacca (one of world's busiest shipping lanes)
- **Aviation**: KLIA (Kuala Lumpur), Penang, Kota Kinabalu, Kuching airports
- **Landslides**: Cameron Highlands and other hillside areas

### FWIS Portal

MetMalaysia operates a Forecasting and Warning Information System (FWIS) at `fwis.met.gov.my` which provides:
- Real-time weather warnings
- Rainfall and river level data
- Tsunami alerts for Andaman Sea/South China Sea coast

### Probe Results

Connection to `www.metmalaysia.gov.my` **failed** (connection timeout). Also `fwis.met.gov.my/fwis/warningList.html` → connection failed. MetMalaysia web infrastructure appears to have connectivity issues from international origins.

### Malaysia Open Data

Malaysia has an impressive open data initiative:
- `data.gov.my` — Modern Next.js portal (open source on GitHub!)
- OpenDOSM — Department of Statistics open data
- KKMNOW — Ministry of Health open data

However, MetMalaysia weather data does not appear to be integrated into `data.gov.my` yet.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Data exists; website shows forecasts and warnings |
| Openness | 0 | Connection failed; FWIS also inaccessible |
| Stability | 1 | Government service; web infrastructure issues |
| Structure | 1 | FWIS suggests structured warning data; but inaccessible |
| Identifiers | 1 | Station names; state-based geography |
| Additive Value | 3 | Strait of Malacca; monsoon flooding; haze monitoring; 33M people |
| **Total** | **8/18** | |

## Verdict

Important SE Asian source but inaccessible. MetMalaysia has modern infrastructure (FWIS, mobile apps) but web access failed during testing. The Strait of Malacca dimension (40% of global trade transits) adds strategic importance beyond weather. Malaysia's impressive open data portal (data.gov.my) may eventually integrate weather data. Worth revisiting.
