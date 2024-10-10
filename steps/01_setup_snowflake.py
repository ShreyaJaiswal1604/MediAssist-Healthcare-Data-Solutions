import snowflake.connector

# Snowflake connection parameters
USER = 'DOLPHIN'
PASSWORD = 'Maapaa@1603'
ACCOUNT = 'URB63596'
# WAREHOUSE = 'None'  # Optional, can be set to None
DATABASE = 'mimic_iv_medi_assist'
SCHEMA = 'raw'

def create_database_and_schema():
    # Connect to Snowflake
    conn = snowflake.connector.connect(
        user=USER,
        password=PASSWORD,
        account=ACCOUNT
        #warehouse=WAREHOUSE
    )
    
    try:
        # Create a cursor object
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE OR REPLACE DATABASE {DATABASE};")
        print(f"Database '{DATABASE}' created or already exists.")

        # Create schema if it doesn't exist
        cursor.execute(f"CREATE OR REPLACE SCHEMA {DATABASE}.{SCHEMA};")
        print(f"Schema '{SCHEMA}' created or already exists in database '{DATABASE}'.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_database_and_schema()
