-- =============================================================================
-- EU.Eurowater.Measurement normalization query
-- Fabric Event Stream SQL operator (Azure Stream Analytics compatible)
--
-- Reads telemetry/measurement events from all 8 European water services
-- and normalizes them into EU.Eurowater.Measurement records.
--
-- Some sources report multiple parameters (water_level, discharge,
-- water_temperature) in a single event. These are unpacked into separate
-- normalized rows using UNION ALL.
-- =============================================================================

-- ---- Pegelonline (Germany) ----
-- Single value per event. Parameter type determined by context (water_level).
-- Fields: station_uuid, timestamp, value, stateMnwMhw, stateNswHsw
SELECT
    CONCAT('de-', data.station_uuid)          AS station_id,
    'de'                                       AS country_code,
    data.[timestamp]                           AS [timestamp],
    'water_level'                              AS parameter,
    data.value                                 AS value,
    'cm'                                       AS unit,
    data.stateMnwMhw                           AS quality,
    'pegelonline'                              AS source_system,
    'EU.Eurowater.Measurement'                 AS [__ce_type]
INTO MeasurementOutput
FROM EventInput
WHERE type = 'de.wsv.pegelonline.CurrentMeasurement'

UNION ALL

-- ---- CHMI Hydro (Czech Republic) ----
-- Multi-parameter: water_level, discharge, water_temperature in one event.
-- Water level
SELECT
    CONCAT('cz-', data.station_id)            AS station_id,
    'cz'                                       AS country_code,
    data.water_level_timestamp                 AS [timestamp],
    'water_level'                              AS parameter,
    data.water_level                           AS value,
    'cm'                                       AS unit,
    NULL                                       AS quality,
    'chmi-hydro'                               AS source_system,
    'EU.Eurowater.Measurement'                 AS [__ce_type]
FROM EventInput
WHERE type = 'CZ.Gov.CHMI.Hydro.WaterLevelObservation'
    AND data.water_level IS NOT NULL

UNION ALL

-- CHMI discharge
SELECT
    CONCAT('cz-', data.station_id)            AS station_id,
    'cz'                                       AS country_code,
    data.discharge_timestamp                   AS [timestamp],
    'discharge'                                AS parameter,
    data.discharge                             AS value,
    'm3/s'                                     AS unit,
    NULL                                       AS quality,
    'chmi-hydro'                               AS source_system,
    'EU.Eurowater.Measurement'                 AS [__ce_type]
FROM EventInput
WHERE type = 'CZ.Gov.CHMI.Hydro.WaterLevelObservation'
    AND data.discharge IS NOT NULL

UNION ALL

-- CHMI water temperature
SELECT
    CONCAT('cz-', data.station_id)            AS station_id,
    'cz'                                       AS country_code,
    data.water_temperature_timestamp           AS [timestamp],
    'water_temperature'                        AS parameter,
    data.water_temperature                     AS value,
    'C'                                        AS unit,
    NULL                                       AS quality,
    'chmi-hydro'                               AS source_system,
    'EU.Eurowater.Measurement'                 AS [__ce_type]
FROM EventInput
WHERE type = 'CZ.Gov.CHMI.Hydro.WaterLevelObservation'
    AND data.water_temperature IS NOT NULL

UNION ALL

-- ---- IMGW Hydro (Poland) ----
-- Water level
SELECT
    CONCAT('pl-', data.station_id)            AS station_id,
    'pl'                                       AS country_code,
    data.water_level_timestamp                 AS [timestamp],
    'water_level'                              AS parameter,
    data.water_level                           AS value,
    'cm'                                       AS unit,
    NULL                                       AS quality,
    'imgw-hydro'                               AS source_system,
    'EU.Eurowater.Measurement'                 AS [__ce_type]
FROM EventInput
WHERE type = 'PL.Gov.IMGW.Hydro.WaterLevelObservation'
    AND data.water_level IS NOT NULL

UNION ALL

-- IMGW discharge
SELECT
    CONCAT('pl-', data.station_id)            AS station_id,
    'pl'                                       AS country_code,
    data.discharge_timestamp                   AS [timestamp],
    'discharge'                                AS parameter,
    data.discharge                             AS value,
    'm3/s'                                     AS unit,
    NULL                                       AS quality,
    'imgw-hydro'                               AS source_system,
    'EU.Eurowater.Measurement'                 AS [__ce_type]
FROM EventInput
WHERE type = 'PL.Gov.IMGW.Hydro.WaterLevelObservation'
    AND data.discharge IS NOT NULL

UNION ALL

-- IMGW water temperature
SELECT
    CONCAT('pl-', data.station_id)            AS station_id,
    'pl'                                       AS country_code,
    data.water_temperature_timestamp           AS [timestamp],
    'water_temperature'                        AS parameter,
    data.water_temperature                     AS value,
    'C'                                        AS unit,
    NULL                                       AS quality,
    'imgw-hydro'                               AS source_system,
    'EU.Eurowater.Measurement'                 AS [__ce_type]
FROM EventInput
WHERE type = 'PL.Gov.IMGW.Hydro.WaterLevelObservation'
    AND data.water_temperature IS NOT NULL

UNION ALL

-- ---- SMHI Hydro (Sweden) ----
-- Single parameter: discharge only
SELECT
    CONCAT('se-', data.station_id)            AS station_id,
    'se'                                       AS country_code,
    data.[timestamp]                           AS [timestamp],
    'discharge'                                AS parameter,
    data.discharge                             AS value,
    'm3/s'                                     AS unit,
    data.quality                               AS quality,
    'smhi-hydro'                               AS source_system,
    'EU.Eurowater.Measurement'                 AS [__ce_type]
FROM EventInput
WHERE type = 'SE.Gov.SMHI.Hydro.DischargeObservation'

UNION ALL

-- ---- Hub'Eau Hydrometrie (France) ----
-- grandeur_hydro = 'H' -> water_level (mm -> cm: /10), 'Q' -> discharge (L/s -> m3/s: /1000)
-- Water level (H)
SELECT
    CONCAT('fr-', data.code_station)          AS station_id,
    'fr'                                       AS country_code,
    data.date_obs                              AS [timestamp],
    'water_level'                              AS parameter,
    data.resultat_obs / 10.0                   AS value,
    'cm'                                       AS unit,
    data.libelle_qualification_obs             AS quality,
    'hubeau-hydrometrie'                       AS source_system,
    'EU.Eurowater.Measurement'                 AS [__ce_type]
FROM EventInput
WHERE type = 'FR.Gov.Eaufrance.HubEau.Hydrometrie.Observation'
    AND data.grandeur_hydro = 'H'

UNION ALL

-- Hub'Eau discharge (Q)
SELECT
    CONCAT('fr-', data.code_station)          AS station_id,
    'fr'                                       AS country_code,
    data.date_obs                              AS [timestamp],
    'discharge'                                AS parameter,
    data.resultat_obs / 1000.0                 AS value,
    'm3/s'                                     AS unit,
    data.libelle_qualification_obs             AS quality,
    'hubeau-hydrometrie'                       AS source_system,
    'EU.Eurowater.Measurement'                 AS [__ce_type]
FROM EventInput
WHERE type = 'FR.Gov.Eaufrance.HubEau.Hydrometrie.Observation'
    AND data.grandeur_hydro = 'Q'

UNION ALL

-- ---- UK EA Flood Monitoring (England) ----
-- Single value per Reading event, parameter type from measure URI
SELECT
    CONCAT('gb-', data.station_reference)     AS station_id,
    'gb'                                       AS country_code,
    data.date_time                             AS [timestamp],
    'water_level'                              AS parameter,
    data.value                                 AS value,
    'm'                                        AS unit,
    NULL                                       AS quality,
    'uk-ea-flood-monitoring'                   AS source_system,
    'EU.Eurowater.Measurement'                 AS [__ce_type]
FROM EventInput
WHERE type = 'UK.Gov.Environment.EA.FloodMonitoring.Reading'

UNION ALL

-- ---- RWS Waterwebservices (Netherlands) ----
-- Water level in cm relative to NAP
SELECT
    CONCAT('nl-', data.location_code)         AS station_id,
    'nl'                                       AS country_code,
    data.[timestamp]                           AS [timestamp],
    'water_level'                              AS parameter,
    data.value                                 AS value,
    'cm'                                       AS unit,
    data.quality_code                          AS quality,
    'rws-waterwebservices'                     AS source_system,
    'EU.Eurowater.Measurement'                 AS [__ce_type]
FROM EventInput
WHERE type = 'NL.RWS.Waterwebservices.WaterLevelObservation'

UNION ALL

-- ---- Waterinfo VMM (Belgium/Flanders) ----
-- parameter_name: H = water_level, Q = discharge
-- Water level
SELECT
    CONCAT('be-', data.station_no)            AS station_id,
    'be'                                       AS country_code,
    data.[timestamp]                           AS [timestamp],
    CASE
        WHEN data.parameter_name = 'Q' THEN 'discharge'
        ELSE 'water_level'
    END                                        AS parameter,
    data.value                                 AS value,
    CASE
        WHEN data.parameter_name = 'Q' THEN 'm3/s'
        ELSE data.unit_name
    END                                        AS unit,
    NULL                                       AS quality,
    'waterinfo-vmm'                            AS source_system,
    'EU.Eurowater.Measurement'                 AS [__ce_type]
FROM EventInput
WHERE type = 'BE.Vlaanderen.Waterinfo.VMM.WaterLevelReading';
