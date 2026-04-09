# NWS Marine Weather Forecasts — Puget Sound Zones

- **Country/Region**: US — Puget Sound / Pacific Northwest
- **Publisher**: NOAA National Weather Service (NWS), Seattle Forecast Office
- **Endpoint**: `https://tgftp.nws.noaa.gov/data/forecasts/marine/coastal/pz/` (text) and `https://api.weather.gov/zones/forecast/` (metadata)
- **Protocol**: HTTP (text files) / REST (metadata)
- **Auth**: None (User-Agent header recommended for api.weather.gov)
- **Format**: Plain text (forecast), JSON (zone metadata)
- **Freshness**: Updated every 6 hours (4x daily), with amendments as conditions warrant
- **Docs**: https://www.weather.gov/marine/sewmz
- **Score**: 13/18

## Overview

The NWS Seattle office issues marine weather forecasts for 14+ zones covering Puget Sound, the Strait of Juan de Fuca, and the Pacific coast of Washington. These forecasts include wind speed/direction, wave height, visibility, and weather conditions. For a Puget Sound free-time advisor, marine forecasts are essential for boating, kayaking, sailing, ferry travel, and coastal hiking safety.

## API Details

**Marine Forecast Text Files (most reliable access):**
```
https://tgftp.nws.noaa.gov/data/forecasts/marine/coastal/pz/pzz{zone}.txt
```

**Key Puget Sound Zones:**

| Zone Code | Area |
|-----------|------|
| PZZ130 | West Entrance U.S. Waters Strait of Juan de Fuca |
| PZZ131 | Central U.S. Waters Strait of Juan de Fuca |
| PZZ132 | East Entrance U.S. Waters Strait of Juan de Fuca |
| PZZ133 | Northern Inland Waters Including The San Juan Islands |
| PZZ134 | Admiralty Inlet |
| PZZ135 | Puget Sound and Hood Canal |

**Zone Metadata via api.weather.gov:**
```
GET https://api.weather.gov/zones/forecast/PZZ135
```
Returns zone metadata (name, geometry, state, office) as JSON. Note: as of testing, the forecast endpoint (`/zones/forecast/PZZ135/forecast`) returns "Marine Forecast Not Supported" — the text file access is the reliable method.

**Forecast Content Includes:**
- Wind speed (knots) and direction
- Wave/swell height and period
- Visibility
- Weather conditions (rain, fog, etc.)
- Small craft advisories, gale warnings
- Tonight, tomorrow, and extended outlook periods

**Alternative: RSS/Atom Feeds:**
NWS provides Atom feeds for weather alerts by zone which can include marine warnings:
```
https://alerts.weather.gov/cap/wwaatmget.php?x=WAZ001&y=0
```

## Freshness Assessment

Good. Marine forecasts are issued 4 times daily (every 6 hours) with additional amendments during rapidly changing conditions. Marine warnings and advisories (small craft advisory, gale warning) are issued immediately when conditions warrant.

## Entity Model

- **Zone** — Zone code (PZZ###), name, geographic area
- **Forecast Period** — Tonight, Tomorrow, Tomorrow Night, etc.
- **Conditions** — Wind (speed, direction, gusts), waves, visibility, weather
- **Advisory** — Small Craft Advisory, Gale Warning, Storm Warning

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 2 | 6-hourly, with amendments; not continuous streaming |
| Openness | 3 | US federal public domain, no auth |
| Stability | 3 | NWS operational service, decades of reliability |
| Structure | 1 | Plain text format requires parsing; no structured JSON for forecasts |
| Identifiers | 2 | Zone codes are stable and well-documented |
| Additive Value | 2 | Marine-specific forecasts not in general NWS weather bridge |
| **Total** | **13/18** | |

## Notes

- The biggest challenge is parsing: marine forecasts are plain text, not structured JSON. The repo's existing RSS bridge could potentially handle Atom alert feeds.
- The NWS api.weather.gov does NOT currently support marine forecast retrieval (returns 404). The text file approach is the reliable path.
- Community project `puget-sound-marine-forecast` (GitHub) wraps these text forecasts into a JSON API — could be a reference implementation.
- Marine forecasts are distinct from land weather forecasts and contain information (wave heights, visibility over water, small craft advisories) that general weather APIs don't provide.
- Existing `noaa-nws` bridge may already handle some of this via general forecast endpoints. The marine zones are specifically what's additive.
