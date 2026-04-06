# Vedur.is — Iceland Met Office Volcanic & Seismic Monitoring

## Source Identity

| Field            | Value |
|------------------|-------|
| **Full Name**    | Veðurstofa Íslands (Icelandic Meteorological Office) |
| **Operator**     | Government of Iceland |
| **URL**          | https://en.vedur.is/ |
| **Earthquake Page** | `https://en.vedur.is/earthquakes-and-volcanism/earthquakes/` |
| **Volcanic Page** | `https://en.vedur.is/earthquakes-and-volcanism/volcanism/` |
| **Coverage**     | Iceland — one of the most volcanically and seismically active places on Earth |
| **Update Freq.** | Continuous; earthquake catalog updated every few minutes |

## What It Does

Iceland sits on the Mid-Atlantic Ridge where the North American and Eurasian plates pull apart, and on top of a mantle plume (the Iceland hotspot). The result is extraordinary: 30+ active volcanic systems, frequent eruptions (Eyjafjallajökull 2010, Bárðarbunga 2014–2015, Fagradalsfjall 2021–2023, Sundhnúksgígar 2023–2026), and constant seismic swarms. Vedur.is monitors all of it.

The web portal shows real-time earthquake maps with events plotted within minutes. The volcanic monitoring section tracks eruption status, gas emissions, and deformation. During the 2023–2026 Reykjanes Peninsula eruption sequence, this became one of the most-watched geoscience portals on the planet.

## Endpoints Probed

| Endpoint | Status | Notes |
|----------|--------|-------|
| Earthquake catalog page (HTML) | ✅ 200 | Interactive map + table; data loaded via JavaScript |
| `api.vedur.is/eqmeasurements/v1/` | ❌ 404 | Old API endpoint defunct |
| `api.vedur.is/skjalftar/v1/quake/array` | ❌ 404 | Old API endpoint defunct |
| `apis.is/earthquake/is` | ❌ SSL error | Third-party wrapper; certificate issues |
| Volcanic eruptions page | ❌ 404 | URL structure changed |

### The API Problem

Vedur.is once had a working JSON API for earthquake data (the `apis.is/earthquake/is` endpoint was a popular wrapper). As of April 2026, all tested API endpoints return 404 or SSL errors. The earthquake data is accessible through the web portal, but it's rendered via JavaScript — meaning the data *is* served as JSON to the browser, just not through a documented public API.

This is a common pattern with national met services: the data exists, the website works, but there's no stable public API contract. The data could be extracted by intercepting the JavaScript XHR calls, but that's fragile.

## Authentication & Licensing

- **Auth**: None for the website.
- **License**: Icelandic government open data. Vedur.is data freely available with attribution.

## Integration Notes

Iceland's volcanic monitoring data is globally significant — the Eyjafjallajökull eruption disrupted European air travel for weeks, and the ongoing Reykjanes eruptions have forced evacuations. But the lack of a stable API makes integration risky.

Options:
1. **Monitor the web portal** — parse the JavaScript data source (fragile)
2. **Use EMSC** — Icelandic earthquakes appear in EMSC data (via SIL network contribution)
3. **Wait for a new API** — Vedur.is may be rebuilding their API infrastructure

For volcanic status specifically, Vedur.is is irreplaceable — no other source provides Iceland-specific eruption status, aviation color codes, and ground deformation data.

## Feasibility Rating

| Dimension                    | Score | Notes |
|------------------------------|-------|-------|
| **API Maturity & Docs**      | 1     | No working API; web scraping only |
| **Data Freshness**           | 3     | Real-time on the website |
| **Format / Schema Quality**  | 1     | No stable format; JavaScript-rendered |
| **Auth / Access Simplicity** | 3     | Open website |
| **Coverage Relevance**       | 3     | Uniquely active volcanic/seismic region |
| **Operational Reliability**  | 2     | Website stable; API endpoints deprecated |
| **Total**                    | **13 / 18** | |

## Verdict

⚠️ **Maybe — high value, low accessibility** — Iceland is one of the most volcanically active places on Earth, and Vedur.is is the only authoritative source. But the lack of a public API makes this fragile to integrate. For earthquakes, EMSC provides Icelandic data through FDSN. For volcanic status, there's no alternative — this is the source. Revisit when/if Vedur.is launches a new API. In the meantime, consider monitoring the aviation color code page as a minimal integration.
