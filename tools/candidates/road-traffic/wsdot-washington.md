# WSDOT Traveler Information API

**Country/Region**: US — Washington State
**Publisher**: Washington State Department of Transportation (WSDOT)
**API Endpoint**: `https://wsdot.wa.gov/traffic/api/`
**Documentation**: https://wsdot.wa.gov/traffic/api/
**Protocol**: REST + SOAP + RSS + KML
**Auth**: Access code required (free email registration)
**Data Format**: JSON, XML, RSS, KML
**Update Frequency**: Real-time / near-real-time
**License**: Washington State travel information terms and disclaimer

## What It Provides

WSDOT's Traveler Information API is the official statewide gateway for Washington transportation operations data. It covers a remarkably broad set of feeds through one platform:

- **Highway alerts** — incidents, closures, construction
- **Highway cameras** — statewide camera metadata and still images
- **Mountain pass conditions** — weather, chains, restrictions, closures
- **Traffic flow** — roadway sensor data
- **Travel times** — corridor travel-time estimates
- **Weather information / stations** — road-weather and station conditions
- **Border crossings** — wait times at the Canadian border
- **Washington State Ferries** — fares, schedules, terminals, vessels

That combination makes this one of the strongest state DOT candidates in the US. It is both a road-traffic source and a ferry/maritime-adjacent source for Puget Sound.

## API Details

The landing page exposes separate documented services for:

- `HighwayAlerts/HighwayAlertsREST.svc/Help`
- `HighwayCameras/HighwayCamerasREST.svc/Help`
- `MountainPassConditions/MountainPassConditionsREST.svc/Help`
- `TrafficFlow/TrafficFlowREST.svc/Help`
- `TravelTimes/TravelTimesREST.svc/Help`
- `WeatherInformation/WeatherInformationREST.svc/Help`
- `WeatherStations/WeatherStationsREST.svc/Help`
- `BorderCrossings/BorderCrossingsREST.svc/Help`
- Washington State Ferries sub-APIs for **fares**, **schedule**, **terminals**, and **vessels**

The ferry schedule API documentation explicitly states that a valid access code is required and that both REST and SOAP access are supported. The WSDOT traveler API page presents the full catalog in one place, which is exactly what you want from a government operations platform.

## Freshness Assessment

Strong. Traffic alerts, pass conditions, weather, and ferry information are operational traveler-information products, not periodic statistical releases. The feeds are intended for third-party travel apps and statewide traveler information systems, which makes them a good fit for polling bridges with low latency.

## Entity Model

- **Highway alert** — incident/work zone/closure with identifier, description, roadway reference, lifecycle
- **Camera** — camera ID, location, image URL, metadata
- **Mountain pass condition** — pass name, restrictions, weather, chain requirements
- **Traffic flow / travel time** — corridor or sensor point with current observed state
- **Weather station** — station ID, location, atmospheric/road measurements
- **Border crossing** — crossing ID/name, wait times, direction
- **Ferry vessel / terminal / sailing** — vessel IDs, terminal IDs, departures, adjustments

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Operational real-time traveler information |
| Openness | 2 | Free access code required |
| Stability | 3 | Official statewide DOT platform with long-lived docs |
| Structure | 3 | Multiple documented machine-readable interfaces |
| Identifiers | 3 | Strong entity IDs across cameras, passes, vessels, terminals, crossings |
| Additive Value | 3 | Unique Washington coverage; road + ferry + weather under one roof |
| **Total** | **17/18** | |

## Notes

- The ferry coverage is the standout for Puget Sound. Most state DOT APIs do not also expose a major ferry system through the same platform.
- This could be implemented either as one broad multi-family source or as a narrower first source focused on **ferries**, **mountain passes**, or **highway alerts**.
- The WSDOT API is also a good proving ground for a reusable US state DOT pattern alongside Bay Area 511 and other US traveler-information systems.
- Because access is key-gated, the runtime would need clear guidance for self-service credential acquisition, but the barrier is low.
