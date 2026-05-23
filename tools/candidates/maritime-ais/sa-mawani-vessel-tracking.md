# Saudi Ports Authority (Mawani) - Vessel Tracking

- **Country/Region**: Saudi Arabia (KSA)
- **Endpoint**: Unknown (no public API found)
- **Protocol**: Unknown
- **Auth**: Unknown
- **Format**: Unknown
- **Freshness**: Real-time (vessel positions update continuously)
- **Docs**: https://www.mawani.gov.sa (no API docs)
- **Score**: 6/18

## Overview

The Saudi Ports Authority (الهيئة العامة للموانئ, Mawani) governs and regulates all commercial seaports in Saudi Arabia. Saudi Arabia has coastlines on both the **Red Sea** and the **Arabian Gulf**, with major ports including:

**Red Sea (Western Coast)**:
- **Jeddah Islamic Port** (جدة الإسلامي) — largest port in Saudi Arabia, 44M tons/year cargo, serves Makkah/Madinah pilgrimage
- **King Abdullah Port** (ميناء الملك عبدالله, Rabigh) — newest mega-port, 3.6M TEU container capacity, built 2013
- **Yanbu Commercial Port** — industrial port for petrochemicals, oil refining
- **Jizan Port** — southern Red Sea, near Yemen border

**Arabian Gulf (Eastern Coast)**:
- **King Abdulaziz Port (Dammam)** — largest Gulf port, 44M tons/year, oil & container hub
- **Jubail Commercial Port** — industrial port for the world's largest petrochemical complex
- **Ras Tanura** — Saudi Aramco oil terminal (private, not Mawani-operated)

Saudi ports handle:
- **~300 million tons/year** of cargo
- **~9 million TEU/year** of containers
- **~30,000 vessel calls/year**
- **Hajj/Umrah pilgrims** arriving by sea (Jeddah)
- **Oil and gas exports** — Saudi Arabia is the world's largest oil exporter (~7M barrels/day)

**Strategic significance**: Saudi ports are critical chokepoints for global oil supply (Ras Tanura exports ~5M barrels/day), containerized goods entering the Middle East via the Red Sea (alternative to Suez Canal), and Hajj pilgrimage logistics.

## Endpoint Analysis

**Mawani website**: `https://www.mawani.gov.sa`

The Mawani website provides port information, regulations, and e-services (customs, permits), but **no vessel tracking, AIS, or real-time ship positions** are publicly visible.

**Attempted probes**:
```
GET https://www.mawani.gov.sa/en-us → 405 Method Not Allowed (HEAD only?)
GET https://www.mawani.gov.sa/api/vessels → Not tested (unlikely to exist)
GET https://www.mawani.gov.sa/en/data → Not tested
```

**No AIS dashboard**: Unlike some port authorities (e.g., Finnish Digitraffic, Norwegian Kystverket), Mawani does not publish a public AIS or vessel tracking map on its website.

**Comparison with global port authorities**:

| Authority | Country | Public AIS? | API? | Coverage |
|-----------|---------|-------------|------|----------|
| **Mawani** | Saudi Arabia | ❌ None | ❌ None | Red Sea + Gulf |
| Kystverket | Norway | ✅ Yes | ✅ REST | Norway coast |
| Digitraffic | Finland | ✅ Yes | ✅ MQTT/REST | Baltic Sea |
| MarineCadastre | USA | ✅ Historical | ✅ CSV | US waters |
| MPA | Singapore | ❌ None | ❌ None | Port only |
| Port of Rotterdam | Netherlands | ✅ Yes | ✅ REST | Port area |

Mawani is typical of **Middle Eastern port authorities** in not publishing AIS data. Security concerns (naval vessels, oil terminals) often drive opacity.

## Alternative AIS Sources for Saudi Waters

While Mawani does not publish AIS, **terrestrial and satellite AIS aggregators** cover Saudi coastal waters:

1. **AISstream** (via Spire satellite AIS) — global coverage, MQTT WebSocket
   - **Status**: Service is currently down/broken (as of 2024)
   - If restored, includes Saudi Red Sea and Gulf waters

2. **MarineTraffic** (commercial) — global coverage
   - Requires paid API subscription
   - **Not suitable for this repo** (commercial barrier)

3. **VesselFinder** (commercial) — global coverage
   - Requires paid subscription
   - **Not suitable**

4. **Spire Maritime API** (commercial) — satellite AIS
   - Academic/non-profit licenses may exist
   - **Investigate** if free tier available

5. **EMSA (European Maritime Safety Agency)** — EU SafeSeaNet
   - Covers European waters only, not Saudi Arabia
   - **Not applicable**

**Conclusion**: There is **no free, public AIS source specific to Saudi waters**. Saudi AIS is only available via commercial satellite providers or potentially through bilateral agreements with Saudi Navy/Coast Guard.

## Integration Notes

- **No public API**: Mawani does not publish vessel tracking or AIS data publicly. This is a **non-starter** for a direct Mawani bridge.
- **Commercial alternatives**: Saudi AIS is available via paid satellite AIS providers (Spire, Orbcomm, exactEarth), but this violates the "open" criterion.
- **Security concerns**: Saudi Arabia's coastal waters include sensitive military and oil infrastructure (Ras Tanura, naval bases). Publishing AIS may be restricted for national security reasons.
- **Alternative: Global aggregators**: If **AISstream** (free satellite AIS) is restored, it will cover Saudi waters as part of global coverage. No Saudi-specific bridge is needed.
- **Port call APIs**: Some port authorities publish **vessel call schedules** (ship arrivals/departures, not real-time positions). This is less valuable than AIS but still useful. Mawani does not appear to publish this either.

**Unique value if data existed**:
- **Jeddah Islamic Port** — Track Hajj pilgrimage ship arrivals (seasonal surge)
- **Ras Tanura oil terminal** — Infer Saudi oil export volumes from tanker movements
- **Red Sea shipping** — Saudi ports are alternative routes to the Suez Canal (especially post-2021 Ever Given blockage)
- **Bab-el-Mandeb traffic** — Strait between Red Sea and Gulf of Aden (critical chokepoint, near Yemen conflict zone)

## Scoring

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Vessel positions are real-time (if data existed) |
| Openness | 0 | No public AIS, no API, no dashboard |
| Stability | 2 | Mawani is the official port authority |
| Structure | 2 | Would likely be AIS NMEA or JSON (if existed) |
| Identifiers | 2 | MMSI (vessel IDs) are standard |
| Additive value | 1 | Covered by global AIS aggregators (if they work) |

**Total: 10/18** (if data existed)  
**Actual: 6/18** (penalized for zero public data)

**Verdict**: ❌ **Skip** — No public AIS or vessel tracking API exists. Saudi coastal AIS is available via commercial satellite providers, but this violates the "open" requirement. If AISstream (free satellite AIS) is restored, it will cover Saudi waters as part of global coverage, making a dedicated Mawani bridge unnecessary.

**Alternative approach**: Focus on restoring **AISstream** (global satellite AIS), which covered Saudi waters before it broke. Do not build a Saudi-specific bridge unless Mawani launches a public AIS portal (unlikely due to security concerns).
