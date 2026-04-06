# Seoul TOPIS — South Korea Transit Open Data

**Country/Region**: South Korea (Seoul Metropolitan Area)
**Publisher**: Seoul Metropolitan Government (TOPIS — Transport OPeration & Information Service) + Korea data.go.kr
**API Endpoint**: `http://ws.bus.go.kr/api/rest/` (Seoul Bus), `http://openapi.seoul.go.kr:8088/` (Seoul Open API)
**Documentation**: https://www.data.go.kr/ (national) and https://topis.seoul.go.kr/ (Seoul TOPIS)
**Protocol**: REST/XML (Seoul Bus), REST/JSON or XML (Seoul Open API)
**Auth**: API key required (free registration at data.go.kr — Korean portal)
**Data Format**: XML (bus), JSON or XML (metro/general)
**Update Frequency**: Real-time — bus positions every ~15 s; metro arrivals real-time
**License**: Korea Open Government License (KOGL Type 1 — free use with attribution)

## What It Provides

Seoul's TOPIS system is one of the most data-rich urban transit monitoring platforms in the world. It covers:

- **Seoul Bus**: real-time GPS positions for all 7,400+ buses on 360+ routes — one of the world's largest real-time bus tracking deployments
- **Seoul Metro**: real-time arrival predictions at all stations across Lines 1-9, Gyeongui-Jungang, Suin-Bundang, Shinbundang, and more
- **Traffic**: real-time road speed data across Seoul's road network
- **Transfer information**: connections between bus/metro/rail

The Korean national open data portal (data.go.kr) provides the API key management and documentation. Seoul-specific transit APIs are accessed through TOPIS endpoints.

## API Details

### Seoul Bus API

- `GET /buspos/getBusPosByRtid?serviceKey={key}&busRouteId={id}` — bus positions on a route
- `GET /arrive/getArrInfoByRouteAll?serviceKey={key}&busRouteId={id}` — arrival predictions
- `GET /busRouteInfo/getBusRouteList?serviceKey={key}&strSrch={query}` — route search
- `GET /stationinfo/getStationByName?serviceKey={key}&stSrch={query}` — stop search

Confirmed: API endpoint is live (returned XML structure, but "key not registered" error with test key — needs proper data.go.kr registration).

### Seoul Metro (Real-time Arrival)

- `GET /{key}/json/realtimeStationArrival/1/5/{stationName}` — real-time metro arrivals
- Returns train position, destination, arrival time, congestion level

### T-money (Smart Card)

T-money (Korea's transit smart card) aggregated usage data is available through data.go.kr as batch datasets — not real-time API, but provides origin-destination matrices and ridership patterns.

## Freshness Assessment

Excellent. Seoul's bus tracking is among the most comprehensive in the world — 7,400+ buses reporting GPS positions in near-real-time. Metro arrival predictions use track circuit data with high accuracy. The TOPIS control center (Transport OPeration & Information Service) is a sophisticated traffic management center that feeds data to these APIs. The main barrier is registration — the data.go.kr portal is Korean-language and requires a Korean phone number for some verification steps, though international registration is possible.

## Entity Model

- **Bus Position**: plainNo (plate), posX/posY (GPS), dataTm, busType, lastStnId, nextStnId, sectDist
- **Bus Arrival**: stNm (stop name), busRouteAbrv (route), arrmsg1/arrmsg2 (arrival messages), traTime1/traTime2 (travel time remaining), isFullFlag (crowding)
- **Metro Arrival**: statnNm (station), trainLineNm (line), barvlDt (arrival seconds), bstatnNm (destination), btrainSttus (express/normal), btrainNo
- All IDs are Korean national standards; stop/route IDs are numeric

## Feasibility Rating

| Criterion       | Score | Notes                                                        |
|-----------------|-------|--------------------------------------------------------------|
| Freshness       | 3     | Massive real-time bus fleet + metro arrivals                  |
| Openness        | 2     | Free API key but Korean portal; international access possible |
| Stability       | 3     | Government-backed (Seoul Metropolitan), TOPIS is long-running |
| Structure       | 2     | XML-dominant; Korean field names; multiple API patterns       |
| Identifiers     | 2     | Korean national codes; not internationally standardized       |
| Additive Value  | 2     | One of world's largest bus tracking deployments; Asian coverage|
| **Total**       | **14/18** |                                                           |

## Notes

- Seoul's 7,400+ bus fleet with real-time GPS tracking is genuinely one of the largest deployments globally — comparable to London or NYC.
- The Korean data portal (data.go.kr) is the gateway to all Korean open data — it hosts transit APIs for other cities too (Busan, Daejeon, Incheon, etc.).
- The metro congestion level data (car-level crowding) is a distinctive feature — very few systems provide this.
- Kakao Map / Naver Map have excellent transit routing in Korea but their APIs are commercial — the government APIs are the open alternative.
- Field names in the API are Korean abbreviations — documentation is essential for interpretation.
- For broader Korean coverage, similar APIs exist for Busan, Daejeon, Gwangju, and Daegu through data.go.kr.
