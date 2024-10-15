import requests
from bs4 import BeautifulSoup
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from typing import List, Set

# Constants for URLs
EATBOOK_NEWS_URL = 'https://eatbook.sg/category/news/'
UNIQLO_NEW_ARRIVALS_URL = 'https://www.uniqlo.com/sg/en/special-feature/ut/collection-lineup'
PROPERTY_GURU_URL = 'https://www.propertyguru.com.sg/property-for-rent?market=residential&freetext=Pinnacle+@+Duxton&listing_type=rent&maxprice=6000&property_id=20538&search=true'
HDB_BTO_URL = 'https://homes.hdb.gov.sg/home/finding-a-flat'


def get_soup_from_url(url: str) -> BeautifulSoup:
    """ Fetches content from a URL and returns a BeautifulSoup object. """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"An error occurred while fetching the URL: {url} - {e}")
        return BeautifulSoup("", 'html.parser')
    return BeautifulSoup(response.text, 'html.parser')


def get_soup_from_webdriver(url: str, wait_time: int = 3) -> BeautifulSoup:
    """ Fetches page source using Selenium WebDriver and returns a BeautifulSoup object. """
    with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
        driver.get(url)
        time.sleep(wait_time)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup


def get_eatbook_food_news() -> List[str]:
    """ Scrapes Eatbook's food news and returns a list of titles. """
    soup = get_soup_from_url(EATBOOK_NEWS_URL)
    results = [
        a_tag.get_text(strip=True)
        for post_header in soup.find_all('div', class_='post-header')
        for h2_tag in post_header.find_all('h2')
        for a_tag in h2_tag.find_all('a')
    ]
    return results


def get_uniqlo_new_arrivals() -> List[str]:
    """ Scrapes Uniqlo's new arrivals page using Selenium and returns a list of item titles. """
    soup = get_soup_from_webdriver(UNIQLO_NEW_ARRIVALS_URL)
    new_arrivals_section = soup.select_one('div#lineup_new_arrivals div.lineup_list')
    if not new_arrivals_section:
        return []
    
    results = [
        post_header.get_text(strip=True)
        for post_header in new_arrivals_section.select('div.lineup_itemBody > div.lineup_itemTtl')
    ]
    return results


def get_property_guru_listings() -> List[str]:
    """ Scrapes PropertyGuru's listings and returns a list of listing URLs. """
    soup = get_soup_from_webdriver(PROPERTY_GURU_URL)
    results = [
        listing['href'] for listing in soup.find_all('a', class_='nav-link', itemprop='url')
    ]
    return results


def get_bto_releases() -> Set[str]:
    """ Scrapes HDB's site for upcoming BTO releases. """
    with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
        driver.get(HDB_BTO_URL)
        try:
            upcoming_bto_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'flat-link')]"
                                                      "//div[contains(@class, 'tag-bto') and contains(text(), 'Upcoming BTO')]"))
            )
            upcoming_bto_button.click()
            time.sleep(3)
        except Exception as e:
            logging.error(f"An error occurred while waiting for the BTO button: {e}")
            return set()
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    results = {release.get_text(strip=True) for release in soup.find_all('h2', class_='h6')}
    return results
