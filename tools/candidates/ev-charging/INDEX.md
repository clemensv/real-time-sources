# EV Charging Candidates

EV charging station registries and real-time availability data sources. The EV charging landscape is fragmented — no single standard dominates like GBFS does for bikeshare. Two standards are emerging: OCPI (Open Charge Point Interface) for data exchange and OICP (Open InterCharge Protocol) for roaming. EU AFIR (Alternative Fuels Infrastructure Regulation) mandates real-time availability data publication via National Access Points by 2025.

## Tier 1 — Real-Time Status, Open Access

These sources provide genuine real-time connector/EVSE status with open or free-registration access. Build bridges for these first.

| Candidate | Region | Score | Protocol | Key Value |
|-----------|--------|-------|----------|-----------|
| [NDL Netherlands](ndl-netherlands.md) | Netherlands | **18/18** | OCPI files | Complete Dutch data; real-time EVSE status; no auth; OCPI v2.2 |
| [NOBIL Norway](nobil-norway.md) | Nordics | **18/18** | REST | Gov registry; real-time connector status; CC BY 4.0; covers NO/SE/FI |
| [Switzerland BFE](switzerland-bfe.md) | Switzerland | 16/18 | OICP JSON | Real-time; Hubject-compatible EVSE IDs; OICP format; no auth |
| [Korea Environment Corp.](korea-environment-corporation.md) | South Korea | 15/18 | REST | Real-time charger status; 200K+ points; free API key (data.go.kr) |

## Tier 2 — Strong Registry, Limited/No Real-Time

Rich station data with daily or near-real-time updates, but no (or limited) connector-level live status.

| Candidate | Region | Score | Protocol | Key Value |
|-----------|--------|-------|----------|-----------|
| [Open Charge Map](open-charge-map.md) | **Global** | 17/18 | REST | 300K+ locations in 180 countries; global aggregator |
| [AFDC / NREL](afdc-nrel.md) | US + Canada | 17/18 | REST | 70K+ US stations + 16K+ Canadian; 90+ networks; DOE/NREL |
| [NRCan Canada](nrcan-canada.md) | Canada | 15/18 | REST (AFDC) | Canadian data via AFDC API; bilingual EN/FR |
| [France IRVE](france-irve.md) | France | 15/18 | CSV/GeoJSON | 100K+ points; legally mandated; daily updates; no dynamic yet |
| [supercharge.info](supercharge-info.md) | **Global** | 13/18 | REST | Tesla Supercharger network; 7K+ sites; open API; no auth |
| [Bundesnetzagentur](bundesnetzagentur-ladesaeulen.md) | Germany | 13/18 | CSV download | Official German register; monthly updates; no real-time |
| [OpenStreetMap](openstreetmap-charging.md) | **Global** | 12/18 | Overpass QL | 200K+ stations globally; ODbL; community-maintained |
| [ChargePlace Scotland](chargeplace-scotland.md) | UK — Scotland | 12/18 | REST | Government network; limited scope and access |
| [GoingElectric](goingelectric.md) | Europe (DACH) | 11/18 | REST | 70K+ European stations; community-verified; ADAC-owned |

## Tier 3 — Limited Access or Static Only

Government registries, commercial platforms, or sources with no public API or significant access barriers.

| Candidate | Region | Score | Protocol | Key Value |
|-----------|--------|-------|----------|-----------|
| [Eco-Movement](eco-movement.md) | **Global** | 15/18 | Commercial | 700K+ connectors; real-time; Apple Maps data provider; paid |
| [Gireve](gireve.md) | Europe | 15/18 | OCPI/eMIP | 680K+ points; European roaming hub; B2B commercial |
| [Hubject](hubject-oicp.md) | **Global** | 15/18 | OICP | 600K+ points; global roaming; OICP standard; B2B commercial |
| [Chargeprice](chargeprice.md) | Europe | 10/18 | REST | Pricing comparison; 35+ countries; commercial API |
| [Austria E-Control](austria-e-control.md) | Austria | 9/18 | XLSX download | Government register; periodic updates; website in transition |
| [Denmark Energistyrelsen](denmark-energistyrelsen.md) | Denmark | 9/18 | Unknown | Nordic gap (NOBIL doesn't cover DK); AFIR implementation pending |
| [Portugal Mobi.E](portugal-mobie.md) | Portugal | 9/18 | Web only | 14K+ points; centralized national network; no public API |
| [UK NCR](uk-ncr-decommissioned.md) | UK | **0/18** | ⚠️ DEAD | **Decommissioned Nov 2024** — significant UK data gap |

## Recommended Approach

### Phase 1: Real-Time OCPI/OICP Bridges
1. **NDL Netherlands (OCPI)** — Gold standard. Real-time EVSE status, OCPI format, no auth. Building an OCPI parser means the same code works with any OCPI-compliant source.
2. **NOBIL Norway (REST)** — Real-time connector status across Nordics. Delta-dump via `fromdate` enables efficient change tracking.
3. **Switzerland BFE (OICP)** — Real-time, Hubject-compatible EVSE data. Building an OICP parser means the same code works with Hubject-connected sources across Europe.
4. **Korea Environment Corp. (REST)** — Real-time charger status for Asia's densest network. Free API key.

### Phase 2: Major Registries
5. **AFDC/NREL** — Definitive US+Canada source. 70K+ stations, 90+ networks, daily updates. Free API key.
6. **Open Charge Map** — Global fallback. 300K+ locations in 180 countries. `modifiedsince` enables delta polling.
7. **France IRVE** — 100K+ points, government-mandated. Watch for dynamic data consolidation under AFIR.

### Phase 3: Specialty Sources
8. **supercharge.info** — Tesla Supercharger global tracking. Open API, no auth.
9. **OpenStreetMap** — Global baseline via Overpass API. ODbL license.
10. **GoingElectric** — European community data with DACH depth.

### Not Recommended (for open-data use)
- **Eco-Movement, Gireve, Hubject** — commercially licensed; excellent data but not openly accessible.
- **Chargeprice** — pricing-focused, commercial.
- **UK NCR** — decommissioned.

## Coverage Summary

### By Region
- **North America**: AFDC/NREL (US+Canada) — comprehensive
- **Nordics**: NOBIL (Norway, Sweden, Finland) — real-time; Denmark gap
- **Netherlands**: NDL — gold standard, real-time OCPI
- **Germany**: Bundesnetzagentur (static registry)
- **France**: IRVE (static, 100K+ points; dynamic schema defined but not consolidated)
- **Switzerland**: BFE (real-time OICP)
- **Austria**: E-Control (static registry, limited format)
- **UK**: ⚠️ Gap — NCR decommissioned Nov 2024; ChargePlace Scotland covers Scotland only
- **Portugal**: Mobi.E (14K+ points, no public API)
- **Denmark**: Gap — NOBIL doesn't cover Denmark; AFIR implementation pending
- **South Korea**: Korea Environment Corp. (real-time, 200K+ points)
- **Global**: Open Charge Map (180 countries), OpenStreetMap, supercharge.info (Tesla)

### By Protocol
- **OCPI**: NDL Netherlands — build this parser first
- **OICP**: Switzerland BFE — Hubject-compatible
- **REST (custom)**: NOBIL, AFDC, Korea, OCM, GoingElectric
- **File download**: France IRVE (CSV/GeoJSON), Bundesnetzagentur (CSV), Austria (XLSX)

### Real-Time Status Availability
- ✅ **Real-time connector/EVSE status**: NDL, NOBIL, Switzerland BFE, Korea
- ⚡ **Station-level status only**: AFDC (Available/Planned/Temp Unavailable)
- ❌ **Static registry only**: France IRVE, Bundesnetzagentur, Austria, Denmark, OSM
- 🔒 **Real-time but commercial**: Eco-Movement, Gireve, Hubject

### Key Standards
- **OCPI v2.2** (Open Charge Point Interface) — Location/EVSE/Connector hierarchy; used by NDL, Gireve, many CPOs
- **OICP** (Open InterCharge Protocol) — EVSEData/EVSEStatus; used by Switzerland BFE, Hubject
- **EU AFIR** — mandates real-time data publication via National Access Points by 2025; will drive more open data sources
- **eMI3** — EVSE ID standard (e.g., `CH*CCI*E22078`); used by OICP, increasingly by OCPI
- **AFIREV** — French variant of eMI3 for charging point IDs
