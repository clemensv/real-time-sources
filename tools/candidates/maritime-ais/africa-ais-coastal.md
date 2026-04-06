# African Maritime AIS via AISHub/MarineTraffic

- **Country/Region**: Pan-African coastal waters
- **Endpoint**: `http://data.aishub.net/ws.php?username={user}&format=1&output=json&compress=0&latmin=-35&latmax=37&lonmin=-20&lonmax=55`
- **Protocol**: REST / Raw TCP (AIS NMEA)
- **Auth**: API key (AISHub community) / Subscription (MarineTraffic)
- **Format**: JSON, CSV, NMEA
- **Freshness**: Real-time (vessel position reports every 2–30 seconds)
- **Docs**: https://www.aishub.net/api
- **Score**: 12/18

## Overview

Africa's coastline stretches over 30,000 km, with some of the world's busiest shipping
lanes (Suez Canal, Strait of Gibraltar, Cape of Good Hope, Mozambique Channel, Gulf
of Guinea). AIS (Automatic Identification System) data from African coastal stations
provides real-time vessel tracking for:

- **Suez Canal traffic**: One of the world's most critical chokepoints
- **Cape route shipping**: Alternative to Suez, used by VLCCs
- **Gulf of Guinea**: Oil tanker traffic, piracy monitoring
- **East African ports**: Mombasa, Dar es Salaam, Maputo
- **West African ports**: Lagos, Tema, Abidjan, Dakar
- **Fishing vessel monitoring**: Combating IUU (illegal, unreported, unregulated) fishing

## Endpoint Analysis

AIS data for African waters is available through multiple channels:

1. **AISHub Community**: Share an AIS receiver, get access to community data
   ```
   GET http://data.aishub.net/ws.php?username=KEY
     &format=1&output=json&compress=0
     &latmin=-35&latmax=37&lonmin=-20&lonmax=55
   ```

2. **MarineTraffic API**: Commercial API with good African coverage
   ```
   GET https://services.marinetraffic.com/api/exportvessels/v:8/{API_KEY}/...
   ```

3. **UN Global Platform AIS**: Academic/research access to satellite AIS data
   covering remote African waters (UNGP)

4. **Kystverket-style feeds**: Some African port authorities (South Africa SAMSA)
   may provide coastal AIS data.

AIS coverage gaps in Africa:
- **West Africa inland**: Limited terrestrial AIS stations between major ports
- **Central African coast**: Cameroon, Gabon, Congo — sparse coverage
- **Madagascar east coast**: Limited stations

Satellite AIS (S-AIS) fills these gaps but typically requires commercial subscriptions.

## Integration Notes

- **Existing bridge**: The repository has a `kystverket-ais` bridge for Norway.
  The same AIS processing logic applies to African waters.
- **AISHub membership**: Requires contributing an AIS receiver. If you have one near
  African waters, you get community access. Otherwise, this is read-only for members.
- **Bounding box filtering**: Use the African coastal bounding box to limit data to
  African waters. This significantly reduces the data volume.
- **IUU fishing**: Vessel tracking in African EEZs (Exclusive Economic Zones) is a
  major policy interest. Foreign fishing vessels operating without transponders is
  a documented problem — AIS "dark" vessels are the signal.
- **Suez Canal monitoring**: Real-time AIS data from the Suez Canal is extremely
  valuable for global supply chain monitoring.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time AIS positions |
| Openness | 1 | Community/commercial access models |
| Stability | 2 | Depends on coastal AIS infrastructure |
| Structure | 2 | NMEA/JSON, well-defined AIS protocol |
| Identifiers | 3 | MMSI (Maritime Mobile Service Identity) |
| Richness | 1 | Position, speed, heading, vessel type |
