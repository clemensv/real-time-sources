# ESA DISCOSweb (Database and Information System Characterising Objects in Space)

**Country/Region**: Europe / Global
**Publisher**: European Space Agency (ESA) / Space Debris Office
**API Endpoint**: `https://discos.esa.int/api/`
**Documentation**: https://discos.esa.int/apidocs
**Protocol**: REST (JSON:API specification)
**Auth**: Token-based (free registration at https://discos.esa.int)
**Data Format**: JSON (JSON:API format)
**Update Frequency**: Regularly updated (catalog maintenance schedule)
**License**: ESA Terms of Use (free for non-commercial research)

## What It Provides

DISCOSweb is ESA's space debris and objects database, providing detailed characterization of objects in Earth orbit. It contains data on launch events, objects (satellites, rocket bodies, debris), reentry predictions, and fragmentation events. The database focuses on object physical characteristics (mass, shape, dimensions) that complement the orbital data from Space-Track/CelesTrak.

The API endpoint was unreachable during probing (connection failures), but the service is documented and known to be operational.

## API Details

- **Base URL**: `https://discos.esa.int/api/`
- **Resources**: `objects`, `launches`, `launch-vehicles`, `launch-sites`, `reentries`, `initial-orbits`, `fragmentations`, `fragmentation-event-types`, `object-classes`, `propulsion-types`
- **Format**: JSON:API specification with relationships and pagination
- **Authentication**: Bearer token in `Authorization` header
- **Filtering**: JSON:API filter syntax (e.g., `filter[eq][objectClass]=Payload`)
- **Pagination**: `page[size]` and `page[number]` parameters
- **Relationships**: Objects → launches → launch vehicles → launch sites; fragmentations → parent objects

## Freshness Assessment

DISCOSweb is a catalog/reference database, not a real-time feed. Object records are updated as new characterization data becomes available. Reentry predictions are updated as events approach. This is more of an enrichment/reference source than a real-time data stream.

## Entity Model

- **Object**: COSPAR ID, NORAD catalog number, name, object class (payload/rocket body/debris), mass, shape, dimensions, span
- **Launch**: Launch date, site, vehicle, cospar ID, mission
- **Reentry**: Predicted/actual reentry date, object, uncertainties
- **Fragmentation**: Event type, parent object, date, fragment count

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Catalog database; not real-time |
| Openness | 2 | Free registration; ESA terms of use |
| Stability | 2 | ESA operated; may have availability issues (connection failures observed) |
| Structure | 3 | JSON:API specification; well-defined relationships |
| Identifiers | 3 | COSPAR IDs, NORAD catalog numbers |
| Additive Value | 2 | Physical characterization data complements orbital data |
| **Total** | **13/18** | |

## Notes

- DISCOSweb's unique value is physical characterization (mass, shape, dimensions) — data not available from Space-Track or CelesTrak.
- The JSON:API format is well-structured but verbose compared to simple REST APIs.
- Connection reliability was poor during probing — may reflect infrastructure or access issues.
- Best used as an enrichment source to complement orbital data from CelesTrak/Space-Track.
- ESA's Space Debris Office maintains this as part of their space surveillance activities.
