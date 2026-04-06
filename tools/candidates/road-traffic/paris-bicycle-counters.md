# Paris Bicycle Counters

**Country/Region**: France — Paris
**Publisher**: Ville de Paris
**API Endpoint**: `https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/comptage-velo-donnees-compteurs/records`
**Documentation**: https://opendata.paris.fr/explore/dataset/comptage-velo-donnees-compteurs/
**Protocol**: REST (Opendatasoft API v2.1)
**Auth**: None
**Data Format**: JSON
**Update Frequency**: Daily (J-1 — previous day's data, hourly resolution)
**License**: Licence Ouverte (Open Licence) 2.0

## What It Provides

Hourly bicycle count data from 141 permanent counting stations across Paris, powered by Eco-Compteur hardware. With nearly 900,000 records in a rolling 13-month window, this is one of the richest cycling measurement datasets available. While not true real-time (J-1 delay), the hourly granularity and comprehensive spatial coverage make it valuable for cycling infrastructure analysis and trend detection.

## API Details

**Counter data (hourly counts):**
```
GET https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/comptage-velo-donnees-compteurs/records?limit=100
```

Returns Opendatasoft records:
```json
{
  "id_compteur": "100003096-353242251",
  "nom_compteur": "97 avenue Denfert Rochereau SE-NO",
  "sum_counts": 42,
  "date": "2026-04-05T14:00:00+02:00",
  "coordinates": {"lon": 2.3345, "lat": 48.8365},
  "installation_date": "2019-03-01",
  "mois_annee_comptage": "04/2026"
}
```

**Counter locations (metadata):**
```
GET https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/comptage-velo-compteurs/records?limit=200
```

Returns 141 counter locations with:
- `id_compteur`, `nom_compteur` — Counter ID and name
- `channel_name` — Direction (e.g., "SE-NO", "N-S")
- `installation_date` — When the counter was installed
- `coordinates` — GPS location
- Photos of installation sites
- Links to Eco-Visio visualization

Key API features:
- Pagination: `limit`, `offset`
- Filtering: `where=date >= '2026-04-01'`
- Aggregation: `group_by=id_compteur`
- Geo-queries: `within_distance(coordinates, ...)`
- Export: JSON, CSV, GeoJSON

## Freshness Assessment

Data is published J-1 (previous day) with hourly resolution. This means today's data appears tomorrow. The rolling 13-month window provides ~896,000 records at any time. While this isn't true real-time, the hourly granularity from 141 locations provides excellent cycling pattern visibility. New data arrives daily.

## Entity Model

- **Counter**: Permanent counting station with ID, name, direction, location
- **Count**: Hourly bicycle count per counter
- **Time Series**: 13-month rolling window of hourly data
- **Direction**: Each counter may have multiple channels (one per direction)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | J-1 daily updates (not real-time, but hourly resolution) |
| Openness | 3 | No auth, Licence Ouverte 2.0 |
| Stability | 3 | City-operated, Opendatasoft platform, running for years |
| Structure | 3 | Clean Opendatasoft JSON, well-documented |
| Identifiers | 3 | Counter IDs, channel names, coordinates |
| Additive Value | 3 | Unique dataset — cycling infrastructure measurement; Eco-Compteur pattern reusable for other cities |
| **Total** | **17/18** | |

## Notes

- Paris bicycle counters use Eco-Compteur hardware, the dominant manufacturer of cycling counting equipment worldwide. Many other cities (Berlin, Munich, Montreal, Vancouver, Nordic cities) publish similar data through their own open data portals. The data model is reusable.
- This is a different kind of traffic data — bicycle flow rather than motorized vehicle flow. Valuable for cycling infrastructure planning, seasonal trends, and event impact analysis.
- The Opendatasoft platform pattern is shared with Ghent parking, Melbourne parking, and Basel parking — building Opendatasoft support enables multiple datasets across categories.
- Direction channels (SE-NO, N-S, etc.) indicate the counter measures bidirectional flow separately.
- The Eco-Visio platform provides visualization but no public API. City open data portals are the programmatic access path.
