# Hubject — OICP Roaming Platform

**Country/Region**: Global (Europe-centric, expanding to Asia-Pacific and Americas)
**Publisher**: Hubject GmbH (Berlin, Germany)
**API Endpoint**: Commercial B2B platform (OICP protocol)
**Documentation**: https://www.hubject.com/ (partner documentation behind login)
**Protocol**: OICP (Open InterCharge Protocol)
**Auth**: Commercial B2B agreement required
**Data Format**: JSON (OICP format — same as Swiss BFE data)
**Real-Time Status**: Yes — real-time EVSE status via OICP
**Update Frequency**: Real-time (push-based via OICP)
**Station Count**: 600,000+ charging points connected globally
**License**: Commercial B2B license

## What It Provides

Hubject operates the world's largest cross-border EV charging roaming network, branded as the "intercharge" platform. Founded in 2012 by BMW, Bosch, Daimler, EnBW, innogy, and Siemens, Hubject connects CPOs and EMSPs via the Open InterCharge Protocol (OICP). When you use an RFID card or app to charge at a station operated by a different company, the authentication and billing often routes through Hubject.

The platform provides:
- EVSEData — static station and EVSE metadata
- EVSEStatus — real-time availability per EVSE
- Authorization — remote authentication of charging sessions
- CDR processing — billing and settlement

## API Details

Hubject's OICP protocol defines two key data modules:

**EVSEData (static):**
```json
{
  "EvseID": "CH*CCI*E22078",
  "ChargingStationNames": [{"lang": "en", "value": "Station Name"}],
  "Address": {"City": "Meyrin", "Country": "CHE", "PostalCode": "1217", "Street": "..."},
  "GeoCoordinates": {"Google": "46.23432 6.055602"},
  "Plugs": ["Type 2 Outlet"],
  "ChargingFacilities": [{"power": "22.0", "powertype": "AC_3_PHASE"}],
  "DynamicInfoAvailable": "true",
  "IsHubjectCompatible": true
}
```

**EVSEStatus (dynamic):**
- Per-EVSE availability: Available, Occupied, OutOfService, Unknown
- Push-based updates from CPOs

EVSE ID format: `{country}*{operator}*E{number}` (eMI3 standard).

The Swiss BFE dataset is published in OICP format — this is the same data model. Any OICP parser built for the Swiss data works with Hubject-connected sources.

## Freshness Assessment

As a roaming hub, Hubject receives real-time status pushes from connected CPOs. This is production-grade real-time data used for actual charging session authentication. However, like Gireve, all access is behind commercial agreements.

The Swiss BFE open data is effectively Hubject data published openly — Switzerland publishes its Hubject-connected EVSE data and status on data.geo.admin.ch.

## Entity Model

OICP model:
- **EVSE**: Identified by eMI3 EVSE ID, with status and capabilities
- **Charging Station**: Groups EVSEs at a physical location
- **Operator**: CPO identified by operator ID prefix
- **Charging Facility**: Power specs (kW, voltage, amperage, AC/DC)
- **Authentication Mode**: RFID, QR code, app, direct payment, Plug&Charge

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time EVSE status via OICP push |
| Openness | 0 | Commercial B2B only; no public access |
| Stability | 3 | Major global infrastructure; backed by automotive OEMs |
| Structure | 3 | OICP — well-defined industry protocol |
| Identifiers | 3 | eMI3 EVSE IDs — globally unique |
| Additive Value | 3 | Global roaming network; 600K+ points |
| **Total** | **15/18** | (but 0 for Openness blocks open-data use) |

## Notes

- Hubject is to OICP what Gireve is to OCPI/eMIP — the dominant roaming hub for that protocol family.
- The key insight: Switzerland's BFE open data IS Hubject/OICP data published openly. If other countries followed Switzerland's lead and published their Hubject-connected data as open data, we'd have real-time EVSE status across Europe.
- EU AFIR requires Member States to establish National Access Points and publish real-time data by 2025. Many will likely source this data from their Hubject/Gireve connections.
- OICP and OCPI are the two dominant roaming protocols in EV charging. A bridge that handles both formats covers most of the European market.
- Hubject shareholders include BMW, Mercedes-Benz, Bosch, Siemens, and Enel — ensuring long-term stability.
