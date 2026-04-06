# OVSICORI Costa Rica — Volcanic Monitoring

**Country/Region**: Costa Rica (national)
**Publisher**: OVSICORI-UNA — Observatorio Vulcanológico y Sismológico de Costa Rica
**API Endpoint**: `https://www.ovsicori.una.ac.cr/` (various 404s / connection failures)
**Documentation**: https://www.ovsicori.una.ac.cr/
**Protocol**: Unknown
**Auth**: N/A
**Data Format**: Unknown
**Update Frequency**: Continuous monitoring
**License**: Universidad Nacional (public university)

## What It Provides

Costa Rica has 5 active volcanoes and several more with potential for reactivation:

- **Rincón de la Vieja**: Frequent phreatic eruptions; most recently active 2022–2024
- **Arenal**: Famous cone volcano; erupted 1968–2010; now in rest phase
- **Poás**: Active crater lake with frequent phreatic activity; visitor facility closed multiple times
- **Irazú**: Highest volcano in Costa Rica (3,432m); erupted 1963–1965, devastating Cartago
- **Turrialba**: Reawakened in 2010 after 150 years; ash falls reach San José

OVSICORI operates seismic, geodetic, gas, and thermal monitoring networks across these volcanoes.

## API Details

All tested endpoints failed:
```
https://www.ovsicori.una.ac.cr/sistemas/sismologia/sismos_ultimos.php → 404
https://www.ovsicori.una.ac.cr/api/volcanes → 404
https://api.ovsicori.una.ac.cr/sismos/ultimos → Connection failed
https://api.volcanes.ovsicori.una.ac.cr/volcano/list → Connection failed
```

### Related: RSN (see seismology/rsn-costa-rica.md)
RSN provides earthquake data via HTML but no volcanic monitoring data.

## Integration Notes

- Costa Rica's volcanoes are popular tourist destinations — eruption alerts have tourism implications
- San José (population 2M metro) is within ashfall range of Turrialba, Irazú, and Poás
- VAAC Washington issues ash advisories for Costa Rican eruptions
- MIROVA provides satellite thermal monitoring
- Smithsonian GVP weekly reports cover Costa Rican activity

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Presumably real-time monitoring |
| Openness | 0 | No working API endpoints found |
| Stability | 1 | University institution |
| Structure | 0 | Cannot assess |
| Identifiers | 0 | Cannot assess |
| Additive Value | 2 | 5 active volcanoes; San José risk zone |
| **Total** | **4/18** | |

## Verdict

⏭️ **Skip** — No programmatic access available. Costa Rica's volcanic activity is covered by MIROVA, Smithsonian GVP, and VAAC ash advisories.
