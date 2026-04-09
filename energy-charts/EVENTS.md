# Energy-Charts European Electricity Data Bridge Events

This document describes the events emitted by the Energy-Charts Bridge.

- [info.energy_charts](#message-group-infoenergy_charts)
  - [info.energy_charts.PublicPower](#message-infoenergy_chartspublicpower)
  - [info.energy_charts.SpotPrice](#message-infoenergy_chartsspotprice)
  - [info.energy_charts.GridSignal](#message-infoenergy_chartsgridsignal)

---

## Message Group: info.energy_charts

---

### Message: info.energy_charts.PublicPower

Net electricity generation by fuel type for a given country at a specific 15-minute interval.

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `info.energy_charts.PublicPower` |
| `source` | CloudEvent source | `string` | `True` | `https://api.energy-charts.info` |
| `subject` | Country code | `uritemplate` | `True` | `{country}` |

#### Schema: PublicPower

| **Field Name** | **Type** | **Unit** | **Description** |
|----------------|----------|----------|-----------------|
| `country` | *string* | — | ISO 3166-1 alpha-2 country code |
| `timestamp` | *string (date-time)* | — | UTC timestamp of the measurement interval |
| `unix_seconds` | *integer (int64)* | — | Unix epoch timestamp in seconds |
| `hydro_pumped_storage_consumption_mw` | *number* | MW | Pumped-storage consumption (typically negative) |
| `cross_border_electricity_trading_mw` | *number* | MW | Net cross-border exchange |
| `hydro_run_of_river_mw` | *number* | MW | Run-of-river hydroelectric generation |
| `biomass_mw` | *number* | MW | Biomass generation |
| `fossil_brown_coal_lignite_mw` | *number* | MW | Brown coal / lignite generation |
| `fossil_hard_coal_mw` | *number* | MW | Hard coal generation |
| `fossil_oil_mw` | *number* | MW | Oil-fired generation |
| `fossil_coal_derived_gas_mw` | *number* | MW | Coal-derived gas generation |
| `fossil_gas_mw` | *number* | MW | Natural gas generation |
| `geothermal_mw` | *number* | MW | Geothermal generation |
| `hydro_water_reservoir_mw` | *number* | MW | Reservoir hydroelectric generation |
| `hydro_pumped_storage_mw` | *number* | MW | Pumped-storage generation |
| `others_mw` | *number* | MW | Other sources |
| `waste_mw` | *number* | MW | Waste incineration generation |
| `wind_offshore_mw` | *number* | MW | Offshore wind generation |
| `wind_onshore_mw` | *number* | MW | Onshore wind generation |
| `solar_mw` | *number* | MW | Solar generation |
| `nuclear_mw` | *number* | MW | Nuclear generation |
| `load_mw` | *number* | MW | Total grid load (demand) |
| `residual_load_mw` | *number* | MW | Residual load (load minus variable renewables) |
| `renewable_share_of_generation_pct` | *number* | % | Renewable share of total generation |
| `renewable_share_of_load_pct` | *number* | % | Renewable share of total load |

---

### Message: info.energy_charts.SpotPrice

Day-ahead electricity spot price per bidding zone per timestamp.

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `info.energy_charts.SpotPrice` |
| `source` | CloudEvent source | `string` | `True` | `https://api.energy-charts.info` |
| `subject` | Country code | `uritemplate` | `True` | `{country}` |

#### Schema: SpotPrice

| **Field Name** | **Type** | **Unit** | **Description** |
|----------------|----------|----------|-----------------|
| `country` | *string* | — | ISO 3166-1 alpha-2 country code |
| `bidding_zone` | *string* | — | ENTSO-E bidding zone identifier |
| `timestamp` | *string (date-time)* | — | UTC timestamp of the price interval |
| `unix_seconds` | *integer (int64)* | — | Unix epoch timestamp in seconds |
| `price_eur_per_mwh` | *number* | EUR/MWh | Day-ahead spot price |
| `unit` | *string* | — | Unit label from the API |

---

### Message: info.energy_charts.GridSignal

Grid carbon signal (traffic light) per country per timestamp.

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `info.energy_charts.GridSignal` |
| `source` | CloudEvent source | `string` | `True` | `https://api.energy-charts.info` |
| `subject` | Country code | `uritemplate` | `True` | `{country}` |

#### Schema: GridSignal

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `country` | *string* | ISO 3166-1 alpha-2 country code |
| `timestamp` | *string (date-time)* | UTC timestamp of the measurement interval |
| `unix_seconds` | *integer (int64)* | Unix epoch timestamp in seconds |
| `signal` | *integer* | Traffic-light signal: 0=green, 1=yellow, 2=red |
| `renewable_share_pct` | *number* | Renewable share of generation (0–100%) |
| `substitute` | *boolean* | Whether this is a forecast/estimate rather than metered data |
