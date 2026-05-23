# Ministry of Hajj and Umrah - Pilgrim Flow and Crowd Monitoring

- **Country/Region**: Saudi Arabia (Makkah, Madinah, holy sites)
- **Endpoint**: Unknown (no public API found)
- **Protocol**: Unknown
- **Auth**: Unknown
- **Format**: Unknown
- **Freshness**: Real-time (crowd monitoring is continuous during Hajj)
- **Docs**: https://www.haj.gov.sa (no data portal)
- **Score**: 10/18

## Overview

The **Ministry of Hajj and Umrah** (وزارة الحج والعمرة) manages the world's largest annual human gathering: the **Hajj pilgrimage** to Makkah. Key facts:

- **~2-3 million pilgrims** attend Hajj annually (international + domestic)
- **~10 million Umrah pilgrims/year** (year-round minor pilgrimage)
- **5-day event** (8-12 Dhu al-Hijjah in the Islamic calendar)
- **Geographic concentration**: Pilgrims move between:
  - **Masjid al-Haram** (Grand Mosque, Makkah) — 400,000 capacity
  - **Mina** (tent city, 5 km from Makkah) — all pilgrims stay overnight
  - **Arafat** (plain, 15 km from Makkah) — all pilgrims gather on Day of Arafah
  - **Muzdalifah** (between Mina and Arafat) — overnight stop
  - **Madinah** (Prophet's Mosque, 400 km north) — most pilgrims visit before/after Hajj

**Logistics challenge**: Moving 2-3 million people between sites in a 5-day window is comparable to evacuating a major city. The 2015 Mina stampede killed 2,400+ pilgrims, underscoring the critical need for crowd management.

## Digital Hajj Initiatives

Saudi Arabia has invested heavily in **smart Hajj** technology:

1. **Nusuk platform** (https://nusuk.sa) — Official Hajj/Umrah booking and e-visa system. Pilgrims register, get permits, book transport/accommodation.

2. **Smart Hajj wristbands** — RFID bracelets with:
   - Pilgrim identity and medical records
   - Location tracking (RFID readers at checkpoints)
   - Emergency contact info

3. **Crowd density monitoring** — Cameras and sensors at:
   - Masjid al-Haram courtyards
   - Jamarat Bridge (site of 2015 stampede)
   - Mina tents
   - Arafat plain

4. **Command and Control Centers** — Real-time dashboards for authorities showing:
   - Crowd density heatmaps
   - Pilgrim flow rates (people/minute through chokepoints)
   - Transport capacity utilization (buses, metro, trains)
   - Medical incidents and ambulance dispatch

5. **Makkah Metro** (Al Mashaaer Al Mugaddassah Metro Line) — Dedicated metro line shuttling pilgrims between Mina, Arafat, and Muzdalifah during Hajj (operational since 2010).

## Potential Data Products

If the Ministry of Hajj published real-time data, it could include:

1. **Pilgrim arrivals** — Daily/hourly counts of pilgrims entering Saudi Arabia (by airport, land border, sea port)
2. **Site occupancy** — Current number of pilgrims at Masjid al-Haram, Mina, Arafat, Muzdalifah
3. **Crowd density** — Heatmaps or zone-level density (e.g., "Jamarat Bridge: 85% capacity")
4. **Transport load** — Buses dispatched, metro trains in service, capacity utilization
5. **Medical incidents** — Heatstroke cases, injuries (anonymized counts, not personal data)
6. **Permit issuance** — Number of Hajj/Umrah permits granted per day (via Nusuk)

**Update frequency**: During Hajj, these metrics change **minute-by-minute**. Outside Hajj, Umrah pilgrim counts are daily/weekly.

## Endpoint Analysis

**Ministry website**: `https://www.haj.gov.sa`

The Ministry's website provides pilgrim guidance, regulations, and Hajj news. **No public data portal or API** is advertised.

**Nusuk platform**: `https://nusuk.sa`

Nusuk is the official booking system for Hajj/Umrah permits. It likely has internal APIs for permit issuance, but these are not public.

**Attempted probes** (not tested due to lack of known endpoints):
```
https://api.haj.gov.sa/v1/pilgrims/count
https://data.haj.gov.sa/hajj/crowd-density
https://nusuk.sa/api/permits
```

**No developer documentation**: Neither the Ministry nor Nusuk publish API docs or open data initiatives.

**Comparison with event crowd monitoring**:

| Event/Authority | Attendance | Public data? | API? |
|-----------------|------------|--------------|------|
| **Hajj** | 2-3M | ❌ None | ❌ None |
| Times Square NYE | 1M | ❌ None | ❌ None |
| Olympics | Varies | ✅ Ticket sales | ❌ No crowd data |
| Music festivals | 100K+ | ❌ None | ❌ None |
| US election polls | — | ✅ Some | ✅ Some |

**Conclusion**: Crowd-level data for mass gatherings is almost never published in real-time due to:
- Security concerns (revealing crowd locations to bad actors)
- Privacy (tracking individual pilgrim movements)
- Commercial sensitivity (Hajj is managed by licensed tour operators)

## Integration Notes

- **No public API exists**: The Ministry of Hajj does not publish crowd or pilgrim data publicly. This is a **non-starter** unless policy changes.
- **Security concerns**: Real-time crowd density data could be exploited by bad actors (e.g., targeting high-density zones). Publishing is unlikely.
- **Aggregated statistics**: The Ministry does publish **post-Hajj statistics** (total pilgrim count, nationalities, demographics). These are batch data, not real-time.
- **Nusuk permit data**: Permit issuance counts (daily Hajj/Umrah permits granted) could be a lower-sensitivity metric, but this is not currently published.
- **Alternative: Twitter/social media**: During Hajj, the Ministry's official Twitter account (@MoHU_En) posts updates. These could be scraped, but are narrative, not structured data.

**Unique value if data existed**:
- **Largest human gathering** — Hajj is unmatched in scale and concentration.
- **Predictable event** — Hajj occurs annually on a known Islamic calendar date, enabling time-series analysis of crowd management improvements.
- **Public health relevance** — Hajj is studied by epidemiologists for infectious disease spread (meningitis, COVID-19, MERS-CoV).
- **Climate adaptation** — Hajj will shift into summer months in the 2030s-2040s (Islamic calendar is lunar). Heatstroke risk will increase. Real-time monitoring is life-saving.

## Scoring

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Crowd monitoring is real-time (if data existed) |
| Openness | 0 | No public data, no API, no portal |
| Stability | 3 | Ministry of Hajj is a permanent government body |
| Structure | 2 | Would likely be JSON (modern dashboard data) |
| Identifiers | 1 | No stable entity IDs (crowds are fluid, not keyed) |
| Additive value | 3 | **Globally unique** — no other dataset tracks 2-3M person gatherings |

**Total: 12/18** (if data existed)  
**Actual: 10/18** (penalized for zero public data and lack of stable IDs)

**Verdict**: ⏭️ **Reference** — This is a **high-value dataset that does not exist in public form** and is **unlikely to ever be published** due to security and privacy concerns. However, it is worth documenting as a "holy grail" source.

**Recommended action**:
1. **Monitor for open data initiatives** — Saudi Arabia's Vision 2030 includes digital transparency goals. If the Ministry launches a public dashboard (even aggregate daily pilgrim counts), reassess.
2. **Focus on post-Hajj statistics** — The Ministry publishes summary statistics after Hajj (total pilgrims, nationalities). These are batch data but still valuable. Consider a scraper for historical analysis.
3. **Alternative: Satellite imagery** — Crowd density at Mina and Arafat can be estimated from satellite imagery (Sentinel-2, Planet Labs). This is not real-time but is public.

If the Ministry of Hajj ever publishes real-time crowd data (even low-resolution, e.g., "Mina: 1.5M pilgrims present"), immediately escalate to ✅ **Build**. This would be a **flagship** addition to the repo and globally significant for crowd dynamics research.
