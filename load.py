import pandas as pd
from sqlalchemy import create_engine
import os

def load_jobs():
    print("Starting data load process...")
    
    input_path = "data/cleaned_jobs.csv"
    
    # SQLite connection string pointing to a local file
    db_path = "sqlite:///data/jobs.db" 
    
    # 1. Safety check
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found. Run transform.py first.")
        return

    # 2. Read the cleaned data
    df = pd.read_csv(input_path)
    
    if df.empty:
        print("No data to load.")
        return

    # 3. Create a database engine
    engine = create_engine(db_path)
    
    # 4. Load data into SQL
    table_name = "job_market_trends"
    
    try:
        # if_exists='append' is crucial. It means if we run this script next week, 
        # it adds the new jobs to the bottom of the table instead of overwriting it.
        df.to_sql(table_name, con=engine, if_exists='append', index=False)
        print(f"Success! Loaded {len(df)} rows into the '{table_name}' table.")
        print("Database file created at: data/jobs.db")
    except Exception as e:
        print(f"Failed to load data: {e}")

if __name__ == "__main__":
    load_jobs()