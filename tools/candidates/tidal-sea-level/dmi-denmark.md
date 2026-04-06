# DMI — Denmark Ocean Observations (Sea Level and Tides)

**Country/Region**: Denmark (including Greenland coastal stations)
**Publisher**: Danish Meteorological Institute (DMI) + Kystdirektoratet (Danish Coastal Authority)
**API Endpoint**: `https://dmigw.govcloud.dk/v2/oceanObs/collections/observation/items`
**Documentation**: https://opendatadocs.dmi.govcloud.dk/en/DMIOpenData
**Protocol**: OGC API Features (REST/GeoJSON)
**Auth**: Free API key required (self-service registration)
**Data Format**: GeoJSON
**Update Frequency**: Real-time (10-minute intervals for primary tide gauges)
**License**: Danish open data (Creative Commons compatible)

## What It Provides

DMI's ocean observation API delivers real-time sea level data from Denmark's network of tide gauges. Both DMI and Kystdirektoratet contribute stations, sharing the mandate for sea level monitoring. The API follows OGC API Features standard.

Collections available:
- **observation**: real-time sea level observations (sea_reg, sealev_dvr, sealev_ln, tw/water temperature)
- **station**: metadata for all tide gauge stations
- **tidewater**: tidal predictions
- **tidewaterstation**: tidal prediction station metadata

Coverage spans the Danish coast from the North Sea (Skagerrak/Kattegat) through the Danish straits to the Baltic Sea, including stations in Greenland.

## API Details

Standard OGC API Features pattern:

```
# List stations
GET https://dmigw.govcloud.dk/v2/oceanObs/collections/station/items?api-key={KEY}

# Get observations for a station
GET https://dmigw.govcloud.dk/v2/oceanObs/collections/observation/items
  ?api-key={KEY}
  &stationId=20002
  &datetime=2025-01-01T00:00:00Z/2025-01-02T00:00:00Z
  &parameterId=sealev_dvr

# Tidal predictions
GET https://dmigw.govcloud.dk/v2/oceanObs/collections/tidewater/items
  ?api-key={KEY}
  &stationId=20002
```

Parameters:
- `sea_reg`: sea level registered (raw)
- `sealev_dvr`: sea level in DVR90 datum (Danish Vertical Reference 1990)
- `sealev_ln`: sea level, local zero
- `tw`: water temperature

Verified working: station list returns GeoJSON FeatureCollection with full metadata including coordinates, owner, parameterId arrays, and operational dates.

## Freshness Assessment

Excellent. Real-time 10-minute observations from primary tide gauges. Historical data goes back to 1953 for some parameters and stations. Both DMI and Kystdirektoratet data accessible through the same API.

## Entity Model

- **Station**: stationId, name, type (Tide-gauge-primary/secondary), coordinates, owner (DMI/Kystdirektoratet), operationFrom/To, parameterId list
- **Observation**: stationId, timestamp, parameterId, value, quality
- **Tidewater Prediction**: stationId, timestamp, predicted level

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time 10-min intervals; historical back to 1953 |
| Openness | 2 | Free but requires API key registration |
| Stability | 3 | National met service, legally mandated |
| Structure | 3 | OGC API Features standard; clean GeoJSON; well-documented |
| Identifiers | 3 | Station IDs, WMO codes, parameter IDs — all standardized |
| Additive Value | 2 | Danish straits are critical shipping bottleneck; Baltic entrance monitoring |
| **Total** | **16/18** | |

## Notes

- The OGC API Features compliance makes this one of the best-structured tide APIs in Europe.
- Danish straits (Øresund, Store Bælt, Lille Bælt) are major international shipping routes — sea level data here is strategically important.
- DMI also provides meteorological observations through a parallel `metObs` API with the same architecture.
- Greenland stations provide Arctic coastal monitoring — rare and valuable.
- API key is free and instant — no barrier beyond a simple registration.
