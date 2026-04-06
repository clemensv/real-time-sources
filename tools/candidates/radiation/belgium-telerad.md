# Belgium FANC Telerad — Automatic Radioactivity Monitoring Network

**Country/Region**: Belgium
**Publisher**: FANC (Federal Agency for Nuclear Control / Federaal Agentschap voor Nucleaire Controle)
**Portal**: `https://www.telerad.be/`
**API Endpoint**: None directly discoverable (ArcGIS backend behind VertiGIS SPA)
**Protocol**: Web portal (VertiGIS Studio / ArcGIS)
**Auth**: None for map viewer
**Data Format**: Raster map tiles via VertiGIS; underlying ArcGIS REST services not directly exposed
**Update Frequency**: Real-time (continuous dose rate monitoring)
**License**: Not explicitly stated

## What It Provides

The Telerad network is Belgium's automatic radioactivity monitoring network, operated by FANC in cooperation with SCK-CEN (Belgian Nuclear Research Centre). It monitors ambient gamma dose rates from approximately 200+ stations distributed across Belgium, with particular density around the nuclear sites at Doel and Tihange.

The network provides continuous real-time dose rate measurements visible on the public Telerad website. The map interface shows current readings at each station with color-coded dose rate levels.

## API Details

### Public Web Interface

| URL | Content |
|---|---|
| `https://www.telerad.be/` | Landing page (FR/NL language choice) |
| `https://www.telerad.be/pageFR.html` | French map viewer |
| `https://www.telerad.be/pageNL.html` | Dutch map viewer |

The map viewers use **VertiGIS Studio** (formerly Geocortex) as a hosted GIS application:

```
https://apps.vertigisstudio.com/web/?app=79611c03e49b47c3bcafe508e372536b
```

### Underlying Architecture

The Telerad data is served through an ArcGIS-based backend via VertiGIS Studio. The ArcGIS MapServer/FeatureServer REST endpoints are loaded dynamically via JavaScript within the SPA and could not be extracted without browser-based network inspection.

### Probing Results

| URL | Result |
|---|---|
| `telerad.fgov.be` | DNS does not resolve |
| `opendata.fanc.be` | DNS does not resolve |
| `opendata.belgium.be` | DNS does not resolve |
| FANC website Telerad pages | Redirect to language selection, no data endpoints |

No CKAN/open-data portal was found for FANC data. Belgium's federal open data portals do not appear to include Telerad data.

## Freshness Assessment

Real-time data exists — the website shows continuous dose rate monitoring. But the data is only accessible through the VertiGIS web interface, not through a discoverable API.

## Entity Model

- **Station** — ~200+ stations across Belgium, concentrated around Doel and Tihange nuclear sites
- **Measurement** — real-time ambient gamma dose rate

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 3 | Real-time continuous data on the website |
| Openness | 1 | Visible on public website but no discoverable API |
| Stability | 3 | Belgian federal government infrastructure |
| Structure | 1 | Data trapped in ArcGIS SPA — likely structured underneath |
| Identifiers | 1 | Station markers visible on map but not exported |
| Additive Value | 1 | Belgium is covered by EURDEP |
| **Total** | **10/18** | |

## Notes

- The Telerad data is very likely accessible via ArcGIS REST endpoints that could be discovered through browser network inspection of the VertiGIS application.
- Belgium's radiation data is also available via EURDEP, which is the recommended route for programmatic access to Belgian dose rate data.
- If Belgium-specific high-resolution data is needed beyond what EURDEP provides, inspecting the VertiGIS SPA's network calls would reveal the ArcGIS service URLs.
- SCK-CEN (Belgian Nuclear Research Centre) may have additional data products but no public API was found.
