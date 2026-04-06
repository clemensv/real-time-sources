# Gireve — European EV Charging Roaming Platform

**Country/Region**: Europe (primary), expanding globally
**Publisher**: Gireve S.A.S. (France)
**API Endpoint**: Commercial B2B platform (OCPI/eMIP protocols)
**Documentation**: https://www.gireve.com/ (partner documentation behind login)
**Protocol**: OCPI v2.2 / eMIP (eMobility Inter-Operation Protocol)
**Auth**: Commercial B2B agreement required
**Data Format**: OCPI JSON / eMIP
**Real-Time Status**: Yes — real-time EVSE status via OCPI/eMIP roaming connections
**Update Frequency**: Real-time (push-based via roaming protocols)
**Station Count**: 680,000+ charging points connected
**License**: Commercial B2B license

## What It Provides

Gireve is Europe's largest B2B roaming platform for EV charging, connecting Charge Point Operators (CPOs) with E-Mobility Service Providers (EMSPs). When you use a charging card from one provider (e.g., Chargemap) to charge at another operator's station (e.g., Ionity), the roaming transaction typically routes through Gireve or Hubject.

The platform processes 1 million+ monthly transactions across 1,200+ connected operations with 13,000+ signed agreements. Gireve provides:
- Station location and static data (OCPI format)
- Real-time EVSE availability status
- Tariff information
- Transaction processing (CDR — Charge Detail Records)
- Authorization and authentication

Gireve also serves as France's de facto OCPI hub and contributes data to the French National Access Point.

## API Details

Gireve operates via standard e-mobility roaming protocols:

**OCPI (Open Charge Point Interface) v2.2:**
- Locations module — station and EVSE data
- Tariffs module — pricing information
- Sessions module — active charging sessions
- CDRs module — completed session records
- Commands module — remote start/stop

**eMIP (eMobility Inter-Operation Protocol):**
- French-origin protocol predating OCPI
- Still used by some legacy connections
- Being gradually replaced by OCPI

Access requires a commercial agreement with Gireve. There is no public/free data access.

## Freshness Assessment

As a roaming hub, Gireve receives real-time data pushes from connected CPOs whenever EVSE status changes. This is genuine real-time data — the same data that powers "available/occupied" indicators in driver-facing apps. Freshness is as good as the source CPOs provide, which for major networks is near-instantaneous.

However, all of this is behind commercial agreements. Gireve does not publish open data directly.

## Entity Model

Standard OCPI model:
- **Location**: Physical charging site
- **EVSE**: Individual charging unit with eMI3 EVSE ID and real-time status
- **Connector**: Physical plug type, power specifications
- **Tariff**: Pricing per kWh, time, session, and parking components
- **CDR**: Charge Detail Record for completed sessions

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time EVSE status via OCPI push |
| Openness | 0 | Commercial B2B only; no public access |
| Stability | 3 | Major European infrastructure; 680K+ points; regulated entity |
| Structure | 3 | OCPI v2.2 — industry standard |
| Identifiers | 3 | eMI3 EVSE IDs; OCPI UIDs |
| Additive Value | 3 | Europe-wide real-time data; 680K+ points |
| **Total** | **15/18** | (but 0 for Openness makes it impractical for open-data use) |

## Notes

- Gireve is the infrastructure behind much of Europe's EV charging interoperability. Understanding it is essential for understanding how EV charging data flows.
- For open-data projects, Gireve itself isn't accessible — but the data that Gireve routes often surfaces in open National Access Points (like the NDL Netherlands and France IRVE).
- Gireve + Hubject together cover most of Europe's roaming-enabled charging infrastructure.
- EU AFIR regulation will require that data published to National Access Points includes real-time availability — Gireve is the plumbing that makes this possible for many operators.
- Gireve also handles parking integration (booking, EV charging at parking facilities) — an emerging convergence of mobility data.
