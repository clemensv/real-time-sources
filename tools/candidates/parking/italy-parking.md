# Italian City Parking (Firenze + Torino + Bologna)

**Country/Region**: Italy — Florence (Firenze), Turin (Torino), Bologna
**Publisher**: Comune di Firenze; 5T S.r.l. (Turin mobility agency); Comune di Bologna
**API Endpoints**:
- Firenze (aggregate): `https://data.comune.fi.it/datastore/download.php?id=6301&type=99&format=url&file_format=geojson&file_id=22774`
- Firenze (per-garage, ~11 feeds): `https://data.comune.fi.it/datastore/...` (Santa Maria Novella, Beccaria, Fortezza, Oltrarno, Sant'Ambrogio, Parterre, Careggi, Pieraccini, San Lorenzo, Palazzo Giustizia, Alberti)
- Torino: `https://opendata.5t.torino.it/get_pk` (5T `traffic_data` XML)
- Bologna (current): `https://opendata.comune.bologna.it/api/v2/catalog/datasets/disponibilita-parcheggi-vigente/records`
- Bologna (history): `.../disponibilita-parcheggi-storico/records`
**Documentation**: data.comune.fi.it · opendata.5t.torino.it · opendata.comune.bologna.it (Opendatasoft)
**Protocol**: REST (GeoJSON / Opendatasoft) + 5T DATEX-like XML
**Auth**: None
**Data Format**: GeoJSON (Firenze), XML `traffic_data` (Torino), JSON/GeoJSON (Bologna Opendatasoft)
**Update Frequency**: Real-time — Torino emits 5-minute measurement windows; Firenze/Bologna `UPDATE_CONT`
**License**: IODL 2.0 / CC BY 4.0 (city-level open data licenses)
**Score**: 15/18

## What It Provides

Live parking-garage occupancy for three major Italian cities, none of which is
covered by the ParkenDD/ParkAPI aggregator (which is DE/CH/DK-centric) or by the
existing parking candidate notes. Each city exposes free-space counts per
structure with current timestamps:

- **Firenze** — the city open-data portal publishes a real-time aggregate
  ("Dati in tempo reale sui posti liberi nei parcheggi") plus ~11 individual
  per-garage GeoJSON feeds. Verified live (per-garage `FreeSpot` with an
  `UpdateDate` timestamp current to the minute).
- **Torino** — 5T (the city's mobility/traffic agency, operator of the SIMONE
  traffic system) publishes `https://opendata.5t.torino.it/get_pk` as
  `traffic_data` XML with `generation_time` and rolling 5-minute
  `start_time`/`end_time` windows per parking structure. This is a DATEX-II-like
  schema (`traffic_data.xsd`) and is the same agency that runs Turin's traffic
  and transit feeds — a high-stability source.
- **Bologna** — the city runs an Opendatasoft portal exposing
  `disponibilita-parcheggi-vigente` (current availability) and
  `disponibilita-parcheggi-storico` (history). This fits the existing
  Opendatasoft parking pattern already recommended in the INDEX.

## API Details

**Firenze aggregate (GeoJSON):**
```
GET https://data.comune.fi.it/datastore/download.php?id=6301&type=99&format=url&file_format=geojson&file_id=22774
```
Per-garage records carry `Id`, `Name`, `FreeSpot`, `UpdateDate`, `Latitude`, `Longitude`.

**Torino 5T (XML):**
```
GET https://opendata.5t.torino.it/get_pk
```
Returns `<traffic_data ... generation_time="…Z">` with `location_reference`
(TMC/coordinates) and measured free-space values on 5-minute windows.

**Bologna (Opendatasoft):**
```
GET https://opendata.comune.bologna.it/api/v2/catalog/datasets/disponibilita-parcheggi-vigente/records?limit=100
```
Standard Opendatasoft v2 record API — same shape as Ghent/Basel.

## Freshness Assessment

Torino is the strongest: explicit 5-minute aggregation windows with a server
`generation_time`, sourced directly from the SIMONE traffic platform. Firenze's
feeds carried `UpdateDate` values current to the minute when probed. Bologna's
"vigente" dataset reflects current availability and is backed by a "storico"
history dataset for backfill/validation.

## Entity Model

- **Parking Structure**: garage/lot with stable per-city ID, name, coordinates
- **Availability**: free spaces, (where published) total capacity, open/closed state
- **Timestamp**: per-record update time (Firenze) or window bounds (Torino)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Torino 5-min windows; Firenze/Bologna `UPDATE_CONT`, verified current |
| Openness | 3 | No auth; IODL/CC BY open licenses |
| Stability | 3 | All government/agency-operated; 5T runs Turin's core mobility platform |
| Structure | 2 | Three different shapes (GeoJSON, 5T XML, Opendatasoft JSON) — no single schema |
| Identifiers | 2 | Stable garage IDs per city, but not harmonized across cities |
| Additive Value | 2 | Closes the Italy gap in the parking domain; Torino XML is a distinct pattern |
| **Total** | **15/18** | |

## Notes

- **This is the genuine new geographic gap found in the 2026-06 data.europa.eu
  Round 3 sweep.** Italy was previously absent from the parking INDEX; ParkenDD
  does not cover Italian cities.
- **Bologna** is a drop-in for the recommended Opendatasoft parking bridge
  (same platform/API as Ghent and Basel) — lowest-effort win.
- **Torino 5T** is the most interesting: a DATEX-like XML feed from a serious
  mobility agency, reusable alongside the NDW/Trafikverket DATEX parking work.
- **Firenze** needs a small per-garage fan-out (one aggregate feed + ~11 garage
  feeds) but is plain GeoJSON with clean fields.
- Many other Italian "parcheggi" datasets (Lombardia `dati.lombardia.it`
  Socrata, Genova/Piemonte/Modena WFS, Toscana `dati.toscana.it` ODALA
  vehicle-passage) are **static inventories or geometry layers**, not live
  occupancy — treat as reference data, not telemetry sources.
