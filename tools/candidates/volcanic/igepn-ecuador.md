# IGEPN Ecuador — Volcanic Monitoring

**Country/Region**: Ecuador (national, including Galápagos)
**Publisher**: Instituto Geofísico, Escuela Politécnica Nacional
**API Endpoint**: `https://www.igepn.edu.ec/` (403 on all paths tested)
**Documentation**: https://www.igepn.edu.ec/servicios/volcanes
**Protocol**: Unknown (website blocked)
**Auth**: N/A (403)
**Data Format**: Unknown
**Update Frequency**: Continuous monitoring
**License**: Ecuadorian government/university

## What It Provides

Ecuador has approximately 80 potentially active volcanoes — including some of the world's most scientifically significant:

- **Cotopaxi** (5,897m): One of the highest active volcanoes; threatens Quito (population 2.8M) and the Interandean Valley via lahars (volcanic mudflows). Reactivated in 2015, remains under elevated alert.
- **Tungurahua** ("Throat of Fire"): Sustained eruption from 1999 to 2016. One of the most studied volcanoes in South America.
- **Reventador**: Ecuador's most active volcano; erupts nearly continuously.
- **Sangay**: UNESCO World Heritage site; persistent Strombolian eruptions since 2019.
- **Sierra Negra** (Galápagos): Shield volcano on Isabela Island; last erupted 2018. The Galápagos volcanic complex is uniquely monitored.
- **Wolf** (Galápagos): Erupted 2022; home to the only population of pink iguanas on Earth.
- **Fernandina** (Galápagos): Most active Galápagos volcano, erupted 2024.

IGEPN provides alert levels, seismicity data, SO2 flux measurements, thermal anomalies, and deformation monitoring.

## API Details

All endpoints returned 403 Forbidden (likely WAF/Cloudflare):
```
https://www.igepn.edu.ec/sismos/sismos-ultimo-sismo → 403
https://www.igepn.edu.ec/api/ultimo-sismo → 403
https://www.igepn.edu.ec/servicios/api/v1/earthquakes/last → 403
```

No alternative API endpoints were discovered.

## Integration Notes

- Galápagos volcanic monitoring is globally unique — the only place where volcanic activity directly threatens endemic species found nowhere else
- MIROVA (satellite thermal monitoring, see volcanic/mirova.md) provides complementary thermal anomaly data for Ecuadorian volcanoes
- Smithsonian GVP provides weekly activity reports that include Ecuadorian volcanoes
- VAAC (Volcanic Ash Advisory Centre — Washington) issues ash advisories for Ecuadorian eruptions
- Ecuador's volcanic monitoring is considered among the best in South America — frustrating that it's not programmatically accessible

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Likely real-time but inaccessible |
| Openness | 0 | 403 on all endpoints |
| Stability | 1 | Government institute |
| Structure | 0 | Cannot assess |
| Identifiers | 0 | Cannot assess |
| Additive Value | 3 | Galápagos uniqueness; Cotopaxi threat to Quito |
| **Total** | **5/18** | |

## Verdict

⏭️ **Skip** — Same 403 blocker as the seismology endpoint. Exceptionally valuable data locked behind WAF. Galápagos volcanic monitoring is one-of-a-kind. Revisit periodically.
