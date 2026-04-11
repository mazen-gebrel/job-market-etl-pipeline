# 📈 Automated Job Market ETL Pipeline

An end-to-end, automated ETL (Extract, Transform, Load) pipeline engineered to track the demand for specific technical skills in the Data Science and Data Engineering job market. 

## 🎯 Business Value
Understanding the job market requires consistent, structured data. This pipeline automatically aggregates live job postings, parses the unstructured text to identify key technical requirements (Python, SQL, AWS, etc.), and loads the structured data into a persistent database. This allows for historical trend analysis of skill demand over time.

## 🏗️ Architecture

The pipeline follows a modular architecture, completely automated via GitHub Actions:

`Live API` ➔ `Extract (Requests)` ➔ `Transform (Pandas/Regex)` ➔ `Load (SQLAlchemy)` ➔ `SQLite Database`

### The Tech Stack
* **Language:** Python 3.10
* **Data Processing:** `pandas`, `regex`
* **Database:** SQLite, `sqlalchemy`
* **Automation & CI/CD:** GitHub Actions
* **Data Source:** Jobicy Remote Jobs API

## ⚙️ How It Works

1. **Extract (`extract.py`):** Queries a public API for the latest 50 remote Data Science, Analytics, and Engineering roles, staging the raw JSON data locally to prevent data loss.
2. **Transform (`transform.py`):** Flattens the nested JSON, strips HTML from descriptions, and engineers new boolean features by scanning the text for core skills (e.g., `requires_sql`, `requires_python`). Outputs a clean CSV.
3. **Load (`load.py`):** Automatically infers the schema and appends the newly cleaned records into a persistent SQLite database (`jobs.db`), ensuring historical data is preserved.
4. **Automation:** A cron job configured in `.github/workflows/etl.yml` spins up a Linux runner every Monday at 8:00 AM UTC, executes the pipeline, and commits the updated database back to the repository.

## 🚀 Running It Locally

If you want to clone this repository and run the pipeline on your local machine:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/mazen-gebrel/job-market-etl-pipeline.git](https://github.com/mazen-gebrel/job-market-etl-pipeline.git)
   cd job-market-etl-pipeline
2. **Install dependencies:**
   ```bash
   pip install requests pandas sqlalchemy
   
3. **Execute the pipeline:**

   ```bash
   python extract.py
   python transform.py
   python load.py

4. **Analyze the data:**
Connect to data/jobs.db using DBeaver, DB Browser for SQLite, or Python to start running SQL aggregations on the job_market_trends table.
