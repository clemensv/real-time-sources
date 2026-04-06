# SHOM REFMAR (Réseau de Référence des Observations Marégraphiques)

**Country/Region**: France (metropolitan + overseas territories)
**Publisher**: SHOM (Service Hydrographique et Océanographique de la Marine), under the Secrétariat Général de la Mer
**API Endpoint**: `https://data.shom.fr/` (WFS/WMS services); `https://services.data.shom.fr/` (data services)
**Documentation**: https://refmar.shom.fr/ ; https://data.shom.fr/
**Protocol**: OGC WFS / WMS; direct download
**Auth**: Free account on data.shom.fr for downloads
**Data Format**: CSV, XML, GeoJSON (via WFS)
**Update Frequency**: Real-time (minutes-level from operational tide gauges)
**License**: Open data (Licence Ouverte / Etalab 2.0 for most products)

## What It Provides

REFMAR coordinates France's national tide gauge observation network. It provides real-time sea level data from approximately 50+ operational tide gauges across:

- Metropolitan France (Atlantic, Channel, Mediterranean coasts)
- French overseas territories (Guadeloupe, Martinique, Réunion, Polynesia, New Caledonia, etc.)

Data includes:
- Real-time sea level observations (water height above chart datum)
- Historical tide gauge records
- Station metadata and geodetic references
- Tidal predictions

Partners include HAROPA PORT (Le Havre, Rouen), Géoazur (Senetosa, Corsica), and other port authorities and research labs.

## API Details

Data is primarily accessed through the data.shom.fr portal, which provides:

- **Interactive map viewer**: Explore tide gauge locations and view real-time data
- **WFS service**: OGC Web Feature Service for machine-readable access to station metadata and observations
- **Direct download**: CSV files for station data series

The portal is built on a modern web stack (JavaScript SPA). Programmatic access requires:
1. Creating a free account on data.shom.fr
2. Using WFS endpoints with proper layer names

Station identification uses SHOM station codes and REFMAR identifiers.

Note: The old `services.data.shom.fr/maregraphie/` endpoint appears to have been deprecated. The current access path is through the main data.shom.fr portal and its WFS services.

## Freshness Assessment

Good. Operational tide gauges report in real-time with minute-level updates. The data is primarily oriented toward operational maritime safety (port operations, coastal flood warning). Historical data extends back decades for some stations.

## Entity Model

- **Station**: SHOM code, REFMAR ID, name, latitude, longitude, partner organization
- **Observation**: timestamp, water level (m), datum reference (chart datum / IGN69)
- **Prediction**: tidal prediction for comparison with observations

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time operational tide gauges |
| Openness | 2 | Open license but requires free account; WFS access not well-documented |
| Stability | 3 | Government-backed (French Navy hydrographic service), operational for decades |
| Structure | 1 | Heavy reliance on map portal (SPA); WFS endpoints exist but aren't well-publicized |
| Identifiers | 2 | SHOM codes, REFMAR IDs; cross-refs to IOC/GLOSS less obvious |
| Additive Value | 2 | French overseas territories provide unique Pacific/Caribbean/Indian Ocean coverage |
| **Total** | **13/18** | |

## Notes

- The major challenge here is API discoverability. SHOM has moved to a modern SPA-based portal (data.shom.fr) that makes programmatic access harder to discover than the old RESTful endpoints.
- French overseas territories are the real value-add — tide gauges in French Polynesia, New Caledonia, Réunion, and Caribbean islands provide coverage in regions with sparse data.
- Many of the same stations also feed into the IOC SLSMF, so there's overlap. The direct SHOM access provides datum-referenced data (which IOC SLSMF does not).
- The 5th REFMAR conference is scheduled for September 2026, suggesting active ongoing development.
- Worth monitoring for improved API access as SHOM modernizes its data infrastructure.
