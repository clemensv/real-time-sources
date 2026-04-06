# NOAA OVATION Aurora Forecast Model

## Source Identity

| Field            | Value |
|------------------|-------|
| **Full Name**    | NOAA OVATION Aurora Forecast Model |
| **Operator**     | NOAA Space Weather Prediction Center (SWPC) |
| **URL**          | https://www.swpc.noaa.gov/products/aurora-30-minute-forecast |
| **API Endpoint** | `https://services.swpc.noaa.gov/json/ovation_aurora_latest.json` |
| **Coverage**     | Global (both hemispheres) |
| **Update Freq.** | ~30 minutes; model run tied to solar wind observations |

## What It Does

The OVATION (Oval Variation, Assessment, Tracking, Intensity, and Online Nowcasting) model predicts aurora intensity across the entire globe on a latitude-longitude grid. It takes real-time solar wind measurements from spacecraft (ACE/DSCOVR at the L1 Lagrange point) and maps them to expected aurora intensity — effectively answering "where can you see the northern/southern lights right now?"

This is a genuine forecast product: it uses current solar wind conditions to predict aurora 30–90 minutes into the future (the propagation time from L1 to Earth). During geomagnetic storms, the auroral oval expands equatorward, and OVATION tracks this in near-real-time.

## Endpoints Verified

| Endpoint | Status | Notes |
|----------|--------|-------|
| `/json/ovation_aurora_latest.json` | ✅ 200 | Full global grid; ~1.4 MB JSON |

### Sample Response (trimmed)

```json
{
  "Observation Time": "2026-04-06T11:07:00Z",
  "Forecast Time": "2026-04-06T11:56:00Z",
  "Data Format": "[Longitude, Latitude, Aurora]",
  "coordinates": [
    [0, -90, 5],
    [0, -89, 0],
    [0, -88, 6],
    [0, -87, 7],
    [0, 65, 0],
    [0, 66, 1],
    [0, 67, 4],
    [0, 68, 12],
    [0, 69, 22],
    [0, 70, 38]
  ]
}
```

The grid covers all longitudes (0–359°) and latitudes (-90° to +90°) in 1-degree steps. The "Aurora" value is a probability/intensity indicator (0–100 scale). Values peak in the auroral oval bands (~65–75° magnetic latitude in quiet conditions, extending to ~50° during storms).

## Authentication & Licensing

- **Auth**: None. Anonymous access.
- **Rate Limits**: None stated; static JSON regenerated on schedule.
- **License**: US Government public domain.

## Integration Notes

The response is a flat coordinate array — `[lon, lat, aurora_intensity]` — covering a 360×181 grid (65,160 data points). This is essentially a global raster dataset served as JSON. It's large (~1.4 MB) but compresses well with gzip.

Useful transformations:
- Extract the northern hemisphere auroral oval (lat > 50°) as a simplified polygon
- Threshold the intensity values to produce a "visible aurora" boundary line
- Combine with Kp index for a human-readable "aurora probability" by city/region

This product is distinct from the magnetic indices already in the NOAA SWPC collection. Kp tells you *how disturbed* the field is; OVATION tells you *where the aurora is visible*. The former is for scientists and grid operators; the latter is for aurora chasers and the general public.

The ~30-minute forecast cadence means this is useful for "should I go outside and look up?" decisions.

## Feasibility Rating

| Dimension                    | Score | Notes |
|------------------------------|-------|-------|
| **API Maturity & Docs**      | 2     | Single JSON endpoint; well-structured but minimal docs |
| **Data Freshness**           | 3     | Updated every ~30 minutes; forecast horizon ~1 hour |
| **Format / Schema Quality**  | 2     | Simple grid format; large payload; no GeoJSON |
| **Auth / Access Simplicity** | 3     | Anonymous; public domain |
| **Coverage Relevance**       | 3     | Global aurora probability — unique product |
| **Operational Reliability**  | 3     | NOAA SWPC operational infrastructure |
| **Total**                    | **16 / 18** | |

## Verdict

✅ **Build** — Unique product with no equivalent elsewhere. The aurora forecast is high-interest data (aurora tourism is a billion-dollar industry) with clean JSON delivery and zero access friction. The NOAA SWPC is already a confirmed source for geomagnetic data; OVATION adds a visually compelling and publicly accessible product. Could be implemented as an extension of the NOAA SWPC bridge or as a standalone source.
