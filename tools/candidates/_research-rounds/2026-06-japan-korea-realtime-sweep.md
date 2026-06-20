# Asia Real-Time Sweep — Japan & South Korea (corrected)

Research conducted: 2026-06-20

Follow-on to the SG/HK/TW sweep. Targeted verification of Japan and South Korea.

> **Correction note.** This sweep initially mis-promoted JMA's disaster/seismic
> feeds as an 18/18 "gap". They are in fact **already implemented** as feeders
> **and listed in `catalog.json`**. The error was a **faulty correlation grep**,
> not stale data: a PowerShell `Select-String -SimpleMatch` call with a
> `jma|bosai|…` alternation pattern silently matched nothing, because
> `-SimpleMatch` disables regex and searched for the literal string with pipes.
> `catalog.json` actually lists every JMA source. The withdrawn candidate note
> (`disaster-alerts/japan-jma-disaster.md`) has been deleted; this note reflects
> reality.

## Authoritative correlation source

Both `feeders/` and the root `catalog.json` are authoritative and **in sync** —
verified: identical 109-id sets, including all seven Japanese feeders below. The
earlier "stale catalog" conclusion was **wrong**; it came from a broken grep
(`Select-String -SimpleMatch` over a `a|b|c` alternation), not missing data.
Correlate by parsing `catalog.json` with `ConvertFrom-Json` (or listing
`feeders/`) — never with `Select-String -SimpleMatch` on a pipe-alternation.

## Japan — already implemented (7 feeders)

| Feeder | Domain / coverage |
|---|---|
| `feeders/jma-japan` | JMA weather bulletins, warnings, forecasts |
| `feeders/jma-bosai-quake` | Earthquake bulletins — hypocenter, magnitude, JMA intensity |
| `feeders/jma-bosai-warning` | Per-prefecture weather warnings **+ tsunami alerts** |
| `feeders/jma-bosai-volcano` | 111 volcanoes — alert levels, eruption observations |
| `feeders/jma-bosai-amedas` | ~1,300 AMeDAS stations, 10-min observations (Bosai JSON) |
| `feeders/tepco-denkiyoho` | TEPCO electricity demand/forecast (電気予報) |
| `feeders/tokyo-docomo-bikeshare` | Tokyo Docomo bikeshare station availability |

Japan's seismic / tsunami / volcano / weather-warning / weather-observation
core is **done** — and pulls from exactly the keyless Bosai JSON endpoints
probed during this sweep (`bosai/quake/data/list.json`, `bosai/.../area.json`,
the `developer/xml/feed/*.xml` Atom feeds).

## Japan — existing candidate notes still un-implemented (gaps)

These were scouted previously and remain valid build candidates (no feeder
exists for any of them):

| Note | Domain | Status |
|---|---|---|
| `transit/odpt-japan.md` | ODPT rail/bus real-time | gap (free key) |
| `tidal-sea-level/jma-tidal.md` | JMA tide-gauge observations | gap (distinct from tsunami warnings in `jma-bosai-warning`) |
| `radiation/japan-nra.md` | NRA radiation monitoring | gap |
| `air-quality/japan-soramame.md` | Soramame (そらまめ君) AQ | gap |
| `reservoir-dam/japan-mlit-dams.md` | MLIT dam/reservoir storage | gap |
| `energy/occto-japan.md` | OCCTO grid-wide electricity | gap (TEPCO-only is covered by `tepco-denkiyoho`) |

No **net-new** Japan gap surfaced this round — the disaster core was already
built, and the remaining domains were already noted.

## South Korea — nothing implemented (the real opportunity)

There is **no Korean feeder** in `feeders/`. All eight existing Korea candidate
notes are valid, unbuilt build candidates:

`weather/kma-south-korea.md` · `air-quality/south-korea-airkorea.md` (+ `-context`) ·
`hydrology/south-korea-kwater.md` · `transit/seoul-topis.md` ·
`bikeshare-gbfs/seoul-ddareungi.md` · `radiation/kins-iernet-korea.md` ·
`ev-charging/korea-environment-corporation.md`

Most are **key-gated but free** (KMA apihub returned 401 without a key);
AirKorea and the Seoul feeds are the highest-value real-time targets.

## Live-probe results (2026-06-20)

| Endpoint | Result | Meaning |
|---|---|---|
| JMA `developer/xml/feed/{eqvol,extra,regular,other}.xml` | 200 live, current to the minute | Already consumed by `jma-*` feeders |
| JMA `bosai/quake/data/list.json` | 200 live, 157 KB, events keyed by `eid` | Already consumed by `jma-bosai-quake` |
| JMA `bosai/common/const/area.json` | 200 live, 262 KB reference | Already consumed by JMA feeders |
| KMA `apihub.kma.go.kr/.../eqk_now.php` | 401 | Real-time but key-gated; **not implemented** |

## Verdict

Japan is **deeply covered** — its flagship JMA disaster/seismic/volcano/weather
stack plus TEPCO electricity and Tokyo bikeshare are already implemented; the
only remaining Japan gaps (ODPT transit, JMA tide gauges, NRA radiation,
Soramame AQ, MLIT dams, OCCTO grid) were already on the candidate list and are
not net-new. **South Korea is the genuine unimplemented opportunity** in
Northeast Asia — eight scouted candidates, none built, AirKorea + Seoul feeds
the standouts. With SG/HK/TW and JP/KR now reconciled against `feeders/`, the
next greenfield is **Southeast Asia** (Malaysia `data.gov.my`, Indonesia/BMKG,
Thailand, Vietnam) and **India** beyond NDMA SACHET (IMD, CWC/WRIS).
