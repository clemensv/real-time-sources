# Space / Orbital Candidates

Real-time and near-real-time data sources for space situational awareness, orbital mechanics, and astronomical transients.

| Source | Protocol | Auth | Freshness | Total Score |
|--------|----------|------|-----------|-------------|
| [NASA DONKI](nasa-donki.md) | REST | API Key (free) | Hours | 17/18 |
| [NASA NEO](nasa-neo.md) | REST | API Key (free) | Daily | 17/18 |
| [CelesTrak](celestrak.md) | REST | None | Hours | 16/18 |
| [ZTF Alerts](ztf-alerts.md) | Kafka | None | Nightly | 16/18 |
| [NASA GCN](nasa-gcn.md) | Kafka | OAuth2 (free) | Seconds | 15/18 |
| [Space-Track](space-track.md) | REST | Account (free) | Hours | 14/18 |
| [ESA DISCOSweb](esa-discos.md) | REST | Token (free) | Catalog | 13/18 |

## Summary

This domain is rich with high-quality data sources. NASA DONKI and NEO provide well-structured event and object data with free API keys. CelesTrak is the no-auth champion for orbital data. The two Kafka-native sources — ZTF and GCN — are exciting for streaming applications. Space-Track is authoritative but requires session authentication. ESA DISCOSweb adds physical characterization data for space objects.
