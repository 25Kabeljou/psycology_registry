from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

def setup_driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scrape_profile_page(profile_url, driver):
    try:
        driver.get(profile_url)
        time.sleep(2)  # Increased wait time
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        email_tag = soup.find('a', href=lambda x: x and x.startswith('mailto:'))
        email = email_tag.text.strip() if email_tag else "N/A"
        return email
    except Exception as e:
        print(f"Error scraping profile page {profile_url}: {e}")
        return "N/A"

def scrape_therapist_directory(base_url):
    driver = setup_driver()
    driver.get(base_url)
    time.sleep(5)  # Increased wait time

    therapist_list = []

    while True:
        print("Scraping current page...")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        listings = soup.find_all('div', class_='sub-blck txt-blck col-12 col-sm-8 col-xl-9')

        if not listings:
            print("No more listings found.")
            break

        for listing in listings:
            try:
                name_tag = listing.find('h3', class_='blck-ttl strng').find('a')
                name = name_tag.text.strip()
                url = name_tag['href']
                credentials = listing.find('p', class_='lstng-spclty').text.strip()
                location = listing.find('p', class_='lstng-lctn pt-0 h4 strng').text.strip()

                profile_url = url
                email = scrape_profile_page(profile_url, driver)

                therapist_list.append([name, credentials, location, profile_url, email])
            except Exception as e:
                print(f"Error processing listing: {e}")

        # Save current data to avoid data loss
        if therapist_list:
            try:
                df = pd.DataFrame(therapist_list, columns=['Name', 'Credentials', 'Location', 'Profile URL', 'Email'])
                file_path = 'therapist_directory.xlsx'

                with pd.ExcelWriter(file_path, mode='a', if_sheet_exists='overlay', engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, header=not writer.sheets, startrow=writer.sheets['Sheet1'].max_row if 'Sheet1' in writer.sheets else 0)
                therapist_list.clear()
                print(f"Data appended to '{file_path}'")
            except Exception as e:
                print(f"Error saving data to Excel: {e}")

        # Click the "Load More" button to load more therapists
        try:
            load_more_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.facetwp-load-more'))
            )
            driver.execute_script("arguments[0].click();", load_more_button)
            print("Clicked 'Load more' button")
            time.sleep(15)  # Increased wait time
        except Exception as e:
            print("No more 'Load more' button found or error clicking it.")
            break

    driver.quit()

if __name__ == "__main__":
    base_url = 'https://www.therapist-directory.co.za/listings/'
    scrape_therapist_directory(base_url)
    scrape_therapist_directory(base_url)
    scrape_therapist_directory(base_url)
    scrape_therapist_directory(base_url)