# WSPRnet (Weak Signal Propagation Reporter Network)

**Country/Region**: Global
**Publisher**: WSPRnet community / Joe Taylor (K1JT)
**API Endpoint**: `https://wsprnet.org/olddb` (database query), `http://wsprnet.org/drupal/wsprnet/spots/json` (JSON spots)
**Documentation**: https://wsprnet.org/drupal/, https://physics.princeton.edu/pulsar/k1jt/wspr.html
**Protocol**: HTTP (web query, CSV/JSON download)
**Auth**: None (read access)
**Data Format**: CSV, JSON, HTML tables
**Update Frequency**: Every 2 minutes (WSPR transmission cycle)
**License**: Free to use; community data

## What It Provides

WSPRnet is the reporting network for WSPR (Weak Signal Propagation Reporter) — a digital radio protocol designed specifically for probing HF radio propagation. WSPR transmitters broadcast low-power (typically 200 mW to 5 W) signals with callsign, grid locator, and power level encoded. Receivers decode these signals and upload "spots" to WSPRnet, creating a continuous, systematic map of HF propagation paths.

The WSPRnet activity page confirmed an active network with stations worldwide — callsigns from every continent transmitting on 14 MHz (20-meter band) and other HF bands. The network produces millions of spots per month.

## API Details

- **Activity page**: `https://wsprnet.org/drupal/wsprnet/activity` — current active stations with frequencies
- **Spots query**: `https://wsprnet.org/olddb?mode=html&band=all&limit=100&findcall=&findreporter=&sort=date` (web form)
- **JSON spots**: `http://wsprnet.org/drupal/wsprnet/spots/json?band=all&minutes=10` (recent spots)
- **Spot fields**: Timestamp, reporter callsign, reporter grid, SNR (dB), frequency (MHz), transmitter callsign, transmitter grid, power (dBm), drift (Hz/min), distance (km), azimuth
- **Bands**: 2200m through 2m (MF/HF/VHF), with 20m and 40m being most active
- **WSPR transmission cycle**: 2-minute windows; transmit on even minutes, decode on odd minutes
- **Bulk download**: Monthly database dumps available (CSV)

## Freshness Assessment

WSPR spots arrive every 2 minutes by protocol design — each transmission window is exactly 110.6 seconds. Receivers decode and upload spots within seconds of reception. The 2-minute cadence is inherent to the protocol, making this highly regular and predictable. The network runs 24/7 with consistent global coverage.

## Entity Model

- **Spot**: Reporter + transmitter pair observation at a specific time and frequency
- **Station**: Amateur callsign with Maidenhead grid locator and transmit power
- **Band**: Frequency band (e.g., 14.097 MHz for 20m WSPR)
- **Propagation Path**: Implicit from sender/receiver locations, with distance and azimuth

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 2-minute cycles; protocol-defined regularity |
| Openness | 2 | Free access; no formal license; web-scraping may be needed |
| Stability | 2 | Community-run; has operated since 2008; Joe Taylor (Nobel laureate) created WSPR |
| Structure | 2 | CSV/JSON available but API is informal; web-based query interface |
| Identifiers | 3 | Amateur callsigns; Maidenhead grid locators; precise frequencies |
| Additive Value | 3 | Unique systematic HF propagation measurement; complements PSKReporter |
| **Total** | **15/18** | |

## Notes

- WSPR is specifically designed for propagation monitoring — unlike PSKReporter (which captures opportunistic contacts), WSPR stations transmit continuously with standardized parameters, making the data more scientifically consistent.
- Joe Taylor (K1JT) created WSPR and is a Nobel Prize-winning physicist (1993, for binary pulsar discovery).
- The low power levels (200 mW typical) mean that WSPR detection implies genuine propagation, not just brute-force signal strength.
- WSPR data is used by researchers studying ionospheric propagation, solar-terrestrial interactions, and radio frequency engineering.
- The 2-minute transmission cadence means the data has a precise, clock-like regularity.
- Bulk monthly database dumps are available for historical analysis.
- Complements PSKReporter: WSPR provides controlled-experiment data; PSKReporter provides wider coverage with varied modes.
