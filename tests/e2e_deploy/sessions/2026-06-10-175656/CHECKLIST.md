# E2E Validation Checklist — Session 2026-06-10-175656

> Subscription: Vasters (041abda7-3870-4275-ae24-6bf4c5300523) | Fabric Workspace: ContosoRealTimeTest (ecdb6d7f-a7b3-4458-9110-f629cfc5a2cb)

## Summary

| Source | Azure EH | Azure SB | Azure EG MQTT | Fabric | Issues |
|--------|----------|----------|---------------|--------|--------|
| pegelonline | ✅ PASS | ✅ PASS | ❌ FAIL | ❌ FAIL | #907 |
| usgs-earthquakes | ✅ PASS | ❌ FAIL | ❌ FAIL | ✅ PASS | #909, #910 |
| noaa | ❌ FAIL | ✅ PASS | ❌ FAIL | ❌ FAIL | #912, #913, #914 |
| entsoe | — | — | — | — | — |
| dwd | — | — | — | — | — |
| aisstream | — | — | — | — | — |
| australia-wildfires | — | — | — | — | — |
| autobahn | — | — | — | — | — |
| aviationweather | — | — | — | — | — |
| bafu-hydro | — | — | — | — | — |
| bfs-odl | — | — | — | — | — |
| billetto | — | — | — | — | — |
| blitzortung | — | — | — | — | — |
| bluesky | — | — | — | — | — |
| bom-australia | — | — | — | — | — |
| canada-aqhi | — | — | — | — | — |
| canada-eccc-wateroffice | — | — | — | — | — |
| carbon-intensity | — | — | — | — | — |
| cbp-border-wait | — | — | — | — | — |
| cdec-reservoirs | — | — | — | — | — |
| chmi-hydro | — | — | — | — | — |
| defra-aurn | — | — | — | — | — |
| digitraffic-maritime | — | — | — | — | — |
| digitraffic-road | — | — | — | — | — |
| dmi | — | — | — | — | — |
| dwd-pollenflug | — | — | — | — | — |
| eaws-albina | — | — | — | — | — |
| elexon-bmrs | — | — | — | — | — |
| energidataservice-dk | — | — | — | — | — |
| energy-charts | — | — | — | — | — |
| entur-norway | — | — | — | — | — |
| environment-canada | — | — | — | — | — |
| epa-uv | — | — | — | — | — |
| eurdep-radiation | — | — | — | — | — |
| fdsn-seismology | — | — | — | — | — |
| fienta | — | — | — | — | — |
| fmi-finland | — | — | — | — | — |
| french-road-traffic | — | — | — | — | — |
| gbfs-bikeshare | — | — | — | — | — |
| gdacs | — | — | — | — | — |
| geosphere-austria | — | — | — | — | — |
| german-waters | — | — | — | — | — |
| gios-poland | — | — | — | — | — |
| gracedb | — | — | — | — | — |
| gtfs | — | — | — | — | — |
| hko-hong-kong | — | — | — | — | — |
| hongkong-epd | — | — | — | — | — |
| hubeau-hydrometrie | — | — | — | — | — |
| imgw-hydro | — | — | — | — | — |
| inpe-deter-brazil | — | — | — | — | — |
| irail | — | — | — | — | — |
| irceline-belgium | — | — | — | — | — |
| ireland-opw-waterlevel | — | — | — | — | — |
| jma-bosai-amedas | — | — | — | — | — |
| jma-bosai-quake | — | — | — | — | — |
| jma-bosai-volcano | — | — | — | — | — |
| jma-bosai-warning | — | — | — | — | — |
| jma-japan | — | — | — | — | — |
| king-county-marine | — | — | — | — | — |
| kmi-belgium | — | — | — | — | — |
| kystverket-ais | — | — | — | — | — |
| laqn-london | — | — | — | — | — |
| luchtmeetnet-nl | — | — | — | — | — |
| madrid-traffic | — | — | — | — | — |
| meteoalarm | — | — | — | — | — |
| mode-s | — | — | — | — | — |
| nasa-firms | — | — | — | — | — |
| ndw-road-traffic | — | — | — | — | — |
| nepal-bipad-hydrology | — | — | — | — | — |
| nextbus | — | — | — | — | — |
| nifc-usa-wildfires | — | — | — | — | — |
| nina-bbk | — | — | — | — | — |
| noaa-goes | — | — | — | — | — |
| noaa-ndbc | — | — | — | — | — |
| noaa-nws | — | — | — | — | — |
| noaa-swpc-l1 | — | — | — | — | — |
| nve-hydro | — | — | — | — | — |
| nws-alerts | — | — | — | — | — |
| nws-forecasts | — | — | — | — | — |
| paris-bicycle-counters | — | — | — | — | — |
| ptwc-tsunami | — | — | — | — | — |
| rss | — | — | — | — | — |
| rws-waterwebservices | — | — | — | — | — |
| seattle-911 | — | — | — | — | — |
| seattle-street-closures | — | — | — | — | — |
| sensor-community | — | — | — | — | — |
| singapore-nea | — | — | — | — | — |
| siri | — | — | — | — | — |
| smhi-hydro | — | — | — | — | — |
| smhi-weather | — | — | — | — | — |
| snotel | — | — | — | — | — |
| syke-hydro | — | — | — | — | — |
| tepco-denkiyoho | — | — | — | — | — |
| tfl-road-traffic | — | — | — | — | — |
| ticketmaster | — | — | — | — | — |
| tokyo-docomo-bikeshare | — | — | — | — | — |
| uba-airdata | — | — | — | — | — |
| uk-bods-siri | — | — | — | — | — |
| uk-ea-flood-monitoring | — | — | — | — | — |
| usgs-geomag | — | — | — | — | — |
| usgs-iv | — | — | — | — | — |
| usgs-nwis-wq | — | — | — | — | — |
| vatsim | — | — | — | — | — |
| wallonia-issep | — | — | — | — | — |
| waterinfo-vmm | — | — | — | — | — |
| wikimedia-eventstreams | — | — | — | — | — |
| wikimedia-osm-diffs | — | — | — | — | — |
| wsdot | — | — | — | — | — |
| xceed | — | — | — | — | — |

## Source: `pegelonline`

### Azure Event Hubs
- Status: ✅ PASS
- Details: messages received and validator passed
- Messages: 1
- Cleanup: resource group delete requested (e2e-pegelonline-eh-20260610180454)

### Azure Service Bus
- Status: ✅ PASS
- Details: messages received and validator passed
- Messages: 10
- Cleanup: resource group delete requested (e2e-pegelonline-sb-20260610180951)

### Azure Event Grid MQTT
- Status: ❌ FAIL
- Messages: 0
- Error: Conversion from JSON failed with error: Unexpected character encountered while parsing value: C. Path '', line 0, position 0.
- Cleanup: resource group delete requested (e2e-pegelonline-eg-20260610181602)

### Fabric Notebook
- Status: ❌ FAIL
- Dispatch rows: 0
- Typed tables: 
- Error: deploy-feeder-notebook.ps1 exited with 1 === pegelonline Notebook Feeder Deployment ===   Source:           pegelonline   Workspace:        ContosoRealTimeTest   Eventhouse:       pegelonline   KQL Database:     pegelonline   Notebook:         pegelonline-feed   Notebook file:    C:\git\real-time-sources\feeders\pegelonline\notebook\pegelonline-feed.ipynb   Source ref:       clemensv/real-time-sources@main   Polling interval: (from notebook) (once-mode=True)  [A] Setting up Fabric infra via deploy-fabric.ps1... === Real-Time Sources — Fabric Deployment ===   Source: pegelonline  [0/6] Validating source assets in repository...   KQL script found   Workspace: ContosoRealTimeTest (ecdb6d7f-a7b3-4458-9110-f629cfc5a2cb)   Creating Eventhouse 'pegelonline'...   Eventhouse: pegelonline (1e6182d6-2d07-4c56-be0d-473ebf77e8d4)  [1/6] Setting up KQL database 'pegelonline'...   Database already exists (ID: 231d6331-3924-4e52-9bf9-1e7ef9422853)  [2/6] Updating KQL schema...   Applying pegelonline.kql...   Applied pegelonline.kql  [3/6] Creating Event Stream 'pegelonline-ingest'...   Event Stream created (ID: 42c1ee94-5b03-4173-a4d1-66bb98f33bcf)  [4/6] Configuring Event Stream topology...   Event Stream topology configured   Waiting for Event Stream topology... pegelonline-input:Running; dispatch-kql:Creating   Waiting for Event Stream topology... pegelonline-input:Running; dispatch-kql:Creating   Waiting for Event Stream topology... pegelonline-input:Running; dispatch-kql:Creating   Waiting for Event Stream topology... pegelonline-input:Running; dispatch-kql:Creating   Event Stream source and Eventhouse destination are Running  [5/6] Retrieving Event Stream connection string...   Source ID:   310d6b1f-0deb-467a-83f6-9dcc07106219   Namespace:   esehmtcybr0lzsyc0jxqr53q.servicebus.windows.net   EventHub:    esehmtcybr0lzsyc0jxqr53q_eh   Event Stream connection string retrieved   Post-deploy hook found locally: C:\git\real-time-sources\feeders\pegelonline\fabric\post-deploy.ps1  [6/6] Running post-deploy hook (pegelonline/fabric/post-deploy.ps1)...   [pegelonline post-deploy] PEGELONLINE_FABRIC_MAP_ID not set; auto-creating Map item 'pegelonline-map' in workspace ecdb6d7f-a7b3-4458-9110-f629cfc5a2cb...   [pegelonline post-deploy] Reusing existing Map 'pegelonline-map' (id b28a3dbe-8d16-4928-b3f8-b345a45a535e)   [pegelonline post-deploy] Acquiring Fabric token via az CLI...   [pegelonline post-deploy] Acquiring Kusto token via az CLI...   [pegelonline post-deploy] Ingesting RiverSegments from C:\git\real-time-sources\feeders\pegelonline\fabric\river_geometries.kql ...     EXEC: .drop table RiverSegments ifexists ...     EXEC: .create table RiverSegments (water_shortname:string, water_longname:string, stat ...     EXEC: .ingest inline into table RiverSegments with (format='multijson') <|  {"water_sh ...   [pegelonline post-deploy] RiverSegments: 3 commands executed (drop + create + single multijson ingest).   pegelonline hydrological state: wired (default-on=True)   pegelonline navigation state: wired (default-on=False)   pegelonline 1h trend: wired (default-on=False)   pegelonline 3h trend: wired (default-on=False)   pegelonline 6h trend: wired (default-on=False)   pegelonline 24h trend: wired (default-on=False)   pegelonline data freshness: wired (default-on=False)   pegelonline station labels: wired (default-on=True) definition: 8 sources, 8 settings Traceback (most recent call last):   File "C:\git\real-time-sources\feeders\pegelonline\fabric\wire_pegelonline_map.py", line 493, in <module>     sys.exit(main())              ^^^^^^   File "C:\git\real-time-sources\feeders\pegelonline\fabric\wire_pegelonline_map.py", line 486, in main     wire(args.workspace_id, args.map_id, args.kql_db_id,   File "C:\git\real-time-sources\feeders\pegelonline\fabric\wire_pegelonline_map.py", line 459, in wire     _poll_lro(fab, r)   File "C:\git\real-time-sources\feeders\pegelonline\fabric\wire_pegelonline_map.py", line 220, in _poll_lro     raise RuntimeError(f"LRO failed: {json.dumps(status)[:400]}") RuntimeError: LRO failed: {"status": "Failed", "createdTimeUtc": "2026-06-10T16:28:59.0357226", "lastUpdatedTimeUtc": "2026-06-10T16:29:01.4531606", "percentComplete": null, "error": {"errorCode": "Unknown", "message": "unknown error", "isRetriable": false}} [33;1mWARNING: Post-deploy hook failed: wire_pegelonline_map.py exited with 1[0m [33;1mWARNING: Core deployment was successful; re-run the hook manually:[0m [33;1mWARNING:   pwsh C:\git\real-time-sources\feeders\pegelonline\fabric\post-deploy.ps1 -Context <hashtable>[0m Exception: C:\git\real-time-sources\feeders\pegelonline\fabric\post-deploy.ps1:183 Line |  183 |  … DE -ne 0) { throw "wire_pegelonline_map.py exited with $LASTEXITCODE" …      |                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~      | wire_pegelonline_map.py exited with 1 
- Cleanup: complete

## Source: `usgs-earthquakes`

### Azure Event Hubs
- Status: ✅ PASS
- Details: messages received and validator passed
- Messages: 1
- Cleanup: resource group delete requested (e2e-usgs-earthquakes-eh-20260610182916)

### Azure Service Bus
- Status: ❌ FAIL
- Messages: 0
- Error: deploy-failed: ACI container did not reach Running state within 180s
- Cleanup: resource group delete requested (e2e-usgs-earthquakes-sb-20260610184739)

### Azure Event Grid MQTT
- Status: ❌ FAIL
- Messages: 0
- Error: Conversion from JSON failed with error: Unexpected character encountered while parsing value: C. Path '', line 0, position 0.
- Cleanup: resource group delete requested (e2e-usgs-earthquakes-eg-20260610185130)

### Fabric Notebook
- Status: ✅ PASS
- Details: dispatch and typed tables populated
- Dispatch rows: 7
- Typed tables: USGS.Earthquakes.Event=7
- Job status: Completed
- Cleanup: complete

## Source: `noaa`

### Azure Event Hubs
- Status: ❌ FAIL
- Messages: 0
- Error: no-data: no Event Hub messages received
- Cleanup: resource group delete requested (e2e-noaa-eh-20260610190639)

### Azure Service Bus
- Status: ✅ PASS
- Details: messages received and validator passed
- Messages: 10
- Cleanup: resource group delete requested (e2e-noaa-sb-20260610201155)

### Azure Event Grid MQTT
- Status: ❌ FAIL
- Messages: 0
- Error: Conversion from JSON failed with error: Unexpected character encountered while parsing value: C. Path '', line 0, position 0.
- Cleanup: resource group delete requested (e2e-noaa-eg-20260610201816)

### Fabric Notebook
- Status: ❌ FAIL
- Dispatch rows: 0
- Typed tables: 
- Job status: Failed
- Error: System cancelled the Spark session due to statement execution failures
- Cleanup: complete
