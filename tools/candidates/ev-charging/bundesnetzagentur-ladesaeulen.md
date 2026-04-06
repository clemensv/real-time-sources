# Bundesnetzagentur Ladesäulenregister

**Country/Region**: Germany
**Publisher**: Bundesnetzagentur (Federal Network Agency)
**API Endpoint**: https://www.bundesnetzagentur.de/DE/Fachthemen/ElektrizitaetundGas/E-Mobilitaet/Ladesaeulenkarte/start.html (map + download)
**Documentation**: https://www.bundesnetzagentur.de/SharedDocs/Downloads/DE/Sachgebiete/Energie/Unternehmen_Institutionen/E_Mobilitaet/Ladesaeulenregister.html
**Protocol**: File download (CSV/XLSX) + interactive map
**Auth**: None
**Data Format**: CSV / XLSX
**Update Frequency**: Monthly register updates; map reflects latest data
**License**: Creative Commons Attribution 4.0 International (CC BY 4.0)

## What It Provides

The Bundesnetzagentur (BNA) maintains the official German register of publicly accessible EV charging infrastructure as mandated by the Ladesäulenverordnung (LSV — Charging Infrastructure Regulation). This is the authoritative government registry for all registered public charging points in Germany. Includes operator details, address, connector types, power levels, and Public Keys for metering verification.

## API Details

There is no REST API. Data is available through:

1. **Downloadable register**: CSV/XLSX file with all registered charging points
   - Updated monthly
   - Contains: operator, address, GPS coordinates, commissioning date, connector types, power (kW), public key
   
2. **Interactive map**: Web-based map with search and filter capabilities
   - Filter by connector type (CCS, CHAdeMO, Type 2, etc.)
   - Proximity search by address
   - Individual station details on click

The downloadable register contains columns:
- Betreiber (operator)
- Straße, Hausnummer, PLZ, Ort, Bundesland (address)
- Breitengrad, Längengrad (coordinates)
- Inbetriebnahmedatum (commissioning date)
- Anschlussleistung (connection power in kW)
- Steckertypen (connector types)
- Public Key

## Freshness Assessment

The register is updated monthly. This is a regulatory filing — operators are required to report new installations to the BNA. There is no real-time availability or occupancy data; this is purely a location registry. For tracking the growth and distribution of German charging infrastructure, monthly updates are adequate. For real-time connector status, this source must be complemented by others (OCM, network-specific APIs).

## Entity Model

- **Charging Point**: A single registered charging point with location, operator, and technical specifications
- **Operator**: The company operating the charging infrastructure
- **Connector**: Type (CCS Combo 2, Type 2, CHAdeMO, Schuko), power level
- **Location**: Full German address + GPS coordinates

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Monthly file updates; no real-time data |
| Openness | 3 | CC BY 4.0, free download, no registration |
| Stability | 3 | Government regulatory register; highly stable |
| Structure | 2 | CSV/XLSX — structured but requires parsing; no API |
| Identifiers | 2 | No standardized station IDs; identified by address + operator |
| Additive Value | 2 | Authoritative for Germany but limited to static registry data |
| **Total** | **13/18** | |

## Notes

- This is a regulatory register, not a real-time API. Its value is as a reference dataset for German charging infrastructure completeness.
- No REST API exists — data must be downloaded as a file and parsed. A bridge would need to periodically fetch the CSV, diff against previous version, and emit events for new/changed stations.
- The lack of standardized station IDs is a challenge for change tracking — matching must be done by address + operator + coordinates.
- For real-time availability in Germany, Open Charge Map or network-specific APIs (Ionity, EnBW, etc.) are needed as complements.
- Germany has ~120,000+ public charging points as of 2025, making this one of the larger national registries.
