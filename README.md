# Psychology Today Scraper

## Functionality

### `scrape_psychology_today_page(soup)`
- **Purpose:** Scrapes data from a single page of Psychology Today search results.
- **Parameters:** 
  - `soup` (BeautifulSoup object): Parsed HTML content of the web page.
- **Returns:** 
  - `data` (list of lists): List containing therapist information extracted from each profile on the page.
- **Extracted Information:**
  - Name
  - Telephone
  - Location
  - Credentials

#### Detailed Description:
The `scrape_psychology_today_page` function extracts therapist information from a single page of search results on Psychology Today's website. It takes a BeautifulSoup object (`soup`) as input, representing the parsed HTML content of the page. The function locates the container (`div.results`) that holds all therapist profiles. For each profile (`div.results-row`), it extracts:
- **Name:** From `div.results-row-info a.profile-title`.
- **Telephone:** From `div.results-row-contact span.results-row-phone`.
- **Location:** From `div.profile-location`.
- **Credentials:** From `div.profile-subtitle-credentials`.

If any of these elements are not found, the function defaults to "N/A" for that field. The extracted data is stored in a list of lists (`data`), where each sublist represents information for one therapist profile on the page.

The function uses a try-except block to handle exceptions, ensuring smooth operation and error reporting during scraping.

## Dependencies

This project requires the following Python libraries:

- `requests`: To handle HTTP requests for fetching web pages.
- `beautifulsoup4`: For parsing HTML content using BeautifulSoup.
- `pandas`: For data manipulation and creating DataFrames.
- `selenium`: To automate web browser interaction for dynamic content scraping.
- `webdriver_manager`: To manage web drivers for Selenium.

You can install these dependencies using pip:

```bash
pip install requests beautifulsoup4 pandas selenium webdriver_manager