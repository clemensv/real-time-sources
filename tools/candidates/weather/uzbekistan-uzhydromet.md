# Uzbekistan Uzhydromet — Hydrometeorological Service

**Country/Region**: Uzbekistan
**Publisher**: Uzhydromet (Centre of Hydrometeorological Service under the Cabinet of Ministers)
**API Endpoint**: `https://www.meteo.uz/` (web portal)
**Documentation**: https://www.meteo.uz/
**Protocol**: Web portal (HTML)
**Auth**: N/A
**Data Format**: HTML (Russian/Uzbek languages)
**Update Frequency**: Synoptic (3-hourly)
**License**: Uzbek government data

## What It Provides

Uzbekistan occupies the heart of Central Asia — a double-landlocked country (35M people) facing acute water scarcity, extreme continental climate, and the Aral Sea environmental catastrophe.

Uzhydromet monitors:
- **Weather**: ~80 synoptic stations across deserts, mountains, and fertile valleys
- **Hydrology**: Amu Darya and Syr Darya river monitoring (Central Asia's lifelines)
- **Air quality**: Major cities (Tashkent, Samarkand, Bukhara)
- **Dust storms**: Aralkum (dried Aral Sea bed) dust — one of the world's newest deserts
- **Agricultural meteorology**: Cotton and wheat growing conditions
- **Glaciology**: Tien Shan mountain glaciers (shrinking rapidly)

### Regional Significance

- **Aral Sea crisis**: The dried Aral Sea bed (Aralkum) generates salt-laden dust storms affecting the entire region
- **Water politics**: Uzbekistan is downstream on Amu Darya/Syr Darya — depends on Kyrgyz/Tajik releases from Toktogul and Nurek dams
- **Cotton monoculture**: Weather data drives irrigation planning for the world's 6th largest cotton producer
- **Tashkent earthquake legacy**: 1966 M5.1 earthquake destroyed much of the capital

### Probe Results

Website not directly probed but known to be operational in Russian/Uzbek with no public API. Central Asian hydrometeorological services uniformly lack public APIs.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Data exists; web only |
| Openness | 0 | No API |
| Stability | 1 | Government service |
| Structure | 0 | HTML |
| Identifiers | 1 | WMO station numbers exist |
| Additive Value | 2 | Aral Sea monitoring; transboundary water; but no unique API |
| **Total** | **5/18** | |

## Verdict

Documented gap. Uzbekistan's hydrometeorological data is regionally critical for Aral Sea environmental monitoring and Central Asian water politics, but no public API exists. Like all Central Asian republics, Uzhydromet operates a web-only service.
