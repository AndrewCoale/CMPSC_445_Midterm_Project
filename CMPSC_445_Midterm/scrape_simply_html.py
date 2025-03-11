import csv
import time
import traceback
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ✅ Edge WebDriver Setup
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

driver.get('https://www.simplyhired.com/search?q=software+engineer')

# ✅ Save Page Source for Debugging
html_source = driver.page_source
with open("test_page.html", "w", encoding="utf-8") as file:
    file.write(html_source)

print("✅ Page HTML saved. Open test_page.html to check element classes manually.")

# ✅ CSV Setup
csv_filename = "simplyhired_jobs.csv"
header_written = False

pages = 0
max_pages = 200  # Avoid infinite loops

with open(csv_filename, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    if not header_written:
        writer.writerow(["Title", "Company", "Location", "Salary"])
        header_written = True

    while pages < max_pages:
        try:
            # ✅ Increase Wait Time to 30 Seconds
            WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="searchSerpJob"]'))
            )

            job_cards = driver.find_elements(By.CSS_SELECTOR, '[data-testid="searchSerpJob"]')
            for job in job_cards:
                try:
                    title = job.find_element(By.CSS_SELECTOR, '[data-testid="searchSerpJobTitle"]').text.strip()
                    company = job.find_element(By.CSS_SELECTOR, '[data-testid="companyName"]').text.strip()

                    location_elements = job.find_elements(By.CSS_SELECTOR, '[data-testid="searchSerpJobLocation"]')
                    location = location_elements[0].text.strip() if location_elements else "Location not listed"

                    salary_elements = job.find_elements(By.CSS_SELECTOR, '[data-testid="searchSerpJobSalaryConfirmed"]')
                    salary = salary_elements[0].text.strip() if salary_elements else "Salary not listed"

                    writer.writerow([title, company, location, salary])
                    print(f"✅ Saved: {title} - {company} - {location} - {salary}")

                except Exception as job_error:
                    print(f"❌ Error extracting job details: {job_error}")
                    traceback.print_exc()

            # ✅ Find "Next" button
            next_buttons = driver.find_elements(By.CSS_SELECTOR, '[data-testid="pageNumberBlockNext"]')

            if not next_buttons:
                print("✅ No more pages.")
                break

            # ✅ Click Next (scroll to it first)
            driver.execute_script("arguments[0].scrollIntoView();", next_buttons[0])
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(next_buttons[0]))
            next_buttons[0].click()

            pages += 1
            time.sleep(3)

        except Exception as e:
            print(f'❌ An error occurred: {e}')
            traceback.print_exc()
            break

driver.quit()
print(f"✅ Scraping complete. Data saved in {csv_filename}")
