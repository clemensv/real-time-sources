# Energi Data Service (Energinet) Denmark Bridge Events

A real-time data bridge that polls the [Energi Data Service](https://www.energidataservice.dk/) API operated by Energinet (the Danish TSO) and streams Danish power system data to Apache Kafka, Azure Event Hubs, or Fabric Event Streams as CloudEvents.

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
| Schemagroups | 2 |

## Endpoints

### Endpoint `dk.energinet.energidataservice.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`dk.energinet.energidataservice`](#messagegroup-dkenerginetenergidataservice) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `energidataservice-dk` |
| Kafka key | `{price_area}` |
| Deployed | False |

## Messagegroups

### Messagegroup `dk.energinet.energidataservice`
<a id="messagegroup-dkenerginetenergidataservice"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `dk.energinet.energidataservice.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `dk.energinet.energidataservice.PowerSystemSnapshot`
<a id="message-dkenerginetenergidataservicepowersystemsnapshot"></a>

Minute-by-minute snapshot of the Danish power system from Energi Data Service (Energinet), including CO2 emission intensity, renewable generation (solar, onshore wind, offshore wind), conventional production bands, total cross-border exchange flows, per-interconnector exchange (DK1–DE, DK1–NL, DK1–GB, DK1–NO, DK1–SE, DK1–DK2, DK2–DE, DK2–SE, Bornholm–SE), automatic and manual frequency restoration reserve activation (aFRR, mFRR) per price area, and grid imbalance per price area.

| Field | Value |
| --- | --- |
| Name | PowerSystemSnapshot |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/dk.energinet.energidataservice.jstruct/schemas/dk.energinet.energidataservice.PowerSystemSnapshot`](#schema-dkenerginetenergidataservicepowersystemsnapshot) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `dk.energinet.energidataservice.PowerSystemSnapshot` |
| `source` |  | `string` | `False` | `https://api.energidataservice.dk` |
| `subject` |  | `uritemplate` | `False` | `{price_area}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `dk.energinet.energidataservice.Kafka` | `KAFKA` | topic `energidataservice-dk`; key `{price_area}` |

#### Message `dk.energinet.energidataservice.SpotPrice`
<a id="message-dkenerginetenergidataservicespotprice"></a>

Day-ahead electricity spot price per bidding zone from Energi Data Service (Energinet / Nord Pool). One record per hour per price area (DK1 – Western Denmark, DK2 – Eastern Denmark). Prices are published in both DKK and EUR.

| Field | Value |
| --- | --- |
| Name | SpotPrice |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/dk.energinet.energidataservice.jstruct/schemas/dk.energinet.energidataservice.SpotPrice`](#schema-dkenerginetenergidataservicespotprice) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `dk.energinet.energidataservice.SpotPrice` |
| `source` |  | `string` | `False` | `https://api.energidataservice.dk` |
| `subject` |  | `uritemplate` | `False` | `{price_area}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `dk.energinet.energidataservice.Kafka` | `KAFKA` | topic `energidataservice-dk`; key `{price_area}` |

## Schemagroups

### Schemagroup `dk.energinet.energidataservice.jstruct`
<a id="schemagroup-dkenerginetenergidataservicejstruct"></a>

#### Schema `dk.energinet.energidataservice.PowerSystemSnapshot`
<a id="schema-dkenerginetenergidataservicepowersystemsnapshot"></a>

| Field | Value |
| --- | --- |
| Name | PowerSystemSnapshot |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/dk/energinet/energidataservice/PowerSystemSnapshot` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/dk/energinet/energidataservice/PowerSystemSnapshot` |
| Type | `object` |

###### Object `PowerSystemSnapshot`
<a id="schema-node-powersystemsnapshot"></a>

Minute-by-minute snapshot of the Danish power system from Energi Data Service (Energinet). Published by the PowerSystemRightNow dataset at approximately 1-minute intervals.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `minutes1_utc` | `string` | `True` | UTC timestamp of the snapshot rounded to the nearest minute, in ISO 8601 format. Sourced from the PowerSystemRightNow 'Minutes1UTC' field. | - | - | - |
| `minutes1_dk` | `string` | `True` | Danish local-time timestamp of the snapshot rounded to the nearest minute, in ISO 8601 format. Sourced from the PowerSystemRightNow 'Minutes1DK' field. | - | - | - |
| `price_area` | `string` | `True` | Price area code. Set to 'DK' for system-wide power system snapshots that cover the entire Danish grid (both DK1 and DK2). | - | - | - |
| `co2_emission` | `union` | `False` | CO2 emission intensity of electricity consumed in Denmark at the time of the snapshot, measured in grams of CO2 per kWh (g/kWh). Sourced from 'CO2Emission'. | unit=`g/kWh` | - | - |
| `production_ge_100mw` | `union` | `False` | Total electricity production from centralized power plants with capacity >= 100 MW, in megawatts (MW). Sourced from 'ProductionGe100MW'. | unit=`MW` | - | - |
| `production_lt_100mw` | `union` | `False` | Total electricity production from decentralized power plants with capacity < 100 MW, in megawatts (MW). Sourced from 'ProductionLt100MW'. | unit=`MW` | - | - |
| `solar_power` | `union` | `False` | Estimated total solar photovoltaic power production in Denmark, in megawatts (MW). Sourced from 'SolarPower'. | unit=`MW` | - | - |
| `offshore_wind_power` | `union` | `False` | Total offshore wind power production in Denmark, in megawatts (MW). Sourced from 'OffshoreWindPower'. | unit=`MW` | - | - |
| `onshore_wind_power` | `union` | `False` | Total onshore wind power production in Denmark, in megawatts (MW). Sourced from 'OnshoreWindPower'. | unit=`MW` | - | - |
| `exchange_sum` | `union` | `False` | Net total cross-border electricity exchange for all Danish interconnectors, in megawatts (MW). Positive values indicate net import; negative values indicate net export. Sourced from 'Exchange_Sum'. | unit=`MW` | - | - |
| `exchange_dk1_de` | `union` | `False` | Electricity exchange flow on the DK1–Germany interconnector, in megawatts (MW). Positive = import to DK1, negative = export from DK1. Sourced from 'Exchange_DK1_DE'. | unit=`MW` | - | - |
| `exchange_dk1_nl` | `union` | `False` | Electricity exchange flow on the DK1–Netherlands (COBRAcable) interconnector, in megawatts (MW). Positive = import to DK1, negative = export from DK1. Sourced from 'Exchange_DK1_NL'. | unit=`MW` | - | - |
| `exchange_dk1_gb` | `union` | `False` | Electricity exchange flow on the DK1–Great Britain (Viking Link) interconnector, in megawatts (MW). Positive = import to DK1, negative = export from DK1. Sourced from 'Exchange_DK1_GB'. | unit=`MW` | - | - |
| `exchange_dk1_no` | `union` | `False` | Electricity exchange flow on the DK1–Norway (Skagerrak) interconnector, in megawatts (MW). Positive = import to DK1, negative = export from DK1. Sourced from 'Exchange_DK1_NO'. | unit=`MW` | - | - |
| `exchange_dk1_se` | `union` | `False` | Electricity exchange flow on the DK1–Sweden interconnector, in megawatts (MW). Positive = import to DK1, negative = export from DK1. Sourced from 'Exchange_DK1_SE'. | unit=`MW` | - | - |
| `exchange_dk1_dk2` | `union` | `False` | Electricity exchange flow on the DK1–DK2 (Great Belt) interconnector, in megawatts (MW). Positive = flow from DK1 to DK2, negative = flow from DK2 to DK1. Sourced from 'Exchange_DK1_DK2'. | unit=`MW` | - | - |
| `exchange_dk2_de` | `union` | `False` | Electricity exchange flow on the DK2–Germany (Kontek) interconnector, in megawatts (MW). Positive = import to DK2, negative = export from DK2. Sourced from 'Exchange_DK2_DE'. | unit=`MW` | - | - |
| `exchange_dk2_se` | `union` | `False` | Electricity exchange flow on the DK2–Sweden (Øresund) interconnector, in megawatts (MW). Positive = import to DK2, negative = export from DK2. Sourced from 'Exchange_DK2_SE'. | unit=`MW` | - | - |
| `exchange_bornholm_se` | `union` | `False` | Electricity exchange flow on the Bornholm–Sweden interconnector, in megawatts (MW). Positive = import to Bornholm, negative = export from Bornholm. Sourced from 'Exchange_Bornholm_SE'. | unit=`MW` | - | - |
| `afrr_activated_dk1` | `union` | `False` | Automatic Frequency Restoration Reserve (aFRR) activated in price area DK1, in megawatts (MW). Positive = upward regulation, negative = downward regulation. Sourced from 'aFRR_ActivatedDK1'. | unit=`MW` | - | - |
| `afrr_activated_dk2` | `union` | `False` | Automatic Frequency Restoration Reserve (aFRR) activated in price area DK2, in megawatts (MW). Positive = upward regulation, negative = downward regulation. Sourced from 'aFRR_ActivatedDK2'. | unit=`MW` | - | - |
| `mfrr_activated_dk1` | `union` | `False` | Manual Frequency Restoration Reserve (mFRR) activated in price area DK1, in megawatts (MW). Positive = upward regulation, negative = downward regulation. Sourced from 'mFRR_ActivatedDK1'. | unit=`MW` | - | - |
| `mfrr_activated_dk2` | `union` | `False` | Manual Frequency Restoration Reserve (mFRR) activated in price area DK2, in megawatts (MW). Positive = upward regulation, negative = downward regulation. Sourced from 'mFRR_ActivatedDK2'. | unit=`MW` | - | - |
| `imbalance_dk1` | `union` | `False` | Net power imbalance in price area DK1, in megawatts (MW). Represents the difference between scheduled and actual generation/consumption. Sourced from 'ImbalanceDK1'. | unit=`MW` | - | - |
| `imbalance_dk2` | `union` | `False` | Net power imbalance in price area DK2, in megawatts (MW). Represents the difference between scheduled and actual generation/consumption. Sourced from 'ImbalanceDK2'. | unit=`MW` | - | - |

#### Schema `dk.energinet.energidataservice.SpotPrice`
<a id="schema-dkenerginetenergidataservicespotprice"></a>

| Field | Value |
| --- | --- |
| Name | SpotPrice |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/dk/energinet/energidataservice/SpotPrice` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/dk/energinet/energidataservice/SpotPrice` |
| Type | `object` |

###### Object `SpotPrice`
<a id="schema-node-spotprice"></a>

Day-ahead electricity spot price per bidding zone from Energi Data Service (Energinet / Nord Pool). One record per hour per price area.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `hour_utc` | `string` | `True` | UTC hour for which the spot price applies, in ISO 8601 format. Each price applies to the full 60-minute interval starting at this timestamp. Sourced from 'HourUTC'. | - | - | - |
| `hour_dk` | `string` | `True` | Danish local-time hour for which the spot price applies, in ISO 8601 format. Sourced from 'HourDK'. | - | - | - |
| `price_area` | `string` | `True` | Nord Pool bidding zone code. 'DK1' is Western Denmark (Jutland and Funen); 'DK2' is Eastern Denmark (Zealand, Lolland-Falster, and Bornholm). Sourced from 'PriceArea'. | - | - | - |
| `spot_price_dkk` | `union` | `False` | Day-ahead spot price in Danish Kroner per megawatt-hour (DKK/MWh). Sourced from 'SpotPriceDKK'. | unit=`DKK/MWh` | - | - |
| `spot_price_eur` | `union` | `False` | Day-ahead spot price in Euros per megawatt-hour (EUR/MWh). Sourced from 'SpotPriceEUR'. | unit=`EUR/MWh` | - | - |

### Schemagroup `dk.energinet.energidataservice.avro`
<a id="schemagroup-dkenerginetenergidataserviceavro"></a>

#### Schema `dk.energinet.energidataservice.PowerSystemSnapshot`
<a id="schema-dkenerginetenergidataservicepowersystemsnapshot"></a>

| Field | Value |
| --- | --- |
| Name | PowerSystemSnapshot |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | Minute-by-minute snapshot of the Danish power system from Energi Data Service (Energinet). |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | PowerSystemSnapshot |
| Namespace | dk.energinet.energidataservice |
| Type | `record` |
| Doc | Minute-by-minute snapshot of the Danish power system from Energi Data Service (Energinet). Published by the PowerSystemRightNow dataset at approximately 1-minute intervals. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `minutes1_utc` | `string` | UTC timestamp of the snapshot rounded to the nearest minute, in ISO 8601 format. | `-` |
| `minutes1_dk` | `string` | Danish local-time timestamp of the snapshot rounded to the nearest minute, in ISO 8601 format. | `-` |
| `price_area` | `string` | Price area code. Set to 'DK' for system-wide power system snapshots. | `-` |
| `co2_emission` | `double` \| `null` | CO2 emission intensity in g/kWh. | `-` |
| `production_ge_100mw` | `double` \| `null` | Production from plants >= 100 MW in MW. | `-` |
| `production_lt_100mw` | `double` \| `null` | Production from plants < 100 MW in MW. | `-` |
| `solar_power` | `double` \| `null` | Solar PV production in MW. | `-` |
| `offshore_wind_power` | `double` \| `null` | Offshore wind production in MW. | `-` |
| `onshore_wind_power` | `double` \| `null` | Onshore wind production in MW. | `-` |
| `exchange_sum` | `double` \| `null` | Net total cross-border exchange in MW. | `-` |
| `exchange_dk1_de` | `double` \| `null` | DK1-Germany exchange in MW. | `-` |
| `exchange_dk1_nl` | `double` \| `null` | DK1-Netherlands exchange in MW. | `-` |
| `exchange_dk1_gb` | `double` \| `null` | DK1-Great Britain exchange in MW. | `-` |
| `exchange_dk1_no` | `double` \| `null` | DK1-Norway exchange in MW. | `-` |
| `exchange_dk1_se` | `double` \| `null` | DK1-Sweden exchange in MW. | `-` |
| `exchange_dk1_dk2` | `double` \| `null` | DK1-DK2 (Great Belt) exchange in MW. | `-` |
| `exchange_dk2_de` | `double` \| `null` | DK2-Germany exchange in MW. | `-` |
| `exchange_dk2_se` | `double` \| `null` | DK2-Sweden exchange in MW. | `-` |
| `exchange_bornholm_se` | `double` \| `null` | Bornholm-Sweden exchange in MW. | `-` |
| `afrr_activated_dk1` | `double` \| `null` | aFRR activated in DK1 in MW. | `-` |
| `afrr_activated_dk2` | `double` \| `null` | aFRR activated in DK2 in MW. | `-` |
| `mfrr_activated_dk1` | `double` \| `null` | mFRR activated in DK1 in MW. | `-` |
| `mfrr_activated_dk2` | `double` \| `null` | mFRR activated in DK2 in MW. | `-` |
| `imbalance_dk1` | `double` \| `null` | Grid imbalance in DK1 in MW. | `-` |
| `imbalance_dk2` | `double` \| `null` | Grid imbalance in DK2 in MW. | `-` |

#### Schema `dk.energinet.energidataservice.SpotPrice`
<a id="schema-dkenerginetenergidataservicespotprice"></a>

| Field | Value |
| --- | --- |
| Name | SpotPrice |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | Day-ahead electricity spot price per bidding zone from Energi Data Service (Energinet / Nord Pool). |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | SpotPrice |
| Namespace | dk.energinet.energidataservice |
| Type | `record` |
| Doc | Day-ahead electricity spot price per bidding zone from Energi Data Service (Energinet / Nord Pool). One record per hour per price area. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `hour_utc` | `string` | UTC hour for which the spot price applies, in ISO 8601 format. | `-` |
| `hour_dk` | `string` | Danish local-time hour, in ISO 8601 format. | `-` |
| `price_area` | `string` | Nord Pool bidding zone code (DK1 or DK2). | `-` |
| `spot_price_dkk` | `double` \| `null` | Day-ahead spot price in DKK/MWh. | `-` |
| `spot_price_eur` | `double` \| `null` | Day-ahead spot price in EUR/MWh. | `-` |
