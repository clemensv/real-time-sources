# Radio Propagation Candidates

Real-time HF radio propagation monitoring from amateur radio networks, ionospheric measurements, and space weather indices.

| Source | Protocol | Auth | Freshness | Total Score |
|--------|----------|------|-----------|-------------|
| [PSKReporter](pskreporter.md) | REST + WebSocket | None/API Key | Real-time | 15/18 |
| [WSPRnet](wsprnet.md) | HTTP/JSON | None | 2 minutes | 15/18 |
| [Reverse Beacon Network](reverse-beacon-network.md) | Telnet | Callsign | Real-time | 15/18 |
| [GIRO Ionosonde](giro-ionosonde.md) | REST | None | 5-15 min | 15/18 |
| [NOAA SWPC Alerts](noaa-swpc-alerts.md) | REST | None | Real-time | 15/18 |
| [DX Cluster](dx-cluster.md) | Telnet/REST | Callsign | Real-time | 14/18 |
| [HamQSL Solar Indices](hamqsl-solar-indices.md) | REST (XML) | None | 15-30 min | 13/18 |
| [DXHeat](dxheat.md) | Web/AJAX | None | Real-time | 12/18 |

## Summary

The radio propagation domain now spans the full chain from cause to effect. NOAA SWPC Alerts provide the authoritative space weather warnings. GIRO ionosonde data gives ground-truth ionospheric measurements (foF2, MUF) — the raw physics that determines what frequencies will propagate. HamQSL aggregates solar and geomagnetic indices into a single convenient endpoint.

On the observation side, the Reverse Beacon Network joins PSKReporter and WSPRnet as a third automated propagation monitoring network — its SDR skimmers decode CW and digital signals across the HF bands continuously. DX Cluster remains the human-reported workhorse. DXHeat aggregates all these into a web interface but lacks a formal API.

The full picture: solar event (SWPC alerts) → ionospheric response (GIRO) → propagation conditions (HamQSL indices) → observed paths (RBN + PSKReporter + WSPRnet + DX Cluster). This domain is a complete, real-time, citizen-science-powered sensing chain from the Sun to your radio.
