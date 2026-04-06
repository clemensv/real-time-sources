# Santander Cycles London

**Country/Region**: United Kingdom — London
**Publisher**: Transport for London (TfL)
**API Endpoint**: `https://tfl.gov.uk/tfl/syndication/feeds/cycle-hire/livecyclehireupdates.xml` (XML) and `https://api.tfl.gov.uk/BikePoint` (REST/JSON)
**Documentation**: https://api.tfl.gov.uk/ and https://tfl.gov.uk/info-for/open-data-users/
**Protocol**: REST (TfL Unified API) + legacy XML feed
**Auth**: Optional API key (for rate limiting; works without)
**Data Format**: JSON (TfL API) / XML (legacy feed)
**Update Frequency**: ~3 minutes (XML feed), near real-time (TfL API)
**License**: Open Government Licence v3.0 / TfL Open Data

## What It Provides

Real-time station-level bike availability for London's public bikeshare system (branded "Santander Cycles", formerly "Boris Bikes"). Covers ~800 docking stations across central and inner London with approximately 14,000 bikes including standard bikes and e-bikes.

## API Details

**TfL Unified API (JSON):**
```
GET https://api.tfl.gov.uk/BikePoint
```
Returns an array of all BikePoint places. Each includes:
- `id`: e.g. `BikePoints_1`
- `commonName`: station name
- `lat`, `lon`: coordinates
- `additionalProperties`: key-value pairs including `NbBikes`, `NbEBikes`, `NbEmptyDocks`, `NbDocks`, `Installed`, `Locked`, `TerminalName`

**Legacy XML feed:**
```xml
<station>
  <id>1</id>
  <name>River Street, Clerkenwell</name>
  <lat>51.52916347</lat>
  <long>-0.109970527</long>
  <nbBikes>6</nbBikes>
  <nbStandardBikes>6</nbStandardBikes>
  <nbEBikes>0</nbEBikes>
  <nbEmptyDocks>12</nbEmptyDocks>
  <nbDocks>19</nbDocks>
  <installed>true</installed>
  <locked>false</locked>
</station>
```

Both endpoints provide the same data. The XML feed updates every ~3 minutes; the JSON API is near real-time.

## Freshness Assessment

The TfL BikePoint API returns `modified` timestamps on each property — typical lag is under 5 minutes. The XML feed's `lastUpdate` epoch is refreshed every ~3 minutes. For a dock-based bikeshare system, this is entirely adequate — station availability doesn't change faster than this.

## Entity Model

- **BikePoint/Station**: ~800 stations with numeric IDs, terminal names, coordinates
- **Availability**: Standard bikes, e-bikes, empty docks, total docks
- **Status**: Installed (boolean), Locked (boolean), Temporary (boolean)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Near real-time via TfL API; 3-min via XML |
| Openness | 3 | No mandatory auth; OGL v3.0 license |
| Stability | 3 | TfL Unified API is mature, well-documented, widely used |
| Structure | 3 | Clean JSON with consistent schema; XML also well-structured |
| Identifiers | 3 | Stable BikePoint IDs and terminal names |
| Additive Value | 2 | London is not in the GBFS catalog (uses TfL proprietary format), so it adds coverage beyond GBFS |
| **Total** | **17/18** | |

## Notes

- Santander Cycles does not publish a GBFS feed. TfL has its own API format. A dedicated bridge is needed to ingest London bike data — the generic GBFS bridge won't cover it.
- The TfL API also provides cycle superhighway disruptions, which could be a bonus data stream.
- Rate limits: 500 req/min with API key, 50 req/min without. Registering for a key is free and instant.
- The XML feed is simpler to parse but the JSON API provides richer metadata.
