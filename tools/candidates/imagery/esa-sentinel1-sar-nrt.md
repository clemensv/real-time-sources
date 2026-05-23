# ESA Sentinel-1 SAR NRT

- **Country/Region**: Global
- **Endpoint**: https://dataspace.copernicus.eu/odata/v1/Products
- **Protocol**: OData / STAC
- **Auth**: OAuth
- **Format**: SAFE (complex SAR data), GeoTIFF (processed products)
- **Freshness**: 3-hour NRT (SLC, GRD products)
- **Score**: 11/18

## Overview

Sentinel-1 (S1A, S1B) is a C-band Synthetic Aperture Radar mission for all-weather day/night imaging:

- **GRD** (Ground Range Detected) — amplitude-only, geocoded, 10m resolution
- **SLC** (Single Look Complex) — phase + amplitude, interferometry-ready
- **IW mode** (Interferometric Wide Swath) — 250 km swath, 5×20m resolution

Applications:
- **InSAR** (Interferometric SAR) — ground deformation, subsidence, earthquakes, volcanoes
- **Ship detection** — maritime surveillance
- **Sea ice monitoring** — ice extent, type, drift
- **Flood mapping** — water extent under clouds
- **Oil spill detection**

NRT products published 3 hours after acquisition.

## Verdict

⏭️ **Reference** — SAR data is **highly specialized**. GRD products are 500MB–2GB per scene.
Requires expert processing (radiometric calibration, speckle filtering, geocoding). Not
suitable for general-purpose streaming. **Skip** unless repo targets SAR/InSAR community.

| Criterion | Score |
|-----------|-------|
| Value | 3 (unique all-weather capability) |
| Freshness | 2 (3-hour NRT) |
| Openness | 2 |
| Schema | 1 (complex SAR formats, steep learning curve) |
| Machine-readability | 2 |
| Repo fit | 1 (granule-based, huge files, specialist processing) |

**Total: 11/18** — **Skip** for general repo. Consider for SAR-specific use cases.
