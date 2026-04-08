# Mobilithek AFIR EV Charging (Germany NAP)

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness (0-3) | 3 | Dynamic data is real-time (seconds), static data updated daily |
| Openness (0-3) | 2 | Most offers are Open Data; some providers return 403 on noauth endpoint (need auth for those); Keycloak OIDC auth available |
| Stability (0-3) | 3 | Federal government platform (BMDV), AFIR regulation mandates data provision, Mobilithek is Germany's official NAP |
| Structure (0-3) | 3 | DATEX II v3 JSON with published JSON Schema profiles; well-defined hierarchical model |
| Identifiers (0-3) | 3 | EVSE IDs in eMI3 format (e.g. DE*TNK*E00163*01), site UUIDs, station UUIDs — all stable |
| Richness (0-3) | 3 | Static: name, address, coordinates, operator, helpdesk, authentication methods, power, connector types, opening hours, NUTS region. Dynamic: real-time status per charging point |
| **Total** | **17/18** | |

**Verdict: VIABLE — Top-tier source**

## Upstream

- **Platform**: Mobilithek (mobilithek.info) — Germany's National Access Point (NAP) for mobility data
- **Operator**: Bundesministerium für Digitales und Verkehr (BMDV)
- **Regulation**: EU Alternative Fuels Infrastructure Regulation (AFIR), mandatory from April 14, 2026
- **Data model**: DATEX II v3 with AFIR-Recharging profiles (Static-01-00-00, Dynamic-01-00-00_Delta)
- **Schema repo**: github.com/MobilithekDE/AFIR-Recharging-Profil Version 01-00-00

## API Access

### Noauth Endpoint (no authentication required)
```
GET https://mobilithek.info/mdp-api/mdp-conn-server/v1/publication/{offerID}/file/noauth
Accept-Encoding: gzip
```
Returns gzip-compressed DATEX II v3 JSON. Works for some providers, returns 403 for others.

### Authenticated Endpoint
```
GET https://mobilithek.info/mdp-api/mdp-conn-server/v1/publication/{offerID}/file/access
Authorization: Bearer {JWT}
```
JWT obtained via Keycloak OIDC at `https://mobilithek.info/auth/realms/MDP`.

### Metadata API
```
GET https://mobilithek.info/mdp-api/mdp-msa-metadata/v2/offers/{offerID}
```

### Schema Files
```
GET https://mobilithek.info/mdp-api/files/aux/schemas/DATEX_2_V3/{profile}/{filename}.json
```

## Verified Providers (from 65 offers in "Tank- und Ladestationen")

### DATEX II V3 Brokered + Open Data (38 DATEX II V3 of 65 total, 44 brokered)

| Provider | Stat Offer ID | Dyn Offer ID | Coverage | Noauth |
|----------|--------------|--------------|----------|--------|
| chargecloud GmbH | 978597062404620288 | 978598831184601088 | All 16 states | ✅ Yes |
| Volkswagen Group Charging | 976221024898781184 | 976223649023320064 | Deutschland | ❌ 403 |
| Аmpeco Ltd. (own) | 973272258671685632 | 973271761172537344 | All 16 states | untested |
| Аmpeco Ltd. (E.ON Drive) | 972837891969273856 | 972842599324557312 | All 16 states | untested |
| Qwello Deutschland GmbH | 972963216296222720 | 972966368902897664 | Deutschland | untested |
| ELU Mobility | — | 971513500454850560 | BW only | untested |
| msu solutions (m8mit) | 970305056590979072 | 970388804493828096 | Deutschland | untested |
| 800 Volt Technologies (PUMP) | 969322788846231552 | — | Deutschland | untested |
| SMATRICS GmbH & Co KG | 969239629194518528 | 961319990963605504 | Deutschland | untested |
| Monta ApS | 963836072152719360 | — | All 16 states | untested |
| ENIO GmbH | — | — | Deutschland | untested |
| Grid & Co. GmbH | 963884581258190848 | 963780195509002240 | Deutschland | Intern |
| Eco-Movement | 954064102947180544 | 955166494396665856 | Deutschland | ❌ 403 |
| Tesla Germany GmbH | 953828817873125376 | 953843379766972416 | Deutschland | ✅ Yes |
| EnBW AG | (pages 4-7) | (pages 4-7) | | untested |
| Smartlab (ladenetz.de) | (pages 4-7) | (pages 4-7) | | untested |
| Wirelane GmbH | (pages 4-7) | (pages 4-7) | | untested |
| eliso GmbH | (pages 4-7) | (pages 4-7) | | untested |
| Hochschule Landshut | (pages 4-7) | (pages 4-7) | | untested |

### Non-DATEX Offers (NOW GmbH / Nationale Leitstelle)
| Offer | Model | Notes |
|-------|-------|-------|
| Bundesnetzagentur Liste der Ladesäulen (Webservice) | — | All 16 states, Not brokered, enriched BNetzA data |
| Lkw-Schnellladenetz an Rastanlagen | Sonstige | 350 truck charging locations, planning data |
| Böttcher Energie Tankstelle Regensburg | DATEX II V2 | MB Energy, single location, restricted license |

## Data Structure

### Static (AFIR-Recharging-Static-01-00-00)
```
payload
  └─ aegiEnergyInfrastructureTablePublication
       ├─ publicationTime, publicationCreator, lang
       └─ energyInfrastructureTable[]
            └─ energyInfrastructureSite[]
                 ├─ idG (UUID), name, lastUpdated
                 ├─ locationReference (lat/lon, address, NUTS)
                 ├─ operator (name, operatorId)
                 ├─ helpdesk (phone)
                 ├─ operatingHours, accessibility, serviceType
                 └─ energyInfrastructureStation[]
                      ├─ idG (UUID), totalMaximumPower
                      ├─ authenticationMethods, numberOfRefillPoints
                      ├─ locationReference (lat/lon)
                      └─ refillPoint[]
                           └─ aegiElectricChargingPoint
                                ├─ idG (EVSE ID, e.g. DE*TNK*E00163*01)
                                ├─ maxPower, connectorType
                                └─ powerType (AC/DC)
```

### Dynamic (AFIR-Recharging-Dynamic-01-00-00_Delta)
```
messageContainer
  └─ payload[]
       └─ aegiEnergyInfrastructureStatusPublication
            ├─ publicationTime, tableReference (→ static)
            └─ energyInfrastructureSiteStatus[]
                 ├─ reference (→ site UUID)
                 └─ energyInfrastructureStationStatus[]
                      ├─ reference (→ station UUID)
                      ├─ lastUpdated
                      └─ refillPointStatus[]
                           └─ aegiElectricChargingPointStatus
                                ├─ reference.idG (→ EVSE ID)
                                └─ status.value: "available"|"charging"|"outOfService"|...
  └─ exchangeInformation
       ├─ codedExchangeProtocol: "deltaPush"
       └─ messageGenerationTimestamp
```

## Verified Data (chargecloud provider, noauth)

- **Static**: 1,965 sites, 3,703 stations, ~23 MB JSON
- **Dynamic**: Delta-based — snapshot contained 8 site statuses, 13 charging point statuses
- **EVSE ID examples**: DE*TNK*E00163*01, DE*ARR*EHD003*001, DE*MVV*E13765*L1, DE*NOM*E20007*001

## Key Identity Model

- **Site**: UUID (e.g. `b5857686-3012-4d89-967b-8cc52fa547eb`)
- **Station**: UUID (e.g. `74bb7fdf-212e-4a75-830a-26495be4589b`)
- **Charging Point (EVSE)**: eMI3 EVSE ID (e.g. `DE*TNK*E00163*01`)
- **Kafka key**: `{provider}/{evse_id}` for point-level status; `{provider}/{site_id}` for site-level reference

## Bridge Design Notes

### Transport Pattern
**Multi-provider poller** — poll multiple offer IDs on separate intervals.

### Data Flow
1. **Startup**: Fetch static data for all subscribed providers → emit reference-data events
2. **Polling loop**: Fetch dynamic data for all providers every 30-60s → emit status-change events
3. **Periodic refresh**: Re-fetch static data every 24h

### Per-Provider Model
Each brokered AFIR offer has its own offer ID. The bridge would maintain a list of provider offer IDs (static + dynamic pairs) and poll each independently. Chargecloud alone has 1,965 sites; combining all providers would give thousands of stations across Germany.

### Delta vs Snapshot
The dynamic endpoint returns delta updates (most recent changes only). The bridge must:
- Maintain local state (last-known status per EVSE)
- On each poll, merge delta into state
- Emit CloudEvents only for actual status changes

### Authentication Options
1. **Noauth** (works for some providers): Simple HTTP GET, no auth needed
2. **Keycloak OIDC** (works for all): Obtain JWT from `https://mobilithek.info/auth/realms/MDP`, pass as Bearer token

### Comparison with MobiData BW
| Aspect | MobiData BW | Mobilithek AFIR |
|--------|-----------|-----------------|
| Coverage | Baden-Württemberg only | All 16 German states |
| Protocol | DATEX II v3.5 + OCPI 3.0 | DATEX II v3 AFIR profiles |
| Auth | None required | Mixed (noauth for some, OIDC for others) |
| Format | Full snapshot | Delta-based |
| Providers | 10 regional | 20+ nationwide CPOs |
| Freshness | Full realtime snapshot | Delta only |

**Recommendation**: Mobilithek AFIR is the superior source for Germany-wide coverage. MobiData BW remains useful as a simpler BW-specific alternative with full snapshots. They could be implemented as separate sources or Mobilithek could supersede MobiData BW.
