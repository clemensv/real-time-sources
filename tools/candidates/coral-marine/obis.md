# OBIS (Ocean Biogeographic Information System)
**Country/Region**: Global (all oceans)
**Publisher**: UNESCO Intergovernmental Oceanographic Commission (IOC)
**API Endpoint**: `https://api.obis.org/v3/`
**Documentation**: https://api.obis.org/v3/ (interactive API docs)
**Protocol**: REST/JSON
**Auth**: None
**Data Format**: JSON
**Update Frequency**: Continuous (as datasets are contributed/updated)
**License**: CC0 (public domain) for most records, CC-BY for some

## What It Provides
OBIS is the world's largest open-access repository of marine biodiversity data, containing:
- **177.6 million+ occurrence records** of marine species
- **Full taxonomic hierarchy**: kingdom, phylum, class, order, family, genus, species
- **Geographic coordinates**: lat/lon with datum and uncertainty
- **Temporal data**: event dates, year, month
- **Depth/bathymetry**: sampling depth and seafloor depth
- **Darwin Core compliant**: standardized biodiversity data schema
- **Species tracked**: birds, fish, mammals, invertebrates, algae, microorganisms
- **Data quality flags**: NO_DEPTH, ON_LAND, etc.

OBIS is the marine node of GBIF (Global Biodiversity Information Facility) and integrates data from hundreds of institutions worldwide.

## API Details
- **Occurrence search**: `GET /v3/occurrence?limit=N` — paginated occurrence records
  - Filters: `scientificname`, `taxonid`, `areaid`, `startdate`, `enddate`, `geometry` (WKT)
  - Returns: full Darwin Core records with taxonomy, location, depth, flags
- **Checklist**: `GET /v3/checklist?taxonid=N` — species checklist for a taxon/area
- **Statistics**: `GET /v3/statistics/composition/class` — aggregate statistics
- **Taxon**: `GET /v3/taxon/{id}` — taxonomic information
- **Area**: `GET /v3/area/{id}` — geographic area definitions
- **Node**: `GET /v3/node/{id}` — contributing node information
- **Dataset**: `GET /v3/dataset/{id}` — dataset metadata
- **Pagination**: `limit` and `offset` parameters, `total` in response

## Probe Results
```json
{
  "total": 177624702,
  "results": [{
    "scientificName": "Larus fuscus",
    "class": "Aves",
    "family": "Laridae",
    "decimalLatitude": 49.8135001,
    "decimalLongitude": 2.7966375,
    "eventDate": "2013-07-25T05:12:51Z",
    "datasetName": "LBBG_ZEEBRUGGE - Lesser black-backed gulls...",
    "basisOfRecord": "MachineObservation",
    "license": "CC0-1.0",
    "aphiaID": 137142,
    "marine": true,
    "flags": ["NO_DEPTH", "ON_LAND"]
  }]
}
```

## Freshness Assessment
Good. Data is contributed continuously by research institutions, monitoring programs, and citizen science projects. Individual records may be historical (archival datasets), but the database grows daily with new observations and dataset contributions. The API serves the latest available data.

## Entity Model
- **Occurrence** (occurrenceID, basisOfRecord, eventDate, coordinates, depth)
- **Taxon** (aphiaID from WoRMS, scientificName, full hierarchy: kingdom→species)
- **Dataset** (datasetID, datasetName, institutionCode, collectionCode, DOI)
- **Node** (contributing OBIS node, typically a national or thematic center)
- **Location** (decimalLatitude/Longitude, geodeticDatum, coordinateUncertainty, bathymetry)
- **Quality** (flags array: NO_DEPTH, ON_LAND, etc.)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 2 | Continuous updates, but individual records may be historical |
| Openness | 3 | No auth, CC0 license, public API |
| Stability | 3 | UNESCO IOC, operational since 2000 |
| Structure | 3 | Clean REST JSON, Darwin Core standard, rich filtering |
| Identifiers | 3 | WoRMS aphiaID, DOIs, stable occurrence IDs |
| Additive Value | 3 | Largest open marine biodiversity database (177M+ records) |
| **Total** | **17/18** | |

## Notes
- 177 million records is an extraordinary data resource — one API call opens an ocean of biodiversity data
- Darwin Core standard ensures interoperability with GBIF and other biodiversity systems
- WoRMS aphiaID provides authoritative taxonomic identifiers for marine species
- Spatial queries accept WKT geometry — can query by reef polygon, marine protected area, etc.
- Quality flags enable filtering for data fitness-for-use
- Pairs beautifully with NOAA Coral Reef Watch (thermal stress) and OTN (animal tracking)
- Consider using OBIS for species-area queries: "what lives on this reef?"
