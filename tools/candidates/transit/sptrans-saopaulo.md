# SPTrans — São Paulo Bus Real-Time

**Country/Region**: Brazil (São Paulo)
**Publisher**: SPTrans (São Paulo Transporte S.A.)
**API Endpoint**: `http://api.olhovivo.sptrans.com.br/v2.1/`
**Documentation**: https://www.sptrans.com.br/desenvolvedores/ (Olho Vivo API)
**Protocol**: REST/JSON (session-based auth)
**Auth**: API key + session authentication (free registration via SPTrans developer portal)
**Data Format**: JSON
**Update Frequency**: Real-time — bus positions updated every ~30 s
**License**: SPTrans Open Data (free for commercial and non-commercial use)

## What It Provides

São Paulo has the largest bus fleet in the Western Hemisphere — approximately 14,000 buses operating on 1,300+ routes, carrying 8+ million passengers daily. SPTrans' Olho Vivo ("Watchful Eye") API provides:

- **Bus Positions**: real-time GPS positions of all 14,000+ buses — one of the largest real-time vehicle tracking datasets in the world
- **Arrival Predictions**: estimated arrival times at bus stops
- **Route Information**: lines, stops, itineraries
- **Corridor Positions**: dedicated bus lanes (BRT corridors) — real-time tracking
- **Bus Stop Data**: all bus stops with coordinates

## API Details

The Olho Vivo API uses a session-based authentication model:

1. `POST /Login/Autenticar?token={apiKey}` — authenticate and get session cookie
2. `GET /Posicao` — all bus positions in the city (returns ~14K vehicles!)
3. `GET /Posicao/Linha?codigoLinha={id}` — positions for a specific route
4. `GET /Previsao/Parada?codigoParada={id}` — arrival predictions at a stop
5. `GET /Previsao/Linha?codigoLinha={id}` — predictions for an entire route
6. `GET /Linha/Buscar?termosBusca={query}` — route search
7. `GET /Parada/Buscar?termosBusca={query}` — stop search

Rate limits: reasonable for development use; session expires and needs re-authentication periodically.

API returned 401 in testing without authentication — confirming the session-based auth requirement.

## Freshness Assessment

Excellent for bus positions — São Paulo's entire fleet of 14,000+ buses reports GPS positions in near-real-time. This is one of the largest open real-time vehicle tracking datasets globally. Arrival predictions are derived from the AVL system and are generally reliable on high-frequency corridors. The main limitation is bus-only coverage — São Paulo Metro (Metrô) and CPTM (commuter rail) have separate systems without open APIs.

## Entity Model

- **Posicao (Position)**: hr (timestamp), l (lines array → cl: route code, lt0/lt1: origin/destination, sl: direction, vs: vehicles array → p: plate, a: accessibility flag, py: lat, px: lon, ta: timestamp)
- **Previsao (Prediction)**: p (stop) → l (lines) → vs (vehicles with t: arrival time, a: accessibility)
- **Linha (Line)**: cl (code), lt (label), tl (type), sl (direction), tp/ts (origin/destination)
- **Parada (Stop)**: cp (code), np (name), py/px (lat/lon)
- All field names are abbreviated Portuguese

## Feasibility Rating

| Criterion       | Score | Notes                                                        |
|-----------------|-------|--------------------------------------------------------------|
| Freshness       | 3     | 14K+ buses in real-time — massive, live dataset               |
| Openness        | 2     | Free registration; session-based auth adds complexity         |
| Stability       | 2     | Long-running (since 2012); but informal API evolution          |
| Structure       | 1     | Abbreviated Portuguese field names; no standard schema         |
| Identifiers     | 1     | SPTrans-internal codes; no international standard alignment   |
| Additive Value  | 2     | Scale is extraordinary; Latin America coverage is unique      |
| **Total**       | **11/18** |                                                           |

## Notes

- The sheer scale of 14,000+ buses reporting GPS in real-time makes this one of the world's largest open transit datasets — comparable only to cities like London or New York.
- The session-based authentication (POST to authenticate, then use cookie) is unusual for a transit API — most use header-based API keys.
- São Paulo also publishes GTFS static feeds that can be paired with the real-time API for schedule-based analysis.
- The abbreviated Portuguese field names (`py`/`px` for lat/lon, `lt` for line text, `ta` for timestamp) make the API challenging without documentation.
- Coverage is bus-only — São Paulo Metro and CPTM commuter rail operate separate systems. The metro does publish some open data through the state government portal.
- The "accessibility flag" (`a`) on each vehicle position indicates whether the bus has wheelchair access — a notable inclusivity feature.
