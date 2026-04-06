# KVERT — Kamchatka Volcanic Eruption Response Team

## Source Identity

| Field            | Value |
|------------------|-------|
| **Full Name**    | Kamchatka Volcanic Eruption Response Team (KVERT) |
| **Operator**     | Institute of Volcanology and Seismology, Russian Academy of Sciences |
| **URL**          | http://www.kscnet.ru/ivs/kvert/ |
| **VONA Page**    | `http://www.kscnet.ru/ivs/kvert/van/index.php?type=1` |
| **Coverage**     | Kamchatka Peninsula and Northern Kuril Islands (Russia) |
| **Update Freq.** | Weekly reports; VONAs issued during eruptions |

## What It Does

Kamchatka has more active volcanoes than almost any comparable-sized area on Earth — about 30 actively erupting volcanoes at any given time. The peninsula is a volcanic conveyor belt where the Pacific Plate subducts under the Okhotsk Plate. Shiveluch, Klyuchevskoy, Bezymianny, Karymsky, Ebeko — these volcanoes erupt with startling regularity.

KVERT monitors all of it and issues Volcano Observatory Notices for Aviation (VONAs) when eruptions pose a hazard to air traffic. Kamchatka lies directly under North Pacific flight routes between Asia and North America, making these advisories operationally critical.

## Endpoints Probed

| Endpoint | Status | Notes |
|----------|--------|-------|
| Main page (HTML) | ✅ 200 | Russian-language; volcano status table |
| VONA information releases | ✅ 200 | HTML pages listing VONAs with aviation color codes |
| RSS feed (kvert/feeds/rss_en.xml) | ❌ Timeout | Feed endpoint unresponsive |
| Current status page | ❌ 404 | URL may have changed |

### VONA Page Structure

The VONA page at `/van/index.php?type=1` lists volcanic activity notifications in a tabular format with:
- Volcano name
- Date/time of observation
- Aviation color code (GREEN/YELLOW/ORANGE/RED)
- Eruption description
- Ash cloud height and drift direction

The content is in English (VONAs are international aviation products) despite the main site being in Russian.

## Authentication & Licensing

- **Auth**: None. Public access.
- **Rate Limits**: Not stated; academic research institution.
- **License**: Russian Academy of Sciences; data freely available for research and operational use.

## Integration Notes

No API — this is pure HTML scraping territory. The VONA pages follow a semi-structured format (HTML tables), but the layout could change without notice. The RSS feed, which would have been the cleanest integration point, was unresponsive during testing.

KVERT VONAs also flow to the Tokyo VAAC (which covers the Kamchatka region for aviation purposes), so the ash advisory data is available through that channel. However, KVERT provides more detailed volcanological context — eruption type, lava flow observations, seismic activity summaries — that the VAAC advisories strip down to aviation-relevant fields.

The website uses HTTP (not HTTPS), which is notable in 2026.

## Feasibility Rating

| Dimension                    | Score | Notes |
|------------------------------|-------|-------|
| **API Maturity & Docs**      | 1     | No API; HTML only; RSS broken |
| **Data Freshness**           | 2     | Weekly reports; VONAs during eruptions |
| **Format / Schema Quality**  | 1     | HTML tables; Russian/English mixed |
| **Auth / Access Simplicity** | 3     | Open, no auth |
| **Coverage Relevance**       | 3     | One of Earth's most active volcanic regions |
| **Operational Reliability**  | 2     | Russian Academy of Sciences; HTTP only; some 404s |
| **Total**                    | **12 / 18** | |

## Verdict

⏭️ **Skip** — Kamchatka is volcanologically critical, but KVERT's web infrastructure is too fragile for reliable integration. No API, broken RSS, HTTP-only, mixed language. Tokyo VAAC covers Kamchatka for aviation ash advisories. For detailed Kamchatka eruption monitoring, KVERT is the source of truth, but it needs a modern web infrastructure before programmatic integration is viable.
