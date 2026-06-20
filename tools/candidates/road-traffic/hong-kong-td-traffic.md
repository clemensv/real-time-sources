# Hong Kong Transport Department — Real-Time Road Traffic

**Country/Region**: Hong Kong SAR, China
**Publisher**: Transport Department (TD), HKSAR Government, via DATA.GOV.HK
**API Endpoints**:
- Speed/volume/occupancy (strategic + major roads): `https://resource.data.one.gov.hk/td/traffic-detectors/rawSpeedVol-all.xml`
- Detector locations (reference): `https://static.data.gov.hk/td/traffic-detectors/...` (detector lat/lon + road segment)
- Plus the wider TD real-time family on DATA.GOV.HK: journey-time indicators, traffic snapshot images (CCTV), special traffic news
**Schema**: `https://static.data.gov.hk/td/traffic-data-strategic-major-roads/info/SpeedVolOcc-BR.xsd`
**Documentation**: https://data.gov.hk/en-data/dataset/ (search "traffic")
**Protocol**: REST (HTTP file polling) — XML
**Auth**: None — fully open, no API key
**Data Format**: XML (XSD-defined)
**Update Frequency**: Real-time — **30-second** aggregation periods
**License**: Hong Kong Government Open Data License
**Score**: 16/18

## What It Provides

Hong Kong's Transport Department publishes live **road-network detector data** —
speed, traffic volume, and occupancy per detector on the strategic and major
road network — at a 30-second cadence, keyless. This is distinct from the
already-noted HK **transit** ETAs (KMB/MTR/Citybus in `transit/hk-transit.md`):
this is vehicular road traffic, a domain with no Hong Kong entry yet.

Verified live: `rawSpeedVol-all.xml` returned 537 KB with
`<date>2026-06-20</date>` and consecutive 30-second periods
(`<period_from>14:46:00</period_from><period_to>14:46:30</period_to>`), each
carrying a `<detectors>` list. The payload validates against the published
`SpeedVolOcc-BR.xsd`.

The broader TD real-time dataset family on DATA.GOV.HK includes:
- **Traffic speed map** — colour-banded speed per road segment
- **Journey-time indicators** — estimated travel time between major points
- **Traffic snapshot images** — CCTV stills refreshed every ~2 minutes
- **Special traffic news** — incident/roadworks bulletins

## API Details

```
GET https://resource.data.one.gov.hk/td/traffic-detectors/rawSpeedVol-all.xml
```
Returns (per 30-second period, per detector):
- `period_from` / `period_to` — 30-second window bounds
- detector ID
- `speed` (km/h), `volume` (vehicles), `occupancy` (%) — typically split by
  lane / vehicle-length class as defined in `SpeedVolOcc-BR.xsd`

Detector IDs join to a static **detector-location** reference (lat/lon + road
segment), so each reading is geo-locatable and stably keyable.

## Freshness Assessment

Excellent — 30-second aggregation windows are among the highest road-traffic
cadences of any open feed in the repo's candidate set (faster than NDW's
per-minute or National Highways' aggregated counts). The feed is a rolling
file refreshed continuously by the TD detector network.

## Entity Model

- **Detector**: stable TD detector ID, location (via reference file), road segment
- **Measurement**: 30-second window with speed / volume / occupancy (per lane/class)
- **Key**: detector ID (subject + Kafka key); subject `{detector_id}`

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 30-second detector windows — exceptional cadence |
| Openness | 3 | No auth, keyless, open government data license |
| Stability | 3 | Official Transport Department feed; versioned XSD on static.data.gov.hk |
| Structure | 2 | XML with a published XSD; needs parsing + lane/class flattening |
| Identifiers | 2 | Stable detector IDs, but location requires a reference-file join (HK-specific) |
| Additive Value | 3 | New region + new domain for HK; rare 30s cadence; complements HK transit ETAs |
| **Total** | **16/18** | |

## Notes

- **Found in the 2026-06 Asia (SG/HK/TW) real-time sweep.** HK weather
  (`hko-hong-kong`) and AQHI (`hongkong-epd`) are already implemented, and HK
  transit ETAs are already a candidate — but HK **road traffic** was a gap.
- The detector feed pairs naturally with a small reference-data emit (detector
  locations) at startup, then 30-second telemetry — the standard reference +
  telemetry pattern used across this repo.
- The wider TD family (journey times, speed map, CCTV, special traffic news)
  could be folded into a single Hong Kong TD road-traffic bridge as additional
  event types, mirroring how other multi-feed road sources are structured.
- Trilingual labels (EN/TC/SC) appear throughout DATA.GOV.HK transport
  datasets, consistent with the HK transit note.
