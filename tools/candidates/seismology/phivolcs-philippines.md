# PHIVOLCS — Philippine Institute of Volcanology and Seismology

**Country/Region**: Philippines
**Publisher**: PHIVOLCS, Department of Science and Technology (DOST)
**API Endpoint**: `https://earthquake.phivolcs.dost.gov.ph/` (web portal — connection failed)
**Documentation**: https://www.phivolcs.dost.gov.ph/
**Protocol**: Web portal (HTML)
**Auth**: N/A (no public API discovered)
**Data Format**: HTML
**Update Frequency**: Real-time earthquake bulletins (within minutes); daily volcanic advisories
**License**: Philippine government data

## What It Provides

PHIVOLCS monitors two of the most active geological hazard domains on Earth:

### Seismology
The Philippines sits on the Pacific Ring of Fire with **multiple active fault systems** (Philippine Fault Zone, Manila Trench, Philippine Trench). PHIVOLCS operates the Philippine Seismic Network with ~100 seismograph stations. The country experiences thousands of earthquakes annually, including several destructive events per decade.

### Volcanology
The Philippines has **24 active volcanoes** including:
- **Taal** — one of the world's most dangerous volcanoes (erupted January 2020)
- **Mayon** — most active Philippine volcano; near-perfect cone
- **Pinatubo** — produced the 20th century's largest eruption (1991)
- **Kanlaon**, **Bulusan**, **Hibok-Hibok** — regularly active

PHIVOLCS issues volcano bulletins, lahar warnings, and maintains 24/7 monitoring for volcanic earthquakes, gas emissions, and ground deformation.

### Probe Results

Connection to `earthquake.phivolcs.dost.gov.ph` **failed** (connection timeout). This is consistent with earlier repository research in Round 1 (seismology INDEX.md notes "Connection failed"). The main PHIVOLCS site at `phivolcs.dost.gov.ph` was also not accessible during testing.

This may indicate:
1. Geographic network routing issues
2. Server maintenance or upgrade
3. Infrastructure limitations
4. Intermittent availability

### Known Data Format

Based on URL patterns observed in links and cached pages:
- Earthquake bulletins: HTML pages at `/2026_Earthquake_Information/Month/filename.html`
- Volcano bulletins: HTML pages organized by volcano and date
- No JSON/XML API endpoints documented

## Freshness Assessment

PHIVOLCS issues earthquake information bulletins within minutes of significant events and daily volcano advisories. The data infrastructure is operational (PHIVOLCS is internationally recognized and contributes to USGS/EMSC global catalogs). However, the public-facing web infrastructure appears unreliable from international access points.

## Entity Model

- **Earthquake**: Location, magnitude, depth, origin time, felt intensity (PHIVOLCS Earthquake Intensity Scale)
- **Volcano**: Named with alert level (0-5), eruption history, monitoring parameters
- **Volcanic Earthquake**: Tremor counts and magnitudes near active volcanoes
- **Lahar Warning**: Rain-triggered warnings for post-eruption areas
- **Tsunami Advisory**: Generated for significant submarine earthquakes

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Bulletins issued within minutes; but web infrastructure unreliable |
| Openness | 0 | Connection failures; no public API documented |
| Stability | 1 | Government agency but web infrastructure issues |
| Structure | 0 | HTML bulletins only; no machine-readable format |
| Identifiers | 1 | Event descriptions; no standardized IDs visible |
| Additive Value | 3 | 24 active volcanoes; Ring of Fire seismicity; globally significant monitoring |
| **Total** | **7/18** | |

## Integration Notes

- **Not currently viable** — connection failures and no public API
- Philippine earthquake data is available through USGS and EMSC global feeds (with some delay)
- Philippine volcanic data is partially available through Smithsonian GVP
- PHIVOLCS contributes FDSN waveform data to the global network — but event catalogs aren't in FDSN format
- The volcanic monitoring capability is globally significant — 24 active volcanoes in a densely populated country
- Worth revisiting periodically — DOST has been investing in digital infrastructure

## Verdict

Critically important but inaccessible. PHIVOLCS monitors some of the most active volcanoes and seismic zones on Earth, but their web infrastructure was unreachable during testing and no public API exists. Philippine geological hazard data is partially available through global aggregators (USGS, EMSC, Smithsonian GVP) but the local detail and speed of PHIVOLCS bulletins would be uniquely valuable if API access becomes available.
