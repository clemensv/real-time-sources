# GCC Interconnection Authority (GCCIA) Grid Data

- **Country/Region**: GCC (Gulf Cooperation Council) — Kuwait, Saudi Arabia, UAE, Qatar, Bahrain, Oman
- **Endpoint**: Unknown (https://www.gccia.com.sa website accessible, no API documented)
- **Protocol**: Unknown
- **Auth**: Unknown
- **Format**: Unknown (website has dashboards and reports, no machine-readable endpoints found)
- **Freshness**: Unknown (website shows real-time grid status dashboard)
- **Docs**: None publicly accessible
- **Score**: ?/18 (cannot evaluate — no API discovered, but high-value potential)

## Overview

The **GCC Interconnection Authority (GCCIA)** operates the electrical grid interconnection linking all six Gulf Cooperation Council member states:

- **Saudi Arabia** (Saudi Electricity Company)
- **Kuwait** (Ministry of Electricity & Water - MEW)
- **UAE** (FEWA, ADWEA, DEWA)
- **Qatar** (Qatar General Electricity & Water Corporation - Kahramaa)
- **Bahrain** (Electricity and Water Authority - EWA)
- **Oman** (Oman Electricity Transmission Company - OETC)

**Grid capacity**:
- Total interconnection capacity: ~2,400 MW (expandable to 4,800 MW)
- North grid: Kuwait ↔ Saudi Arabia ↔ Bahrain ↔ Qatar
- South grid: UAE ↔ Oman
- Cross-link: Saudi Arabia ↔ UAE

**GCCIA functions**:
- Real-time grid balancing and energy trading across borders
- Emergency power support (load shedding prevention)
- Economic dispatch optimization
- Frequency regulation (50 Hz synchronous grid)

Kuwait's role:
- **Imports** power from Saudi Arabia during peak summer demand (June–September)
- **Exports** surplus power during mild months (December–April)
- Peak load: ~15,000 MW (summer afternoons)
- Installed capacity: ~18,000 MW (mostly natural gas and oil-fired)

## Endpoint Analysis

**Website accessible** (2025-05-23):

```
GET https://www.gccia.com.sa
```

- HTTP 200 OK
- Website is in Arabic and English
- Homepage shows real-time dashboard with:
  - Current interconnection load (MW)
  - Power flow direction between countries
  - System frequency (Hz)
  - Color-coded grid status (green = normal, yellow/red = alerts)

**No API discovered** — probing attempts:

```
GET https://www.gccia.com.sa/api
GET https://www.gccia.com.sa/api/v1/current
GET https://www.gccia.com.sa/data/live
GET https://www.gccia.com.sa/data/realtime.json
GET https://api.gccia.com.sa/v1/grid
GET https://data.gccia.com.sa/api/realtime
```

All attempts: HTTP 404 or subdomain DNS failure

**Dashboard inspection**:
- Real-time dashboard appears to load via **embedded iframe or Flash (deprecated)**
- DevTools network tab shows no obvious JSON/API calls
- Data may be pushed via proprietary protocol (e.g., SCADA, OPC UA) to internal visualization tool
- Public website is informational, not a data portal

**Reports and publications**:
- Website hosts annual reports (PDF) with historical load statistics
- Monthly bulletin (PDF) with energy exchange volumes
- No CSV/Excel downloads or machine-readable historical data

**Arabic-language searches**:
- Searched "هيئة الربط الكهربائي لدول مجلس التعاون الخليجي API" (GCCIA API) — no results
- Searched "بيانات الربط الكهربائي الخليج" (GCC grid interconnection data) — only reports and news

## Why This Would Be Valuable

If GCCIA published a real-time API, it would provide:

1. **Cross-border power flows** (MW) between Kuwait ↔ Saudi, Qatar ↔ Saudi, Bahrain ↔ Saudi, etc.
2. **Grid frequency** (50 Hz ± deviation) — indicator of supply/demand balance
3. **Energy exchange volumes** (MWh) by hour/day
4. **Emergency support activations** — when one country assists another during outages/peaks
5. **Fuel mix implications** — Kuwait imports imply gas/oil generation in Saudi displacing Kuwait's own capacity

**Use cases**:
- Energy market analysis (spot prices, trading patterns)
- Grid stability monitoring (frequency deviations)
- Climate impact (fossil fuel dispatch optimization across region)
- Geopolitical insights (energy interdependence among GCC states)

**Uniqueness**:
- No other public API (to our knowledge) publishes real-time cross-border power flows for the Middle East
- ENTSO-E (Europe) publishes similar data — GCCIA would be the Gulf equivalent

## Schema / Sample Payload

**Cannot provide** — no machine-readable endpoint discovered.

**Expected data model** (if API existed):

```json
{
  "timestamp": "2025-05-23T10:15:00Z",
  "frequency": 50.02,
  "interconnections": [
    {
      "from": "KW",
      "to": "SA",
      "flow_mw": -450,
      "capacity_mw": 1200,
      "status": "normal"
    },
    {
      "from": "SA",
      "to": "QA",
      "flow_mw": 200,
      "capacity_mw": 750,
      "status": "normal"
    }
  ],
  "countries": [
    {
      "code": "KW",
      "load_mw": 12500,
      "generation_mw": 12050,
      "net_import_mw": 450
    }
  ]
}
```

Negative flow = import, positive = export.

## Limitations

- **No public API** — Despite having real-time dashboard, GCCIA does not expose machine-readable endpoints
- **SCADA/OPC UA proprietary** — Grid control systems typically use industrial protocols (not HTTP/JSON)
- **Regulatory/security restrictions** — Grid data may be considered sensitive infrastructure information
- **Membership access** — GCCIA members (Kuwait MEW, Saudi SEC, etc.) likely have internal access, but not public
- **Arabic-first organization** — English documentation is limited, developer resources non-existent

## Alternative: National TSO APIs

Instead of a regional GCCIA API, check if individual national transmission system operators publish data:

| Country | TSO | API Status |
|---------|-----|------------|
| **Kuwait** | MEW Transmission | ❌ No public API found (www.mew.gov.kw inaccessible during probe) |
| **Saudi Arabia** | Saudi Electricity Company (SEC) | ❌ No public API documented |
| **UAE** | TRANSCO (Abu Dhabi), DEWA (Dubai) | ⚠️ DEWA has some open data (check separately) |
| **Qatar** | Kahramaa | ❌ No public API found |
| **Bahrain** | EWA | ❌ No public API found |
| **Oman** | OETC | ❌ No public API found |

**UAE (DEWA) exception**:
- Dubai Electricity & Water Authority (DEWA) has published some open data initiatives
- May include load/generation statistics (worth separate investigation)
- Not real-time, likely daily/monthly aggregates

## Verdict

**Verdict**: ❌ **Skip** — GCCIA website is accessible and shows real-time grid dashboard, but **no public API** exists. Data is likely restricted to GCCIA members or locked behind proprietary SCADA systems. Documented here as a **high-value but inaccessible source**.

**Recommendation**:
- **For pan-GCC grid monitoring**, GCCIA would be ideal if an API existed
- **For Kuwait-specific electricity data**, check if Kuwait MEW (Ministry of Electricity & Water) publishes load/generation stats (separate investigation needed)
- **For comparison**, if building Middle East energy sources, prioritize:
  1. **Israel Electric Corporation (IEC)** — publishes real-time grid data
  2. **DEWA (Dubai)** — has open data portal (check for real-time feeds)
  3. Direct contact with GCCIA or Kuwait MEW to request API access (low probability of success)

**Next steps** (if pursuing):
1. Contact GCCIA info@gccia.com.sa to inquire about API/data access (unlikely to succeed)
2. Check if Kuwait MEW (www.mew.gov.kw) publishes electricity load/generation data independently
3. Monitor GCCIA annual reports for announcements of open data initiatives
4. Check if GCC energy market liberalization drives publish transparency requirements (similar to EU)

**Cross-Gulf observation**:
If any GCC TSO publishes real-time grid data, that should be prioritized. A single GCC-wide energy bridge (if multiple TSOs publish) would be more valuable than per-country bridges. However, current state is that **none of the six GCC states appear to have public real-time electricity APIs**.
