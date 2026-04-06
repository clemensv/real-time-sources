# Costa Rica ICE — Energy Grid

**Country/Region**: Costa Rica (national)
**Publisher**: ICE — Instituto Costarricense de Electricidad
**API Endpoint**: Not found
**Documentation**: https://www.grupoice.com/
**Protocol**: Unknown
**Auth**: Unknown
**Data Format**: Unknown
**Update Frequency**: Real-time (grid operation)
**License**: Costa Rican state enterprise

## What It Provides

Costa Rica is a global renewable energy champion — the country regularly generates **98-99% of its electricity from renewables**, primarily:

- **Hydro**: ~65% (fed by abundant rainfall on volcanic terrain)
- **Geothermal**: ~15% (volcanic heat — Miravalles, Las Pailas plants near Rincón de la Vieja volcano)
- **Wind**: ~15% (growing, especially in Guanacaste)
- **Solar**: ~3% (growing)
- **Biomass**: ~2% (sugarcane bagasse)

In recent years, Costa Rica has run for 300+ consecutive days on 100% renewable electricity. The country has no nuclear or coal generation.

ICE operates both generation and transmission. The energy mix's dependence on hydro creates vulnerability to drought (El Niño years reduce hydropower).

## API Details

No public API found. ICE publishes generation reports on its website but no structured data endpoints were discovered.

### Alternative: CENCE

CENCE (Centro Nacional de Control de Energía) is Costa Rica's grid dispatch center within ICE. They publish daily dispatch reports in PDF format.

## Integration Notes

- Costa Rica's near-100% renewable grid makes it the gold standard for clean energy
- Geothermal generation from active volcanoes is unique — volcanic monitoring and energy generation are linked
- El Niño creates drought conditions that reduce hydro generation, requiring backup thermal plants
- Costa Rica + Uruguay are the two most compelling Latin American renewable energy stories
- Small grid (~3.5 GW peak demand) but exceptionally clean

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Grid data exists; no API found |
| Openness | 0 | No API; PDF reports only |
| Stability | 1 | State enterprise |
| Structure | 0 | PDFs only |
| Identifiers | 0 | Cannot assess |
| Additive Value | 3 | 98-99% renewable; geothermal from active volcanoes |
| **Total** | **5/18** | |

## Verdict

⏭️ **Skip** — No API access. Costa Rica's near-100% renewable grid is remarkable but not programmatically accessible. The volcano-geothermal link is unique — eruption risk directly affects a significant generation source.
