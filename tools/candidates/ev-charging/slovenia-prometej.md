# Slovenia Prometej / NAP EV Charging

**Country/Region**: Slovenia
**Publisher**: Ministrstvo za okolje, podnebje in energijo Republike Slovenije (MOPE)
**NAP Catalog**:
- https://nap.si/en/datasets_details?id=46963663-38dd-eb04-43a9-cca9bdc0e4ba
- https://nap.si/en/datasets_details?id=acc8a643-9dac-ecad-58da-0ce20f88f4bd
- https://nap.si/en/datasets_details?id=b0b212f3-6694-ad01-719c-918e51b8fba0
**Access URLs**:
- https://b2b.nap.si/data/b2b.prometej.energyInfrastructureTablePublication
- https://b2b.nap.si/data/b2b.prometej.energyInfrastructureStatusPublication
- https://b2b.ncup.si/data/b2b.tpeg.emi
**Documentation**:
- https://www.nap.si/_resources/profiles/DatexII3.6_NAP_prometej_profile.zip
- https://nap.si/resources/doc/nap_B2B_en.pdf
**Protocol**: HTTP/HTTPS pull
**Auth**: Public metadata and sample pages; live B2B access URLs returned `401` unauthenticated during probe
**Data Format**: XML (DATEX II v3.6 / TPEG EMI)
**Update Frequency**: Up to 1 min
**License**: Free of charge; CC BY-SA 4.0

## What It Provides

Slovenia's official NAP (`nap.si`) exposes a family of Prometej IDACS datasets for
charging and refuelling stations. The published metadata confirms three relevant
feeds:

1. **Prometej IDACS Energy Infrastructure Table (DATEX II v3.6)**
   - Locations, operational hours, and charging station details
2. **Prometej IDACS Energy Infrastructure Status**
   - Status publication in DATEX II v3.6
3. **Prometej IDACS Energy Infrastructure TPEG EMI**
   - Status and locations in TPEG EMI

This is the first clearly documented official EU NAP deployment of DATEX II v3.6 EV
charging data found in this survey.

## API Details

The dataset detail pages publish:
- Access URLs for the live B2B pull feeds
- Public sample links
- A DATEX II v3.6 profile zip for the Prometej datasets
- Quality metadata claiming `Up to 1 min` update frequency and `24/7` availability

Important caveat: the live B2B access URLs returned `401` during probe, so the
catalog metadata is public but the production pull feeds are not anonymously open.
This may still be workable if access is granted under light-touch registration, but it
is not plug-and-play open data in the same way as NDL Netherlands.

## Freshness Assessment

Technically, this is a very strong source:
- Official NAP publication
- DATEX II v3.6 and TPEG EMI formats
- Up-to-1-minute update claim
- Charging-location and status split that maps well to reference-vs-telemetry event design

Operationally, the access barrier is the issue. Public samples exist, but the live
pull endpoints appear to require credentials.

## Entity Model

- **Energy Infrastructure Site**: site-level location and operating-hours data
- **Charging Infrastructure Status**: dynamic status publication for the infrastructure
- **Transport Message Feed**: TPEG EMI representation of status and locations

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Official metadata says updates are available up to every minute |
| Openness | 1 | Metadata and samples are public, but live access URLs returned `401` |
| Stability | 3 | Official national access point and ministry-backed publication |
| Structure | 3 | DATEX II v3.6 / TPEG EMI with published profile documentation |
| Identifiers | 2 | IDACS framing strongly suggests stable infrastructure identifiers, but exact identifier practice still needs sample validation |
| Additive Value | 3 | First confirmed official DATEX II v3.6 EV charging NAP found in this survey |
| **Total** | **15/18** | |

## Notes

- This source matters even if access remains gated, because it proves DATEX II EV
  charging is no longer hypothetical in Europe.
- If the NAP's access process is lightweight and compatible with open-data reuse,
  this becomes a high-priority European bridge candidate.
- If the B2B URLs remain credential-gated under restrictive terms, the source is more
  useful as a standards and field-model reference than as an immediate open-data bridge.