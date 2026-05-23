# EUMETSAT SEVIRI Full Disk Imagery (MSG)

- **Country/Region**: Europe, Africa, Atlantic, Middle East (Meteosat disk 0°, prime view)
- **Endpoint**: EUMETSAT Data Store, EUMETView WMS, EUMETCast
- **Protocol**: File download (NetCDF, native format), WMS, EUMETCast broadcast
- **Auth**: Free EUMETSAT registration (Data Store), WMS open
- **Format**: HRIT (native), NetCDF-4, PNG/GeoTIFF (via WMS)
- **Freshness**: 15 minutes (full disk scan), RSS 5 minutes (rapid scan Europe)
- **Docs**: https://www.eumetsat.int/seviri
- **Score**: 10/18

## Overview

The Spinning Enhanced Visible and Infrared Imager (SEVIRI) on Meteosat Second Generation (MSG) satellites provides continuous 15-minute full disk imagery in 12 spectral channels (visible, near-IR, IR, water vapor).

**Channels** (subset):
- VIS0.6, VIS0.8: Reflected sunlight (clouds, land, vegetation)
- IR3.9, IR10.8, IR12.0: Thermal emission (temperature)
- WV6.2, WV7.3: Water vapor (upper/mid troposphere)
- HRV: High-resolution visible (1 km nadir)

**SEVIRI scan modes**:
- **Full Disk Service (FDS)**: Every 15 minutes, entire Meteosat view (60°S-60°N, 60°W-60°E)
- **Rapid Scan Service (RSS)**: Every 5 minutes, Europe only (MSG-9 satellite)

**Why SEVIRI matters**:
- **Weather animation**: 15-min loops show storm development, cloud motion
- **Derived products**: SEVIRI feeds NWC SAF, H SAF, LSA SAF, OSI SAF algorithms
- **True color imagery**: Combine RGB channels for public communication
- **Fog detection**: Night-time IR difference (IR10.8 - IR3.9) detects low cloud
- **Volcanic ash**: IR brightness temperature difference detects ash plumes

However: SEVIRI **imagery is not inherently event-based** — it's a gridded image product. To stream as events, must derive **phenomena** (cloud motion vectors, fog polygons, ash plumes, storm cells).

## Endpoint Analysis

**EUMETSAT Data Store**:
```
GET https://api.eumetsat.int/data/browse/collections?q=SEVIRI
```

Products available:
- Level 1.5: Calibrated radiances (NetCDF, HRIT)
- Level 2: Derived products (cloud mask, SST, etc.)

**EUMETView WMS**:
```
https://view.eumetsat.int/geoserver/wms?
  service=WMS&
  request=GetMap&
  layers=msg:rgb_naturalcolor&
  time=2024-06-15T12:00:00Z
```

**EUMETCast**: Primary operational channel (HRIT format, DVB-S broadcast). **Not suitable for HTTP bridge**.

**File size**:
- Full disk, single channel: ~20 MB (compressed HRIT)
- Full disk, all 12 channels: ~200 MB
- HRV channel: ~100 MB (higher resolution)

**Update cadence**:
- FDS: Every 15 minutes
- RSS: Every 5 minutes (Europe window)

## Schema / Sample

**SEVIRI is imagery, not tabular**. To bridge as CloudEvents, must:

1. **Derive phenomena**: Use NWC SAF cloud products, H SAF precipitation, LSA SAF fire (already covered in separate candidates) — **those are the event streams**.

2. **Emit metadata events**: Publish "new image available" events:
```json
{
  "type": "eumetsat.seviri.image-available",
  "source": "msg-seviri/msg4",
  "id": "seviri_msg4_20240615_120000",
  "time": "2024-06-15T12:00:00Z",
  "subject": "imagery/msg/full-disk",
  "data": {
    "satellite": "MSG-4",
    "scan_time": "2024-06-15T12:00:00Z",
    "channels": ["VIS0.6", "VIS0.8", "IR3.9", "IR10.8", "IR12.0", "HRV"],
    "data_store_url": "https://api.eumetsat.int/data/.../SEVIRI_20240615_1200.nc",
    "wms_time_parameter": "2024-06-15T12:00:00Z",
    "coverage_bbox": [-60, -60, 60, 60]
  }
}
```

3. **Extract features**: Run computer vision on imagery to detect:
   - Cloud motion vectors (AMV)
   - Fog polygons
   - Volcanic ash plumes
   - Dust storms

## Why Strong (for raw imagery)

| Criterion | Score | Notes |
|-----------|-------|-------|
| **Freshness** | 3 | 15 min (FDS), 5 min (RSS Europe) |
| **Openness** | 2 | Free registration, WMS open |
| **Stability** | 3 | Operational since 2004 (MSG-1) |
| **Structure** | 2 | Imagery (HRIT/NetCDF), not tabular |
| **Identifiers** | 0 | No entities (pixels, not events) |
| **Additive value** | 0 | Imagery is raw input; derived products are valuable |

**For derived phenomena** (cloud cells, fog, ash):
- Identifiers: 2 (can assign cell IDs)
- Additive value: 2 (if repo doesn't have phenomena type)

**Issue**: SEVIRI **raw imagery is not event-based**. The repo pattern is CloudEvents for observations, not image tile notifications.

## Limitations

1. **Not event-based**: Imagery is a continuous field, not discrete events. Repo sources are point observations (weather stations, AIS positions, river gauges) or point phenomena (fires, lightning).

2. **Overlap with derived SAFs**: NWC SAF, H SAF, LSA SAF already extract **events from SEVIRI** (cloud types, precipitation, fires). Creating a separate SEVIRI raw imagery feed duplicates the input without adding phenomena.

3. **Large payloads**: Full disk imagery is 200 MB per observation (all channels). Not suitable for Kafka event stream (5 MB typical message limit).

4. **Consumer complexity**: Downstream consumers would need to process imagery to extract value. Better to publish derived products (already covered by SAF candidates).

## Verdict

**SKIP** (10/18) — Raw SEVIRI imagery does not fit the repo's event-based model. The **derived SAF products** (NWC SAF clouds, H SAF precip, LSA SAF fire) are the **event streams from SEVIRI** and are covered in separate candidates.

**Exception**: If a specific use case requires **image availability notifications** (e.g., triggering external processing pipelines), a lightweight "image metadata" event could work:
- Emit one event per scan with download URL and WMS time parameter
- Consumers use the metadata to fetch imagery via Data Store or WMS
- Volume: 96 events/day (15-min FDS) + 288 events/day (5-min RSS) = 384 events/day

**Recommendation**: **Skip raw SEVIRI**. Focus on:
- **NWC SAF** (cloud/precip nowcasting) — covered
- **H SAF** (precipitation) — covered
- **LSA SAF** (fire) — covered

These are the SEVIRI-derived **event products**. Raw imagery is the input, not the output.
