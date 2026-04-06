# TransMilenio Bogotá — Colombia

**Country/Region**: Colombia (Bogotá)
**Publisher**: TransMilenio S.A.
**API Endpoint**: `https://datos.transmilenio.gov.co/` (connection failed)
**Documentation**: https://www.transmilenio.gov.co/
**Protocol**: CKAN (suspected — datos.transmilenio.gov.co)
**Auth**: Unknown
**Data Format**: Unknown
**Update Frequency**: Real-time (vehicle tracking exists)
**License**: Bogotá municipal entity

## What It Provides

TransMilenio is Bogotá's Bus Rapid Transit (BRT) system — one of the largest and most studied BRT systems in the world:

- **Ridership**: ~2.5 million daily passengers
- **Network**: 12 trunk routes on dedicated lanes + 260+ feeder routes
- **Fleet**: ~2,000+ buses (articulated and bi-articulated on trunk routes)
- **Historical significance**: TransMilenio (opened 2000) pioneered the modern BRT concept, inspiring systems worldwide (Lima, Santiago, Istanbul, Jakarta, etc.)

The system has GPS tracking on all trunk vehicles and Bogotá has an open data portal (datos.transmilenio.gov.co) that was designed to host GTFS and real-time data.

## API Details

```
https://datos.transmilenio.gov.co/ → Connection failed
```

The open data portal was unreachable during testing. Historically, GTFS static feeds have been published.

### Alternative: datos.gov.co

Colombia's national open data portal (datos.gov.co) hosts some TransMilenio datasets, but real-time vehicle positions were not found there.

## Integration Notes

- TransMilenio is THE reference BRT system — used as a case study in transit planning worldwide
- Bogotá also has a growing bike network (ciclovía) with potential GBFS data
- The datos.transmilenio.gov.co portal suggests CKAN-based data hosting
- GTFS feeds are periodically published but real-time feeds are unconfirmed
- Bogotá is at 2,640m elevation — the highest-altitude major BRT system

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | GPS tracking exists; real-time API unconfirmed |
| Openness | 1 | Open data portal exists but unreachable |
| Stability | 2 | Major transit agency; open data initiative known |
| Structure | 1 | GTFS likely available; real-time status unknown |
| Identifiers | 1 | Unknown |
| Additive Value | 2 | THE reference BRT system worldwide |
| **Total** | **8/18** | |

## Verdict

⏭️ **Skip for now** — Open data portal unreachable. TransMilenio's significance in transit planning makes it worth revisiting. Check datos.transmilenio.gov.co periodically and look for GTFS-RT feeds.
