---- Creating table ----

CREATE TABLE IF NOT EXISTS MIMIC_DISCHARGE_RAW (
   note_id TEXT,
   subject_id NUMBER(8, 0),
   hadm_id NUMBER(8, 0),
   note_type TEXT,
   note_seq NUMBER(2, 0),
   charttime TIMESTAMP_NTZ,
   storetime TIMESTAMP_NTZ,
   text TEXT)
---- Copying data into table ----

    COPY INTO mimic_discharge_raw
    FROM @my_internal_stage/discharge.csv.gz
    FILE_FORMAT = (FORMAT_NAME = 'file_format_load')
    ON_ERROR = 'CONTINUE';;
    