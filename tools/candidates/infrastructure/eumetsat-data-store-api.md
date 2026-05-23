# EUMETSAT Data Store API (Collection Overview)

- **Country/Region**: Global (all EUMETSAT missions)
- **Endpoint**: `https://api.eumetsat.int/data`
- **Protocol**: REST API (OData), HTTP file download
- **Auth**: Free EUMETSAT registration (access key + secret)
- **Format**: Varies (NetCDF-4, GRIB2, BUFR, HDF5, native formats)
- **Freshness**: Varies by product (NRT to archival)
- **Docs**: https://data.eumetsat.int, https://user.eumetsat.int/resources/user-guides/eumetsat-data-store-api-guide
- **Score**: N/A (infrastructure, not a data source)

## Overview

The EUMETSAT Data Store is the **unified HTTP API** for accessing EUMETSAT satellite data. It replaces earlier systems (Product Navigator, Data Centre) and provides:

- **OData query interface**: Search collections by product, time, geography
- **Direct HTTP download**: Files delivered via signed URLs
- **WMS/WMTS integration**: Links to EUMETView visualization layers
- **Subscription system**: Automated notifications when new data arrives

**Authentication**:
1. Register at https://eoportal.eumetsat.int
2. Generate access key + secret
3. Use OAuth2 bearer token or HTTP Basic Auth

**API structure**:
```
GET /data/browse/collections
  → List all available product collections

GET /data/browse/collections/{collectionId}
  → Metadata for specific collection (temporal coverage, formats, etc.)

GET /data/search-products/1.0.0/os?
  pi={collectionId}&
  dtstart={start_time}&
  dtend={end_time}&
  geo={bbox}
  → Search for products matching criteria

GET /data/download/{productId}
  → Download specific product file
```

## Product Coverage

**Collections available** (subset):
- **Meteosat**: SEVIRI Level 1.5, cloud products, fire detection
- **Metop**: AVHRR, ASCAT, IASI, GOME-2, AMSU-A, MHS
- **MTG**: FCI Level 1C, Lightning Imager (LI) Level 2
- **Sentinel-3**: OLCI, SLSTR (EUMETSAT marine distribution)
- **Sentinel-6**: Altimetry
- **Jason-3**: Altimetry

**SAF products** in Data Store (partial):
- OSI SAF: ASCAT winds, SST, sea ice
- H SAF: Precipitation (limited)
- NWC SAF: Cloud products (limited)
- LSA SAF: Fire, LST (limited)

**Note**: Not all SAF products are in Data Store. Some SAFs (H SAF, LSA SAF, NWC SAF) have their own FTP servers with more complete archives.

## Why This Matters for Bridging

**Advantages**:
- **Single API**: One authentication system for multiple products
- **OData standard**: Programmatic search and discovery
- **HTTP download**: No FTP polling needed
- **Metadata rich**: Each product has detailed descriptors (time, bbox, quality)

**Challenges**:
- **Latency**: Data Store may lag behind EUMETCast or SAF FTP servers (minutes to hours)
- **Completeness**: Not all NRT products are in Data Store (especially SAF operational streams)
- **Rate limits**: 1000 requests/hour per user (acceptable for polling, but not for high-frequency searches)

## Recommended Usage for This Repo

For each EUMETSAT candidate source:
1. **Check Data Store first**: Search for collection ID via `/collections?q={product_name}`
2. **Verify NRT availability**: Check `temporalResolution` and `updateFrequency` in collection metadata
3. **Fallback to FTP**: If Data Store lacks NRT stream or has high latency, use SAF-specific FTP servers

**Polling strategy** (if using Data Store):
```python
# Every N minutes, poll for new products
GET /data/search-products/1.0.0/os?
  pi=EO:EUM:DAT:METOP:ASCSZOL&
  dtstart={last_poll_time}&
  dtend={now}

# Download new products and emit events
for product in results:
    download(product.downloadUrl)
    parse_and_emit_events(product)
```

## Verdict

**Infrastructure Tool** — The Data Store API is a **key access path** for EUMETSAT products, especially those not available via SAF FTP servers. For products covered in this research:

**Use Data Store for**:
- OSI SAF ASCAT winds (if FTP is unstable)
- Metop AVHRR/IASI (if EARS not available)
- MTG FCI/LI products (once fully operational)

**Use SAF FTP for**:
- H SAF precipitation (FTP more complete + lower latency)
- LSA SAF fire (FTP primary channel)
- NWC SAF (if Data Store access unclear)

**Status**: Critical infrastructure for polling-based EUMETSAT bridges. Document Data Store API patterns in implementation guides.
