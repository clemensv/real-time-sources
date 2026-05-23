# Saudi Electricity Company (SEC) - National Grid Load

- **Country/Region**: Saudi Arabia (KSA)
- **Endpoint**: `https://www.se.com.sa/en-us/pages/currentload.aspx` (broken)
- **Protocol**: Unknown
- **Auth**: Unknown
- **Format**: Unknown (likely HTML dashboard)
- **Freshness**: Real-time (grid load updates second-by-second)
- **Docs**: None
- **Score**: 7/18

## Overview

The Saudi Electricity Company (الشركة السعودية للكهرباء, SEC) is the monopoly electricity provider for Saudi Arabia, serving **35+ million people** across 2.15 million km². SEC is the largest utility in the Middle East by installed capacity (~85 GW as of 2024) and electricity sales (~350 TWh/year).

Saudi Arabia's electricity system has unique characteristics:

- **Extreme summer peaking** — Air conditioning drives peak demand to **~75 GW** in July-August (45-50°C temperatures). Winter baseload is ~40 GW, a 2:1 peak-to-base ratio.
- **Oil and gas dominated** — ~95% of electricity is generated from fossil fuels (natural gas, crude oil, diesel). Saudi Arabia burns **~1 million barrels/day of crude** for power in summer.
- **Desalination coupling** — ~40% of Saudi water supply comes from desalination plants, which consume ~15% of total electricity. Power outages cascade into water crises.
- **Vision 2030 transformation** — Saudi Arabia is building **~60 GW** of solar and wind by 2030 to reduce oil consumption and free crude for export. This is the world's largest renewable energy buildout by a petro-state.
- **No electricity market** — SEC operates as a vertically integrated monopoly. There is no wholesale market, no real-time pricing, and minimal transparency compared to liberalized grids (e.g., Europe, Australia, US ISOs).

**Grid structure**: Saudi Arabia's grid is divided into four regions:
1. **Central** (Riyadh) — largest load center
2. **Western** (Jeddah, Makkah, Madinah) — Hajj pilgrimage grid stress
3. **Eastern** (Dammam, Dhahran, Jubail) — oil industry, industrial load
4. **Southern** (Abha, Najran) — mountainous, lower demand

SEC is interconnected with the **GCC grid** (via GCCIA) and can import/export with UAE, Kuwait, Bahrain, Qatar, Oman.

## Endpoint Analysis

**Current Load page**: `https://www.se.com.sa/en-us/pages/currentload.aspx`

This page is **documented to exist** and historically displayed real-time electricity demand in MW for Saudi Arabia.

**Probe result**:
```
GET https://www.se.com.sa/en-us/pages/currentload.aspx
→ HTTP 200 OK, text/html; charset=utf-8
Response body: "Something went wrong, Please contact the system administrator..."
Support ID: 4099955062320314018
```

The page exists but is returning an error. Possible causes:
1. **Temporary outage** — SEC's website may be down for maintenance.
2. **WAF/access control** — The site may block automated requests.
3. **Removed feature** — SEC may have discontinued the public load dashboard.
4. **Login required** — Real-time load may now require authentication.

**No API documentation**: SEC does not publish any developer docs, API endpoints, or open data portals. The "Current Load" page was likely a simple HTML dashboard, not a JSON API.

**Historical context**: Other grid operators publish real-time load data:

| Operator | Country | Public load data? | Format | Update |
|----------|---------|-------------------|--------|--------|
| **SEC** | Saudi Arabia | ❓ Page broken | Unknown | Unknown |
| CAISO | California | ✅ Yes | JSON | 5-min |
| AEMO | Australia | ✅ Yes | CSV/JSON | 5-min |
| ERCOT | Texas | ✅ Yes | XML | 5-min |
| RTE | France | ✅ Yes | JSON | 15-min |
| ENTSO-E | Europe | ✅ Yes | XML | 30-min |

SEC is unusual in **not publishing real-time load**. Most major grid operators worldwide have moved toward transparency.

## Integration Notes

- **Page broken**: The primary obstacle is the broken "Current Load" page. Without a working endpoint, there is no data to fetch.
- **No JSON API**: Even if the page worked, it was likely an HTML dashboard (human-readable, not machine-readable). Building a bridge would require scraping, which is fragile.
- **Alternative: GCCIA**: If GCCIA (GCC Interconnection Authority) publishes cross-border flows, Saudi load could be inferred as (Saudi generation + imports - exports). However, GCCIA has no public data either.
- **Alternative: Vision 2030 dashboards**: Saudi Arabia's SDAIA (Data & AI Authority) is leading open data initiatives. SEC load data may appear on data.gov.sa in the future.
- **Unique value**: Saudi Arabia's electricity demand profile is globally unique:
  - **Largest oil consumer for power** (burning crude for electricity is rare in 2024)
  - **Fastest solar buildout** (60 GW by 2030 is larger than Germany's entire solar fleet)
  - **Hajj grid stress** (annual pilgrimage causes 40% demand spike in Makkah region)

Real-time load data would enable:
- Tracking solar integration progress (daytime load reduction as solar comes online)
- Monitoring Hajj grid stability (critical public safety)
- Analyzing oil-to-gas switching (Saudi Arabia is shifting from crude to natural gas)

## Scoring

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Grid load is real-time (if data existed) |
| Openness | 0 | Page is broken; no API |
| Stability | 2 | SEC is the national utility; website is unreliable |
| Structure | 1 | Likely HTML dashboard, not JSON |
| Identifiers | 1 | National total only (no regional breakdown confirmed) |
| Additive value | 3 | Unique dataset — largest MENA grid, oil-to-solar transition |

**Total: 10/18** (if data existed)  
**Actual: 7/18** (penalized for broken endpoint)

**Verdict**: ⏭️ **Reference** — This is a **high-value dataset that is currently inaccessible**. Saudi Arabia's grid is the largest in the Middle East and undergoing the world's most aggressive renewable energy transition. Real-time load data would track:
- Solar integration (daytime demand reduction)
- Seasonal extremes (summer air conditioning peaks)
- Hajj pilgrimage grid stress
- Oil consumption for power (declining as gas/solar grow)

**Recommended action**:
1. **Retry the endpoint** periodically — SEC's website may be temporarily down.
2. **Contact SEC** — Request API access or ask if the "Current Load" page will be restored.
3. **Monitor data.gov.sa** — Saudi Arabia's open data portal may eventually publish SEC load data.
4. **Alternative: ACWA Power** — ACWA Power is Saudi Arabia's largest private power producer (builds many of the new solar plants). They may publish generation data for their projects.

If SEC restores the load dashboard or publishes a JSON API, immediately reassess as ✅ **Build**. This would be the first Gulf Arab grid monitoring source in the repo.
