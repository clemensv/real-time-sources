# Border Crossings — Candidate Sources

| Slug | Source | Region | Protocol | Auth | Score |
|------|--------|--------|----------|------|-------|
| [cbsa-wait-times](cbsa-wait-times.md) | Canada CBSA Wait Times | Canada borders | HTML | None | 13/18 |
| [eurotunnel](eurotunnel.md) | Eurotunnel / Channel Tunnel | UK–France | Web SPA | None | 12/18 |

## Summary
Three candidates covering US borders (CBP), Canadian borders (CBSA), and the UK–France Channel Tunnel (Eurotunnel). The CBP entry was significantly upgraded from 14/18 to 17/18 after discovering the `bwt.cbp.gov/api/bwtnew` REST endpoint — a clean JSON API returning lane-level wait time data for all 81 US border crossings (both Mexico and Canada) with no authentication and CORS enabled. CBSA provides the Canadian complement as structured HTML. Eurotunnel adds Europe's most important fixed-link crossing but lacks an API. Together, CBP and CBSA cover both directions of the world's longest international border.

## Round 2026-05 — Gulf + Satellite EO sweep

Added in May 2026 by the Gulf (KW/AE/OM/SA/BH/QA/IQ) and satellite-EO (NASA/ESA/NOAA/EUMETSAT/JAXA/ISRO/KARI/CNSA/Other) research fleets.

| Candidate | File | Score | Verdict |
|---|---|---|---|
| King Fahd Causeway - Border Crossing Wait Times | [bh-king-fahd-causeway.md](bh-king-fahd-causeway.md) | 2/18 | — |

