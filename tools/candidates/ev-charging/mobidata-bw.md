# MobiData BW E-Ladesäulen

**Country/Region**: Germany — Baden-Württemberg
**Publisher**: MobiData BW
**NAP / Catalog**: https://mobilithek.info/offers/-2035239451501556619
**Public Endpoints**:
- https://api.mobidata-bw.de/ocpdb/api/public/v1/sources
- https://api.mobidata-bw.de/ocpdb/api/public/datex/v3.5/json/realtime
- https://api.mobidata-bw.de/ocpdb/api/ocpi/3.0/evses?limit=1
**Documentation**:
- https://api.mobidata-bw.de/ocpdb/documentation/public.html#/
- https://www.mobidata-bw.de/data/MobiData-BW-Factsheet-Ladesaeulendaten.pdf
**Protocol**: HTTPS pull
**Auth**: None observed during probe
**Data Format**: DATEX II v3.5 JSON realtime, OCPI 3.0 JSON, CSV/WFS export
**Real-Time Status**: Yes — observed `status.value` entries include `available`, `charging`, and `outOfOrder`
**Update Frequency**: Near-real-time; public source inventory and DATEX publication timestamps updated on 2026-04-08 during probe
**License**: Open-data publication on Mobilithek; attribution and licence details vary by integrated source

## What It Provides

MobiData BW publishes a bundled Baden-Württemberg charging dataset on Mobilithek.
The offer explicitly combines the Bundesnetzagentur register with AFIR-mandated
static and dynamic data from integrated providers.

During this probe, the public source inventory listed 10 integrated sources:
- Bundesnetzagentur
- Albwerk
- EnBW Datex II
- Heilbronn Neckarbogen
- OpenData Swiss
- PBW
- Stadtwerke Ludwigsburg
- Stadtwerke Pforzheim
- Stadtwerke Stuttgart
- Stadtwerke Tübingen

The same public inventory showed realtime `ACTIVE` for nine provider feeds and
realtime `PROVISIONED` for the Bundesnetzagentur component.

## API Details

The strongest live-status evidence is the public DATEX endpoint:

```text
GET https://api.mobidata-bw.de/ocpdb/api/public/datex/v3.5/json/realtime
```

During the probe, it returned an `aegiEnergyInfrastructureStatusPublication` with:
- `publicationTime` timestamps from the current minute
- `energyInfrastructureSiteStatus[]`
- nested `refillPointStatus[]`
- per-refill-point `status.value` values including `available`, `charging`, and `outOfOrder`
- stable refill-point identifiers such as `DE*STR*E10002*001`

The public OCPI documentation also exposes unauthenticated endpoints for:
- locations
- charge stations
- EVSEs
- connectors
- businesses

The public source inventory endpoint is useful operationally because it shows which
integrated providers currently have active static and realtime ingestion.

## Freshness Assessment

This is a genuine live-status source. The public `sources` endpoint exposed same-day
`realtime_data_updated_at` timestamps, and the DATEX realtime publication returned
current-minute `publicationTime` and `lastUpdated` values during the probe.

The main limitation is scope, not freshness. This is a Baden-Württemberg aggregation,
not yet a proven nationwide German live-status feed.

## Entity Model

- **Energy Infrastructure Site**: site-level publication object in DATEX
- **Station / Charge Station**: grouped charging infrastructure at one location
- **Refill Point / EVSE**: live status entity keyed by stable EVSE-style identifier
- **Connector**: OCPI connector records with power and format details
- **Source**: upstream provider inventory record with static and realtime ingestion state

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Live DATEX publication and same-day realtime source timestamps were observed directly |
| Openness | 2 | Public unauthenticated endpoints, but attribution and licence terms vary across integrated sources |
| Stability | 3 | Official regional mobility data platform published on Germany's national access point |
| Structure | 3 | Documented DATEX realtime and OCPI 3.0 endpoints |
| Identifiers | 3 | Stable EVSE-style identifiers are present in the live payload |
| Additive Value | 3 | First confirmed open German live-status feed found on Mobilithek |
| **Total** | **17/18** | |

## Notes

- This is the strongest currently confirmed German open-data source for live charging-point status.
- Bundesnetzagentur remains important as the wider national baseline, but MobiData BW is the better bridge target when actual live state matters.
- The provider mix is still evolving, so this source is best treated as a high-value regional live feed rather than full Germany-wide coverage.