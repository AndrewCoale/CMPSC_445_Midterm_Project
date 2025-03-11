from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import traceback
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By

# Set up the WebDriver
edge_driver_path = "C:\\Users\\admin\\Downloads\\edgedriver_win64\\msedgedriver.exe"
service = Service(edge_driver_path)
options = webdriver.EdgeOptions()

# ✅ User-Agent Spoofing (Prevents Blocking)
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")

# ✅ Open Browser
try:
    driver = webdriver.Edge(service=service, options=options)
except Exception as e:
    print("❌ EdgeDriver failed to start.")
    traceback.print_exc()
    exit()

# Open USAJobs website
url = "https://www.usajobs.gov/Search/Results?l=New%20York&k=software%20engineer"
driver.get(url)
time.sleep(5)  # Allow time for the page to load

# Lists to store data
titles = []
companies = []
locations = []
salaries = []

# Extract job cards
job_cards = driver.find_elements(By.CLASS_NAME, "usajobs-search-result--core__body")

for job in job_cards:
    try:
        title = job.find_element(By.CLASS_NAME, "usajobs-search-result--core__agency").text.strip()
    except:
        title = "N/A"

    try:
        company = job.find_element(By.CLASS_NAME, "usajobs-search-result--core__department").text.strip()
    except:
        company = "N/A"

    try:
        location = job.find_element(By.CLASS_NAME, "usajobs-search-result--core__location").text.strip()
    except:
        location = "N/A"

    try:
        salary = job.find_element(By.CLASS_NAME, "usajobs-search-result--core__details-list").find_element(By.CLASS_NAME, "usajobs-search-result--core__item").text.strip()
    except:
        salary = "N/A"

    titles.append(title)
    companies.append(company)
    locations.append(location)
    salaries.append(salary)

# Close the browser
driver.quit()

# Save to CSV
df = pd.DataFrame({
    "Title": titles,
    "Company": companies,
    "Location": locations,
    "Salary": salaries
})

df.to_csv("usajobs_listings.csv", index=False)
print("Data saved to usajobs_listings.csv")
