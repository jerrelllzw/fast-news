import os
import logging
import requests
from scraper import get_eatbook_food_news, get_uniqlo_new_arrivals, get_property_guru_listings, get_bto_releases
from config import TELEGRAM_TOKEN, CHAT_ID, FAST_FOOD_SEEN_FILE, UNIQLO_SEEN_FILE, PROPERTY_SEEN_FILE
from typing import List, Set

# Helper Functions for File Operations
def read_seen_file(file_path: str) -> Set[str]:
    """Reads seen data from the specified file."""
    if not os.path.exists(file_path):
        return set()
    
    with open(file_path, 'r') as file:
        return set(line.strip() for line in file)

def write_seen_file(file_path: str, new_items: List[str]) -> None:
    """Writes new seen items to the specified file."""
    with open(file_path, 'a') as file:
        for item in new_items:
            file.write(f"{item}\n")

# Telegram Message Sender
def send_telegram_message(message: str) -> None:
    """Sends a message to a specific Telegram chat."""
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': message}
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        logging.info(f"Message sent: {message}")
    except requests.RequestException as e:
        logging.error(f"An error occurred while sending the Telegram message: {e}")

# Notification Helper
def filter_and_notify(data: List[str], file_path: str, title: str, emoji: str) -> None:
    """Filters new items from file-stored seen data and sends notification if there are any unseen."""
    seen_data = read_seen_file(file_path)
    unseen_data = [item for item in data if item not in seen_data]
    
    if unseen_data:
        message = f"{emoji} {title} {emoji}\n\n" + "\n".join([f"⚡ {item}" for item in unseen_data])
        send_telegram_message(message)
        write_seen_file(file_path, unseen_data)
    else:
        logging.info(f"No new {title.lower()} updates to notify.")

# Fast Food Notification
def fetch_and_notify_fast_food() -> None:
    """Fetches fast food news and sends a notification for unseen items."""
    topics = {"McDonald’s", "KFC", "Popeyes", "Burger King"}
    fast_food_data = [news for news in set(get_eatbook_food_news()) if any(topic in news for topic in topics)]
    filter_and_notify(fast_food_data, FAST_FOOD_SEEN_FILE, "Fast Food News", "🍔")

# Uniqlo Notification
def fetch_and_notify_uniqlo() -> None:
    """Fetches Uniqlo new arrivals and sends a notification for unseen items."""
    uniqlo_data = get_uniqlo_new_arrivals()
    filter_and_notify(uniqlo_data, UNIQLO_SEEN_FILE, "Uniqlo New Arrivals", "👕")

# Property Notification
def fetch_and_notify_property() -> None:
    """Fetches property listings and sends a notification for unseen items."""
    property_data = get_property_guru_listings()
    filter_and_notify(property_data, PROPERTY_SEEN_FILE, "Property Listings", "🏠")

# BTO Notification
def fetch_and_notify_bto() -> None:
    """Fetches BTO releases and sends a notification."""
    bto_data = get_bto_releases()

    if bto_data:
        message = "🏢 BTO Releases 🏢\n\n" + "\n".join([f"⚡ {release}" for release in bto_data])
        send_telegram_message(message)
    else:
        logging.info("No new BTO releases to notify.")
