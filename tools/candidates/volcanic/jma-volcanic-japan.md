# JMA Volcanic Warnings (Japan Meteorological Agency)

**Country/Region**: Japan
**Publisher**: Japan Meteorological Agency (気象庁, JMA)
**API Endpoint**: `https://www.data.jma.go.jp/svd/vois/data/tokyo/STOCK/activity_info/`
**Documentation**: https://www.data.jma.go.jp/multi/volcano/index.html?lang=en (multilingual portal)
**Protocol**: HTTP (HTML pages, some structured data)
**Auth**: None
**Data Format**: HTML, PDF (activity reports), JSON (some endpoints)
**Update Frequency**: As events occur; monthly activity reports; weekly summaries for active volcanoes
**License**: Japan government open data (with attribution)

## What It Provides

JMA monitors 111 active volcanoes in Japan — one of the most volcanically active countries on Earth. The volcanic monitoring program provides:

- **Volcanic Warnings** — Eruption warnings with alert levels (Level 1-5 scale)
- **Volcanic Forecasts** — Level 1 (potential for increased activity)
- **Activity information** — Detailed situation reports for each volcano
- **Monthly activity reports** — PDF documents per volcano per month
- **Submarine volcano warnings** — Alerts for underwater volcanic activity

Japan uses a 5-level volcanic alert system:
- Level 5: Evacuate (居住地域に重大な被害)
- Level 4: Prepare to evacuate
- Level 3: Do not approach volcano (入山規制)
- Level 2: Regulation around crater (火口周辺規制)
- Level 1: Potential for increased activity

## API Details

JMA volcanic data is primarily served through HTML pages:

**Current alert status (Japanese):**
```
https://www.data.jma.go.jp/svd/vois/data/tokyo/STOCK/activity_info/map_0.png
```
Returns an HTML page listing all volcanoes with current warning levels and recent information bulletins.

**Multilingual portal:**
```
https://www.data.jma.go.jp/multi/volcano/index.html?lang=en
```
English-language interface showing current volcanic warning levels on a map.

**Monthly activity reports (PDF):**
```
https://www.data.jma.go.jp/vois/data/report/monthly_v-act_doc/{region}/{YYMM}/{volcanoID}_{YYMM}.pdf
```

**Volcano-specific pages:**
```
https://www.data.jma.go.jp/svd/vois/data/tokyo/STOCK/activity_info/{volcanoID}.html
```

During testing, the site showed current warnings for: Sakurajima (Level 3), Nishino-shima (Level 2), multiple volcanoes at Level 2, and several submarine volcano warnings.

## Freshness Assessment

Good for alert-driven data. Warning level changes are published immediately. Weekly situation updates are published for volcanoes with elevated activity. Monthly comprehensive reports are published ~1 week after month-end.

## Entity Model

**Volcano record:**
- Volcano ID (JMA internal numbering, e.g., 506 = Sakurajima)
- Volcano name (Japanese primary, English available)
- Location / Region
- Current alert level (1-5)
- Warning type (eruption warning, forecast, submarine warning)

**Activity report:**
- Volcano reference
- Report datetime
- Activity description (Japanese; some English translations)
- Warning level recommendation
- Observation data summary

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Real-time alerts, weekly/monthly reports |
| Openness | 2 | Public access but HTML-based, limited structured data |
| Stability | 3 | Official national met service, highly reliable |
| Structure | 1 | Primarily HTML/PDF, no REST API |
| Identifiers | 2 | JMA volcano IDs, not globally standardized |
| Additive Value | 3 | Japan — one of the most active volcanic regions globally |
| **Total** | **13/18** | |

## Notes

- Japan monitors more active volcanoes than almost any other country. This data source is critical for Pacific Rim volcanic coverage.
- Content is primarily in Japanese with limited English translations through the multilingual portal.
- No discoverable REST/JSON API for volcanic data, though JMA does provide JSON APIs for earthquake and weather data.
- Sakurajima (Level 3) erupts frequently — good for testing data freshness.
- JMA's volcano numbering system maps to Smithsonian GVP VNUM but uses a different scheme.
- Consider parsing the HTML status pages or monitoring RSS/Atom feeds if available.
- The monthly PDF reports are comprehensive but not machine-readable.
