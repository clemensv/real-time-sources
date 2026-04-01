-- =============================================================================
-- EU.Eurowater.Measurement normalization query
-- Fabric Event Stream SQL operator (Azure Stream Analytics compatible)
--
-- Reads telemetry/measurement events from all 12 European water services
-- and normalizes them into EU.Eurowater.Measurement records.
--
-- Structured as three UNION ALL branches (water_level, discharge,
-- water_temperature) with CASE expressions for source-specific mappings.
-- =============================================================================

-- ===================== WATER LEVEL =====================
-- Sources: Pegelonline, CHMI, IMGW, Hub'Eau (H), UK EA, RWS, Waterinfo VMM,
--          NVE, SYKE, BAFU, German Waters
SELECT
    CASE
        WHEN type = 'de.wsv.pegelonline.CurrentMeasurement'
            THEN CONCAT('de-', data.station_uuid)
        WHEN type = 'CZ.Gov.CHMI.Hydro.WaterLevelObservation'
            THEN CONCAT('cz-', data.station_id)
        WHEN type = 'PL.Gov.IMGW.Hydro.WaterLevelObservation'
            THEN CONCAT('pl-', data.station_id)
        WHEN type = 'FR.Gov.Eaufrance.HubEau.Hydrometrie.Observation'
            THEN CONCAT('fr-', data.code_station)
        WHEN type = 'UK.Gov.Environment.EA.FloodMonitoring.Reading'
            THEN CONCAT('gb-', data.station_reference)
        WHEN type = 'NL.RWS.Waterwebservices.WaterLevelObservation'
            THEN CONCAT('nl-', data.location_code)
        WHEN type = 'BE.Vlaanderen.Waterinfo.VMM.WaterLevelReading'
            THEN CONCAT('be-', data.station_no)
        WHEN type = 'NO.NVE.Hydrology.WaterLevelObservation'
            THEN CONCAT('no-', data.station_id)
        WHEN type = 'FI.SYKE.Hydrology.WaterLevelObservation'
            THEN CONCAT('fi-', data.station_id)
        WHEN type = 'CH.BAFU.Hydrology.WaterLevelObservation'
            THEN CONCAT('ch-', data.station_id)
        WHEN type = 'DE.Waters.Hydrology.WaterLevelObservation'
            THEN CONCAT('de-', data.station_id)
        ELSE NULL
    END AS station_id,

    CASE
        WHEN type = 'de.wsv.pegelonline.CurrentMeasurement' THEN 'de'
        WHEN type = 'CZ.Gov.CHMI.Hydro.WaterLevelObservation' THEN 'cz'
        WHEN type = 'PL.Gov.IMGW.Hydro.WaterLevelObservation' THEN 'pl'
        WHEN type = 'FR.Gov.Eaufrance.HubEau.Hydrometrie.Observation' THEN 'fr'
        WHEN type = 'UK.Gov.Environment.EA.FloodMonitoring.Reading' THEN 'gb'
        WHEN type = 'NL.RWS.Waterwebservices.WaterLevelObservation' THEN 'nl'
        WHEN type = 'BE.Vlaanderen.Waterinfo.VMM.WaterLevelReading' THEN 'be'
        WHEN type = 'NO.NVE.Hydrology.WaterLevelObservation' THEN 'no'
        WHEN type = 'FI.SYKE.Hydrology.WaterLevelObservation' THEN 'fi'
        WHEN type = 'CH.BAFU.Hydrology.WaterLevelObservation' THEN 'ch'
        WHEN type = 'DE.Waters.Hydrology.WaterLevelObservation' THEN 'de'
        ELSE NULL
    END AS country_code,

    CASE
        WHEN type = 'de.wsv.pegelonline.CurrentMeasurement'
            THEN data.[timestamp]
        WHEN type = 'CZ.Gov.CHMI.Hydro.WaterLevelObservation'
            THEN data.water_level_timestamp
        WHEN type = 'PL.Gov.IMGW.Hydro.WaterLevelObservation'
            THEN data.water_level_timestamp
        WHEN type = 'FR.Gov.Eaufrance.HubEau.Hydrometrie.Observation'
            THEN data.date_obs
        WHEN type = 'UK.Gov.Environment.EA.FloodMonitoring.Reading'
            THEN data.date_time
        WHEN type = 'NL.RWS.Waterwebservices.WaterLevelObservation'
            THEN data.[timestamp]
        WHEN type = 'BE.Vlaanderen.Waterinfo.VMM.WaterLevelReading'
            THEN data.[timestamp]
        WHEN type = 'NO.NVE.Hydrology.WaterLevelObservation'
            THEN data.water_level_timestamp
        WHEN type = 'FI.SYKE.Hydrology.WaterLevelObservation'
            THEN data.water_level_timestamp
        WHEN type = 'CH.BAFU.Hydrology.WaterLevelObservation'
            THEN data.water_level_timestamp
        WHEN type = 'DE.Waters.Hydrology.WaterLevelObservation'
            THEN data.water_level_timestamp
        ELSE NULL
    END AS [timestamp],

    'water_level' AS parameter,

    CASE
        WHEN type = 'de.wsv.pegelonline.CurrentMeasurement'
            THEN data.value
        WHEN type = 'CZ.Gov.CHMI.Hydro.WaterLevelObservation'
            THEN data.water_level
        WHEN type = 'PL.Gov.IMGW.Hydro.WaterLevelObservation'
            THEN data.water_level
        WHEN type = 'FR.Gov.Eaufrance.HubEau.Hydrometrie.Observation'
            THEN data.resultat_obs / 10.0
        WHEN type = 'UK.Gov.Environment.EA.FloodMonitoring.Reading'
            THEN data.value
        WHEN type = 'NL.RWS.Waterwebservices.WaterLevelObservation'
            THEN data.value
        WHEN type = 'BE.Vlaanderen.Waterinfo.VMM.WaterLevelReading'
            THEN data.value
        WHEN type = 'NO.NVE.Hydrology.WaterLevelObservation'
            THEN data.water_level
        WHEN type = 'FI.SYKE.Hydrology.WaterLevelObservation'
            THEN data.water_level
        WHEN type = 'CH.BAFU.Hydrology.WaterLevelObservation'
            THEN data.water_level
        WHEN type = 'DE.Waters.Hydrology.WaterLevelObservation'
            THEN data.water_level
        ELSE NULL
    END AS value,

    CASE
        WHEN type = 'de.wsv.pegelonline.CurrentMeasurement' THEN 'cm'
        WHEN type = 'CZ.Gov.CHMI.Hydro.WaterLevelObservation' THEN 'cm'
        WHEN type = 'PL.Gov.IMGW.Hydro.WaterLevelObservation' THEN 'cm'
        WHEN type = 'FR.Gov.Eaufrance.HubEau.Hydrometrie.Observation' THEN 'cm'
        WHEN type = 'UK.Gov.Environment.EA.FloodMonitoring.Reading' THEN 'm'
        WHEN type = 'NL.RWS.Waterwebservices.WaterLevelObservation' THEN 'cm'
        WHEN type = 'BE.Vlaanderen.Waterinfo.VMM.WaterLevelReading'
            THEN data.unit_name
        WHEN type = 'NO.NVE.Hydrology.WaterLevelObservation'
            THEN data.water_level_unit
        WHEN type = 'FI.SYKE.Hydrology.WaterLevelObservation'
            THEN data.water_level_unit
        WHEN type = 'CH.BAFU.Hydrology.WaterLevelObservation'
            THEN data.water_level_unit
        WHEN type = 'DE.Waters.Hydrology.WaterLevelObservation'
            THEN data.water_level_unit
        ELSE NULL
    END AS unit,

    CASE
        WHEN type = 'de.wsv.pegelonline.CurrentMeasurement'
            THEN data.stateMnwMhw
        WHEN type = 'FR.Gov.Eaufrance.HubEau.Hydrometrie.Observation'
            THEN data.libelle_qualification_obs
        WHEN type = 'NL.RWS.Waterwebservices.WaterLevelObservation'
            THEN data.quality_code
        ELSE NULL
    END AS quality,

    CASE
        WHEN type = 'de.wsv.pegelonline.CurrentMeasurement' THEN 'pegelonline'
        WHEN type = 'CZ.Gov.CHMI.Hydro.WaterLevelObservation' THEN 'chmi-hydro'
        WHEN type = 'PL.Gov.IMGW.Hydro.WaterLevelObservation' THEN 'imgw-hydro'
        WHEN type = 'FR.Gov.Eaufrance.HubEau.Hydrometrie.Observation' THEN 'hubeau-hydrometrie'
        WHEN type = 'UK.Gov.Environment.EA.FloodMonitoring.Reading' THEN 'uk-ea-flood-monitoring'
        WHEN type = 'NL.RWS.Waterwebservices.WaterLevelObservation' THEN 'rws-waterwebservices'
        WHEN type = 'BE.Vlaanderen.Waterinfo.VMM.WaterLevelReading' THEN 'waterinfo-vmm'
        WHEN type = 'NO.NVE.Hydrology.WaterLevelObservation' THEN 'nve-hydro'
        WHEN type = 'FI.SYKE.Hydrology.WaterLevelObservation' THEN 'syke-hydro'
        WHEN type = 'CH.BAFU.Hydrology.WaterLevelObservation' THEN 'bafu-hydro'
        WHEN type = 'DE.Waters.Hydrology.WaterLevelObservation' THEN 'german-waters'
        ELSE NULL
    END AS source_system,

    System.Timestamp() AS ingestion_time,

    'EU.Eurowater.Measurement' AS [__ce_type]

INTO MeasurementOutput
FROM EventInput
WHERE (
    type = 'de.wsv.pegelonline.CurrentMeasurement'
    OR type = 'UK.Gov.Environment.EA.FloodMonitoring.Reading'
    OR type = 'NL.RWS.Waterwebservices.WaterLevelObservation'
    OR (type = 'CZ.Gov.CHMI.Hydro.WaterLevelObservation' AND data.water_level IS NOT NULL)
    OR (type = 'PL.Gov.IMGW.Hydro.WaterLevelObservation' AND data.water_level IS NOT NULL)
    OR (type = 'FR.Gov.Eaufrance.HubEau.Hydrometrie.Observation' AND data.grandeur_hydro = 'H')
    OR (type = 'BE.Vlaanderen.Waterinfo.VMM.WaterLevelReading' AND (data.parameter_name IS NULL OR data.parameter_name <> 'Q'))
    OR (type = 'NO.NVE.Hydrology.WaterLevelObservation' AND data.water_level IS NOT NULL)
    OR (type = 'FI.SYKE.Hydrology.WaterLevelObservation' AND data.water_level IS NOT NULL)
    OR (type = 'CH.BAFU.Hydrology.WaterLevelObservation' AND data.water_level IS NOT NULL)
    OR (type = 'DE.Waters.Hydrology.WaterLevelObservation' AND data.water_level IS NOT NULL)
)

UNION ALL

-- ===================== DISCHARGE =====================
-- Sources: CHMI, IMGW, SMHI, Hub'Eau (Q), Waterinfo VMM (Q), NVE, SYKE, BAFU, German Waters
SELECT
    CASE
        WHEN type = 'CZ.Gov.CHMI.Hydro.WaterLevelObservation'
            THEN CONCAT('cz-', data.station_id)
        WHEN type = 'PL.Gov.IMGW.Hydro.WaterLevelObservation'
            THEN CONCAT('pl-', data.station_id)
        WHEN type = 'SE.Gov.SMHI.Hydro.DischargeObservation'
            THEN CONCAT('se-', data.station_id)
        WHEN type = 'FR.Gov.Eaufrance.HubEau.Hydrometrie.Observation'
            THEN CONCAT('fr-', data.code_station)
        WHEN type = 'BE.Vlaanderen.Waterinfo.VMM.WaterLevelReading'
            THEN CONCAT('be-', data.station_no)
        WHEN type = 'NO.NVE.Hydrology.WaterLevelObservation'
            THEN CONCAT('no-', data.station_id)
        WHEN type = 'FI.SYKE.Hydrology.WaterLevelObservation'
            THEN CONCAT('fi-', data.station_id)
        WHEN type = 'CH.BAFU.Hydrology.WaterLevelObservation'
            THEN CONCAT('ch-', data.station_id)
        WHEN type = 'DE.Waters.Hydrology.WaterLevelObservation'
            THEN CONCAT('de-', data.station_id)
        ELSE NULL
    END AS station_id,

    CASE
        WHEN type = 'CZ.Gov.CHMI.Hydro.WaterLevelObservation' THEN 'cz'
        WHEN type = 'PL.Gov.IMGW.Hydro.WaterLevelObservation' THEN 'pl'
        WHEN type = 'SE.Gov.SMHI.Hydro.DischargeObservation' THEN 'se'
        WHEN type = 'FR.Gov.Eaufrance.HubEau.Hydrometrie.Observation' THEN 'fr'
        WHEN type = 'BE.Vlaanderen.Waterinfo.VMM.WaterLevelReading' THEN 'be'
        WHEN type = 'NO.NVE.Hydrology.WaterLevelObservation' THEN 'no'
        WHEN type = 'FI.SYKE.Hydrology.WaterLevelObservation' THEN 'fi'
        WHEN type = 'CH.BAFU.Hydrology.WaterLevelObservation' THEN 'ch'
        WHEN type = 'DE.Waters.Hydrology.WaterLevelObservation' THEN 'de'
        ELSE NULL
    END AS country_code,

    CASE
        WHEN type = 'CZ.Gov.CHMI.Hydro.WaterLevelObservation'
            THEN data.discharge_timestamp
        WHEN type = 'PL.Gov.IMGW.Hydro.WaterLevelObservation'
            THEN data.discharge_timestamp
        WHEN type = 'SE.Gov.SMHI.Hydro.DischargeObservation'
            THEN data.[timestamp]
        WHEN type = 'FR.Gov.Eaufrance.HubEau.Hydrometrie.Observation'
            THEN data.date_obs
        WHEN type = 'BE.Vlaanderen.Waterinfo.VMM.WaterLevelReading'
            THEN data.[timestamp]
        WHEN type = 'NO.NVE.Hydrology.WaterLevelObservation'
            THEN data.discharge_timestamp
        WHEN type = 'FI.SYKE.Hydrology.WaterLevelObservation'
            THEN data.discharge_timestamp
        WHEN type = 'CH.BAFU.Hydrology.WaterLevelObservation'
            THEN data.discharge_timestamp
        WHEN type = 'DE.Waters.Hydrology.WaterLevelObservation'
            THEN data.discharge_timestamp
        ELSE NULL
    END AS [timestamp],

    'discharge' AS parameter,

    CASE
        WHEN type = 'CZ.Gov.CHMI.Hydro.WaterLevelObservation'
            THEN data.discharge
        WHEN type = 'PL.Gov.IMGW.Hydro.WaterLevelObservation'
            THEN data.discharge
        WHEN type = 'SE.Gov.SMHI.Hydro.DischargeObservation'
            THEN data.discharge
        WHEN type = 'FR.Gov.Eaufrance.HubEau.Hydrometrie.Observation'
            THEN data.resultat_obs / 1000.0
        WHEN type = 'BE.Vlaanderen.Waterinfo.VMM.WaterLevelReading'
            THEN data.value
        WHEN type = 'NO.NVE.Hydrology.WaterLevelObservation'
            THEN data.discharge
        WHEN type = 'FI.SYKE.Hydrology.WaterLevelObservation'
            THEN data.discharge
        WHEN type = 'CH.BAFU.Hydrology.WaterLevelObservation'
            THEN data.discharge
        WHEN type = 'DE.Waters.Hydrology.WaterLevelObservation'
            THEN data.discharge
        ELSE NULL
    END AS value,

    CASE
        WHEN type = 'NO.NVE.Hydrology.WaterLevelObservation'
            THEN data.discharge_unit
        WHEN type = 'FI.SYKE.Hydrology.WaterLevelObservation'
            THEN data.discharge_unit
        WHEN type = 'CH.BAFU.Hydrology.WaterLevelObservation'
            THEN data.discharge_unit
        WHEN type = 'DE.Waters.Hydrology.WaterLevelObservation'
            THEN data.discharge_unit
        ELSE 'm3/s'
    END AS unit,

    CASE
        WHEN type = 'SE.Gov.SMHI.Hydro.DischargeObservation'
            THEN data.quality
        WHEN type = 'FR.Gov.Eaufrance.HubEau.Hydrometrie.Observation'
            THEN data.libelle_qualification_obs
        ELSE NULL
    END AS quality,

    CASE
        WHEN type = 'CZ.Gov.CHMI.Hydro.WaterLevelObservation' THEN 'chmi-hydro'
        WHEN type = 'PL.Gov.IMGW.Hydro.WaterLevelObservation' THEN 'imgw-hydro'
        WHEN type = 'SE.Gov.SMHI.Hydro.DischargeObservation' THEN 'smhi-hydro'
        WHEN type = 'FR.Gov.Eaufrance.HubEau.Hydrometrie.Observation' THEN 'hubeau-hydrometrie'
        WHEN type = 'BE.Vlaanderen.Waterinfo.VMM.WaterLevelReading' THEN 'waterinfo-vmm'
        WHEN type = 'NO.NVE.Hydrology.WaterLevelObservation' THEN 'nve-hydro'
        WHEN type = 'FI.SYKE.Hydrology.WaterLevelObservation' THEN 'syke-hydro'
        WHEN type = 'CH.BAFU.Hydrology.WaterLevelObservation' THEN 'bafu-hydro'
        WHEN type = 'DE.Waters.Hydrology.WaterLevelObservation' THEN 'german-waters'
        ELSE NULL
    END AS source_system,

    System.Timestamp() AS ingestion_time,

    'EU.Eurowater.Measurement' AS [__ce_type]

FROM EventInput
WHERE (
    type = 'SE.Gov.SMHI.Hydro.DischargeObservation'
    OR (type = 'CZ.Gov.CHMI.Hydro.WaterLevelObservation' AND data.discharge IS NOT NULL)
    OR (type = 'PL.Gov.IMGW.Hydro.WaterLevelObservation' AND data.discharge IS NOT NULL)
    OR (type = 'FR.Gov.Eaufrance.HubEau.Hydrometrie.Observation' AND data.grandeur_hydro = 'Q')
    OR (type = 'BE.Vlaanderen.Waterinfo.VMM.WaterLevelReading' AND data.parameter_name = 'Q')
    OR (type = 'NO.NVE.Hydrology.WaterLevelObservation' AND data.discharge IS NOT NULL)
    OR (type = 'FI.SYKE.Hydrology.WaterLevelObservation' AND data.discharge IS NOT NULL)
    OR (type = 'CH.BAFU.Hydrology.WaterLevelObservation' AND data.discharge IS NOT NULL)
    OR (type = 'DE.Waters.Hydrology.WaterLevelObservation' AND data.discharge IS NOT NULL)
)

UNION ALL

-- ===================== WATER TEMPERATURE =====================
-- Sources: CHMI, IMGW, BAFU
SELECT
    CASE
        WHEN type = 'CZ.Gov.CHMI.Hydro.WaterLevelObservation'
            THEN CONCAT('cz-', data.station_id)
        WHEN type = 'PL.Gov.IMGW.Hydro.WaterLevelObservation'
            THEN CONCAT('pl-', data.station_id)
        WHEN type = 'CH.BAFU.Hydrology.WaterLevelObservation'
            THEN CONCAT('ch-', data.station_id)
        ELSE NULL
    END AS station_id,

    CASE
        WHEN type = 'CZ.Gov.CHMI.Hydro.WaterLevelObservation' THEN 'cz'
        WHEN type = 'PL.Gov.IMGW.Hydro.WaterLevelObservation' THEN 'pl'
        WHEN type = 'CH.BAFU.Hydrology.WaterLevelObservation' THEN 'ch'
        ELSE NULL
    END AS country_code,

    CASE
        WHEN type = 'CZ.Gov.CHMI.Hydro.WaterLevelObservation'
            THEN data.water_temperature_timestamp
        WHEN type = 'PL.Gov.IMGW.Hydro.WaterLevelObservation'
            THEN data.water_temperature_timestamp
        WHEN type = 'CH.BAFU.Hydrology.WaterLevelObservation'
            THEN data.water_temperature_timestamp
        ELSE NULL
    END AS [timestamp],

    'water_temperature' AS parameter,

    CASE
        WHEN type = 'CZ.Gov.CHMI.Hydro.WaterLevelObservation'
            THEN data.water_temperature
        WHEN type = 'PL.Gov.IMGW.Hydro.WaterLevelObservation'
            THEN data.water_temperature
        WHEN type = 'CH.BAFU.Hydrology.WaterLevelObservation'
            THEN data.water_temperature
        ELSE NULL
    END AS value,

    CASE
        WHEN type = 'CH.BAFU.Hydrology.WaterLevelObservation'
            THEN data.water_temperature_unit
        ELSE 'C'
    END AS unit,

    NULL AS quality,

    CASE
        WHEN type = 'CZ.Gov.CHMI.Hydro.WaterLevelObservation' THEN 'chmi-hydro'
        WHEN type = 'PL.Gov.IMGW.Hydro.WaterLevelObservation' THEN 'imgw-hydro'
        WHEN type = 'CH.BAFU.Hydrology.WaterLevelObservation' THEN 'bafu-hydro'
        ELSE NULL
    END AS source_system,

    System.Timestamp() AS ingestion_time,

    'EU.Eurowater.Measurement' AS [__ce_type]

FROM EventInput
WHERE (
    (type = 'CZ.Gov.CHMI.Hydro.WaterLevelObservation' AND data.water_temperature IS NOT NULL)
    OR (type = 'PL.Gov.IMGW.Hydro.WaterLevelObservation' AND data.water_temperature IS NOT NULL)
    OR (type = 'CH.BAFU.Hydrology.WaterLevelObservation' AND data.water_temperature IS NOT NULL)
);
