{{ config(
    materialized='table',
    schema='prod_mimic'
) }}

SELECT
    ROW_NUMBER() OVER (ORDER BY NOTE_ID) AS DIS_RECORD_ID,
    NOTE_ID AS DIS_NOTE_ID,
    SUBJECT_ID AS DIS_SUBJECT_ID,
    HADM_ID AS DIS_HADM_ID,
    CHARTTIME AS DIS_CHART_TIME,
    STORETIME AS DIS_STORE_TIME,
    TEXT AS DIS_NOTE_TEXT,
    NULL AS DIS_NOTE_SUMMARY  -- Placeholder for discharge note summary
FROM
    {{ source('staging_mimic', 'STG_DISCHARGE') }}
