# Radio Propagation Candidates

Real-time HF radio propagation monitoring from amateur radio networks.

| Source | Protocol | Auth | Freshness | Total Score |
|--------|----------|------|-----------|-------------|
| [PSKReporter](pskreporter.md) | REST + WebSocket | None/API Key | Real-time | 15/18 |
| [WSPRnet](wsprnet.md) | HTTP/JSON | None | 2 minutes | 15/18 |
| [DX Cluster](dx-cluster.md) | Telnet/REST | Callsign | Real-time | 14/18 |

## Summary

All three sources provide unique windows into HF radio propagation — effectively crowd-sourced ionospheric monitoring. PSKReporter offers the most modern integration (WebSocket) with the broadest mode coverage. WSPRnet provides the most scientifically rigorous data thanks to WSPR's standardized transmission protocol. DX Cluster is the legacy workhorse with the longest history. Together they create a comprehensive picture of real-time radio propagation conditions worldwide.

The radio propagation domain is inherently tied to geomagnetic and solar activity — combining these sources with Kp index and NOAA SWPC data creates a powerful space-weather-to-propagation correlation capability.
