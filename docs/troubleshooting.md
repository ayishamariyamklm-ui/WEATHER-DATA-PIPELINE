# Troubleshooting Guide

## Overview

This document helps you debug common issues across the entire Weather Data Pipeline (Advanced Version) including:

- Setup issues
- API errors
- Database problems
- Logging issues
- Pipeline failures
- Dashboard errors

---

## Setup Issues

❌ Problem: Modules not found

ModuleNotFoundError: No module named 'config'

✅ Fix:

Make sure project root is added to path:

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

❌ Problem: Dependencies not installed

✅ Fix:

pip install -r requirements.txt

❌ Problem: Virtual environment not activated

✅ Fix:

# Windows
venv\Scripts\activate

---

## API Issues (api_client.py)

❌ Problem: API request failed

requests.exceptions.RequestException

✅ Fix:

Check internet connection
Verify API URL
Ensure API key is valid

❌ Problem: Empty or invalid response

✅ Fix:

Validate JSON response
Add retry logic (already included)
Check API rate limits

❌ Problem: Timeout error

✅ Fix:

Increase timeout:
requests.get(url, timeout=10)

---

## Validation Issues (validators.py)

❌ Problem: Data rejected

✅ Fix:

Check missing fields
Validate numeric ranges
Print invalid records for debugging

---

## Database Issues (database.py)

❌ Problem: Database not created

✅ Fix:

Run:
python scripts/setup_database.py

❌ Problem: Table not found

sqlite3.OperationalError: no such table

✅ Fix:

Ensure schema.sql is correct
Run init_db.py

❌ Problem: Data not inserted

✅ Fix:

Check DB connection
Verify commit is called
Add debug logs

❌ Problem: Database locked

sqlite3.OperationalError: database is locked

✅ Fix:

Close other connections
Avoid parallel writes
Use retry logic

---

## ETL Pipeline Issues (etl_pipeline.py)

❌ Problem: Pipeline fails

✅ Fix:

Check logs (logs/error.log)
Wrap steps in try-except
Validate API + DB

❌ Problem: No data processed

✅ Fix:

Check city list in config
Ensure API returns data

❌ Problem: Alerts not triggered

✅ Fix:

Verify threshold values in config
Check alert logic in alerts.py

---

## Alerts Issues (alerts.py)

❌ Problem: Alerts not saved

✅ Fix:

Ensure insert_alert() is called
Check DB schema

❌ Problem: Wrong alerts triggered

✅ Fix:

Verify threshold logic
Print values for debugging

---

## Logging Issues (logger.py)

❌ Problem: UnicodeEncodeError (EMOJIS)

UnicodeEncodeError: 'charmap' codec can't encode character

✅ Fix (IMPORTANT):

Remove emojis OR enforce UTF-8:

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler("logs/pipeline.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

OR (simpler)

 Remove emojis from all logger messages 

❌ Problem: Logs not generated

✅ Fix:

Ensure logs folder exists
Check logger setup is called first

---

## Dashboard Issues (dashboard.py)

❌ Problem: Streamlit not recognized

streamlit : command not found

✅ Fix:

python -m streamlit run dashboard/dashboard.py

❌ Problem: Running dashboard using Python

missing ScriptRunContext
❗ Cause:
Wrong command used

✅ Fix:

streamlit run dashboard/dashboard.py

❌ Problem: Timestamp parsing error

ValueError: unconverted data remains

✅ Fix:

pd.to_datetime(column, format="ISO8601")

OR:

pd.to_datetime(column, format="mixed")

❌ Problem: Empty dashboard

✅ Fix:

Run pipeline first
Check database data
Verify queries

---

## Scheduler Issues (scheduler.py)

❌ Problem: Job not running

✅ Fix:

Ensure scheduler is started
Check interval settings

❌ Problem: Multiple runs

✅ Fix:

Avoid duplicate scheduler start
Use singleton pattern

---

## Reporter Issues (reporter.py)

❌ Problem: Report not generated

✅ Fix:

python scripts/generate_report.py

❌ Problem: Empty report

✅ Fix:

Ensure data exists
Check query logic

---

## Monitor Issues (monitor.py)

❌ Problem: Health check fails

✅ Fix:

Verify DB connection
Ensure pipeline runs successfully

---

## Test Failures (tests/)

❌ Problem: Tests failing

✅ Fix:

pytest tests/
Check assertion errors
Debug failing module

---

## Script Issues (scripts/)

❌ Problem: Script not running

✅ Fix:

Ensure correct path
Run from project root

❌ Problem: Import errors in scripts

✅ Fix:

Add:
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

---

## Backup Issues (backup_database.py)

❌ Problem: Backup not created

✅ Fix:

Check file path
Ensure DB exists

---

## General Debugging Tips

✅ Always check logs:

logs/pipeline.log
logs/error.log
logs/alerts.log

✅ Add debug prints/logs:

logger.info("Debugging step")

✅ Run modules independently:

python scripts/run_pipeline.py
python scripts/generate_report.py

✅ Verify data manually:

SELECT * FROM weather_data;
SELECT * FROM alerts;

---

## Still stuck?

- Reinstall dependencies
- Restart VS Code
- Check Python version

---

## Final Checklist

Before running full system:

- Dependencies installed
- Database initialized
- API working
- Pipeline runs successfully
- Logs generated
- Dashboard loads correctly

---

## Summary

This guide helps you debug:

- Setup
- API
- Database
- ETL
- Alerts
- Dashboard
- Tests