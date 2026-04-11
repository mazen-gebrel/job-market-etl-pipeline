import requests
import json
import os

def extract_jobs():
    """
    Pulls the latest remote Data Science, Analytics, and Engineering jobs 
    from the public Jobicy API.
    """
    url = "https://jobicy.com/api/v2/remote-jobs"
    
    # We pass only the parameters explicitly supported by the API
    params = {
        "industry": "data-science", # Captures Data Analytics, DE, and ML roles
        "count": 50 # Number of listings to retrieve
    }

    print("Fetching live job listings...")
    response = requests.get(url, params=params)

    # 200 means the request was successful
    if response.status_code == 200:
        data = response.json()
        jobs = data.get("jobs", [])
        
        # Best practice: create a directory for raw data if it doesn't exist
        os.makedirs("data", exist_ok=True)
        
        # Save the raw JSON data before doing any transformations
        file_path = "data/raw_jobs.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(jobs, f, indent=4)
            
        print(f"Success! Extracted {len(jobs)} jobs and saved to {file_path}")
    else:
        print(f"Failed to fetch data. HTTP Status code: {response.status_code}")
        # Print the exact error message from the server to help debug
        print(f"Error details: {response.text}")

if __name__ == "__main__":
    extract_jobs()