import pandas as pd


df = pd.read_excel('saudi_jobs_dataset (2).xlsx')


print(df.shape)
print(df.head())
print(df.info())



print("Duplicates:", df.duplicated().sum())


print("\nMissing values:")
print(df.isnull().sum())


print("\nJob titles:")
print(df['job_title'].value_counts())



def standardize_title(title):
    title = title.lower()
    if 'business analyst' in title or 'business operations' in title:
        return 'Business Analyst'
    elif 'bi analyst' in title or 'business intelligence' in title or 'power bi' in title:
        return 'BI Analyst'
    elif 'data engineer' in title or 'machine learning engineer' in title:
        return 'Data Engineer'
    elif 'data scientist' in title or 'data science' in title:
        return 'Data Scientist'
    elif 'data analyst' in title or 'analytics analyst' in title \
     or 'analytics developer' in title or 'ai analyst' in title:
        return 'Data Analyst'
    else:
        return 'Other'

df['job_category'] = df['job_title'].apply(standardize_title)

print(df['job_category'].value_counts())

print(df[df['job_category'] == 'Other']['job_title'])

print(df['city'].value_counts())

df['city'] = df['city'].str.strip()
df['city'] = df['city'].replace('Makkah, Jeddah', 'Makkah')
print(df['city'].value_counts())

print(df['experience_years'].value_counts().sort_index())

df.to_excel('saudi_jobs_cleaned.xlsx', index=False)
print("Saved!")

print(df['skills'].head(10))

from collections import Counter

all_skills = []

for skills_str in df['skills']:
    skills_list = [s.strip() for s in skills_str.split(',')]
    all_skills.extend(skills_list)

skills_count = Counter(all_skills)
print(skills_count.most_common(15))

print(df['job_category'].value_counts())

print(df['city'].value_counts())

print(df['experience_years'].describe())

print(df.groupby('job_category')['experience_years'].mean().sort_values(ascending=False))

import matplotlib.pyplot as plt

job_counts = df['job_category'].value_counts()

plt.figure(figsize=(10, 6))
plt.bar(job_counts.index, job_counts.values, color='steelblue')
plt.title('Most In-Demand Job Categories in Saudi Arabia')
plt.xlabel('Job Category')
plt.ylabel('Number of Jobs')
plt.tight_layout()
plt.savefig('job_categories.png')
plt.show()



city_counts = df['city'].value_counts()

plt.figure(figsize=(10, 6))
plt.barh(city_counts.index, city_counts.values, color='teal')
plt.title('Job Distribution by City in Saudi Arabia')
plt.xlabel('Number of Jobs')
plt.tight_layout()
plt.savefig('city_distribution.png')
plt.show()


skills_df = pd.DataFrame(skills_count.most_common(10), columns=['Skill', 'Count'])

plt.figure(figsize=(12, 6))
plt.bar(skills_df['Skill'], skills_df['Count'], color='steelblue')
plt.title('Top 10 Most Required Skills in Saudi Tech Market')
plt.xlabel('Skill')
plt.ylabel('Frequency')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('top_skills.png')
plt.show()


plt.figure(figsize=(10, 6))
plt.hist(df['experience_years'], bins=8, color='steelblue', edgecolor='white')
plt.title('Distribution of Required Experience Years')
plt.xlabel('Years of Experience')
plt.ylabel('Number of Jobs')
plt.tight_layout()
plt.savefig('experience_distribution.png')
plt.show()

import sqlite3

conn = sqlite3.connect('saudi_jobs.db')
df.to_sql('jobs', conn, if_exists='replace', index=False)
print("Database created!")

query1 = """
SELECT job_category, COUNT(*) as job_count
FROM jobs
GROUP BY job_category
ORDER BY job_count DESC
"""

result1 = pd.read_sql_query(query1, conn)
print(result1)

query2 = """
SELECT city, COUNT(*) as job_count, 
       ROUND(AVG(experience_years), 1) as avg_experience
FROM jobs
GROUP BY city
ORDER BY job_count DESC
"""

result2 = pd.read_sql_query(query2, conn)
print(result2)

query3 = """
SELECT job_title, company, city, skills
FROM jobs
WHERE experience_years = 0
ORDER BY company
"""

result3 = pd.read_sql_query(query3, conn)
print(result3)