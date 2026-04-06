# France IRVE (Infrastructures de Recharge pour Véhicules Électriques)

**Country/Region**: France
**Publisher**: data.gouv.fr / transport.data.gouv.fr (Point d'Accès National)
**API Endpoint**: `https://transport.data.gouv.fr/datasets/fichier-consolide-des-bornes-de-recharge-pour-vehicules-electriques` (file download)
**Documentation**: https://doc.transport.data.gouv.fr/producteurs/infrastructures-de-recharge-de-vehicules-electriques-irve
**Protocol**: File download (CSV, GeoJSON)
**Auth**: None
**Data Format**: CSV (schema IRVE v2.3.1) / GeoJSON
**Real-Time Status**: Static registry only — dynamic schema defined but no national consolidation yet
**Update Frequency**: Daily consolidation
**Station Count**: 100,000+ charging points across France
**License**: Licence Ouverte v2.0 (French open data license, compatible with CC-BY)

## What It Provides

France mandates by law (arrêté du 4 mai 2021) that all operators of public EV charging infrastructure publish their data on data.gouv.fr. The national consolidation merges all operator submissions into a single file — the Base Nationale des IRVE. This covers every publicly accessible charging point in France with location, connector types, power levels, operator information, and AFIREV-compliant identifiers.

A dynamic data schema (schema-irve-dynamique v2.2.0) also exists for real-time availability and status data, but as of early 2026 there is no national consolidation of dynamic feeds. Individual operators may publish dynamic data separately.

## API Details

**Static consolidated data (CSV):**
```
https://www.data.gouv.fr/fr/datasets/fichier-consolide-des-bornes-de-recharge-pour-vehicules-electriques/
```
Resources include:
- Consolidated CSV (schema v2.3.1) — updated daily
- GeoJSON export — updated daily
- Historical versions available via transport.data.gouv.fr resource history

**Schema fields (static, v2.3.1):**
- `id_pdc_itinerance` — unique charging point ID (AFIREV format, e.g., `FRELCPE680011`)
- `id_station_itinerance` — station ID
- `nom_operateur`, `nom_enseigne` — operator and brand names
- `nom_station` — station name
- `adresse_station`, `code_commune_INSEE` — location
- `coordonneesXY` — GPS coordinates (WGS84)
- `puissance_nominale` — power in kW
- `type_prise` — connector types (Type 2, CCS, CHAdeMO, etc.)
- `condition_acces` — access conditions
- `tarification` — pricing information
- `date_mise_en_service` — commissioning date
- `date_maj` — last update date

**Dynamic schema (v2.2.0) — not yet consolidated nationally:**
- `id_pdc_itinerance` — links to static data
- `etat_pdc` — operational status (en service, hors service, en maintenance)
- `occupation_pdc` — occupancy (libre, occupé, réservé, inconnu)
- `etat_prise_type_2`, `etat_prise_type_ccs`, etc. — per-connector status
- `horodatage` — timestamp of status observation

## Freshness Assessment

The static consolidation is rebuilt daily — resource history shows daily timestamps. For location and infrastructure data, this is authoritative and reasonably fresh. However, there is no national consolidation of real-time availability/occupancy data yet. The dynamic schema exists and individual operators are required to publish it, but the national aggregation pipeline is not yet operational.

France's approach mirrors what EU AFIR will require by 2025 — open publication of both static and dynamic EV charging data via National Access Points. France is ahead on static data but still building out the dynamic layer.

## Entity Model

- **Point de Charge (PDC)**: Individual charging point with unique `id_pdc_itinerance` (AFIREV format)
- **Station**: Physical location grouping multiple PDCs, identified by `id_station_itinerance`
- **Opérateur**: The entity operating the charging infrastructure
- **Aménageur**: The entity that installed/owns the infrastructure
- **Enseigne**: The commercial brand visible to drivers
- AFIREV ID format: country code + operator code + station/point numbers (e.g., `FRELCPE680011`)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Daily static updates; no national dynamic data consolidation yet |
| Openness | 3 | Licence Ouverte v2.0, no auth, direct download |
| Stability | 3 | Government-mandated, legally required publication, well-maintained |
| Structure | 2 | CSV with defined schema; GeoJSON also available; not OCPI |
| Identifiers | 3 | AFIREV-compliant unique IDs for stations and charging points |
| Additive Value | 3 | Authoritative French national registry; 100K+ points; legally mandated |
| **Total** | **15/18** | |

## Notes

- France has the second-largest charging network in Europe after the Netherlands. The legal mandate for open data publication makes this a model for other countries.
- The AFIREV ID scheme (`id_pdc_itinerance`) provides stable, globally unique identifiers — essential for cross-referencing with roaming platforms like Gireve.
- The dynamic data gap is significant. Individual operators (e.g., Ionity, TotalEnergies, Izivia) may publish real-time feeds separately on data.gouv.fr, but there's no single consolidated real-time feed.
- The schema has undergone several revisions (v1.0.3 → v2.0.3 → v2.1.0 → v2.3.1). Current consolidation uses v2.3.1.
- The Validata tool can be used to check schema compliance: https://validata.fr/table-schema?schema_name=schema-datagouvfr.etalab%2Fschema-irve-statique
- For real-time French data, Gireve (the French OCPI roaming hub) would be the better target — but it's a commercial platform.
