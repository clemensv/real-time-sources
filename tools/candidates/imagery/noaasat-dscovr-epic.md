# NOAA DSCOVR EPIC Earth Imagery

- **Country/Region**: USA / Global (deep space L1 orbit)
- **Endpoint**: `https://epic.gsfc.nasa.gov/api/natural`
- **Protocol**: REST (JSON)
- **Auth**: None
- **Format**: JSON metadata + PNG images
- **Freshness**: 1-2 hours (10-20 images per day)
- **Docs**: https://epic.gsfc.nasa.gov/about/api
- **Score**: 14/18

## Overview

The DSCOVR (Deep Space Climate Observatory) spacecraft orbits at the Sun-Earth Lagrange point 1 (L1), ~1.5 million km from Earth. Its EPIC (Earth Polychromatic Imaging Camera) captures full-disk images of the sunlit Earth every 1-2 hours in 10 spectral channels (UV to near-IR).

EPIC imagery is used for:
- **Climate science**: tracking vegetation, aerosols, ozone, cloud cover
- **Space weather**: observing Earth's magnetosphere from a unique vantage point
- **Public engagement**: iconic "Blue Marble" views updated daily
- **Solar wind monitoring**: DSCOVR also carries the NOAA Plasma-Mag instrument for real-time solar wind data (already in `noaa-goes` bridge)

EPIC images are **not real-time** — they are downlinked, processed, and published with 12-36 hour latency. However, the API provides structured JSON metadata for each image, including timestamps, coordinates, and spacecraft ephemeris.

NASA GSFC hosts the EPIC API, but DSCOVR is a NOAA operational mission (SWPC uses the solar wind data).

## Endpoint Analysis

**Endpoint verified live:**

```
GET https://epic.gsfc.nasa.gov/api/natural
```

Response: JSON array of ~22 images (recent captures).

Sample record:
```json
{
  "identifier": "20260520001752",
  "caption": "This image was taken by NASA's EPIC camera onboard the NOAA DSCOVR spacecraft",
  "image": "epic_1b_20260520001752",
  "version": "04",
  "centroid_coordinates": {
    "lat": 19.138184,
    "lon": 164.311523
  },
  "dscovr_j2000_position": {
    "x": 971331.881252,
    "y": 1005119.436159,
    "z": 481733.225691
  },
  "lunar_j2000_position": {
    "x": -85179.896155,
    "y": 313384.899148,
    "z": 162751.764668
  },
  "sun_j2000_position": {
    "x": 78733741.209631,
    "y": 118609738.979571,
    "z": 51414974.599961
  },
  "attitude_quaternions": {
    "q0": -0.18655,
    "q1": 0.72089,
    "q2": -0.55572,
    "q3": 0.36973
  },
  "date": "2026-05-20 00:13:03"
}
```

**Fields:**
- `identifier`: Unique image ID (YYYYMMDDHHmmss format)
- `image`: Image filename (without extension)
- `version`: Processing version
- `date`: Capture timestamp (UTC)
- `centroid_coordinates`: Earth's sunlit center point (lat/lon)
- `dscovr_j2000_position`: Spacecraft position in J2000 frame (km)
- `lunar_j2000_position`: Moon position (km)
- `sun_j2000_position`: Sun position (km)
- `attitude_quaternions`: Spacecraft orientation

**Image URL pattern**:
```
https://epic.gsfc.nasa.gov/archive/natural/{YYYY}/{MM}/{DD}/png/{image}.png
```

**Key model**: `{identifier}` (unique per image capture).

**Volume**: ~20 images/day (~140/week).

## Schema / Sample

Full JSON sample above. Metadata is rich with ephemeris and geolocation data.

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 2/3 | Valuable for climate and Earth observation, less for real-time operations |
| Freshness | 1/3 | 12-36 hour latency; not near-real-time |
| Openness | 3/3 | No auth, NASA open data, stable API |
| Schema Clarity | 3/3 | Excellent JSON with full ephemeris and metadata |
| Machine-Readability | 3/3 | Clean JSON, image URLs easily constructed |
| Repo Fit | 2/3 | Imagery domain not yet represented, but latency is a mismatch |

**Total: 14/18**

- Unique vantage point: full-disk Earth from L1
- Rich metadata: spacecraft/Moon/Sun positions, Earth centroid
- High scientific value for climate monitoring
- Public engagement potential
- No authentication required
- Stable NASA API

## Limitations

- **12-36 hour latency** — disqualifies as "real-time" or "near-real-time"
- Images are large (~3-5 MB PNGs per spectral channel)
- No event-driven updates (just periodic polling for new image metadata)
- Keying is trivial (one image = one event)
- Not operationally actionable (unlike flare or proton data)
- Mixed ownership: NASA hosts API, NOAA operates DSCOVR

## Verdict

**SKIP** — While scientifically interesting and beautifully documented, EPIC imagery has **12-36 hour latency**, placing it outside the "near-real-time" scope of this repo. The metadata API is excellent, but the use case is more suited to a climate data archive than a real-time event stream. If the repo expands to include delayed satellite imagery products, EPIC would be a strong candidate. For now, **defer** due to freshness mismatch.
