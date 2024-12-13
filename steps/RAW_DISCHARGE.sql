---- Following statement is creating table

CREATE TABLE IF NOT EXISTS RAW_DISCHARGE (
   note_id TEXT,
   subject_id NUMBER(8, 0),
   hadm_id NUMBER(8, 0),
   note_type TEXT,
   note_seq NUMBER(3, 0),
   charttime TIMESTAMP_NTZ,
   storetime TIMESTAMP_NTZ,
   text TEXT)
-- Following statement is executing copy command

    COPY INTO RAW_DISCHARGE
    FROM @my_internal_stage_csv/discharge.csv.gz
    FILE_FORMAT = (FORMAT_NAME = 'file_format_load')
    ;
    