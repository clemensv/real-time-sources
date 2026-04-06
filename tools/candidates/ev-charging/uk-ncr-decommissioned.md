# UK National Chargepoint Registry (NCR) — DECOMMISSIONED

**Country/Region**: United Kingdom
**Publisher**: Office for Zero Emission Vehicles (OZEV) / Department for Transport (DfT)
**API Endpoint**: Was at `https://chargepoints.dft.gov.uk/api/retrieve/registry/...` (no longer available)
**Documentation**: https://www.gov.uk/guidance/find-and-use-data-on-public-electric-vehicle-chargepoints
**Protocol**: Was REST + file download
**Auth**: None (was freely accessible)
**Data Format**: Was CSV / JSON / XML
**Real-Time Status**: Had connector status data
**Update Frequency**: N/A — decommissioned
**Station Count**: Was ~50,000+ connectors
**License**: Open Government Licence

## What It Provides

The NCR **was** the UK's official database of publicly accessible EV chargepoints, established in 2011. It provided station locations, connector types, power levels, and status information in multiple formats. The dataset was freely available with no registration required.

**The NCR was decommissioned on 28 November 2024.**

## API Details

The NCR formerly provided:
- Full dataset downloads in CSV, JSON, XML formats
- A Retrieve API with endpoints for:
  - `registry` — Charge Point Registry (all chargepoints)
  - `type` — Connector Types
  - `bearing` — Bearings
  - `method` — Charging Methods
  - `mode` — Charge Modes
  - `status` — Connector Statuses

All endpoints are now defunct.

## Freshness Assessment

No longer relevant — the service is decommissioned. The gov.uk guidance page confirms: "The National Chargepoint Registry was decommissioned 28 November 2024."

## Entity Model

Historical reference only.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 0 | Decommissioned |
| Openness | 0 | No longer available |
| Stability | 0 | Decommissioned |
| Structure | 0 | N/A |
| Identifiers | 0 | N/A |
| Additive Value | 0 | N/A |
| **Total** | **0/18** | |

## Notes

- The NCR was decommissioned in November 2024. This is a significant gap in UK open charging data.
- The UK government has not announced a direct replacement as of early 2026. 
- For UK charging data, alternatives include:
  - **Open Charge Map** — has good UK coverage via community contributions
  - **ChargePlace Scotland** — covers Scotland (already documented)
  - **National Charge Point Registry data on data.gov.uk** — historical snapshots may still be available
  - **Individual network APIs** — bp pulse, Pod Point, Osprey, etc.
- The decommissioning is surprising given EU AFIR-equivalent regulations. The UK, post-Brexit, may be pursuing a different approach to charging data publication.
- This entry is kept for reference to document the gap and explain why the UK lacks a national open charging data source as of 2026.
