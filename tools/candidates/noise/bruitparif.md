# Bruitparif RUMEUR Network (Paris/Île-de-France)
**Country/Region**: Île-de-France region, France (Paris and surrounds)
**Publisher**: Bruitparif (regional noise observatory, mandated by French law)
**API Endpoint**: `https://rumeur.bruitparif.fr/` (web application)
**Documentation**: https://www.bruitparif.fr/ (organization), https://rumeur.bruitparif.fr/ (data portal)
**Protocol**: Web SPA (Leaflet map, no public REST API discovered)
**Auth**: None for web portal
**Data Format**: HTML/JavaScript (data loaded dynamically)
**Update Frequency**: Real-time (continuous monitoring network)
**License**: French open data principles (loi pour une République numérique)

## What It Provides
Bruitparif operates one of the world's most comprehensive urban noise monitoring networks:
- **RUMEUR network**: ~170 permanent noise monitoring stations across Île-de-France
- **Real-time noise levels**: Continuous LAeq, Lden, Lnight measurements
- **Source categories**: Road traffic, rail, aircraft, neighborhood, construction
- **Airport noise**: Specific monitoring around Paris CDG, Orly, Le Bourget airports
- **Environmental noise maps**: Strategic noise mapping per EU Environmental Noise Directive
- **Health impact assessments**: Years of healthy life lost to noise exposure
- **Quiet area monitoring**: Parks and protected quiet zones
- **Temporal patterns**: Day/evening/night breakdown per EU directive

Bruitparif is one of France's authorized noise observatories (observatoires du bruit) under the code de l'environnement.

## API Details
- **RUMEUR portal**: `https://rumeur.bruitparif.fr/` — interactive Leaflet map (HTTP 200)
  - Station locations, real-time levels, historical charts
  - Data loaded via JavaScript (not directly accessible)
- **Organization**: `https://www.bruitparif.fr/` — reports, publications, methodology
- **Île-de-France open data**: `https://data.iledefrance.fr/` — portal with 1000+ datasets
  - Bruitparif-specific datasets not found via API search (may require catalog browsing)
- **Paris open data**: `https://opendata.paris.fr/` — may host Bruitparif subsets
- **No REST API endpoints found**: `/api`, `/main/stations`, direct JSON paths all returned 404

## Probe Results
```
https://rumeur.bruitparif.fr/: HTTP 200 OK (Leaflet SPA)
https://rumeur.bruitparif.fr/api: HTTP 404
https://rumeur.bruitparif.fr/main/stations: HTTP 404
https://data.iledefrance.fr/ API search for "bruit": HTTP 400 (syntax issue)
Assessment: Major monitoring network, data locked behind web SPA
```

## Freshness Assessment
The monitoring network operates continuously — data is genuinely real-time. Access is the challenge. The RUMEUR web portal displays current noise levels at each station with historical charts. The underlying data exists in real-time but is not exposed via a developer-friendly API.

## Entity Model (Inferred from web interface)
- **Station** (ID, name, location, lat/lon, type: permanent/temporary)
- **Measurement** (LAeq, Lden, Lnight, L10, L50, L90 — percentile levels)
- **Source** (road, rail, aircraft, neighborhood, construction)
- **Period** (day 07-19h, evening 19-23h, night 23-07h per EU directive)
- **Indicator** (annual Lden for strategic noise mapping)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Continuous real-time monitoring |
| Openness | 1 | No public API, web portal only |
| Stability | 3 | Government-mandated observatory, operating since 2004 |
| Structure | 1 | Data locked in JavaScript SPA |
| Identifiers | 2 | Station IDs visible in web interface |
| Additive Value | 3 | One of world's largest urban noise monitoring networks |
| **Total** | **13/18** | |

## Notes
- ~170 stations make this one of the densest urban noise monitoring networks globally
- EU Environmental Noise Directive compliance means standardized metrics (Lden, Lnight)
- French law mandates noise observatories — this is not a voluntary project
- The web SPA likely loads JSON from internal endpoints — reverse-engineering possible
- Contact Bruitparif directly for data access — they may provide researcher/developer APIs
- Île-de-France open data portal may eventually host this data
- Pairs with Dublin Sonitus and Schiphol NOMOS for a European noise monitoring picture
