import time
from main import run_etl  # Import your ETL function or main logic

while True:
    print("Starting ETL process...")
    run_etl() 
    print("ETL process completed. Waiting 24 hours until the next run...")
    time.sleep(24 * 60 * 60)  # Wait for 24 hours (in seconds)
