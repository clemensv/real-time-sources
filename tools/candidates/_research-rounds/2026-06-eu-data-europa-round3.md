# data.europa.eu SPARQL/REST Sweep — Round 3

Research conducted: 2026-06-20

This pass re-ran the `data.europa.eu` discovery workflow from the search
playbook, but deliberately targeted the **seams Round 2 (2026-04-08)
under-sampled**: the greenfield domains (parking occupancy, noise,
EV-charging operator status, reservoir/dam, power outages) queried in their
**native languages**, mined through the portal's live-API formats.

The methodological upgrade this round: instead of trusting fuzzy full-text
relevance, results were filtered on two high-signal portal fields —
`accrual_periodicity` (DCAT update frequency) and `distributions[].format` —
combined with a **title/keyword relevance gate** to kill cross-domain noise
(e.g. the Swiss "real-time popular votes" datasets that flood any query
containing "real-time"). The `1MIN`/`5MIN`/`BIHOURLY`/`HOURLY`/`UPDATE_CONT`
periodicity codes are the cleanest real-time discriminator the portal exposes.

## Strong new leads

| Category | Candidate | Country | Portal finding | Verified endpoint | Assessment |
|---|---|---|---|---|---|
| Parking | **Italian city parking (Firenze + Torino + Bologna)** | Italy | Multiple `UPDATE_CONT` GeoJSON/XML/Opendatasoft datasets; Italy was absent from the parking INDEX and is not covered by ParkenDD | Firenze `data.comune.fi.it/datastore/...` (live per-garage `FreeSpot`/`UpdateDate`, current to the minute); Torino `https://opendata.5t.torino.it/get_pk` (`traffic_data` XML, `generation_time=2026-06-20T06:32Z`, 5-min windows); Bologna `opendata.comune.bologna.it/api/v2/.../disponibilita-parcheggi-vigente/records` | **Strong new candidate — promoted to [`parking/italy-parking.md`](../parking/italy-parking.md) (15/18).** The single genuine new geographic gap this round. Torino 5T is a DATEX-like agency feed; Bologna is a drop-in Opendatasoft case; Firenze needs a small per-garage fan-out. |

## Detail-only improvements for existing candidate families

| Category | Existing family | New detail from the portal | Why it matters |
|---|---|---|---|
| Parking | NDW/RDW Netherlands | Technolution exposes a clean dynamic REST endpoint: `https://opendata.technolution.nl/opendata/parkingdata/v1/dynamic/{id}` returning `vacantSpaces`/`parkingCapacity`/`lastUpdated` per facility | A simpler JSON access path than DATEX-II XML for the same NDW open-parking data — worth noting alongside the existing DATEX note. |
| Parking | Opendatasoft pattern | Confirmed live again at Basel (`data.bs.ch`, 987k occupancy records) and Bologna — same `/api/v2/catalog/datasets/{id}/records` shape | Reinforces recommended-approach #3 (generic Opendatasoft parking bridge); now spans BE/CH/IT/AU. |
| Parking | DATEX-II parking | Trafikverket (`prk:parkingStatusInformation`) and Luxembourg/Amberg Parkleitsysteme surface DATEX/XML parking alongside road feeds | Confirms the DATEX-II parking parser (recommended-approach #2) is reusable across SE/LU/DE. |
| EV charging | AFIR / city occupancy | Basel IWB (`data.bs.ch` dataset 100004) publishes live per-station **occupancy** (not just locations); German Mobilithek "Sensor Parking/Charging" feeds at `5MIN` | Reinforces that EV *occupancy* (the event-bearing part) is reachable via the Opendatasoft seam, not only the static AFIR location registries. |

## Low-signal / firm negative findings (portal genuinely exhausted here)

| Category | What the portal actually held | Conclusion |
|---|---|---|
| **Noise** | Only static `Lärmkartierung` contour maps, INSPIRE noise-action-plan WFS layers, and airport noise zones (DE Brandenburg, NL Schiphol, IE EPA, CH Zürich) — **no live LAeq station telemetry** | Live noise networks (Dublin Sonitus, Bruitparif Paris, Schiphol NOMOS) are **not** harvested into data.europa.eu. Stop sweeping the portal for noise; probe those national/city APIs directly. |
| **Reservoir / dam** | Only static dam-classification datasets (FR "Barrages classés", 2019) — and the `invas-` keyword mostly matched *invasive species*. No storage/level telemetry | Reservoir telemetry (Spanish SAIH, etc.) lives **outside** the portal. Pursue via direct basin-authority probing. |
| **Power outages** | Only static "emergency shelter during blackout" / "urbanization cuts" datasets — **no live outage feeds** | Confirms the domain is API-immature and scrape-only in the EU portal. Pursue UK Power Networks / national DSO APIs directly. |
| Parking (non-viable, consistent with prior notes) | Vienna = Tempo-30/zone WFS geometry; Madrid = static station inventory; many Lombardia `dati.lombardia.it` comune lists = static | Matches the existing "Sources Investigated but Not Viable" list — no change. |

## Category-by-category take

- **Parking**: The clear winner. Italy is a real multi-city gap (Firenze/Torino/Bologna confirmed live). The domain is larger than the INDEX implies, and the three reusable patterns (Opendatasoft exports, NL ParkingData `v1/dynamic`, DATEX-II parking) all re-confirmed.
- **EV charging**: The portal is an *occupancy* amplifier — city Opendatasoft instances (Basel IWB) expose the live status that the AFIR location registries don't. No new family, but useful confirmation.
- **Noise / reservoir / power outages**: **Exhausted for this portal.** It carries only static maps, classifications, and contingency datasets. These domains must be sourced by direct national-agency probing, not data.europa.eu.
- **Hydrology / air quality**: No clean *new* live national feeds surfaced through the portal this round (Italian `idrometrico` / Spanish `aforos` real-time feeds are not well-indexed in DCAT; probe ISPRA/SAIH directly).

## Practical query pattern that worked

Two high-signal portal fields beat fuzzy relevance:

```
GET https://data.europa.eu/api/hub/search/search?q=<native-language phrase>&filters=dataset&limit=120
```
Then client-side filter each result on:
1. `accrual_periodicity` ∈ {`1MIN`,`5MIN`,`10MIN`,`15MIN`,`30MIN`,`BIHOURLY`,`HOURLY`,`UPDATE_CONT`,`CONT`}
2. `distributions[].format` ∈ {gtfs-rt, datex, sensorthings, sos, json, geojson, wfs}
3. `distributions[].access_url` contains a live hint (`/api/`, `/records`, `explore/v2.1`, `geoserver`/`ows`, `datastore`, `/v1/`,`/v2/`)
4. **Relevance gate**: dataset title/keywords must contain a domain term in the
   query language — without this, "real-time" tokens drag in unrelated datasets.

## Recommended follow-up

1. Promote done: **Italy parking** → [`parking/italy-parking.md`](../parking/italy-parking.md).
2. Fold the **NL Technolution `parkingdata/v1/dynamic`** JSON path and the
   **Basel IWB EV occupancy** endpoint into the existing NL-parking and
   Swiss/AFIR EV notes as cleaner access paths (detail, not new sources).
3. Treat **noise, reservoir/dam, and power-outage** as **closed for
   data.europa.eu** — record that the portal holds only static layers for them,
   and route future effort to direct national-agency APIs.
4. The portal's remaining value is now mostly as a **metadata amplifier** for
   already-known families (parking, EV, road DATEX), not as a source of new
   greenfield domains. Round 4 would have diminishing returns unless aimed at a
   specific national portal (data.gouv.fr / GovData) rather than the aggregate.
