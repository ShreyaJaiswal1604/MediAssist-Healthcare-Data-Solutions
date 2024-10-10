---- Creating table ----

CREATE TABLE IF NOT EXISTS MIMIC_ADMISSIONS_RAW (
   subject_id NUMBER(8, 0),
   hadm_id NUMBER(8, 0),
   admittime TIMESTAMP_NTZ,
   dischtime TIMESTAMP_NTZ,
   deathtime TIMESTAMP_NTZ,
   admission_type TEXT,
   admit_provider_id TEXT,
   admission_location TEXT,
   discharge_location TEXT,
   insurance TEXT,
   language TEXT,
   marital_status TEXT,
   race TEXT,
   edregtime TIMESTAMP_NTZ,
   edouttime TIMESTAMP_NTZ,
   hospital_expire_flag NUMBER(1, 0))
---- Copying data into table ----

    COPY INTO mimic_admissions_raw
    FROM @my_internal_stage/admissions.csv.gz
    FILE_FORMAT = (FORMAT_NAME = 'file_format_load')
    ON_ERROR = 'CONTINUE';;
    