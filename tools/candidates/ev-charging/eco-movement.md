# Eco-Movement — EV Charging Data Platform

**Country/Region**: Global (60+ countries, strongest in Europe)
**Publisher**: Eco-Movement B.V. (Netherlands)
**API Endpoint**: Commercial API (contact required)
**Documentation**: https://www.eco-movement.com/ (no public API docs)
**Protocol**: REST API
**Auth**: Commercial API key (paid)
**Data Format**: JSON (OCPI-aligned)
**Real-Time Status**: Yes — real-time EVSE status updates "within milliseconds"
**Update Frequency**: Real-time (millisecond-level dynamic updates)
**Station Count**: 700,000+ connectors in 60+ countries (per their website)
**License**: Commercial license

## What It Provides

Eco-Movement is the leading commercial EV charging data aggregator, used by Apple Maps, major OEMs, and navigation platforms worldwide. They aggregate data from all public and semi-public charging networks into a single normalized dataset that includes:
- Station locations and static metadata
- Real-time EVSE availability status
- Tariff/pricing data
- Data quality management for CPOs (Charge Point Operators)

They serve as the data backbone for much of the consumer-facing EV charging experience — when you see charging stations in Apple Maps or a car's built-in navigation, the data often comes from Eco-Movement.

## API Details

No public API documentation is available. The API is commercial and requires a business agreement.

Based on their website and industry knowledge:
- Location data: coordinates, address, operator, amenities
- Static EVSE data: connector types, power levels, access conditions
- Dynamic data: real-time availability status per EVSE
- Tariff data: pricing per network/operator
- Data coverage: 60+ countries, all major and most minor networks
- Data format: likely OCPI-aligned given their role in the ecosystem
- NAP/regulatory compliance service for CPOs

## Freshness Assessment

Eco-Movement claims real-time dynamic data "within milliseconds" — they have direct integrations with charging networks and roaming hubs (Hubject, Gireve) that provide push-based status updates. For real-time connector availability, this is as close to the source as you can get without being a charging network yourself.

However, this is a commercial service. The data is not openly available.

## Entity Model

Likely follows OCPI model:
- **Location**: Physical charging site
- **EVSE**: Individual charging unit with real-time status
- **Connector**: Physical plug with type, power specs
- **Tariff**: Pricing structure

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time EVSE status, millisecond updates |
| Openness | 0 | Commercial license only; no public/free access |
| Stability | 3 | Major commercial platform; used by Apple Maps, OEMs |
| Structure | 3 | Industry-standard format; OCPI-aligned |
| Identifiers | 3 | EVSE IDs compatible with roaming standards |
| Additive Value | 3 | Largest aggregator; 60+ countries; 700K+ connectors |
| **Total** | **15/18** | |

## Notes

- Eco-Movement is the "Bloomberg Terminal" of EV charging data — comprehensive, high-quality, real-time, and expensive.
- They are the preferred data connector for Apple Maps EV charging features.
- For an open-data project, Eco-Movement itself isn't usable — but understanding what they offer helps benchmark what open sources lack.
- They also provide data management services for CPOs, helping operators comply with NAP (National Access Point) regulations under EU AFIR.
- Eco-Movement's existence demonstrates the market value of aggregated, normalized, real-time EV charging data — exactly what open data sources are slowly building toward.
- If budget were no constraint, Eco-Movement + AFDC would cover the world with real-time connector-level data.
