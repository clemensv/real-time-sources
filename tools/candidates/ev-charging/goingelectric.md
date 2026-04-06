# GoingElectric Stromtankstellen API

**Country/Region**: Europe (focus on Germany/DACH, but covers all of Europe)
**Publisher**: GoingElectric community / Fastercom GmbH
**API Endpoint**: `https://api.goingelectric.de/chargepoints/`
**Documentation**: https://www.goingelectric.de/stromtankstellen/api/ (registration required)
**Protocol**: REST
**Auth**: API Key (free registration required)
**Data Format**: JSON
**Real-Time Status**: Partial — community-reported status updates, not real-time connector telemetry
**Update Frequency**: Community-contributed updates (continuous but crowdsourced)
**Station Count**: ~70,000+ charging locations across Europe
**License**: Free for non-commercial use; commercial use requires agreement

## What It Provides

GoingElectric is Germany's largest EV community platform, akin to PlugShare for the DACH region. Its Stromtankstellen (charging station) API provides programmatic access to the community's charging station database, which covers most of Europe with particular depth in Germany, Austria, and Switzerland. The data includes station locations, connector types, power levels, operator information, and community-contributed status reports and photos.

## API Details

**Chargepoints endpoint (requires API key):**
```
GET https://api.goingelectric.de/chargepoints/?key={api_key}&sw_lat=52.0&sw_lng=13.0&ne_lat=52.5&ne_lng=13.5
```

The API was confirmed running (`{"status":"OK","message":"ChargePoint API is running"}`) but returns 401 without a valid API key.

Key parameters (based on community documentation):
- Geographic bounding box: `sw_lat`, `sw_lng`, `ne_lat`, `ne_lng`
- Connector type filters
- Power level filters
- Network/operator filters
- Clustering support for map applications

Response typically includes:
- Station ID, name, address, coordinates
- Connector types and power levels
- Operator/network information
- Community ratings and status reports
- Photo URLs
- Opening hours

## Freshness Assessment

GoingElectric data is community-maintained — users report new stations, verify existing ones, and submit status updates. The data quality is very high for Germany (where the community is most active) and good across Western Europe. However, "status" here means community-verified operational state, not real-time connector occupancy. A station might be marked as "working" by a user who charged there yesterday, but you won't know if a specific plug is currently available.

Think of it as a very detailed, well-maintained registry with crowd-verified freshness, not a real-time telemetry feed.

## Entity Model

- **Chargepoint**: A charging location with address, coordinates, operator
- **Connector**: Plug type, power (kW), count
- **Operator**: Charging network name
- **Status**: Community-reported (verified/unverified/defect/planned)
- **Comments**: User-submitted reports, tips, photos

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Community-verified, not real-time; no connector-level status |
| Openness | 2 | Free API key for non-commercial use; commercial requires agreement |
| Stability | 2 | Community-run platform; API has been available for years but no SLA |
| Structure | 2 | JSON API; proprietary schema (not OCPI/OICP) |
| Identifiers | 2 | Platform-specific IDs; some cross-references to operator IDs |
| Additive Value | 2 | Strong DACH coverage; community verification adds quality layer |
| **Total** | **11/18** | |

## Notes

- GoingElectric is the PlugShare of the German-speaking world. If you want to know about a charging station in Germany, GoingElectric usually has the most detailed community reports.
- The API is primarily designed for app developers building EV navigation tools.
- API key registration is at https://www.goingelectric.de/stromtankstellen/api/ — requires a GoingElectric account.
- The data overlaps significantly with Open Charge Map, which aggregates from GoingElectric among other sources.
- For a bridge focused on real-time data, GoingElectric is lower priority — it's a rich registry but lacks real-time connector telemetry. The Bundesnetzagentur register or NDL Netherlands offer better structured government data.
- GoingElectric was acquired by ADAC (Germany's largest automobile club) in 2021, which should provide long-term stability.
