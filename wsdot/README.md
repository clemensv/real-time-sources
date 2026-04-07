# WSDOT Traveler Information

This source bridges the Washington State Department of Transportation (WSDOT)
Traveler Information API and Washington State Ferries API to Apache Kafka,
producing real-time data across eight event families: traffic flow, travel
times, mountain pass conditions, road weather, toll rates, commercial vehicle
restrictions, US-Canada border crossing wait times, and ferry vessel
locations.

## Upstream Sources

### Traveler Information API

The WSDOT Traveler Information API provides data for Washington State
highways organized into four geographic regions:

- **Northwest** — I-5, I-90, SR 520, I-405, and surrounding highways in the Puget Sound area
- **Olympic** — I-5, SR 16, SR 167 in the Olympic Peninsula and south Puget Sound
- **Southwest** — I-5 and I-205 near the Oregon border and southwest Washington
- **Eastern** — I-90 and US 395 in eastern Washington

### Washington State Ferries API

The WSF Vessel Locations API reports real-time GPS positions for
approximately 21 ferry vessels operating across Puget Sound.

## API Access

Both APIs require a free access code. Register at:
https://www.wsdot.wa.gov/traffic/api/

## Data Model

| Message Group | Event Types | Key | Description |
|---------------|-------------|-----|-------------|
| `us.wa.wsdot.traffic` | TrafficFlowStation (ref), TrafficFlowReading (tel) | `{flow_data_id}` | ~1,400 inductive loop sensors reporting Level of Service |
| `us.wa.wsdot.traveltimes` | TravelTimeRoute | `{travel_time_id}` | ~163 monitored route segments with average and current travel times |
| `us.wa.wsdot.mountainpass` | MountainPassCondition | `{mountain_pass_id}` | 16 mountain passes with temperature, weather, road conditions, restrictions |
| `us.wa.wsdot.weather` | WeatherStation (ref), WeatherReading (tel) | `{station_id}` | ~134 RWIS stations with temperature, wind, pressure, humidity, visibility |
| `us.wa.wsdot.tolls` | TollRate | `{trip_name}` | ~84 dynamic toll segments on SR 99, I-405, SR 167 |
| `us.wa.wsdot.cvrestrictions` | CommercialVehicleRestriction | `{state_route_id}/{bridge_number}` | ~354 bridge/road weight, height, length, width restrictions |
| `us.wa.wsdot.border` | BorderCrossing | `{crossing_name}` | 11 US-Canada border crossing lanes with wait times |
| `us.wa.wsdot.ferries` | VesselLocation | `{vessel_id}` | ~21 WSF vessels with GPS, speed, heading, route, terminal, ETA |

Reference data is emitted at startup and refreshed every 6 hours. Telemetry
is polled every 120 seconds (configurable).

## Links

- API Documentation: https://www.wsdot.wa.gov/traffic/api/
- Ferries API: https://www.wsdot.wa.gov/ferries/api/vessels/rest/
- Event catalog: [EVENTS.md](EVENTS.md)
- Container deployment: [CONTAINER.md](CONTAINER.md)
