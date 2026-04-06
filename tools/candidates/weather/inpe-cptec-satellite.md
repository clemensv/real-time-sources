# INPE CPTEC — Satellite Imagery and Weather Forecasting

**Country/Region**: Brazil (national; South America coverage)
**Publisher**: CPTEC/INPE — Centro de Previsão de Tempo e Estudos Climáticos
**API Endpoint**: `http://ftp.cptec.inpe.br/goes/goes16/retangular/ch13/` (FTP directory)
**Documentation**: http://www.cptec.inpe.br/
**Protocol**: HTTP/FTP (file-based)
**Auth**: None
**Data Format**: Binary image files (NetCDF, PNG, JPEG)
**Update Frequency**: Sub-hourly (satellite imagery every 10-15 minutes)
**License**: Brazilian government

## What It Provides

CPTEC is INPE's weather forecasting center, providing:

- **GOES-16 satellite imagery**: Full-disk and regional imagery for South America (Channel 13 = IR longwave, plus all 16 ABI channels)
- **Weather forecasting models**: Numerical weather prediction for South America
- **Tropical cyclone tracking**: Rare South Atlantic tropical cyclones (Hurricane Catarina, 2004)
- **UV index forecasts**: Critical for Brazil's tropical latitudes

### FTP Data Archive (confirmed accessible)

```
http://ftp.cptec.inpe.br/goes/goes16/retangular/ch13/
```

Directory listing confirmed (2026-04-06) with year-organized subdirectories from 2017–2025. Each directory contains processed GOES-16 imagery in rectangular projection.

### Known Additional Endpoints

CPTEC is known to provide:
- Wave forecasting (WAVEWATCH III model output)
- Wind and current forecasts for Brazilian waters
- Fire weather forecasts
- Agricultural weather bulletins

## Integration Notes

- GOES-16 imagery from CPTEC is processed for South American coverage specifically
- The FTP directory structure enables automated crawling
- File-based access (not REST API) requires different adapter pattern
- NOAA already provides GOES-16 data globally, but CPTEC's processed products may have South American-specific enhancements
- Complementary to existing NOAA GOES candidate (noaa-goes/)
- The sub-hourly refresh rate makes this genuinely real-time satellite monitoring

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Sub-hourly satellite imagery |
| Openness | 3 | Public FTP; no auth |
| Stability | 2 | Government FTP; has been operational since 2017 |
| Structure | 1 | File-based; binary imagery; no REST API |
| Identifiers | 1 | File naming convention; no standard IDs |
| Additive Value | 1 | NOAA GOES already covers this; CPTEC adds processing |
| **Total** | **11/18** | |

## Verdict

⚠️ **Maybe** — Accessible public data but low additive value over NOAA GOES. File-based access requires different adapter pattern. Most valuable if South American-specific processed products (wave forecasts, fire weather) become available via API.
