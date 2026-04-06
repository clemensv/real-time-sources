# Denmark — Energistyrelsen / Danish Energy Agency

**Country/Region**: Denmark
**Publisher**: Energistyrelsen (Danish Energy Agency)
**API Endpoint**: No confirmed public API (data may be accessed via the Danish National Access Point)
**Documentation**: https://ens.dk/ (Energistyrelsen); https://www.registreringsportalen.dk/ (registration portal)
**Protocol**: Unknown (likely file download)
**Auth**: Unknown
**Data Format**: Unknown (likely CSV or similar)
**Real-Time Status**: Unknown — registry exists but real-time data publication unclear
**Update Frequency**: Periodic (as operators register/update)
**Station Count**: ~15,000+ public charging points in Denmark (estimate)
**License**: Danish open government data (expected)

## What It Provides

Denmark requires charging point operators to register their infrastructure with the Energistyrelsen. The registration portal (registreringsportalen.dk) serves as Denmark's National Access Point for EV charging data under EU AFIR requirements.

Denmark's EV market is growing rapidly — the country has ambitious electrification targets and a dense charging network for its size. The data should include station locations, connector types, power levels, and operator information.

Note: Denmark is NOT covered by NOBIL. Despite being a Nordic country, NOBIL only covers Norway, Sweden, and Finland. Denmark requires separate data sourcing.

## API Details

No public REST API was confirmed during research. The data may be available through:
- The registration portal (registreringsportalen.dk) — likely requires operator login
- Danish national open data portal (data.gov.dk)
- EU data portals that aggregate National Access Point data
- Open Charge Map has Danish charging data (~15,000+ locations)

Denmark's implementation of AFIR National Access Point requirements is ongoing. The exact technical implementation (API vs. file download vs. DATEX II) was not publicly documented at the time of research.

## Freshness Assessment

As a regulatory registry, the data is updated when operators register or modify their infrastructure. Real-time connector availability is the AFIR aspiration but may not yet be implemented for Denmark.

For current programmatic access to Danish charging data, Open Charge Map or NOBIL (which does NOT cover Denmark) alternatives should be considered.

## Entity Model

Expected to follow EU AFIR requirements:
- Unique charging point identifiers (eMI3/EVSE ID format)
- Location, address, GPS coordinates
- Connector types and power levels
- Operator information
- Access conditions

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Regulatory registry; periodic updates; real-time status unknown |
| Openness | 1 | Data exists but public API access unconfirmed |
| Stability | 2 | Government-operated; AFIR-mandated |
| Structure | 1 | Format unclear; likely evolving under AFIR |
| Identifiers | 2 | Expected to use eMI3 EVSE IDs under AFIR |
| Additive Value | 2 | Fills Nordic gap (NOBIL doesn't cover Denmark) |
| **Total** | **9/18** | |

## Notes

- Denmark is the notable gap in Nordic EV charging data — NOBIL covers Norway, Sweden, and Finland, but NOT Denmark.
- As EU AFIR implementation progresses, Denmark will need to publish real-time charging data via its National Access Point. This may significantly improve data availability.
- For immediate needs, Open Charge Map provides the best programmatic access to Danish charging data.
- Denmark's charging infrastructure is growing fast — Clever, E.ON, Ionity, Tesla, and Spirii are major operators.
- The Danish Energy Agency (Energistyrelsen) also publishes energy data more broadly — worth monitoring for charging data releases.
