# UAE Real-Time Data Source Discovery Report

**Date**: 2025-01-23  
**Country**: United Arab Emirates (الإمارات العربية المتحدة), ISO 3166-1: AE  
**Coverage**: Federal + All Seven Emirates (Abu Dhabi, Dubai, Sharjah, Ajman, Umm Al-Quwain, Ras Al Khaimah, Fujairah)

---

## Executive Summary

**Total candidates evaluated**: 24  
**Verdict breakdown**:
- **Build** (score 15–18, production-ready): **2 candidates**
- **Maybe** (score 10–14, pending endpoint discovery): **17 candidates**
- **Skip** (score <10, WAF-blocked, overlaps existing sources, or too infrequent): **5 candidates**

**Top findings**:
1. ✅ **Careem BIKE Dubai** and **Yaldi Dubai** are production-ready GBFS feeds (no auth, real-time, comprehensive)
2. 🔍 **NCM weather**, **FANR radiation**, **DEWA solar**, **EAD air quality** are high-value but endpoints require discovery
3. 🚫 **RTA Dubai traffic/transit** is blocked by aggressive WAF despite data existing
4. ❌ **Bayanat.ae** (federal data portal) is unreachable, hindering centralized discovery
5. 🇦🇪 **UAE is data-mature** but access is fragmented across agencies with inconsistent open data practices

---

## Detailed Results by Domain

### 🚴 Bikeshare / Micromobility (GBFS)

| Source | Endpoint | Verdict | Score | Key Findings |
|--------|----------|---------|-------|--------------|
| **Careem BIKE Dubai** | careem.publicbikesystem.net/customer/gbfs/v3.0 | **BUILD** ✅ | 16/18 | 223 stations, GBFS 3.0, no auth, real-time availability |
| **Yaldi Dubai** | yaldi.rideatom.com/gbfs/511/v3.0 | **BUILD** ✅ | 16/18 | Free-floating e-scooters, vehicle-level tracking |
| **Dott (5 emirates)** | ridedott.com/public/v2/{city}/gbfs.json | **MAYBE** ⚠️ | TBD | Feeds return empty []; likely defunct |

---

### 🌦️ Weather & Atmospheric

| Source | Agency | Verdict | Score | Notes |
|--------|--------|---------|-------|-------|
| **NCM Weather Network** | National Center of Meteorology | **MAYBE** ⚠️ | TBD | 86+ AWS, 5 radars, lightning, marine buoys; WAF blocks all endpoints |
| **NCM Lightning** | NCM or Blitzortung.org | **MAYBE** ⚠️ | 14–16 | Check Blitzortung.org coverage for UAE |

---

### 🏭 Air Quality

| Source | Agency | Verdict | Score | Notes |
|--------|--------|---------|-------|-------|
| **EAD Abu Dhabi AQ** | Environment Agency Abu Dhabi | **MAYBE** ⚠️ | 14–16 | Check maps.ead.gov.ae ArcGIS |
| **Dubai Municipality AQ** | Dubai Municipality | **MAYBE** ⚠️ | 14–16 | Check dm.gov.ae |
| **Sensor.Community UAE** | Citizen network | **MAYBE** ⚠️ | 13–15 | API verified; check if UAE has active sensors |

---

### ⚡ Energy & Grid

| Source | Network | Verdict | Score | Notes |
|--------|---------|---------|-------|-------|
| **DEWA MBR Solar Park** | Dubai Electricity & Water Authority | **MAYBE** ⚠️ | 16–17 | 2,427 MW (world top-5 solar park); check DEWA open data |
| **GCCIA Grid** | Gulf Cooperation Council Interconnection | **MAYBE** ⚠️ | 15–17 | Cross-border power flows; check gccia.com.sa |

---

### ☢️ Radiation Monitoring

| Source | Agency | Verdict | Score | Notes |
|--------|--------|---------|-------|-------|
| **FANR Barakah NPP** | Federal Authority for Nuclear Regulation | **MAYBE** ⚠️ | 15–17 | First Arab NPP; environmental monitoring network expected |

---

### 🚗 Road Traffic & Transit

| Source | Agency | Verdict | Score | Notes |
|--------|--------|---------|-------|-------|
| **RTA Dubai Traffic/Parking** | Roads & Transport Authority | **SKIP** ❌ | Blocked | WAF blocks all automated access |
| **RTA/DoT GTFS-RT** | RTA + Abu Dhabi DoT | **MAYBE** ⚠️ | 15–16 | Reverse-engineer S'hail / Darb apps |
| **Etihad Rail** | UAE National Railway | **FUTURE** 🔮 | 17–18 | Launches 2025–2026; expect GTFS-RT |

---

### 🚢 Maritime, Tidal, & Coastal

| Source | Coverage | Verdict | Score | Notes |
|--------|----------|---------|-------|-------|
| **AISstream UAE** | Dubai, Abu Dhabi, Fujairah ports | **SKIP** ❌ | N/A | Already covered by global \`aisstream\` |
| **EAD Coastal Monitoring** | Abu Dhabi marine/tidal | **MAYBE** ⚠️ | 12–15 | 50+ marine stations; check EAD ArcGIS |
| **Dubai/Abu Dhabi Ferries** | RTA + DoT | **MAYBE** ⚠️ | 13–15 | Low priority (small fleet) |

---

### 🔌 EV Charging & Parking

| Source | Operator | Verdict | Score | Notes |
|--------|----------|---------|-------|-------|
| **DEWA Green Charger** | Dubai Electricity & Water Authority | **MAYBE** ⚠️ | 15–16 | 300+ charging points; reverse-engineer DEWA Smart App |
| **Open Charge Map UAE** | Global aggregator | **MAYBE** ⚠️ | 13/18 | Static registry only (no real-time status) |
| **Smart Parking** | RTA + Abu Dhabi ITC | **SKIP** ❌ | Blocked | RTA WAF-blocked; low priority |

---

### 🚨 Disaster Alerts

| Source | Agency | Verdict | Score | Notes |
|--------|--------|---------|-------|-------|
| **NCEMA / NCM Alerts** | National Emergency & NCM | **MAYBE** ⚠️ | 14–16 | Fog, dust, extreme heat warnings; check for CAP feeds |

---

### 💧 Water Quality & Hydrology

| Source | Agency | Verdict | Score | Notes |
|--------|--------|---------|-------|-------|
| **Dubai Beach Water Quality** | Dubai Municipality | **SKIP** ❌ | 10–12 | Weekly sampling (too infrequent) |
| **UAE Groundwater** | EAD, MOCCAE | **SKIP** ❌ | Low | Monthly-quarterly (too infrequent) |

---

### ❌ Overlaps with Global Sources (Not New)

| Domain | Global Source | Verdict |
|--------|---------------|---------|
| **Seismology** | USGS (global) | **SKIP** — bounding box filter of existing source |
| **Aviation ADS-B** | OpenSky/ADSBexchange | **SKIP** — already covers UAE airspace |

---

## 🏆 Top 5 Picks (Immediate Build Candidates)

### 1. **Careem BIKE Dubai (GBFS)** ✅
- **Why**: Production-ready, no auth, 223 stations, GBFS 3.0, real-time
- **Impact**: Establishes GBFS protocol in repo
- **Effort**: Low (standard GBFS)

### 2. **Yaldi Dubai (GBFS)** ✅
- **Why**: Free-floating e-scooters, vehicle-level tracking
- **Impact**: Multi-operator GBFS pattern
- **Effort**: Low (same bridge as Careem)

### 3. **NCM Weather Network** ⚠️ *(pending discovery)*
- **Why**: 86+ AWS, radar, lightning; federal authority; unique Gulf datasets
- **Impact**: **Highest scientific value** in UAE
- **Effort**: Medium-High (WAF bypass, app reverse-engineering, or direct contact)

### 4. **FANR Barakah Radiation** ⚠️ *(pending discovery)*
- **Why**: First Arab NPP, establishes radiation domain, international norm
- **Impact**: Unique dataset, high public interest
- **Effort**: Medium (direct FANR contact)

### 5. **DEWA MBR Solar Park** ⚠️ *(pending discovery)*
- **Why**: World top-5 solar park, climate leadership
- **Impact**: Renewable energy transition analytics
- **Effort**: Medium (DEWA open data initiative)

---

## 🚧 Notable Gaps & Blockers

### Blocked by WAF / Infrastructure
- **RTA Dubai**: Traffic/parking XML feeds blocked by aggressive WAF
- **Bayanat.ae**: Federal portal unreachable (timeouts)
- **Dubai Pulse / Dubai Data**: Emirate portals unreachable

### Endpoints Not Found (Despite Operational Systems)
- **NCM weather API**: System exists but API unknown
- **GCCIA grid**: No public transparency platform found
- **RTA/DoT GTFS-RT**: Mobile apps exist but no public feeds

### Data Too Infrequent
- **Beach water quality**: Weekly (below real-time threshold)
- **Groundwater**: Monthly-quarterly

### Future Sources
- **Etihad Rail**: Launches 2025–2026; expect GTFS-RT

---

## 🌍 Cross-Gulf Observations

**UAE is the most data-mature Gulf country**, but:
- **Execution gap**: Many announced platforms (Bayanat, Dubai Pulse) are incomplete/unreachable
- **Pan-GCC opportunities**: GCCIA grid, NCM seismic network
- **Unique Gulf datasets**: Extreme fog, dust storms, hypersaline marine environment, cloud seeding

---

## 📋 Recommendations

### Immediate (Low-Hanging Fruit)
1. ✅ Deploy Careem + Yaldi GBFS
2. Check Sensor.Community API for UAE sensors (1-min query)
3. Verify Blitzortung lightning coverage

### High Priority (1–2 Weeks)
4. NCM weather API hunt (app reverse-engineering, direct contact)
5. EAD ArcGIS probing (air quality, marine, groundwater)
6. RTA/DoT GTFS-RT reverse-engineering (S'hail, Darb apps)

### Medium Priority (2–4 Weeks)
7. FANR radiation monitoring (fanr.gov.ae, direct contact)
8. DEWA solar generation (DEWA open data, app reverse-engineering)
9. GCCIA grid transparency (gccia.com.sa, Saudi data.gov.sa)

### Low Priority / Contingent
10. Bayanat.ae CKAN queries (if portal becomes accessible)
11. RTA WAF bypass (requires direct contact for API key)
12. Etihad Rail monitoring (2025 watchlist)

---

## 🎯 Conclusion

**UAE offers rich real-time data potential, but access is fragmented:**

✅ **Success**: Careem, Yaldi GBFS (production-ready)  
⚠️ **High-value but gated**: NCM, FANR, DEWA, EAD  
❌ **Blocked**: RTA (WAF), Bayanat/Dubai Pulse (portal downtime)  
🔮 **Future**: Etihad Rail (2025–2026)

**The UAE is data-mature but not yet data-open.** Direct agency engagement required to unlock the full catalog.

**Total viable for immediate build**: 2 (Careem, Yaldi)  
**High-value pending discovery**: ~8 (NCM, FANR, DEWA, EAD, GCCIA, RTA GTFS-RT, alerts)

**Recommended focus**: Deploy GBFS now. Invest 2–4 weeks in NCM, FANR, EAD discovery.

---

**End of Report**
