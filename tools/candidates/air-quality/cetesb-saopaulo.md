# CETESB São Paulo — Air Quality

**Country/Region**: Brazil (São Paulo State)
**Publisher**: CETESB — Companhia Ambiental do Estado de São Paulo
**API Endpoint**: `https://qualar.cetesb.sp.gov.br/` (registration required)
**Documentation**: https://cetesb.sp.gov.br/ar/qualar/
**Protocol**: Web portal (Java servlets)
**Auth**: Required (registration)
**Data Format**: HTML / CSV downloads
**Update Frequency**: Hourly
**License**: São Paulo State environmental agency

## What It Provides

CETESB operates one of the most extensive air quality monitoring networks in Latin America. São Paulo metropolitan area (21+ million people) has serious air quality challenges from vehicle emissions, industry, and biomass burning (sugarcane harvest season).

Monitored parameters:
- **PM2.5** and **PM10** (particulate matter)
- **O3** (ozone — São Paulo's primary pollutant)
- **NO2**, **NO**, **NOx** (nitrogen oxides)
- **CO** (carbon monoxide)
- **SO2** (sulfur dioxide)
- **Meteorological**: temperature, humidity, wind speed/direction, radiation

Station coverage: ~60+ monitoring stations across São Paulo State, with dense coverage in the capital metro area.

## API Details

### QUALAR System
```
https://qualar.cetesb.sp.gov.br/qualar/conDadosHorarios.do?method=pesquisar
```

Returns a registration prompt:
> "Favor, realizar o cadastro novamente. Clique em 'Não sou Cadastrado'."

The QUALAR system requires free registration (email + Brazilian CPF/CNPJ) to access hourly data. Once registered, data is available through web queries with CSV export capability.

### Alternative: dados.gov.br

Brazil's federal open data portal may host CETESB data. Not tested.

## Integration Notes

- São Paulo is the largest city in the Southern Hemisphere — air quality data here is inherently significant
- The QUALAR registration wall is a barrier but the data itself is free
- Ozone is São Paulo's signature pollutant (photochemical smog from vehicle emissions)
- Sugarcane burning season (April–November) creates dramatic PM2.5 spikes visible across the state
- A Python scraper with registered credentials could automate data extraction
- Existing OpenAQ aggregator may already ingest CETESB data

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Hourly data; registration wall adds latency |
| Openness | 1 | Free registration required (CPF/CNPJ barrier for non-Brazilians) |
| Stability | 2 | State agency; QUALAR system operational for years |
| Structure | 1 | Web forms + CSV; no REST API |
| Identifiers | 2 | Station codes are stable |
| Additive Value | 2 | Largest Southern Hemisphere city; may be in OpenAQ already |
| **Total** | **10/18** | |

## Verdict

⚠️ **Maybe** — Registration barrier and web scraping requirement make this harder than typical API integrations. Check if OpenAQ already ingests CETESB data (if so, use OpenAQ instead). São Paulo's air quality is scientifically significant, especially during biomass burning season.
