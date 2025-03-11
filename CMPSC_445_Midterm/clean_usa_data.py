import pandas as pd
import re

# Load the CSV file
df = pd.read_csv("usajobs_listings.csv")

# Update job titles to "Government Engineer"
df["Title"] = "Government Engineer"

# Convert location to "New York, NY" if it contains "NY", otherwise "Remote"
df["Location"] = df["Location"].apply(lambda x: "New York, NY" if "New York" in x else "Remote")

# Function to extract salary as a decimal number
def extract_salary(salary_text):
    match = re.search(r"\$([\d,]+)", salary_text)
    if match:
        return float(match.group(1).replace(",", ""))
    return None  # Return None if no salary found

# Apply salary extraction
df["Salary"] = df["Salary"].apply(extract_salary)

df["Experience"] = "standard"

# Append the cleaned data to the simplyhired cleaned data
df.to_csv('cleaned_jobs.csv', mode='a', header=False, index=False)

print("Data cleaned and saved to cleaned_jobs.csv")
