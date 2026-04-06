# FAO Desert Locust Information Service (DLIS)

- **Country/Region**: Sahel, Horn of Africa, North Africa, Arabian Peninsula (locust breeding/invasion zones)
- **Endpoint**: `https://locust-hub-hqfao.hub.arcgis.com` (ArcGIS Hub)
- **Protocol**: ArcGIS REST API / Hub API
- **Auth**: None
- **Format**: JSON, GeoJSON
- **Freshness**: Updated as reports come in (daily during outbreaks)
- **Docs**: https://locust-hub-hqfao.hub.arcgis.com/
- **Score**: 12/18

## Overview

Desert locusts are the world's most destructive migratory pest. A single swarm can
cover 1,200 km² and consume the food supply of 2,500 people per day. The FAO Desert
Locust Information Service (DLIS) monitors swarms across the Sahel, Horn of Africa,
North Africa, and Arabian Peninsula — publishing observation data through an ArcGIS
Hub portal.

The 2019–2021 East Africa locust crisis was the worst in 70 years, devastating crops
in Kenya, Ethiopia, and Somalia. Real-time locust tracking is critical for agricultural
early warning.

Key affected African countries: Kenya, Ethiopia, Somalia, Eritrea, Djibouti, Sudan,
Niger, Mali, Mauritania, Chad, Morocco, Algeria, Libya, Egypt.

## Endpoint Analysis

**Hub portal verified** — the FAO Locust Hub is an ArcGIS Hub site with public datasets.

The Hub API was queried for datasets:
```
GET https://locust-hub-hqfao.hub.arcgis.com/api/v3/datasets?q=swarm
```

The search results returned non-locust results, indicating the dataset naming may differ.
The actual locust data layers are likely named differently (e.g., "Swarm observations",
"Band observations", "Hoppers", "Adults").

Known data layers (from FAO documentation):
- **Swarm observations**: Location, date, size, direction of movement
- **Band observations**: Hopper bands (immature locusts)
- **Adult observations**: Solitary/gregarious adult sightings
- **Control operations**: Pesticide spraying locations and areas treated
- **Soil moisture/vegetation**: Environmental conditions for breeding

The underlying ArcGIS Feature Services need to be identified through the Hub content
API or by examining the hub site's datasets page directly.

## Integration Notes

- **Dataset discovery needed**: The exact ArcGIS Feature Service URLs for locust data
  need to be identified. Try browsing the hub content or searching for "DLIS" or
  "locust" in the ArcGIS Online public datasets.
- **eLocust3 data**: The FAO's mobile reporting system (eLocust3) is used by national
  survey teams. This is the primary data source — field reports uploaded from tablets
  in the desert.
- **Seasonal relevance**: Locust activity is seasonal (tied to rainfall and vegetation).
  The bridge should handle periods of low/no activity gracefully.
- **Critical for food security**: Combine with FEWS NET data to connect locust
  observations with food security impacts.
- **Alternative approach**: If the ArcGIS Hub data is difficult to access programmatically,
  the FAO Locust Watch website (https://www.fao.org/ag/locusts/) publishes situation
  updates and maps that could be scraped.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Daily during outbreaks, weekly otherwise |
| Openness | 2 | Public hub but service URLs not straightforward |
| Stability | 3 | FAO/UN operational system |
| Structure | 2 | ArcGIS services (once discovered) |
| Identifiers | 1 | Observation IDs within ArcGIS |
| Richness | 2 | Swarm location, size, movement, control operations |
