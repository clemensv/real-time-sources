# GCC Interconnection Authority (GCCIA) - Regional Grid Data

- **Country/Region**: GCC (Bahrain, Kuwait, Oman, Qatar, Saudi Arabia, UAE)
- **Endpoint**: Unknown (no public API found)
- **Protocol**: N/A
- **Auth**: N/A
- **Format**: N/A
- **Freshness**: Unknown
- **Docs**: https://gccia.com.sa
- **Score**: 3/18 (estimated if data were available)

## Overview

The **GCC Interconnection Authority (GCCIA)** operates the **GCC Interconnection Grid**, a high-voltage transmission network linking the electricity systems of six Gulf Cooperation Council member states:
- Saudi Arabia (SEC, SCECO)
- Kuwait (MEW)
- Bahrain (EWA)
- Qatar (Kahramaa)
- UAE (TRANSCO, ADWEA, DEWA, SEWA)
- Oman (OETC, OPWP, Nama Power, Mazoon)

The grid enables power exchange between countries to balance supply/demand, share reserves, and optimize generation cost. Key infrastructure:
- **3,000+ km** of 400 kV transmission lines
- **4,800 MW** interconnection capacity (north-south: Saudi-Kuwait-Bahrain-Qatar-UAE; east: UAE-Oman)
- **Interchange scheduling** (day-ahead and real-time balancing)

For a real-time data bridge, the relevant data would be:
- **Cross-border power flows** (MW) between each country pair
- **Total GCC demand** and **generation by country**
- **Frequency** (50 Hz target; deviations indicate grid stress)
- **Interchange prices** or **imbalance volumes**

Similar data is publicly available from other grid operators worldwide:
- **ENTSO-E** (European grid) publishes real-time flows, generation, and prices via Transparency Platform API
- **CAISO** (California ISO) publishes 5-minute OASIS data (load, generation, interchange)
- **AEMO** (Australia) publishes 5-minute NEM dispatch data

## Endpoint Analysis

**No public API or data portal found** — investigation of the GCCIA website (gccia.com.sa) revealed:
- Corporate information (governance, projects, annual reports)
- Grid map (static image showing interconnection topology)
- News and events
- **No real-time data dashboard**
- **No public API** or data download section

The GCCIA website is **informational** (for stakeholders, media, regulators) rather than operational (for grid operators or data consumers).

Testing during discovery (2026-05-23):
```
curl -I https://gccia.com.sa
HTTP/1.1 301 Moved Permanently (redirects to https://gccia.com.sa/)
```

The site loads but contains no "Data" or "Transparency" section typical of grid operators that publish real-time data.

### Why Grid Data May Not Be Public

Unlike ENTSO-E (European Union regulatory requirement for transparency) or CAISO (U.S. FERC Order 889 open access rules), the GCC does not have a **regulatory mandate** for public disclosure of grid data. Possible reasons:
- **Commercial sensitivity**: Power prices, fuel costs, and generation mix may be considered proprietary by state-owned utilities
- **Security concerns**: Real-time grid data could be seen as critical infrastructure information
- **Lack of market competition**: GCC electricity sectors are mostly state monopolies (no competitive wholesale market requiring transparency)

Some individual GCC utilities publish limited data:
- **UAE TRANSCO** (Abu Dhabi) publishes annual peak demand but not real-time
- **Saudi SEC** publishes monthly generation statistics but not real-time SCADA
- **Oman OETC** website (oetc.om) provides general grid information but no real-time API found

## Integration Notes

- **If GCCIA published real-time data**, the value would be:
  - **Regional grid stress indicators** (demand spikes, cross-border flows during peak hours)
  - **Oman's integration with GCC grid** (imports from UAE during summer peak, exports during low-demand periods)
  - **Renewable energy penetration** (as GCC countries add solar, grid interchange patterns change)
  
  This would be **highly additive** — the repo currently has no Middle East electricity data.

- **Keying strategy**: Events would be keyed by country pair (e.g., `OM-AE` for Oman-UAE interchange) or by zone/node ID if the grid uses a nodal market model.

- **Update frequency**: Grid interchange data is typically recorded at **5-minute intervals** (same as generation dispatch) in modern grids. If GCCIA operates a real-time balancing market, data would update every 5-15 minutes.

- **Alternative: National utility APIs**: If GCCIA does not publish data, check individual GCC utilities:
  - **Oman OETC** (Oman Electricity Transmission Company) — grid operator for Oman
  - **Oman OPWP** (Oman Power and Water Procurement) — procures generation capacity
  - **Nama Power / Mazoon** — distribution companies
  
  None of these were found to have public real-time data APIs during discovery, but a direct inquiry to OETC could confirm.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 0 | No data available to assess |
| Openness | 0 | No public API or portal found |
| Stability | 1 | GCCIA is a permanent intergovernmental organization, but no data service exists |
| Structure | 1 | Unknown; assume JSON/XML if an API were developed |
| Identifiers | 1 | Country codes or zone IDs would be stable |
| Additive value | 0 | No data to bridge |

**Verdict**: ❌ Skip

**Rationale**: **No public real-time data or API was found** for the GCC Interconnection Authority or individual Omani electricity utilities (OETC, OPWP, Nama Power, Mazoon). Grid interchange data and real-time load/generation are not published publicly in the GCC region, unlike Europe (ENTSO-E) or North America (ISOs).

**Recommendations**:
1. **Contact GCCIA directly** to inquire whether:
   - Real-time grid data is available to researchers or third parties (potentially under NDA or restricted access)
   - GCCIA plans to launch a transparency platform similar to ENTSO-E
   - Annual or monthly aggregated data (not real-time) is available

2. **Contact Oman OETC** to inquire about Oman-specific grid data:
   - Real-time load (MW)
   - Generation by fuel type (gas, solar, imports)
   - Interchange with UAE via 400 kV interconnection

3. **Monitor for policy changes**: As GCC countries pursue Vision 2030 goals (renewable energy, economic diversification), **grid transparency** may increase to attract private investment in generation and storage. If a public data portal is launched, revisit this as ✅ Build.

**Low priority for immediate bridge work** — focus on sources with confirmed public APIs (seismology, weather, disasters) before pursuing restricted or unavailable grid data.
