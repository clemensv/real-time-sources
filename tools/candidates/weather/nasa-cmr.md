# NASA CMR (Common Metadata Repository) NRT Collections API

- **Country/Region**: Global (metadata catalog for all NASA Earthdata)
- **Endpoint**: `https://cmr.earthdata.nasa.gov/search/collections.json`
- **Protocol**: REST (JSON, XML, UMM-JSON, ATOM, OpenSearch)
- **Auth**: None (search); Earthdata Login for data access
- **Format**: JSON, XML
- **Freshness**: Metadata updated as collections ingest (varies by product, minutes to hours)
- **Docs**: https://cmr.earthdata.nasa.gov/search/site/docs/search/api.html
- **Score**: 8/18

## Overview

NASA's Common Metadata Repository (CMR) is the authoritative catalog of all Earth science data collections and granules across NASA's Earth Observing System Data and Information System (EOSDIS). CMR provides a unified search API across 12 Distributed Active Archive Centers (DAACs) — GES DISC, NSIDC, ORNL, LANCE, LP DAAC, PO.DAAC, SEDAC, ASF, LAADS, ASDC, CDDIS, and OB.DAAC.

CMR metadata includes collection-level descriptions (mission, instrument, temporal coverage, spatial extent, processing level, latency) and granule-level details (individual files, timestamps, bounding boxes, download URLs). The API supports keyword search, spatial/temporal filtering, faceted queries, and federation across NASA DAACs.

For NRT data, CMR is the discovery layer: you query CMR to find which NASA products have near-real-time variants, what their latency is, where they're archived, and how to access them. CMR does not serve the *data itself* (that comes from individual DAACs), but it provides the *metadata* to locate and describe NRT products.

## Endpoint Analysis

**Search for NRT collections:**
```
GET https://cmr.earthdata.nasa.gov/search/collections.json?keyword=near%20real-time&page_size=10
```

**Sample response (truncated):**
```json
{
  "feed": {
    "entry": [
      {
        "id": "C3380708978-OB_CLOUD",
        "title": "Aqua MODIS Level-2 Regional Ocean Color (OC) - Near Real-time (NRT) Data, version 2022.0",
        "short_name": "MODISA_L2_OC_NRT",
        "data_center": "OB_CLOUD",
        "processing_level_id": "2",
        "time_start": "2002-07-04T00:00:00.000Z",
        "updated": "2025-01-23T00:00:00.000Z",
        "summary": "The Ocean Biology DAAC produces near real-time (NRT) products...",
        "links": [
          {
            "rel": "http://esipfed.org/ns/fedsearch/1.1/data#",
            "href": "https://oceandata.sci.gsfc.nasa.gov/directdataaccess/Level-2/Aqua-MODIS/"
          }
        ]
      }
    ]
  }
}
```

**Query parameters (examples):**
- `keyword=fire` — keyword search
- `temporal=2024-01-01T00:00:00Z,2024-01-31T23:59:59Z` — date range
- `bounding_box=-130,20,-60,50` — spatial extent (W,S,E,N)
- `instrument=MODIS` — filter by sensor
- `processing_level_id=2` — Level 2 products
- `data_center=LANCE` — filter by DAAC

**Granule search (file-level):**
```
GET https://cmr.earthdata.nasa.gov/search/granules.json?short_name=MOD14&temporal=2024-01-15T00:00:00Z,2024-01-15T23:59:59Z
```

Returns individual HDF5 files, download URLs, file sizes, checksums.

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | CMR metadata is current, but it's a catalog, not a data stream; the *products* it describes have varying latency |
| Openness | 3 | No auth for search; clean REST API |
| Stability | 3 | NASA operational system since 2010s, stable API |
| Structure | 1 | JSON/XML metadata is well-structured, but CMR is a *catalog*, not a data product |
| Identifiers | 0 | Collection IDs and granule IDs exist, but CMR is not an event source |
| Richness | 0 | Metadata only; no science measurements |

**CMR is the right place to *discover* NASA NRT products,** but it is not itself a data stream to bridge. CMR tells you "MOD14 active fire granules arrive within 3 hours" and "here's the download URL," but it doesn't emit fire pixel events. For that, you query FIRMS (which wraps MOD14).

**Why it's here:** CMR is the authoritative index of all NASA NRT collections. When evaluating NASA feeds for this repo, CMR is where you'd start: search for `keyword=near real-time`, filter by domain (fire, precipitation, air quality), and identify candidates. But CMR itself is not bridged; the *products* it catalogs are.

## Limitations

- **CMR is a metadata catalog, not a data API.** It returns collection descriptions and granule lists, not science measurements or event records.
- **No event-level granularity.** CMR describes *files* (HDF5, NetCDF, GeoTIFF), not *events* (fire pixels, precipitation measurements, air quality observations). You must download and parse the files to extract events.
- **Inconsistent latency metadata.** Some collections document "NRT" or "LOW_LATENCY" in the collection type, but exact delivery latency is often buried in documentation PDFs, not exposed as structured metadata.
- **No change notifications.** CMR is pull-only; you query for new granules by polling with temporal filters. There's no WebSocket or webhook that pushes "a new MOD14 granule just arrived."

**CMR is a discovery tool, not a bridge target.**

## Final Verdict

**Verdict**: ⏭️ **Reference**

CMR is essential for *finding* NASA NRT products but not for *bridging* them. Use CMR to:
- Discover which NASA collections have NRT variants (`keyword=near real-time`)
- Find download URLs and DAAC endpoints for granule access
- Filter by spatial extent, temporal range, instrument, processing level

Once you've identified a product (e.g., FIRMS MOD14, GPM IMERG, TEMPO NO₂), bridge the *product's API or data files*, not CMR.

**CMR is the index; FIRMS/EONET/IMERG/TEMPO are the event streams.**

**Use CMR when:**
- Researching what NASA NRT products exist
- Building a multi-product data pipeline and need centralized metadata queries
- Monitoring EOSDIS system status (granule availability, latency tracking)

**Do not use CMR when:**
- You need structured event records (fire pixels, precipitation measurements, air quality observations)
- You want real-time event streaming (CMR is pull-based metadata, not push-based events)

**For NASA event streams, bridge:**
- **FIRMS** (active fire from MODIS/VIIRS)
- **EONET** (natural events aggregator)
- **GPM IMERG** (global precipitation)
- **TEMPO** (hourly air quality over North America)
- **SMAP** (soil moisture)

**Bridge type:** N/A (metadata catalog, not event source)
