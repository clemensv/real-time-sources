# ETHZ Swiss Seismological Service (SED)

## Source Identity

| Field            | Value |
|------------------|-------|
| **Full Name**    | Swiss Seismological Service (SED) at ETH Zürich |
| **Operator**     | ETH Zürich, Department of Earth Sciences |
| **URL**          | https://www.seismo.ethz.ch/ |
| **API Base**     | `http://eida.ethz.ch/fdsnws/event/1/` |
| **Coverage**     | Switzerland, greater Alpine region, and global (M4+) |
| **Update Freq.** | Near-real-time; automatic locations within minutes |

## What It Does

SED is Switzerland's official earthquake monitoring service, operating a dense network of seismographs across the Alps. The FDSN event web service provides standard text, QuakeML, and JSON output for earthquake catalog queries. Switzerland sits on an active plate boundary zone between the European and African plates — not headline-grabbing, but seismically interesting. The Basel 1356 earthquake was one of Europe's most destructive.

SED is a primary node on the European Integrated Data Archive (EIDA), the federated European seismic data infrastructure.

## Endpoints Verified

| Endpoint | Status | Notes |
|----------|--------|-------|
| `/query?limit=5&format=text&orderby=time` | ✅ 200 | Standard FDSN text output |
| `/query?format=text&minmagnitude=3` | ✅ Documented | Filter by magnitude |
| `/query?format=xml` | ✅ Documented | QuakeML XML output |

### Sample Response (FDSN text, trimmed)

```
#EventID|Time|Latitude|Longitude|Depth/km|Author|Catalog|Contributor|ContributorID|MagType|Magnitude|MagAuthor|EventLocationName|EventType
smi:ch.ethz.sed/sc25a/Event/2026gsnkqo|2026-04-06T01:43:18.625898|45.688|7.021|5.29|toni@sc25ag||SED|...|MLhc|1.49|toni@sc25ag|Courmayeur I|earthquake
```

## Authentication & Licensing

- **Auth**: None. Anonymous access.
- **Rate Limits**: Not explicitly stated; standard FDSN etiquette applies.
- **License**: SED data policy — freely available for research and public use with attribution.

## Integration Notes

Standard FDSN event service — identical query parameters and response format to EMSC, GFZ, INGV. The generic FDSN bridge adapter would work here by changing the base URL. Event IDs use `smi:ch.ethz.sed/` URN scheme. Magnitude type is `MLhc` (local magnitude, horizontal component). The `EventType` field distinguishes earthquakes from blasts and other event types — useful for filtering.

The service contributes to EIDA and EMSC, so many events will appear in those aggregators too. The value here is authoritative Swiss/Alpine detail and lower-magnitude events that don't make the global catalogs.

## Feasibility Rating

| Dimension                    | Score | Notes |
|------------------------------|-------|-------|
| **API Maturity & Docs**      | 3     | FDSN standard; well-documented |
| **Data Freshness**           | 2     | Near-real-time but poll-only |
| **Format / Schema Quality**  | 3     | FDSN text/QuakeML — standardized |
| **Auth / Access Simplicity** | 3     | Anonymous, open |
| **Coverage Relevance**       | 2     | Alpine region; moderate seismicity |
| **Operational Reliability**  | 3     | ETH Zürich — premier research university; long track record |
| **Total**                    | **16 / 18** | |

## Verdict

✅ **Build** — as a target for the generic FDSN adapter. Zero additional parsing needed beyond what GFZ and INGV already require. Switzerland's Alpine seismicity provides European coverage that complements INGV (Italy) and GFZ (global). The real win is proving the FDSN adapter pattern works across yet another node.
