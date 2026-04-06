# Power Outages — Candidate Sources

| Slug | Source | Region | Protocol | Auth | Score |
|------|--------|--------|----------|------|-------|
| [eskomsepush](eskomsepush.md) | EskomSePush API | South Africa | REST/JSON | API Key (paid) | 14/18 |
| [hydro-quebec](hydro-quebec.md) | Hydro-Québec Outages | Québec, Canada | Web SPA (Angular) | None | 14/18 |
| [uk-power-networks](uk-power-networks.md) | UK Power Networks | UK (SE/E/London) | Web/JSON | None | 12/18 |
| [poweroutage-us](poweroutage-us.md) | PowerOutage.us | US | Web (scraping) | N/A | 11/18 |
| [eskom-loadshedding](eskom-loadshedding.md) | Eskom Direct Loadshedding | South Africa | HTTP/plain text | None | 10/18 |

## Summary
Five candidates covering South African loadshedding (EskomSePush + Eskom Direct), Québec (Hydro-Québec), UK regional (UK Power Networks), and US-wide aggregation (PowerOutage.us). EskomSePush is the domain's first confirmed production REST API — returning proper JSON with area-level loadshedding schedules, though it requires a paid API key. The complementary free Eskom endpoint returns the national stage as a single integer. Hydro-Québec serves 4.4 million customers through an Angular SPA with structured data behind JavaScript. The power outage domain remains challenging — utilities treat outage data as operational rather than developer-facing, but South Africa's loadshedding crisis has forced API innovation.
