# open.africa — Pan-African Open Data Platform

- **Country/Region**: Pan-African (54 countries)
- **Endpoint**: `https://open.africa/api/3/action/package_search?q={query}&rows=10`
- **Protocol**: REST (CKAN API)
- **Auth**: None
- **Format**: JSON (CKAN standard), datasets in CSV/JSON/XML
- **Freshness**: Static — no real-time or regularly-updating datasets found
- **Docs**: https://docs.ckan.org/en/latest/api/
- **Score**: 5/18
- **Verdict**: **REJECTED** — static file repository, not a real-time data source

## Overview

open.africa (formerly africaopendata.org, now redirects to open.africa) is an
NGO-maintained CKAN data catalog aggregating datasets from national portals,
NGOs, and international organizations across Africa. Run by Code for Africa.

## Deep Dive Results (April 2026)

The CKAN API is live and responsive. Systematic probing across every plausible
real-time domain reveals **no actual real-time or near-real-time data feeds**.

### Dataset Counts by Query

| Query | Count | What's Actually There |
|-------|------:|----------------------|
| `real-time` | 198 | Text matches only — South African commuting surveys from 2015 |
| `weather` | 6 | Ghana accident weather 1991-2010, Ghana precip 2000-2015, Kenya rain gauges (static) |
| `water level` | 22 | Lake Tanganyika level (one static CSV, 2021), SA dam levels 2014-2016 (static CSVs) |
| `air quality` | 102 | sensors.AFRICA archive entries — **most have 0 resources** (empty dataset shells) |
| `electricity` | 189 | Static transmission network GeoJSON/SHP files, access statistics |
| `transport` | 298 | Almost entirely South Africa budget documents (Vulekamali harvest) |
| `flood` | 13 | Kenya flash floods 2020 static CSV, IOM displacement tracking (Cyclone Idai, static) |

### Why It Fails for This Repo

1. **No live feeds.** Every dataset is a static file upload (CSV, XLSX, PDF,
   GeoJSON, TIFF). CKAN here is a file repository, not a live data API.
2. **The "198 real-time results" are false positives.** They match the word
   "real-time" in descriptions of static commuting time surveys.
3. **Stale data.** Most `metadata_modified` dates fall in 2015-2019. Very few
   datasets have been touched since 2021.
4. **sensors.AFRICA air quality datasets are empty shells.** Of the 102 air
   quality results, the vast majority have `num_resources: 0`. The one that
   does (Temeke, Tanzania) is a static XLSX upload from 2018. The actual
   sensors.AFRICA live API (`api.sensors.africa`) is a separate system.
5. **Harvest sources are broken.** Many resource URLs point at defunct portals
   (e.g., `data.code4sa.org` Socrata instance, `opendata.go.ke` endpoints
   returning 404).

### Groups and Organizations

**Groups** = country tags (Algeria through Zimbabwe) plus thematic groups
(armed-conflict, climate, covid-19, ebola, education, health-data,
sensorsafrica-airquality-archive).

**Notable organizations**: Code for Africa, sensors.AFRICA, World Bank,
ILRI, eHealth Africa, Vulekamali (SA Treasury), Tanzania NBS, various
Code-for-X chapters.

### Interesting Leads Discovered (for separate evaluation)

The probing revealed upstream sources that **might** have live data — these
should be evaluated independently, not through open.africa:

- **sensors.AFRICA** (`api.sensors.africa`) — citizen science air quality
  sensor network across ~15 African cities. Has its own live API. This is
  the actual real-time source behind the empty CKAN shells.
- **South Africa Dept. of Water and Sanitation** — weekly dam level data
  exists in static form; the department may have a live API.
- **Kenya Open Data** (`opendata.go.ke`) — government Socrata portal,
  harvested into open.africa. May have fresher endpoints directly.
- **ENERGYDATA.INFO** — World Bank energy data portal, harvested here.
  Static infrastructure data, not real-time.

## CKAN API Reference (for future African data scouting)

```
GET https://open.africa/api/3/action/package_search?q={query}&rows={n}
GET https://open.africa/api/3/action/package_show?id={id}
GET https://open.africa/api/3/action/organization_list
GET https://open.africa/api/3/action/group_list
```

No auth required. Standard CKAN 3 API. The platform can be useful as a
**discovery tool** to find upstream African portals — but those portals, not
open.africa itself, would be the integration targets.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 0 | All static uploads, no updating feeds |
| Openness | 3 | No auth, CKAN standard API |
| Stability | 1 | NGO-maintained, many broken harvest links |
| Structure | 1 | Files in mixed formats, no consistent schema |
| Identifiers | 0 | No stable real-time entity identifiers |
| Richness | 0 | Meta-catalog of stale files |
