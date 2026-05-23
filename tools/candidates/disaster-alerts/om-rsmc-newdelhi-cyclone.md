# RSMC New Delhi - Arabian Sea Tropical Cyclone Warnings

- **Country/Region**: North Indian Ocean (Arabian Sea and Bay of Bengal) — covers Oman, India, Pakistan, Yemen, Somalia
- **Endpoint**: `https://rsmcnewdelhi.imd.gov.in` (web portal), no documented public API found
- **Protocol**: HTML/web scraping or CAP XML (if available)
- **Auth**: None (web portal is public)
- **Format**: HTML, potentially XML (CAP alerts), potentially JSON
- **Freshness**: Bulletins issued every 3-6 hours during active cyclones, daily summaries otherwise
- **Docs**: https://rsmcnewdelhi.imd.gov.in , https://mausam.imd.gov.in
- **Score**: 8/18

## Overview

The **Regional Specialized Meteorological Centre (RSMC) New Delhi** is the World Meteorological Organization (WMO)-designated center for tropical cyclone forecasting in the **North Indian Ocean** basin, which includes the Arabian Sea and Bay of Bengal. RSMC New Delhi, operated by the India Meteorological Department (IMD), issues official tropical cyclone forecasts, warnings, and advisories for all countries bordering the North Indian Ocean, including:
- **Arabian Sea**: Oman, Yemen, Somalia, Pakistan, western India
- **Bay of Bengal**: India, Bangladesh, Myanmar, Sri Lanka, Thailand

Oman is directly exposed to Arabian Sea tropical cyclones. Recent major impacts:
- **Cyclone Shaheen** (October 2021) — first recorded tropical cyclone to make landfall in Oman as a Category 1 storm, struck Muscat with 150 mm rainfall, killed 14 people, caused $1.3 billion in damage
- **Cyclone Mekunu** (May 2018) — Category 3 equivalent, struck Salalah with 278 mm rainfall in 36 hours (10× annual average), killed 11 in Oman, swept away entire villages in Dhofar Governorate
- **Cyclone Hikaa** (September 2019) — made landfall near Duqm, caused flash flooding across central and southern Oman

Arabian Sea cyclones are less frequent than Bay of Bengal storms (average 1-2 per year vs. 4-5), but **warming sea surface temperatures** in the Arabian Sea are increasing cyclone intensity. The 2018-2021 period saw four landfalling cyclones in Oman/Yemen — unprecedented in modern records.

## Endpoint Analysis

**Website accessible but no public API documented** — the RSMC New Delhi portal (rsmcnewdelhi.imd.gov.in) was reachable during testing (2026-05-23) but returned a complex HTML page with heavy client-side JavaScript. No RESTful API endpoints were advertised in documentation.

### Potential Data Access Methods

1. **Web scraping** — the RSMC portal publishes:
   - **Current cyclone bulletins** (text, HTML)
   - **Forecast track maps** (PNG, sometimes GeoJSON overlays)
   - **Intensity forecasts** (tabular data in HTML)
   - **Warning zones** (graphical, occasionally KML/GeoJSON)
   
   Scraping is **fragile** — website redesigns break parsers, JavaScript-heavy pages are hard to scrape, no structured schema.

2. **CAP XML feeds** (Common Alerting Protocol) — WMO recommends CAP for tropical cyclone warnings. India participates in WMO Integrated Global Observing System (WIGOS) and may publish CAP feeds, but no public CAP endpoint URL was found during discovery.
   
   Attempted endpoint (returned 404):
   ```
   https://mausam.imd.gov.in/responsive/cyclone_indian_activeData.php
   ```
   
   This suggests IMD may have had a structured cyclone API in the past but it's either moved, deprecated, or restricted.

3. **GDACS integration** — the Global Disaster Alert and Coordination System (GDACS) aggregates tropical cyclone data from multiple RSMCs including New Delhi. GDACS provides a **GeoJSON API**:
   ```
   GET https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH?eventtype=TC&country=OM&fromdate=YYYY-MM-DD
   ```
   
   GDACS ingests RSMC bulletins and republishes them in a standardized format. This is a **more stable alternative** to scraping RSMC directly.

### Data Model

RSMC cyclone bulletins typically include:
- **Storm name and ID** (e.g., "Cyclone Shaheen", "ARB 03/2021")
- **Current position** (lat/lon)
- **Intensity** (maximum sustained winds in km/h or knots, central pressure in hPa)
- **Movement** (direction and speed)
- **Forecast track** (positions at +12h, +24h, +48h, +72h, +96h, +120h)
- **Forecast intensity**
- **Warning areas** (coastal districts, ports, offshore zones)
- **Issuance time** (UTC)

For a real-time bridge, the event model would be:
- **Key**: Storm ID (e.g., `ARB03/2021` for Arabian Sea cyclone #3 of 2021)
- **Event types**: Bulletin (position update), Track Forecast (predicted path), Warning (alert for specific zones)
- **Update frequency**: Every 3-6 hours during active cyclone, daily otherwise

## Integration Notes

- **GDACS as aggregator**: Rather than building a fragile scraper for RSMC New Delhi directly, **ingest tropical cyclone data from GDACS**, which already aggregates RSMC bulletins alongside JTWC (Joint Typhoon Warning Center, U.S. military) and other regional centers. GDACS provides:
  - Structured GeoJSON API
  - Global coverage (all ocean basins)
  - Includes historical storms and forecasts
  - Open, no auth required
  
  This would be a **global tropical cyclone bridge** (all basins: Atlantic, Pacific, Indian Ocean) rather than Oman-specific, but it would capture all Arabian Sea storms affecting Oman.

- **Alternative: JTWC** — the U.S. Navy/Air Force Joint Typhoon Warning Center also issues forecasts for the North Indian Ocean and competes with RSMC New Delhi as an authoritative source. JTWC products are publicly available via https://www.metoc.navy.mil/jtwc/ but the site was **inaccessible (403 Forbidden)** during testing, suggesting it may be geofenced or temporarily down. JTWC data is also aggregated by GDACS.

- **Overlap with existing sources**: The repo does not currently have tropical cyclone coverage. A GDACS-based tropical cyclone bridge would be **highly additive**:
  - Covers Oman's Arabian Sea cyclone threat (Shaheen, Mekunu, Hikaa-type events)
  - Extends to all global cyclone basins (Atlantic hurricanes, Western Pacific typhoons, Southern Hemisphere cyclones)
  - Event-driven (only produces data when storms are active)
  - High public interest and disaster response value

- **Update frequency**: During an active Arabian Sea cyclone threatening Oman, RSMC bulletins are issued every 3 hours. Between cyclones, the basin may be quiet for months. This is a **seasonal, event-driven source** (May-December is the North Indian Ocean cyclone season, with peaks in May-June and October-November).

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | 3-6 hour bulletin cadence during active storms |
| Openness | 1 | No documented public API; GDACS aggregator is open |
| Stability | 1 | RSMC portal is HTML-based, no API versioning or SLA; GDACS is more stable |
| Structure | 1 | HTML scraping required unless CAP XML exists; GDACS provides GeoJSON |
| Identifiers | 2 | Storm IDs (ARB03/2021) are stable within a season |
| Additive value | 1 | GDACS covers same data but is global aggregator, not Oman-specific |

**Verdict**: ⏭️ Reference

**Rationale**: RSMC New Delhi does not provide a documented public API for tropical cyclone data. Web scraping the HTML portal is possible but fragile. **Instead, build a global tropical cyclone bridge using GDACS** as the upstream source. GDACS aggregates RSMC New Delhi, JTWC, and other regional centers into a single, stable, machine-readable GeoJSON API. This approach:
- Captures all Arabian Sea cyclones affecting Oman (Shaheen, Mekunu-type events)
- Extends to global cyclone coverage (value beyond Oman)
- Avoids building a fragile scraper for a single regional center
- Provides a standardized data model across all ocean basins

If RSMC New Delhi publishes a CAP XML feed or structured JSON API in the future, revisit this as a standalone source. Until then, **GDACS is the better path** for tropical cyclone data.

**Note for global cyclone bridge**: GDACS event API should be polled with `eventtype=TC` (tropical cyclone) to retrieve active and recent storms. Keying would use GDACS's `eventid` or the upstream storm ID (e.g., `ARB03/2021` from RSMC or `IO012021` from JTWC). Track forecast positions (lat/lon at +12h, +24h, etc.) would be separate event types or nested in the bulletin message schema.
