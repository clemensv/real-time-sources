# Border Crossings — Candidate Sources

| Slug | Source | Region | Protocol | Auth | Score |
|------|--------|--------|----------|------|-------|
| [cbp-border-wait-times](cbp-border-wait-times.md) | US CBP Border Wait Times | US borders | REST/Angular | None | 14/18 |
| [cbsa-wait-times](cbsa-wait-times.md) | Canada CBSA Wait Times | Canada borders | HTML | None | 13/18 |

## Summary
Two complementary candidates covering US (CBP) and Canadian (CBSA) border wait times. Together they provide both directions of the US-Canada border. CBP has a more modern Angular SPA but the internal API is not well-documented. CBSA provides data as an HTML table that is well-structured but requires parsing. Both update at least hourly. The main challenge in this domain is the lack of formal, documented REST APIs — both agencies serve data primarily through web portals rather than developer-friendly endpoints.
