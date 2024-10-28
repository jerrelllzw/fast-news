import logging
import requests
import os
from scraper import get_eatbook_food_news, get_uniqlo_new_arrivals, get_property_guru_listings, get_bto_releases
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, BEN_CHAT_ID, FAST_FOOD_SEEN_FILE, UNIQLO_SEEN_FILE, PROPERTY_SEEN_FILE, BTO_SEEN_FILE
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

# Helper functions for file-based seen tracking
def load_seen_data(file_path: str) -> Set[str]:
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return set(line.strip() for line in f)
    return set()

def save_seen_data(data: Set[str], file_path: str) -> None:
    with open(file_path, 'w') as f:
        for item in data:
            f.write(f"{item}\n")

# Notification Helper
def filter_and_notify(data: List[str], title: str, emoji: str, chat_id: str, file_path: str) -> None:
    seen_data = load_seen_data(file_path)
    unseen_data = [item for item in data if item not in seen_data]
    if unseen_data:
        message = f"{emoji} {title} {emoji}\n\n" + "\n".join([f"⚡ {item} \n" for item in unseen_data])
        if send_telegram_message(message, chat_id):
            seen_data.update(unseen_data)
            save_seen_data(seen_data, file_path)
    else:
        logging.info(f"No new {title.lower()} updates to notify.")

# Fetch and Notify Functions
def fetch_and_notify_fast_food() -> None:
    topics = {"McDonald’s", "KFC", "Popeyes", "Burger King"}
    fast_food_data = [news for news in set(get_eatbook_food_news()) if any(topic in news for topic in topics)]
    filter_and_notify(fast_food_data, "Fast Food News", "🍔", TELEGRAM_CHAT_ID, FAST_FOOD_SEEN_FILE)

def fetch_and_notify_uniqlo() -> None:
    uniqlo_data = get_uniqlo_new_arrivals()
    filter_and_notify(uniqlo_data, "Uniqlo New Arrivals", "👕", TELEGRAM_CHAT_ID, UNIQLO_SEEN_FILE)

def fetch_and_notify_property() -> None:
    property_data = get_property_guru_listings()
    filter_and_notify(property_data, "Property Listings", "🏠", TELEGRAM_CHAT_ID, PROPERTY_SEEN_FILE)

def fetch_and_notify_bto() -> None:
    bto_data = get_bto_releases()
    filter_and_notify(bto_data, "BTO Releases", "🏢", TELEGRAM_CHAT_ID, BTO_SEEN_FILE)
