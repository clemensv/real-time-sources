# SuperMAG — Global Ground Magnetometer Network

## Source Identity

| Field            | Value |
|------------------|-------|
| **Full Name**    | SuperMAG |
| **Operator**     | Johns Hopkins University Applied Physics Laboratory (JHU/APL) |
| **URL**          | https://supermag.jhuapl.edu/ |
| **API Base**     | `https://supermag.jhuapl.edu/services/data-api.php` |
| **Coverage**     | Global (500+ ground magnetometer stations) |
| **Update Freq.** | 1-minute cadence from contributing stations |

## What It Does

SuperMAG is a worldwide collaboration of organizations that operate ground-based magnetometers. It provides a unified interface to data from over 500 stations operated by dozens of agencies worldwide. The network computes its own magnetic indices (SME, SMU, SML — SuperMAG equivalents of AE, AU, AL) and provides baseline-subtracted magnetic field perturbations that reveal the magnetic signature of ionospheric and magnetospheric currents.

If INTERMAGNET is the "official" observatory network with strict quality standards and limited station count (~150), SuperMAG is the "big tent" — more stations, faster data availability, and derived products designed for space physics research.

## Endpoints Probed

| Endpoint | Status | Notes |
|----------|--------|-------|
| Website | ✅ 200 | Full interactive portal |
| API (no auth) | ✅ 200 | Returns "ERROR: No username" |
| API (with test logon) | ✅ 200 | Returns "ERROR: No station selected" — auth works |
| `/info/?page=rulesoftheroad` | ✅ 200 | Data usage policy |

### API Structure

The API requires a username parameter (`logon=`) obtained through free registration:

```
/services/data-api.php?service=indices&start=2026-01-01T00:00:00&extent=3600&logon={username}
```

Available services:
- `indices` — SuperMAG magnetic indices (SME, SMU, SML, etc.)
- `mag` — Individual station magnetic field data
- `declin` — Magnetic declination data
- `baseline` — Baseline values

Parameters include start time, time extent (in seconds), station selection, and output format.

## Authentication & Licensing

- **Auth**: Free registration required. Username passed as query parameter.
- **Rate Limits**: Subject to "Rules of the Road" — proper attribution required.
- **License**: Data from contributing agencies; SuperMAG-derived products available for research. Publications must acknowledge SuperMAG and contributing networks. Not strictly open data — acknowledgment and co-authorship rules apply for academic use.

## Integration Notes

The authentication requirement (free registration) is a minor hurdle but not a blocker. The API exists, responds, and has a clear parameter structure. The "Rules of the Road" are typical academic data sharing: attribute properly, share derived products, acknowledge contributors.

SuperMAG's value proposition vs. INTERMAGNET:
- **More stations** (500+ vs 150+): Better spatial coverage
- **Derived indices** (SME, SML): Substorm-specific indices not available elsewhere
- **Baseline subtraction**: Data is processed to remove secular variation, showing only space-weather-driven perturbations

The `extent` parameter (in seconds) controls the time window — e.g., 86400 for one day, 3600 for one hour.

SuperDARN (Super Dual Auroral Radar Network) is a related but separate project measuring ionospheric convection — also operated by academic collaborations but with different data access policies.

## Feasibility Rating

| Dimension                    | Score | Notes |
|------------------------------|-------|-------|
| **API Maturity & Docs**      | 2     | Working API; documentation on website; parameter-based |
| **Data Freshness**           | 3     | 1-minute cadence from contributing stations |
| **Format / Schema Quality**  | 2     | Text/CSV output; clear structure |
| **Auth / Access Simplicity** | 2     | Free registration; username in query string |
| **Coverage Relevance**       | 3     | 500+ stations globally; unique indices |
| **Operational Reliability**  | 3     | JHU/APL; long-running collaboration |
| **Total**                    | **15 / 18** | |

## Verdict

⚠️ **Maybe** — SuperMAG provides unmatched global magnetometer coverage and unique magnetic indices. The free registration requirement is minimal, but the academic "Rules of the Road" may not fit all use cases. For space weather applications that need ground-level magnetic perturbations from hundreds of stations, SuperMAG is the source. For simpler geomagnetic monitoring, NOAA SWPC and USGS provide the key data without registration. Recommended if the project expands into detailed space weather analysis.
