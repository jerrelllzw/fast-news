import requests
from bs4 import BeautifulSoup
import logging
from selenium import webdriver

def get_eatbook_food_news():
    try:
        response = requests.get('https://eatbook.sg/category/news/')
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"An error occurred while fetching the URL: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    results = []
    for post_header in soup.find_all('div', class_='post-header'):
        for h2_tag in post_header.find_all('h2'):
            for a_tag in h2_tag.find_all('a'):
                results.append(a_tag.get_text(strip=True))

    return results

def get_uniqlo_new_arrivals():
    # Scrape using webdriver
    driver = webdriver.Chrome()
    driver.get('https://www.uniqlo.com/sg/en/special-feature/ut/collection-lineup')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    new_arrivals_section = soup.select_one('div#lineup_new_arrivals div.lineup_list')
    driver.quit()

    results = []
    if new_arrivals_section:
        for post_header in new_arrivals_section.select('div.lineup_itemBody > div.lineup_itemTtl'):
            results.append(post_header.get_text(strip=True))

    return results

def get_property_guru_listings():
    try:
        response = requests.get('https://www.propertyguru.com.sg/property-for-sale')
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"An error occurred while fetching the URL: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    results = []
    for listing in soup.find_all('div', class_='listing-card'):
        results.append(listing.get_text(strip=True))

    return results

def get_bto_releases():
    # Scrape using webdriver
    driver = webdriver.Chrome()
    driver.get('https://homes.hdb.gov.sg/home/finding-a-flat')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    results = []
    for release in soup.find_all('div', class_='bto-release'):
        results.append(release.get_text(strip=True))
    print(results)
    return results
