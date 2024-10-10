---- Creating table ----

CREATE TABLE IF NOT EXISTS MIMIC_D_ICD_PROCEDURES_RAW (
   icd_code TEXT,
   icd_version NUMBER(2, 0),
   long_title TEXT)
---- Copying data into table ----

    COPY INTO mimic_d_icd_procedures_raw
    FROM @my_internal_stage/d_icd_procedures.csv.gz
    FILE_FORMAT = (FORMAT_NAME = 'file_format_load')
    ON_ERROR = 'CONTINUE';;
    