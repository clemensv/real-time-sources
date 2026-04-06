# CDMX Air Quality — Mexico City RAMA/SIMAT

**Country/Region**: Mexico (Mexico City / CDMX)
**Publisher**: SEDEMA — Secretaría del Medio Ambiente de la Ciudad de México
**API Endpoint**: `https://www.aire.cdmx.gob.mx/` (connection timeout)
**Documentation**: http://www.aire.cdmx.gob.mx/
**Protocol**: REST (known to exist)
**Auth**: None (historically)
**Data Format**: JSON (historically)
**Update Frequency**: Hourly
**License**: Mexico City government open data

## What It Provides

Mexico City operates one of the oldest and most extensive air quality monitoring networks in Latin America — RAMA (Red Automática de Monitoreo Atmosférico), now part of SIMAT (Sistema de Monitoreo Atmosférico).

Mexico City's air quality is notorious due to:
- **Geography**: 2,240m altitude in a valley surrounded by mountains (7,000m+ volcanoes) — temperature inversions trap pollutants
- **Population**: 22+ million metro area, one of the world's largest
- **Vehicle fleet**: Millions of vehicles; historical lead pollution legacy
- **Ozone**: Primary pollutant, formed by photochemical reactions at altitude
- **PM2.5**: Worsened during biomass burning season

Monitored parameters:
- **PM2.5, PM10** (particulate matter)
- **O3** (ozone — Mexico City's signature pollutant)
- **NO2, NO, NOx** (nitrogen oxides from traffic)
- **CO** (carbon monoxide)
- **SO2** (sulfur dioxide — volcanic contribution from Popocatépetl)

Station coverage: ~30+ stations across the metropolitan area.

### Hoy No Circula

Mexico City's "Hoy No Circula" (today don't drive) program restricts vehicle use based on plate numbers when air quality is poor. The program's activation status is driven by SIMAT data.

## API Details

```
https://www.aire.cdmx.gob.mx/api/datos-abiertos/ultima-hora → Connection timeout
https://www.aire.cdmx.gob.mx/opendata/catalogos/contaminantes_702.json → Connection timeout
```

The aire.cdmx.gob.mx website was unreachable during testing (consistent with other Mexican government servers being down). The API paths suggest JSON endpoints exist.

### Alternative: datos.cdmx.gob.mx

Mexico City's open data portal (datos.cdmx.gob.mx) was also unreachable.

## Integration Notes

- Mexico City's air quality story is one of partial success — conditions have improved dramatically since the 1990s
- Popocatépetl volcano (60 km away) contributes SO2 during eruptions, creating a volcanic-air quality connection
- The altitude (2,240m) means lower atmospheric pressure, which affects pollutant chemistry
- OpenAQ may already ingest SIMAT data
- When accessible, the JSON API format would make integration straightforward

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Hourly data (when accessible) |
| Openness | 0 | Connection timeout; API likely exists |
| Stability | 1 | Government service; unreachable during testing |
| Structure | 2 | JSON API paths suggest good structure |
| Identifiers | 2 | Station codes; standard pollutant parameters |
| Additive Value | 2 | One of world's largest metro areas; volcanic SO2 connection |
| **Total** | **9/18** | |

## Verdict

⚠️ **Maybe** — API likely exists but server infrastructure was unreachable. Revisit when Mexican government servers recover. Check OpenAQ for existing coverage of SIMAT data.
