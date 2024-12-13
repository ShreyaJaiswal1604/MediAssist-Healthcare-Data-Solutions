{{ config(
    materialized='table',
    schema='prod_mimic'
) }}

SELECT
    ROW_NUMBER() OVER (ORDER BY DIS.DIS_RECORD_ID) AS FRS_RECORD_ID,  -- Surrogate Key
    DIS.DIS_RECORD_ID,
    DRG.DRG_RECORD_ID,
    CASE
        WHEN DRG.DRG_SEVERITY >= 3 AND DRG.DRG_MORTALITY >= 3 THEN 3
        WHEN DRG.DRG_SEVERITY >= 2 AND DRG.DRG_MORTALITY >= 2 THEN 2
        ELSE 1
    END AS FRS_RISK_LEVEL  -- Risk Level
FROM
    {{ ref('DIM_DISCHARGE') }} AS DIS
JOIN
    {{ ref('DIM_DRGCODES') }} AS DRG
    ON DIS.DIS_HADM_ID = DRG.DRG_HADM_ID