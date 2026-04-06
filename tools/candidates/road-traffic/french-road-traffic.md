# French Road Traffic (transport.data.gouv.fr)

**Country/Region**: France (national non-conceded road network)
**Publisher**: Ministère de la Transition écologique / DIRs (Directions Interdépartementales des Routes)
**API Endpoint**: Various — datasets listed on `https://transport.data.gouv.fr/datasets?type=road-data`
**Documentation**: https://transport.data.gouv.fr/
**Protocol**: DATEX II (XML), GeoJSON
**Auth**: None (Licence Ouverte / Open Licence)
**Data Format**: DATEX II XML, CSV
**Update Frequency**: Real-time for traffic circulation; periodic for historical data
**License**: Licence Ouverte 2.0

## What It Provides

France's national transport data portal publishes real-time traffic data for the non-conceded (non-tolled) national road network. Data includes real-time traffic circulation, road events (incidents, roadworks, closures), and historical traffic volumes. The data follows the DATEX II European standard, making it interoperable with Dutch NDW, Swedish Trafikverket, and other European traffic data publishers.

## API Details

**Key datasets on transport.data.gouv.fr:**

1. **"Circulation en temps réel — Réseau routier non concédé"**
   - Real-time traffic flow on national roads
   - Format: DATEX II XML
   - Published by DIRs (regional road directorates)

2. **"Évènements routiers — Réseau routier non concédé"**
   - Road events: incidents, roadworks, weight restrictions, closures
   - Format: DATEX II XML

3. **"Base Nationale des Lieux de Stationnement (BNLS)"**
   - National parking database
   - Cross-referenced with parking category

4. **"Trafic moyen journalier annuel sur le réseau routier national"**
   - Annual Average Daily Traffic (TMJA)
   - Format: CSV/ZIP
   - 31 files, updated August 2025
   - Historical data spanning multiple years

**Historical traffic (data.gouv.fr):**
```
https://www.data.gouv.fr/fr/datasets/trafic-moyen-journalier-annuel-sur-le-reseau-routier-national/
```

## Freshness Assessment

Real-time traffic circulation and events are published in DATEX II format through the national transport portal. Historical TMJA data is updated annually. The DATEX II feeds follow the same European standard used by NDW Netherlands, Trafikverket Sweden, and Digitraffic Finland.

## Entity Model

- **Traffic Situation**: DATEX II situation with type (flow, event), location, time
- **Road Event**: Incident, roadwork, closure with severity, duration, affected segments
- **Traffic Flow**: Speed, intensity on road segments
- **Measurement Point**: Counting station with historical TMJA data

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time DATEX II feeds |
| Openness | 3 | No auth, Licence Ouverte 2.0 |
| Stability | 3 | Government-operated national platform |
| Structure | 3 | DATEX II standard — same as NDW, Trafikverket |
| Identifiers | 3 | Road numbers, DIR codes, DATEX II situation IDs |
| Additive Value | 3 | French national road network; DATEX II reuse with existing parsers |
| **Total** | **18/18** | |

## Notes

- The DATEX II format is the key value here — building a DATEX II traffic parser for NDW Netherlands (already in the candidate list) means the same parser works for French traffic data with minimal adaptation.
- France's road network is split between conceded (tolled, operated by Vinci/Sanef/etc.) and non-conceded (state-managed). Only the non-conceded network is in the open data feeds. Toll road operators do not publish open data.
- The DIRs (Directions Interdépartementales des Routes) are regional road management authorities — data may be published per DIR or nationally aggregated.
- transport.data.gouv.fr is France's equivalent of the UK's data.gov.uk for transport — it aggregates transit, cycling, road, and parking data nationally.
- Historical TMJA data enables baseline traffic pattern analysis.
