---- Creating table ----

CREATE TABLE IF NOT EXISTS MIMIC_DRGCODES_RAW (
   subject_id NUMBER(8, 0),
   hadm_id NUMBER(8, 0),
   drg_type TEXT,
   drg_code NUMBER(3, 0),
   description TEXT,
   drg_severity NUMBER(1, 0),
   drg_mortality NUMBER(1, 0))
---- Copying data into table ----

    COPY INTO mimic_drgcodes_raw
    FROM @my_internal_stage/drgcodes.csv.gz
    FILE_FORMAT = (FORMAT_NAME = 'file_format_load')
    ON_ERROR = 'CONTINUE';;
    