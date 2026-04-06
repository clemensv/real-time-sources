# PSKReporter

**Country/Region**: Global
**Publisher**: Philip Gladstone (N1DQ)
**API Endpoint**: `https://retrieve.pskreporter.info/query` (REST), `wss://retrieve.pskreporter.info/monitor` (WebSocket)
**Documentation**: https://pskreporter.info/pskdev.html
**Protocol**: REST (XML/JSON) + WebSocket (real-time)
**Auth**: None for basic queries; API key for higher rate limits
**Data Format**: XML (default), JSON (via parameter)
**Update Frequency**: Real-time (reports arrive within seconds of reception)
**License**: Free to use; no formal open data license

## What It Provides

PSKReporter is the world's largest real-time HF (high-frequency) radio propagation monitoring network. Amateur radio operators running digital mode software (FT8, FT4, WSPR, JS8Call, PSK31, etc.) automatically report received signals to PSKReporter. Each report contains the callsign of the transmitter and receiver, frequency, mode, signal-to-noise ratio, and the grid locators (Maidenhead) of both stations — effectively creating a real-time map of radio propagation conditions across the entire HF spectrum.

The network processes millions of reception reports per day, with over 100,000 active reporters worldwide.

## API Details

- **REST query**: `https://retrieve.pskreporter.info/query?senderCallsign={call}&receiverCallsign={call}&flowStartSeconds={seconds_ago}&mode={mode}&frange={low}-{high}`
- **WebSocket**: `wss://retrieve.pskreporter.info/monitor` — real-time stream of reception reports
- **Parameters**: `senderCallsign`, `receiverCallsign`, `senderLocator`, `receiverLocator`, `mode` (FT8, FT4, WSPR, etc.), `frange` (frequency range in Hz), `flowStartSeconds` (lookback window), `rronly` (reporters only), `noactive` (exclude active monitoring), `encap` (0=raw, 1=multipart), `callback` (JSONP)
- **Response fields**: `senderCallsign`, `senderLocator`, `senderDXCC` (country), `receiverCallsign`, `receiverLocator`, `receiverDXCC`, `frequency`, `mode`, `sNR` (signal-to-noise), `flowStartSeconds` (timestamp), `senderRegion`, `receiverRegion`
- **Rate limits**: Basic access is rate-limited; API key removes some limits
- **Note**: The API returned 403 during probing — may require specific User-Agent or be temporarily restricted

## Freshness Assessment

PSKReporter is genuinely real-time — reception reports arrive within seconds of the radio signal being decoded. The WebSocket interface provides push-based streaming. The REST API supports lookback windows down to the current minute. During active HF conditions, millions of reports flow through daily. This is one of the freshest crowd-sourced data streams in existence.

## Entity Model

- **Reception Report**: Sender callsign + receiver callsign + frequency + mode + SNR + timestamp
- **Station**: Amateur radio callsign with Maidenhead grid locator and DXCC entity (country)
- **Propagation Path**: Implicit — the sender/receiver pair defines a radio path with distance and bearing
- **Band/Mode**: Frequency in Hz, mode (FT8, WSPR, etc.)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time; WebSocket streaming available |
| Openness | 2 | Free to use; 403 on some queries; rate limits; no formal license |
| Stability | 2 | Single-operator project (Philip Gladstone); running since 2008 |
| Structure | 2 | XML/JSON but inconsistent documentation; WebSocket protocol not fully documented |
| Identifiers | 3 | Amateur callsigns are globally unique identifiers; Maidenhead grid locators |
| Additive Value | 3 | Unique real-time HF propagation data; nothing else like it |
| **Total** | **15/18** | |

## Notes

- PSKReporter is a fascinating real-time data source — it essentially crowd-sources ionospheric propagation measurement using amateur radio.
- The WebSocket endpoint is the most interesting for real-time integration but documentation is limited.
- FT8 mode dominates modern HF amateur radio (~80%+ of reports) and provides standardized signal reports.
- The Maidenhead grid locator system provides ~5 km resolution for station locations.
- DXCC entities (countries) are assigned by callsign prefix, enabling country-level aggregation.
- The single-operator nature is a stability concern, but the service has been reliable for 15+ years.
- Combined with Kp index and solar flux data, PSKReporter data can characterize real-time ionospheric conditions.
