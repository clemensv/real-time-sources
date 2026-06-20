# Asia Real-Time Sweep — Singapore, Hong Kong, Taiwan

Research conducted: 2026-06-20

Targeted verification pass over the three most mature real-time open-data
ecosystems in Asia: **Singapore**, **Hong Kong**, and **Taiwan**. Unlike the
`data.europa.eu` rounds, these countries don't share one faceted catalog —
each runs its own platform — so this pass worked by **direct live-probing the
known real-time API families** and reconciling them against what's already
implemented (`catalog.json`) and already scouted (candidate notes).

The headline result: **these three are already well-covered**. The net-new
finding is a single genuine gap — Hong Kong **road traffic**.

## Already implemented (catalog.json)

| Source | Country | Coverage |
|---|---|---|
| `singapore-nea` | SG | 62 weather stations + 5 air-quality regions (data.gov.sg real-time API) |
| `hko-hong-kong` | HK | 27 temperature stations, 18 rainfall districts (HKO) |
| `hongkong-epd` | HK | 18 AQHI stations, hourly health index |

## Already scouted (existing candidate notes)

| Note | Country | Score | Domain |
|---|---|---|---|
| `transit/singapore-lta.md` | SG | 14/18 | LTA DataMall — bus arrivals (with crowding), positions, train alerts, taxi |
| `road-traffic/singapore-lta-traffic.md` | SG | 17/18 | LTA — speed bands, incidents, images, travel times, VMS, carpark |
| `parking/singapore-lta-carparks.md` | SG | 17/18 | LTA carpark availability |
| `transit/hk-transit.md` | HK | 14/18 | KMB / MTR / Citybus real-time ETAs (keyless) |
| `transit/taiwan-tdx.md` | TW | 16/18 | TDX — rail/metro/bus/ferry/bikeshare/aviation real-time |
| `weather/cwa-taiwan.md` | TW | 17/18 | CWA — observations, forecasts, **earthquake**, typhoon, radar, tide |
| `air-quality/taiwan-moenv.md` | TW | — | MOENV real-time AQI |
| `hydrology/taiwan-wra.md` | TW | 14/18 | WRA water-level stations + reservoir daily + rain |
| `bikeshare-gbfs/taipei-youbike.md` | TW | — | YouBike 2.0 real-time station availability |

## Live-probe results (2026-06-20)

| Endpoint | Result |
|---|---|
| HK KMB route list `data.etabus.gov.hk/v1/transport/kmb/route/` | **200 live** — `generated_timestamp 2026-06-20T14:53:47+08:00`, trilingual (confirms `hk-transit.md`) |
| **HK TD traffic `resource.data.one.gov.hk/td/traffic-detectors/rawSpeedVol-all.xml`** | **200 live — 30-second detector speed/volume/occupancy**, 537 KB, XSD-validated. **New gap.** |
| TW YouBike 2.0 Taipei `tcgbusfs.blob.core.windows.net/.../youbike_immediate.json` | **200 live** — `updateTime 2026-06-20 14:52:52` (confirms `taipei-youbike.md`) |
| TW CWA earthquake `opendata.cwa.gov.tw/.../E-A0015-001` | 401 without key — endpoint live, free key required (confirms `cwa-taiwan.md`) |
| TW MOENV AQI `data.moenv.gov.tw/api/v2/aqx_p_432` | 500 without proper `api_key` — endpoint live, key required |
| SG data.gov.sg v2 `real-time/api/carpark-availability` | 403 from this host (UA/IP block) — SG carpark is covered anyway via LTA |
| TW Freeway Bureau `tisvcloud.freeway.gov.tw/.../VDLive.xml.gz` | Timeout from this network — unconfirmed (see open threads) |

## The one new gap → promoted

| Candidate | Country | Why it's new |
|---|---|---|
| **[Hong Kong TD Traffic](../road-traffic/hong-kong-td-traffic.md) (16/18)** | HK | HK had weather, AQHI, and transit ETAs noted/implemented — but **no road traffic**. The TD detector feed is keyless, XSD-defined, and runs at a **30-second** cadence (faster than most European road feeds). Promoted to a full note + road-traffic INDEX row. |

## Open threads (verify-next, not promoted)

- **Taiwan Freeway Bureau real-time** (`tisvcloud.freeway.gov.tw` — VD vehicle
  detectors, ETag section travel times, CMS): keyless and canonical for TW road
  traffic, but the gzipped live feeds **timed out from this network**. TW has no
  road-traffic INDEX entry; TDX (`taiwan-tdx.md`) is transit-only. If reachable,
  this is a likely second TW candidate — worth a re-probe from a different host.
- **Taiwan WRA real-time water levels**: `taiwan-wra.md` already flags that the
  real-time gauge endpoint (beyond reservoir *daily*) was never discovered. The
  `fhy.wra.gov.tw` portal shows live gauge readings, so a real-time water-level
  endpoint exists — worth dedicated endpoint discovery to lift WRA from 14/18.

## Verdict

**SG / HK / TW are largely exhausted** as discovery targets — they are the most
instrumented, most open real-time ecosystems in Asia and were already well
scouted. This pass added one solid new source (HK road traffic) and left two
narrow verify-next threads (TW freeway, TW WRA real-time gauge). The higher-
yield *unscouted* Asian targets are now elsewhere: **South Korea** (`data.go.kr`,
KMA/AirKorea), **Japan** (JMA earthquake EEW / tsunami XML, MLIT river), and
the road-traffic-immature but transit-rich Southeast Asian portals
(Malaysia `data.gov.my`, Indonesia, Thailand).
