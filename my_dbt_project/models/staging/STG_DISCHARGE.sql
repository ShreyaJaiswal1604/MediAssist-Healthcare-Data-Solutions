{{ config(materialized='table') }}

WITH raw_discharge AS (
    SELECT
        COALESCE(NOTE_ID, 'UNKNOWN') AS NOTE_ID,                      -- Handling NULLs in NOTE_ID
        COALESCE(SUBJECT_ID, 0) AS SUBJECT_ID,                        -- Replace NULLs with 0 for SUBJECT_ID
        COALESCE(HADM_ID, 0) AS HADM_ID,                              -- Replace NULLs with 0 for HADM_ID
        COALESCE(CHARTTIME, '1900-01-01 00:00:00') AS CHARTTIME,      -- Default timestamp for NULL CHARTTIME
        COALESCE(STORETIME, '1900-01-01 00:00:00') AS STORETIME,      -- Default timestamp for NULL STORETIME
        COALESCE(TEXT, 'UNKNOWN') AS TEXT                             -- Replace NULLs in TEXT with 'UNKNOWN'
    FROM {{ source('raw_mimic', 'RAW_DISCHARGE') }}                   -- Source raw data
    WHERE SUBJECT_ID IS NOT NULL                                      -- Exclude rows with NULL SUBJECT_ID
      AND HADM_ID IS NOT NULL                                         -- Exclude rows with NULL HADM_ID
)

SELECT * FROM raw_discharge
