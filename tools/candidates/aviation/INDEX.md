# Aviation — Candidate Sources

Research date: 2026-04-06 (updated)

| Slug | Source | Region | Protocol | Auth | Score |
|------|--------|--------|----------|------|-------|
| [aviationweather-gov](aviationweather-gov.md) | AviationWeather.gov | Global | REST/JSON/GeoJSON | None | 17/18 |
| [opensky-network](opensky-network.md) | OpenSky Network | Global | REST/JSON | OAuth2 (free) | 17/18 |
| [vatsim](vatsim.md) | VATSIM Live Data | Global (sim) | REST/JSON | None | 16/18 |
| [faa-notam-api](faa-notam-api.md) | FAA NOTAM API | US/Global | REST/JSON | API Key (free) | 16/18 |
| [adsb-exchange](adsb-exchange.md) | ADS-B Exchange | Global | REST/JSON | API Key (paid) | 15/18 |
| [faa-swim](faa-swim.md) | FAA SWIM | US | JMS/SOLACE | Cert + registration | 15/18 |
| [eurocontrol-b2b](eurocontrol-b2b.md) | EUROCONTROL B2B | Europe | SOAP/REST | Cert + registration | 15/18 |
| [ivao](ivao.md) | IVAO Whazzup | Global (sim) | REST/JSON | None | 15/18 |
| [adsbhub](adsbhub.md) | ADSBHub | Global | TCP/SBS | IP whitelist (reciprocal) | 12/18 |
| [drone-remote-id](drone-remote-id.md) | Drone Remote ID | US/EU | BLE/WiFi broadcast | None (broadcast) | 2/18 (current) |

## Already Covered
- **mode-s/**: Mode-S local receiver bridge (in main repo)

## Summary

Ten candidates spanning the full spectrum of aviation data. **AviationWeather.gov** is the standout
new discovery — a free, no-auth, OpenAPI-documented service providing global METAR/TAF/SIGMET/PIREP
data in JSON, GeoJSON, XML, CSV, and IWXXM formats. Combined with OpenSky Network for flight tracking,
these two sources provide a comprehensive open aviation data foundation.

**VATSIM** and **IVAO** are surprising additions — flight simulation networks with rich real-time data
feeds that mirror real-world ATC data structures. VATSIM serves ~1,500 concurrent "flights" with full
ICAO flight plans, making it an excellent test data source or demonstration stream.

**FAA NOTAM API** fills a unique niche — airspace restrictions and operational changes are data that
no flight tracking source provides. Free API key required.

**ADSBHub** offers unrestricted-use community ADS-B data via reciprocal sharing — more permissive
licensing than ADS-B Exchange.

**Drone Remote ID** is a forward-looking investigation — the infrastructure is deploying but no
aggregated public API exists yet.

### For immediate integration:
1. **AviationWeather.gov** — Zero friction (no auth), global coverage, GeoJSON output, OpenAPI spec
2. **VATSIM** — Zero friction (no auth), rich flight plan data, excellent for testing
3. **OpenSky Network** — Now requires OAuth2 (was basic auth), credit system limits free tier

### For evaluation:
4. **FAA NOTAM API** — Unique data type, free API key
5. **IVAO** — Richer data model than VATSIM, smaller community
6. **ADSBHub** — Reciprocal sharing model, unrestricted commercial use

### Commercial / restricted:
7. **ADS-B Exchange** — Fully commercial, unfiltered data
8. **FAA SWIM** — US government restricted
9. **EUROCONTROL B2B** — European operational stakeholders only

### Future monitoring:
10. **Drone Remote ID** — No API yet, but regulatory mandates ensure data will be available
