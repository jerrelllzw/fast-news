import requests
from bs4 import BeautifulSoup
import logging

# Constants
TOPICS = {"McDonald’s", 'KFC', 'Popeyes', 'Burger King'}
TELEGRAM_TOKEN = ''
CHAT_ID = ''

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# In-Memory Storage
seen_news = set()

# Scrape
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

def parse_news(news_list):
    return [news for news in set(news_list) if any(topic in news for topic in TOPICS)]

# Send Telegram message
def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': message}
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"An error occurred while sending the Telegram message: {e}")

# Main function
def main():
    food_news = parse_news(get_eatbook_food_news())
    new_news = [news for news in food_news if news not in seen_news]

    if new_news:
        message = "New food news:\n" + "\n".join(new_news)
        send_telegram_message(message)
        seen_news.update(new_news)

if __name__ == "__main__":
    main()
