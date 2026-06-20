# JMA Disaster Prevention Information XML — Japan (Earthquake / Tsunami / Volcano / Weather Warnings)

**Country/Region**: Japan
**Publisher**: Japan Meteorological Agency (JMA / 気象庁)
**API Endpoints**:
- Atom publishing feeds (気象庁防災情報XML): `https://www.data.jma.go.jp/developer/xml/feed/{regular,extra,eqvol,other}.xml`
- Earthquake list (bosai JSON): `https://www.jma.go.jp/bosai/quake/data/list.json`
- Per-event detail: `https://www.jma.go.jp/bosai/quake/data/{eid}.json`
- Area reference (centers/offices/regions): `https://www.jma.go.jp/bosai/common/const/area.json`
**Documentation**: https://xml.kishou.go.jp/ (JMAXML format spec); https://www.data.jma.go.jp/developer/index.html (feed list, Japanese)
**Protocol**: REST (HTTP polling) — Atom 1.0 feeds linking to JMAXML documents; plus bosai JSON
**Auth**: None — fully keyless
**Data Format**: XML (JMAXML / 気象庁防災情報XMLフォーマット) + JSON (bosai)
**Update Frequency**: Real-time — EEW within seconds; earthquake/tsunami bulletins within 1–3 minutes; warning feeds refreshed continuously (feeds observed updated to the current minute)
**License**: Government of Japan open data (free for commercial and non-commercial use with attribution)
**Score**: 18/18

## What It Provides

JMA's **防災情報XML (Disaster Prevention Information XML)** is the official,
keyless, machine-readable channel for one of the most seismically and
meteorologically active nations on earth. It is multi-hazard:

- **Earthquake** — hypocenter & seismic-intensity reports (震源・震度情報),
  intensity bulletins (震度速報), and Earthquake Early Warning (緊急地震速報/EEW)
- **Tsunami** — tsunami warnings/advisories (津波警報・注意報) and observed/
  forecast tsunami information (津波情報)
- **Volcano** — eruption warnings/forecasts (噴火警報・予報), ashfall forecasts
- **Weather** — weather warnings & advisories (気象警報・注意報), heavy-rain /
  flood / storm bulletins, typhoon information

Verified live (2026-06-20): all four publishing feeds returned HTTP 200 with
`<updated>` timestamps at the current minute —
`eqvol.xml` (高頻度・地震火山, 19 KB), `extra.xml` (高頻度・随時, 208 KB),
`regular.xml` (高頻度・定時, 240 KB), `other.xml` (高頻度・その他, 19 KB).
The bosai earthquake list `list.json` returned 157 KB of recent events, each
with a stable `eid` (e.g. `"eid":"20260620053914"`, title 震源・震度情報) and
`rdt` report time. `area.json` returned 262 KB of center/office/region
reference definitions.

## API Details

**Atom feed pattern (the canonical, documented channel):**
```
GET https://www.data.jma.go.jp/developer/xml/feed/eqvol.xml      # earthquake + volcano
GET https://www.data.jma.go.jp/developer/xml/feed/extra.xml      # warnings (as-needed)
GET https://www.data.jma.go.jp/developer/xml/feed/regular.xml    # scheduled bulletins
GET https://www.data.jma.go.jp/developer/xml/feed/other.xml      # other
```
Each Atom `<entry>` carries `<id>` (the JMAXML document URL), `<updated>`,
`<title>` (bulletin type in Japanese), and a `<link>` to the full JMAXML
document. Poll the feed, diff on entry `<id>`, fetch new documents. (JMA also
operates a PubSubHubbub/WebSub push hub for low-latency delivery — a future
upgrade path beyond polling.)

**bosai JSON (lighter, website-backing channel):**
```
GET https://www.jma.go.jp/bosai/quake/data/list.json   # recent quake events
GET https://www.jma.go.jp/bosai/quake/data/{eid}.json  # one event's full detail
```
`list.json` fields: `eid` (event ID — stable key), `rdt` (report datetime),
`ttl` (bulletin title), `ift` (発表/announcement), `ser` (serial), `at` (event
time), `anm` (epicenter area name), plus magnitude / max-intensity fields.

## Freshness Assessment

Best-in-class. EEW (緊急地震速報) is issued within seconds of P-wave detection;
hypocenter/intensity reports follow within 1–3 minutes; tsunami warnings are
issued within ~3 minutes of a major offshore quake. The warning feeds refresh
continuously and were observed current to the minute.

## Entity Model

- **Event** (earthquake / tsunami / volcano / warning) — keyed by JMAXML
  document ID or bosai `eid` (subject + Kafka key)
- **Area** — JMA area codes (forecast region / city / observation point) for
  intensity, warnings, and tsunami zones; defined in `area.json` (reference data)
- **Reference-data emit**: `area.json` (centers → offices → regions → cities)
  emitted at startup, then event telemetry — the repo's reference + telemetry
  pattern fits cleanly.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | EEW in seconds; quake/tsunami bulletins in 1–3 min; warning feeds continuous |
| Openness | 3 | No auth, keyless, officially published developer feeds |
| Stability | 3 | Official JMAXML format with a public spec (xml.kishou.go.jp); Atom standard; long-running |
| Structure | 3 | Well-specified JMAXML schema + clean bosai JSON; stable element model |
| Identifiers | 3 | Document IDs / `eid` event IDs + JMA area codes; `area.json` reference; ideal keys |
| Additive Value | 3 | Flagship multi-hazard feed for the most seismically active major nation; new region + first Japan entry in disaster-alerts/seismology |
| **Total** | **18/18** | |

## Notes

- **Found in the 2026-06 Japan/Korea real-time sweep.** Japan had tidal
  (`tidal-sea-level/jma-tidal.md`), radiation (`radiation/japan-nra.md`),
  dams, air quality, transit (ODPT), and energy notes — but **no JMA disaster
  feed**, and there is **no Japan entry in either the seismology or
  disaster-alerts index**. This is the single highest-value Japan gap.
- Multi-hazard scope means this could be modeled as one message group with
  several event types (earthquake, tsunami, volcano, weather-warning), each
  keyed by event ID, sharing the JMA area-code reference — analogous to how
  multi-family pollers (`dwd`, `entsoe`) are structured in this repo.
- The JMAXML documents are richly structured but **Japanese-labeled**; the
  bridge should carry both the original Japanese and the documented English
  control vocabularies (intensity scale, warning kinds) where JMA publishes
  them. JMA also provides English EEW/tsunami summaries via the bosai layer.
- **Push upgrade path**: JMA runs a WebSub (PubSubHubbub) hub for the XML
  feeds, enabling near-zero-latency delivery instead of polling — worth using
  for EEW/tsunami once the polling bridge is proven.
- Complements `seismology/usgs-earthquakes` (implemented) and
  `seismology/bmkg-indonesia` / `phivolcs-philippines` candidates by adding the
  Japan arc — and adds tsunami + volcano + weather-warning hazards that the
  pure-seismology FDSN sources do not carry.
