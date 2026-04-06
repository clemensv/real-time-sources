# Santiago RED/Metro Transit — Chile

**Country/Region**: Chile (Santiago metropolitan area)
**Publisher**: Directorio de Transporte Público Metropolitano (DTPM)
**API Endpoint**: `https://www.red.cl/` (connection failed), `https://api.scltrans.cl/` (connection failed)
**Documentation**: https://www.dtpm.cl/
**Protocol**: GTFS / GTFS-RT (suspected)
**Auth**: Unknown
**Data Format**: GTFS / Protobuf (suspected)
**Update Frequency**: Real-time (for GTFS-RT)
**License**: Chilean government / municipal

## What It Provides

Santiago's public transport system ("RED" — formerly Transantiago) serves 6.5 million people and includes:

- **Bus network**: ~6,000 buses across ~300 routes; second-largest BRT system in the Americas
- **Metro**: 7 lines, 136 stations, serving 2.5+ million daily trips
- **Intermodal integration**: Unified fare card (bip!)

Santiago's transit system is notable for:
- Complete fleet GPS tracking (all buses have GPS units)
- Unified fare collection providing trip data
- Known to have produced GTFS feeds historically
- Integration of electric buses (Santiago has the largest electric bus fleet outside China)

## API Details

All tested endpoints failed:
```
https://www.red.cl/restservice_v2/rest/getdetenpilugar/all → Connection failed
https://api.scltrans.cl/api/v3/stops → Connection failed
https://api.xor.cl/red/bus-stop/PA1 → Timeout
https://www.dtpm.cl/descargas/gtfs/GTFS.zip → Connection failed
```

The `api.xor.cl/red/` community API (by the same developer who provides Chile's earthquake API) timed out but may work intermittently.

### Known Historical GTFS-RT

Santiago historically provided GTFS-RT vehicle positions at:
```
https://gtfs.transantiago.cl/v3/vehiclepositions.pb
```

This endpoint was not tested directly (Protobuf binary format).

## Integration Notes

- Santiago has the largest electric bus fleet outside China (~2,000 electric buses from BYD and Yutong)
- The DTPM publishes service quality indicators and operational data
- GTFS static feeds have been available historically
- GTFS-RT would provide real-time vehicle positions
- The api.xor.cl community wrapper suggests there are underlying APIs
- Santiago Metro is the most extensive subway in South America

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | GTFS-RT likely exists; GPS tracking confirmed |
| Openness | 1 | API endpoints unreachable; GTFS feeds known to exist |
| Stability | 2 | Major city transit system; DTPM is well-resourced |
| Structure | 2 | GTFS/GTFS-RT are standard formats |
| Identifiers | 2 | GTFS route/stop/trip IDs are standard |
| Additive Value | 2 | Largest electric bus fleet outside China; first LatAm Metro |
| **Total** | **11/18** | |

## Verdict

⚠️ **Maybe** — GTFS-RT likely exists but endpoints were unreachable during testing. The historical `gtfs.transantiago.cl` URL should be probed directly for Protobuf data. Santiago's electric bus fleet data is unique. Worth revisiting with direct Protobuf fetching.
