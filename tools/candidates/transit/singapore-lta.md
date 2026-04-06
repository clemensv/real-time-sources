# Singapore LTA DataMall

**Country/Region**: Singapore
**Publisher**: Land Transport Authority (LTA)
**API Endpoint**: `https://datamall2.mytransport.sg/ltaodataservice/`
**Documentation**: https://datamall.lta.gov.sg/content/datamall/en/dynamic-data.html
**Protocol**: REST/JSON (OData-style)
**Auth**: API key required (free registration via MyTransport DataMall)
**Data Format**: JSON
**Update Frequency**: Real-time — bus arrivals update every ~60 s; train disruptions near real-time
**License**: Singapore Open Data License (Terms of Use on DataMall)

## What It Provides

Singapore's LTA DataMall is a comprehensive transport data API covering the island city-state's efficient, well-integrated transit network:

- **Bus Arrivals**: real-time ETAs at any bus stop — estimated arrival times for next 3 buses per service, with load information (Seats Available / Standing Available / Limited Standing)
- **Bus Positions**: real-time GPS positions of all public buses
- **Train Service Alerts**: MRT/LRT line status and disruption notifications (5 MRT lines + 3 LRT lines)
- **Traffic Incidents**: real-time road incidents
- **Taxi Availability**: real-time positions of available taxis
- **Bicycle Parking**: availability at stations
- **Passenger Volume**: historical ridership data by station/stop

## API Details

All endpoints require the `AccountKey` header with a registered API key.

- `GET /BusArrivalv2?BusStopCode={code}` — real-time bus arrivals at a stop
- `GET /BusPositions` — all bus GPS positions
- `GET /TrainServiceAlerts` — MRT/LRT line status
- `GET /v1/TaxiAvailability` — real-time taxi locations
- `GET /BusRoutes` — all bus routes with stop sequences
- `GET /BusStops` — all bus stop locations

OData-compatible: `?$skip=500` for pagination. Responses return `odata.metadata` URI.

Rate limits: not strictly published but DataMall is designed for reasonable use. The platform serves Singapore's developer community and numerous production apps.

## Freshness Assessment

Good. Bus arrival predictions are the core real-time data — they use AVL (Automatic Vehicle Location) systems deployed across Singapore's entire bus fleet. The `EstimatedArrival` field provides ISO 8601 timestamps for the next 1–3 buses, plus `Load` (crowding level) and `Type` (single/double-deck/bendy). Train alerts are event-driven — published when disruptions occur. Data is refreshed roughly every 60 seconds.

## Entity Model

- **BusArrival**: ServiceNo, Operator, NextBus/NextBus2/NextBus3 (each: EstimatedArrival, Load, Feature, Type, OriginCode, DestinationCode, Latitude, Longitude, VisitNumber)
- **BusPosition**: VehiclePlate, Latitude, Longitude (simple but comprehensive)
- **TrainServiceAlert**: Status (1=Normal, 2=Disrupted), AffectedLine, Direction, Stations, FreePublicBus, FreeShuttleBus, MRTShuttleDirection
- **BusStop**: BusStopCode, RoadName, Description, Latitude, Longitude
- All entities use LTA's internal codes; BusStopCode is a 5-digit national standard

## Feasibility Rating

| Criterion       | Score | Notes                                                        |
|-----------------|-------|--------------------------------------------------------------|
| Freshness       | 3     | Real-time bus arrivals with crowding data; train alerts live  |
| Openness        | 2     | Free API key required — straightforward registration          |
| Stability       | 3     | Government-backed (LTA), long-running, powers major apps      |
| Structure       | 2     | Clean JSON with OData metadata; proprietary schema            |
| Identifiers     | 2     | LTA-specific codes (BusStopCode, ServiceNo); no GTFS alignment|
| Additive Value  | 2     | Crowding/load data is unique; covers a major Asian city-state |
| **Total**       | **14/18** |                                                           |

## Notes

- Singapore's real-time bus load/crowding information (Seats Available → Standing Available → Limited Standing) is a standout feature. Very few transit APIs provide real-time occupancy data at the per-vehicle level.
- Singapore is small but exceptionally well-instrumented — every bus has AVL, the entire MRT network is monitored, even taxis report positions.
- LTA also provides historical ridership data by time of day — useful for analytics, though not real-time.
- The MRT network (Thomson-East Coast, Downtown, Circle, North-South, East-West lines plus LRT) is all covered by the service alerts endpoint.
- DataMall also includes non-transit transport data: traffic speeds, ERP rates, carpark availability, cycling paths.
