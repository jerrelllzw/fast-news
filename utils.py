import logging
import requests
from scraper import get_eatbook_food_news, get_uniqlo_new_arrivals, get_property_guru_listings, get_bto_releases
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, BEN_CHAT_ID
from typing import List, Set

# Telegram Message Sender
def send_telegram_message(message: str, chat_id: str) -> bool:
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    data = {'chat_id': chat_id, 'text': message}
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        logging.info(f"Message sent: {message}")
        return True
    except requests.RequestException as e:
        logging.error(f"An error occurred while sending the Telegram message: {e}")
        return False

# Seen Trackers
fast_food_seen = set()
uniqlo_seen = set()
property_seen = set()
bto_seen = set()

# Notification Helper
def filter_and_notify(data: List[str], title: str, emoji: str, chat_id: str, tracker: Set[str]) -> None:
    unseen_data = [item for item in data if item not in tracker]
    if unseen_data:
        message = f"{emoji} {title} {emoji}\n\n" + "\n".join([f"⚡ {item} \n" for item in unseen_data])
        if send_telegram_message(message, chat_id):
            tracker.update(unseen_data)
    else:
        logging.info(f"No new {title.lower()} updates to notify.")

# Fetch and Notify Functions
def fetch_and_notify_fast_food() -> None:
    topics = {"McDonald’s", "KFC", "Popeyes", "Burger King"}
    fast_food_data = [news for news in set(get_eatbook_food_news()) if any(topic in news for topic in topics)]
    filter_and_notify(fast_food_data, "Fast Food News", "🍔", TELEGRAM_CHAT_ID, fast_food_seen)

def fetch_and_notify_uniqlo() -> None:
    uniqlo_data = get_uniqlo_new_arrivals()
    filter_and_notify(uniqlo_data, "Uniqlo New Arrivals", "👕", TELEGRAM_CHAT_ID, uniqlo_seen)

def fetch_and_notify_property() -> None:
    property_data = get_property_guru_listings()
    filter_and_notify(property_data, "Property Listings", "🏠", TELEGRAM_CHAT_ID, property_seen)

def fetch_and_notify_bto() -> None:
    bto_data = get_bto_releases()
    filter_and_notify(bto_data, "BTO Releases", "🏢", TELEGRAM_CHAT_ID, bto_seen)
