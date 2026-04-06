# Austria E-Control Ladepunktregister

**Country/Region**: Austria
**Publisher**: E-Control (Austrian regulatory authority for electricity and gas)
**API Endpoint**: `https://www.e-control.at/marktteilnehmer/strom/e-mobilitaet/ladepunktregister` (portal, file download)
**Documentation**: https://www.e-control.at/en/marktteilnehmer/strom/e-mobilitaet/ladepunktregister
**Protocol**: File download (Excel/CSV)
**Auth**: None (public download)
**Data Format**: XLSX / CSV
**Real-Time Status**: No — static registry only
**Update Frequency**: Periodic (quarterly or as operators report changes)
**Station Count**: ~25,000+ charging points across Austria
**License**: Open government data (Austrian open data license)

## What It Provides

E-Control, Austria's energy regulator, maintains the official national register of all publicly accessible EV charging points in Austria (Ladepunktregister). Under Austrian law (Elektrizitätswirtschaftsgesetz / ElWG), charging point operators must register their infrastructure with E-Control. The register includes location data, connector types, power levels, operator information, and accessibility details.

Austria also has a vibrant community of e-mobility portals — e-tankstellen-finder.com and GoingElectric provide complementary data with user reviews and real-time community reports.

## API Details

The Ladepunktregister is published as a downloadable file (Excel format) on the E-Control website. No REST API is available.

Expected data fields (based on Austrian regulatory requirements):
- Operator name and ID
- Location: address, GPS coordinates, municipality
- Charging point specifications: connector types (Type 2, CCS, CHAdeMO), power (kW)
- Number of charging points per location
- Accessibility: 24/7 access, parking restrictions
- Authentication methods: RFID, app-based, direct payment
- Commission date

The E-Control website was undergoing restructuring in early 2026 due to the new ElWG (Elektrizitätswirtschaftsgesetz) taking effect on 24.12.2025, which may affect the exact URL and format of the register.

## Freshness Assessment

This is a regulatory registry — operators submit data as they install or modify charging infrastructure. Updates are periodic, not real-time. The register tells you what exists and where, but not whether a specific connector is currently available or occupied.

Austria is subject to EU AFIR requirements, which will mandate real-time availability data publication by 2025. The current static register may evolve into a dynamic data source as AFIR implementation progresses.

## Entity Model

- **Ladepunkt**: Individual charging point
- **Ladestation**: Charging station (groups multiple Ladepunkte)
- **Betreiber**: Operator
- **Standort**: Location with address and GPS
- **Stecker**: Connector type and power

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Static registry; periodic updates; no real-time status |
| Openness | 2 | Open data download; no API; website in transition |
| Stability | 2 | Government-operated but undergoing legal/technical restructuring |
| Structure | 1 | Excel download; no standardized API; no OCPI/OICP format |
| Identifiers | 1 | Regulatory IDs; not clear if eMI3/EVSE ID standard is used |
| Additive Value | 2 | Authoritative Austrian source; complements Bundesnetzagentur for DACH |
| **Total** | **9/18** | |

## Notes

- Austria is a mid-priority source — similar to Bundesnetzagentur in that it's an authoritative government registry but lacks real-time data and a modern API.
- The Swiss BFE data (OICP format, real-time) provides a much better model for what Austrian data could become under AFIR.
- e-tankstellen-finder.com provides a more user-friendly view of Austrian charging data with community reports, but has no public API.
- The ElWG restructuring in late 2025 may improve the data publication format — worth monitoring.
- For DACH coverage: Germany (Bundesnetzagentur), Austria (E-Control), Switzerland (BFE) are the three national registries. Switzerland is by far the most technically advanced in terms of data format and freshness.
