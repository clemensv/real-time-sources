# National Water Company (NWC) - Water Network Monitoring

- **Country/Region**: Saudi Arabia (KSA)
- **Endpoint**: Unknown (likely internal SCADA only)
- **Protocol**: Unknown
- **Auth**: Unknown
- **Format**: Unknown
- **Freshness**: Real-time (water networks report continuously)
- **Docs**: https://www.nwc.com.sa (no public data)
- **Score**: 6/18

## Overview

The **National Water Company** (الشركة الوطنية للمياه, NWC) is Saudi Arabia's water and wastewater utility, serving **~15 million customers** across all regions. NWC operates:

- **Water distribution networks** — Delivering desalinated water (from SWCC) and treated groundwater to homes and businesses
- **Wastewater collection and treatment** — Sewerage networks and treatment plants
- **Storage reservoirs** — Buffer tanks to handle demand fluctuations
- **Pumping stations** — Lift water to elevated areas (Riyadh is ~600m elevation)

**Service area**: NWC covers all major Saudi cities including Riyadh, Jeddah, Dammam, Makkah, Madinah, plus smaller towns.

**Context**: Saudi water distribution faces unique challenges:
- **Extreme heat** — Pipelines in desert areas experience thermal expansion, leaks
- **High demand volatility** — Hajj season causes 40% demand spikes in Makkah/Madinah
- **Aging infrastructure** — Non-revenue water (leaks, theft) is ~20-30% in some cities
- **Chlorine decay** — Long pipelines (Riyadh is 400 km from coast) require rechlorination

Modern water utilities use **SCADA systems** to monitor:
- **Flow rates** — m³/hour in main transmission pipes
- **Pressure** — kPa at key nodes (low pressure = leaks or pump failures)
- **Water quality** — Chlorine residual, turbidity, pH (sensors in network)
- **Tank levels** — % full in reservoirs
- **Pump status** — On/off, power consumption, vibration

## Potential Data Products

If NWC published SCADA data, it could include:

1. **Network pressure** — kPa at district meter areas (DMAs)
2. **Flow rates** — m³/hour at key pipes
3. **Water quality** — Chlorine residual, turbidity at monitoring points
4. **Reservoir levels** — % full, inflow/outflow rates
5. **Pump stations** — Status (on/off), flow, energy consumption
6. **Non-revenue water** — Leak detection zone activity
7. **Demand by city** — Total m³/day for Riyadh, Jeddah, Makkah, etc.

**Update frequency**: Water SCADA typically reports every **5-60 seconds** for critical alarms, and **1-15 minutes** for trend data.

## Endpoint Analysis

**NWC website**: `https://www.nwc.com.sa`

NWC's website provides customer services (bill payment, service requests) and corporate information. **No public data portal or SCADA dashboard** is advertised.

**Comparison with water utilities**:

| Utility | Country | Public SCADA? | API? |
|---------|---------|---------------|------|
| **NWC** | Saudi Arabia | ❌ None | ❌ None |
| Sydney Water | Australia | ✅ Some (dam levels) | ✅ REST |
| Thames Water | UK | ✅ Some (reservoir levels) | ❌ None |
| Singapore PUB | Singapore | ✅ Reservoir levels | ✅ REST (data.gov.sg) |
| NYC DEP | USA | ✅ Reservoir levels | ✅ REST |

**Pattern**: Most water utilities publish **reservoir/dam levels** (public lakes, low-sensitivity), but **not network pressure or flow data** (security concern: sabotage targets).

## Integration Notes

- **No public data**: NWC does not publish network monitoring data. This is typical for water utilities worldwide.
- **Security concerns**: Real-time pressure and flow data could reveal:
  - **Weak points** (low-pressure zones vulnerable to contamination)
  - **Critical infrastructure** (pumping stations, key pipelines)
  - **Operational patterns** (predictable for sabotage)
- **Reservoir levels**: NWC **may** publish aggregate reservoir/tank levels (% storage), as this is less sensitive. However, none were found during probing.
- **Alternative: Customer consumption data** — NWC's smart meters (if deployed) track individual household usage. This data is **extremely unlikely** to be published (privacy).

**Unique value if data existed**:
- **Desert water network** — Extreme heat, long transmission distances, unique operational challenges
- **Hajj demand spikes** — 40% surge in Makkah during pilgrimage (once per year)
- **Non-revenue water** — High leak rates in some cities; monitoring improvements is valuable

However, **security barriers make this data unpublishable**.

## Scoring

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | SCADA is real-time (if data existed) |
| Openness | 0 | No public data, no API |
| Stability | 2 | NWC is the national utility; infrastructure is stable |
| Structure | 2 | Would be time-series JSON (SCADA standard) |
| Identifiers | 1 | Sensor IDs, DMA codes (if existed) |
| Additive value | 1 | Overlaps with reservoir/hydrology sources; network data is universally closed |

**Total: 9/18** (if data existed)  
**Actual: 6/18** (penalized for zero public data and security barriers)

**Verdict**: ❌ **Skip** — Water network SCADA data is **universally non-public** for security reasons. NWC is extremely unlikely to publish flow, pressure, or quality data. The only plausible data product is **reservoir/tank levels** (aggregate storage %), but none were found.

**Alternative approach**: If NWC publishes reservoir levels on **data.gov.sa** (Saudi open data portal), reassess. Reservoir data alone is low-value (snapshot every 1-24 hours, not real-time flow).

Do not pursue NWC network monitoring data unless a formal open data initiative is announced (unlikely due to security).
