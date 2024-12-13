{{ config(
    materialized='table'
) }}

SELECT
    ROW_NUMBER() OVER (ORDER BY DRG_CODE) AS DRG_RECORD_ID,
    DRG_CODE AS DRG_CODE,
    DESCRIPTION AS DRG_DESCRIPTION,
    DRG_SEVERITY,
    DRG_MORTALITY
FROM
    {{ source('staging_mimic', 'STG_DRGCODES') }}
