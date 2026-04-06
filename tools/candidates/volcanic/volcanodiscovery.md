# VolcanoDiscovery

**Country/Region**: Global
**Publisher**: VolcanoDiscovery GmbH (Germany) — private company / Tom Pfeiffer
**API Endpoint**: N/A — content website, no API
**Documentation**: https://www.volcanodiscovery.com/
**Protocol**: Web (HTML)
**Auth**: None (web viewing)
**Data Format**: HTML
**Update Frequency**: Multiple times daily (news articles, VAAC reposts)
**License**: Proprietary content, all rights reserved

## What It Provides

VolcanoDiscovery is a popular volcano information website and tour operator that aggregates volcanic activity information from multiple sources worldwide. It provides:

- **Volcano news** — Aggregated news articles about volcanic activity worldwide
- **VAAC advisory reposts** — Volcanic ash advisories republished with additional context
- **Volcano database** — Information pages for volcanoes worldwide
- **Earthquake listings** — Near-real-time earthquake lists near volcanoes
- **Webcam links** — Links to volcano webcams
- **Activity maps** — Map of currently active volcanoes

## API Details

No API. VolcanoDiscovery is a content website with no programmatic data access. The site includes:

**Latest news:**
```
https://www.volcanodiscovery.com/volcano/news.html
```

**Volcano database:**
```
https://www.volcanodiscovery.com/volcanoes/alphabetical-list/a-z.html
```

**Earthquake lists:**
```
https://www.volcanodiscovery.com/earthquakes/lists.html
```

During testing, the site showed current VAAC advisories (Popocatépetl, Reventador, Fuego, Sangay) and was actively updating with new content.

## Freshness Assessment

Good for a content site — news articles and VAAC reposts appear within minutes/hours of events. However, this is editorial content, not structured data.

## Entity Model

Not applicable — no structured data API. Content is editorial HTML articles.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Frequently updated editorial content |
| Openness | 0 | No API, proprietary content |
| Stability | 2 | Long-running site but commercial entity |
| Structure | 0 | HTML articles, no structured data |
| Identifiers | 1 | Uses volcano names, links to GVP |
| Additive Value | 1 | Aggregation value, but no unique data |
| **Total** | **6/18** | |

## Notes

- **Dismissed** — No API or structured data. Content website only.
- Useful as a human-readable reference and news aggregation but not suitable for machine integration.
- Much of the "data" is reposted from primary sources (VAACs, USGS, GVP) that should be consumed directly.
- The earthquake listings appear to source from USGS, EMSC, and other seismic agencies.
- The site is also a commercial tour operator, which influences content priorities.
