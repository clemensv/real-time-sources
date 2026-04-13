# NDW Road Traffic

Real-time road traffic data from the Dutch [Nationaal Dataportaal Wegverkeer (NDW)](https://www.ndw.nu/), the Netherlands national road traffic data platform. Provides live traffic speed, travel time, Dynamic Route Information Panel (DRIP) signs, Matrix Signal Installation (MSI) lane signals, and situation events (road works, bridge openings, temporary closures, speed limits, safety messages) for the Dutch national road network (rijkswegen and provinciale wegen).

## Data Sources

All data feeds are DATEX II XML files published as gzip-compressed files at [https://opendata.ndw.nu/](https://opendata.ndw.nu/):

| Feed | Format | Update Frequency | Description |
|------|--------|-----------------|-------------|
| `measurement_current.xml.gz` | DATEX II v3 | Static/periodic | Measurement site reference catalog (point and route sites) |
| `trafficspeed.xml.gz` | DATEX II v2 | ~1 min | Traffic speed and flow at fixed measurement points |
| `traveltime.xml.gz` | DATEX II v2 | ~1 min | Travel times on route sections |
| `dynamische_route_informatie_paneel.xml.gz` | DATEX II v3 | ~1 min | DRIP (Dynamic Route Information Panel) signs |
| `Matrixsignaalinformatie.xml.gz` | DATEX II v3 | ~1 min | MSI (Matrix Signal Installation) lane signals |
| `planningsfeed_wegwerkzaamheden_en_evenementen.xml.gz` | DATEX II v3 | ~5 min | Planned roadworks and events |
| `planningsfeed_brugopeningen.xml.gz` | DATEX II v3 | ~5 min | Bridge opening events |
| `tijdelijke_verkeersmaatregelen_afsluitingen.xml.gz` | DATEX II v3 | ~5 min | Temporary road closures |
| `tijdelijke_verkeersmaatregelen_maximum_snelheden.xml.gz` | DATEX II v3 | ~5 min | Temporary speed limits |
| `veiligheidsgerelateerde_berichten_srti.xml.gz` | DATEX II v3 | ~5 min | Safety-related traffic information |

## Event Model

### NL.NDW.AVG (Measurement Sites and Observations)

| Event Type | Subject/Key | Description |
|-----------|-------------|-------------|
| `NL.NDW.AVG.PointMeasurementSite` | `measurement-sites/{measurement_site_id}` | Reference: fixed sensor site metadata |
| `NL.NDW.AVG.RouteMeasurementSite` | `measurement-sites/{measurement_site_id}` | Reference: route section site metadata |
| `NL.NDW.AVG.TrafficObservation` | `measurement-sites/{measurement_site_id}` | Live speed and flow measurement |
| `NL.NDW.AVG.TravelTimeObservation` | `measurement-sites/{measurement_site_id}` | Live travel time measurement |

### NL.NDW.DRIP (Dynamic Route Information Panels)

| Event Type | Subject/Key | Description |
|-----------|-------------|-------------|
| `NL.NDW.DRIP.DripSign` | `drips/{vms_controller_id}/{vms_index}` | Reference: DRIP sign installation |
| `NL.NDW.DRIP.DripDisplayState` | `drips/{vms_controller_id}/{vms_index}` | Live sign display content |

### NL.NDW.MSI (Matrix Signal Installations)

| Event Type | Subject/Key | Description |
|-----------|-------------|-------------|
| `NL.NDW.MSI.MsiSign` | `msi-signs/{sign_id}` | Reference: MSI lane signal installation |
| `NL.NDW.MSI.MsiDisplayState` | `msi-signs/{sign_id}` | Live displayed image/speed limit |

### NL.NDW.Situations (Traffic Situations)

| Event Type | Subject/Key | Description |
|-----------|-------------|-------------|
| `NL.NDW.Situations.Roadwork` | `situations/{situation_record_id}` | Roadwork and maintenance events |
| `NL.NDW.Situations.BridgeOpening` | `situations/{situation_record_id}` | Bridge opening events |
| `NL.NDW.Situations.TemporaryClosure` | `situations/{situation_record_id}` | Temporary road closures |
| `NL.NDW.Situations.TemporarySpeedLimit` | `situations/{situation_record_id}` | Temporary speed limits |
| `NL.NDW.Situations.SafetyRelatedMessage` | `situations/{situation_record_id}` | Safety-related traffic information |

## Links

- [NDW Open Data Portal](https://www.ndw.nu/pagina/en/77/open_data)
- [NDW Data Catalog](https://opendata.ndw.nu/)
- [DATEX II Standard](https://www.datex2.eu/)
