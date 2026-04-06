# ODPT — Japan Open Data for Public Transportation

**Country/Region**: Japan (Tokyo Metropolitan Area + expanding)
**Publisher**: Association for Open Data of Public Transportation (ODPT / 公共交通オープンデータ協議会)
**API Endpoint**: `https://api.odpt.org/api/v4/`
**Documentation**: https://developer.odpt.org/ and https://ckan.odpt.org/
**Protocol**: REST/JSON-LD (Linked Data)
**Auth**: API key required (free registration — `acl:consumerKey` parameter)
**Data Format**: JSON-LD (schema.org / odpt vocabulary)
**Update Frequency**: Real-time — train locations update every ~30 s; departure boards near real-time
**License**: Public Transportation Open Data Basic License (operator-specific terms; mostly CC BY 4.0)

## What It Provides

Japan's ODPT is a pioneering effort to open up data from Tokyo's famously complex and punctual rail network. It covers:

- **Tokyo Metro**: real-time train locations on all 9 lines (Ginza, Marunouchi, Hibiya, Tozai, Chiyoda, Yurakucho, Hanzomon, Namboku, Fukutoshin)
- **Toei (Tokyo Metropolitan)**: subway (4 lines), bus, streetcar, Nippori-Toneri Liner
- **JR East**: limited real-time data for Greater Tokyo area
- **Odakyu, Keio, Tokyu, Seibu, Tobu**: private railway operators (varying coverage)
- **Bus operators**: Toei Bus, Odakyu Bus, and others
- **Airport access**: Keisei (Narita), Keikyu (Haneda)

Additionally, ODPT hosts 270+ GTFS datasets on ckan.odpt.org covering operators across Japan.

## API Details

The API uses JSON-LD (Linked Data) with the `odpt:` vocabulary:

- `GET /odpt:Train?odpt:operator=odpt.Operator:TokyoMetro` — real-time train positions
- `GET /odpt:TrainInformation?odpt:operator=odpt.Operator:TokyoMetro` — train status/delay info
- `GET /odpt:StationTimetable?odpt:station=odpt.Station:TokyoMetro.Ginza.Shibuya` — timetable at a station
- `GET /odpt:BusStop?odpt:operator=odpt.Operator:Toei` — bus stop data

All requests require `acl:consumerKey={key}` parameter. API returned 403 in testing (needs valid registered key — registration is open but may require a Japanese address for some operators).

JSON-LD entities use URIs as identifiers: `odpt.Station:TokyoMetro.Ginza.Shibuya`, `odpt.Railway:TokyoMetro.Ginza`, `odpt.Operator:TokyoMetro`.

## Freshness Assessment

Good for operators that participate. Tokyo Metro has excellent real-time train tracking — positions update every ~30 seconds with track section precision. Toei subway and bus data is also real-time. JR East participation is more limited. Private railways vary — some provide full real-time, others only timetable data. The system has been running since 2017 (originally the Tokyo Open Data Challenge) and has matured significantly.

## Entity Model

- **odpt:Train**: railway, trainNumber, trainType, fromStation, toStation, delay (seconds), carComposition, trainOwner
- **odpt:TrainInformation**: railway, trainInformationStatus (text), trainInformationCause, timeOfOrigin — delay/disruption reports
- **odpt:StationTimetable**: station, railway, departures with destinationStation, trainType, departureTime
- **odpt:BusTimetable**: busroute, departures with time, destinationSign
- All entities use Linked Data URIs (e.g., `odpt.Railway:TokyoMetro.Ginza`) — globally unique identifiers

## Feasibility Rating

| Criterion       | Score | Notes                                                        |
|-----------------|-------|--------------------------------------------------------------|
| Freshness       | 3     | Real-time train tracking for Tokyo Metro/Toei; variable for others|
| Openness        | 2     | Free registration; some operators restrict international access |
| Stability       | 2     | Running since 2017; individual operators can change participation|
| Structure       | 3     | JSON-LD with formal vocabulary — exceptional semantic structure|
| Identifiers     | 3     | Linked Data URIs — globally unique, semantically rich         |
| Additive Value  | 3     | Japan rail is iconic; JSON-LD is unique protocol territory    |
| **Total**       | **16/18** |                                                           |

## Notes

- This is one of the only transit APIs using JSON-LD (Linked Data) — the entity URIs and vocabulary (`odpt:Train`, `odpt:Railway`) make it architecturally distinctive. A JSON-LD–to–CloudEvents bridge would be a novel contribution.
- Japan's rail punctuality is legendary — when delays DO occur, the system reports them precisely (to the second).
- The CKAN portal (ckan.odpt.org) hosts 270+ GTFS datasets from operators across Japan — a treasure trove of static data even for operators without real-time APIs.
- ODPT previously ran as the "Tokyo Open Data Challenge" with time-limited API access. It has since transitioned to a permanent open data platform with ongoing registration.
- Car composition data (train consist information — how many cars, which types) is a distinctive feature rarely seen in Western transit APIs.
- The INDEX.md previously listed Japan as "not pursued" due to access concerns. The platform has matured since then and warrants reassessment.
