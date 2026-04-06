# EV Charging Candidates

EV charging station registries and real-time availability data sources. The EV charging landscape is fragmented — no single standard dominates like GBFS does for bikeshare. OCPI (Open Charge Point Interface) is emerging as the industry interchange format.

## Candidates

| Candidate | Region | Score | Protocol | Key Value |
|-----------|--------|-------|----------|-----------|
| [Open Charge Map](open-charge-map.md) | **Global** | 17/18 | REST | 300K+ locations in 180 countries; global aggregator |
| [NOBIL Norway](nobil-norway.md) | Nordics | **18/18** | REST | Government registry with real-time connector status; CC BY 4.0 |
| [NDL Netherlands](ndl-netherlands.md) | Netherlands | **18/18** | OCPI files | Complete Dutch charging data with real-time EVSE status; industry-standard OCPI format |
| [Bundesnetzagentur](bundesnetzagentur-ladesaeulen.md) | Germany | 13/18 | CSV download | Official German register; monthly updates; no real-time |
| [ChargePlace Scotland](chargeplace-scotland.md) | UK — Scotland | 12/18 | REST | Government network operator; limited scope and access |

## Recommended Approach

1. **Build an NDL/OCPI bridge first** — the Netherlands dataset is the gold standard: real-time EVSE status, OCPI format, no auth, continuously updated. Building an OCPI parser means the same code works with any OCPI-compliant source.

2. **Build a NOBIL bridge** — authoritative Nordic data with real-time connector status. Covers Norway, Sweden, Finland. The delta-dump API (`fromdate` parameter) makes efficient change tracking straightforward.

3. **Build an Open Charge Map bridge** — global coverage as a complement. The `modifiedsince` parameter enables efficient delta polling. API key required but free.

4. **Bundesnetzagentur** is lower priority — monthly CSV downloads, no real-time data, no station IDs. Useful as reference data but not ideal for a real-time bridge.

5. **ChargePlace Scotland** is lowest priority — limited scope, uncertain API access.

## Coverage Summary

- **Authoritative government sources**: NOBIL (Nordics), Bundesnetzagentur (Germany), NDL (Netherlands)
- **Global aggregator**: Open Charge Map (180+ countries)
- **Key standard**: OCPI — building OCPI support enables future integration with roaming platforms (Hubject, Gireve)
