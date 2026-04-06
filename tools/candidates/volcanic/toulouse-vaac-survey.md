# Toulouse VAAC — European Volcanic Ash Advisory Center

## Source Identity

| Field            | Value |
|------------------|-------|
| **Full Name**    | Toulouse Volcanic Ash Advisory Center (VAAC) |
| **Operator**     | Météo-France |
| **URL**          | https://vaac.meteo.fr/ |
| **Coverage**     | Europe, Africa, Middle East (ICAO EUR/AFI regions) |
| **Update Freq.** | Every 6 hours during active ash events; continuous monitoring |

## What It Does

The Toulouse VAAC is one of nine Volcanic Ash Advisory Centers worldwide, responsible for monitoring and issuing ash cloud advisories for a vast area covering Europe, Africa, and parts of the Middle East. This is the VAAC that would activate for eruptions of Etna (Italy), Cumbre Vieja (Canary Islands), Nyiragongo (DRC), or the Icelandic volcanoes that periodically shut down European airspace.

The 2010 Eyjafjallajökull crisis — when a single Icelandic eruption closed European airspace for six days and stranded 10 million passengers — was primarily a Toulouse (and London) VAAC event. That crisis reshaped volcanic ash monitoring worldwide.

## Endpoints Probed

| Endpoint | Status | Notes |
|----------|--------|-------|
| Main website | ✅ 200 | Modern web application; volcano list, advisories |
| `/api/advisories` | ❌ 404 | No public API found |
| `/rss` | ❌ 404 | No RSS feed |
| `/ajax/volcanoHandler.php` | ❌ Blocked | WAF rejection ("Request Rejected") |
| `/volcano-list` | ❌ 404 | URL not found |

### Website Content

The Toulouse VAAC website is a modern, well-designed web application that provides:
- Interactive map of monitored volcanoes
- Current and historical VAAs (Volcanic Ash Advisories)
- Volcanic ash dispersion model outputs
- Archive of past eruption events

The data is JavaScript-rendered with XHR calls to backend services — the WAF (Web Application Firewall) actively blocks programmatic access to the AJAX endpoints.

## All Nine VAACs — Status Survey

| VAAC | Location | Operator | Region | URL | API Status |
|------|----------|----------|--------|-----|------------|
| **Washington** | USA | NOAA | Americas (continental) | ssd.noaa.gov/VAAC/ | ✅ XML/KML files |
| **Anchorage** | USA | NOAA | North Pacific, Alaska | ssd.noaa.gov/VAAC/AKVAAC/ | ✅ Part of Washington VAAC system |
| **Montreal** | Canada | ECCC | Canada, North Atlantic | canada.ca (path) | ❌ Timeout |
| **Buenos Aires** | Argentina | SMN | South America | smn.gob.ar/vaac | ❌ 403 Forbidden |
| **London** | UK | Met Office | UK, NE Atlantic, Iceland | metoffice.gov.uk/aviation/vaac/ | ✅ Website accessible |
| **Toulouse** | France | Météo-France | Europe, Africa, Middle East | vaac.meteo.fr | ⚠️ Website only; API blocked |
| **Darwin** | Australia | BoM | Australia, SE Asia | bom.gov.au/aviation/warnings/ | ✅ Website accessible |
| **Tokyo** | Japan | JMA | Western Pacific, Asia | ds.data.jma.go.jp/svd/vaac/ | ✅ Advisory table accessible |
| **Wellington** | New Zealand | MetService | SW Pacific | vaac.metservice.com | ❌ Timeout |

### Machine-Readable Feeds

Only the **Washington/Anchorage VAAC** (NOAA) provides documented machine-readable feeds (XML advisories, KML ash cloud polygons). The other VAACs primarily serve HTML websites with no public API.

The **Tokyo VAAC** has an HTML advisory table at `/vaac_list.html` that could be parsed — it lists active volcanoes with color codes and advisory timestamps in a tabular format with JavaScript sorting.

The **London VAAC** (Met Office) may have data products behind their aviation services portal, but no public API was found during probing.

## Authentication & Licensing

- **Auth**: None for websites; no public APIs found.
- **License**: Varies by national met service. VAAC advisories are ICAO operational products — intended for free distribution to aviation.

## Feasibility Rating

| Dimension                    | Score | Notes |
|------------------------------|-------|-------|
| **API Maturity & Docs**      | 1     | No API; WAF blocks programmatic access |
| **Data Freshness**           | 2     | Updated during events; quiet between |
| **Format / Schema Quality**  | 1     | HTML websites only (except Washington VAAC) |
| **Auth / Access Simplicity** | 2     | Websites open; APIs absent or blocked |
| **Coverage Relevance**       | 3     | Europe/Africa — Etna, Iceland, Canary Islands |
| **Operational Reliability**  | 3     | ICAO-mandated operational service |
| **Total**                    | **12 / 18** | |

## Verdict

⏭️ **Skip (Toulouse specifically)** — The Toulouse VAAC has no public API and actively blocks programmatic access. The Washington VAAC (already documented) remains the only VAAC with machine-readable feeds. The Tokyo VAAC's HTML table is the next most parseable. For European volcanic ash coverage, the London VAAC (Icelandic eruptions) would be higher priority than Toulouse, but neither offers an API.

The broader lesson: **VAACs are operationally critical but API-hostile.** The data distribution model is designed for aviation briefing systems (SADIS, ISCS), not public web APIs. The Washington VAAC is the exception. Consider monitoring aviation weather wire services (AFTN/AMHS) if comprehensive VAAC coverage is needed.
