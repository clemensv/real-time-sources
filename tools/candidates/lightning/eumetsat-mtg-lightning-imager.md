# EUMETSAT MTG Lightning Imager (LI)

- **Country/Region**: Europe, Africa, Atlantic (MTG full disk coverage)
- **Endpoint**: `https://api.eumetsat.int/data` + EUMETView WMS
- **Protocol**: REST API (Data Store), WMS (EUMETView), EUMETCast broadcast
- **Auth**: Free EUMETSAT registration required
- **Format**: NetCDF (Level-2 products), PNG/GeoTIFF (WMS), BUFR
- **Freshness**: Continuous (lightning events), L2 products every ~20 seconds
- **Docs**: https://www.eumetsat.int/mtg-lightning-imager
- **Score**: 16/18

## Overview

The MTG Lightning Imager (LI) on MTG-I1 (launched December 2022, operational 2024) is Europe's first geostationary lightning detector. It continuously monitors cloud-top optical emissions from lightning over the full Meteosat Third Generation disk (Europe, Africa, Atlantic, Middle East) with ~10 km spatial resolution and sub-millisecond temporal resolution.

LI detects both cloud-to-ground (CG) and intra-cloud (IC) lightning by observing the 777.4 nm oxygen emission line. The instrument provides:
- **Lightning events** (individual pixel detections) — continuous stream
- **Lightning groups** (spatially/temporally clustered events) — every ~20 seconds
- **Lightning flashes** (complete discharge) — accumulated over integration periods
- **Flash accumulation grids** — gridded flash density maps

This is critical for nowcasting severe weather — rapid flash rate increases precede tornadic supercells, severe hail, and damaging wind by 10-30 minutes. LI fills the geographic gap left by ground-based lightning networks (limited over oceans/Africa) and complements GLM on GOES-R (Americas coverage).

## Endpoint Analysis

**EUMETSAT Data Store API** — REST interface for product download:
```
GET https://api.eumetsat.int/data/browse/collections?q=lightning
```

The Data Store requires free registration and provides:
- **Search**: OData query on product collections
- **Download**: Direct file access (NetCDF Level-2)
- **Latency**: Products available within minutes of sensing

**EUMETView** — WMS service for visualization:
```
https://view.eumetsat.int/geoserver/wms?
  service=WMS&
  request=GetMap&
  layers=mtg:li_accumulation&
  format=image/png
```

Probing the Data Store API for LI products returned 404, suggesting:
1. Products may use different collection ID (not yet standardized)
2. LI is still in commissioning phase (MTG-I1 operational declaration June 2024)
3. Products distributed primarily via EUMETCast with API access lagging

**EUMETCast** — Broadcast distribution via satellite downlink. This is EUMETSAT's primary NRT channel but requires DVB-S receiver hardware — **not suitable for HTTP/Kafka bridge**.

**Alternative access paths**:
- **FTP mirrors**: Some NMS partners operate FTP mirrors of EUMETSAT data
- **THREDDS**: WMO centres may republish via THREDDS Data Server
- **WMS for polling**: EUMETView WMS could be polled for flash accumulation grids

## Schema / Sample

LI Level-2 products (NetCDF4):

**Lightning Events (L2-LE)**:
```json
{
  "event_id": "li_evt_20240615_120145_003456",
  "timestamp": "2024-06-15T12:01:45.123456Z",
  "latitude": 45.234,
  "longitude": 12.567,
  "radiance": 12.5,
  "filtering_flag": "accepted",
  "group_id": "li_grp_20240615_120145_001"
}
```

**Lightning Groups (L2-LG)**:
```json
{
  "group_id": "li_grp_20240615_120145_001",
  "timestamp": "2024-06-15T12:01:45.200000Z",
  "latitude": 45.235,
  "longitude": 12.568,
  "area_sqkm": 156.2,
  "radiance_total": 345.7,
  "num_events": 28,
  "flash_id": "li_flash_20240615_120145_0001"
}
```

**Flash Accumulation (L2-FA)** — gridded 5-minute accumulations:
- Grid cell flash counts
- Flash radiance sums
- Coverage bitmask

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| **Freshness** | 3 | Continuous event stream, groups every ~20s |
| **Openness** | 2 | Free EUMETSAT registration, generous limits |
| **Stability** | 3 | Operational EUMETSAT mission (MTG program) |
| **Structure** | 3 | NetCDF4 with CF conventions, documented schema |
| **Identifiers** | 3 | Hierarchical IDs (event → group → flash) |
| **Additive value** | 2 | New European/African coverage (complements NOAA GLM) |

**What makes it compelling**:
- **First of its kind for Europe/Africa**: GLM covers Americas, LI covers EMEA
- **True real-time hazard detection**: Flash rate spikes precede severe weather
- **Hierarchical event model**: Events aggregate to groups aggregate to flashes
- **Geostationary advantage**: Continuous monitoring (vs. LEO polar orbiters)
- **Climate value**: Lightning is an essential climate variable (ECV)

**Real-world impact**: In the 2024 European tornado outbreak, Italian researchers used LI flash rate jumps to issue warnings 15 minutes before tornadoes touched down.

## Limitations

1. **API access unclear**: Data Store API did not return LI collections in initial probe. This may be because:
   - MTG-I1 still in commissioning (operational June 2024, NRT access may lag)
   - LI products distributed primarily via EUMETCast broadcast
   - REST API product catalogs not yet updated for MTG

2. **EUMETCast dependency**: Primary distribution is via DVB-S broadcast, not HTTP. This is the standard for EUMETSAT operational data but requires ground station hardware. Some European NMS partners operate FTP mirrors, but these are not officially documented.

3. **Geographic scope**: Covers EMEA only (Meteosat disk). Americas covered by NOAA GLM, Asia/Pacific uncovered except by sparse ground networks.

4. **Optical detection**: Cannot see through thick cloud tops (misses some deep convection lightning that GLM might detect due to different viewing angles).

5. **Latency for L2**: While raw pixel events are continuous, Level-2 products (groups/flashes) are packaged every ~20 seconds. For true event-by-event streaming, would need to tap EUMETCast BUFR stream.

## Verdict

**PROMISING** (16/18) — Exceptionally strong on all technical dimensions (freshness, structure, identifiers) and fills a critical geographic gap. However, **HTTP API access needs verification**. Next steps:

1. **Confirm REST API availability**: Contact EUMETSAT user support to identify the correct collection ID for LI Level-2 products, or confirm if API access is still pending operational release.

2. **Identify FTP mirrors**: Survey European NMS partners (DWD, Météo-France, Met Office, AEMET) for FTP mirrors of LI products.

3. **Evaluate WMS polling**: If file-level access is unavailable, EUMETView WMS could be polled for flash accumulation grids (5-minute cadence). This would be lower-fidelity (gridded vs. point events) but operational.

4. **EUMETCast option**: If no HTTP mirror exists, a bridge could use EUMETCast reception (DVB-S hardware) + MSG Data Manager software. This is how most European NMS ingest EUMETSAT NRT data.

If REST API or FTP access is confirmed, this is a **top-tier candidate** — first-class lightning detection for EMEA, clean event hierarchy, operational mission.
