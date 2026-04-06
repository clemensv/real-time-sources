# JMA — Japan Meteorological Agency (Earthquake and Tsunami)

## Source Identity

| Field            | Value |
|------------------|-------|
| **Full Name**    | Japan Meteorological Agency — Earthquake and Tsunami Information |
| **Operator**     | 気象庁 / Japan Meteorological Agency, Ministry of Land, Infrastructure, Transport and Tourism |
| **URL**          | https://www.jma.go.jp/bosai/quake/ |
| **API Base**     | `https://www.jma.go.jp/bosai/quake/data/list.json` |
| **Coverage**     | Japan and surrounding waters |
| **Update Freq.** | Near-real-time; bulletins issued within minutes of felt events |

## What It Does

JMA is the authoritative source for earthquake information in Japan — the most seismically monitored country on Earth. Their dense network of thousands of seismometers and intensity meters detects virtually every earthquake, down to magnitude 1 or less in populated areas.

The `list.json` endpoint returns a JSON array of recent earthquake bulletins. Each entry includes the event time, epicenter location (as a coded string), magnitude, maximum observed seismic intensity (shindō scale), and links to detailed per-event JSON files. The data includes English translations for titles and region names.

Japan's shindō intensity scale (0–7, with subdivisions 5-lower, 5-upper, 6-lower, 6-upper) is distinct from MMI and is included in the response. The per-city intensity breakdown is remarkably detailed — individual municipalities are listed with their observed intensity.

## Endpoints Verified

| Endpoint | Status | Notes |
|----------|--------|-------|
| `/bosai/quake/data/list.json` | ✅ 200 | JSON array of earthquake bulletins |
| `/bosai/quake/data/{json}` | ✅ Expected | Individual event detail (referenced in list) |

### Sample JSON Response (trimmed, Unicode decoded)

```json
[
  {
    "ctt": "20260406155029",
    "eid": "20260406154529",
    "rdt": "2026-04-06T15:50:00+09:00",
    "ttl": "震源・震度情報",
    "at": "2026-04-06T15:45:00+09:00",
    "anm": "南海道南方沖",
    "mag": "4.6",
    "maxi": "1",
    "en_ttl": "Earthquake and Seismic Intensity Information",
    "en_anm": "Off the south Coast of Nankaido",
    "cod": "+32.0+135.9-10000/",
    "int": [{"code": "30", "maxi": "1", "city": [{"code": "3020400", "maxi": "1"}]}],
    "json": "20260406155029_20260406154529_VXSE5k_1.json"
  }
]
```

## Authentication & Licensing

- **Auth**: None. Anonymous access.
- **Rate Limits**: Not documented; this is a public government service.
- **License**: Japanese government public data. Open for use; attribution expected. JMA data is used by virtually every earthquake app in Japan.

## Integration Notes

The JSON schema is compact and uses abbreviated field names: `ctt` (content time), `eid` (event ID), `rdt` (report datetime), `at` (origin time), `anm` (area name), `mag` (magnitude), `maxi` (max intensity), `cod` (coordinates encoded as string), `int` (intensity distribution array).

The `cod` field encodes latitude/longitude/depth as a string (e.g., `+32.0+135.9-10000/` means 32.0°N, 135.9°E, 10 km depth). Needs parsing.

The `int` array provides intensity observations by prefecture and city — extremely granular. The `json` field references a detail file for full event information.

Primary content is in Japanese (`ttl`, `anm`) with English translations available (`en_ttl`, `en_anm`). The English region names use JMA's own naming convention.

Polling the `list.json` endpoint periodically and tracking by `eid` would work. The list appears to include the most recent ~50 bulletins.

No streaming/push endpoint is available through this public API. Japan does have a real-time earthquake early warning system, but that's a separate broadcast infrastructure not exposed via REST.

## Feasibility Rating

| Dimension                    | Score | Notes |
|------------------------------|-------|-------|
| **API Maturity & Docs**      | 2     | Works well but minimal English documentation; abbreviated field names |
| **Data Freshness**           | 2     | Near-real-time polling; no push/WebSocket |
| **Format / Schema Quality**  | 2     | Compact JSON but needs custom parsing (encoded coords, abbreviated keys) |
| **Auth / Access Simplicity** | 3     | Anonymous, open |
| **Coverage Relevance**       | 3     | Japan — world's most densely monitored seismic zone; Pacific Ring of Fire |
| **Operational Reliability**  | 3     | National meteorological agency; mission-critical infrastructure |
| **Total**                    | **15 / 18** | |

## Verdict

Japan is *the* seismically monitored country, and JMA data is uniquely detailed with per-municipality intensity observations you won't find anywhere else. The custom JSON schema requires more parsing work than FDSN sources, but the data richness justifies it. The shindō intensity scale adds a dimension that MMI-based sources don't provide. Worth building for anyone interested in Japanese or Pacific Rim seismicity. Moderate integration effort.
