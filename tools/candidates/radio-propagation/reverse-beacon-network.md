# Reverse Beacon Network

**Country/Region**: Global (ham radio operators, primarily NA/EU)
**Publisher**: Reverse Beacon Network community
**API Endpoint**: `telnet://telnet.reversebeacon.net:7000` (Telnet); `https://www.reversebeacon.net/` (web)
**Documentation**: https://www.reversebeacon.net/pages/About+the+RBN
**Protocol**: Telnet (DX Cluster protocol), Web scraping
**Auth**: Callsign (Telnet), None (web)
**Data Format**: DX Cluster spot format (text), HTML tables (web)
**Update Frequency**: Real-time (continuous stream, spots every few seconds)
**License**: Public; community-generated data

## What It Provides

The Reverse Beacon Network is an automated network of Software Defined Receivers (SDR "skimmers") that continuously decode CW (Morse code) and digital mode (RTTY, FT8, FT4, PSK) signals on the HF and VHF amateur radio bands. When a skimmer decodes a signal, it posts a "spot" — who was heard, on what frequency, at what signal strength, by which skimmer, and when.

Unlike traditional DX Cluster spots (which are human-reported), RBN spots are fully automated and standardized. The network effectively functions as a distributed HF radio propagation sensor array, mapping which paths are open between which points on the globe, right now.

## API Details

- **Telnet stream**: Connect to `telnet.reversebeacon.net:7000`, authenticate with callsign, receive continuous spot stream
- **Spot format**: `DX de {skimmer_call}: {freq} {spotted_call} {mode} {snr} dB {wpm} WPM {type} {time}Z`
- **Web interface**: Real-time spot display at `reversebeacon.net/main.php`
- **DX Spider protocol**: Standard DX Cluster commands for filtering (`set/filter`, `sh/dx`)
- **No formal REST API**: Data is accessed via Telnet stream or web scraping
- **Volume**: Hundreds to thousands of spots per minute during active periods

## Freshness Assessment

Spots appear within seconds of signal detection. The Telnet stream is continuous and push-based. During active ham radio hours, the network produces thousands of spots per minute across CW, RTTY, FT8, and FT4 modes. This is one of the highest-velocity real-time feeds in the radio propagation domain.

The lack of a REST/JSON API is a friction point, but the Telnet protocol is well-established and trivial to parse programmatically.

## Entity Model

- **Spot**: Skimmer callsign, spotted callsign, frequency (kHz), mode, SNR (dB), speed (WPM for CW), timestamp (UTC)
- **Skimmer**: Callsign, grid square (location), receiver type
- **Band**: Derived from frequency (160m, 80m, 40m, 20m, 15m, 10m, 6m, etc.)
- **Propagation path**: Implicit from skimmer location → spotted station location (if known via callsign database)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time, seconds latency |
| Openness | 2 | Free but requires callsign auth; no REST API |
| Stability | 3 | Running since 2008, large established community |
| Structure | 2 | Text-format spots (parseable but not JSON); no REST API |
| Identifiers | 2 | Callsigns as identifiers; frequencies; timestamps |
| Additive Value | 3 | Unique automated HF propagation monitoring — complements PSKReporter |
| **Total** | **15/18** | |

## Notes

- RBN and PSKReporter are complementary: RBN is automated skimmers only; PSKReporter includes self-reporting stations.
- The Telnet interface uses the standard DX Spider cluster protocol — any DX cluster client library will work.
- FT8/FT4 spots have exploded RBN volume since ~2018 due to the popularity of these digital modes.
- Skimmer locations (grid squares) are known, making it possible to compute propagation path geometry.
- For a REST-based alternative, PSKReporter's MQTT/WebSocket endpoint may be preferable.
- Pairs with WSPRnet for calibrated propagation measurement, and DSCOVR/SWPC for space weather correlation.
