# Coral / Marine Biology — Candidate Sources

| Slug | Source | Region | Protocol | Auth | Score |
|------|--------|--------|----------|------|-------|
| [obis](obis.md) | OBIS (Ocean Biogeographic Info) | Global | REST/JSON | None | 17/18 |
| [otn-tracking](otn-tracking.md) | Ocean Tracking Network | Global | ERDDAP/JSON | None* | 16/18 |
| [noaa-coral-reef-watch](noaa-coral-reef-watch.md) | NOAA Coral Reef Watch | Global | HTTP/ERDDAP | None | 15/18 |
| [aims-reef-monitoring](aims-reef-monitoring.md) | AIMS Reef Monitoring | Australia/GBR | REST/ERDDAP | API Key | 14/18 |
| [allen-coral-atlas](allen-coral-atlas.md) | Allen Coral Atlas | Global | Web/GCS | None | 13/18 |

## Summary
Five candidates covering marine biodiversity (OBIS), animal tracking (OTN), coral bleaching (NOAA CRW), in-situ reef monitoring (AIMS), and satellite reef mapping (Allen Coral Atlas). OBIS is a powerhouse addition — 177 million+ marine occurrence records via a clean REST JSON API with Darwin Core compliance, WoRMS taxonomy, and no auth required. OTN adds acoustic telemetry tracking of tagged marine animals (sharks, turtles, fish) via ERDDAP, a first for this domain. The Allen Coral Atlas brings the world's only high-resolution global reef classification but lacks a proper API. Together these five sources span the coral/marine monitoring stack from satellite (CRW, Atlas) through in-situ sensors (AIMS) to species-level biodiversity (OBIS, OTN).
