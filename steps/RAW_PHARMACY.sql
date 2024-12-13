---- Following statement is creating table

CREATE TABLE IF NOT EXISTS RAW_PHARMACY (
   subject_id NUMBER(8, 0),
   hadm_id NUMBER(8, 0),
   pharmacy_id NUMBER(8, 0),
   poe_id TEXT,
   starttime TIMESTAMP_NTZ,
   stoptime TIMESTAMP_NTZ,
   medication TEXT,
   proc_type TEXT,
   status TEXT,
   entertime TIMESTAMP_NTZ,
   verifiedtime TIMESTAMP_NTZ,
   route TEXT,
   frequency TEXT,
   disp_sched TEXT,
   infusion_type TEXT,
   sliding_scale BOOLEAN,
   lockout_interval TEXT,
   basal_rate NUMBER(6, 3),
   one_hr_max TEXT,
   doses_per_24_hrs NUMBER(2, 0),
   duration NUMBER(8, 2),
   duration_interval TEXT,
   expiration_value NUMBER(3, 0),
   expiration_unit TEXT,
   expirationdate TIMESTAMP_NTZ,
   dispensation TEXT,
   fill_quantity TEXT)
-- Following statement is executing copy command

    COPY INTO RAW_PHARMACY
    FROM @my_internal_stage_csv/pharmacy.csv.gz
    FILE_FORMAT = (FORMAT_NAME = 'file_format_load')
    ;
    