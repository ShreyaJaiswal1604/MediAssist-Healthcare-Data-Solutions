{{ config(
    materialized='table',
    schema='prod_mimic'
) }}

SELECT
    ROW_NUMBER() OVER (ORDER BY ICD_CODE) AS ICD_RECORD_ID,
    ICD_CODE AS ICD_CODE,
    ICD_VERSION AS ICD_VERSION,
    LONG_TITLE AS ICD_LONG_TITLE,
    'DIAGNOSIS' AS ICD_TYPE,
    'D' AS ICD_TYPEFLAG  -- Flag for Diagnosis
FROM
    {{ source('staging_mimic', 'STG_D_ICD_DIAGNOSES') }}

UNION ALL

SELECT
    ROW_NUMBER() OVER (ORDER BY ICD_CODE) AS ICD_RECORD_ID,
    ICD_CODE AS ICD_CODE,
    ICD_VERSION AS ICD_VERSION,
    LONG_TITLE AS ICD_LONG_TITLE,
    'PROCEDURE' AS ICD_TYPE,
    'P' AS ICD_TYPEFLAG  -- Flag for Procedure
FROM
    {{ source('staging_mimic', 'STG_D_ICD_PROCEDURES') }}
