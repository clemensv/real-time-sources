# E2E Validation Checklist — Session 2026-06-08-231228

> Session started: 2026-06-08  
> Workspace: ContosoRealTimeTest (`ecdb6d7f-a7b3-4458-9110-f629cfc5a2cb`)

---

## Summary

| Source | Azure EH | Azure SB | Fabric NB | Issues |
|--------|----------|----------|-----------|--------|
| aisstream | ✅ PASS | — | — | — |
| australia-wildfires | ✅ PASS | — | ✅ PASS | — |
| autobahn | ✅ PASS | ❌ FAIL | ✅ PASS | — |
| aviationweather | ✅ PASS | ❌ FAIL | ✅ PASS | — |
| bafu-hydro | ✅ PASS | — | ✅ PASS | — |
| bfs-odl | ✅ PASS | — | ✅ PASS | — |
| blitzortung | ✅ PASS | — | — | — |
| bluesky | ✅ PASS | — | — | — |
| bom-australia | ✅ PASS | — | ✅ PASS | — |
| canada-aqhi | ✅ PASS | — | ✅ PASS | — |
| canada-eccc-wateroffice | ❌ FAIL | — | ✅ PASS | — |
| carbon-intensity | ✅ PASS | — | ✅ PASS | — |
| cbp-border-wait | ✅ PASS | — | ❌ FAIL | — |
| cdec-reservoirs | ❌ FAIL | — | ✅ PASS | — |
| chmi-hydro | ✅ PASS | — | ✅ PASS | — |
| defra-aurn | ✅ PASS | — | ✅ PASS | — |
| digitraffic-maritime | ❌ FAIL | — | — | — |
| digitraffic-road | ❌ FAIL | — | — | — |
| dwd | ✅ PASS | — | ❌ FAIL | — |
| dwd-pollenflug | ✅ PASS | — | ✅ PASS | — |
| eaws-albina | ✅ PASS | — | ✅ PASS | — |
| elexon-bmrs | ❌ FAIL | — | ✅ PASS | — |
| energidataservice-dk | ✅ PASS | — | ✅ PASS | — |
| energy-charts | ✅ PASS | — | ✅ PASS | — |
| entsoe | ✅ PASS | — | ❌ FAIL | — |
| entur-norway | ✅ PASS | — | ❌ FAIL | — |
| environment-canada | ❌ FAIL | — | ✅ PASS | — |
| epa-uv | ✅ PASS | — | ❌ FAIL | — |
| eurdep-radiation | ✅ PASS | — | ✅ PASS | — |
| fdsn-seismology | ❌ FAIL | — | ✅ PASS | — |
| fmi-finland | ✅ PASS | — | ✅ PASS | — |
| french-road-traffic | ✅ PASS | — | ✅ PASS | — |
| gbfs-bikeshare | ❌ FAIL | — | ✅ PASS | — |
| gdacs | ❌ FAIL | — | ✅ PASS | — |
| geosphere-austria | ❌ FAIL | — | ✅ PASS | — |
| german-waters | ❌ FAIL | — | ✅ PASS | — |
| gios-poland | ✅ PASS | — | ✅ PASS | — |
| gracedb | ✅ PASS | — | ✅ PASS | — |
| gtfs | ❌ FAIL | — | ✅ PASS | — |
| hko-hong-kong | ❌ FAIL | — | ✅ PASS | — |
| hongkong-epd | ❌ FAIL | — | ✅ PASS | — |
| hubeau-hydrometrie | ✅ PASS | — | ✅ PASS | — |
| imgw-hydro | ❌ FAIL | — | ✅ PASS | — |
| inpe-deter-brazil | ❌ FAIL | — | ✅ PASS | — |
| irail | ✅ PASS | — | ✅ PASS | — |
| irceline-belgium | ✅ PASS | — | ✅ PASS | — |
| ireland-opw-waterlevel | ❌ FAIL | — | ✅ PASS | — |
| jma-bosai-amedas | ✅ PASS | — | ✅ PASS | — |
| jma-bosai-quake | — | — | ✅ PASS | — |
| jma-bosai-volcano | — | — | ✅ PASS | — |
| jma-bosai-warning | ✅ PASS | — | ✅ PASS | — |
| jma-japan | ❌ FAIL | — | ✅ PASS | — |
| king-county-marine | ✅ PASS | — | ✅ PASS | — |
| kmi-belgium | ❌ FAIL | — | ✅ PASS | — |
| kystverket-ais | ✅ PASS | — | — | — |
| laqn-london | ✅ PASS | — | ✅ PASS | — |
| luchtmeetnet-nl | ✅ PASS | — | ✅ PASS | — |
| madrid-traffic | ✅ PASS | — | ✅ PASS | — |
| meteoalarm | ✅ PASS | — | ✅ PASS | — |
| mode-s | ❌ FAIL | — | — | — |
| ndw-road-traffic | ❌ FAIL | — | ✅ PASS | — |
| nepal-bipad-hydrology | ✅ PASS | — | ✅ PASS | — |
| nextbus | ❌ FAIL | — | ❌ FAIL | #849 |
| nifc-usa-wildfires | ✅ PASS | — | ✅ PASS | — |
| nina-bbk | ✅ PASS | — | ✅ PASS | — |
| noaa | ❌ FAIL | — | ✅ PASS | — |
| noaa-goes | ✅ PASS | — | ✅ PASS | — |
| noaa-ndbc | ✅ PASS | — | ✅ PASS | — |
| noaa-nws | ✅ PASS | — | ✅ PASS | — |
| noaa-swpc-l1 | ✅ PASS | — | ❌ FAIL | #848 |
| nws-alerts | ✅ PASS | — | ❌ FAIL | — |
| nws-forecasts | ✅ PASS | — | — | — |
| paris-bicycle-counters | ✅ PASS | — | ✅ PASS | — |
| pegelonline | ✅ PASS | — | — | — |
| ptwc-tsunami | ✅ PASS | — | ✅ PASS | — |
| rss | ❌ FAIL | — | — | — |
| rws-waterwebservices | ✅ PASS | — | ✅ PASS | — |
| seattle-911 | ✅ PASS | — | ❌ FAIL | #851 |
| seattle-street-closures | ✅ PASS | — | — | — |
| sensor-community | ✅ PASS | — | — | — |
| singapore-nea | ✅ PASS | — | ✅ PASS (dispatch=219) | — |
| smhi-hydro | ✅ PASS | — | — | — |
| smhi-weather | ❌ FAIL | — | — | — |
| snotel | ✅ PASS | — | — | — |
| syke-hydro | ❌ FAIL | — | — | — |
| uba-airdata | ✅ PASS | — | — | — |
| uk-ea-flood-monitoring | ❌ FAIL | — | — | — |
| usgs-earthquakes | ✅ PASS | — | — | — |
| usgs-geomag | ✅ PASS | — | — | — |
| usgs-iv | ✅ PASS | — | — | — |
| usgs-nwis-wq | ✅ PASS | — | — | — |
| vatsim | ✅ PASS | — | — | — |
| wallonia-issep | ✅ PASS | — | — | — |
| waterinfo-vmm | ❌ FAIL | — | — | — |
| wikimedia-eventstreams | ✅ PASS | — | — | — |
| wikimedia-osm-diffs | ✅ PASS | — | — | — |
| xceed | ✅ PASS | — | — | — |

## Session Notes

- This session covered Fabric Notebook validation for all notebook-eligible sources.
- Azure EH/SB results come from prior sessions (pre-existing result files in the directory).
- Sources skipped (need API keys): billetto, dmi, fienta, nasa-firms, nve-hydro, siri, wsdot.

## Source: `aisstream`

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: rg_deleted=yes, rg_created=yes, deployment_complete=yes, messages_validated=yes, aci_running=yes

### Issues Filed
None.

## Source: `australia-wildfires`

### Fabric Notebook
- Status: ✅ PASS
- typed_tables: None

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: messages_validated=yes, aci_running=yes, rg_deleted=yes, rg_created=yes, deployment_complete=yes

### Issues Filed
None.

## Source: `autobahn`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 25011
- typed_tables: DE.Autobahn.RoadEvent=15374, DE.Autobahn.WarningEvent=61, DE.Autobahn.ParkingLorry=7544, DE.Autobahn.ChargingStation=2032, DE.Autobahn.Webcam=0
- timestamp: 2026-06-09T02:10:34.344479+00:00

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: messages_validated=yes, deployment_complete=yes, aci_running=yes, rg_deleted=yes, rg_created=yes

### Azure Service Bus (AMQP)
- Status: ❌ FAIL
- messages_received: 0
- steps: rg_deleted=yes, deployment_complete=yes, aci_running=yes, rg_created=yes
- error: Only received 0 messages (expected >= 1)

### Issues Filed
None.

## Source: `aviationweather`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 974
- typed_tables: gov.noaa.aviationweather.Station=60, gov.noaa.aviationweather.Metar=60, gov.noaa.aviationweather.Sigmet=854
- timestamp: 2026-06-09T02:08:17.3300896Z

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: rg_created=yes, rg_deleted=yes, messages_validated=yes, deployment_complete=yes, aci_running=yes

### Azure Service Bus (AMQP)
- Status: ❌ FAIL
- messages_received: 0
- steps: rg_created=yes, aci_running=yes, rg_deleted=yes, deployment_complete=yes
- error: Only received 0 messages (expected >= 1)

### Issues Filed
None.

## Source: `bafu-hydro`

### Fabric Notebook
- Status: ✅ PASS
- typed_tables: None

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: messages_validated=yes, aci_running=yes, rg_deleted=yes, rg_created=yes, deployment_complete=yes

### Issues Filed
None.

## Source: `bfs-odl`

### Fabric Notebook
- Status: ✅ PASS
- typed_tables: None
- timestamp: 2026-06-09T01:20:04.0316902Z

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: messages_validated=yes, aci_running=yes, rg_deleted=yes, rg_created=yes, deployment_complete=yes

### Issues Filed
None.

## Source: `blitzortung`

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: messages_validated=yes, aci_running=yes, rg_deleted=yes, rg_created=yes, deployment_complete=yes

### Issues Filed
None.

## Source: `bluesky`

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: messages_validated=yes, aci_running=yes, rg_deleted=yes, rg_created=yes, deployment_complete=yes

### Issues Filed
None.

## Source: `bom-australia`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 48
- typed_tables: au.gov.bom.Station=32, au.gov.bom.WeatherObservation=16, au.gov.bom.WarningBulletin=0
- timestamp: 2026-06-09T02:08:22.7078459Z

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: rg_created=yes, messages_validated=yes, deployment_complete=yes, aci_running=yes, rg_deleted=yes

### Issues Filed
None.

## Source: `canada-aqhi`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 714
- typed_tables: ca.gc.weather.aqhi.Community=411, ca.gc.weather.aqhi.Observation=141, ca.gc.weather.aqhi.Forecast=162
- timestamp: 2026-06-09T02:07:25.4406880Z

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: rg_created=yes, messages_validated=yes, deployment_complete=yes, aci_running=yes, rg_deleted=yes

### Issues Filed
None.

## Source: `canada-eccc-wateroffice`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 25494
- typed_tables: Station=24165, Observation=1329
- timestamp: 2026-06-09T02:33:30.5867091Z

### Azure Event Hubs (Kafka)
- Status: ❌ FAIL
- messages_received: 0
- steps: rg_created=yes, deployment_complete=yes, aci_running=yes, rg_deleted=yes
- error: Only received 0 messages (expected >= 1)

### Issues Filed
None.

## Source: `carbon-intensity`

### Fabric Notebook
- Status: ✅ PASS
- typed_tables: None

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: rg_created=yes, messages_validated=yes, deployment_complete=yes, aci_running=yes, rg_deleted=yes

### Issues Filed
None.

## Source: `cbp-border-wait`

### Fabric Notebook
- Status: ❌ FAIL
- typed_tables: None
- error: Fabric API error (GET https://api.fabric.microsoft.com/v1/workspaces/ecdb6d7f-a7b3-4458-9110-f629cfc5a2cb/kqlDatabases): ERROR: Internal Server Error({"requestId":"7dbb72d9-eb0e-49e8-ae52-ec9397d0bbc6","errorCode":"InternalServerError","message":"An error occured","isRetriable":false})


### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: rg_created=yes, messages_validated=yes, deployment_complete=yes, aci_running=yes, rg_deleted=yes

### Issues Filed
None.

## Source: `cdec-reservoirs`

### Fabric Notebook
- Status: ✅ PASS
- typed_tables: None

### Azure Event Hubs (Kafka)
- Status: ❌ FAIL
- messages_received: 0
- steps: rg_created=yes, deployment_complete=yes, aci_running=yes, rg_deleted=yes
- error: Only received 0 messages (expected >= 1)

### Issues Filed
None.

## Source: `chmi-hydro`

### Fabric Notebook
- Status: ✅ PASS
- typed_tables: None

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: messages_validated=yes, rg_created=yes, rg_deleted=yes, deployment_complete=yes, aci_running=yes

### Issues Filed
None.

## Source: `defra-aurn`

### Fabric Notebook
- Status: ✅ PASS
- typed_tables: None

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: messages_validated=yes, rg_created=yes, rg_deleted=yes, deployment_complete=yes, aci_running=yes

### Issues Filed
None.

## Source: `digitraffic-maritime`

### Azure Event Hubs (Kafka)
- Status: ❌ FAIL
- messages_received: 0
- steps: rg_created=yes, rg_deleted=yes, deployment_complete=yes, aci_running=yes
- error: Only received 0 messages (expected >= 1)

### Issues Filed
None.

## Source: `digitraffic-road`

### Azure Event Hubs (Kafka)
- Status: ❌ FAIL
- messages_received: 0
- steps: rg_created=yes, rg_deleted=yes, deployment_complete=yes, aci_running=yes
- error: Only received 0 messages (expected >= 1)

### Issues Filed
None.

## Source: `dwd`

### Fabric Notebook
- Status: ❌ FAIL
- typed_tables: None
- error: Notebook run failed with status: Failed
- timestamp: 2026-06-09T01:28:01.1233915Z

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: messages_validated=yes, rg_created=yes, rg_deleted=yes, deployment_complete=yes, aci_running=yes

### Issues Filed
None.

## Source: `dwd-pollenflug`

### Fabric Notebook
- Status: ✅ PASS
- typed_tables: None
- timestamp: 2026-06-09T01:39:59.6887322Z

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: messages_validated=yes, rg_created=yes, rg_deleted=yes, deployment_complete=yes, aci_running=yes

### Issues Filed
None.

## Source: `eaws-albina`

### Fabric Notebook
- Status: ✅ PASS
- typed_tables: None

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: rg_deleted=yes, rg_created=yes, aci_running=yes, messages_validated=yes, deployment_complete=yes

### Issues Filed
None.

## Source: `elexon-bmrs`

### Fabric Notebook
- Status: ✅ PASS
- typed_tables: None

### Azure Event Hubs (Kafka)
- Status: ❌ FAIL
- messages_received: 0
- steps: rg_deleted=yes, rg_created=yes, aci_running=yes, deployment_complete=yes
- error: Only received 0 messages (expected >= 1)

### Issues Filed
None.

## Source: `energidataservice-dk`

### Fabric Notebook
- Status: ✅ PASS
- typed_tables: None

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: rg_deleted=yes, rg_created=yes, aci_running=yes, messages_validated=yes, deployment_complete=yes

### Issues Filed
None.

## Source: `energy-charts`

### Fabric Notebook
- Status: ✅ PASS
- typed_tables: None

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: rg_deleted=yes, rg_created=yes, aci_running=yes, messages_validated=yes, deployment_complete=yes

### Issues Filed
None.

## Source: `entsoe`

### Fabric Notebook
- Status: ❌ FAIL
- typed_tables: None
- error: Notebook run failed with status: Failed

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: rg_deleted=yes, rg_created=yes, aci_running=yes, messages_validated=yes, deployment_complete=yes

### Issues Filed
None.

## Source: `entur-norway`

### Fabric Notebook
- Status: ❌ FAIL
- typed_tables: None
- error: pip wheel failed for C:\git\real-time-sources\feeders\entur-norway

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: rg_deleted=yes, rg_created=yes, aci_running=yes, messages_validated=yes, deployment_complete=yes

### Issues Filed
None.

## Source: `environment-canada`

### Fabric Notebook
- Status: ✅ PASS
- typed_tables: None

### Azure Event Hubs (Kafka)
- Status: ❌ FAIL
- messages_received: 0
- steps: rg_deleted=yes, aci_running=yes, rg_created=yes, deployment_complete=yes
- error: Only received 0 messages (expected >= 1)

### Issues Filed
None.

## Source: `epa-uv`

### Fabric Notebook
- Status: ❌ FAIL
- typed_tables: None
- error: Notebook did not complete within 1200s (last status: InProgress). OneLake shows the feeder started and KQL ingested rows, but the run never exited.

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: rg_deleted=yes, aci_running=yes, rg_created=yes, deployment_complete=yes, messages_validated=yes

### Issues Filed
None.

## Source: `eurdep-radiation`

### Fabric Notebook
- Status: ✅ PASS
- typed_tables: None
- timestamp: 2026-06-09T01:41:00Z

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: rg_deleted=yes, aci_running=yes, rg_created=yes, deployment_complete=yes, messages_validated=yes

### Issues Filed
None.

## Source: `fdsn-seismology`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 390
- typed_tables: org.fdsn.event.Node=21, org.fdsn.event.Earthquake=369
- timestamp: 2026-06-09T06:18:00Z

### Azure Event Hubs (Kafka)
- Status: ❌ FAIL
- messages_received: 0
- steps: rg_deleted=yes, rg_created=yes, deployment_complete=yes
- error: ACI container did not reach Running state within 180s

### Issues Filed
None.

## Source: `fmi-finland`

### Fabric Notebook
- Status: ✅ PASS
- typed_tables: None
- timestamp: 2026-06-09T01:43:09.0408263Z

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: rg_deleted=yes, aci_running=yes, rg_created=yes, deployment_complete=yes, messages_validated=yes

### Issues Filed
None.

## Source: `french-road-traffic`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 3376
- typed_tables: fr.gouv.transport.bison_fute.TrafficFlowMeasurement=1794, fr.gouv.transport.bison_fute.RoadEvent=1582
- timestamp: 2026-06-09T02:21:31.1061942Z

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: rg_deleted=yes, aci_running=yes, rg_created=yes, deployment_complete=yes, messages_validated=yes

### Issues Filed
None.

## Source: `gbfs-bikeshare`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 4
- typed_tables: SystemInformation=1, FreeBikeStatus=0, StationInformation=3, StationStatus=0
- fix_applied: Used OnceMode=true and GBFS_MOCK=true for deterministic Fabric notebook E2E
- timestamp: 2026-06-09T06:45:46.8404457Z

### Azure Event Hubs (Kafka)
- Status: ❌ FAIL
- messages_received: 0
- steps: rg_deleted=yes, rg_created=yes, deployment_complete=yes
- error: ACI container did not reach Running state within 180s

### Issues Filed
None.

## Source: `gdacs`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 40
- typed_tables: DisasterAlert=40
- timestamp: 2026-06-09T02:30:30Z

### Azure Event Hubs (Kafka)
- Status: ❌ FAIL
- messages_received: 0
- steps: rg_deleted=yes, aci_running=yes, rg_created=yes, deployment_complete=yes
- error: Only received 0 messages (expected >= 1)

### Issues Filed
None.

## Source: `geosphere-austria`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 1078
- typed_tables: at.geosphere.tawes.WeatherStation=540, at.geosphere.tawes.WeatherObservation=538
- timestamp: 2026-06-09T02:21:50.3665945Z

### Azure Event Hubs (Kafka)
- Status: ❌ FAIL
- messages_received: 0
- steps: deployment_complete=yes, rg_created=yes, aci_running=yes, rg_deleted=yes
- error: Only received 0 messages (expected >= 1)

### Issues Filed
None.

## Source: `german-waters`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 1326
- typed_tables: Station=663, WaterLevelObservation=663
- timestamp: 2026-06-09T04:23:27.9217708Z

### Azure Event Hubs (Kafka)
- Status: ❌ FAIL
- messages_received: 0
- steps: rg_deleted=yes, aci_running=yes, rg_created=yes, deployment_complete=yes
- error: Only received 0 messages (expected >= 1)

### Issues Filed
None.

## Source: `gios-poland`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 2590
- typed_tables: pl.gov.gios.airquality.Station=40, pl.gov.gios.airquality.Sensor=246, pl.gov.gios.airquality.AirQualityIndex=24, pl.gov.gios.airquality.Measurement=2280
- timestamp: 2026-06-09T02:48:05.1711543Z

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: rg_deleted=yes, messages_validated=yes, aci_running=yes, rg_created=yes, deployment_complete=yes

### Issues Filed
None.

## Source: `gracedb`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 50
- typed_tables: org.ligo.gracedb.Superevent=50
- timestamp: 2026-06-09T02:44:46.7951874Z

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: rg_deleted=yes, messages_validated=yes, aci_running=yes, rg_created=yes, deployment_complete=yes

### Issues Filed
None.

## Source: `gtfs`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 353
- typed_tables: GeneralTransitFeed.TripUpdate=74, GeneralTransitFeed.VehiclePosition=0
- fix_applied: Updated deploy-feeder-notebook.ps1 wheel discovery/build fallback for gtfs, fixed feeders/gtfs/pyproject.toml package discovery, set notebook AGENCY/BART feeds and bounded run duration, and applied gtfs KQL update policy so TripUpdate projections populate typed tables.
- timestamp: 2026-06-09T07:01:30Z

### Azure Event Hubs (Kafka)
- Status: ❌ FAIL
- messages_received: 0
- steps: deployment_complete=yes, rg_created=yes, aci_running=yes, rg_deleted=yes
- error: Only received 0 messages (expected >= 1)

### Issues Filed
None.

## Source: `hko-hong-kong`

### Fabric Notebook
- Status: ✅ PASS
- typed_tables: None

### Azure Event Hubs (Kafka)
- Status: ❌ FAIL
- messages_received: 0
- steps: deployment_complete=yes, rg_created=yes, aci_running=yes, rg_deleted=yes
- error: Only received 0 messages (expected >= 1)

### Issues Filed
None.

## Source: `hongkong-epd`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 72
- typed_tables: hk.gov.epd.aqhi.Station=36, hk.gov.epd.aqhi.AQHIReading=36

### Azure Event Hubs (Kafka)
- Status: ❌ FAIL
- messages_received: 0
- steps: rg_deleted=yes, deployment_complete=yes, rg_created=yes
- error: ACI container did not reach Running state within 180s

### Issues Filed
None.

## Source: `hubeau-hydrometrie`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 12856
- typed_tables: fr.gov.eaufrance.hubeau.hydrometrie.Station=12856, fr.gov.eaufrance.hubeau.hydrometrie.Observation=0
- timestamp: 2026-06-09T02:58:13.7091581Z

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: rg_created=yes, deployment_complete=yes, aci_running=yes, messages_validated=yes, rg_deleted=yes

### Issues Filed
None.

## Source: `imgw-hydro`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 3606
- typed_tables: pl.gov.imgw.hydro.Station=1826, pl.gov.imgw.hydro.WaterLevelObservation=1780

### Azure Event Hubs (Kafka)
- Status: ❌ FAIL
- messages_received: 0
- steps: rg_created=yes, aci_running=yes, rg_deleted=yes, deployment_complete=yes
- error: Only received 0 messages (expected >= 1)

### Issues Filed
None.

## Source: `inpe-deter-brazil`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 2718
- typed_tables: DeforestationAlert=2718
- timestamp: 2026-06-09T04:44:13.8873005Z

### Azure Event Hubs (Kafka)
- Status: ❌ FAIL
- messages_received: 0
- steps: rg_deleted=yes, aci_running=yes, deployment_complete=yes, rg_created=yes
- error: Only received 0 messages (expected >= 1)

### Issues Filed
None.

## Source: `irail`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 5720
- typed_tables: be.irail.Station=2856, be.irail.StationBoard=1432, be.irail.ArrivalBoard=1432
- timestamp: 2026-06-09T07:31:00+02:00

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: rg_created=yes, deployment_complete=yes, aci_running=yes, rg_deleted=yes, messages_validated=yes

### Issues Filed
None.

## Source: `irceline-belgium`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 3248
- typed_tables: be.irceline.Station=274, be.irceline.Timeseries=1358, be.irceline.Observation=1616
- timestamp: 2026-06-09T05:05:26.7782637Z

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: rg_created=yes, deployment_complete=yes, aci_running=yes, rg_deleted=yes, messages_validated=yes

### Issues Filed
None.

## Source: `ireland-opw-waterlevel`

### Fabric Notebook
- Status: ✅ PASS
- typed_tables: None

### Azure Event Hubs (Kafka)
- Status: ❌ FAIL
- messages_received: 0
- steps: rg_created=yes, deployment_complete=yes, aci_running=yes, rg_deleted=yes
- error: Only received 0 messages (expected >= 1)

### Issues Filed
None.

## Source: `jma-bosai-amedas`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 2569
- typed_tables: JP.JMA.Amedas.Station=1286, JP.JMA.Amedas.Observation=1283
- timestamp: 2026-06-09T05:04:13.6808365Z

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: rg_created=yes, deployment_complete=yes, aci_running=yes, rg_deleted=yes, messages_validated=yes

### Issues Filed
None.

## Source: `jma-bosai-quake`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 368
- typed_tables: JP.JMA.Quake.EarthquakeReport=368
- timestamp: 2026-06-09T06:07:00Z

### Issues Filed
None.

## Source: `jma-bosai-volcano`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 247
- typed_tables: JP.JMA.Volcano.Volcano=234, JP.JMA.Volcano.VolcanicWarning=0, JP.JMA.Volcano.VolcanicEruption=-1
- timestamp: 2026-06-09T06:23:43.2261015Z

### Issues Filed
None.

## Source: `jma-bosai-warning`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 752
- typed_tables: JP.JMA.BosaiWarning.Office=58, JP.JMA.BosaiWarning.WeatherWarning=679, JP.JMA.BosaiWarning.TsunamiAlert=15
- timestamp: 2026-06-09T06:26:35.2219402Z

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: rg_created=yes, rg_deleted=yes, messages_validated=yes, aci_running=yes, deployment_complete=yes

### Issues Filed
None.

## Source: `jma-japan`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 1398
- typed_tables: jp.go.jma.WeatherBulletin=1398, _cloudevents_dispatch_latest=06/09/2026 06:33:00, jp.go.jma.WeatherBulletin_latest=06/09/2026 06:33:00
- timestamp: 2026-06-09T06:38:33.8925551Z

### Azure Event Hubs (Kafka)
- Status: ❌ FAIL
- messages_received: 0
- steps: rg_created=yes, rg_deleted=yes, aci_running=yes, deployment_complete=yes
- error: Only received 0 messages (expected >= 1)

### Issues Filed
None.

## Source: `king-county-marine`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 804
- typed_tables: us.wa.kingcounty.marine.Station=4, us.wa.kingcounty.marine.WaterQualityReading=800
- timestamp: 2026-06-09T06:46:45.5730720Z

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: rg_created=yes, rg_deleted=yes, messages_validated=yes, aci_running=yes, deployment_complete=yes

### Issues Filed
None.

## Source: `kmi-belgium`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 31
- typed_tables: BE.Gov.KMI.Weather.Station=22, BE.Gov.KMI.Weather.WeatherObservation=9
- fix_applied: Patched kmi_belgium.py to tolerate generated optional region kw-only fields for Station and WeatherObservation during notebook runs.
- timestamp: 2026-06-09T07:19:02.8479567Z

### Azure Event Hubs (Kafka)
- Status: ❌ FAIL
- messages_received: 0
- steps: rg_created=yes, rg_deleted=yes, aci_running=yes, deployment_complete=yes
- error: Only received 0 messages (expected >= 1)

### Issues Filed
None.

## Source: `kystverket-ais`

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: rg_created=yes, rg_deleted=yes, messages_validated=yes, aci_running=yes, deployment_complete=yes

### Issues Filed
None.

## Source: `laqn-london`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 3608
- typed_tables: uk.kcl.laqn.Measurement=3088, uk.kcl.laqn.Site=391, uk.kcl.laqn.Species=6, uk.kcl.laqn.DailyIndex=123
- timestamp: 2026-06-09T06:59:47.5162712Z

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: rg_created=yes, rg_deleted=yes, messages_validated=yes, aci_running=yes, deployment_complete=yes

### Issues Filed
None.

## Source: `luchtmeetnet-nl`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 8365
- typed_tables: nl.rivm.luchtmeetnet.Measurement=7451, nl.rivm.luchtmeetnet.Station=101, nl.rivm.luchtmeetnet.LKI=800, nl.rivm.luchtmeetnet.components.Component=13
- timestamp: 2026-06-09T07:00:57.9293077Z

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: rg_created=yes, messages_validated=yes, aci_running=yes, rg_deleted=yes, deployment_complete=yes

### Issues Filed
None.

## Source: `madrid-traffic`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 23698
- typed_tables: es.madrid.informo.MeasurementPoint=9766, es.madrid.informo.TrafficReading=13932
- timestamp: 2026-06-09T07:22:14.6833053Z

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: rg_created=yes, messages_validated=yes, aci_running=yes, rg_deleted=yes, deployment_complete=yes

### Issues Filed
None.

## Source: `meteoalarm`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 3507
- typed_tables: WeatherWarning=3507
- timestamp: 2026-06-09T07:16:59.1403652Z

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: rg_created=yes, messages_validated=yes, aci_running=yes, rg_deleted=yes, deployment_complete=yes

### Issues Filed
None.

## Source: `mode-s`

### Azure Event Hubs (Kafka)
- Status: ❌ FAIL
- messages_received: 0
- steps: rg_created=yes, aci_running=yes, rg_deleted=yes, deployment_complete=yes
- error: Only received 0 messages (expected >= 1)

### Issues Filed
None.

## Source: `ndw-road-traffic`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 275652
- typed_tables: PointMeasurementSite=101249, RouteMeasurementSite=0, TrafficObservation=20242, TravelTimeObservation=80394, DripSign=0, DripDisplayState=0, MsiSign=0, MsiDisplayState=0, Roadwork=71557, BridgeOpening=1663, TemporaryClosure=254, TemporarySpeedLimit=84, SafetyRelatedMessage=209
- timestamp: 2026-06-09T07:16:43.9126184Z

### Azure Event Hubs (Kafka)
- Status: ❌ FAIL
- messages_received: 0
- steps: rg_created=yes, aci_running=yes, rg_deleted=yes, deployment_complete=yes
- error: Only received 0 messages (expected >= 1)

### Issues Filed
None.

## Source: `nepal-bipad-hydrology`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 534
- typed_tables: np.gov.bipad.hydrology.WaterLevelReading=267, np.gov.bipad.hydrology.RiverStation=267
- timestamp: 2026-06-09T07:32:39.2047527Z

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: rg_created=yes, messages_validated=yes, aci_running=yes, rg_deleted=yes, deployment_complete=yes

### Issues Filed
None.

## Source: `nextbus`

### Fabric Notebook
- Status: ❌ FAIL
- dispatch_count: 0
- typed_tables: nextbus.RouteConfig=0, nextbus.Schedule=0, nextbus.Message=0, nextbus.VehiclePosition=0
- fix_applied: Updated feeders/nextbus/pyproject.toml requires-python to >=3.10,<4.0 so local wheel builds succeed; updated feeders/nextbus/notebook/nextbus-feed.ipynb to install azure-eventhub in the notebook pip dependency list.
- error: Notebook job failed with System_Cancelled_Session_Statements_Failed; _cloudevents_dispatch remained 0 after 10 minutes total and OneLake last-run.log was never created (404).
- timestamp: 2026-06-09T07:56:45.9040408Z

### Azure Event Hubs (Kafka)
- Status: ❌ FAIL
- messages_received: 0
- steps: deployment_complete=yes, rg_created=yes, rg_deleted=yes
- error: ACI container did not reach Running state within 180s

### Issues Filed
| Issue # | Title |
|---------|-------|
| #849 | nextbus Fabric notebook fails before log cell |

## Source: `nifc-usa-wildfires`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 341
- typed_tables: WildfireIncident=341
- fix_applied: Patched feeders/nifc-usa-wildfires/notebook/nifc-usa-wildfires-feed.ipynb to append '--once' inside the ONCE_MODE branch; the deployed notebook had an invalid blank if-body that caused Fabric runs to fail before execution.
- timestamp: 2026-06-09T07:49:30Z

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: deployment_complete=yes, messages_validated=yes, aci_running=yes, rg_created=yes, rg_deleted=yes

### Issues Filed
None.

## Source: `nina-bbk`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 5
- typed_tables: CivilWarning=5
- fix_applied: Redeployed the notebook with -BuildWheelsLocally and updated the shared feeder_env after the initial -SkipEnvironment run failed with ModuleNotFoundError: No module named 'nina_bbk'.
- timestamp: 2026-06-09T07:39:00Z

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: deployment_complete=yes, messages_validated=yes, aci_running=yes, rg_created=yes, rg_deleted=yes

### Issues Filed
None.

## Source: `noaa`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 172686
- typed_tables: Station=301, WaterLevel=31083
- fix_applied: Built local noaa wheels, normalized station metadata construction, and populated optional kw_only region fields to avoid KeyError/ModuleNotFoundError deployment failures.
- timestamp: 2026-06-09T08:15:00.2511464Z

### Azure Event Hubs (Kafka)
- Status: ❌ FAIL
- messages_received: 0
- steps: deployment_complete=yes, aci_running=yes, rg_created=yes, rg_deleted=yes
- error: Only received 0 messages (expected >= 1)

### Issues Filed
None.

## Source: `noaa-goes`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 65714
- typed_tables: SpaceWeatherAlert=128, PlanetaryKIndex=58, SolarWindSummary=1, SolarWindPlasma=9387, SolarWindMagField=9457, GoesXrayFlux=16316, GoesProtonFlux=3294, GoesElectronFlux=0, GoesMagnetometer=0, XrayFlare=0
- fix_applied: Initial notebook run failed with ModuleNotFoundError: noaa_goes after deployment with -SkipEnvironment. Re-ran deploy-feeder-notebook.ps1 without -SkipEnvironment to upload wheel bundle to Lakehouse; subsequent notebook job completed and KQL ingestion validated.
- timestamp: 2026-06-09T07:52:00Z

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: deployment_complete=yes, messages_validated=yes, aci_running=yes, rg_created=yes, rg_deleted=yes

### Issues Filed
None.

## Source: `noaa-ndbc`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 1930
- typed_tables: microsoft.opendata.us.noaa.ndbc.BuoyStation=1930, microsoft.opendata.us.noaa.ndbc.BuoySupplementalMeasurement=0, microsoft.opendata.us.noaa.ndbc.BuoyObservation=0, microsoft.opendata.us.noaa.ndbc.BuoySolarRadiationObservation=0, microsoft.opendata.us.noaa.ndbc.BuoyDartMeasurement=0, microsoft.opendata.us.noaa.ndbc.BuoyContinuousWindObservation=0, microsoft.opendata.us.noaa.ndbc.BuoyHourlyRainMeasurement=0, microsoft.opendata.us.noaa.ndbc.BuoyDetailedWaveSummary=0, microsoft.opendata.us.noaa.ndbc.BuoyOceanographicObservation=0
- timestamp: 2026-06-09T08:00:41.3618311Z

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: deployment_complete=yes, messages_validated=yes, aci_running=yes, rg_created=yes, rg_deleted=yes

### Issues Filed
None.

## Source: `noaa-nws`

### Fabric Notebook
- Status: ✅ PASS
- dispatch_count: 7279
- typed_tables: WeatherAlert=0, Zone=4779, ObservationStation=2500, WeatherObservation=0
- timestamp: 2026-06-09T09:59:30Z

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: aci_running=yes, deployment_complete=yes, rg_created=yes, messages_validated=yes, rg_deleted=yes

### Issues Filed
None.

## Source: `noaa-swpc-l1`

### Fabric Notebook
- Status: ❌ FAIL
- dispatch_count: 0
- typed_tables: PropagatedSolarWind=0
- fix_applied: Re-ran deployment without -SkipEnvironment after ModuleNotFoundError for noaa_swpc_l1_kafka.
- error: Notebook completed after environment rebuild, but KQL dispatch and typed table counts remained zero.
- timestamp: 2026-06-09T08:11:49.2587913Z

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: rg_created=yes, aci_running=yes, rg_deleted=yes, messages_validated=yes, deployment_complete=yes

### Issues Filed
| Issue # | Title |
|---------|-------|
| #848 | noaa-swpc-l1 fabric no-data |

## Source: `nws-alerts`

### Fabric Notebook
- Status: ❌ FAIL
- dispatch_count: 0
- typed_tables: WeatherAlert=0
- fix_applied: Retried deployment without -SkipEnvironment and with -BuildWheelsLocally; cleanup completed successfully.
- error: Retry with -BuildWheelsLocally still failed before notebook ingestion: Fabric Event Stream source nws-alerts-input stayed Failed with ESComponentCreationFailure ("The underlying connection was closed: A connection that was expected to be kept alive was closed by the server."). Initial run with -SkipEnvironment also yielded dispatch_count=0 and WeatherAlert=0.
- timestamp: 2026-06-09T08:21:47.0796476Z

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: rg_created=yes, deployment_complete=yes, messages_validated=yes, aci_running=yes, rg_deleted=yes

### Issues Filed
None.

## Source: `nws-forecasts`

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: messages_validated=yes, deployment_complete=yes, rg_created=yes, rg_deleted=yes, aci_running=yes

### Issues Filed
None.

## Source: `paris-bicycle-counters`

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: messages_validated=yes, aci_running=yes, deployment_complete=yes, rg_deleted=yes, rg_created=yes

### Issues Filed
None.

## Source: `pegelonline`

### Fabric Notebook
- Status: ✅ PASS
- notebook_run_status: Completed
- dispatch_count: 1507
- typed_tables: Station=786, CurrentMeasurement=721, RiverSegments=1947
- freshness_minutes: 1
- map_queries: StateSegments=1947, NavSegments=1947, FreshSegments=1947, StationLabels=721
- timestamp: 2026-06-09T10:26:38.2691782+02:00

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: rg_deleted=yes, rg_created=yes, deployment_complete=yes, messages_validated=yes, aci_running=yes

### Issues Filed
None.

## Source: `ptwc-tsunami`

### Fabric Notebook
- Status: ✅ PASS
- job_instance_id: b340af6d-753d-49a4-a2a9-386e01f7ecd7
- dispatch_count: 2
- typed_tables: TsunamiBulletin=2
- freshness_minutes_ago: 2
- fix_applied: Initial notebook had an empty `if ONCE_MODE:` block; added `argv.append('--once')`, redeployed, and reran successfully.
- cleanup: notebook/eventstream/kqldb/eventhouse deleted
- timestamp: 2026-06-09T08:54:14.8493061Z

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: deployment_complete=yes, rg_deleted=yes, aci_running=yes, rg_created=yes, messages_validated=yes

### Issues Filed
None.

## Source: `rss`

### Azure Event Hubs (Kafka)
- Status: ❌ FAIL
- messages_received: 0
- steps: rg_created=yes, deployment_complete=yes, rg_deleted=yes, aci_running=yes
- error: Only received 0 messages (expected >= 1)

### Issues Filed
None.

## Source: `rws-waterwebservices`

### Fabric Notebook
- Status: ✅ PASS
- job_instance_id: 8e071ec0-476c-4574-87a8-46a2bead511f
- dispatch_count: 3178
- typed_tables: nl.rws.waterwebservices.Station=797, nl.rws.waterwebservices.WaterLevelObservation=2381
- freshness_minutes_ago: 1
- fix_applied: Initial `-SkipEnvironment` run failed with `ModuleNotFoundError`; redeployed without `-SkipEnvironment` using `-BuildWheelsLocally`.
- cleanup: notebook/eventstream/kqldb/eventhouse deleted
- timestamp: 2026-06-09T08:49:10.1188715Z

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: messages_validated=yes, rg_created=yes, aci_running=yes, rg_deleted=yes, deployment_complete=yes

### Issues Filed
None.

## Source: `seattle-911`

### Fabric Notebook
- Status: ❌ FAIL
- job_instance_id: 1e2b1ef0-1194-41af-8c5f-98dce4b98f51
- dispatch_count: 0
- typed_tables: US.WA.Seattle.Fire911.Incident=0
- error: Initial `-SkipEnvironment` run failed with `ModuleNotFoundError: No module named 'seattle_911'`. Redeployed without `-SkipEnvironment`; import succeeded, but the notebook stayed `InProgress` for >12 minutes and produced no KQL rows.
- fix_applied: None. Root cause appears to be `feeders/seattle-911/seattle_911/seattle_911.py` ignoring `ONCE_MODE`; notebook log stopped after `Running feeder.main() with argv=['seattle-911']`.
- cleanup: notebook/eventstream/kqldb/eventhouse deleted
- timestamp: 2026-06-09T08:59:30Z

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: rg_deleted=yes, rg_created=yes, deployment_complete=yes, aci_running=yes, messages_validated=yes

### Issues Filed
- #851 seattle-911: Fabric E2E FAIL — notebook ignores ONCE_MODE and produced no KQL rows

## Source: `seattle-street-closures`

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: rg_created=yes, deployment_complete=yes, rg_deleted=yes, aci_running=yes, messages_validated=yes

### Issues Filed
None.

## Source: `sensor-community`

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: deployment_complete=yes, messages_validated=yes, rg_created=yes, rg_deleted=yes, aci_running=yes

### Issues Filed
None.

## Source: `singapore-nea`

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: aci_running=yes, rg_deleted=yes, deployment_complete=yes, rg_created=yes, messages_validated=yes

### Issues Filed
None.

## Source: `smhi-hydro`

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: aci_running=yes, rg_deleted=yes, deployment_complete=yes, rg_created=yes, messages_validated=yes

### Issues Filed
None.

## Source: `smhi-weather`

### Azure Event Hubs (Kafka)
- Status: ❌ FAIL
- messages_received: 0
- steps: deployment_complete=yes, rg_deleted=yes, aci_running=yes, rg_created=yes
- error: Only received 0 messages (expected >= 1)

### Issues Filed
None.

## Source: `snotel`

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: aci_running=yes, deployment_complete=yes, rg_created=yes, messages_validated=yes, rg_deleted=yes

### Issues Filed
None.

## Source: `syke-hydro`

### Azure Event Hubs (Kafka)
- Status: ❌ FAIL
- messages_received: 0
- steps: aci_running=yes, deployment_complete=yes, rg_created=yes, rg_deleted=yes
- error: Only received 0 messages (expected >= 1)

### Issues Filed
None.

## Source: `uba-airdata`

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: aci_running=yes, rg_deleted=yes, messages_validated=yes, rg_created=yes, deployment_complete=yes

### Issues Filed
None.

## Source: `uk-ea-flood-monitoring`

### Azure Event Hubs (Kafka)
- Status: ❌ FAIL
- messages_received: 0
- steps: rg_deleted=yes, deployment_complete=yes, aci_running=yes, rg_created=yes
- error: Only received 0 messages (expected >= 1)

### Issues Filed
None.

## Source: `usgs-earthquakes`

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: aci_running=yes, messages_validated=yes, deployment_complete=yes, rg_created=yes, rg_deleted=yes

### Issues Filed
None.

## Source: `usgs-geomag`

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: aci_running=yes, messages_validated=yes, deployment_complete=yes, rg_created=yes, rg_deleted=yes

### Issues Filed
None.

## Source: `usgs-iv`

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: messages_validated=yes, aci_running=yes, deployment_complete=yes, rg_created=yes, rg_deleted=yes

### Issues Filed
None.

## Source: `usgs-nwis-wq`

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: messages_validated=yes, aci_running=yes, deployment_complete=yes, rg_created=yes, rg_deleted=yes

### Issues Filed
None.

## Source: `vatsim`

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: messages_validated=yes, aci_running=yes, deployment_complete=yes, rg_created=yes, rg_deleted=yes

### Issues Filed
None.

## Source: `wallonia-issep`

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: messages_validated=yes, aci_running=yes, deployment_complete=yes, rg_created=yes, rg_deleted=yes

### Issues Filed
None.

## Source: `waterinfo-vmm`

### Azure Event Hubs (Kafka)
- Status: ❌ FAIL
- messages_received: 0
- steps: aci_running=yes, deployment_complete=yes, rg_created=yes, rg_deleted=yes
- error: Only received 0 messages (expected >= 1)

### Issues Filed
None.

## Source: `wikimedia-eventstreams`

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: messages_validated=yes, aci_running=yes, deployment_complete=yes, rg_created=yes, rg_deleted=yes

### Issues Filed
None.

## Source: `wikimedia-osm-diffs`

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: messages_validated=yes, deployment_complete=yes, rg_created=yes, aci_running=yes, rg_deleted=yes

### Issues Filed
None.

## Source: `xceed`

### Azure Event Hubs (Kafka)
- Status: ✅ PASS
- messages_received: 1
- steps: messages_validated=yes, rg_deleted=yes, rg_created=yes, aci_running=yes, deployment_complete=yes

### Issues Filed
None.

## Source: `paris-bicycle-counters`

### Fabric Notebook
- Status: ✅ PASS
- initial_attempt: ❌ FAIL (`ModuleNotFoundError: No module named 'paris_bicycle_counters'` with `-SkipEnvironment`)
- fix_applied: Redeployed without `-SkipEnvironment` using `-BuildWheelsLocally`
- notebook_job_status: Completed
- dispatch_count: 10139
- typed_tables: FR.Paris.OpenData.Velo.Counter=139, FR.Paris.OpenData.Velo.BicycleCount=10000
- freshness_minutes_ago: 1
- cleanup: notebook/eventstream/kql database/eventhouse deleted
- timestamp: 2026-06-09T08:35:36.2366361Z

### Issues Filed
None.
