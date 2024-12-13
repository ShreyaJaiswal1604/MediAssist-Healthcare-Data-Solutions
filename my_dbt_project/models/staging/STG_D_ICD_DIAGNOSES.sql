{{ config(materialized='table') }}

WITH transformed_icd_diagnoses AS (
    SELECT
        COALESCE(ICD_CODE, 'UNKNOWN') AS ICD_CODE,
        COALESCE(ICD_VERSION, 0) AS ICD_VERSION,
        COALESCE(LONG_TITLE, 'NO DESCRIPTION AVAILABLE') AS LONG_TITLE
    FROM {{ source('raw_mimic', 'RAW_D_ICD_DIAGNOSES') }}  -- Reference to the source table
)

SELECT * 
FROM transformed_icd_diagnoses