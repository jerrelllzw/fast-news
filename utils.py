import logging
import requests
from scraper import get_eatbook_food_news, get_uniqlo_new_arrivals
from config import TELEGRAM_TOKEN, CHAT_ID

# In-Memory Storage
fast_food_seen = set()
uniqlo_seen = set()
property_seen = set()
bto_seen = set()

# Topics
FAST_FOOD = {"McDonald’s", 'KFC', 'Popeyes', 'Burger King'}
UNIQLO = {}
PROPERTY = {}
BTO = {}

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

    # Uniqlo
    uniqlo_data = get_uniqlo_new_arrivals()
    uniqlo_unseen = [news for news in uniqlo_data if news not in uniqlo_seen]

    if uniqlo_unseen:
        message = "New uniqlo news:\n" + "\n".join(uniqlo_unseen)
        send_telegram_message(message)
        uniqlo_seen.update(uniqlo_unseen)

def parse_data(news_list, test):
    return [news for news in set(news_list) if any(topic in news for topic in test)]
