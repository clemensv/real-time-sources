# Saudi Red Crescent (SRCA) - Ambulance Dispatch and Emergency Medical Services

- **Country/Region**: Saudi Arabia (KSA)
- **Endpoint**: Unknown (emergency medical services, likely closed)
- **Protocol**: Unknown
- **Auth**: Unknown
- **Format**: Unknown
- **Freshness**: Real-time (ambulance dispatch is second-by-second)
- **Docs**: https://www.srca.org.sa (no public data)
- **Score**: 7/18

## Overview

The **Saudi Red Crescent Authority** (هيئة الهلال الأحمر السعودي, SRCA) is Saudi Arabia's emergency medical services (EMS) provider, analogous to ambulance services in other countries. SRCA operates:

- **997** emergency number (medical emergencies)
- **Ambulance fleet**: ~2,000 ambulances nationwide
- **Air ambulances**: Helicopters for remote areas, Hajj
- **Emergency medical technicians** (EMTs) and paramedics
- **Blood banks** and disaster response

**Service area**: All of Saudi Arabia, with special focus on:
- **Hajj/Umrah** — 24/7 medical coverage for 2-3 million pilgrims (peak: Day of Arafah)
- **Remote areas** — Desert regions, mountain villages (helicopter evacuation)
- **Road accidents** — Saudi Arabia has one of the world's highest traffic fatality rates (~9,000 deaths/year)

**Hajj EMS**: During Hajj, SRCA deploys:
- **5,000+ staff**
- **300+ ambulances** in Makkah and holy sites
- **30+ field hospitals**
- **Air ambulances** for helicopter evacuation from Arafat, Mina

**Context**: Saudi Arabia's geography presents extreme EMS challenges:
- **Vast desert** — Response times in remote areas can be hours (helicopter required)
- **Extreme heat** — Heatstroke is common (50°C in summer)
- **Language barriers** — Hajj pilgrims from 180+ countries
- **Crowd density** — Hajj gatherings have 500,000+ people/km² at peak (stampede risk)

## Potential Data Products

If SRCA published dispatch data, it could include:

1. **Ambulance positions** — Real-time GPS locations of active ambulances
2. **Response times** — Dispatch-to-arrival times by region
3. **Call volume** — Emergencies per hour/day
4. **Incident types** — Cardiac, trauma, respiratory, etc. (anonymized)
5. **Hospital capacity** — Emergency room availability (beds, staff)
6. **Hajj medical incidents** — Heatstroke, injuries, cardiac events during pilgrimage (aggregate counts)

**Update frequency**: EMS dispatch systems (CAD — Computer-Aided Dispatch) update every **5-30 seconds** for active calls.

## Endpoint Analysis

**SRCA website**: `https://www.srca.org.sa`

The SRCA website provides news, volunteer recruitment, and blood donation info. **No public data portal or dispatch map** is advertised.

**Comparison with other EMS providers**:

| Provider | Country | Public data? | API? |
|----------|---------|--------------|------|
| **SRCA** | Saudi Arabia | ❌ None | ❌ None |
| London Ambulance | UK | ✅ Aggregate stats | ❌ None |
| FDNY EMS | USA (NYC) | ✅ Aggregate stats | ✅ Open Data portal |
| NSW Ambulance | Australia | ✅ Some | ❌ None |
| Hatzalah | Israel | ❌ None | ❌ None |

**Pattern**: **No EMS provider publishes real-time ambulance positions** publicly due to:
- **Patient privacy** — Medical calls are protected health information (HIPAA-equivalent laws)
- **Security** — Real-time ambulance locations could be exploited by criminals
- **Operational security** — Revealing coverage gaps enables exploitation

Some providers (FDNY, London) publish **aggregate statistics** (response times, call volumes) as batch data (monthly/annual reports), but not real-time dispatch.

## Integration Notes

- **No public data**: SRCA does not publish dispatch or ambulance data. This is **universal for EMS providers** (privacy + security).
- **Aggregate statistics**: SRCA may publish **annual reports** with total calls, response times, and Hajj medical incidents. These are batch data, not real-time.
- **Alternative: Hajj reports** — Ministry of Hajj and Umrah may publish post-Hajj medical statistics (total heatstroke cases, injuries, deaths). These are aggregate, not real-time.
- **Research publications**: Academic papers on Hajj medical care may include incident data, but this is historical, not real-time.

**Unique value if data existed** (but will never be published):
- **Hajj EMS** — Medical response for the world's largest gathering
- **Desert EMS** — Helicopter evacuations in extreme heat, remote areas
- **Road traffic incidents** — Saudi Arabia has high traffic fatality rates (~9,000/year); tracking EMS response would highlight road safety issues

However, **patient privacy and operational security make this impossible to publish**.

## Scoring

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | EMS dispatch is real-time (if data existed) |
| Openness | 0 | No public data, no API, patient privacy laws prohibit |
| Stability | 3 | SRCA is a permanent government agency |
| Structure | 2 | CAD systems use structured data (internal only) |
| Identifiers | 1 | Incident IDs, ambulance IDs (internal only, no public value) |
| Additive value | 1 | Globally unique Hajj EMS data, but privacy-prohibited |

**Total: 10/18** (if data existed, ignoring privacy)  
**Actual: 7/18** (penalized for zero public data and privacy barriers)

**Verdict**: ❌ **Skip** — EMS dispatch data is **universally non-public** due to patient privacy and operational security. SRCA will never publish real-time ambulance positions or medical call data. If emergency medical statistics are needed, use **SRCA annual reports** (batch data, aggregate totals).

Do not pursue real-time EMS data from any provider globally — this is prohibited everywhere.
