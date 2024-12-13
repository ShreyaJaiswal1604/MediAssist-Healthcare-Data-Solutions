{{ config(materialized='table') }}

WITH raw_pharmacy AS (
    SELECT
        COALESCE(SUBJECT_ID, -1) AS SUBJECT_ID,             -- Replace NULLs with -1 for SUBJECT_ID
        COALESCE(HADM_ID, -1) AS HADM_ID,                  -- Replace NULLs with -1 for HADM_ID
        COALESCE(PHARMACY_ID, -1) AS PHARMACY_ID,          -- Replace NULLs with -1 for PHARMACY_ID
        COALESCE(TRIM(MEDICATION), 'UNKNOWN') AS MEDICATION,  -- Replace NULLs with 'UNKNOWN' for MEDICATION
        COALESCE(TRIM(FREQUENCY), 'NOT SPECIFIED') AS FREQUENCY -- Replace NULLs with 'NOT SPECIFIED' for FREQUENCY
    FROM {{ source('raw_mimic', 'RAW_PHARMACY') }}    -- Source raw data
    WHERE SUBJECT_ID IS NOT NULL                           -- Exclude rows with NULL SUBJECT_ID
      AND HADM_ID IS NOT NULL                              -- Exclude rows with NULL HADM_ID
)

SELECT * 
FROM raw_pharmacy
