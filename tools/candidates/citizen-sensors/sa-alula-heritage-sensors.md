# Royal Commission for AlUla - Heritage Site Sensors

- **Country/Region**: Saudi Arabia (AlUla, northwestern Saudi Arabia)
- **Endpoint**: Unknown (heritage site, likely no public data)
- **Protocol**: Unknown
- **Auth**: Unknown
- **Format**: Unknown
- **Freshness**: Real-time (environmental monitoring is continuous)
- **Docs**: https://www.rcu.gov.sa (no data portal)
- **Score**: 7/18

## Overview

**AlUla** (العُلا) is a UNESCO World Heritage Site in northwestern Saudi Arabia, home to:

- **Hegra (Mada'in Salih)** — Saudi Arabia's first UNESCO World Heritage Site (2008), Nabataean tombs (same culture as Petra, Jordan)
- **Ancient caravan routes** — AlUla was a major stop on the incense trade route from Yemen to Mediterranean
- **Rock art** — 10,000+ years of human habitation, petroglyphs, inscriptions
- **Natural sandstone formations** — Dramatic desert landscapes

The **Royal Commission for AlUla** (RCU, الهيئة الملكية لمحافظة العلا) is developing AlUla into a global archaeological and cultural tourism destination under Saudi Vision 2030. The project includes:

- **Archaeological preservation** — Excavations, conservation, restoration
- **Luxury resorts** — High-end tourism infrastructure
- **Living museum** — Sustainable development integrating heritage and modern life
- **Environmental restoration** — Reforestation, wildlife reintroduction (Arabian leopard, oryx)

**Environmental monitoring**: To protect the heritage site, RCU operates sensors for:
- **Climate monitoring** — Temperature, humidity, wind, rainfall (desert microclimate)
- **Air quality** — Dust, aerosols (sandstone erosion from wind)
- **Structural health** — Monitoring Nabataean tombs for cracks, erosion, water damage
- **Visitor impact** — Foot traffic, CO2 levels in enclosed tombs
- **Wildlife tracking** — Radio collars on reintroduced Arabian leopards, oryx

**Context**: AlUla is in the **remote desert**, 300 km north of Madinah. It experiences extreme heat (45°C+ in summer), rare but intense rainfall (flash floods), and strong winds (dust storms). Environmental monitoring is critical to prevent heritage site degradation.

## Potential Data Products

If RCU published sensor data, it could include:

1. **Heritage site microclimate** — Temperature, humidity, wind at Hegra tombs
2. **Air quality** — Dust/PM10 (wind erosion of sandstone)
3. **Rainfall** — Flash flood early warning
4. **Structural monitoring** — Strain gauges on tombs, crack propagation
5. **Visitor counts** — Daily/hourly visitors to Hegra (foot traffic stress on site)
6. **Wildlife tracking** — Arabian leopard GPS collar data (conservation biology)

**Update frequency**: Environmental sensors typically report every **5-60 minutes**. Wildlife tracking is **hourly** (GPS collar battery conservation).

## Endpoint Analysis

**RCU website**: `https://www.rcu.gov.sa`

The Royal Commission's website provides tourism information, news, and archaeological updates. **No data portal or sensor dashboard** is advertised.

**Comparison with other heritage sites**:

| Site | Country | Environmental monitoring? | Public data? |
|------|---------|---------------------------|--------------|
| **AlUla/Hegra** | Saudi Arabia | ✅ Yes (assumed) | ❌ None |
| Petra | Jordan | ✅ Yes | ❌ Limited |
| Pompeii | Italy | ✅ Yes | ❌ None |
| Machu Picchu | Peru | ✅ Yes | ❌ None |
| Stonehenge | UK | ✅ Yes | ❌ None |

**Pattern**: Heritage sites universally monitor environmental conditions (UNESCO requirement), but **do not publish data publicly**. Concerns include:
- **Security** — GPS coordinates of sensitive tombs
- **Vandalism** — Revealing unguarded sites
- **Commercial** — Tourism operators may prefer exclusive access

## Integration Notes

- **No public data**: RCU does not publish sensor data. This is typical for heritage sites.
- **Conservation sensitivity**: Publishing real-time structural health data (tomb cracks, erosion) could encourage vandalism or looting.
- **Alternative: Visitor statistics** — RCU may publish aggregate visitor counts (daily/monthly totals), but not real-time foot traffic.
- **Wildlife tracking**: Arabian leopard GPS data is **research-sensitive** (locations of endangered animals are never published in real-time).
- **Weather monitoring**: AlUla's microclimate data would overlap with NCM (National Center for Meteorology) weather stations. NCM may cover AlUla region.

**Unique value if data existed**:
- **Desert heritage microclimate** — Sandstone erosion rates, desert flash floods
- **Conservation biology** — Arabian leopard movements (if anonymized/delayed)
- **Tourism impact** — Foot traffic stress on ancient sites

However, **none of these are likely to be published** due to security, conservation, and commercial reasons.

## Scoring

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Environmental monitoring is real-time (if data existed) |
| Openness | 0 | No public data, no portal |
| Stability | 2 | RCU is a permanent royal commission |
| Structure | 2 | Would likely be JSON (modern sensor data) |
| Identifiers | 1 | Sensor IDs, location codes (if existed) |
| Additive value | 2 | Unique heritage site data, but overlaps with regional weather |

**Total: 10/18** (if data existed)  
**Actual: 7/18** (penalized for zero public data)

**Verdict**: ❌ **Skip** — Heritage site monitoring data is **universally non-public** for security, conservation, and commercial reasons. RCU is unlikely to publish sensor data. If AlUla weather data is needed, check **NCM** (National Center for Meteorology) for regional weather stations instead.

**Alternative approaches**:
- **Satellite monitoring** — Landsat/Sentinel-2 can track vegetation changes (reforestation), surface temperature, and flood extent. Updated every 5-16 days.
- **Visitor statistics** — RCU may publish annual tourism reports with aggregate visitor counts. These are batch data, not real-time.
- **Archaeological research** — Published papers may include environmental data, but this is historical, not real-time.

Do not pursue AlUla sensor data unless RCU launches a public data initiative (unlikely).
