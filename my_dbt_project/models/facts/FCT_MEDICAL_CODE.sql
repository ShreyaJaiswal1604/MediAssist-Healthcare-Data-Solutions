{{ config(
    materialized='table'
) }}


SELECT
    ROW_NUMBER() OVER (ORDER BY MC.DMC_RECORD_ID) AS FMC_RECORD_ID,  -- Surrogate Key
    MC.DMC_RECORD_ID,  -- Foreign key referencing DIM_MEDICAL_CODES_LLM
    DP.ICD_RECORD_ID AS IDP_RECORD_ID  -- Foreign key referencing DIM_ICD_DIAGNOSES_PROCEDURES
FROM
    {{ source('prod_mimic', 'DIM_MEDICAL_CODES_LLM') }} AS MC  -- Source for medical codes
LEFT JOIN
    {{ source('prod_mimic', 'DIM_ICD_DIAGNOSES_PROCEDURES') }} AS DP  -- Source for diagnoses/procedures
    ON MC.DMC_ICD_CODE = DP.ICD_CODE  -- Match ICD codes



