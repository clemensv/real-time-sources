# Ambee Pollen API

- **Country/Region**: Global (including Seattle / Puget Sound / Pacific Northwest)
- **Publisher**: Ambee (private company)
- **Endpoint**: `https://api.ambeedata.com/latest/pollen/by-lat-lng`
- **Protocol**: REST
- **Auth**: API Key (free tier available)
- **Format**: JSON
- **Freshness**: Daily forecasts with hourly updates
- **Docs**: https://docs.ambeedata.com/apis/pollen
- **Score**: 12/18

## Overview

Ambee provides hyperlocal pollen data at 500m resolution, including species-specific counts for trees, grasses, and weeds. For the Puget Sound area, relevant allergens include alder, birch, cedar, Douglas fir, and grass pollens which drive seasonal allergies from February through September. This data enables a free-time advisor to warn allergy sufferers about high pollen days and recommend indoor activities or less-allergenic areas.

## API Details

**Base URL:** `https://api.ambeedata.com/`

**Authentication:** `x-api-key: {YOUR_API_KEY}` header

**Key Endpoints:**

| Endpoint | Description |
|----------|-------------|
| `GET /latest/pollen/by-lat-lng?lat=47.6062&lng=-122.3321` | Current pollen for Seattle |
| `GET /forecast/pollen/by-lat-lng?lat=47.6062&lng=-122.3321` | Pollen forecast |
| `GET /history/pollen/by-lat-lng?lat=47.6062&lng=-122.3321&from=...&to=...` | Historical data |

**Response Fields:**
- `Count` — Pollen grains per cubic meter (tree, grass, weed categories)
- `Risk` — Risk level per category (Low, Moderate, High, Very High)
- `Species` — Individual species data (Alder, Birch, Cedar, Oak, Grass, Ragweed, etc.)
- `updatedAt` — Timestamp of data

**Alternative Free Pollen APIs:**
- Google Maps Pollen API (requires Google Cloud billing account)
- BreezoMeter Pollen API (commercial, limited free tier)
- No fully open/free pollen API exists; all require registration

## Freshness Assessment

Fair. Pollen forecasts are generated daily with model-based predictions. Actual pollen counts depend on station sampling (which is sparse in the PNW — Northwest Asthma & Allergy Center in Seattle is the primary station). API provides interpolated/modeled data rather than direct measurements.

## Entity Model

- **Location** — Latitude/longitude point
- **Pollen Index** — Overall and per-category (tree, grass, weed)
- **Species** — Individual plant species pollen counts
- **Risk Level** — Categorical severity assessment
- **Forecast** — Multi-day pollen outlook

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 2 | Daily model updates, not real-time measured |
| Openness | 1 | Free tier exists but commercial API; rate limits apply |
| Stability | 2 | Private company; API has been stable but no government backing |
| Structure | 3 | Well-designed REST JSON API |
| Identifiers | 2 | Coordinate-based; species names are stable |
| Additive Value | 2 | Unique allergen data not covered by air quality feeds |
| **Total** | **12/18** | |

## Notes

- Pollen is a significant outdoor activity factor in the PNW: alder pollen starts in February, grass pollen peaks June–July, and weed pollen runs through September.
- No truly open/free pollen API exists. Ambee's free tier is the most accessible option.
- The existing `air-quality/dwd-pollenflug.md` candidate covers Germany's DWD pollen data — similar concept but different region.
- Alternative approach: NWS forecast discussions sometimes mention pollen conditions, and the existing NWS bridge could be monitored for pollen-related text.
- Consider combining pollen risk with UV index for a comprehensive "outdoor comfort" score.
