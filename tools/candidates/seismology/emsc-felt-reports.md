# EMSC Felt Reports & Testimonies

## Source Identity

| Field            | Value |
|------------------|-------|
| **Full Name**    | EMSC LastQuake — Felt Report Collection System |
| **Operator**     | Euro-Mediterranean Seismological Centre (EMSC) |
| **URL**          | https://www.seismicportal.eu/ , https://www.emsc-csem.org/ |
| **API Base**     | `https://www.seismicportal.eu/testimonies-ws/api/search?` |
| **Coverage**     | Global (crowdsourced felt reports) |
| **Update Freq.** | Real-time; testimonies arrive within minutes of felt events |

## What It Does

Beyond instrumental earthquake data, EMSC operates one of the world's largest earthquake felt-report collection systems. When people feel an earthquake, they report their experience through the LastQuake app or EMSC website. These "testimonies" are collected, geolocated, and made available through a dedicated API.

Felt reports are a fundamentally different kind of data from seismometer readings. They answer "what did humans experience?" rather than "what did instruments measure?" — capturing shaking intensity, damage observations, and behavioral responses that no sensor can provide.

EMSC collects testimonies in multiple languages and provides them alongside the FDSN instrumental catalog. Other felt-report systems include USGS "Did You Feel It?" (DYFI), INGV "Hai Sentito il Terremoto?", and various national systems. EMSC's is the most internationally diverse.

## Endpoints Verified

| Endpoint | Status | Notes |
|----------|--------|-------|
| EMSC FDSN event service | ✅ 200 | Instrumental data (already documented) |
| WebSocket push | ✅ Documented | Real-time event notifications |
| Testimonies API | ⚠️ Not probed | Documented in EMSC API docs |
| DYFI (USGS) | ✅ Part of event GeoJSON | Embedded in USGS feed `felt` and `cdi` fields |

### USGS DYFI Data (embedded in standard feed)

```json
{
  "properties": {
    "mag": 4.8,
    "felt": 42,
    "cdi": 4.2,
    "mmi": 3.6,
    "place": "153 km ESE of Kokopo, Papua New Guinea"
  }
}
```

The `felt` field gives number of felt reports, `cdi` gives the community decimal intensity (crowdsourced), and `mmi` gives the instrumental Modified Mercalli Intensity.

## Authentication & Licensing

- **Auth**: None for EMSC FDSN; testimonies API may require registration.
- **License**: EMSC open data policy; USGS public domain.

## Integration Notes

Felt-report data is valuable as an enrichment layer on instrumental earthquake data. The USGS already embeds DYFI data directly in the standard GeoJSON feed (`felt`, `cdi` fields), meaning the existing USGS bridge already carries this information. EMSC's testimony data would add European/Mediterranean felt reports.

The real opportunity is correlating instrumental magnitude with felt intensity — a M3.5 at 5 km depth will be felt very differently from a M5.0 at 100 km. Felt reports ground-truth the human impact.

## Feasibility Rating

| Dimension                    | Score | Notes |
|------------------------------|-------|-------|
| **API Maturity & Docs**      | 2     | Documented but not fully probed |
| **Data Freshness**           | 3     | Real-time crowdsourced |
| **Format / Schema Quality**  | 2     | JSON; schema varies by system |
| **Auth / Access Simplicity** | 2     | USGS embedded (free); EMSC may need registration |
| **Coverage Relevance**       | 3     | Global crowdsourced impact data |
| **Operational Reliability**  | 3     | USGS and EMSC both well-established |
| **Total**                    | **15 / 18** | |

## Verdict

⚠️ **Maybe — enrichment value** — USGS DYFI data is already in the existing feed. EMSC testimonies would add value for non-US events. This is best treated as an enrichment layer rather than a standalone source. The existing EMSC bridge (when built) should capture testimony counts as part of event metadata. No separate bridge needed unless detailed testimony text/location data is required.
