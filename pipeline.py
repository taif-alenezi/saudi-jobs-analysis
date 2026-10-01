import sqlite3

import pandas as pd

RAW_PATH = "data/raw/saudi_jobs_raw.xlsx"
PROCESSED_CSV = "data/processed/saudi_jobs_clean.csv"
DB_PATH = "data/processed/saudi_jobs.db"


def extract(path):
    df = pd.read_excel(path)
    print(f"Extracted {len(df)} rows and {df.shape[1]} columns")
    return df


def profile(df):
    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate rows:", df.duplicated().sum())

    print("\nCities:")
    print(df["city"].value_counts())

    print("\nJob types:")
    print(df["job_type"].value_counts())

    skills = df["skills"].dropna().str.split(",").explode().str.strip()
    print("\nUnique skills:")
    print(sorted(skills.unique()))


def standardize_title(title):
    title = title.lower()
    if "business analyst" in title or "business operations" in title:
        return "Business Analyst"
    elif "bi analyst" in title or "business intelligence" in title or "power bi" in title:
        return "BI Analyst"
    elif "data engineer" in title or "machine learning engineer" in title:
        return "Data Engineer"
    elif "data scientist" in title or "data science" in title:
        return "Data Scientist"
    elif "data analyst" in title or "analytics" in title or "analyst" in title:
        return "Data Analyst"
    else:
        return "Other"


def transform(df):
    df = df.copy()

    text_cols = ["job_title", "company", "city", "job_type", "skills", "source"]
    for col in text_cols:
        df[col] = df[col].str.strip()

    df["city"] = df["city"].replace("Makkah, Jeddah", "Makkah")

    df["job_category"] = df["job_title"].apply(standardize_title)

    df["date_collected"] = pd.to_datetime(df["date_collected"], dayfirst=True)

    before = len(df)
    df = df.drop_duplicates(subset=["job_title", "company"])
    print(f"Removed {before - len(df)} duplicate postings")

    return df


def quality_checks(df):
    checks = {
        "No missing job titles": df["job_title"].notna().all(),
        "No duplicate postings": not df.duplicated(subset=["job_title", "company"]).any(),
        "All jobs categorized": (df["job_category"] != "Other").all(),
        "Experience is not negative": (df["experience_years"] >= 0).all(),
        "All dates are valid": df["date_collected"].notna().all(),
    }

    print("\nQuality checks:")
    for name, passed in checks.items():
        status = "PASS" if passed else "FAIL"
        print(f"{status}: {name}")

    conflicts = df[(df["city"] == "Remote") & (df["job_type"] != "Remote")]
    print(f"\nCity / job type conflicts: {len(conflicts)}")
    if len(conflicts) > 0:
        print(conflicts[["job_title", "city", "job_type"]])

    return all(checks.values())


def load(df):
    df.to_csv(PROCESSED_CSV, index=False)
    print(f"\nSaved clean data to {PROCESSED_CSV}")

    conn = sqlite3.connect(DB_PATH)
    df.to_sql("jobs", conn, if_exists="replace", index=False)
    count = pd.read_sql("SELECT COUNT(*) AS n FROM jobs", conn)["n"][0]
    conn.close()
    print(f"Loaded {count} rows into {DB_PATH}")


if __name__ == "__main__":
    raw_df = extract(RAW_PATH)
    clean_df = transform(raw_df)
    passed = quality_checks(clean_df)

    if passed:
        load(clean_df)
    else:
        print("\nLoad skipped: fix the failed checks first.")