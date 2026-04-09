# King County Swim Beach Water Quality

- **Country/Region**: US — King County, WA (Puget Sound area)
- **Publisher**: King County Department of Natural Resources and Parks
- **Endpoint**: `https://data.kingcounty.gov/resource/vam5-kgis.json`
- **Protocol**: REST (Socrata SODA API)
- **Auth**: None (app token optional)
- **Format**: JSON, CSV, XML
- **Freshness**: Weekly during swim season (May–September), updated within days of sampling
- **Docs**: https://kingcounty.gov/en/dept/dnrp/nature-recreation/parks-recreation/king-county-parks/water-recreation/swimming-beach-bacteria-temperature
- **Score**: 12/18

## Overview

King County monitors bacteria levels (E. coli for freshwater, Enterococcus for saltwater) and water temperature at popular swimming beaches including Green Lake, Lake Washington, Lake Sammamish, and marine beaches. Beach advisories and closures are issued when bacteria exceed safe levels. For a free-time advisor, this data directly answers "Is it safe to swim today?" — one of the most actionable questions during summer.

## API Details

**Socrata Open Data API:**
```
GET https://data.kingcounty.gov/resource/vam5-kgis.json
```

Alternative dataset (bacteria and temperature):
```
GET https://data.kingcounty.gov/resource/2dss-p56t.json
```

**SODA Query Examples:**

| Query | URL |
|-------|-----|
| Latest results | `?$order=sampledate DESC&$limit=20` |
| Specific beach | `?$where=locator='0434'&$order=sampledate DESC` |
| Recent season | `?$where=sampledate > '2024-05-01'` |

**Key Fields:**
- `locator` — Beach/station ID
- `name` — Beach name (e.g., "Madrona Park Beach", "Matthews Beach")
- `sampledate` — Date of sample collection
- `value` — Bacteria count (colony forming units per 100mL)
- `parameter` — "E. coli", "Enterococcus", "Temperature"
- `units` — CFU/100mL or °C
- `latitude`, `longitude` — Beach location

**Key Beaches Monitored:**
- Green Lake (multiple sites)
- Lake Washington: Madison Park, Madrona, Matthews, Magnuson, Seward Park, Juanita, Houghton
- Lake Sammamish: Idylwood, Pine Lake
- Marine: Alki, Golden Gardens, Carkeek Park

**Advisory Thresholds:**
- Freshwater (E. coli): Advisory at >235 CFU/100mL; Closure at >1000 CFU/100mL
- Saltwater (Enterococcus): Advisory at >104 CFU/100mL

## Freshness Assessment

Seasonal. Sampling occurs weekly during the swim season (typically late May through September). Results are typically posted within a few days of sample collection. Outside swim season, no sampling occurs. This is not real-time monitoring but rather a weekly safety assessment cycle.

## Entity Model

- **Beach** — Locator code, name, water body, type (fresh/salt), coordinates
- **Sample** — Date, parameter, value, units, quality flags
- **Advisory** — Derived from bacteria counts exceeding thresholds
- **Season** — Annual monitoring period (May–September)

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 1 | Weekly during swim season; no data Oct–Apr |
| Openness | 3 | Socrata SODA API, no auth, county government data |
| Stability | 2 | County program; annual funding dependent |
| Structure | 2 | Socrata JSON; straightforward flat records |
| Identifiers | 2 | Beach locator codes; parameter names |
| Additive Value | 2 | Unique "is it safe to swim?" data for Seattle area |
| **Total** | **12/18** | |

## Notes

- Weekly frequency is a limitation, but this is the nature of bacteria testing (requires lab analysis).
- The Washington Department of Ecology BEACH program monitors saltwater beaches statewide using a similar approach.
- King County also provides an ArcGIS-based swim beach status dashboard at `experience.arcgis.com` that shows current advisories.
- Water temperature readings are a bonus — useful for "is the water warm enough?" questions.
- Pairs well with UV index data: sunny days + safe bacteria levels = ideal swim day.
- For more real-time water quality, the King County marine buoy and NANOOS candidates provide continuous monitoring (though of different parameters).
