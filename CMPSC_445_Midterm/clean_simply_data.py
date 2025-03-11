import pandas as pd
import numpy as np
import re

# Load the CSV file
file_path = "simplyhired_jobs.csv"
df = pd.read_csv(file_path)

# Remove rows where Salary is missing or listed as 'Salary not listed'
df = df.dropna(subset=["Salary"])
df = df[df["Salary"] != "Salary not listed"]

mismatches = 0

# Standardize job titles
def standardize_title(title):
    title_lower = title.lower()
    if "software" in title_lower and "engineer" in title_lower:
        return "Software Engineer"
    elif "backend" in title_lower and "engineer" in title_lower:
        return "Backend Engineer"
    elif "ai" in title_lower and "trainer" in title_lower:
        return "AI Trainer"
    elif "software" in title_lower and ("developer" in title_lower or "dev" in title_lower):
        return "Software Developer"
    elif "backend" in title_lower and ("developer" in title_lower or "dev" in title_lower):
        return "Backend Developer"
    elif "engineer" in title_lower:
        return "Engineer"
    elif "developer" in title_lower or "dev" in title_lower or "programmer" in title_lower:
        return "Developer"
    return title


df["Title"] = df["Title"].apply(standardize_title)


# Add experience level column
def categorize_experience(title):
    title_lower = title.lower()
    if "junior" in title_lower or "jr" in title_lower:
        return "junior"
    elif "senior" in title_lower or "sr" in title_lower:
        return "senior"
    else:
        return "standard"


df["Experience"] = df["Title"].apply(categorize_experience)


# Standardize salary column

def parse_salary(salary):
    if pd.isna(salary):
        return np.nan

    salary = salary.lower().replace(",", "")

    # Hourly wages
    if "hour" in salary:
        match = re.search(r"\$?([0-9]+)\s?an hour", salary)
        if match:
            return float(match.group(1)) * 2080  # Convert to yearly salary

    # Salary ranges
    match = re.findall(r"\$([0-9]+(?:\.?[0-9]*))", salary)
    if len(match) == 2:
        return (float(match[0]) + float(match[1])) / 2  # Average the range
    elif len(match) == 1:
        return float(match[0])

    return np.nan


df["Salary"] = df["Salary"].apply(parse_salary)

# Save cleaned data
df.to_csv("cleaned_jobs.csv", index=False)
print("Data cleaning complete. Processed file saved as 'cleaned_jobs.csv'.")

