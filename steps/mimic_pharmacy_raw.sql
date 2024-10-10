---- Creating table ----

CREATE TABLE IF NOT EXISTS MIMIC_PHARMACY_RAW (
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
   sliding_scale TEXT,
   lockout_interval TEXT,
   basal_rate TEXT,
   one_hr_max TEXT,
   doses_per_24_hrs NUMBER(1, 0),
   duration NUMBER(1, 0),
   duration_interval TEXT,
   expiration_value NUMBER(2, 0),
   expiration_unit TEXT,
   expirationdate TEXT,
   dispensation TEXT,
   fill_quantity TEXT)
---- Copying data into table ----

    COPY INTO mimic_pharmacy_raw
    FROM @my_internal_stage/pharmacy.csv.gz
    FILE_FORMAT = (FORMAT_NAME = 'file_format_load')
    ON_ERROR = 'CONTINUE';;
    