---- Following statement is creating table

CREATE TABLE IF NOT EXISTS RAW_DRGCODES (
   subject_id NUMBER(8, 0),
   hadm_id NUMBER(8, 0),
   drg_type TEXT,
   drg_code NUMBER(3, 0),
   description TEXT,
   drg_severity NUMBER(1, 0),
   drg_mortality NUMBER(1, 0))
-- Following statement is executing copy command

    COPY INTO RAW_DRGCODES
    FROM @my_internal_stage_csv/drgcodes.csv.gz
    FILE_FORMAT = (FORMAT_NAME = 'file_format_load')
    ;
    