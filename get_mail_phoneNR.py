import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import time
import difflib
import re
import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

start_time = time.time()

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--diable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options= chrome_options
    )
driver.set_page_load_timeout(30)
wait = WebDriverWait(driver, 20)


file_path = "selskaper_ 2025-05-24__MED_kommune.xlsx"      #open file with previously gathered information and read it into a list, which will be used to scrape 180.no and gulesider.no
df = pd.read_excel(file_path)



def excel_to_list():
    company_info_list = []
    for _, row in df.iterrows():
        selskap = row["Selskapsnavn"].strip()
        kommune = row["kommune"].strip()
        daglig_leder = row["Navn"].strip()
                                                                        #turns data from excel file into a list

        if selskap and daglig_leder:
            company_info = {
            "selskap" : selskap,
            "kommune" : kommune,
            "daglig_leder" : daglig_leder,
            "phone_number" : ""
            }

            company_info_list.append(company_info)
    return company_info_list

company_info_list = excel_to_list()                                    #saves the data into variable



def create_search_list_180(company_info_list):
    time.sleep(random.uniform(1.5, 3.0))
    urls_to_search = []
    for company in company_info_list:
        if company["daglig_leder"] and company["kommune"]:                              #combines name of daglig leder and kommune to create search queries for 180.no 
            cleaned_name = company["daglig_leder"].lower().replace(" ", "-")
            cleaned_kommune = company["kommune"].lower().replace(" ", "-")
            url_query = f"{cleaned_name}--{cleaned_kommune}"
            urls_to_search.append(url_query)
    return urls_to_search

urls_to_search = create_search_list_180(company_info_list)                               #saves search queries in a list


def normalize_text(text):
    return ''.join(e for e in text.lower() if e.isalnum())

def safe_driver_get(driver, url, retries=3, delay=5):                           #fcuntion for better handling of driver.get
    for attempt in range(retries):
        try:
            driver.get(url)
            return True
        except Exception as e:
            print(f"[Retry {attempt + 1} / error fetching {url}: {e}]")
    return False


def autosave_results(df, company_list_info, index):
    autosave_file = f"selskaper_autosave_row_{index}.xlsx"
    for i, company in enumerate(company_info_list):
        df.at[i, "phone_number"] = company.get("phone_number", "")
    df.to_excel(autosave_file, index=False)
    print(f"[Autosave] saved partial results to file: {autosave_file}")


def validate_chromedriver(driver):
    try:
        _ = driver.title
        return True
    except Exception as e:
        print(f"[FATAL] chromdriver is no longer responding: {e}")
        return False



start = 1370
end = 1380
driver.get("https://www.180.no/")

if driver.title:

    try:
        accept_cookie_button = wait.until(EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button")))
        accept_cookie_button.click()
        time.sleep(random.uniform(1, 2.5))
                
    except Exception as e:
        print("No cookie popup found or button was not found", e)


#for index, url in enumerate(urls_to_search[start:end], start=start):           #For testing code with a lot of data. 


for index, url in enumerate(urls_to_search):

    print("retrieveing info from index:", index, url)
    if not url:
        continue
    
    base_url = "https://www.180.no/search/all?w="
    search_url = base_url + quote_plus(url)
    
    try:
        if not safe_driver_get(driver, search_url):
            print("driver failed to load url. Skip to next url")
            continue

        if not validate_chromedriver(driver):
            print("chromedriver is broken, exit script")
            break
        
        """driver.get(search_url)                                                #fetch the page and wait for popup to appear.
        time.sleep(random.uniform(1, 2.5))"""

        """try:
            accept_cookie_button = wait.until(EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button")))
            accept_cookie_button.click()
            time.sleep(random.uniform(1, 2.5))
            
        except Exception as e:
            print("No cookie popup found or button was not found", e)"""

        if "180.no har 0 treff" in driver.title:
                print(f"No results found for {url}")
                continue
        
        try:
            company_name = company_info_list[index]["selskap"]
            company_name_without_AS = re.sub(r'\s*A/?S$', '', company_name, flags=re.IGNORECASE).strip()
            company_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href*="firmavis/"]')))

            best_match = None
            highest_score = 0
            target_for_comparison = normalize_text(company_name_without_AS)

            #matched_link_with_company_name = None

            for link in company_links:
                raw_link_text = link.text.strip()
                link_text = raw_link_text.replace("Infoside", "").strip()
                print(link_text)
                if not link_text:
                    continue

                candidate = normalize_text(link_text)
                similarity = difflib.SequenceMatcher(None, target_for_comparison, candidate).ratio()
                print(f"comparing '{link_text}' with '{company_name_without_AS}' Score: {similarity:.2f}")
                
                if similarity > highest_score:
                    highest_score = similarity
                    best_match = link

                """if normalize_text(company_name) in normalize_text(link_text) or normalize_text(link_text) in normalize_text(company_name):
                    matched_link_with_company_name = link
                    break"""

            if best_match and highest_score >= 0.85:
                company_page_href = best_match.get_attribute("href")
                print(f"Opening company page {company_page_href} that matches {company_name_without_AS}")
                driver.get(company_page_href)
                time.sleep(random.uniform(1, 2.5))
            else:
                print(f"No match found for {company_name_without_AS}")
                continue

        except Exception as e:
            print(f"Error fetching company page or did not find matching company link {e}")
            continue


        
        """try:
            link_to_company_page = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href*="firmavis/"]')))

            company_page_href = link_to_company_page.get_attribute("href")
            print("Opening next page:", link_to_company_page.get_attribute("href"))
            driver.get(company_page_href)
    
        except Exception as e:
            print("No company page link found", e)
            raise"""

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href^="/person/"]')))      

            print("page title:", driver.title)
            #print("current_url", driver.current_url)
            link_to_person = driver.find_elements(By.CSS_SELECTOR, 'a[href^="/person/"]')
            
            if len(link_to_person) > 1:
                name_for_matching = normalize_text(company_info_list[index]["daglig_leder"])

                for person in link_to_person:
                    person_text = normalize_text(person.text.strip())
                    print(person_text)

                    if person_text == name_for_matching:
                        print("clicking link:", person.get_attribute("href"))
                        person.click()
                        WebDriverWait(driver, 5)
                    else:
                        print(f"No links matching name: {name_for_matching} found")
                        continue
            elif len(link_to_person) == 1:
                print("clicking link:", link_to_person[0].get_attribute("href"))
                link_to_person[0].click()
            else:
                print("didnt find any further links")

        except Exception as e:
            print("no links to person page found", e)

        try:            
            if driver.title:
                print(driver.title)

                retrieve_number_and_name = []
                for item in driver.title.split(","):
                    retrieve_number_and_name.append(item)
                print("page title:", retrieve_number_and_name)

                name_or_company = retrieve_number_and_name[0]

                if normalize_text(name_or_company) == normalize_text(company_info_list[index]["daglig_leder"]):

                    phone_number = None

                    for item in retrieve_number_and_name[1:]:
                        cleaned = item.strip().replace(" ", "")

                        #checking for phone number using regex
                        if re.fullmatch(r"(\+47)?\d{8,}", cleaned):
                            phone_number = cleaned
                            break

                    if phone_number:
                        company_info_list[index]["phone_number"] = phone_number
                        print(f"[{index+1}] found the number of: {name_or_company}")
                    else:
                        print(f"found no phone number for {driver.title}")
                else:
                    print(f"name: {normalize_text(name_or_company)} did not match: {normalize_text(company_info_list[index]['daglig_leder'])}")
            else:
                print(f"[{index+1}] couldnt find anything in driver.title. possibly 404 error")
                

        except Exception as e:
            print("Error:", e)
            continue

        if index > 0 and index % 50 ==0:
            autosave_results(df, company_info_list, index)
            print(f"autosaved results at index: {index}")
            time.sleep(random.uniform(40, 45))


            """autosave_file = f"selskaper_autosave_row_{index}.xlsx"
            for i, company in enumerate(company_info_list):
                df.at[i, "phone_number"] = company.get("phone_number", "")
            df.to_excel(autosave_file, index=False)
            print(f"saving partial results on every 50 row, to {autosave_file}")
            print(f"autosaving triggered at row {index}")

            time.sleep(random.uniform(40, 45))"""

            
            
            """phone_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//img[contains(@class, "cc-number-icon")]/following-sibling::span')))
            phone_number = phone_element.text().strip(" ", "")
            #print(type("phone number:", driver.title))              #mulig å bruke driver.title når man er på riktig side fordi den inneholder navn og telefonnummer. dette må sjekkes.
            #print("phone_number: ", phone_number)

            if phone_number:
                print("phone_number: ", phone_number)"""
            
        
    except Exception as e:
        print("Error", e)
        print("page title:", driver.title)
        print("current_url", driver.current_url)
    
for i, company in enumerate(company_info_list):
    df.at[i, "phone_number"] = company.get("phone_number", "")

output_file = "selskaper_with_numbers_2025-05-24_4.xlsx"
df.to_excel(output_file, index=False)
print(f"fil lagret til {output_file}")

driver.quit()

end_time = time.time()
total_time = end_time - start_time

print(f"total runtime for script: {total_time:.2f} seconds")