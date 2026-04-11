import json
import pandas as pd
import re
import os

def clean_html(raw_html):
    """Removes HTML tags and extra whitespace from a string."""
    if not raw_html:
        return ""
    # Regex to strip HTML tags
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    # Remove extra spaces and newlines
    cleantext = re.sub(r'\s+', ' ', cleantext).strip()
    return cleantext

def extract_skills(description):
    """Scans the description for key data engineering/analytics skills."""
    desc_lower = description.lower()
    # Returns True if the skill is found, False otherwise
    return {
        'requires_python': bool(re.search(r'\bpython\b', desc_lower)),
        'requires_sql': bool(re.search(r'\bsql\b', desc_lower)),
        'requires_aws': bool(re.search(r'\baws\b', desc_lower)),
        'requires_azure': bool(re.search(r'\bazure\b', desc_lower)),
        'requires_spark': bool(re.search(r'\bspark\b', desc_lower)),
        'requires_tableau': bool(re.search(r'\btableau\b', desc_lower))
    }

def transform_jobs():
    print("Starting data transformation...")
    
    input_path = "data/raw_jobs.json"
    
    # 1. Safety check
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found. Run extract.py first.")
        return

    # 2. Load the raw data
    with open(input_path, "r", encoding="utf-8") as f:
        raw_jobs = json.load(f)

    if not raw_jobs:
        print("No jobs to transform.")
        return

    # 3. Process each job
    processed_jobs = []
    for job in raw_jobs:
        # Extract basic info
        title = job.get("jobTitle", "")
        company = job.get("companyName", "")
        location = job.get("jobGeo", "")
        pub_date = job.get("pubDate", "")
        
        # Clean the description
        description = clean_html(job.get("jobDescription", ""))
        
        # Extract our skill flags
        skills = extract_skills(description)
        
        # Build the clean record
        job_record = {
            "title": title,
            "company": company,
            "location": location,
            "published_date": pub_date,
        }
        
        # Merge the skill flags into our record
        job_record.update(skills)
        processed_jobs.append(job_record)

    # 4. Convert to a Pandas DataFrame
    df = pd.DataFrame(processed_jobs)
    
    # 5. Save the cleaned data to CSV for easy inspection
    output_path = "data/cleaned_jobs.csv"
    df.to_csv(output_path, index=False, encoding="utf-8")
    
    print(f"Success! Transformed {len(df)} jobs and saved to {output_path}")
    print("\nData Preview:")
    # Print the first 3 rows, showing just the title and a few skill columns
    print(df[['title', 'requires_python', 'requires_sql']].head(3))

if __name__ == "__main__":
    transform_jobs()