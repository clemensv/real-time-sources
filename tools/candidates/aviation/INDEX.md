# Aviation — Candidate Sources

| Slug | Source | Region | Protocol | Auth | Score |
|------|--------|--------|----------|------|-------|
| [opensky-network](opensky-network.md) | OpenSky Network | Global | REST/JSON | None/Account | 17/18 |
| [adsb-exchange](adsb-exchange.md) | ADS-B Exchange | Global | REST/JSON | API Key (paid) | 15/18 |
| [faa-swim](faa-swim.md) | FAA SWIM | US | JMS/SOLACE | Cert + registration | 15/18 |
| [eurocontrol-b2b](eurocontrol-b2b.md) | EUROCONTROL B2B | Europe | SOAP/REST | Cert + registration | 15/18 |

## Already Covered
- **mode-s/**: Mode-S local receiver bridge (in main repo)

## Summary
Four candidates spanning the accessibility spectrum. OpenSky Network is the clear winner for open integration — free, well-documented REST API, global coverage. ADS-B Exchange offers unfiltered data (including military) but requires paid API access. FAA SWIM and EUROCONTROL B2B are the authoritative sources for US and European ATM data respectively, but both require organizational registration and complex authentication. For an open-source project, OpenSky is the natural choice, with ADS-B Exchange as a premium option.
