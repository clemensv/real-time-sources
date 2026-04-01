-- =============================================================================
-- EU.Eurowater.Station normalization query
-- Fabric Event Stream SQL operator (Azure Stream Analytics compatible)
--
-- Reads station reference events from all 12 European water services
-- and normalizes them into a single EU.Eurowater.Station schema.
-- =============================================================================

-- Pegelonline (Germany) - Avro payload, fields: uuid, number, shortname, longname,
-- km, agency, longitude, latitude, water.shortname, water.longname
-- CloudEvents type: de.wsv.pegelonline.Station

-- German Waters (Germany state gauges) - JSON payload, fields: station_id,
-- station_name, water_body, state, provider, latitude, longitude
-- CloudEvents type: DE.Waters.Hydrology.Station

-- CHMI Hydro (Czech Republic) - JSON payload, fields: station_id, dbc,
-- station_name, stream_name, latitude, longitude, flood_level_*
-- CloudEvents type: CZ.Gov.CHMI.Hydro.Station

-- IMGW Hydro (Poland) - JSON payload, fields: id_stacji, stacja, rzeka,
-- wojewodztwo, longitude, latitude
-- CloudEvents type: PL.Gov.IMGW.Hydro.Station

-- SMHI Hydro (Sweden) - JSON payload, fields: station_id, name, owner,
-- catchment_name, latitude, longitude
-- CloudEvents type: SE.Gov.SMHI.Hydro.Station

-- Hub'Eau Hydrometrie (France) - JSON payload, fields: code_station,
-- libelle_station, libelle_cours_eau, longitude_station, latitude_station
-- CloudEvents type: FR.Gov.Eaufrance.HubEau.Hydrometrie.Station

-- UK EA Flood Monitoring (England) - JSON payload, fields: station_reference,
-- label, river_name, lat, long
-- CloudEvents type: UK.Gov.Environment.EA.FloodMonitoring.Station

-- RWS Waterwebservices (Netherlands) - JSON payload, fields: code, name,
-- latitude, longitude
-- CloudEvents type: NL.RWS.Waterwebservices.Station

-- Waterinfo VMM (Belgium) - JSON payload, fields: station_no, station_name,
-- station_latitude, station_longitude, river_name
-- CloudEvents type: BE.Vlaanderen.Waterinfo.VMM.Station

-- NVE Hydro (Norway) - JSON payload, fields: station_id, station_name,
-- river_name, latitude, longitude
-- CloudEvents type: NO.NVE.Hydrology.Station

-- SYKE Hydro (Finland) - JSON payload, fields: station_id, name,
-- river_name, latitude, longitude
-- CloudEvents type: FI.SYKE.Hydrology.Station

-- BAFU Hydro (Switzerland) - JSON payload, fields: station_id, name,
-- water_body_name, latitude, longitude
-- CloudEvents type: CH.BAFU.Hydrology.Station

SELECT
    CASE
        WHEN type = 'de.wsv.pegelonline.Station'
            THEN CONCAT('de-', data.uuid)
        WHEN type = 'CZ.Gov.CHMI.Hydro.Station'
            THEN CONCAT('cz-', data.station_id)
        WHEN type = 'PL.Gov.IMGW.Hydro.Station'
            THEN CONCAT('pl-', data.id_stacji)
        WHEN type = 'SE.Gov.SMHI.Hydro.Station'
            THEN CONCAT('se-', data.station_id)
        WHEN type = 'FR.Gov.Eaufrance.HubEau.Hydrometrie.Station'
            THEN CONCAT('fr-', data.code_station)
        WHEN type = 'UK.Gov.Environment.EA.FloodMonitoring.Station'
            THEN CONCAT('gb-', data.station_reference)
        WHEN type = 'NL.RWS.Waterwebservices.Station'
            THEN CONCAT('nl-', data.code)
        WHEN type = 'BE.Vlaanderen.Waterinfo.VMM.Station'
            THEN CONCAT('be-', data.station_no)
        WHEN type = 'NO.NVE.Hydrology.Station'
            THEN CONCAT('no-', data.station_id)
        WHEN type = 'FI.SYKE.Hydrology.Station'
            THEN CONCAT('fi-', data.station_id)
        WHEN type = 'CH.BAFU.Hydrology.Station'
            THEN CONCAT('ch-', data.station_id)
        WHEN type = 'DE.Waters.Hydrology.Station'
            THEN CONCAT('de-', data.station_id)
        ELSE NULL
    END AS station_id,

    CASE
        WHEN type = 'de.wsv.pegelonline.Station' THEN 'de'
        WHEN type = 'CZ.Gov.CHMI.Hydro.Station' THEN 'cz'
        WHEN type = 'PL.Gov.IMGW.Hydro.Station' THEN 'pl'
        WHEN type = 'SE.Gov.SMHI.Hydro.Station' THEN 'se'
        WHEN type = 'FR.Gov.Eaufrance.HubEau.Hydrometrie.Station' THEN 'fr'
        WHEN type = 'UK.Gov.Environment.EA.FloodMonitoring.Station' THEN 'gb'
        WHEN type = 'NL.RWS.Waterwebservices.Station' THEN 'nl'
        WHEN type = 'BE.Vlaanderen.Waterinfo.VMM.Station' THEN 'be'
        WHEN type = 'NO.NVE.Hydrology.Station' THEN 'no'
        WHEN type = 'FI.SYKE.Hydrology.Station' THEN 'fi'
        WHEN type = 'CH.BAFU.Hydrology.Station' THEN 'ch'
        WHEN type = 'DE.Waters.Hydrology.Station' THEN 'de'
        ELSE NULL
    END AS country_code,

    CASE
        WHEN type = 'de.wsv.pegelonline.Station' THEN data.number
        WHEN type = 'CZ.Gov.CHMI.Hydro.Station' THEN data.station_id
        WHEN type = 'PL.Gov.IMGW.Hydro.Station' THEN data.id_stacji
        WHEN type = 'SE.Gov.SMHI.Hydro.Station' THEN data.station_id
        WHEN type = 'FR.Gov.Eaufrance.HubEau.Hydrometrie.Station' THEN data.code_station
        WHEN type = 'UK.Gov.Environment.EA.FloodMonitoring.Station' THEN data.station_reference
        WHEN type = 'NL.RWS.Waterwebservices.Station' THEN data.code
        WHEN type = 'BE.Vlaanderen.Waterinfo.VMM.Station' THEN data.station_no
        WHEN type = 'NO.NVE.Hydrology.Station' THEN data.station_id
        WHEN type = 'FI.SYKE.Hydrology.Station' THEN data.station_id
        WHEN type = 'CH.BAFU.Hydrology.Station' THEN data.station_id
        WHEN type = 'DE.Waters.Hydrology.Station' THEN data.station_id
        ELSE NULL
    END AS source_station_id,

    CASE
        WHEN type = 'de.wsv.pegelonline.Station' THEN data.longname
        WHEN type = 'CZ.Gov.CHMI.Hydro.Station' THEN data.station_name
        WHEN type = 'PL.Gov.IMGW.Hydro.Station' THEN data.stacja
        WHEN type = 'SE.Gov.SMHI.Hydro.Station' THEN data.name
        WHEN type = 'FR.Gov.Eaufrance.HubEau.Hydrometrie.Station' THEN data.libelle_station
        WHEN type = 'UK.Gov.Environment.EA.FloodMonitoring.Station' THEN data.label
        WHEN type = 'NL.RWS.Waterwebservices.Station' THEN data.name
        WHEN type = 'BE.Vlaanderen.Waterinfo.VMM.Station' THEN data.station_name
        WHEN type = 'NO.NVE.Hydrology.Station' THEN data.station_name
        WHEN type = 'FI.SYKE.Hydrology.Station' THEN data.name
        WHEN type = 'CH.BAFU.Hydrology.Station' THEN data.name
        WHEN type = 'DE.Waters.Hydrology.Station' THEN data.station_name
        ELSE NULL
    END AS station_name,

    CASE
        WHEN type = 'de.wsv.pegelonline.Station' THEN data.water.longname
        WHEN type = 'CZ.Gov.CHMI.Hydro.Station' THEN data.stream_name
        WHEN type = 'PL.Gov.IMGW.Hydro.Station' THEN data.rzeka
        WHEN type = 'SE.Gov.SMHI.Hydro.Station' THEN data.catchment_name
        WHEN type = 'FR.Gov.Eaufrance.HubEau.Hydrometrie.Station' THEN data.libelle_cours_eau
        WHEN type = 'UK.Gov.Environment.EA.FloodMonitoring.Station' THEN data.river_name
        WHEN type = 'NL.RWS.Waterwebservices.Station' THEN NULL
        WHEN type = 'BE.Vlaanderen.Waterinfo.VMM.Station' THEN data.river_name
        WHEN type = 'NO.NVE.Hydrology.Station' THEN data.river_name
        WHEN type = 'FI.SYKE.Hydrology.Station' THEN data.river_name
        WHEN type = 'CH.BAFU.Hydrology.Station' THEN data.water_body_name
        WHEN type = 'DE.Waters.Hydrology.Station' THEN data.water_body
        ELSE NULL
    END AS river_name,

    CASE
        WHEN type = 'de.wsv.pegelonline.Station' THEN data.latitude
        WHEN type = 'FR.Gov.Eaufrance.HubEau.Hydrometrie.Station' THEN
            CASE WHEN data.latitude_station < 20 AND data.longitude_station > 35
                 THEN data.longitude_station
                 ELSE data.latitude_station
            END
        WHEN type = 'UK.Gov.Environment.EA.FloodMonitoring.Station' THEN data.lat
        WHEN type = 'BE.Vlaanderen.Waterinfo.VMM.Station' THEN data.station_latitude
        ELSE data.latitude
    END AS latitude,

    CASE
        WHEN type = 'de.wsv.pegelonline.Station' THEN data.longitude
        WHEN type = 'FR.Gov.Eaufrance.HubEau.Hydrometrie.Station' THEN
            CASE WHEN data.latitude_station < 20 AND data.longitude_station > 35
                 THEN data.latitude_station
                 ELSE data.longitude_station
            END
        WHEN type = 'UK.Gov.Environment.EA.FloodMonitoring.Station' THEN data.[long]
        WHEN type = 'BE.Vlaanderen.Waterinfo.VMM.Station' THEN data.station_longitude
        ELSE data.longitude
    END AS longitude,

    CASE
        WHEN type = 'de.wsv.pegelonline.Station' THEN 'pegelonline'
        WHEN type = 'CZ.Gov.CHMI.Hydro.Station' THEN 'chmi-hydro'
        WHEN type = 'PL.Gov.IMGW.Hydro.Station' THEN 'imgw-hydro'
        WHEN type = 'SE.Gov.SMHI.Hydro.Station' THEN 'smhi-hydro'
        WHEN type = 'FR.Gov.Eaufrance.HubEau.Hydrometrie.Station' THEN 'hubeau-hydrometrie'
        WHEN type = 'UK.Gov.Environment.EA.FloodMonitoring.Station' THEN 'uk-ea-flood-monitoring'
        WHEN type = 'NL.RWS.Waterwebservices.Station' THEN 'rws-waterwebservices'
        WHEN type = 'BE.Vlaanderen.Waterinfo.VMM.Station' THEN 'waterinfo-vmm'
        WHEN type = 'NO.NVE.Hydrology.Station' THEN 'nve-hydro'
        WHEN type = 'FI.SYKE.Hydrology.Station' THEN 'syke-hydro'
        WHEN type = 'CH.BAFU.Hydrology.Station' THEN 'bafu-hydro'
        WHEN type = 'DE.Waters.Hydrology.Station' THEN 'german-waters'
        ELSE NULL
    END AS source_system,

    source AS source_url,

    System.Timestamp() AS ingestion_time,

    'EU.Eurowater.Station' AS [__ce_type]

INTO StationOutput
FROM EventInput
WHERE type IN (
    'de.wsv.pegelonline.Station',
    'CZ.Gov.CHMI.Hydro.Station',
    'PL.Gov.IMGW.Hydro.Station',
    'SE.Gov.SMHI.Hydro.Station',
    'FR.Gov.Eaufrance.HubEau.Hydrometrie.Station',
    'UK.Gov.Environment.EA.FloodMonitoring.Station',
    'NL.RWS.Waterwebservices.Station',
    'BE.Vlaanderen.Waterinfo.VMM.Station',
    'NO.NVE.Hydrology.Station',
    'FI.SYKE.Hydrology.Station',
    'CH.BAFU.Hydrology.Station',
    'DE.Waters.Hydrology.Station'
);
