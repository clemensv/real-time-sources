# EUMETSAT MTG Flexible Combined Imager (FCI) Level-1C

- **Country/Region**: Europe, Africa, Atlantic, Middle East (MTG full disk)
- **Endpoint**: EUMETSAT Data Store, EUMETView WMS, EUMETCast
- **Protocol**: File download (NetCDF), WMS, EUMETCast broadcast
- **Auth**: Free EUMETSAT registration (Data Store), WMS open
- **Format**: NetCDF-4, native MTG format
- **Freshness**: 10 minutes (full disk), 2.5 minutes (RSS Europe)
- **Docs**: https://www.eumetsat.int/mtg-fci
- **Score**: 10/18

## Overview

The Flexible Combined Imager (FCI) on Meteosat Third Generation (MTG-I1, operational 2024) is the successor to SEVIRI. FCI provides:

- **16 spectral channels** (vs. 12 on SEVIRI)
- **10-minute full disk** (vs. 15-minute SEVIRI)
- **2.5-minute Rapid Scan Europe** (vs. 5-minute SEVIRI RSS)
- **1 km resolution** (High-Resolution Visible), 0.5 km experimental

**Improvements over SEVIRI**:
- Faster refresh (10 min vs. 15 min)
- More channels (better cloud discrimination, aerosol detection)
- Higher resolution (1 km HRV vs. SEVIRI's variable resolution)

## Endpoint Analysis

**EUMETSAT Data Store**:
```
GET https://api.eumetsat.int/data/browse/collections?q=FCI
```

MTG-I1 became operational in June 2024. FCI Level-1C data (calibrated radiances) is being distributed via:
- **EUMETCast** (primary, broadcast)
- **Data Store** (HTTP download)
- **EUMETView** (WMS visualization)

**Update cadence**:
- Full Disk High Spectral Resolution (FDHSI): Every 10 minutes
- Rapid Scan High Spectral Resolution (RSS): Every 2.5 minutes (Europe window)

**File size**: 300-500 MB per full disk scan (16 channels, NetCDF-4 compressed)

## Schema / Sample

FCI is **imagery, not tabular events** — same issue as SEVIRI (covered in separate candidate).

**Event model** (metadata notification):
```json
{
  "type": "eumetsat.mtg.fci.image-available",
  "source": "mtg-fci/mtg-i1",
  "id": "fci_mtgi1_20240615_120000",
  "time": "2024-06-15T12:00:00Z",
  "subject": "imagery/mtg/full-disk",
  "data": {
    "satellite": "MTG-I1",
    "scan_time": "2024-06-15T12:00:00Z",
    "scan_mode": "FDHSI",
    "channels": 16,
    "data_store_url": "https://api.eumetsat.int/.../FCI_20240615_1200.nc",
    "wms_layers": ["mtg:fci_rgb_naturalcolor", "mtg:fci_ir10.8"]
  }
}
```

## Why Weak for Event Streaming

| Criterion | Score | Notes |
|-----------|-------|-------|
| **Freshness** | 3 | 10 min (full disk), 2.5 min (RSS) |
| **Openness** | 2 | Free registration, WMS open |
| **Stability** | 3 | Operational MTG mission (just launched 2024) |
| **Structure** | 2 | Imagery (NetCDF-4), not tabular |
| **Identifiers** | 0 | No entities (pixels, not events) |
| **Additive value** | 0 | Raw imagery; derived SAF products are events |

## Verdict

**SKIP** (10/18) — Same as SEVIRI: **raw imagery is not event-based**. The repo pattern is CloudEvents for observations, not image tile notifications.

**Derived SAF products from FCI** (once MTG is fully operational):
- **NWC SAF** will process FCI for cloud/precip nowcasts
- **H SAF** will use FCI for precipitation estimates
- **LSA SAF** will use FCI for fire detection

These derived products are the **event streams from FCI**. Raw imagery is the input.

**Recommendation**: Skip raw FCI imagery. Focus on SAF products that process FCI once they transition from SEVIRI to FCI/MTG.
