# Border Crossings — Candidate Sources

| Slug | Source | Region | Protocol | Auth | Score |
|------|--------|--------|----------|------|-------|
| [cbp-border-wait-times](cbp-border-wait-times.md) | US CBP Border Wait Times | US borders | REST/JSON | None | 17/18 |
| [cbsa-wait-times](cbsa-wait-times.md) | Canada CBSA Wait Times | Canada borders | HTML | None | 13/18 |
| [eurotunnel](eurotunnel.md) | Eurotunnel / Channel Tunnel | UK–France | Web SPA | None | 12/18 |

## Summary
Three candidates covering US borders (CBP), Canadian borders (CBSA), and the UK–France Channel Tunnel (Eurotunnel). The CBP entry was significantly upgraded from 14/18 to 17/18 after discovering the `bwt.cbp.gov/api/bwtnew` REST endpoint — a clean JSON API returning lane-level wait time data for all 81 US border crossings (both Mexico and Canada) with no authentication and CORS enabled. CBSA provides the Canadian complement as structured HTML. Eurotunnel adds Europe's most important fixed-link crossing but lacks an API. Together, CBP and CBSA cover both directions of the world's longest international border.
