# NOAA SWPC Alerts and Watches

**Country/Region**: Global
**Publisher**: NOAA Space Weather Prediction Center
**API Endpoint**: `https://services.swpc.noaa.gov/products/alerts.json`
**Documentation**: https://www.swpc.noaa.gov/products/alerts-watches-and-warnings
**Protocol**: REST (JSON)
**Auth**: None
**Data Format**: JSON (array of alert objects)
**Update Frequency**: Real-time — alerts posted within minutes of issuance
**License**: Public domain (US government)

## What It Provides

NOAA SWPC issues space weather alerts, watches, and warnings — the meteorological equivalent of severe weather alerts, but for space weather. These cover geomagnetic storms (G-scale), solar radiation storms (S-scale), radio blackouts (R-scale), and various observational summaries. The alerts JSON endpoint provides the full archive of recent alerts as structured text messages.

Each alert contains a product code, issuance time, and the full message text including serial numbers, begin/end times, observed values, and potential impacts.

## API Details

- **Alerts list**: `GET /products/alerts.json` — full array of recent alerts
- **Alert structure**: `product_id` (code like `ALTEF3`, `WARSUD`), `issue_datetime`, `message` (full text)
- **Product codes**: `ALTK{n}` (Kp alerts), `ALTEF{n}` (electron flux), `WARSUD` (geomagnetic sudden impulse), `WATA{n}` (watches), `SUMX{n}` (X-ray event summaries)
- **No auth required**: Public JSON endpoint
- **No rate limit**: Static JSON file, updated on alert issuance
- **Companion endpoints**: `/products/summary/solar-wind-speed.json`, `/products/summary/10cm-flux.json`

## Freshness Assessment

Alerts appear in the JSON within minutes of issuance. During active space weather, multiple alerts may be issued per hour. The alert file is regenerated with each new issuance.

Confirmed live: 203 alerts in the file. Most recent was a continued electron flux alert (ALTEF3) issued 2026-04-06 04:59 UTC, reporting 2MeV flux at 5995 pfu with begin time April 3. This aligns perfectly with the DSCOVR data showing elevated solar wind.

## Entity Model

- **Alert**: `product_id` (code), `issue_datetime` (UTC), `message` (full text with structured content)
- **Alert types**: Kp alerts, electron/proton flux, radio blackouts, geomagnetic sudden impulses, watches, warnings
- **Serial numbers**: Sequential within alert type for tracking and continuation
- **Impact descriptions**: Standardized potential impact text for each severity level

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time, alerts posted within minutes of issuance |
| Openness | 3 | No auth, public domain, public JSON |
| Stability | 3 | NOAA operational infrastructure |
| Structure | 2 | JSON array but alert text is unstructured narrative (requires text parsing for values) |
| Identifiers | 2 | Product IDs and serial numbers; no unique event URIs |
| Additive Value | 2 | Authoritative space weather alerts; operational decision-making data |
| **Total** | **15/18** | |

## Notes

- Confirmed live with 203 alerts — active space weather at time of probing.
- Alert messages are human-readable text with embedded structured data (serial numbers, timestamps, values) — parsing requires regex or template matching.
- Product code taxonomy is the key to filtering: `ALT*` = alerts, `WAR*` = warnings, `WAT*` = watches, `SUM*` = summaries.
- These alerts drive operational decisions: satellite operators, airlines (polar routes), power grid operators all consume SWPC alerts.
- Pairs with DSCOVR (raw measurements that trigger alerts), DONKI (CME/flare events that cause alerts), and radio propagation sources (alerts predict HF blackouts).
