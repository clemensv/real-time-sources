# Earth Networks Total Lightning Network (ENTLN)

**Country/Region**: Global
**Publisher**: Earth Networks, Inc.
**Developer Portal**: `https://developer.earthnetworks.com/`
**API Base**: `https://earthnetworks.azure-api.net/data/`
**Protocol**: REST over HTTPS (Azure API Management)
**Auth**: Subscription key required (`Ocp-Apim-Subscription-Key` header) — commercial license
**Data Format**: JSON
**Update Frequency**: Near real-time (Sferic Data Stream is push/streaming)
**License**: Commercial only — no free tier

## What It Provides

Earth Networks operates the Total Lightning Network (ENTLN), claiming 1,800+ sensors in 100+ countries. The network detects both cloud-to-ground (CG) and intra-cloud (IC) lightning globally. It's the largest commercial ground-based lightning detection network and also powers the WeatherBug consumer weather application.

Products include:
- **Sferic Data Stream** — real-time streaming lightning data feed
- **Lightning Alerts** — location-based lightning proximity warnings
- **Historical Lightning Data** — archive access
- **Forecasts** — daily/hourly weather forecasts

## API Details

The developer portal at `https://developer.earthnetworks.com/` documents a REST API behind Azure API Management:

- Base URL: `https://earthnetworks.azure-api.net/data/`
- Auth: `Ocp-Apim-Subscription-Key` header (subscription key required)
- Format: JSON responses
- Documented endpoints: Forecasts (daily/hourly). Lightning-specific endpoints (`/lightning/`, Sferic Data Stream) exist but require commercial agreement.

### Access Barrier

All attempts to access data without a subscription key return 401 Unauthorized. No free tier, trial period, or public data sample was discoverable. Contact sales is required.

## Freshness Assessment

Real-time by reputation. The Sferic Data Stream is a push/streaming product designed for operational weather monitoring. However, no data was retrievable to verify freshness independently.

## Entity Model

- **Lightning Stroke** — individual CG or IC event with location, time, polarity, peak current
- **Lightning Alert** — proximity-based warning for a specified location
- **Forecast** — weather forecast data (secondary product)

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 3 | Real-time streaming (by reputation) |
| Openness | 0 | Commercial only, no free tier, no public data |
| Stability | 3 | Azure APIM infrastructure, established company |
| Structure | 3 | Well-documented REST API, JSON |
| Identifiers | 2 | Stroke-level data with timestamps |
| Additive Value | 2 | Global coverage but duplicated by open sources (GLM, Blitzortung) |
| **Total** | **13/18** | |

## Notes

- Earth Networks has excellent API infrastructure (Azure APIM, developer portal, multi-language SDKs) — this is a production-grade commercial product.
- The commercial-only access model means this is not viable for open data integration unless a commercial agreement is established.
- For comparable coverage at no cost, combine NOAA GLM (Western Hemisphere) + EUMETSAT MTG-LI (Europe/Africa) + Blitzortung (global crowdsourced).
- Earth Networks also provides severe weather alerts, precipitation data, and air quality monitoring — potentially interesting for a broader commercial data strategy.
- Dismissed for open integration but noted for reference — if commercial lightning data becomes a requirement, this is the primary alternative to Vaisala.
