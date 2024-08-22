import logging
import requests
from scraper import get_eatbook_food_news
from config import TELEGRAM_TOKEN, CHAT_ID

# In-Memory Storage
fast_food_seen = set()
uniqlo_seen = set()
property_seen = set()

# Topics
FAST_FOOD = {"McDonald’s", 'KFC', 'Popeyes', 'Burger King', 'Cold Break'}
UNIQLO = {"Uniqlo", "GU"}
PROPERTY = {"property", "HDB", "condo"}

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': message}
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"An error occurred while sending the Telegram message: {e}")

def fetch_and_notify():
    # Fast Food
    fast_food_data = parse_data(get_eatbook_food_news(), FAST_FOOD)
    fast_food_unseen = [news for news in fast_food_data if news not in fast_food_seen]

    if fast_food_unseen:
        message = "New food news:\n" + "\n".join(fast_food_unseen)
        send_telegram_message(message)
        fast_food_seen.update(fast_food_unseen)

def parse_data(news_list, test):
    return [news for news in set(news_list) if any(topic in news for topic in test)]
