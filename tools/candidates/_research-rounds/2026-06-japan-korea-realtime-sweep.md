# Asia Real-Time Sweep — Japan & South Korea

Research conducted: 2026-06-20

Follow-on to the SG/HK/TW sweep. Targeted verification of the two most
instrumented real-time ecosystems in Northeast Asia: **Japan** and
**South Korea**. As with SG/HK/TW, the method was direct live-probing of the
known national real-time API families, reconciled against `catalog.json`
(implemented) and existing candidate notes (already scouted).

Headline result: both countries are **already heavily scouted** (6 Japan
notes, 8 Korea notes), but neither had its **flagship disaster/seismic feed**
captured. The net-new finding is **Japan's JMA Disaster Prevention XML** — a
keyless, best-in-class multi-hazard feed.

## Already implemented (catalog.json)

None. No Japan or Korea source is implemented yet — both are entirely at the
candidate-note stage.

## Already scouted (existing candidate notes)

**Japan (6):**
| Note | Domain |
|---|---|
| `transit/odpt-japan.md` | ODPT public-transport open data (rail/bus real-time; free key) |
| `tidal-sea-level/jma-tidal.md` | JMA tide-gauge observations |
| `radiation/japan-nra.md` | NRA radiation monitoring network |
| `air-quality/japan-soramame.md` | Soramame (そらまめ君) air quality |
| `reservoir-dam/japan-mlit-dams.md` | MLIT dam / reservoir storage |
| `energy/occto-japan.md` | OCCTO grid / electricity |

**South Korea (8):**
| Note | Domain |
|---|---|
| `weather/kma-south-korea.md` | KMA API Hub — weather + earthquake/volcano + typhoon (key) |
| `air-quality/south-korea-airkorea.md` (+ `-context`) | AirKorea real-time AQI |
| `hydrology/south-korea-kwater.md` | K-water river / reservoir |
| `transit/seoul-topis.md` | Seoul TOPIS traffic/transit |
| `bikeshare-gbfs/seoul-ddareungi.md` | Ddareungi (따릉이) bikeshare |
| `radiation/kins-iernet-korea.md` | KINS IERNet radiation |
| `ev-charging/korea-environment-corporation.md` | EV charging status |

## Live-probe results (2026-06-20)

| Endpoint | Result |
|---|---|
| **JMA `developer/xml/feed/eqvol.xml`** (earthquake/volcano Atom) | **200 live** — `<updated>2026-06-20T14:01:03+09:00</updated>`, 19 KB |
| **JMA `developer/xml/feed/extra.xml`** (warnings, as-needed) | **200 live** — `2026-06-20T16:05:03+09:00`, 208 KB |
| **JMA `developer/xml/feed/regular.xml`** (scheduled) | **200 live** — 高頻度（定時）, 240 KB |
| **JMA `developer/xml/feed/other.xml`** | **200 live** — 高頻度（その他）, 19 KB |
| **JMA `bosai/quake/data/list.json`** | **200 live** — 157 KB; events keyed by `eid` (e.g. `20260620053914`), 震源・震度情報 |
| **JMA `bosai/common/const/area.json`** | **200 live** — 262 KB area-code reference (centers/offices/regions) |
| KMA `apihub.kma.go.kr/.../eqk_now.php` (earthquake, no key) | **401** — real-time but **key-gated** |

## The one new gap → promoted

| Candidate | Country | Why it's new |
|---|---|---|
| **[JMA Disaster Prevention XML](../disaster-alerts/japan-jma-disaster.md) (18/18)** | Japan | Japan had tidal/radiation/dams/AQ/transit/energy noted — but **not** the JMA 防災情報XML. There was **no Japan entry in either the seismology or disaster-alerts index**. The feed is keyless (Atom + bosai JSON), multi-hazard (earthquake/EEW + tsunami + volcano + weather warnings), with EEW issued in seconds. Promoted to a full note + disaster-alerts and seismology INDEX rows. |

This is a flagship — arguably one of the best open real-time disaster feeds in
the world. Note the contrast the seismology index already records: **US
ShakeAlert EEW is not publicly accessible**, whereas Japan's EEW is keyless.

## Open threads (verify-next, not promoted)

- **Korea KMA earthquake/tsunami** — real-time but **key-gated**
  (`apihub.kma.go.kr` → 401). Already documented as a category inside
  `weather/kma-south-korea.md`. Could be split into a dedicated seismology
  note if/when a bridge is built, but it adds no keyless coverage.
- **Japan MLIT river water levels** (川の防災情報) — the hydrology white-spot
  lists "Japan (MLIT water info)"; `reservoir-dam/japan-mlit-dams.md` covers
  dams, but real-time *river gauge* coverage may be a separate endpoint worth
  dedicated discovery.
- **Seoul real-time city data** (`data.seoul.go.kr` 도시데이터 / citydata) —
  real-time population/road/parking per district, but key-gated; lower priority
  given Seoul TOPIS + Ddareungi already noted.

## Verdict

Japan and Korea are **largely exhausted** as discovery targets — both are
deeply instrumented and were already well scouted across weather, air quality,
hydrology, transit, radiation, and energy. This pass added one top-tier source
(**JMA Disaster XML, 18/18**) and left three narrow verify-next threads (KMA EQ
key-gated, MLIT river, Seoul citydata). With SG/HK/TW and JP/KR now swept, the
remaining higher-yield *unscouted* Asian targets are the road-traffic- and
disaster-immature but transit-rich **Southeast Asian** portals — Malaysia
(`data.gov.my`), Indonesia (BMKG beyond seismic; Jakarta), Thailand, Vietnam —
and **India** beyond NDMA SACHET (IMD weather, CWC/WRIS hydrology).
