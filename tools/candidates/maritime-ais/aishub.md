# AISHub

**Country/Region**: Global (community-operated, servers in multiple countries)
**Publisher**: AISHub.net (community data-sharing cooperative)
**API Endpoint**: `https://data.aishub.net/ws.php`
**Documentation**: https://aishub.net/api
**Protocol**: REST
**Auth**: Membership (must contribute your own AIS feed to receive aggregated data)
**Data Format**: JSON, XML, CSV
**Update Frequency**: Near-real-time (polled, max 1 request/minute)
**License**: Community sharing agreement (must contribute to access)

## What It Provides

AISHub is a cooperative AIS data-sharing network. Members who operate AIS receiving stations
share their raw AIS feeds with AISHub, and in return get access to the aggregated data from all
860+ contributing stations worldwide. The API exposes this aggregated data as a REST service.

Data includes:
- Vessel position (lat/lon, COG, SOG, heading, ROT, navigational status)
- Vessel identity (MMSI, IMO, name, callsign, ship type)
- Voyage data (destination, ETA, draught)
- Vessel dimensions (A, B, C, D reference points)

## API Details

Single endpoint with query parameters:

```
https://data.aishub.net/ws.php?username=USERNAME&format=1&output=json&compress=0
  &latmin=E&latmax=F&lonmin=G&lonmax=H&mmsi=I&imo=J&interval=K
```

Parameters:
| Param | Description |
|---|---|
| `username` | AISHub username (received after joining) |
| `format` | 0 = AIS encoding, 1 = human-readable |
| `output` | `xml`, `json`, or `csv` |
| `compress` | 0=none, 1=ZIP, 2=GZIP, 3=BZIP2 |
| `latmin/latmax/lonmin/lonmax` | Bounding box filter |
| `mmsi` | Filter by MMSI (comma-separated list) |
| `imo` | Filter by IMO number |
| `interval` | Maximum age of positions in minutes |

Response (JSON, human-readable format):
```json
[
  {"ERROR":false,"USERNAME":"...","FORMAT":"HUMAN","RECORDS":5},
  [
    {
      "MMSI":311733000,
      "TIME":"2021-07-09 12:08:05 GMT",
      "LONGITUDE":-63.04667,
      "LATITUDE":18.01317,
      "COG":48.7,"SOG":0,"HEADING":49,
      "ROT":0,"NAVSTAT":5,
      "IMO":9111802,"NAME":"ENCHANTMENT OTS",
      "CALLSIGN":"C6FZ7","TYPE":60,
      "A":49,"B":253,"C":17,"D":15,
      "DRAUGHT":7.2,"DEST":"PHILIPSBURG",
      "ETA":"07-04 13:00"
    }
  ]
]
```

A separate stations API lists all contributing stations:
```
https://data.aishub.net/stations.php?username=USERNAME&output=json
```

Rate limit: maximum 1 request per minute.

## Freshness Assessment

Good, but constrained. Data freshness depends on the contributing stations and their coverage.
In well-covered areas (Northern Europe, US East Coast, Mediterranean), data is near-real-time.
In remote areas, coverage is sparse. The 1-request-per-minute rate limit makes this a polling
source, not a streaming one — suitable for periodic snapshots rather than continuous tracking.

## Entity Model

Flat record per vessel with fields:
- `MMSI`, `IMO`, `NAME`, `CALLSIGN`, `TYPE` (AIS ship type code)
- `LATITUDE`, `LONGITUDE`, `COG`, `SOG`, `HEADING`, `ROT`, `NAVSTAT`
- `A`, `B`, `C`, `D` (dimension reference points in meters)
- `DRAUGHT`, `DEST`, `ETA`
- `TIME` (timestamp of position report)

Identifiers: MMSI (primary), IMO, callsign.

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 2 | Near-real-time in covered areas, 1 req/min limit |
| Openness | 1 | Requires contributing your own AIS feed — not truly open |
| Stability | 2 | Long-running community project, but no SLA |
| Structure | 2 | Simple flat JSON, but no OpenAPI spec, no GeoJSON |
| Identifiers | 3 | MMSI, IMO, callsign, vessel name all included |
| Additive Value | 3 | Global coverage from 860+ community stations |

**Total: 13/18**

## Notes

- The quid-pro-quo model (share your feed to get access) makes this unsuitable for consumers
  who don't operate their own AIS receiver. But for organizations that do, it's a valuable
  global data source.
- Coverage is heavily biased toward coastal areas with enthusiast communities (Europe, North America,
  parts of Asia). Open ocean coverage is minimal (terrestrial AIS only, no satellite).
- The simple REST/JSON interface is easy to integrate but lacks modern API niceties like
  streaming, webhooks, or OpenAPI documentation.
- Useful as a supplementary global data source alongside regional government feeds.
