import requests
from bs4 import BeautifulSoup
import logging

# Constants
TOPICS = {"McDonald’s", 'KFC', 'Popeyes', 'Burger King'}
SEEN_NEWS_FILE = 'seen_news.txt'

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Scrape
def get_eatbook_food_news():
    try:
        response = requests.get('https://eatbook.sg/category/news/')
        response.raise_for_status()  # Check if the request was successful
    except requests.RequestException as e:
        logging.error(f"An error occurred while fetching the URL: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract titles from post headers
    titles = []
    for post_header in soup.find_all('div', class_='post-header'):
        for h2_tag in post_header.find_all('h2'):
            for a_tag in h2_tag.find_all('a'):
                titles.append(a_tag.get_text(strip=True))

    return titles

def parse_news(news_list):
    return [news for news in set(news_list) if any(topic in news for topic in TOPICS)]

# File I/O
def load_seen_news(file_path):
    try:
        with open(file_path, 'r') as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def save_seen_news(file_path, news_list):
    with open(file_path, 'a') as f:
        for news in news_list:
            f.write(news + '\n')

# Main
def main():
    seen_news = load_seen_news(SEEN_NEWS_FILE)
    food_news = parse_news(get_eatbook_food_news())

    # Find new news
    new_news = [news for news in food_news if news not in seen_news]

    if new_news:
        logging.info("New food news:")
        for news in new_news:
            logging.info(news)
        # Update the seen titles file
        save_seen_news(SEEN_NEWS_FILE, new_news)
    else:
        logging.info("No new food news found.")

if __name__ == "__main__":
    main()
