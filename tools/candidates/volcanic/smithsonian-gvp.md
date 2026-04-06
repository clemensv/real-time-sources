# Smithsonian GVP (Global Volcanism Program)

**Country/Region**: Global
**Publisher**: Smithsonian Institution, National Museum of Natural History
**API Endpoint**: `https://volcano.si.edu/` (web portal; also GeoJSON feeds)
**Documentation**: https://volcano.si.edu/
**Protocol**: Web portal / downloadable datasets
**Auth**: None
**Data Format**: HTML, downloadable spreadsheets (Excel/CSV), some GeoJSON
**Update Frequency**: Weekly (Weekly Volcanic Activity Report), periodic (database updates)
**License**: Public domain / Smithsonian open access

## What It Provides

The Global Volcanism Program (GVP) maintains the definitive global database of Holocene volcanoes and their eruption histories. Key products include:

- **Holocene Volcano Database** — ~1,400+ volcanoes with comprehensive eruption histories, morphology, and tectonic settings
- **Weekly Volcanic Activity Report** — Published every Wednesday, summarizing global volcanic activity for the past week
- **Bulletin of the Global Volcanism Network** — Monthly detailed reports on specific volcanoes
- **Current eruptions / ongoing activity** — Tracking of volcanoes with elevated activity
- **Volcano Number (VNUM)** — The authoritative global volcano identifier system

## API Details

GVP does not expose a conventional REST API. Access methods include:

**Weekly Volcanic Activity Report:**
```
https://volcano.si.edu/news/WeeklyVolcanicActivity.cfm
```
(Returns 403 in automated testing — may require browser User-Agent)

**Database search (web interface):**
```
https://volcano.si.edu/volcanolist_holocene.cfm
```
(Also 403 in automated testing)

**Downloadable data products:**
- Excel spreadsheets of the complete Holocene volcano list
- Eruption database in CSV/Excel
- GVP database available through WOVODAT

**GeoJSON feeds** (referenced in partner integrations):
Some derivative products may be available through partner APIs.

The website appears to use Cloudflare or similar protection that blocks non-browser automated access.

## Freshness Assessment

Moderate for reports (weekly); low for database (periodic bulk updates). The Weekly Volcanic Activity Report is the freshest product — published every Wednesday. The Holocene database is updated periodically as new eruptions occur or historical records are revised.

## Entity Model

**Volcano record:**
- Volcano Number (VNUM) — globally unique identifier (e.g., 211060)
- Volcano Name (primary + synonyms)
- Country / Region / Subregion
- Latitude, Longitude, Elevation
- Volcano Type (stratovolcano, shield, caldera, etc.)
- Tectonic Setting
- Dominant Rock Type
- Last Known Eruption date
- Evidence Category

**Eruption record:**
- Eruption start/stop dates
- VEI (Volcanic Explosivity Index)
- Eruption type and characteristics
- Evidence types

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Weekly reports, periodic database updates |
| Openness | 1 | Website blocks automated access (403) |
| Stability | 3 | Smithsonian institution, decades of operation |
| Structure | 1 | No REST API, web scraping difficult |
| Identifiers | 3 | VNUM is the global standard volcano identifier |
| Additive Value | 3 | Definitive reference database, unique authority |
| **Total** | **12/18** | |

## Notes

- GVP is the **authoritative source** for global volcano identification and eruption history. The VNUM system is used universally.
- However, the lack of a public API and blocking of automated access severely limits integration potential.
- The Weekly Volcanic Activity Report is the key "near-real-time" product but is published as HTML web pages.
- For reference data (volcano lists, eruption histories), downloadable spreadsheets may work for periodic bulk ingest.
- Consider using GVP as a reference/enrichment source (VNUM lookups) rather than a real-time feed.
- Partner projects like WOVODAT may offer better programmatic access to portions of the data.
