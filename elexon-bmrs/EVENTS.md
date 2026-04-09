# Elexon BMRS (GB Electricity Market) Bridge Events

This document describes the events emitted by the Elexon BMRS Bridge.

- [UK.Co.Elexon.BMRS](#message-group-ukcoelexonbmrs)
  - [UK.Co.Elexon.BMRS.GenerationMix](#message-ukcoelexonbmrsgenerationmix)
  - [UK.Co.Elexon.BMRS.DemandOutturn](#message-ukcoelexonbmrsdemandoutturn)

---

## Message Group: UK.Co.Elexon.BMRS

---

### Message: UK.Co.Elexon.BMRS.GenerationMix

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `UK.Co.Elexon.BMRS.GenerationMix` |
| `source` | CloudEvent source | `string` | `True` | `https://data.elexon.co.uk/bmrs` |
| `subject` | Settlement period | `uritemplate` | `True` | `{settlement_period}` |

#### Schema: GenerationMix

| **Field Name** | **Type** | **Unit** | **Description** |
|----------------|----------|----------|-----------------|
| `settlement_period` | *int32* | — | GB electricity settlement period number (1-50) |
| `start_time` | *datetime* | — | UTC start time of the settlement period |
| `biomass_mw` | *double (nullable)* | MW | Biomass generation output |
| `ccgt_mw` | *double (nullable)* | MW | Combined cycle gas turbine output |
| `coal_mw` | *double (nullable)* | MW | Coal-fired generation output |
| `nuclear_mw` | *double (nullable)* | MW | Nuclear generation output |
| `wind_mw` | *double (nullable)* | MW | Wind generation output |
| `ocgt_mw` | *double (nullable)* | MW | Open cycle gas turbine output |
| `oil_mw` | *double (nullable)* | MW | Oil-fired generation output |
| `npshyd_mw` | *double (nullable)* | MW | Non-pumped-storage hydro output |
| `ps_mw` | *double (nullable)* | MW | Pumped storage output |
| `intfr_mw` | *double (nullable)* | MW | France interconnector (IFA) import |
| `intned_mw` | *double (nullable)* | MW | Netherlands interconnector (BritNed) import |
| `intnem_mw` | *double (nullable)* | MW | Belgium interconnector (Nemo Link) import |
| `intelec_mw` | *double (nullable)* | MW | Ireland interconnector (EWIC) import |
| `intifa2_mw` | *double (nullable)* | MW | France interconnector (IFA2) import |
| `intnsl_mw` | *double (nullable)* | MW | Norway interconnector (NSL) import |
| `intvkl_mw` | *double (nullable)* | MW | Denmark interconnector (Viking Link) import |
| `other_mw` | *double (nullable)* | MW | Other fuel types |

---

### Message: UK.Co.Elexon.BMRS.DemandOutturn

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `UK.Co.Elexon.BMRS.DemandOutturn` |
| `source` | CloudEvent source | `string` | `True` | `https://data.elexon.co.uk/bmrs` |
| `subject` | Settlement period | `uritemplate` | `True` | `{settlement_period}` |

#### Schema: DemandOutturn

| **Field Name** | **Type** | **Unit** | **Description** |
|----------------|----------|----------|-----------------|
| `settlement_period` | *int32* | — | GB electricity settlement period number (1-50) |
| `settlement_date` | *string* | — | Settlement date (YYYY-MM-DD) |
| `start_time` | *datetime* | — | UTC start time of the settlement period |
| `publish_time` | *datetime (nullable)* | — | Publication timestamp |
| `initial_demand_outturn_mw` | *double (nullable)* | MW | Initial national demand outturn (INDO) |
| `initial_transmission_system_demand_outturn_mw` | *double (nullable)* | MW | Initial transmission system demand outturn (ITSDO) |
