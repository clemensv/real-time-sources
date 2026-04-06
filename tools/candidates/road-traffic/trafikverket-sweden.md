# Trafikverket Sweden

**Country/Region**: Sweden
**Publisher**: Trafikverket (Swedish Transport Administration)
**API Endpoint**: `https://api.trafikinfo.trafikverket.se/v2/data.json` (Trafikinfo API) and `https://datex.trafikverket.se/` (DATEX II portal)
**Documentation**: https://data.trafikverket.se/ (Datautbytesportal)
**Protocol**: REST (POST with XML query body) / DATEX II
**Auth**: API Key (free registration at data.trafikverket.se)
**Data Format**: JSON / XML (DATEX II)
**Update Frequency**: Real-time (1–5 minutes for traffic flow; immediate for incidents)
**License**: Creative Commons Zero (CC0)

## What It Provides

Trafikverket operates Sweden's national road traffic data platform, providing comprehensive real-time traffic information including traffic flow (speeds, volumes), road conditions, weather, incidents, roadworks, travel times, and camera images. The platform serves both a custom REST API (Trafikinfo) and a DATEX II portal for European-standard data exchange.

## API Details

**Trafikinfo API (custom query language):**
```
POST https://api.trafikinfo.trafikverket.se/v2/data.json
Content-Type: text/xml

<REQUEST>
  <LOGIN authenticationkey="{API_KEY}"/>
  <QUERY objecttype="TrafficFlow" schemaversion="1.5">
    <FILTER>
      <WITHIN name="Geometry.WGS84" shape="center" value="18.0686 59.3293" radius="5000"/>
    </FILTER>
  </QUERY>
</REQUEST>
```

Available object types include:
- `TrafficFlow` — real-time traffic speeds and volumes
- `Situation` — incidents, accidents, roadworks (DATEX II aligned)
- `RoadCondition` — road surface conditions and weather effects
- `WeatherMeasurepoint` — road weather station data
- `Camera` — traffic camera metadata and images
- `TravelTimeRoute` — estimated travel times between points
- `FerryAnnouncement` — ferry service information

**DATEX II portal (datex.trafikverket.se):**
Provides DATEX II v3 feeds for:
- Situation publications (incidents, roadworks)
- Measurement data
- Travel time data

The DATEX II portal requires separate registration.

## Freshness Assessment

Traffic flow data updates every 1–5 minutes from road sensors. Situations (incidents, roadworks) are updated in real-time as events occur. Weather data updates every 10–30 minutes. Travel times are computed in real-time from sensor data. CC0 license means zero restrictions on use. Very fresh data overall.

## Entity Model

- **Traffic Flow**: Speed, volume, occupancy per measurement point
- **Situation**: Incident/roadwork with type, location, severity, expected duration
- **Road Condition**: Surface state, friction, ice warning
- **Weather**: Temperature, wind, precipitation, visibility at road weather stations
- **Travel Time**: Route-based estimated travel times
- **Camera**: Traffic camera metadata with image URLs

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time traffic flow, instant incident updates |
| Openness | 3 | CC0 license; free API key registration |
| Stability | 3 | Government-operated, well-established platform |
| Structure | 3 | Custom XML query language + DATEX II; well-documented |
| Identifiers | 3 | Measurement point IDs, situation IDs, route IDs |
| Additive Value | 3 | Comprehensive Swedish traffic data; DATEX II alignment with EU standards |
| **Total** | **18/18** | |

## Notes

- Trafikverket's custom query API is unusual — it uses XML POST requests with a proprietary query language including spatial filters, change tracking, and subscription support. The query language supports `FILTER`, `WITHIN` (geographic), `GT`/`LT` (comparisons), and `CHANGEDSINCECHANGEID` (delta updates).
- The `CHANGEDSINCECHANGEID` feature is particularly powerful for building a bridge — it provides efficient delta polling without needing to diff full snapshots.
- CC0 license is the most permissive possible — no attribution required.
- Trafikverket also provides rail traffic data through the same platform (TrainStation, TrainMessage, etc.) — potential bonus data source.
- The DATEX II portal provides EU-standard data format, useful for building bridges that work across multiple European countries.
- Registration is free at https://data.trafikverket.se/ — provides an API key instantly.
