# aprs.fi AIS Data API

**Country/Region**: Global (Finland-based service, worldwide AIS coverage)
**Publisher**: aprs.fi (Hessu, OH7LZB — community project)
**API Endpoint**: `https://api.aprs.fi/api/get`
**Documentation**: https://aprs.fi/page/api
**Protocol**: REST
**Auth**: API Key (free account registration at aprs.fi)
**Data Format**: JSON, XML
**Update Frequency**: Near-real-time (seconds-level for tracked vessels)
**License**: Free for non-commercial use (must credit aprs.fi, link back required)

## What It Provides

aprs.fi is primarily known as an APRS (Automatic Packet Reporting System) tracking platform for
amateur radio, but it also ingests and serves AIS vessel tracking data. The same API that queries
APRS stations can query AIS targets by MMSI or callsign, returning position, course, speed,
heading, and vessel metadata.

AIS-specific data fields include:
- Position (lat/lng), course, speed, heading
- MMSI, IMO, vessel class
- Navigational status
- Vessel dimensions (length, width, draught)
- Reference point distances (front, left)

## API Details

Query format:
```
GET https://api.aprs.fi/api/get?name=MMSI_OR_CALLSIGN&what=loc&apikey=APIKEY&format=json
```

Parameters:
| Param | Description |
|---|---|
| `name` | Station/vessel name, MMSI, or callsign (up to 20 comma-separated) |
| `what` | `loc` for location data |
| `apikey` | Your API key from account settings |
| `format` | `json` or `xml` |

Response example (AIS target):
```json
{
  "command": "get",
  "result": "ok",
  "what": "loc",
  "found": 1,
  "entries": [
    {
      "class": "i",
      "name": "244234000",
      "type": "a",
      "time": "1267445689",
      "lasttime": "1270580127",
      "lat": "52.46015",
      "lng": "5.03812",
      "course": "48.7",
      "speed": "0",
      "mmsi": "244234000",
      "imo": "9361354",
      "vesselclass": "A",
      "navstat": "5",
      "heading": "49",
      "length": "302",
      "width": "32",
      "draught": "7.2"
    }
  ]
}
```

Key AIS-specific response fields:
- `class`: "i" = AIS, "a" = APRS
- `type`: "a" = AIS target
- `mmsi`, `imo`, `vesselclass`, `navstat`, `heading`, `length`, `width`, `draught`
- `ref_front`, `ref_left` (reference point distances)

Batch queries: up to 20 targets per request.

Rate limiting: per-API-key, adjustable on request. Designed for lookup-by-name, not bulk data dumps.

## Freshness Assessment

Good for individual vessel lookups. aprs.fi receives AIS data from community-contributed
receivers and internet-connected feeds. Data for actively tracked vessels is typically
seconds to minutes old. However, this is NOT a bulk data API — you must know the vessel
identifier beforehand. There is no "all vessels in area" endpoint.

## Entity Model

Per-target record with mixed APRS/AIS fields:
- `name` (MMSI or callsign), `mmsi`, `imo`
- `lat`, `lng`, `course`, `speed`, `altitude`
- `heading`, `navstat`, `vesselclass`
- `length`, `width`, `draught`
- `ref_front`, `ref_left`
- `time` (first seen at position), `lasttime` (last seen at position)
- `comment` (may contain AIS destination/ETA)

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 2 | Real-time for tracked vessels, but not a bulk/area feed |
| Openness | 2 | Free API key, but non-commercial use only, must credit |
| Stability | 2 | Long-running community project (~15 years), no SLA |
| Structure | 2 | Clean JSON, but no OpenAPI spec, mixed APRS/AIS schema |
| Identifiers | 3 | MMSI, IMO, callsign, vessel class all present |
| Additive Value | 1 | Lookup-only (no area/streaming), covered better by other sources |

**Total: 12/18**

## Notes

- aprs.fi is a niche but interesting source: it bridges the amateur radio and maritime worlds.
- The API is strictly lookup-by-identifier — you cannot discover vessels in an area. This makes
  it useful for enrichment (look up details for a known MMSI) but not for area monitoring.
- The community nature means coverage varies wildly by region. Strong in Scandinavia and Europe,
  weaker elsewhere.
- The non-commercial license and credit requirement are important constraints for any integration.
- Best suited as a secondary enrichment source rather than a primary AIS feed.
