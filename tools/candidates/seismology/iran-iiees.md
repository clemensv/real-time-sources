# Iran IIEES — International Institute of Earthquake Engineering and Seismology

**Country/Region**: Iran
**Publisher**: International Institute of Earthquake Engineering and Seismology (IIEES)
**API Endpoint**: `https://www.iiees.ac.ir/en/` (institutional website), `http://irsc.ut.ac.ir/` (Iranian Seismological Center)
**Documentation**: http://irsc.ut.ac.ir/currentearthquakes_en.php
**Protocol**: Web portal (HTML)
**Auth**: N/A (no public API discovered)
**Data Format**: HTML, tabular web data
**Update Frequency**: Near-real-time earthquake bulletins; FDSN waveform data for some events
**License**: Iranian academic/government data

## What It Provides

Iran sits atop the Alpide seismic belt — one of the most seismically active regions on Earth. The collision between the Arabian and Eurasian plates generates frequent, destructive earthquakes. Major recent events include:
- 2003 Bam earthquake (M6.6, ~26,000 deaths)
- 2017 Iran-Iraq earthquake (M7.3)
- 2022 Hormozgan earthquakes (M6.0+)

### Iranian Seismological Center (IRSC)

The IRSC at the University of Tehran maintains Iran's national earthquake catalog and operates the Iranian Seismic Network. The website at `irsc.ut.ac.ir` provides:
- Real-time earthquake listings (updated within minutes)
- Earthquake parameters: magnitude, depth, location, origin time
- Historical catalog
- Focal mechanism solutions

### IIEES

IIEES is the premier earthquake engineering research institute in Iran:
- Strong motion records
- Seismic hazard analysis
- Building damage surveys
- FDSN data node

### Probe Results

Connection to `irimo.ir` (weather) **failed**. The IRSC and IIEES websites were not probed directly but are known to be operational. Iranian web infrastructure can be intermittent from international connections due to network routing through limited peering points.

### FDSN Status

Iran operates FDSN-compatible seismographic stations. The IIEES is listed as an FDSN member, but their FDSN web services endpoint status was not verified. FDSN event query:
```
http://service.iiees.ac.ir/fdsnws/event/1/query?starttime=...&endtime=...&format=text
```
This endpoint could not be tested due to connection issues but is documented in the FDSN registry.

## Entity Model

- **Earthquake**: Location, magnitude (ML, Mw, mb), depth, origin time
- **Station**: Iranian Seismic Network stations (codes: THKV, TAFM, etc.)
- **Strong Motion**: Acceleration records from strong motion instruments
- **Focal Mechanism**: Fault plane solutions for larger events

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Near-real-time earthquake bulletins; confirmed by global catalog comparison |
| Openness | 1 | Websites exist but connectivity issues; FDSN endpoint documented but unverified |
| Stability | 1 | Academic/government institutions; infrastructure may have connectivity issues |
| Structure | 1 | HTML listings on IRSC; FDSN waveforms if endpoint works |
| Identifiers | 2 | FDSN station codes; event IDs in IRSC catalog |
| Additive Value | 3 | Iran is among the top 10 seismically active countries; local data has unique detail |
| **Total** | **10/18** | |

## Integration Notes

- Iranian seismic events are already captured by USGS, EMSC, and GFZ global feeds — but with less local detail
- The FDSN endpoint, if functional, would integrate with existing FDSN adapter pattern
- Connectivity to Iranian web infrastructure may be unreliable from some geographic locations
- Iran's seismological data is scientifically important for understanding the Zagros and Alborz mountain building
- The AFAD Turkey feed (existing candidate) already captures some Iran-Turkey border events

## Verdict

Seismologically critical but operationally challenging. Iran experiences frequent destructive earthquakes and has institutional capacity for monitoring. The data may be accessible through FDSN protocols, but connectivity from international origins is unreliable. Global feeds provide partial coverage, but local Iranian data would add significant value for the Zagros/Alborz seismic zones. Worth retesting periodically, especially the FDSN endpoint.
