# Jordan Meteorological Department (JMD)

**Country/Region**: Jordan
**Publisher**: Jordan Meteorological Department, Ministry of Transport
**API Endpoint**: `https://jmd.gov.jo/` (web portal)
**Documentation**: https://jmd.gov.jo/
**Protocol**: Web portal (HTML)
**Auth**: N/A
**Data Format**: HTML (Arabic/English)
**Update Frequency**: Synoptic observations; daily forecasts
**License**: Jordanian government data

## What It Provides

Jordan's meteorological department monitors weather across a small (89,000 km²) but climatically significant country — from the Jordan Valley (Earth's lowest elevation on land) to desert plateaus. Jordan is one of the world's most water-scarce countries.

Key data:
- **Weather observations**: ~30 stations across a country the size of Indiana
- **Forecasts**: Daily weather forecasts
- **Warnings**: Flash floods (wadis), dust storms, heat waves
- **Dead Sea monitoring**: Lowest point on Earth (-430m); unique meteorological conditions
- **Water resources**: Rainfall is critical — Jordan has <100 m³ per capita per year (extreme scarcity)

### Probe Results

Not directly probed. JMD is expected to be a web-only service with Arabic-primary content.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Data exists |
| Openness | 0 | No API expected |
| Stability | 1 | Government service |
| Structure | 0 | HTML |
| Identifiers | 1 | Station names |
| Additive Value | 1 | Small network; limited unique data; Jordan covered by regional models |
| **Total** | **4/18** | |

## Verdict

Low priority. Jordan's small observation network and lack of API make this a minimal candidate. Regional weather coverage is available through ECMWF and Open-Meteo global models. Documented for completeness of Middle East coverage mapping.
