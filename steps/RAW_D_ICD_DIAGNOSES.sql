---- Following statement is creating table

CREATE TABLE IF NOT EXISTS RAW_D_ICD_DIAGNOSES (
   icd_code TEXT,
   icd_version NUMBER(2, 0),
   long_title TEXT)
-- Following statement is executing copy command

    COPY INTO RAW_D_ICD_DIAGNOSES
    FROM @my_internal_stage_csv/d_icd_diagnoses.csv.gz
    FILE_FORMAT = (FORMAT_NAME = 'file_format_load')
    ;
    