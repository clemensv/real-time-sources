# Chargeprice API

**Country/Region**: Europe (35+ countries) + expanding globally
**Publisher**: Chargeprice GmbH (Austria)
**API Endpoint**: Commercial API (Notion-based documentation)
**Documentation**: https://chargeprice.notion.site/ (requires contact for API access)
**Protocol**: REST
**Auth**: API Key (commercial, tiered pricing)
**Data Format**: JSON
**Real-Time Status**: Partial — focuses on pricing rather than connector availability, but includes station metadata
**Update Frequency**: Near real-time for pricing; station data refreshed regularly
**Station Count**: 500,000+ charging points across 35+ European countries
**License**: Commercial license

## What It Provides

Chargeprice is Europe's leading EV charging price comparison platform ("Der Ladetarifrechner für dein Elektroauto"). Their API provides detailed pricing information for EV charging across all major networks and tariff plans in Europe. Beyond pricing, the API includes station location data, connector types, power levels, and network information — making it useful as both a price intelligence and station registry source.

The core value proposition is answering "What will it cost to charge here with my specific tariff card?" — comparing prices across all available RFID cards, apps, and direct payment options at any given station.

## API Details

Documentation is hosted on Notion (https://chargeprice.notion.site/). API access requires registration and commercial agreement.

Based on the platform's features and industry knowledge, the API likely provides:
- Station locations with GPS coordinates
- Connector types and power levels per station
- Operator/CPO (Charge Point Operator) information
- EMP (E-Mobility Service Provider) tariff data
- Price calculation per session (based on kWh, time, flat fees, etc.)
- Network coverage mapping

Key use cases:
- Price comparison at a specific station for different tariff cards
- Cheapest charging option along a route
- Network/tariff analysis across regions
- CPO pricing intelligence

## Freshness Assessment

Pricing data is Chargeprice's core product and is actively maintained — changes in tariffs are reflected quickly. Station location data is refreshed regularly but is likely sourced from aggregators (possibly Eco-Movement, OCM, or direct CPO feeds) rather than being Chargeprice's own primary data.

Not a source for real-time connector availability. The focus is on pricing intelligence, not operational status.

## Entity Model

- **Station**: Physical charging location
- **Connector**: Type (CCS, CHAdeMO, Type 2), power (kW)
- **CPO**: Charge Point Operator (who operates the station)
- **EMP**: E-Mobility Service Provider (who sells the charging card/app)
- **Tariff**: Pricing structure per EMP at a given CPO's stations
- **Price Calculation**: Session cost based on energy, time, and fee components

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Active pricing updates; station data moderately fresh |
| Openness | 0 | Commercial API only; no free tier apparent |
| Stability | 2 | Established platform; API documented; commercial product |
| Structure | 2 | JSON API; proprietary schema focused on pricing |
| Identifiers | 2 | Station/network IDs; likely cross-references to standard EVSE IDs |
| Additive Value | 2 | Unique pricing dimension; 35+ European countries |
| **Total** | **10/18** | |

## Notes

- Chargeprice fills a unique niche — pricing transparency for EV charging. No other open source provides comparable tariff comparison data.
- For a real-time bridge focused on station availability, Chargeprice is not the right source. But for enriching station data with pricing information, it's highly valuable.
- The platform covers 35+ European countries — roughly the same footprint as EU+EEA.
- Chargeprice data could complement a station registry (AFDC, NOBIL, NDL) with pricing intelligence — "station X has 4 CCS connectors at 150 kW, and the cheapest tariff is €0.39/kWh via EnBW mobility+."
- Similar to Eco-Movement, this is a commercial data product that helps benchmark what open data sources should aspire to provide.
