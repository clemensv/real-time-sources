# KINS IERNet — South Korea Integrated Environmental Radiation Monitoring

**Country/Region**: South Korea
**Publisher**: Korea Institute of Nuclear Safety (KINS)
**Portal**: `https://iernet.kins.re.kr/main.asp`
**API Endpoint**: None discovered
**Protocol**: Web portal only (legacy ASP, Korean-language)
**Auth**: None for website viewing
**Data Format**: HTML (no machine-readable API)
**Update Frequency**: Real-time (15-minute intervals on website)
**License**: Korean government data — terms not stated

## What It Provides

IERNet (Integrated Environmental Radiation monitoring Network) is South Korea's nationwide automatic environmental radiation monitoring system, operated by KINS. It monitors ambient gamma dose rates from 251 monitoring stations distributed across the country, with particular density around nuclear power plant sites.

Sensor types deployed:

- **HPIC** (High Pressurized Ion Chamber) — dose rate, 15-minute intervals
- **NaI(Tl) Scintillation detectors** (3"×3") — gamma spectrometry, 15-minute intervals
- **TLD** (Thermoluminescent Dosimeters) — quarterly integration

## API Details

No programmatic API was discovered. All probed paths return generic error pages:

| Path | Result |
|---|---|
| `/api/` | Error page |
| `/json/` | Error page |
| `/data/` | Error page |
| `/realtime/` | Error page |

### Accessible Pages

| URL | Content |
|---|---|
| `https://iernet.kins.re.kr/main.asp` | Main page (Korean, frames) |
| `https://iernet.kins.re.kr/iernet/ie_01.asp` | IERNet description |
| `https://iernet.kins.re.kr/iernet/ie_02.asp` | Monitoring equipment info |
| `https://iernet.kins.re.kr/information/if_01.asp` | Alert/anomaly info |

The real-time radiation display uses Flash (`/flash/information.swf`), which is non-scrapable and deprecated.

## Freshness Assessment

Real-time data exists — the website displays 15-minute interval dose rates. But there is no programmatic access to this data. The Flash-based display is a dead end for data extraction.

## Entity Model

- **Station** — 251 stations across South Korea, concentrated around nuclear facilities
- **Measurement** — gamma dose rate, gamma spectra at 15-minute intervals
- No station IDs, coordinates, or structured data available outside the web interface

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 3 | Real-time 15-min data exists on the website |
| Openness | 0 | No API, Flash-dependent, Korean-only |
| Stability | 2 | Government infrastructure but legacy technology |
| Structure | 0 | No machine-readable data format |
| Identifiers | 1 | Station names visible on website but not exported |
| Additive Value | 2 | 251 stations, major nuclear nation, not in EURDEP |
| **Total** | **8/18** | |

## Notes

- South Korea is a significant nuclear energy nation (24 operational reactors) and has one of the densest radiation monitoring networks in Asia.
- The 251-station network is comparable in density to Japan's NRA network.
- Data is real-time but completely locked behind a legacy web interface.
- Korea Open Data Portal (data.go.kr) may have some radiation data but was not probed (Korean-language interface).
- Not part of EURDEP — this data is only available through Korean sources.
- Would require HTML scraping of Korean-language ASP pages or direct contact with KINS for API access.
- Consider Safecast as a proxy for Korean radiation data if KINS data is inaccessible.
