{{ config(materialized='table') }}

WITH standardized_icd_procedures AS (
    SELECT
        COALESCE(ICD_CODE, 'UNKNOWN') AS ICD_CODE,
        COALESCE(ICD_VERSION, 0) AS ICD_VERSION,
        COALESCE(LONG_TITLE, 'NO DESCRIPTION AVAILABLE') AS LONG_TITLE
    FROM {{ source('raw_mimic', 'RAW_D_ICD_PROCEDURES') }}  -- Reference to the source table
)

SELECT * 
FROM standardized_icd_procedures