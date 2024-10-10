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



def generate_copy_statement(table_name, stage_name, csv_file_path, file_format):
    """
    Generates a COPY INTO statement to load data from a file into a table.
    """
    copy_command = f"""
    COPY INTO {table_name}
    FROM @{stage_name}/{csv_file_path}
    FILE_FORMAT = (FORMAT_NAME = '{file_format}')
    ON_ERROR = 'CONTINUE';;
    """
    return copy_command

def create_file_format(session):
    print("Creating file format for DDL...")
    session.sql("""
        CREATE OR REPLACE FILE FORMAT file_format_ddl
        TYPE = 'CSV'
        COMPRESSION = 'auto'                   -- Specify GZIP compression for .gz files
        FIELD_DELIMITER = ','                   -- Specify the field delimiter
        PARSE_HEADER = TRUE                    -- Parse the header row for column names
        FIELD_OPTIONALLY_ENCLOSED_BY = '\042'
        ESCAPE_UNENCLOSED_FIELD = NONE 
        TRIM_SPACE = TRUE 
        ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE;
    """).collect()

    print("File format 'file_format_ddl' created successfully.")
    print("===========")

    session.sql("""
        CREATE OR REPLACE FILE FORMAT file_format_load
        TYPE = 'CSV'
        COMPRESSION = 'auto'                   -- Specify GZIP compression for .gz files
        FIELD_DELIMITER = ','                   -- Specify the field delimiter
        RECORD_DELIMITER = '\n' 
        SKIP_HEADER = 1                      -- Parse the header row for column names
        FIELD_OPTIONALLY_ENCLOSED_BY = '\042'     -- Optional field enclosure
        ;
    """).collect()

    print("File format 'file_format_load' created successfully.")
    print("===========")

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

    # List files in the internal stage
    stg_files = session.sql("LIST @my_internal_stage").collect()
    print("Files in stage:", stg_files)


    for row in stg_files:
        print("======================================================\n")
        row_value = row.as_dict()
        stg_file_path_value = row_value.get('name')

        file_path, file_name = os.path.split(stg_file_path_value)
        print(f"Processing file: {file_name}")

        stg_location = "@" + file_path

        if file_name == 'discharge.csv.gz' or file_name == 'pharmacy.csv.gz':
                    # Construct the SQL for schema inference
            infer_schema_sql = f"""
                SELECT * 
                FROM TABLE(
                    INFER_SCHEMA(
                        LOCATION => '{stg_location}/',
                        FILES => '{file_name}',
                        FILE_FORMAT => 'file_format_ddl',
                        MAX_RECORDS_PER_FILE => 5
                        
                    )
                );
            """
        else:
            # Construct the SQL for schema inference
            infer_schema_sql = f"""
                SELECT * 
                FROM TABLE(
                    INFER_SCHEMA(
                        LOCATION => '{stg_location}/',
                        FILES => '{file_name}',
                        FILE_FORMAT => 'file_format_ddl'
                        
                    )
                );
            """

        print(f"\n=========== INFER SCHEMA SQL =============\n{infer_schema_sql}\n")

        # Infer the schema from the CSV file
        try:
            inferred_schema_rows = session.sql(infer_schema_sql).collect()
            print("Inferred schema:", inferred_schema_rows)
        except Exception as e:
            print(f"Error inferring schema for {file_name}: {e}")
            continue

        col_name_lst = []
        col_data_type_lst = []

        for schema_row in inferred_schema_rows:
            row_value = schema_row.as_dict()
            column_name = row_value.get('COLUMN_NAME')
            column_type = row_value.get('TYPE')
            col_name_lst.append(column_name)
            col_data_type_lst.append(column_type)

        # Generate the DDL statement
        table_name = f"mimic_{file_name.split('.')[0]}_raw"
        create_ddl_stmt = generate_ddl_statement(col_name_lst, col_data_type_lst, table_name.upper())
        print("=================== DDL STATEMENT =====================\n\n", create_ddl_stmt)

        # Generate the COPY INTO statement
        copy_stmt = generate_copy_statement(table_name, 'my_internal_stage', file_name, 'file_format_load')
        print("=================== COPY STATEMENT =====================\n\n", copy_stmt)

        # Write SQL statements to a file
        sql_file_path = f"{table_name}.sql"
        print(f"Writing SQL statements to: {sql_file_path}")
        with open(sql_file_path, "w") as sql_file:
            sql_file.write("---- Creating table ----\n\n")
            sql_file.write(create_ddl_stmt)
            sql_file.write("\n---- Copying data into table ----\n")
            sql_file.write(copy_stmt)

        # Execute the DDL and COPY statements
        try:
            session.sql(create_ddl_stmt).collect()
            print(f"Table {table_name} created successfully.")
        except Exception as e:
            print(f"Error creating table {table_name}: {e}")
            continue

        try:
            session.sql(copy_stmt).collect()
            print(f"Data loaded into {table_name} successfully.")
        except Exception as e:
            print(f"Error loading data into {table_name}: {e}")
            continue

    utc_end_time = datetime.utcnow()
    print("Total time taken to load the entire data:", utc_end_time - utc_start_time)

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

