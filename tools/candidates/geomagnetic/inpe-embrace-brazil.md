# INPE EMBRACE — Brazilian Space Weather Program

**Country/Region**: Brazil (national; South Atlantic Anomaly coverage)
**Publisher**: INPE — Instituto Nacional de Pesquisas Espaciais (EMBRACE program)
**API Endpoint**: `https://embrace.inpe.br/` (connection failed)
**Documentation**: http://www2.inpe.br/climaespacial/portal/
**Protocol**: Unknown
**Auth**: Unknown
**Data Format**: Unknown
**Update Frequency**: Real-time (space weather monitoring)
**License**: Brazilian government

## What It Provides

INPE's EMBRACE (Estudo e Monitoramento Brasileiro do Clima Espacial) program is uniquely positioned for space weather monitoring because of the **South Atlantic Anomaly (SAA)** — a region where the Earth's inner Van Allen radiation belt comes closest to the surface, centered over Brazil and the South Atlantic.

Monitoring includes:
- **Geomagnetic indices**: Kp equivalent for South American observatories
- **Ionospheric TEC** (Total Electron Content): Critical for GPS accuracy; the equatorial ionosphere over Brazil is among the most disturbed on Earth
- **Scintillation monitoring**: Ionospheric irregularities that cause GPS signal loss — severe over Brazil due to equatorial plasma bubbles
- **Solar activity**: Flare monitoring, CME tracking
- **Magnetometers**: EMBRACE Magnetometer Network across Brazil

### Why Brazil Matters for Space Weather

The South Atlantic Anomaly means:
- Satellites in Low Earth Orbit experience their highest radiation doses over Brazil
- GPS accuracy is worst over equatorial South America (ionospheric scintillation)
- The Brazilian sector is where equatorial plasma bubbles form most frequently
- EMBRACE data complements NOAA SWPC (US-centric) with Southern Hemisphere perspective

## API Details

```
https://embrace.inpe.br/kindex.php → Connection failed
https://embrace.inpe.br/api/v2/kindex → Connection failed
http://www2.inpe.br/climaespacial/portal/kindex-api/ → Connection failed
http://www2.inpe.br/climaespacial/portal/tec-map-api/ → Connection failed
```

All endpoints were unreachable during testing. INPE's space weather services may be on internal networks or experiencing downtime.

## Integration Notes

- Ionospheric TEC maps from EMBRACE are critical for aviation and precision agriculture (GPS-dependent)
- The equatorial ionosphere over Brazil is the most disturbed on Earth — making this uniquely valuable data
- South Atlantic Anomaly monitoring is relevant for satellite operators
- Existing geomagnetic candidates (NOAA SWPC, INTERMAGNET) provide global context but not Southern Hemisphere detail
- EMBRACE data would complement existing space-orbital and geomagnetic candidates

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Real-time monitoring program; endpoints unreachable |
| Openness | 0 | All endpoints failed |
| Stability | 1 | INPE program; infrastructure issues |
| Structure | 0 | Cannot assess |
| Identifiers | 0 | Cannot assess |
| Additive Value | 3 | South Atlantic Anomaly; equatorial ionosphere; unique Southern Hemisphere |
| **Total** | **5/18** | |

## Verdict

⏭️ **Skip** — Endpoints unreachable. The scientific value is exceptional (SAA, equatorial ionosphere), but no programmatic access confirmed. NOAA SWPC and INTERMAGNET provide some complementary global data. Revisit when INPE's space weather services are accessible.
