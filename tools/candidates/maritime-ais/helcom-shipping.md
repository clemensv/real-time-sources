# HELCOM Shipping Data — Baltic Sea AIS-Derived Intelligence

**Country/Region**: Baltic Sea (9 littoral states)
**Publisher**: HELCOM (Baltic Marine Environment Protection Commission / Helsinki Commission)
**API Endpoint**: `https://shipping-data-helcom.hub.arcgis.com/` (ArcGIS Hub)
**Documentation**: https://helcom.fi/baltic-sea-trends/data-maps/, https://maps.helcom.fi/
**Protocol**: ArcGIS REST / OGC WMS / WFS
**Auth**: None (open access for most data)
**Data Format**: GeoJSON, Shapefile, CSV, WMS images
**Update Frequency**: Annual/periodic updates (AIS-derived aggregate data)
**License**: HELCOM data policy (open for non-commercial use)

## What It Provides

HELCOM is the intergovernmental organization governing the protection of the Baltic Sea
marine environment. As part of its mandate, HELCOM collects and publishes shipping-related
data derived from AIS vessel tracking across the Baltic Sea.

Available data categories:

**Shipping Data Platform** (ArcGIS Hub at `shipping-data-helcom.hub.arcgis.com/`):
- Vessel traffic intensity maps (AIS-derived)
- Shipping accident data (from EMSA/EMCIP, verified by HELCOM Maritime)
- Illegal oil spill observations (aerial surveillance data)
- Shipping emissions estimates
- Ballast water management data

**AIS Traffic Intensity** (via HELCOM MADS):
- Annual vessel traffic intensity grids for the Baltic Sea
- Derived from shore-based AIS data from all 9 Baltic states
- Breakdown by vessel type
- Historical time series (available since ~2006)
- Metadata: `https://metadata.helcom.fi/geonetwork/srv/eng/catalog.search#/metadata/2558244b-0cea-46e9-8053-af6ef5d01853`

**Map and Data Service (MADS)**:
- `https://maps.helcom.fi/website/mapservice/`
- Shipping → Traffic intensity category
- View, search, and download capabilities

## API Details

### ArcGIS Hub (shipping-data-helcom.hub.arcgis.com):

The shipping data platform is built on ArcGIS Hub. DCAT metadata feed available at:
`/api/feed/dcat-us/1.1`

At time of probing, the DCAT feed returned 0 datasets — the hub may use ArcGIS feature
services directly rather than DCAT cataloging.

Individual datasets are accessed via ArcGIS REST endpoints (specific URLs available
through the hub interface).

### HELCOM MADS (maps.helcom.fi):

WMS services available for traffic intensity layers. The HELCOM Map and Data Service
provides OGC-compliant web services for geospatial shipping data.

### AIS Explorer:

Previously at `https://maps.helcom.fi/website/AISexplorer/` — currently under maintenance.
The page redirects users to the MADS service for traffic intensity data.

## Freshness Assessment

Moderate to Low. This is aggregated, periodically updated data — not real-time AIS.
Traffic intensity maps are typically updated annually with approximately 1-year lag.
Accident and oil spill data is updated as reports are verified by HELCOM.

The value lies in the comprehensive Baltic-wide coverage and multi-year time series,
not in data freshness.

## Entity Model

- **Traffic Intensity**: Raster grids (vessel transits per cell per time period), by vessel type
- **Shipping Accidents**: Location, date, severity, vessel type, flag state, cause (from EMCIP)
- **Oil Spills**: Location, date, estimated volume, detection method (aerial surveillance)
- **Port data**: Via HELCOM Contracting Parties reporting

Identifiers: Geographic coordinates, vessel type classifications, flag states, EMCIP IDs.

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 1 | Annual aggregate updates, not real-time |
| Openness | 2 | Open access, but HELCOM data policy applies |
| Stability | 3 | Intergovernmental organization, treaty-backed |
| Structure | 2 | ArcGIS/OGC standards, but complex access patterns |
| Identifiers | 1 | Geographic-based, limited vessel-level identifiers |
| Additive Value | 2 | Unique Baltic-wide shipping intelligence, accident data |

**Total: 11/18**

## Notes

- HELCOM's primary value for this project is as contextual/reference data for the Baltic
  Sea, not as a real-time data source. The traffic intensity maps complement the real-time
  AIS feeds from Finland Digitraffic and Norway Kystverket/BarentsWatch.
- The AIS Explorer tool is currently under maintenance — HELCOM is transitioning to the
  MADS platform for all geospatial data access.
- HELCOM member states (Denmark, Estonia, Finland, Germany, Latvia, Lithuania, Poland,
  Russia, Sweden) all contribute shore-based AIS data to HELCOM's aggregate analysis.
  However, this data is processed and aggregated — individual vessel positions are not
  exposed.
- The shipping accident database (sourced from EMSA/EMCIP) is a unique dataset with
  PowerBI dashboards available for analysis.
- For real-time Baltic AIS data, use Finland Digitraffic (REST or MQTT) or Norway
  BarentsWatch — HELCOM is the intelligence layer on top.
- Contact for data requests: data@helcom.fi
