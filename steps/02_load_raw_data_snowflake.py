#------------------------------------------------------------------------------
# MediAssist: Data Engineering with Snowpark
# Script:       02_load_raw.py
# Author:       Shreya Jaiswal
# Last Updated: 10/09/2024
#------------------------------------------------------------------------------

# 01_load_raw_data_snowflake.py

from snowflake.snowpark import Session
import os
from datetime import datetime

def snowpark_basic_auth() -> Session:
    """
    Establishes a Snowpark session using basic authentication.
    """
    connection_parameters = {
        "ACCOUNT":"URB63596",
        "USER":"DOLPHIN",
        "PASSWORD":"Maapaa@1603"
    }
    return Session.builder.configs(connection_parameters).create()


def generate_ddl_statement(column_names, data_types, table_name):
    ddl_template = "CREATE TABLE IF NOT EXISTS {} (\n{})"
    columns = []
    for name, data_type in zip(column_names, data_types):
        column_definition = f"   {name} {data_type}"
        columns.append(column_definition)

    ddl_statement = ddl_template.format(table_name, ",\n".join(columns))
    return ddl_statement



def generate_copy_statement(table_name,stage_name,csv_file_path,file_format):
    copy_command = f"""
    COPY INTO {table_name}
    FROM @{stage_name}/{csv_file_path}
    FILE_FORMAT = (FORMAT_NAME = '{file_format}')
    ;
    """

    return copy_command

def create_file_format(session):
    print("Creating file format for DDL...")
    session.sql("""
        CREATE OR REPLACE FILE FORMAT file_format_ddl
        TYPE = 'CSV'
        COMPRESSION = 'GZIP'                   -- Specify GZIP compression for .gz files
        FIELD_DELIMITER = ','                   -- Specify the field delimiter
        PARSE_HEADER = TRUE                    -- Parse the header row for column names
        FIELD_OPTIONALLY_ENCLOSED_BY = '"'
        ESCAPE_UNENCLOSED_FIELD = NONE 
        TRIM_SPACE = TRUE 
        ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE;
    """).collect()

    print("File format 'file_format_ddl' created successfully.")
    print("===========")

    session.sql("""
        CREATE OR REPLACE FILE FORMAT file_format_load
        TYPE = 'CSV'
        COMPRESSION = 'auto'                   
        FIELD_DELIMITER = ','                   
        RECORD_DELIMITER = '\n'
        SKIP_HEADER = 1                      
        FIELD_OPTIONALLY_ENCLOSED_BY = '"'
        NULL_IF = ('NA', 'NULL', '')
        ESCAPE_UNENCLOSED_FIELD = None;
    """).collect()

    print("File format 'file_format_load' created successfully.")
    print("===========")

def create_audit_table(session):
    """
    Creates an audit table to log metadata about the data load process.
    """
    audit_table_ddl = """
    CREATE TABLE IF NOT EXISTS data_load_audit (
        load_id INT AUTOINCREMENT,          -- Changed to INT for AUTOINCREMENT
        table_name STRING,
        file_name STRING,
        load_status STRING,
        start_time TIMESTAMP,
        end_time TIMESTAMP,
        total_time STRING,                  -- Assuming you need total_time as STRING or change type if needed
        file_size STRING,                   -- Assuming you need file_size as STRING or change type if needed
        error_message STRING,
        processed_rows INT,
        PRIMARY KEY (load_id)
    );
    """
    session.sql(audit_table_ddl).collect()
    print("Audit table 'data_load_audit' created successfully.")


def log_audit_record(session, table_name, file_name, load_status, start_time, end_time, error_message, processed_rows, file_size):
    """
    Logs a record in the audit table with file size in MB, total time, and processed rows.
    """
    # Calculate total load time in seconds
    total_time = (end_time - start_time).total_seconds()

    # # Convert file size from bytes to MB (or GB)
    # file_size_mb = file_size / (1024 * 1024)  # Convert bytes to MB
    # file_size_gb = file_size / (1024 * 1024 * 1024)  # Convert bytes to GB

    # # You can choose which size unit to store (MB or GB), here I am using MB
    # file_size_for_audit = round(file_size_gb, 2)  # Round to 2 decimal places

    # Prepare the SQL query to insert the audit record
    insert_sql = f"""
    INSERT INTO data_load_audit (
        table_name, file_name, load_status, start_time, end_time, total_time, file_size, error_message, processed_rows
    ) VALUES (
        '{table_name}', '{file_name}', '{load_status}', '{start_time}', '{end_time}', {total_time}, {file_size}, '{error_message}', {processed_rows}
    );
    """
    
    # Execute the insert query
    session.sql(insert_sql).collect()
    print("Audit record logged successfully.")


def main():
    """
    Main function to execute the data loading process.
    """
    utc_start_time = datetime.utcnow()
    session = snowpark_basic_auth()

    # Set the context: database, schema, warehouse
    session.sql("USE DATABASE mimic_iv_medi_assist").collect()
    session.sql("USE SCHEMA raw").collect()
    session.sql("USE WAREHOUSE my_warehouse").collect()

    # Create necessary file formats
    create_file_format(session)
      # Create the audit table
    create_audit_table(session)

    # List files in the internal stage
    stg_files = session.sql("LIST @my_internal_stage_csv").collect()
    print("Files in stage:", stg_files)


    utc_start_time = datetime.utcnow()
    print("Process started at:", utc_start_time)

    for row in stg_files:
        print(f"======================= PROCESSING TABLE : {row}===============================\n")
        print("Processing row:", row)
        
        # Convert row to dictionary
        row_value = row.as_dict()
        print("Row as dictionary:", row_value)
        
        # Extract the staged file path value
        stg_file_path_value = row_value.get('name')
        print("Staged file path value:", stg_file_path_value)
        file_size = row_value.get('size')  # Get the file size in bytes

        print("File size:", file_size)

        # Split file path and name
        file_path, file_name = os.path.split(stg_file_path_value)
        print("File path:", file_path)
        print("File name:", file_name)

        # Create staged location variable
        stg_location = "@" + file_path
        print("Staged location:", stg_location)
        
        print(f"Processing target file: {file_name}")
        
        # Generate SQL for inferring schema
        infer_schema_sql = """\
            SELECT * 
            FROM TABLE(
                INFER_SCHEMA(
                LOCATION=>'{}/',
                files => '{}',
                FILE_FORMAT => 'file_format_ddl'
            )    
        )
        """.format(stg_location, file_name)
        
        print("\n=========== INFER SCHEMA SQL =============")
        print(f"File: {file_name}")
        print(infer_schema_sql)

        # Execute schema inference
        inferred_schema_rows = session.sql(infer_schema_sql).collect()
        print("\nSchema inference completed. Inferred schema rows:")
        print(inferred_schema_rows)

        # Prepare lists for column names and types
        col_name_lst = []
        col_data_type_lst = []

        # Process each row in inferred schema
        for row in inferred_schema_rows:
            row_value = row.as_dict()
            print("Inferred schema row:", row_value)
            
            column_name = row_value.get('COLUMN_NAME')
            column_type = row_value.get('TYPE')

            col_name_lst.append(column_name)
            col_data_type_lst.append(column_type)

        print("Column names list:", col_name_lst)
        print("Column data types list:", col_data_type_lst)

        # Generate table name and DDL statement
        table_name = "RAW_" + file_name.split('.')[0] 
        create_ddl_stmt = generate_ddl_statement(col_name_lst, col_data_type_lst, table_name.upper())
        print("=================== DDL STATEMENT =====================")
        print(create_ddl_stmt)

        # Generate copy statement for loading data
        copy_stmt = generate_copy_statement(table_name.upper(), 'my_internal_stage_csv', file_name, 'file_format_load')
        print("=================== COPY STATEMENT =====================")
        print(copy_stmt)

        # Define SQL file path and save DDL and copy statements to file
        sql_file_path = table_name.upper() + ".sql"
        print("=================== SQL FILE PATH =====================")
        print("File path for saving SQL:", sql_file_path)
        with open(sql_file_path, "w") as sql_file:
            sql_file.write("---- Following statement is creating table\n\n")
            sql_file.write(create_ddl_stmt)
            sql_file.write("\n-- Following statement is executing copy command\n")
            sql_file.write(copy_stmt)
        print("SQL statements written to file:", sql_file_path)

        try:
            # Execute DDL to create the table
            start_time = datetime.utcnow()
            # Execute DDL to create the table
            session.sql(create_ddl_stmt).collect()
            print("Table created successfully with DDL statement.")

            # Execute copy command to load data into the table
            session.sql(copy_stmt).collect()
            print("Data loaded into the table with COPY statement.")

            # Query the target table to get the row count after loading the data
            row_count_result = session.sql(f"SELECT COUNT(*) FROM {table_name}").collect()
            processed_rows = row_count_result[0][0]  # Extract row count from the result
            print(f"Processed rows: {processed_rows}")

            # Calculate total load time
            end_time = datetime.utcnow()

            # Log success in audit table
            log_audit_record(session, table_name, file_name, 'SUCCESS', start_time, end_time, None, processed_rows, file_size)


        except Exception as e:
            # Log failure in audit table
            end_time = datetime.utcnow()
            log_audit_record(session, table_name, file_name, 'FAILURE', utc_start_time, end_time, str(e), 0, file_size)

            print(f"Exception - {e}")



    # End of processing and time calculation
    utc_end_time = datetime.utcnow()
    print("Process completed at:", utc_end_time)
    print("Total processing time:", utc_end_time - utc_start_time)


if __name__ == "__main__":
    main()


















# import snowflake.snowpark as snowpark
# from snowflake.snowpark import Session

# # Snowflake connection parameters
# USER = 'DOLPHIN'
# PASSWORD = 'Maapaa@1603'
# ACCOUNT = 'URB63596'
# DATABASE = 'mimic_iv_medi_assist'  # Already created
# SCHEMA = 'raw'  # Already created
# WAREHOUSE = 'my_warehouse'  # Define your warehouse here

# # Internal stage name
# STAGE_NAME = 'my_internal_stage'

# # CSV files and their naming conventions
# TABLES_TO_LOAD = [
#     'admissions.csv.gz',
#     'd_icd_diagnoses.csv.gz',
#     'd_icd_procedures.csv.gz',
#     'discharge.csv.gz',
#     'drgcodes.csv.gz',
#     'pharmacy.csv.gz',
# ]


# def create_file_format(session):
#     print("Creating file format...")
#     session.sql("""
#         CREATE OR REPLACE FILE FORMAT file_format_csv
#         TYPE = 'CSV'
#         COMPRESSION = 'GZIP'                   -- Specify GZIP compression for .gz files
#         FIELD_DELIMITER = ','                   -- Specify the field delimiter
#         PARSE_HEADER = TRUE                      -- Parse the header row for column names
#         FIELD_OPTIONALLY_ENCLOSED_BY = '"';     -- Optional field enclosure
#     """).collect()

#     print("File format 'file_format_csv' created successfully.")
#     print("===========")

# def create_table(session, table_name, file_path):
#     # Use the schema
#     #session.use_schema(SCHEMA)
#     # Use the database and schema
#     session.sql(f"USE DATABASE {DATABASE}").collect()
#     session.sql(f"USE SCHEMA {SCHEMA}").collect()

#     # Load data from internal stage into the Snowflake table
#     location = f'@{STAGE_NAME}/{file_path}'  # Reference to internal stage
#     print(f"Creating table '{table_name}' with inferred schema from {location}...")

#     try:
#         # Create or replace the table with inferred schema from the specified file
#         session.sql(f"""
#             CREATE OR REPLACE TABLE {table_name}
#             USING TEMPLATE (
#                 SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
#                 FROM TABLE(
#                     INFER_SCHEMA(
#                         LOCATION => '{location}',
#                         FILE_FORMAT => 'file_format_csv',
#                         ON_ERROR => 'CONTINUE'
#                     )
#                 )
#             );
#         """).collect()

#         print(f"Table '{table_name}' created successfully with inferred schema.")
#     except Exception as e:
#         print(f"Error creating table '{table_name}': {e}")
#     print("===========\n\n")

# def load_data(session, table_name, file_path):
#     """
#     Load data from the internal stage into the specified Snowflake table.

#     Parameters:
#     - session: Snowpark session object
#     - table_name: Name of the table to load data into
#     - file_path: Path to the CSV file in the internal stage
#     """
#     # Construct the location for the CSV file
#     location = f'@{STAGE_NAME}/{file_path}'  # Reference to internal stage
#     print(f"Loading data into '{table_name}' from {location}...")

#     try:
#         # Load data into the Snowflake table using the COPY INTO command
#         session.sql(f"""
#             COPY INTO {table_name}
#             FROM {location}
#             FILE_FORMAT = (TYPE = CSV, COMPRESSION = 'GZIP', RECORD_DELIMITER = '\n', SKIP_HEADER = 1)
#             ON_ERROR = 'CONTINUE';
#         """).collect()

#         print(f"Data loaded into table '{table_name}' successfully.")
#     except Exception as e:
#         print(f"Error loading data into '{table_name}': {e}")
#     print("===========")



# def load_all_raw_tables(session):
#     # Ensure the warehouse is active
#     print(f"Using warehouse: {WAREHOUSE}")
#     session.sql(f"USE WAREHOUSE {WAREHOUSE};").collect()

#     # Load all specified tables with naming conventions
#     print(f"Starting to load tables from the list: {TABLES_TO_LOAD}")
    
#     for file in TABLES_TO_LOAD:

#         # Extract the table name and apply naming convention
#         table_name = f"{file.split('.')[0]}"  # Remove .gz extension
#         print(f"Creating table: {table_name} from file: {file}")
        
#         # Create the table
#         create_table(session, table_name, file)
        
#         # If needed in the future, uncomment the line below to load data into the table
#         # print(f"Loading data into table: {table_name} from file: {file}")
#         # load_data(session, table_name, file)
    
#     print("All tables loaded successfully.")


# # For local debugging
# if __name__ == "__main__":
#     # Create a local Snowpark session
#     with snowpark.Session.builder \
#         .config("user", USER) \
#         .config("password", PASSWORD) \
#         .config("account", ACCOUNT) \
#         .config("database", DATABASE) \
#         .config("schema", SCHEMA) \
#         .getOrCreate() as session:

#         create_file_format(session)  # Create file format
#         load_all_raw_tables(session)

