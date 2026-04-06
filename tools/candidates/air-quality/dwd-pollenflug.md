# DWD Pollenflug (Pollen Forecast) & European Pollen Networks

**Country/Region**: Germany (DWD); Europe-wide networks
**Publisher**: Deutscher Wetterdienst (DWD) / PID (Stiftung Deutscher Polleninformationsdienst)
**API Endpoint**: `https://opendata.dwd.de/climate_environment/health/alerts/s31fg.json`
**Documentation**: https://opendata.dwd.de/climate_environment/health/alerts/
**Protocol**: HTTP file download (JSON)
**Auth**: None
**Data Format**: JSON
**Update Frequency**: Daily (weekdays, updated in the morning)
**License**: Open data (DWD Geodatenzugangsgesetz — free for all uses with attribution)

## What It Provides

DWD provides daily pollen forecasts for Germany, covering 8 allergenic plant types across 27 forecast regions. The forecast uses a 0-3 intensity scale for today and tomorrow. This is one of the few machine-readable, open-access pollen forecast APIs in Europe. Additionally, European networks like Polleninfo.org (EAN — European Aeroallergen Network), RNSA (France), and the UK Met Office pollen forecast provide regional data, though most lack structured APIs.

## API Details

- **DWD Pollen Endpoint**: `https://opendata.dwd.de/climate_environment/health/alerts/s31fg.json`
- **Response Structure**: JSON object with metadata (last_update, next_update, sender) and content by region
- **Pollen Types** (8): Hasel (Hazel), Erle (Alder), Birke (Birch), Esche (Ash), Gräser (Grasses), Roggen (Rye), Beifuß (Mugwort), Ambrosia (Ragweed)
- **Intensity Scale**: 0 (none), 0-1 (none to low), 1 (low), 1-2 (low to moderate), 2 (moderate), 2-3 (moderate to high), 3 (high)
- **Regions** (27): German regions grouped by state (e.g., Schleswig-Holstein und Hamburg, Nordrhein-Westfalen, Bayern nördl. der Donau, etc.)
- **Forecast Periods**: today, tomorrow, day_after_tomorrow (varies by availability)
- **European Networks** (no structured API confirmed):
  - **Polleninfo.org / EAN**: European Aeroallergen Network — web-based forecasts for multiple countries
  - **RNSA (France)**: Réseau National de Surveillance Aérobiologique — weekly pollen bulletins
  - **UK Met Office Pollen**: 5-day pollen forecast for UK regions — available on website but no public API

## Freshness Assessment

DWD updates pollen forecasts daily on weekdays (not weekends/holidays). The JSON file includes `last_update` and `next_update` timestamps. During the pollen season (typically February-September), forecasts are most relevant. Outside the season, values are typically 0.

## Entity Model

- **Region** → id, name (German region), list of sub-regions
- **Pollen Type** → 8 types with German and Latin names
- **Forecast** → region × pollen type × period (today/tomorrow/day_after_tomorrow) → intensity (0-3 scale)
- **Metadata** → last_update, next_update, sender

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 2 | Daily forecasts (weekdays only); not real-time measurements |
| Openness | 3 | No auth, open government data, simple JSON file |
| Stability | 3 | DWD is Germany's national weather service; long-standing service |
| Structure | 3 | Simple, self-contained JSON; easy to parse |
| Identifiers | 2 | Region IDs and pollen type keys (German names) |
| Additive Value | 3 | Unique data type — pollen forecasts are not covered by standard AQ APIs |
| **Total** | **16/18** | |

## Notes

- This is a pollen *forecast*, not a measurement. It's based on phenological models and observed pollen counts, but the API output is a predicted intensity, not a measured pollen concentration.
- The endpoint serves a single JSON file covering all of Germany — trivially simple to consume.
- German-language field names (Hasel, Erle, Birke, etc.) need to be mapped to English/Latin names for international use.
- Weekend/holiday gaps mean forecasts may become stale by Monday — client code should respect the `next_update` timestamp.
- European pollen networks (Polleninfo.org, RNSA, UK Met Office) generally only provide web-based forecasts without structured APIs. DWD's JSON endpoint is the exception.
- CAMS (Copernicus) also provides modelled pollen forecasts for Europe (birch, grass, olive, ragweed, alder) — this may be a better source for pan-European coverage.
- Pollen data is a natural complement to air quality data for health-focused applications, especially for allergy sufferers.
