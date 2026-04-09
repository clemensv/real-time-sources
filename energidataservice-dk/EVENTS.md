# Energi Data Service (Energinet) Denmark Bridge Events

This document describes the events emitted by the Energi Data Service Denmark Bridge.

- [dk.energinet.energidataservice](#message-group-dkenerginetenergi-dataservice)
  - [dk.energinet.energidataservice.PowerSystemSnapshot](#message-dkenerginetenergi-dataservicepowersystemsnapshot)
  - [dk.energinet.energidataservice.SpotPrice](#message-dkenerginetenergi-dataservicespotprice)

---

## Message Group: dk.energinet.energidataservice

---

### Message: dk.energinet.energidataservice.PowerSystemSnapshot

*Telemetry — polled every ~90 seconds from the PowerSystemRightNow dataset.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `dk.energinet.energidataservice.PowerSystemSnapshot` |
| `source` | CloudEvent source | `string` | `True` | `https://api.energidataservice.dk` |
| `subject` | Price area code | `string` | `True` | `{price_area}` |

#### Schema: PowerSystemSnapshot

| **Field Name** | **Type** | **Unit** | **Description** |
|----------------|----------|----------|-----------------|
| `minutes1_utc` | *string* | — | UTC timestamp of the snapshot (ISO 8601) |
| `minutes1_dk` | *string* | — | Danish local-time timestamp (ISO 8601) |
| `price_area` | *string* | — | Price area code (DK for system-wide) |
| `co2_emission` | *double / null* | g/kWh | CO2 emission intensity |
| `production_ge_100mw` | *double / null* | MW | Production from plants ≥ 100 MW |
| `production_lt_100mw` | *double / null* | MW | Production from plants < 100 MW |
| `solar_power` | *double / null* | MW | Solar PV production |
| `offshore_wind_power` | *double / null* | MW | Offshore wind production |
| `onshore_wind_power` | *double / null* | MW | Onshore wind production |
| `exchange_sum` | *double / null* | MW | Net total cross-border exchange |
| `exchange_dk1_de` | *double / null* | MW | DK1–Germany exchange |
| `exchange_dk1_nl` | *double / null* | MW | DK1–Netherlands exchange |
| `exchange_dk1_gb` | *double / null* | MW | DK1–Great Britain exchange |
| `exchange_dk1_no` | *double / null* | MW | DK1–Norway exchange |
| `exchange_dk1_se` | *double / null* | MW | DK1–Sweden exchange |
| `exchange_dk1_dk2` | *double / null* | MW | DK1–DK2 (Great Belt) exchange |
| `exchange_dk2_de` | *double / null* | MW | DK2–Germany exchange |
| `exchange_dk2_se` | *double / null* | MW | DK2–Sweden exchange |
| `exchange_bornholm_se` | *double / null* | MW | Bornholm–Sweden exchange |
| `afrr_activated_dk1` | *double / null* | MW | aFRR activated in DK1 |
| `afrr_activated_dk2` | *double / null* | MW | aFRR activated in DK2 |
| `mfrr_activated_dk1` | *double / null* | MW | mFRR activated in DK1 |
| `mfrr_activated_dk2` | *double / null* | MW | mFRR activated in DK2 |
| `imbalance_dk1` | *double / null* | MW | Grid imbalance in DK1 |
| `imbalance_dk2` | *double / null* | MW | Grid imbalance in DK2 |

---

### Message: dk.energinet.energidataservice.SpotPrice

*Telemetry — polled hourly from the ElspotPrices dataset.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `dk.energinet.energidataservice.SpotPrice` |
| `source` | CloudEvent source | `string` | `True` | `https://api.energidataservice.dk` |
| `subject` | Price area code | `string` | `True` | `{price_area}` |

#### Schema: SpotPrice

| **Field Name** | **Type** | **Unit** | **Description** |
|----------------|----------|----------|-----------------|
| `hour_utc` | *string* | — | UTC hour of the price (ISO 8601) |
| `hour_dk` | *string* | — | Danish local-time hour (ISO 8601) |
| `price_area` | *string* | — | Nord Pool bidding zone (DK1, DK2) |
| `spot_price_dkk` | *double / null* | DKK/MWh | Day-ahead spot price in DKK |
| `spot_price_eur` | *double / null* | EUR/MWh | Day-ahead spot price in EUR |
