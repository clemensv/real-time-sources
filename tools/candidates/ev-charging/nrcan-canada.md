# NRCan Electric Charging Station Locator

**Country/Region**: Canada
**Publisher**: Natural Resources Canada (NRCan)
**API Endpoint**: Powered by AFDC/NREL (shared database with US AFDC)
**Documentation**: https://natural-resources.canada.ca/energy-efficiency/transportation-alternative-fuels/electric-charging-alternative-fuelling-stationslocator-map/20487
**Protocol**: REST (AFDC API with `country=CA` filter)
**Auth**: API Key (same NREL developer key as AFDC)
**Data Format**: JSON / CSV / GeoJSON (via AFDC API)
**Real-Time Status**: Partial — station-level status only (Available/Planned/Temporarily Unavailable)
**Update Frequency**: Daily (synchronized with AFDC)
**Station Count**: 16,706 EV stations / 46,792 EV ports in Canada
**License**: Public domain (government data)

## What It Provides

Natural Resources Canada (NRCan) maintains Canada's official Electric Vehicle and Alternative Fuel Charging Station Locator. The web map at nrcan.gc.ca provides a visual interface, but the underlying data is shared with (and accessible through) the US DOE's AFDC database. This means the AFDC API with `country=CA` provides programmatic access to the complete Canadian charging station dataset.

Canada's 16,706 EV stations host 46,792 individual charging ports across all provinces and territories. Major networks include FLO, Electrify Canada, Petro-Canada (owned by Suncor), ChargePoint, Tesla, Circuit électrique, BC Hydro, and Sun Country Highway.

## API Details

Canadian data is accessed via the AFDC API with country filter:
```
GET https://developer.nrel.gov/api/alt-fuel-stations/v1.json?api_key={key}&fuel_type=ELEC&country=CA&limit=200
```

All AFDC API features apply — see the [AFDC NREL](afdc-nrel.md) doc for full API details.

Canadian-specific notes:
- Province/territory codes use standard two-letter codes (ON, QC, BC, AB, etc.)
- Bilingual data: French translations for key fields (`access_days_time_fr`, `ev_pricing_fr`, `groups_with_access_code_fr`)
- Federal agency ownership tracking includes Canadian departments (NRCan, Transport Canada, National Defence, etc.)
- Canadian charging networks are included in the AFDC network list (FLO, Circuit électrique, Electrify Canada, Petro-Canada, etc.)
- NEVI-equivalent: Canada's ZEVIP (Zero Emission Vehicle Infrastructure Program) and EVAFIDI funding programs are tracked

## Freshness Assessment

Identical to AFDC — daily updates, station-level status. NRCan's web locator may have its own refresh cycle, but the underlying data in the AFDC database is updated daily from network API imports and CSV feeds.

## Entity Model

Same as AFDC. Canadian stations follow the same data model with bilingual support.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Daily updates; station-level status only |
| Openness | 3 | Public domain; free API key; shared with AFDC |
| Stability | 3 | Government-operated; 10+ years of service |
| Structure | 3 | Rich JSON with bilingual support (EN/FR) |
| Identifiers | 3 | Numeric IDs; network-specific cross-references |
| Additive Value | 1 | Fully contained within AFDC — no independent access needed |
| **Total** | **15/18** | |

## Notes

- NRCan's data is fully accessible via the AFDC API — there is no need for a separate NRCan-specific bridge. Use `country=CA` on the AFDC API.
- This entry exists to document that Canadian data is covered and to note the bilingual (EN/FR) data support.
- Canada's charging network is growing rapidly, driven by federal EV mandates and ZEVIP infrastructure funding.
- Major networks: FLO (Quebec-based, largest Canadian network), Electrify Canada (Volkswagen), Petro-Canada (Suncor), ChargePoint, Tesla.
- The bilingual requirement (Official Languages Act) means French translations are provided for user-facing fields — useful for Quebec-focused applications.
