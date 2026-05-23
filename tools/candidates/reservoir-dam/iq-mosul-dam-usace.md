# Mosul Dam Monitoring - USACE / Trevi Grouting Telemetry

- **Country/Region**: Iraq (Mosul, Nineveh Governorate)
- **Endpoint**: Not publicly accessible
- **Protocol**: Unknown
- **Auth**: Restricted
- **Format**: Unknown
- **Freshness**: Unknown (likely real-time for internal monitoring)
- **Docs**: None public
- **Score**: 0/18

## Overview

Mosul Dam (also called Saddam Dam) on the Tigris River is the **most dangerous dam in the world** according to multiple engineering assessments. Key facts:
- **Largest dam in Iraq** — 3.4 km long, 131m high
- **Critical infrastructure** — provides water and electricity for northern Iraq
- **Foundation problem** — built on soluble gypsum bedrock that dissolves in water
- **Catastrophic failure risk** — if the dam fails, a 20-meter flood wave would hit Mosul (2 million people) within hours, killing hundreds of thousands and flooding Baghdad
- **Continuous grouting** — since 1986, the dam has required 24/7 foundation grouting (injecting concrete to fill voids as they form)
- **ISIS occupation** — the dam was briefly held by ISIS in 2014, halting grouting and accelerating deterioration

The dam's instrumentation includes:
- **Piezometers** — water pressure sensors in the foundation (detect seepage and void formation)
- **Extensometers** — measure foundation deformation
- **Tiltmeters** — measure dam body movement
- **Flow meters** — measure seepage through the foundation
- **Grouting injection tracking** — volume and location of concrete injections

This telemetry is monitored 24/7 by:
- **U.S. Army Corps of Engineers (USACE)** — has supported Iraq with dam safety assessments since 2003
- **Trevi Group (Italy)** — operates the grouting machinery under contract
- **Iraqi Ministry of Water Resources** — nominal owner/operator

**This data is among the most critical infrastructure monitoring in Iraq.** A real-time public feed would be invaluable for disaster preparedness.

## Endpoint Analysis

**No public access** — Mosul Dam telemetry is classified or restricted:

- **USACE** does not publish the data (considered sensitive infrastructure)
- **Trevi Group** operates under contract, data is proprietary
- **Iraqi government** does not publish the data

Searched for:
- USACE Mosul Dam public reports — only periodic engineering assessments (PDF reports, not real-time)
- Satellite monitoring — NASA/ESA satellite altimetry can detect gross changes in reservoir level, but not foundation instrumentation
- Academic papers — some researchers have published about Mosul Dam's condition, but no real-time data access

## Known Reporting

USACE has published warnings and assessments:
- 2007 — report called Mosul Dam "the most dangerous dam in the world"
- 2016 — after ISIS occupation, urgent warnings of potential collapse
- 2020s — situation improved due to resumed grouting, but risk remains

These are **periodic reports**, not real-time data feeds.

## Why It's Not Published

Likely reasons Mosul Dam telemetry is not public:
- **Security** — dam failure could be a target of sabotage/terrorism
- **Political sensitivity** — Iraqi government does not want to publicize the scale of the risk
- **Panic avoidance** — public real-time monitoring showing foundation deterioration could cause evacuations or panic
- **International relations** — U.S. involvement in monitoring is sensitive

## Alternative Monitoring

If Mosul Dam telemetry cannot be accessed, alternatives:
- **Satellite reservoir level** — NASA G-REALM or ESA Sentinel altimetry (monthly, not real-time)
- **News alerts** — monitor for emergency reports (via ReliefWeb or news scraping)
- **Seismic** — if dam failure occurred, USGS/EMSC would detect the flood wave impact

**None of these are substitutes for real-time instrumentation.**

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 0 | Data exists but not public |
| Openness | 0 | Restricted |
| Stability | 0 | N/A |
| Structure | 0 | N/A |
| Identifiers | 0 | N/A |
| Richness | 0 | N/A |

**Verdict**: ❌ **Skip** — This is the **single most valuable dam/water infrastructure monitoring dataset in Iraq**, possibly in the world given the catastrophic failure risk. But it is **classified/restricted and not publicly accessible**. USACE and Trevi Group monitor the dam 24/7 but do not publish telemetry. Iraqi government does not publish it. **If Mosul Dam monitoring data ever becomes public (extremely unlikely for security reasons), it should be added immediately as top-priority critical infrastructure.** For now, no implementation is possible.

**Note**: This is worth documenting even as a dead end because it highlights a critical gap in Iraq's infrastructure transparency. The dam poses existential risk to millions, but the monitoring data is not public.
