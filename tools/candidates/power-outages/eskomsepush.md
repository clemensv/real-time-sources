# EskomSePush API (South Africa Loadshedding)
**Country/Region**: South Africa
**Publisher**: EskomSePush (third-party developer service)
**API Endpoint**: `https://developer.sepush.co.za/business/2.0/`
**Documentation**: https://eskomsepush.gumroad.com/l/api
**Protocol**: REST/JSON
**Auth**: API key (paid, via Gumroad)
**Data Format**: JSON
**Update Frequency**: Real-time (loadshedding schedule changes propagate immediately)
**License**: Commercial API (paid tiers)

## What It Provides
EskomSePush is South Africa's most-used loadshedding app, and its API provides:
- **Current loadshedding status**: National stage level (0-8)
- **Area schedules**: When power will be off for specific suburbs/areas
- **Area search**: Find your area by name or GPS coordinates
- **Events/calendar**: Upcoming loadshedding windows
- **Allowance system**: API calls tracked per tier (free tier: 50 calls/day)

Loadshedding is South Africa's rolling blackout system where Eskom (state utility) cuts power to areas on a schedule to prevent grid collapse. Stages 1-8 indicate severity (Stage 8 = 12+ hours/day without power).

## API Details
- **Status**: `GET /business/2.0/status` — current national loadshedding stage
- **Area search**: `GET /business/2.0/areas_search?text={query}` — find area by name
- **Area info**: `GET /business/2.0/area?id={area_id}` — schedule for specific area
- **Areas nearby**: `GET /business/2.0/areas_nearby?lat={lat}&lon={lon}` — GPS lookup
- **Topics nearby**: `GET /business/2.0/topics_nearby?lat={lat}&lon={lon}` — nearby topics
- **Allowance**: `GET /business/2.0/api_allowance` — remaining API calls
- **Auth header**: `Token: {api_key}`
- **Response**: JSON with proper error messages (confirmed: `{"error":"invalid token"}` on 403)

## Probe Results
```
https://developer.sepush.co.za/business/2.0/status
  Status: 403 Forbidden
  Content-Type: application/json
  Body: {"error":"invalid token"}
  Assessment: CONFIRMED PRODUCTION API — requires valid API key

https://loadshedding.eskom.co.za/LoadShedding/GetStatus
  Status: 200 OK
  Body: 1 (integer — Stage 0, no loadshedding)
  Assessment: Free Eskom direct endpoint (limited, no area data)
```

## Freshness Assessment
Excellent. The API reflects loadshedding stage changes within minutes. During active loadshedding (common in South Africa), the status can change multiple times per day. Area schedules update when Eskom publishes new rotation tables.

## Entity Model
- **Status** (stage: 0-8, stage_updated timestamp)
- **Area** (id, name, region, municipality)
- **Event** (start, end, note — loadshedding window)
- **Schedule** (days[], date, name, stage)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Real-time stage changes |
| Openness | 1 | Paid API key required |
| Stability | 2 | Third-party service (not Eskom itself) |
| Structure | 3 | Clean REST JSON with proper error handling |
| Identifiers | 2 | Area IDs specific to EskomSePush |
| Additive Value | 3 | Only API for South African loadshedding schedules |
| **Total** | **14/18** | |

## Notes
- EskomSePush is used by millions of South Africans daily
- The free Eskom direct endpoint (`GetStatus`) returns only the national stage as an integer — no area data
- API key costs are modest (free tier: 50 calls/day; paid tiers available)
- Loadshedding data is uniquely South African — no equivalent exists elsewhere
- Stage interpretation: 1 = current stage minus 1 (value 1 = Stage 0 = no loadshedding)
- Consider using the free Eskom endpoint for status monitoring + EskomSePush API for area details
- The service has survived multiple Eskom website changes — more resilient than direct scraping
