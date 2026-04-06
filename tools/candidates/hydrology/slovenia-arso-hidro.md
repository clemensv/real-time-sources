# Slovenia — ARSO Hydrological Monitoring

**Country/Region**: Slovenia
**Publisher**: Agencija Republike Slovenije za okolje (ARSO) — Slovenian Environment Agency
**API Endpoint**: `https://www.arso.gov.si/xml/vode/hidro_podatki_zadnji.xml`
**Documentation**: https://www.arso.gov.si/vode/podatki/
**Protocol**: REST (static XML feed)
**Auth**: None
**Data Format**: XML
**Update Frequency**: Every 30 minutes
**License**: Open access (Slovenian government public data)

## What It Provides

Real-time water level (vodostaj), discharge (pretok), water temperature (temp_vode), and flood warning thresholds for all monitored river stations across Slovenia. The feed covers major rivers including the Sava, Drava, Mura, Soča, and their tributaries. Each station also includes three flood warning levels (prvi/drugi/tretji vodni val pretok) and a flow characterization (e.g., "mali pretok" = low flow, "običajni pretok" = normal flow).

## API Details

### Latest Data (all stations, single XML)
```
GET https://www.arso.gov.si/xml/vode/hidro_podatki_zadnji.xml
```

Returns a single XML document with all stations and their latest readings:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<arsopodatki verzija="1.5">
  <vir>Agencija RS za okolje</vir>
  <predlagan_zajem>5 minut čez polno uro ali pol ure</predlagan_zajem>
  <predlagan_zajem_perioda>30 min</predlagan_zajem_perioda>
  <datum_priprave>2026-04-06 11:30</datum_priprave>
  <postaja sifra="1060" wgs84_dolzina="15.9953" wgs84_sirina="46.68124" kota_0="202.35">
    <reka>Mura</reka>
    <merilno_mesto>Gornja Radgona</merilno_mesto>
    <ime_kratko>Mura - Gor. Radgona I</ime_kratko>
    <datum>2026-04-06 11:30</datum>
    <vodostaj>71</vodostaj>
    <pretok>71</pretok>
    <prvi_vv_pretok>600.0</prvi_vv_pretok>
    <drugi_vv_pretok>905.0</drugi_vv_pretok>
    <tretji_vv_pretok>1180.0</tretji_vv_pretok>
    <pretok_znacilni>mali pretok</pretok_znacilni>
    <temp_vode>11.3</temp_vode>
  </postaja>
  ...
</arsopodatki>
```

Key fields per station:
- `sifra` — station code (numeric)
- `wgs84_dolzina/sirina` — longitude/latitude (WGS84)
- `kota_0` — zero-point elevation (m)
- `reka` — river name
- `merilno_mesto` — measurement location
- `vodostaj` — water level (cm)
- `pretok` — discharge (m³/s)
- `temp_vode` — water temperature (°C)
- `prvi/drugi/tretji_vv_pretok` — flood warning thresholds 1/2/3 (m³/s)
- `pretok_znacilni` — flow characterization

The XML header recommends polling every 30 minutes on the hour or half-hour.

## Freshness Assessment

Probed 2026-04-06 ~12:30 UTC: Feed showed `datum_priprave` (preparation date) of `2026-04-06 11:30`, with all stations reporting at the same timestamp. Data is effectively real-time with 30-minute granularity.

## Entity Model

- **Station Code**: `sifra` — numeric 4-digit code, e.g., `1060`
- **River**: `reka` — river name string
- **Location**: `merilno_mesto` — location name
- **Kafka key**: `stations/{sifra}`
- **CloudEvents subject**: `stations/{sifra}`

Station codes (`sifra`) are stable numeric identifiers assigned by ARSO.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | 30-minute updates — good but not sub-15-minute |
| Openness | 3 | No auth, freely accessible, government data |
| Stability | 3 | National environment agency, long-running service |
| Structure | 3 | Clean XML with consistent schema, rich metadata per station |
| Identifiers | 3 | Stable numeric station codes with WGS84 coordinates |
| Additive Value | 3 | Slovenia not covered; includes water temperature and flood thresholds |
| **Total** | **17/18** | |

## Notes

- One of the most elegant hydrometric feeds found — a single XML document contains the entire national network's latest readings
- Includes water temperature, which is relatively rare for real-time hydrometric feeds
- The flood warning thresholds (three levels) embedded in the feed add context for each station
- The `pretok_znacilni` field provides a human-readable flow characterization
- Slovenian-language field names but consistent and documentable
- Water level in cm, discharge in m³/s, temperature in °C
- Station coordinates are in WGS84 — embedded directly in the XML attributes
- The single-file approach is very efficient for polling — one request gets the entire network
- Some stations may have empty `pretok` or `temp_vode` fields when data is unavailable
