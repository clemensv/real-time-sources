# Bahrain Electricity & Water Authority (EWA) - Grid and Water Network Data

- **Country/Region**: Bahrain (BH)
- **Endpoint**: Unknown (no public API found)
- **Protocol**: N/A
- **Auth**: N/A
- **Format**: N/A
- **Freshness**: Unknown
- **Docs**: https://www.ewa.bh (informational site only)
- **Score**: 2/18

## Overview

The Electricity & Water Authority (EWA) is Bahrain's state-owned utility responsible
for electricity generation, transmission, distribution, water production (desalination),
and water distribution across the Kingdom. EWA operates:

**Electricity:**
- Total generation capacity: ~4,000 MW (combined cycle gas turbines, steam turbines)
- Peak demand: ~3,000 MW (summer, due to air conditioning load)
- Fuel: Natural gas (domestic production and imports)
- Interconnection: Member of GCC Interconnection Authority (GCCIA) grid
- Substations: 100+ across the Kingdom
- Renewable energy: Solar PV integration under Energy Transition Plan (2023+)

**Water:**
- Total production capacity: ~140 MIGD (million imperial gallons per day)
- Desalination plants: Multiple facilities (MSF, RO technologies)
- Groundwater: Limited extraction (aquifers are stressed and saline intrusion is an issue)
- Distribution network: Serves all households and businesses in Bahrain
- Storage: Reservoirs and elevated tanks for supply reliability

**Data EWA likely collects but does not publish publicly:**
- **Real-time grid load**: Total electricity demand (MW) by hour/minute
- **Generation dispatch**: Output by power plant (MW, fuel type)
- **Cross-border flows**: Imports/exports via GCCIA interconnection (MW, direction)
- **Outages**: Planned maintenance and unplanned outages by area
- **Water production**: Daily/hourly output by desalination plant (MIGD or m³)
- **Water storage levels**: Reservoir and tank levels (% of capacity)
- **Water consumption**: Metered usage by sector (residential, industrial, agricultural)
- **Solar generation**: Output from distributed rooftop PV systems under net-metering
  program

This data would be analogous to what utility companies publish in more transparent
markets (e.g., UK Power Networks outage map, AEMO 5-minute dispatch data in Australia,
US utility outage maps).

## Endpoint Analysis

**EWA website reviewed:**
```
GET https://www.ewa.bh
```
**Result:** Website loads successfully, but no public data portal or API found
- Site focuses on customer services (bill payment, account management), sustainability
  initiatives (Energy Transition Plan, solar programs), and corporate information
- No "Open Data," "Statistics," or "Developer API" sections
- No real-time dashboards for grid load, outages, or water production
- Site mentions "smart app" for customers (EWA mobile app) but does not document API
  or data feeds

**Site content includes:**
- **EWA in Numbers** section: Static figures (total generation capacity, total water
  production, number of substations) but no live data or time-series
- **Sustainability initiatives**: Energy Transition Plan, Net-Metering/Net-Billing for
  solar, KAFA'A energy efficiency program
- **Customer services**: Bill viewing, payment, consumption tracking (account-specific,
  not public)

**Mobile app review (not tested):**
EWA mentions a "smart app" for iOS/Android that allows customers to:
- View and pay bills
- Monitor energy and water usage
- Get support
- Toggle between accounts

If the app includes real-time or near-real-time consumption tracking, it likely has an
API backend (for authenticated users). However, this would be **customer-specific data**,
not system-wide grid or water network data suitable for public bridging.

**No evidence found for:**
- Public real-time grid load dashboard
- Outage map or planned maintenance schedule (public-facing)
- Water production statistics by plant or day
- Historical time-series data downloads (CSV, JSON, API)
- Developer documentation or data portal

**Comparison to transparent utilities:**
- **UK Power Networks** (electricity): Real-time outage map, planned work map, power cut
  history, all via public API
- **AEMO** (Australia): 5-minute electricity dispatch data, prices, renewable generation,
  interconnector flows, all via API
- **CAISO, ERCOT, PJM** (US ISOs): Real-time load, generation by fuel type, prices,
  some via API/CSV downloads
- **Singapore PUB** (water): Water level dashboards for reservoirs, some data downloads

EWA does **not** follow the transparency model of these utilities. Grid and water data
are treated as operational/internal information, not public goods.

## Integration Notes

**Why EWA data would be valuable:**
- **Energy domain**: Extends repo coverage to Gulf electricity markets (currently
  Euro-focused via ENTSO-E)
- **Island grid**: Bahrain is a small, isolated grid (though connected to GCCIA for
  backup). Real-time load and generation data would show daily/seasonal patterns,
  renewable integration, and interconnection dependency.
- **Water scarcity context**: Bahrain is one of the most water-scarce countries
  globally. Real-time desalination output and reservoir levels would provide insights
  into water security.
- **Climate adaptation**: Bahrain's Energy Transition Plan and solar integration make
  it a case study for fossil-fuel-dependent grids transitioning to renewables.

**Current blockers:**
- No public API or data portal
- EWA treats operational data as internal/commercial information
- No regulatory requirement for transparency (unlike EU electricity markets)
- Customer-facing app (if it has an API) is authenticated and user-specific, not
  system-wide

**Potential future developments:**
- **Energy Transition Plan**: As Bahrain integrates more solar and renewable energy,
  transparency may increase (to demonstrate progress and manage public expectations)
- **Net-metering dashboard**: EWA could publish aggregated statistics on distributed
  solar generation from net-metered rooftop systems
- **Outage transparency**: Customer pressure for outage maps and real-time updates
  during maintenance/failures
- **GCCIA interconnection**: If GCCIA adopts an ENTSO-E-style transparency platform,
  EWA's cross-border flows would become visible
- **Data.gov.bh integration**: If Bahrain's open data portal becomes operational, EWA
  could publish monthly/daily aggregates (total generation, total water production,
  peak demand, etc.)

**Recommended next steps:**
1. **Contact EWA public affairs office**: Inquire about plans to publish grid load,
   generation, or water production data
2. **Test mobile app API** (if ethically permissible): Reverse-engineer app API to see
   if it exposes real-time consumption data (customer-specific, not bridgeable, but
   informative for future developments)
3. **Monitor Energy Transition Plan progress**: Watch for transparency commitments or
   renewable energy dashboards
4. **Check data.gov.bh**: If CKAN portal becomes functional, search for EWA datasets
5. **GCCIA monitoring**: If GCCIA publishes interconnection data, Bahrain's cross-border
   flows would become visible (partial substitute for direct EWA data)

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 0 | No real-time data found |
| Openness | 0 | No public access |
| Stability | 1 | EWA is stable state-owned utility, but no API exists |
| Structure | 0 | N/A |
| Identifiers | 1 | Could key by plant/substation/district, but not applicable without data |
| Additive value | 0 | Cannot assess without endpoint |

**Verdict**: **Not viable at this time**. EWA likely collects real-time electricity
grid load, generation dispatch, water production, and outage data, but **does not
publish this information publicly**. The EWA website focuses on customer services and
corporate information, with no open data portal, API, or real-time dashboards. This
**could become viable** if EWA adopts transparency practices common in more open
electricity markets (UK, Australia, parts of US) or if Bahrain's Energy Transition
Plan includes data publication commitments.

**Recommendation**: Contact EWA to inquire about open data plans and monitor Energy
Transition Plan announcements for transparency initiatives. If GCCIA publishes
interconnection data, that would provide partial visibility into Bahrain's grid
(cross-border flows). In the meantime, focus on the confirmed source: Aviation Weather
API (OBBI METAR) and investigate OpenAQ (air quality) and AISstream (maritime) as
potential Bahrain coverage options.
