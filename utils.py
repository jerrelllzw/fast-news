import logging
import requests
from scraper import get_eatbook_food_news
from config import TELEGRAM_TOKEN, CHAT_ID

# In-Memory Storage
seen = set()

# Topics
FAST_FOOD = {"McDonald’s", 'KFC', 'Popeyes', 'Burger King', 'Cold Break'}
# instagram ut colleection
# property prices

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': message}
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"An error occurred while sending the Telegram message: {e}")

def fetch_and_notify():
    food_news = parse_news(get_eatbook_food_news(), FAST_FOOD)
    unseen = [news for news in food_news if news not in seen]

    if unseen:
        message = "New food news:\n" + "\n".join(unseen)
        send_telegram_message(message)
        seen.update(unseen)

def parse_news(news_list, test):
    return [news for news in set(news_list) if any(topic in news for topic in test)]
