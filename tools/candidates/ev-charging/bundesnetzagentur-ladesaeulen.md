# Bundesnetzagentur Ladesäulenregister

**Country/Region**: Germany
**Publisher**: NOW GmbH / Nationale Leitstelle Ladeinfrastruktur using Bundesnetzagentur source data
**NAP / Catalog**: https://mobilithek.info/offers/951517095896416256
**Public Access URLs**:
- https://d1269bxe5ubfat.cloudfront.net/bnetza-api/data/bnetza_api_ladestation000.csv?v=1
- https://d1269bxe5ubfat.cloudfront.net/bnetza-api/data/bnetza_api_ladepunkt000.csv?v=1
- https://d1269bxe5ubfat.cloudfront.net/bnetza-api/data/bnetza_api_stecker000.csv?v=1
**Documentation**: https://d1269bxe5ubfat.cloudfront.net/bnetza-api/metadata/BNetzA-API_Metadaten.xlsx?v=1
**Protocol**: HTTPS pull of CSV files via Mobilithek/NOW offer
**Auth**: None for the published CSV files
**Data Format**: CSV
**Update Frequency**: Mobilithek metadata declares continuous publication; exact operational cadence needs longer observation
**License**: Creative Commons Attribution 4.0 International (CC BY 4.0)

## What It Provides

Germany's charging-data story is now better than the old monthly Bundesnetzagentur
register alone. Mobilithek exposes an official NOW/Nationale Leitstelle offer called
`Bundesnetzagentur Liste der Ladesäulen aus Webserviceschnittstelle`, which republishes
cleaned Bundesnetzagentur data as three stable CSV tables.

The result is still not a modern JSON API, but it is a real machine-readable pull
source with explicit station, charge-point, and connector identifiers.

## API Details

There is still no REST-style JSON API, but there is now a structured pull interface
with three public CSV distributions:

1. **Ladestation table**
   - `bnetza_api_ladestation000.csv`
   - Includes `ladestation_id`, operator fields, address, coordinates, commissioning
     date, `betriebsstatus`, station power, payment-system flags, opening hours,
     use-case classification, and `datenstand`

2. **Ladepunkt table**
   - `bnetza_api_ladepunkt000.csv`
   - Includes `ladepunkt_id`, `ladestation_id`, `evse_id`, point power,
     classification fields, and `datenstand`

3. **Stecker table**
   - `bnetza_api_stecker000.csv`
   - Includes `stecker_id`, connector capabilities, power, and `datenstand`

The metadata workbook documents the field model. This is materially stronger than the
old one-file monthly register because the data now has stable internal IDs and
separate station/point/connector granularity.

## Freshness Assessment

The source is no longer best described as a monthly static register. Mobilithek marks
the offer with continuous publication metadata, and the CSVs carry per-row
`datenstand` timestamps. During this probe, the public CloudFront objects returned `200`
without authentication and exposed recent object metadata.

What is still unproven is connector occupancy. The station table includes
`betriebsstatus`, which is useful operational state, but this probe did not confirm
OCPI-like live availability semantics such as `AVAILABLE`, `OCCUPIED`, or `OUTOFORDER`
at connector level.

## Entity Model

- **Charging Station**: Station-level entity with operator, address, payment systems, opening hours, and operational status
- **Charging Point**: A single charge point tied to a station and optional `evse_id`
- **Connector**: Individual connector records with connector-type flags and power
- **Operator**: The company operating the charging infrastructure
- **Location**: Full German address + GPS coordinates

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Continuous publication metadata and per-row timestamps, but connector occupancy is still unverified |
| Openness | 3 | CC BY 4.0, public CSV URLs, no registration observed |
| Stability | 3 | Government-backed NAP/catalog publication via NOW and Mobilithek |
| Structure | 2 | Stable CSV pull interface with metadata workbook, but still not a modern API |
| Identifiers | 3 | Explicit station, point, and connector IDs are present |
| Additive Value | 2 | Official German baseline with operational fields, but not yet full live availability |
| **Total** | **15/18** | |

## Notes

- For actual live refill-point state in Germany, the better currently confirmed
  source is MobiData BW's `Gebündelte Daten E-Ladesäulen Baden-Württemberg`
  offer on Mobilithek. This Bundesnetzagentur feed remains the broader national
  baseline, not the strongest live-status publication.
- The old Bundesnetzagentur CSV/XLSX register is no longer the best access point; the
   Mobilithek/NOW offer is better because it provides stable internal IDs and cleaner
   table separation.
- A bridge would still be a poller: fetch the three CSVs, key by station/point/
   connector ID, and emit reference plus status-style events.
- Germany now looks closer to AFDC's "station-level operational status" tier than to a
   purely static registry, but it still is not a confirmed open connector-occupancy
   feed.
- For richer live availability in Germany, network-specific APIs or roaming platforms
   may still be needed as complements.
- Germany has ~120,000+ public charging points as of 2025, making this one of the larger national registries.
