# NASA GCN (General Coordinates Network)

**Country/Region**: Global
**Publisher**: NASA / GSFC (Goddard Space Flight Center)
**API Endpoint**: `kafka://kafka.gcn.nasa.gov/`
**Documentation**: https://gcn.nasa.gov/docs
**Protocol**: Kafka (Apache Kafka over TLS)
**Auth**: OAuth2 client credentials (free registration at gcn.nasa.gov)
**Data Format**: VOEvent XML, JSON, plain text (varies by topic)
**Update Frequency**: Event-driven (alerts within seconds of detection)
**License**: US Government public domain

## What It Provides

GCN (General Coordinates Network) is NASA's platform for distributing astronomical transient alerts — gamma-ray bursts, gravitational wave events, neutrino detections, and other high-energy phenomena. It is the established platform for multi-messenger astronomy, connecting space observatories (Fermi, Swift, INTEGRAL), ground-based facilities (LIGO/Virgo/KAGRA, IceCube), and thousands of astronomers worldwide.

GCN has two data products: **Notices** (automated machine-to-machine real-time alerts) and **Circulars** (human-readable rapid bulletins). The modern GCN uses Apache Kafka for distribution, replacing the legacy socket-based GCN Classic.

## API Details

- **Kafka broker**: `kafka.gcn.nasa.gov:9092` (TLS)
- **Authentication**: OAuth2 client credentials from https://gcn.nasa.gov/quickstart
- **Client libraries**: `gcn-kafka` for Python and Node.js (wrappers around confluent-kafka)
- **Topics**: `gcn.classic.text.*`, `gcn.classic.voevent.*`, `gcn.notices.*`
- **Example topics**: `gcn.classic.text.FERMI_GBM_FIN_POS`, `gcn.classic.text.LVC_INITIAL`, `gcn.notices.swift.bat.guano`, `gcn.notices.icecube.lvk_nu_track_search`
- **Message formats**: VOEvent XML (legacy), JSON (new notices), plain text (classic text format)
- **Replay**: Kafka consumer groups allow replay from earliest offset
- **Circulars API**: `https://gcn.nasa.gov/circulars` — REST API for human-readable bulletins

## Freshness Assessment

GCN notices are among the fastest scientific alerts on Earth — gamma-ray burst positions from Fermi GBM arrive within seconds of detection. Gravitational wave alerts from LIGO/Virgo arrive within minutes. The Kafka-based architecture ensures reliable, low-latency delivery. This is genuine real-time science.

## Entity Model

- **Notice**: Machine-generated alert with event type, sky position (RA/Dec), error region, instrument, trigger time
- **Circular**: Human-authored bulletin with GCN Circular number, subject, body text, author
- **Event**: Transient astronomical event (GRB, GW, neutrino) that may have multiple notices and circulars
- **Mission/Instrument**: Source observatory (Fermi GBM, Swift BAT, LIGO, IceCube, etc.)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Sub-second to minutes; real-time alerts |
| Openness | 2 | Free registration required; OAuth2 credentials |
| Stability | 3 | NASA GSFC operated; critical astronomy infrastructure |
| Structure | 2 | Mixed formats (VOEvent XML, JSON, text) across topics |
| Identifiers | 2 | Trigger IDs, GCN Circular numbers; no unified URI scheme |
| Additive Value | 3 | Unique — the world's multi-messenger astronomy alert system |
| **Total** | **15/18** | |

## Notes

- GCN is Kafka-native — a rare and exciting real-time streaming source for the project.
- The `gcn-kafka` Python library makes it trivial to start consuming alerts.
- This is operational science infrastructure — alerts from GCN trigger telescope slews worldwide.
- The transition from GCN Classic (socket-based, since 1992) to modern Kafka GCN is ongoing.
- VOEvent XML is the IVOA standard for astronomical transient alerts; newer notices use JSON.
- The Circulars archive goes back to 1997 and is a rich corpus of rapid-response astronomy.
