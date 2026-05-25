# Elexon BMRS (GB Electricity Market) Poller Events

**Elexon BMRS Poller** polls the Elexon Balancing Mechanism Reporting Service (BMRS) API for the latest GB electricity market data and sends it to a Kafka topic as CloudEvents. The tool tracks previously seen settlement periods to avoid sending duplicates.

## Table of Contents

- [Registry](#registry)
- [Endpoints](#endpoints)
- [Messagegroups](#messagegroups)
- [Schemagroups](#schemagroups)

---

## Registry

| Field | Value |
| --- | --- |
| Endpoints | 1 |
| Messagegroups | 1 |
| Schemagroups | 1 |

## Endpoints

### Endpoint `UK.Co.Elexon.BMRS.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`UK.Co.Elexon.BMRS`](#messagegroup-ukcoelexonbmrs) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `elexon-bmrs` |
| Kafka key | `{settlement_period}` |
| Deployed | False |

## Messagegroups

### Messagegroup `UK.Co.Elexon.BMRS`
<a id="messagegroup-ukcoelexonbmrs"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `UK.Co.Elexon.BMRS.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `UK.Co.Elexon.BMRS.GenerationMix`
<a id="message-ukcoelexonbmrsgenerationmix"></a>

| Field | Value |
| --- | --- |
| Name | GenerationMix |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/UK.Co.Elexon.BMRS.jstruct/schemas/UK.Co.Elexon.BMRS.GenerationMix`](#schema-ukcoelexonbmrsgenerationmix) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `UK.Co.Elexon.BMRS.GenerationMix` |
| `source` |  | `string` | `False` | `https://data.elexon.co.uk/bmrs` |
| `subject` |  | `uritemplate` | `False` | `{settlement_period}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `UK.Co.Elexon.BMRS.Kafka` | `KAFKA` | topic `elexon-bmrs`; key `{settlement_period}` |

#### Message `UK.Co.Elexon.BMRS.DemandOutturn`
<a id="message-ukcoelexonbmrsdemandoutturn"></a>

| Field | Value |
| --- | --- |
| Name | DemandOutturn |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/UK.Co.Elexon.BMRS.jstruct/schemas/UK.Co.Elexon.BMRS.DemandOutturn`](#schema-ukcoelexonbmrsdemandoutturn) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `UK.Co.Elexon.BMRS.DemandOutturn` |
| `source` |  | `string` | `False` | `https://data.elexon.co.uk/bmrs` |
| `subject` |  | `uritemplate` | `False` | `{settlement_period}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `UK.Co.Elexon.BMRS.Kafka` | `KAFKA` | topic `elexon-bmrs`; key `{settlement_period}` |

## Schemagroups

### Schemagroup `UK.Co.Elexon.BMRS.jstruct`
<a id="schemagroup-ukcoelexonbmrsjstruct"></a>

#### Schema `UK.Co.Elexon.BMRS.GenerationMix`
<a id="schema-ukcoelexonbmrsgenerationmix"></a>

| Field | Value |
| --- | --- |
| Name | GenerationMix |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://data.elexon.co.uk/schemas/UK/Co/Elexon/BMRS/GenerationMix` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `GenerationMix`
<a id="schema-node-generationmix"></a>

Half-hourly generation outturn summary for the GB electricity system from the Elexon BMRS API. Each record represents one settlement period and contains the generation output in megawatts (MW) broken down by fuel type, including domestic generation (biomass, CCGT, coal, nuclear, wind, OCGT, oil, hydro, pumped storage) and interconnector imports (France IFA, France IFA2, Netherlands BritNed, Belgium Nemo, Ireland EWIC, Norway NSL, Denmark Viking Link). Sourced from the BMRS /generation/outturn/summary endpoint.

| Field | Value |
| --- | --- |
| $id | `https://data.elexon.co.uk/schemas/UK/Co/Elexon/BMRS/GenerationMix` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `settlement_period` | `int32` | `True` | GB electricity settlement period number (1-50). Each settlement period is 30 minutes long, starting at midnight UTC. Period 1 covers 00:00-00:30, period 2 covers 00:30-01:00, and so on. | - | - | - |
| `start_time` | `datetime` | `True` | UTC start time of the settlement period as reported by the BMRS generation outturn summary endpoint. | - | - | - |
| `biomass_mw` | `union` | `False` | Generation output from biomass-fuelled power stations in megawatts (MW). Biomass includes dedicated biomass plants and biomass co-firing units. | unit=`MW` symbol=`MW` | - | - |
| `ccgt_mw` | `union` | `False` | Generation output from combined cycle gas turbine (CCGT) power stations in megawatts (MW). CCGT is the primary gas-fired generation technology in GB. | unit=`MW` symbol=`MW` | - | - |
| `coal_mw` | `union` | `False` | Generation output from coal-fired power stations in megawatts (MW). | unit=`MW` symbol=`MW` | - | - |
| `nuclear_mw` | `union` | `False` | Generation output from nuclear power stations in megawatts (MW). | unit=`MW` symbol=`MW` | - | - |
| `wind_mw` | `union` | `False` | Generation output from wind farms (onshore and offshore combined) in megawatts (MW). | unit=`MW` symbol=`MW` | - | - |
| `ocgt_mw` | `union` | `False` | Generation output from open cycle gas turbine (OCGT) power stations in megawatts (MW). OCGT units are typically used for peaking and reserve. | unit=`MW` symbol=`MW` | - | - |
| `oil_mw` | `union` | `False` | Generation output from oil-fired power stations in megawatts (MW). | unit=`MW` symbol=`MW` | - | - |
| `npshyd_mw` | `union` | `False` | Generation output from non-pumped-storage hydroelectric power stations in megawatts (MW). | unit=`MW` symbol=`MW` | - | - |
| `ps_mw` | `union` | `False` | Generation output from pumped storage hydroelectric power stations in megawatts (MW). PS units can act as both generation and demand. | unit=`MW` symbol=`MW` | - | - |
| `intfr_mw` | `union` | `False` | Net import via the France interconnector (IFA) in megawatts (MW). Positive values indicate import to GB. | unit=`MW` symbol=`MW` | - | - |
| `intned_mw` | `union` | `False` | Net import via the Netherlands interconnector (BritNed) in megawatts (MW). Positive values indicate import to GB. | unit=`MW` symbol=`MW` | - | - |
| `intnem_mw` | `union` | `False` | Net import via the Belgium interconnector (Nemo Link) in megawatts (MW). Positive values indicate import to GB. | unit=`MW` symbol=`MW` | - | - |
| `intelec_mw` | `union` | `False` | Net import via the East-West Interconnector (EWIC) to Ireland in megawatts (MW). Positive values indicate import to GB. | unit=`MW` symbol=`MW` | - | - |
| `intifa2_mw` | `union` | `False` | Net import via the IFA2 interconnector to France in megawatts (MW). Positive values indicate import to GB. | unit=`MW` symbol=`MW` | - | - |
| `intnsl_mw` | `union` | `False` | Net import via the North Sea Link interconnector to Norway in megawatts (MW). Positive values indicate import to GB. | unit=`MW` symbol=`MW` | - | - |
| `intvkl_mw` | `union` | `False` | Net import via the Viking Link interconnector to Denmark in megawatts (MW). Positive values indicate import to GB. | unit=`MW` symbol=`MW` | - | - |
| `other_mw` | `union` | `False` | Generation output from other fuel types not individually categorised in megawatts (MW). | unit=`MW` symbol=`MW` | - | - |

#### Schema `UK.Co.Elexon.BMRS.DemandOutturn`
<a id="schema-ukcoelexonbmrsdemandoutturn"></a>

| Field | Value |
| --- | --- |
| Name | DemandOutturn |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://data.elexon.co.uk/schemas/UK/Co/Elexon/BMRS/DemandOutturn` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `DemandOutturn`
<a id="schema-node-demandoutturn"></a>

Half-hourly demand outturn for the GB electricity transmission system from the Elexon BMRS API. Each record represents one settlement period and contains the initial national demand outturn (INDO) and initial transmission system demand outturn (ITSDO) in megawatts (MW). Sourced from the BMRS /demand/outturn endpoint. Published under CC-BY 4.0 licence by Elexon.

| Field | Value |
| --- | --- |
| $id | `https://data.elexon.co.uk/schemas/UK/Co/Elexon/BMRS/DemandOutturn` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `settlement_period` | `int32` | `True` | GB electricity settlement period number (1-50). Each settlement period is 30 minutes long, starting at midnight UTC. | - | - | - |
| `settlement_date` | `string` | `True` | Settlement date in ISO 8601 format (YYYY-MM-DD) as reported by the BMRS demand outturn endpoint. | - | - | - |
| `start_time` | `datetime` | `True` | UTC start time of the settlement period as reported by the BMRS demand outturn endpoint. | - | - | - |
| `publish_time` | `datetime` | `False` | UTC timestamp when the demand outturn data was published by Elexon. | - | - | - |
| `initial_demand_outturn_mw` | `union` | `False` | Initial national demand outturn (INDO) in megawatts (MW). This is the metered generation output less station transformer, unit transformer, and pumped storage demand, measured at the Grid Supply Point (GSP). | unit=`MW` symbol=`MW` | - | - |
| `initial_transmission_system_demand_outturn_mw` | `union` | `False` | Initial transmission system demand outturn (ITSDO) in megawatts (MW). This represents the national demand plus station demand, pumping, and interconnector exports. | unit=`MW` symbol=`MW` | - | - |
