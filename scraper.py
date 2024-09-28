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
    titles = []
    for post_header in soup.find_all('div', class_='post-header'):
        for h2_tag in post_header.find_all('h2'):
            for a_tag in h2_tag.find_all('a'):
                titles.append(a_tag.get_text(strip=True))

    return titles

def get_uniqlo_new_arrivals():
    # Set up the WebDriver (you need to have a driver like ChromeDriver installed)
    driver = webdriver.Chrome()
    driver.get('https://www.uniqlo.com/sg/en/special-feature/ut/collection-lineup')

    # Let the page load fully
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find the specific div with id lineup_new_arrivals and extract titles under it
    new_arrivals_section = soup.select_one('div#lineup_new_arrivals div.lineup_list')

    titles = []
    if new_arrivals_section:
        for post_header in new_arrivals_section.select('div.lineup_itemBody > div.lineup_itemTtl'):
            titles.append(post_header.get_text(strip=True))

    driver.quit()
    
    return titles
