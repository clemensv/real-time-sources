# Power Outages — Candidate Sources

| Slug | Source | Region | Protocol | Auth | Score |
|------|--------|--------|----------|------|-------|
| [eskomsepush](eskomsepush.md) | EskomSePush API | South Africa | REST/JSON | API Key (paid) | 14/18 |
| [hydro-quebec](hydro-quebec.md) | Hydro-Québec Outages | Québec, Canada | Web SPA (Angular) | None | 14/18 |
| [uk-power-networks](uk-power-networks.md) | UK Power Networks | UK (SE/E/London) | Web/JSON | None | 12/18 |
| [poweroutage-us](poweroutage-us.md) | PowerOutage.us | US | Web (scraping) | N/A | 11/18 |
| [eskom-loadshedding](eskom-loadshedding.md) | Eskom Direct Loadshedding | South Africa | HTTP/plain text | None | 10/18 |
| [eskom-loadshedding-api](eskom-loadshedding-api.md) | Eskom Loadshedding Status API (raw) | South Africa | REST/plain text | None | 11/18 |
| [eskomsepush-africa](eskomsepush-africa.md) | EskomSePush (Africa context) | South Africa | REST/JSON | API Key | 14/18 |

## Summary
Seven candidates covering South African loadshedding (EskomSePush + Eskom Direct + raw API), Québec (Hydro-Québec), UK regional (UK Power Networks), and US-wide aggregation (PowerOutage.us). The Eskom raw API provides the most upstream signal — a single integer representing the current loadshedding stage, polled in real-time with no authentication. EskomSePush adds area-specific schedules and richer metadata. South Africa's loadshedding crisis has produced Africa's most innovative power outage APIs, making it a standout for the continent.
