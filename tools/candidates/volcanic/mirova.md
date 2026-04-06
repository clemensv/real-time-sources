# MIROVA (Middle InfraRed Observation of Volcanic Activity)

**Country/Region**: Global
**Publisher**: University of Turin (Università di Torino), Italy / HOTVOLC consortium
**API Endpoint**: `https://www.mirova.unito.it/` (web portal only)
**Documentation**: https://www.mirova.unito.it/
**Protocol**: Web portal (no API)
**Auth**: None (web viewing)
**Data Format**: PNG images, time-series plots (no structured data API)
**Update Frequency**: Near-real-time (updated with each MODIS/VIIRS satellite pass)
**License**: Academic use; citation required

## What It Provides

MIROVA is a near-real-time volcanic hotspot detection system based on analysis of Middle InfraRed (MIR) radiation from MODIS satellite data. It provides:

- **Volcanic Radiative Power (VRP)** — Thermal output measurements for volcanoes worldwide
- **Time-series plots** — Historical thermal output for individual volcanoes
- **Hotspot maps** — Spatial distribution of thermal anomalies around volcanoes
- **Alert classification** — Automated detection of anomalous thermal activity

MIROVA focuses specifically on volcanic thermal anomalies (as opposed to general fire detection systems like FIRMS), applying volcano-specific algorithms to distinguish volcanic heat from wildfires and other sources.

## API Details

MIROVA does not provide a public API. The website at `www.mirova.unito.it` was unreachable during testing (connection failures). Access methods include:

**Web portal (when available):**
- Interactive volcano selection
- Time-series VRP plots
- Current thermal activity maps
- Historical analysis tools

**Data access:**
- No REST API or data download endpoints discovered
- Results are presented as images/plots on the web interface
- Some data may be available through academic collaboration

The site appears to have intermittent availability issues based on testing.

## Freshness Assessment

When operational, MIROVA updates with each MODIS satellite pass (approximately 4 passes/day for any given location). The automated processing pipeline provides near-real-time thermal monitoring. However, the system's availability was not confirmed during testing.

## Entity Model

**Volcanic thermal observation:**
- Volcano name (linked to Smithsonian GVP VNUM)
- Observation datetime
- Volcanic Radiative Power (VRP) in Watts
- Spatial extent of thermal anomaly
- Background thermal level
- Anomaly classification

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Near-real-time satellite processing |
| Openness | 0 | No API, website unreachable during testing |
| Stability | 1 | Academic project, site availability issues |
| Structure | 0 | No structured data output, image-based |
| Identifiers | 2 | Uses GVP volcano identifiers |
| Additive Value | 3 | Unique volcano-specific thermal monitoring |
| **Total** | **8/18** | |

## Notes

- **Effectively dismissed for API integration** — no programmatic access available and the site was unreachable.
- MIROVA's scientific value is high — it provides volcano-specific thermal monitoring that general fire detection systems (FIRMS) cannot match.
- The Volcanic Radiative Power metric is scientifically meaningful for tracking eruption intensity.
- For satellite-based volcanic thermal monitoring, consider using FIRMS with the `type` field filter (`type=1` indicates active volcanoes in VIIRS data).
- MIROVA data may be accessible through the HOTVOLC platform or via academic collaboration with the University of Turin.
- If the website recovers, it would be worth revisiting for potential data access.
