# Helioviewer — Solar Imagery API

**Country/Region**: Global
**Publisher**: ESA / NASA (Helioviewer Project)
**API Endpoint**: `https://api.helioviewer.org/v2/`
**Documentation**: https://api.helioviewer.org/docs/v2/
**Protocol**: REST (JSON)
**Auth**: None
**Data Format**: JSON (metadata), JPEG/PNG (images), FITS (science data via links)
**Update Frequency**: Near real-time — SDO images available within minutes of capture
**License**: Public domain (NASA/ESA data)

## What It Provides

Helioviewer provides near-real-time access to solar imagery from SDO (Solar Dynamics Observatory), SOHO (Solar and Heliospheric Observatory), STEREO, and other heliophysics missions. The API lets you query for the closest available image to any timestamp across multiple instruments and wavelengths — AIA 171Å (coronal loops), AIA 304Å (chromosphere), HMI magnetograms, LASCO coronagraph, and more.

This is a window into the Sun in near-real-time: solar flares, coronal mass ejections, filament eruptions, and coronal holes — all visible through the API.

## API Details

- **Closest image**: `GET /v2/getClosestImage/?date={ISO8601}&sourceId={id}` — nearest image to timestamp
- **JP2 image**: `GET /v2/getJP2Image/?date={ISO8601}&sourceId={id}` — JPEG2000 science image
- **Screenshot**: `GET /v2/takeScreenshot/?date={ISO8601}&layers={layer_string}&imageScale={arcsec/px}` — rendered composite
- **Data sources**: `GET /v2/getDataSources/` — list all available instruments/detectors/measurements
- **Source IDs**: SDO/AIA 171Å = 10, SDO/AIA 304Å = 13, SDO/HMI magnetogram = 19, SOHO/LASCO C2 = 28
- **No auth required**: Public API
- **Movie generation**: API can generate movies from time ranges (async with callback)

## Freshness Assessment

SDO images are available within 15-30 minutes of capture. SOHO LASCO coronagraph images have slightly longer latency. The `getClosestImage` endpoint returns the nearest available image to your requested timestamp, making it trivial to get "latest" data.

Confirmed live: queried SDO AIA 171Å for 2026-04-06 12:00 UTC, received image metadata with 4096×4096 resolution and precise solar disk parameters.

## Entity Model

- **Image**: `id` (database ID), `date` (observation timestamp), `name` (instrument/measurement), `scale` (arcsec/pixel)
- **Source**: `sourceId`, instrument, detector, measurement (wavelength/type)
- **Solar parameters**: `refPixelX/Y`, `rsun` (solar radius in pixels), `dsun` (distance to Sun in meters), `sunCenterOffsetParams`

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | 15-30 minute lag for SDO; SOHO can be longer |
| Openness | 3 | No auth, public API, NASA/ESA public domain data |
| Stability | 3 | Operational since 2009, ESA/NASA-funded infrastructure |
| Structure | 3 | Clean JSON metadata, standard image formats |
| Identifiers | 3 | Integer image IDs, source IDs, precise timestamps |
| Additive Value | 2 | Unique near-real-time solar imagery; complements SWPC numerical data |
| **Total** | **16/18** | |

## Notes

- Confirmed live: API returned detailed metadata for SDO AIA 171Å imagery.
- The API is a metadata and image retrieval layer over NASA/ESA heliophysics data archives.
- Supports composite images — overlay multiple wavelengths/instruments in a single rendered image.
- Movie generation feature is async — submit request, get callback URL, poll for completion.
- Solar disk parameters (rsun, refPixel, scale) enable precise coordinate transforms between image pixels and solar coordinates.
- Pairs with DSCOVR solar wind data (see a CME launch in imagery, then track its arrival at L1) and NOAA DONKI (event database for what you're seeing in the images).
