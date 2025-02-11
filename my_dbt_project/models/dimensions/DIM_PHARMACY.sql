{{ config(
    materialized='table',
    schema='prod_mimic'
) }}

SELECT
    ROW_NUMBER() OVER (ORDER BY SUBJECT_ID, PHARMACY_ID) AS PHR_RECORD_ID,
    PHARMACY_ID AS PHR_PHARMACY_ID,
    MEDICATION AS PHR_MEDICATION,
    FREQUENCY AS PHR_FREQUENCY,
    IS_HIGH_RISK AS PHR_IS_HIGH_RISK,
    IS_UNUSUAL_FREQUENCY AS PHR_IS_UNUSUAL_FREQUENCY
FROM
    {{ source('staging_mimic', 'STG_PHARMACY') }}