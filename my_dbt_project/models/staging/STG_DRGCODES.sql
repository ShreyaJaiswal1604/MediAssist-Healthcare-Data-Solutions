{{ config(materialized='table') }}

WITH transformed_drgcodes AS (
    SELECT
        COALESCE(SUBJECT_ID, 0) AS SUBJECT_ID,
        COALESCE(HADM_ID, 0) AS HADM_ID,
        COALESCE(DRG_CODE, 0) AS DRG_CODE,
        COALESCE(DESCRIPTION, 'UNKNOWN') AS DESCRIPTION,
        COALESCE(DRG_SEVERITY, 0) AS DRG_SEVERITY,
        COALESCE(DRG_MORTALITY, 0) AS DRG_MORTALITY
    FROM {{ source('raw_mimic', 'RAW_DRGCODES') }}  -- Reference to the source table
    WHERE DRG_TYPE = 'APR'
)

SELECT * FROM transformed_drgcodes