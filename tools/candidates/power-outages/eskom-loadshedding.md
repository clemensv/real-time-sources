# Eskom Direct Loadshedding Status
**Country/Region**: South Africa
**Publisher**: Eskom Holdings SOC Ltd (South African state power utility)
**API Endpoint**: `https://loadshedding.eskom.co.za/LoadShedding/GetStatus`
**Documentation**: None (undocumented endpoint)
**Protocol**: HTTP GET (returns plain integer)
**Auth**: None
**Data Format**: Plain text (integer)
**Update Frequency**: Real-time
**License**: Public (South African government utility)

## What It Provides
Eskom's direct web endpoint exposes the current national loadshedding stage as a simple integer:
- **Stage value**: Single integer indicating current loadshedding severity
- **Interpretation**: Value minus 1 = current stage (1 = Stage 0/no loadshedding, 2 = Stage 1, etc.)
- **No area data**: Only the national stage — no per-suburb schedules
- **No metadata**: No timestamps, no forecasts, no schedule windows

## API Details
- **Status endpoint**: `GET https://loadshedding.eskom.co.za/LoadShedding/GetStatus`
  - Returns: plain integer (e.g., `1`)
  - No Content-Type header (plain text)
- **Stage mapping**:
  - 1 → Stage 0 (no loadshedding)
  - 2 → Stage 1
  - 3 → Stage 2
  - ...
  - 9 → Stage 8
- **Other potential endpoints** (not confirmed):
  - `/LoadShedding/GetScheduleM/{suburb}/{stage}/{province}`
  - These returned HTTP 500 during probing

## Probe Results
```
https://loadshedding.eskom.co.za/LoadShedding/GetStatus
  Status: 200 OK
  Body: 1
  Type: Int64
  Assessment: Working — returns current stage (1 = no loadshedding)

https://loadshedding.eskom.co.za/LoadShedding/GetScheduleM/1/1/Western%20Cape
  Status: 500 Internal Server Error
  Assessment: Schedule endpoint appears broken or requires different parameters
```

## Freshness Assessment
Excellent for the single data point it provides. The status value updates within minutes when Eskom announces a stage change. However, this is literally one integer — no schedule or area information.

## Entity Model
- **Status** (integer value, derived stage number)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Real-time stage updates |
| Openness | 3 | No auth, completely public |
| Stability | 1 | Undocumented, schedule endpoints broken |
| Structure | 1 | Single integer, no JSON, no metadata |
| Identifiers | 0 | No identifiers — single global value |
| Additive Value | 2 | Free alternative to EskomSePush for status only |
| **Total** | **10/18** | |

## Notes
- Dead simple: one GET, one integer — doesn't get easier to integrate
- But also dead simple: no area schedules, no timestamps, no forecast
- Pair with EskomSePush API for area-specific data
- The endpoint is undocumented and may change without notice
- Schedule endpoints appear broken — Eskom's web infrastructure is notoriously unstable
- Useful as a free health check / canary for loadshedding status
