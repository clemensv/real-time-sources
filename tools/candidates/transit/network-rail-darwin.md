# Network Rail DARWIN (GB Rail Real-Time)

**Country/Region**: United Kingdom (Great Britain)
**Publisher**: National Rail / Rail Delivery Group (RDG)
**API Endpoint**: Available via Rail Data Marketplace (https://raildata.org.uk/)
**Documentation**: https://www.nationalrail.co.uk/developers/darwin-data-feeds/
**Protocol**: STOMP (push), SOAP (pull), REST (HSP)
**Auth**: Registration on Rail Data Marketplace (free for open data feeds)
**Data Format**: XML (Push Port), SOAP XML, JSON (HSP)
**Update Frequency**: Real-time push — sub-second latency via STOMP/ActiveMQ
**License**: Open by default (via Rail Data Marketplace); attribution required

## What It Provides

Darwin is the GB rail industry's official train running information engine. It is the only system that takes feeds directly from every Train Operating Company's (TOC) Customer Information System, combined with train location data from Network Rail infrastructure. Darwin provides:

- **Real-time predictions** — arrival/departure times at every station for every train
- **Platform numbers** — including last-minute platform changes
- **Delay estimates** — predicted delay in minutes
- **Cancellations** — full and partial cancellations with reason codes
- **Schedule changes** — diversions, additional stops, removed stops
- **Historic Service Performance (HSP)** — up to 1 year of historical on-time data

Darwin powers departure boards at every station in GB, the National Rail website, Trainline, Google Maps, and hundreds of third-party apps.

## API Details

Three main access methods:

### 1. Push Port (STOMP)
- Real-time push feed via Apache ActiveMQ (STOMP protocol)
- XML messages pushed as trains progress through the network
- Message types: Schedule updates, Train Status, Station Messages, Deactivated trains
- Lowest latency — messages arrive within seconds of events

### 2. Staff/Public SOAP Web Service (OpenLDBWS)
- `https://lite.realtime.nationalrail.co.uk/OpenLDBWS/`
- SOAP API for departure boards: `GetDepartureBoard`, `GetArrivalBoard`, `GetServiceDetails`
- Returns next trains at a station with predicted times, platforms, delay reasons
- Staff version (OpenLDBSVWS) includes additional detail

### 3. Historic Service Performance (HSP)
- REST API returning JSON
- Query historical performance metrics by service, route, station, date range

### Data Model (Push Port)
XML elements include:
- `<schedule>` — planned schedule with calling points
- `<TS>` (Train Status) — real-time updates: `<Location>` elements with `<arr>`, `<dep>`, `<pass>` times (predicted vs. working)
- `<OW>` (Station Messages) — disruption messages per station
- CRS codes (3-letter station codes), TIPLOC codes for timing points, headcodes for train IDs

## Freshness Assessment

Excellent. The Push Port provides sub-second real-time updates — among the freshest transit data feeds globally. The SOAP web service adds ~5 seconds latency. Darwin is the authoritative single source of truth for GB rail operations.

## Entity Model

- **Schedule**: a train service's planned calling pattern for a given day (RTTI ID)
- **TrainStatus** (`<TS>`): real-time position/prediction update for a service
- **Location**: a calling point within a service (CRS/TIPLOC code, platform, times)
- **StationMessage**: disruption/information text for a station or area
- Trains identified by RTTI UID + service date; stations by CRS (3-letter) or TIPLOC codes

## Feasibility Rating

| Criterion       | Score | Notes                                                        |
|-----------------|-------|--------------------------------------------------------------|
| Freshness       | 3     | Push-based, sub-second latency — best-in-class               |
| Openness        | 2     | Free registration but via marketplace; some feeds have terms  |
| Stability       | 3     | Industry-standard, powers all GB rail information             |
| Structure       | 2     | Custom XML schema (well-documented but proprietary)           |
| Identifiers     | 3     | CRS codes, TIPLOCs, headcodes — well-established UK rail IDs  |
| Additive Value  | 3     | Push-based STOMP protocol — unique architecture pattern       |
| **Total**       | **16/18** |                                                           |

## Notes

- The Push Port (STOMP/ActiveMQ) is architecturally distinctive — a genuine push feed, unlike most transit APIs which are poll-based. This makes it an excellent candidate for event-driven bridge design.
- The Rail Data Marketplace (raildata.org.uk) is the new centralized portal replacing the old NRE data feeds registration.
- Darwin Knowledgebase provides reference/static data (station facilities, TOC info, service patterns) — needed to resolve the real-time stream.
- The SOAP web service (OpenLDBWS) is simpler to consume but less efficient for bulk monitoring — better suited for per-station queries.
- Good community support via the Open Rail Data-Talk Google Group.
- Complementary to BODS (buses) — together they cover all of UK public transport.
