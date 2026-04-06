# Power Outages — Candidate Sources

| Slug | Source | Region | Protocol | Auth | Score |
|------|--------|--------|----------|------|-------|
| [poweroutage-us](poweroutage-us.md) | PowerOutage.us | US | Web (scraping) | N/A | 11/18 |
| [uk-power-networks](uk-power-networks.md) | UK Power Networks | UK (SE/E/London) | Web/JSON | None | 12/18 |

## Summary
Two candidates covering US-wide (PowerOutage.us) and UK regional (UK Power Networks) outage data. Both face the fundamental challenge of no public REST API — outage data in the power industry is typically served through web portals rather than developer-friendly APIs. PowerOutage.us provides the unique value of aggregating 1000+ utility feeds but has no API. UKPN is one of six UK DNOs. This domain has lower overall API maturity compared to weather or transport. Direct integration with individual utility OMS platforms may be a more sustainable approach.
