# Saudi Tech Job Market Analysis 2026

## Overview
I collected and analyzed 49 data-related job postings from LinkedIn and Jadarat across Saudi Arabia in May 2026. The goal was simple — instead of guessing what the job market looks like, I wanted real numbers to guide my career decisions as a fresh graduate.

## What I Found
- Riyadh dominates the market with 80% of all tech jobs
- SQL and Python appear in 80% and 63% of job postings — making them non-negotiable skills
- Data Analyst is the most in-demand role with 16 out of 49 postings
- 1 in 4 jobs requires zero experience — good news for fresh graduates
- Power BI is the go-to visualization tool in the Saudi market, ahead of Tableau

## Tools Used
- Python — pandas, matplotlib, collections
- SQL — SQLite via Python
- Excel — data collection and formatting

## Project Files
```
saudi-jobs-project/
├── data/
│   ├── raw/
│   │   └── saudi_jobs_raw.xlsx
│   └── processed/
│       ├── saudi_jobs_clean.csv
│       └── saudi_jobs.db
├── pipeline.py
├── analysis.py
├── job_categories.png
├── city_distribution.png
├── top_skills.png
└── experience_distribution.png
```

## Data Pipeline

I rebuilt the data preparation as a separate ETL pipeline (`pipeline.py`), so the analysis always runs on clean, verified data.

Run it with:

    python pipeline.py

Steps:
1. **Extract:** reads the raw file from `data/raw/`. The raw file is never edited.
2. **Transform:** trims text, fixes city entries, groups job titles into 5 categories, and converts dates.
3. **Validate:** runs 5 quality checks (missing titles, duplicates, uncategorized jobs, negative experience, invalid dates). It also flags conflicts between the city and job type columns.
4. **Load:** only if all checks pass, saves the clean data to `data/processed/` as a CSV file and a SQLite database.

## Data Dictionary

| Column | Type | Description |
| --- | --- | --- |
| job_title | Text | Job title as written in the posting |
| company | Text | Hiring company |
| city | Text | City of the job, or "Remote" |
| experience_years | Number | Minimum years of experience. If a range was given, I used the lower bound. If not stated, 0 |
| job_type | Text | Full-time, Hybrid, or Remote |
| skills | Text | Technical skills only, comma separated |
| salary | Text | Salary if listed |
| source | Text | Where the posting was found: LinkedIn or Jadarat |
| date_collected | Date | Date I collected the posting |
| job_category | Text | Added by the pipeline. One of 5 groups: Data Analyst, Data Engineer, Data Scientist, Business Analyst, BI Analyst |

## Data Notes

- All 49 postings were collected manually from public job listings. No personal data was collected.
- Salary is missing in 44 of 49 postings (about 90%), so it was kept but not analyzed.
- One posting listed two cities ("Makkah, Jeddah"). I kept it as Makkah.
- The job_type column mixes contract type (Full-time) and work location (Remote, Hybrid). One posting is both full-time and remote. In a future version, I would split this into two columns.
- This is a small sample collected over a short period, so it shows a snapshot of the market, not the full picture.


## About
**Taif Sultan Alenezi** — Computer Science Graduate 2026
[GitHub](https://github.com/taif-alenezi)