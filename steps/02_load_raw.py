#------------------------------------------------------------------------------
# MediAssist: Data Engineering with Snowpark
# Script:       02_load_raw.py
# Author:       Shreya Jaiswal
# Last Updated: 10/04/2024
#------------------------------------------------------------------------------

import snowflake.snowpark as snowpark

# Snowflake connection parameters
USER = 'DOLPHIN'
PASSWORD = 'Maapaa@1603'
ACCOUNT = 'URB63596'
DATABASE = 'medi_assist_mimic_iv'  # Already created
SCHEMA = 'raw'  # Already created
WAREHOUSE = 'my_warehouse'  # Define your warehouse here

# Internal stage name
STAGE_NAME = 'my_internal_stage'

# CSV files and their naming conventions
HOSP_FILES = [
    'admissions.csv.gz',
    'd_icd_diagnoses.csv.gz',
    'd_icd_procedures.csv.gz',
    'drgcodes.csv.gz',
    'labevents.csv.gz',
    'patients.csv.gz',
    'pharmacy.csv.gz',
]

ICU_FILES = [
    'chartevents.csv.gz',
    'icustays.csv.gz',
]

# Define the tables to load with naming conventions
TABLES_TO_LOAD = {
    'hosp': HOSP_FILES,
    'icu': ICU_FILES
}

def create_file_format(session):
    print("Creating file format...")
    session.sql("""
        CREATE OR REPLACE FILE FORMAT file_format_csv
        TYPE = 'CSV'
        COMPRESSION = 'GZIP'                   -- Specify GZIP compression for .gz files
        FIELD_DELIMITER = ','                   -- Specify the field delimiter
        PARSE_HEADER = TRUE                      -- Parse the header row for column names
        FIELD_OPTIONALLY_ENCLOSED_BY = '"';     -- Optional field enclosure
    """).collect()

    print("File format 'file_format_csv' created successfully.")
    print("===========")

def create_table(session, table_name, file_path):
    # Use the schema
    #session.use_schema(SCHEMA)
    # Use the database and schema
    session.sql(f"USE DATABASE {DATABASE}").collect()
    session.sql(f"USE SCHEMA {SCHEMA}").collect()

    # Load data from internal stage into the Snowflake table
    location = f'@{STAGE_NAME}/{file_path}'  # Reference to internal stage
    print(f"Creating table '{table_name}' with inferred schema from {location}...")

    try:
        # Create or replace the table with inferred schema from the specified file
        session.sql(f"""
            CREATE OR REPLACE TABLE {table_name}
            USING TEMPLATE (
                SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
                FROM TABLE(
                    INFER_SCHEMA(
                        LOCATION => '{location}',
                        FILE_FORMAT => 'file_format_csv'
                    )
                )
            );
        """).collect()

        print(f"Table '{table_name}' created successfully with inferred schema.")
    except Exception as e:
        print(f"Error creating table '{table_name}': {e}")
    print("===========\n\n")

def load_data(session, table_name, file_path):
    """
    Load data from the internal stage into the specified Snowflake table.

    Parameters:
    - session: Snowpark session object
    - table_name: Name of the table to load data into
    - file_path: Path to the CSV file in the internal stage
    """
    # Construct the location for the CSV file
    location = f'@{STAGE_NAME}/{file_path}'  # Reference to internal stage
    print(f"Loading data into '{table_name}' from {location}...")

    try:
        # Load data into the Snowflake table using the COPY INTO command
        session.sql(f"""
            COPY INTO {table_name}
            FROM {location}
            FILE_FORMAT = (TYPE = CSV, COMPRESSION = 'GZIP', RECORD_DELIMITER = '\n', SKIP_HEADER = 1)
            ON_ERROR = 'CONTINUE';
        """).collect()

        print(f"Data loaded into table '{table_name}' successfully.")
    except Exception as e:
        print(f"Error loading data into '{table_name}': {e}")
    print("===========")



def load_all_raw_tables(session):
    # Use the warehouse
    session.sql(f"USE WAREHOUSE {WAREHOUSE};").collect()  # Ensure the warehouse is active
    
    # Load all specified tables with naming conventions
    for category, files in TABLES_TO_LOAD.items():
        for file in files:
            # Extract the table name and apply naming convention
            table_name = f"{category}_{file.split('.')[0]}"  # Remove .gz extension
            #create_table(session, table_name, file)  # Create the table
            load_data(session, table_name, file)  # Load the data

# For local debugging
if __name__ == "__main__":
    # Create a local Snowpark session
    with snowpark.Session.builder \
        .config("user", USER) \
        .config("password", PASSWORD) \
        .config("account", ACCOUNT) \
        .config("database", DATABASE) \
        .config("schema", SCHEMA) \
        .getOrCreate() as session:

        create_file_format(session)  # Create file format
        load_all_raw_tables(session)


# def load_data(session, table_name, file_path):
#     # Load data from internal stage into the Snowflake table
#     location = f'@{STAGE_NAME}/{file_path}'  # Reference to internal stage
#     print(f"Loading data into {table_name} from {location}...")
#     try:
#         session.sql(f"""
#             COPY INTO {table_name}
#             FROM {location};
#         """).collect()
#         print(f"Data loaded into table '{table_name}' successfully.")
#     except Exception as e:
#         print(f"Error loading data into '{table_name}': {e}")


# def load_raw_table(session, table_name, file_path):
#     # Use the schema
#     session.use_schema(SCHEMA)

#     # Load data from internal stage into the Snowflake table
#     location = f'@{STAGE_NAME}/{file_path}'  # Reference to internal stage
#     print(f"location --> {location}")
#     print(f"Loading data into {table_name} from {location}...")

#     # Create or replace the table with inferred schema from the specified file
#     session.sql(f"""
#         CREATE OR REPLACE TABLE {table_name}
#         USING TEMPLATE (
#             SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
#             FROM TABLE(
#                 INFER_SCHEMA(
#                     LOCATION => '{location}',
#                     FILE_FORMAT => 'file_format_csv'
#                 )
#             )
#         );
#     """).collect()

#     print(f"Table '{table_name}' created successfully with inferred schema.")
#     print(f"Loading data into table '{table_name}' from internal stage...")

#     # # Load data into Snowflake using COPY INTO
#     # session.sql(f"""
#     #     COPY INTO {table_name}
#     #     FROM {location}
#     #     FILE_FORMAT = (FORMAT_NAME = 'file_format_csv');
#     # """).collect()

#     # print(f"Data loaded into table '{table_name}' successfully.")
#     # print("===========")

# def load_all_raw_tables(session):
#     # Load all specified tables with naming conventions
#     for category, files in TABLES_TO_LOAD.items():
#         for file in files:
#             # Extract the table name and apply naming convention
#             table_name = f"{category}_{file.split('.')[0]}"  # Remove .gz extension
#             load_raw_table(session, table_name, file)

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


