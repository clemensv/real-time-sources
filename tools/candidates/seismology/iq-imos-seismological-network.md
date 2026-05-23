# Iraqi Meteorological Organization & Seismology (IMOS) - Seismological Network

- **Country/Region**: Iraq
- **Endpoint**: `https://meteoseism.gov.iq` (unreachable), `http://www.meteoseism.gov.iq` (unreachable)
- **Protocol**: Unknown (site offline)
- **Auth**: Unknown
- **Format**: Unknown
- **Freshness**: Unknown
- **Docs**: None accessible
- **Score**: 0/18

## Overview

The Iraqi Meteorological Organization & Seismology (IMOS, formerly Iraq Meteorological and Seismology Organization) is the federal government agency responsible for weather forecasting and earthquake monitoring in Iraq. The organization operates under the Ministry of Transport.

IMOS is supposed to operate:
- A seismological network for earthquake monitoring (Iraq Seismological Network)
- Weather stations across Iraq
- Dust storm monitoring and forecasting (critical — Iraq is one of the world's worst-hit countries for dust/sandstorms)

The agency's website `meteoseism.gov.iq` has been offline or blocking automated access for an extended period.

## Endpoint Analysis

**Site unreachable** — multiple connection attempts failed:

```
curl https://meteoseism.gov.iq
# Result: HTTP 403 Forbidden

curl http://www.meteoseism.gov.iq
# Result: HTTP 403 Forbidden
```

No alternative endpoints discovered. No API documentation found. No evidence of FDSN-compatible web services (checked `meteoseism.gov.iq/fdsnws/event/1/query` and similar paths — all return 403).

## Search Attempts (Arabic)

Searched for:
- "المنظمة العراقية للأنواء الجوية والرصد الزلزالي API"
- "meteoseism.gov.iq بيانات زلزال"
- "رصد الزلازل العراق الوقت الحقيقي"

No evidence of any public API or real-time data feeds from IMOS found.

## Status Assessment

The Iraqi government's digital infrastructure has been severely degraded over the past decade due to:
- Chronic underfunding
- Brain drain (many qualified technicians have emigrated)
- Security issues and cyber-attacks
- Power supply problems (Iraq has severe electricity shortages)
- Lack of institutional continuity

IMOS appears to be functionally offline for public data access. It is unclear if the seismological network is even operational. If instruments are recording, the data is not being published in any accessible form.

## Alternative Coverage

Iraq earthquake monitoring is currently served by:
- **USGS** — global coverage, FDSN web services, M4.5+ events
- **EMSC** — European-Mediterranean coverage including Zagros, FDSN, better for M2.5-4.5 regional events
- **Iranian networks** — cover western Iran (Zagros), which affects Iraqi border regions

These international sources are the only available real-time earthquake data for Iraq.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 0 | Site unreachable, no evidence of real-time data |
| Openness | 0 | No API, no data access |
| Stability | 0 | Website offline/blocking |
| Structure | 0 | N/A |
| Identifiers | 0 | N/A |
| Richness | 0 | N/A |

**Verdict**: ❌ **Skip** — National seismological service is offline. No accessible endpoint. No evidence of real-time data publication. Iraq earthquake monitoring must rely on USGS and EMSC international sources. Document this as a known gap — if IMOS comes back online and publishes data, it should be re-evaluated.
