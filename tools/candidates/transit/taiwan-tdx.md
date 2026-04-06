# Taiwan TDX — Transport Data eXchange

**Country/Region**: Taiwan (national)
**Publisher**: Ministry of Transportation and Communications (MOTC) / Transport Data eXchange (TDX)
**API Endpoint**: `https://tdx.transportdata.tw/api/basic/v2/`
**Documentation**: https://tdx.transportdata.tw/ and https://github.com/tdxmotc
**Protocol**: REST/JSON (OData-compatible query syntax)
**Auth**: Free registration for basic tier; OAuth2 client credentials for higher tiers
**Data Format**: JSON
**Update Frequency**: Real-time — train live boards update every ~60 s; bus positions every 15–30 s
**License**: Open Government Data License (Taiwan)

## What It Provides

Taiwan's TDX is one of the best-designed national transit data platforms in Asia — possibly the world. It provides a unified API covering every mode of public transport across the island:

- **TRA (Taiwan Railways)**: real-time live board with delay times for every station — confirmed working
- **THSR (Taiwan High Speed Rail)**: real-time schedule with delay information
- **Metro**: Taipei MRT, Kaohsiung MRT — real-time departures
- **Bus**: every city bus system (Taipei, Kaohsiung, Taichung, Tainan, etc.) — real-time GPS positions and ETAs
- **InterCity Bus**: long-distance coaches with real-time tracking
- **Ferries**: island ferry services
- **Bike sharing**: YouBike station availability (real-time)
- **Aviation**: flight information

## API Details

The API uses OData-style query parameters for filtering and selection:

- `GET /Rail/TRA/LiveBoard?$top=10&$format=JSON` — TRA train positions/delays at all stations
- `GET /Rail/THSR/DailyTimetable/Today?$format=JSON` — THSR today's timetable with real-time
- `GET /Bus/RealTimeByCity/{City}?$format=JSON` — all bus positions in a city
- `GET /Bus/EstimatedTimeOfArrival/City/{City}?$format=JSON` — bus ETAs
- `GET /Rail/Metro/LiveBoard/{System}?$format=JSON` — metro departures

OData filters: `$filter=`, `$select=`, `$top=`, `$skip=`, `$orderby=`, `$format=JSON|XML`

Confirmed: TRA LiveBoard endpoint returns JSON with `DelayTime` (minutes), bilingual station names (Chinese + English), train type, direction, and schedule times — no authentication required for the basic v2 endpoint.

Rate limits: Guest (no auth): 50 calls/day. Free member: 10,000 calls/day. Premium: higher.

## Freshness Assessment

Excellent. The TRA LiveBoard returned live data with accurate delay times (tested: trains showing 2-minute delays). Bus real-time data is GPS-sourced with high frequency. Taiwan's transit operators maintain tight integration with TDX — data quality is consistently high across all modes. Bilingual (Chinese/English) throughout, making it accessible to international developers.

## Entity Model

- **TRA LiveBoard**: StationID, StationName (Zh_tw/En), TrainNo, Direction, TrainType, ScheduledArrival/Departure, DelayTime, SrcUpdateTime
- **Bus RealTime**: PlateNumb, BusPosition (lat/lon), Speed, Direction, DutyStatus, BusStatus, RouteID, SubRouteID
- **Bus ETA**: StopID, StopName, RouteID, EstimateTime (seconds), StopStatus, SrcUpdateTime
- **Metro LiveBoard**: StationID, Destination, EstimateTime
- All entities include bilingual names and standardized national IDs

## Feasibility Rating

| Criterion       | Score | Notes                                                        |
|-----------------|-------|--------------------------------------------------------------|
| Freshness       | 3     | Excellent real-time across all modes; confirmed live          |
| Openness        | 2     | Basic access works without auth; higher tiers need free registration|
| Stability       | 3     | Government-backed (MOTC), versioned API, active development   |
| Structure       | 3     | OData query syntax, clean JSON, bilingual, consistent schema  |
| Identifiers     | 3     | National standardized IDs for stations, routes, operators     |
| Additive Value  | 2     | Proprietary REST — not coverable by GTFS-RT bridge; Asian transit coverage|
| **Total**       | **16/18** |                                                           |

## Notes

- TDX is the successor to the older PTX (Public Transport data eXchange) platform. The URL structure changed but the data model is largely compatible.
- The bilingual JSON output is a standout feature — every entity has `Zh_tw` and `En` name fields, making it immediately usable internationally.
- The OData query syntax is powerful and familiar to anyone who's used Microsoft's data APIs.
- Taiwan has GTFS static feeds for most operators (available through TDX), but the real-time data is primarily through the proprietary REST API — not GTFS-RT.
- The TRA (conventional rail) live board with per-station delay data is particularly valuable — it's essentially a national train tracking API.
- Bus real-time coverage is comprehensive — every major city's bus network is included with GPS positions and ETAs.
