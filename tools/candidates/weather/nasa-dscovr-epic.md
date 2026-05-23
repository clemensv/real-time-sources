# NASA DSCOVR / EPIC (Earth Polychromatic Imaging Camera)

- **Country/Region**: Global (full-disk Earth imagery from L1)
- **Endpoint**: `https://epic.gsfc.nasa.gov/api/natural` (REST), `https://epic.gsfc.nasa.gov/archive/natural/` (image files)
- **Protocol**: REST (JSON), HTTPS file download (PNG, natural-color or enhanced)
- **Auth**: None
- **Format**: JSON (metadata), PNG (imagery)
- **Freshness**: 12–36 hours from image capture
- **Docs**: https://epic.gsfc.nasa.gov/about/api
- **Score**: 9/18

## Overview

The Earth Polychromatic Imaging Camera (EPIC) aboard NASA's Deep Space Climate Observatory (DSCOVR) satellite captures full-disk natural-color images of the entire sunlit side of Earth from the L1 Lagrange point, ~1.5 million km away. DSCOVR is positioned between Earth and the Sun, providing a continuous view of the daylit hemisphere.

EPIC captures images in 10 narrowband channels spanning UV to near-IR (~317 nm to 780 nm). Natural-color RGB images are composited from the 443 nm (blue), 551 nm (green), and 680 nm (red) channels. Enhanced-color products use different band combinations to highlight vegetation, aerosols, or ozone.

The satellite maintains a roughly 2-hour cadence (varies slightly due to orbital geometry) between images. Each image captures the entire Earth disc at ~8 km/pixel spatial resolution. The API provides image metadata (timestamp, Sun/satellite geometry, image URL); the images themselves are PNG files.

## Endpoint Analysis

**REST API for natural-color images (most recent):**
```
GET https://epic.gsfc.nasa.gov/api/natural
```

**Response (truncated):**
```json
[
  {
    "identifier": "20240115001249",
    "caption": "This image was taken by NASA's EPIC camera onboard the NOAA DSCOVR spacecraft",
    "image": "epic_1b_20240115001249",
    "version": "03",
    "centroid_coordinates": {
      "lat": -5.12,
      "lon": 157.89
    },
    "dscovr_j2000_position": {
      "x": -1394852.61,
      "y": 532063.55,
      "z": 238045.33
    },
    "sun_j2000_position": {...},
    "date": "2024-01-15 00:12:49"
  }
]
```

**Image download URL:**
```
https://epic.gsfc.nasa.gov/archive/natural/2024/01/15/png/epic_1b_20240115001249.png
```

**Available endpoints:**
- `/api/natural` — Most recent natural-color images
- `/api/natural/date/2024-01-15` — All images from a specific date
- `/api/enhanced` — Enhanced-color (vegetation highlight)
- `/api/images` — All available image identifiers (no metadata)

**Image characteristics:**
- Resolution: 2048×2048 pixels (full-disk Earth)
- Spatial resolution: ~8 km/pixel at nadir (Earth's center), degrades toward limb
- Cadence: ~2 hours between images (13–22 images per day depending on season/orbit)
- Projection: Orthographic (as seen from L1)

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | 12–36 hour latency from image capture — not real-time |
| Openness | 3 | No auth, no registration, public REST API and image archive |
| Stability | 3 | DSCOVR operational since 2015, EPIC stable since 2016 |
| Structure | 2 | REST JSON metadata is clean; images are PNG (raster, not structured data) |
| Identifiers | 0 | Image timestamp is unique; no entity IDs (whole-Earth snapshot) |
| Richness | 0 | Full-disk imagery only; no per-pixel science products, no event detection |

**EPIC provides iconic whole-Earth imagery** — the same view Apollo astronauts saw. The images are scientifically useful for tracking global-scale phenomena (continental cloud systems, polar ice extent, seasonal vegetation changes, volcanic ash/dust plumes, solar eclipses on Earth). The L1 vantage point means EPIC always sees the daylit hemisphere and captures the same face of Earth throughout the day.

**Why it's not an event stream:** EPIC delivers whole-Earth images, not events with identifiers and measurements. There's no "EPIC detected a wildfire" or "EPIC measured aerosol optical depth at lat/lon X,Y." The images are for visualization and qualitative monitoring, not structured event generation.

**Latency is too slow for NRT.** Images arrive 12–36 hours after capture. This is acceptable for public outreach (the "Earth from space" website) but not for operational applications that need same-day imagery.

## Limitations

- **12–36 hour latency** from image capture to public availability. This is slower than GOES-16/17 (15-minute full-disk images delivered in near real-time), MODIS/VIIRS (3-hour NRT), or geostationary weather satellites.
- **Whole-Earth images, not gridded data.** You cannot query "temperature at lat/lon X,Y" or "all fire pixels in this region." The output is a picture, not a data product.
- **No derived science products.** EPIC provides raw imagery (calibrated radiances converted to natural color). There are no cloud masks, vegetation indices, aerosol retrievals, or fire detections. Contrast with MODIS/VIIRS, which have dozens of derived L2/L3 products.
- **~2 hour cadence** is too coarse for rapid-evolving phenomena (thunderstorm tracking, flash floods, urban heat islands). Geostationary weather satellites (GOES, Himawari, Meteosat) deliver 5–15 minute updates.
- **8 km spatial resolution** is coarse compared to MODIS (250 m to 1 km), VIIRS (375 m to 750 m), or Landsat (30 m). You cannot see individual cities, small fires, or detailed cloud structures.

**EPIC is excellent for public engagement and whole-Earth monitoring, not for event-driven analytics.**

## Final Verdict

**Verdict**: ⏭️ **Reference**

EPIC delivers visually stunning whole-Earth imagery from L1, but it does not fit the repo's event-streaming model. The 12–36 hour latency, whole-disk raster output (no per-pixel data), and lack of derived science products place it outside the NRT event bridge domain.

**Use EPIC for:**
- Public dashboards showing "Earth right now" (iconic imagery)
- Time-lapse visualizations of seasonal vegetation cycles, polar ice changes, or continental weather systems
- Background full-disk imagery in geospatial applications

**Do not use EPIC for:**
- Real-time event detection (fire, storms, floods)
- Quantitative analysis (temperature, aerosol, vegetation indices)
- High-resolution monitoring (cities, infrastructure, small-scale features)

**For operational NRT Earth imagery, use:**
- **GOES-16/17 (NOAA)** — 15-minute full-disk, 5-minute CONUS, 1-minute mesoscale; multiple bands including fire/smoke detection
- **MODIS/VIIRS (NASA LANCE)** — 3-hour NRT delivery, 250 m to 1 km resolution, dozens of derived products
- **Himawari-8/9 (JMA)** — 10-minute full-disk, Asia-Pacific geostationary
- **Meteosat Third Generation (EUMETSAT)** — 10-minute full-disk, Europe/Africa geostationary

**Bridge type:** N/A (not suitable for event streaming)
