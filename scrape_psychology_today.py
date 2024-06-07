import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Function to scrape data from a single page
def scrape_psychology_today_page(soup):
    data = []
    try:
        results = soup.find('div', class_='results')  # Find the 'results' container
        if results:
            profiles = results.find_all('div', class_='results-row')  # Find all profile rows within 'results'
            for profile in profiles:
                # Extracting name
                name_tag = profile.find('div', class_='results-row-info').find('a', class_='profile-title')
                name = name_tag.text.strip() if name_tag else "N/A"

                # Extracting location
                location_tag = profile.find('div', class_='profile-location')
                location = location_tag.text.strip() if location_tag else "N/A"

                # Extracting telephone from results-row-contact
                contact_tag = profile.find('div', class_='results-row-contact')
                if contact_tag:
                    telephone_tag = contact_tag.find('span', class_='results-row-phone')
                    telephone = telephone_tag.text.strip() if telephone_tag else "N/A"
                else:
                    telephone = "N/A"

                # Extracting credentials
                credentials_tag = profile.find('div', class_='profile-subtitle-credentials')
                credentials = credentials_tag.text.strip() if credentials_tag else "N/A"

                data.append([name, telephone, location, credentials])
        else:
            print("No 'results' found on the page.")
    except Exception as e:
        print(f"Error scraping page: {e}")

    return data


# Function to set up Selenium WebDriver
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run Chrome in headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


# Main scraping function
def scrape_psychology_today():
    base_url = 'https://www.psychologytoday.com/za/counselling/western-cape?gad_source=1&gclid=CjwKCAjw34qzBhBmEiwAOUQcF-He8jKjI85vy5mw8PjjeOsXA1zM4Tps4iDW4jHgrwgRL3tLKgz9-xoCxjkQAvD_BwE&page='
    driver = setup_driver()
    all_data = []

    try:
        for page in range(1, 11):  # Adjust range for the number of pages you want to scrape
            url = base_url + str(page)
            driver.get(url)
            time.sleep(3)  # Wait for the page to load
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            page_data = scrape_psychology_today_page(soup)
            all_data.extend(page_data)
            print(f"Scraped page {page}")
    except Exception as e:
        print(f"Error scraping page {page}: {e}")
    finally:
        driver.quit()

    # Save data to Excel
    if all_data:
        # Create a DataFrame
        df = pd.DataFrame(all_data, columns=['Name', 'Telephone', 'Location', 'Credentials'])

        # Specify the Excel file path
        file_path = 'psychology_today_therapists.xlsx'
        sheet_name = 'Psychology Today Therapists'

        # Use ExcelWriter to write data to separate columns
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name=sheet_name)
            writer._save()

        print(f"Data saved to '{file_path}'")

# Call the main scraping function
scrape_psychology_today()