# Ministry of Water Resources Iraq - Tigris/Euphrates Monitoring

- **Country/Region**: Iraq
- **Endpoint**: `http://www.mowr.gov.iq` (unreachable), `https://www.mowr.gov.iq` (unreachable)
- **Protocol**: Unknown
- **Auth**: Unknown
- **Format**: Unknown
- **Freshness**: Unknown
- **Docs**: None accessible
- **Score**: 0/18

## Overview

The Tigris and Euphrates rivers are the lifeblood of Iraq. Both rivers originate in Turkey, flow through Syria (Euphrates) or directly into Iraq (Tigris), and converge at the Shatt al-Arab before emptying into the Persian Gulf near Basra.

Water monitoring is **critical infrastructure** for Iraq:
- **Mosul Dam** (Tigris) — largest dam in Iraq, at risk of catastrophic failure (chronic foundation grouting required)
- **Haditha Dam** (Euphrates) — second-largest, power generation
- **Agriculture** — Iraq's irrigated agriculture depends entirely on these rivers
- **Water scarcity** — upstream dam construction in Turkey and drought have reduced flow dramatically
- **Transboundary conflict** — Turkey, Syria, and Iraq dispute water allocation

The Ministry of Water Resources (MOWR) is responsible for:
- River gauge networks on Tigris and Euphrates
- Dam water level and storage monitoring
- Flood forecasting
- Irrigation system operation

**This would be the highest-value water data source for Iraq if it existed in accessible form.**

## Endpoint Analysis

**Website unreachable** — the ministry's website has been offline or blocking automated access:

```
curl http://www.mowr.gov.iq
# Result: HTTP 403 Forbidden

curl https://www.mowr.gov.iq  
# Result: HTTP 403 Forbidden
```

No alternative URLs discovered. No evidence of any API, real-time data portal, or even static data downloads.

## Search Attempts (Arabic)

Searched for:
- "وزارة الموارد المائية العراق بيانات الوقت الحقيقي"
- "مستوى نهر دجلة الفرات API"
- "mowr.gov.iq بيانات المحطات الهيدرولوجية"
- "سد الموصل مستوى المياه الوقت الحقيقي"

No real-time data feeds found from MOWR.

## Known Context

Based on international reporting and satellite analysis:
- Iraq operates river gauges on the Tigris and Euphrates, but the data is not published publicly in real-time.
- Mosul Dam water levels are monitored by the U.S. Army Corps of Engineers (USACE) and Italian contractor Trevi Group (grouting operations), but this data is not published.
- **FAO SWALIM** (Somalia Water and Land Information Management) has worked with Iraq on water data in the past, but no current real-time stream exists.
- **Copernicus GloFAS** (Global Flood Awareness System) may have modeled flow forecasts for Tigris/Euphrates, but these are models, not gauge observations.

## Alternative Approaches

Since MOWR is offline, alternative Iraq water monitoring:

1. **Satellite altimetry** — NASA/ESA satellites can measure river levels and reservoir storage from space (not real-time, days lag).
2. **Copernicus GloFAS** — modeled flood forecasts (not observations).
3. **G-REALM** (USDA/NASA) — satellite-derived reservoir and lake levels globally, includes Mosul Dam and other Iraq reservoirs (monthly updates, not real-time).
4. **Academic collaborations** — some universities (MIT, Stanford, University of Oklahoma) monitor Tigris/Euphrates via satellite but do not publish real-time streams.

**None of these are real-time gauge observations.**

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 0 | No data accessible |
| Openness | 0 | No endpoint |
| Stability | 0 | Website offline |
| Structure | 0 | N/A |
| Identifiers | 0 | N/A |
| Richness | 0 | N/A |

**Verdict**: ❌ **Skip** — This is the **highest-value missing data source** for Iraq. Tigris and Euphrates river monitoring is critical infrastructure. Mosul Dam is a potential catastrophic failure point. Upstream water disputes with Turkey and Syria make real-time flow data politically and economically vital. **But no accessible endpoint exists.** Iraq's Ministry of Water Resources does not publish real-time data. This is a frontier gap that should be re-evaluated if MOWR ever restores public data access or if international agencies (FAO, World Bank, USACE) publish Mosul Dam telemetry.
