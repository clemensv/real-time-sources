# Space / Orbital Candidates

Real-time and near-real-time data sources for space situational awareness, orbital mechanics, and astronomical transients.

| Source | Protocol | Auth | Freshness | Total Score |
|--------|----------|------|-----------|-------------|
| [GraceDB Gravitational Waves](gracedb-gravitational-waves.md) | REST | None | Seconds | 18/18 |
| [NASA DONKI](nasa-donki.md) | REST | API Key (free) | Hours | 17/18 |
| [NASA NEO](nasa-neo.md) | REST | API Key (free) | Daily | 17/18 |
| [CelesTrak](celestrak.md) | REST | None | Hours | 16/18 |
| [ZTF Alerts](ztf-alerts.md) | Kafka | None | Nightly | 16/18 |
| [JPL Horizons](jpl-horizons.md) | REST | None | On-demand | 16/18 |
| [DSCOVR Solar Wind](dscovr-solar-wind.md) | REST | None | ~1 minute | 16/18 |
| [Helioviewer Solar Imagery](helioviewer-solar-imagery.md) | REST | None | 15-30 min | 16/18 |
| [JPL SBDB Close Approach](jpl-sbdb-close-approach.md) | REST | None | Continuous | 16/18 |
| [AAVSO Variable Stars](aavso-variable-stars.md) | REST | None/Key | Hours | 16/18 |
| [NASA GCN](nasa-gcn.md) | Kafka | OAuth2 (free) | Seconds | 15/18 |
| [Minor Planet Center](minor-planet-center.md) | HTTP | None | Daily | 15/18 |
| [Space-Track](space-track.md) | REST | Account (free) | Hours | 14/18 |
| [ESA DISCOSweb](esa-discos.md) | REST | Token (free) | Catalog | 13/18 |

## Summary

GraceDB is the new crown jewel — a perfect 18/18 for the LIGO/Virgo/KAGRA gravitational wave candidate database, with real-time events, no auth, and clean JSON. This is spacetime rippling, accessible via REST.

The solar/heliophysics chain is now well-represented: DSCOVR provides real-time solar wind measurements from L1, Helioviewer serves near-real-time solar imagery (SDO, SOHO), and NOAA DONKI catalogs the events. JPL Horizons and the SBDB Close Approach API cover the solar system ephemeris and asteroid traffic. The Minor Planet Center is the authoritative asteroid/comet clearinghouse (legacy text format, but irreplaceable). AAVSO adds a century of variable star observations with a modern API.

The existing sources remain strong: CelesTrak for no-auth orbital data, ZTF and GCN for streaming transient astronomy, Space-Track for authoritative orbital catalogs, and ESA DISCOSweb for physical characterization.
