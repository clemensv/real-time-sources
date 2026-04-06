# RESIF — French Seismological and Geodetic Network

## Source Identity

| Field            | Value |
|------------------|-------|
| **Full Name**    | RESIF — Réseau Sismologique et Géodésique Français |
| **Operator**     | EOST (École et Observatoire des Sciences de la Terre), Strasbourg |
| **URL**          | https://www.resif.fr/ |
| **API Base**     | `http://ws.resif.fr/fdsnws/event/1/` |
| **Coverage**     | France, global teleseismic (M5+) |
| **Update Freq.** | Near-real-time; automatic locations within minutes |

## What It Does

RESIF is France's national seismic and geodetic research infrastructure. The FDSN event service at `ws.resif.fr` serves the "Namazu" catalog — a merged view of French regional seismicity and global teleseismic events detected by EOST's network. It's part of the European EIDA federation and an official FDSN data center.

France has moderate seismicity (Pyrenees, Alps, Rhine Graben) plus responsibility for seismic monitoring of overseas territories (Caribbean, Indian Ocean, Pacific), making this a geographically broader source than the name suggests.

## Endpoints Verified

| Endpoint | Status | Notes |
|----------|--------|-------|
| `/query?limit=5&format=text&orderby=time` | ✅ 200 | FDSN text; includes global teleseismic |
| `/query?format=text&minmagnitude=4` | ✅ Documented | Magnitude filtering |
| `/query?format=xml` | ✅ Documented | QuakeML XML |

### Sample Response (FDSN text, trimmed)

```
# EventID | Time | Latitude | Longitude | Depth/km | Author | Catalog | Contributor | ... | MagnitudeType | Magnitude | ...
fr2026tlgkdp|2026-04-06T08:27:48.860653Z|-4.635|153.750|104.6|scautoloc2@wvf01|Namazu|EOSTtele|...|mb|5.05|...
fr2026tlgejj|2026-04-06T07:22:43.185339Z|11.029|124.115|10.0|scautoloc2@wvf01|Namazu|EOSTtele|...|mb|5.08|...
```

## Authentication & Licensing

- **Auth**: None. Anonymous access.
- **Rate Limits**: Standard FDSN etiquette.
- **License**: RESIF data policy — open access with attribution.

## Integration Notes

Another clean FDSN event service — the generic adapter pattern applies directly. Catalog name is "Namazu" (named after the Japanese earthquake catfish — a nice touch). The contributor field distinguishes regional French events ("EOSTlocal") from global teleseismic detections ("EOSTtele"). Event IDs use `fr` prefix.

Note: IPGP (Institut de Physique du Globe de Paris) also runs a separate FDSN node at `ws.ipgp.fr` that serves REVOSIMA data (Mayotte volcanic seismic swarm monitoring). These are distinct institutions with distinct catalogs — RESIF covers mainland France seismicity, IPGP/REVOSIMA covers the Indian Ocean volcanic crisis.

## Feasibility Rating

| Dimension                    | Score | Notes |
|------------------------------|-------|-------|
| **API Maturity & Docs**      | 3     | FDSN standard; EIDA node |
| **Data Freshness**           | 2     | Near-real-time; poll-only |
| **Format / Schema Quality**  | 3     | FDSN text/QuakeML — standardized |
| **Auth / Access Simplicity** | 3     | Anonymous, open |
| **Coverage Relevance**       | 2     | France + global M5+; moderate regional seismicity |
| **Operational Reliability**  | 3     | Government-funded research infrastructure |
| **Total**                    | **16 / 18** | |

## Verdict

✅ **Build** — via the generic FDSN adapter. France is another FDSN node that just works. The global teleseismic component means it picks up large events worldwide, providing a useful cross-reference for USGS/EMSC data. Low incremental effort given the FDSN adapter pattern.
