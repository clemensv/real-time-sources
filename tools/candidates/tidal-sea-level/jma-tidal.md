# JMA Tidal Observation Data (Japan Meteorological Agency)

**Country/Region**: Japan
**Publisher**: Japan Meteorological Agency (JMA / 気象庁)
**API Endpoint**: `https://www.jma.go.jp/bosai/tidelevel/` (web application); `https://www.data.jma.go.jp/` (data portal)
**Documentation**: https://www.jma.go.jp/bosai/tidelevel/ (Japanese)
**Protocol**: Web application with JSON data feeds (internal API); file downloads
**Auth**: None
**Data Format**: JSON (internal), CSV/ASCII (download)
**Update Frequency**: Real-time (minutes-level observations)
**License**: Government of Japan open data (free for non-commercial and commercial use with attribution)

## What It Provides

JMA operates a network of approximately 80+ tidal observation stations (検潮所) across Japan. The system is integral to Japan's tsunami warning infrastructure but also provides routine tidal observations.

Data includes:
- Real-time observed tide levels (潮位観測情報)
- Astronomical tide predictions (天文潮位)
- High tide warning/caution periods (高潮注意・警戒期間)
- Historical tidal observations

The web application at `/bosai/tidelevel/` provides interactive graphs showing observed vs. predicted tide levels, enabling visual comparison and anomaly detection.

## API Details

The primary interface is a JavaScript web application that loads JSON data from JMA's internal API endpoints. These are not officially documented as a public API but can be reverse-engineered:

- Station list and metadata: loaded via JSON from JMA's bosai (防災) data infrastructure
- Tidal observation data: JSON time series with observed/predicted values
- The application uses Leaflet maps and chart.js-style visualization

Historical/archival data may be available through:
- `https://www.data.jma.go.jp/gmd/kaiyou/db/tide/` — historical tide data portal
- Monthly/annual tide table publications

The lack of a formally documented REST API is the main barrier. The internal JSON feeds exist but are subject to change without notice.

## Freshness Assessment

Excellent for the web application — real-time operational data for tsunami monitoring. However, programmatic access is not officially supported, making reliability uncertain for automated ingestion.

## Entity Model

- **Station (検潮所)**: station code, name (Japanese), latitude, longitude, prefecture
- **Observation**: timestamp, observed tide level (cm), predicted astronomical tide (cm)
- **Alert Period**: high tide warning/caution time windows

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time operational data for tsunami warning |
| Openness | 2 | Data is publicly viewable; no documented API; data reuse policy exists |
| Stability | 3 | Government agency, critical national infrastructure |
| Structure | 1 | No public API; internal JSON feeds; web-scraping required |
| Identifiers | 2 | JMA station codes; limited international cross-referencing |
| Additive Value | 2 | ~80 Japanese coastal stations; tsunami-optimized network |
| **Total** | **13/18** | |

## Notes

- Japan's tide gauge network is primarily designed for tsunami detection and warning — it reports faster than most other national networks.
- The biggest challenge is the lack of a public API. JMA's data infrastructure (bosai system) uses internal JSON feeds that power their web applications but aren't documented for external consumption.
- Many JMA tidal stations also report through the IOC SLSMF, which may be a more reliable programmatic access path.
- Japanese language throughout — station names, documentation, and data labels are all in Japanese.
- The JMA open data policy technically allows reuse, but the practical access barrier (no API) significantly reduces feasibility for automated integration.
- Worth monitoring: Japan has been progressively opening government data, and a formal API may emerge.
