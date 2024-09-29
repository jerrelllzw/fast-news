import logging
import requests
from scraper import get_eatbook_food_news, get_uniqlo_new_arrivals, get_property_guru_listings, get_bto_releases
from config import TELEGRAM_TOKEN, CHAT_ID
from typing import List, Set

# In-Memory Storage
fast_food_seen: Set[str] = set()
uniqlo_seen: Set[str] = set()
property_seen: Set[str] = set()

# Helper Functions
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

def filter_and_notify(data: List[str], seen: Set[str], title: str, emoji: str) -> None:
    """Filters new items from seen data and sends notification if there are any unseen."""
    unseen_data = [item for item in data if item not in seen]
    
    if unseen_data:
        message = f"{emoji}{title}{emoji}\n" + "\n".join([f"• {item}" for item in unseen_data])
        send_telegram_message(message)
        seen.update(unseen_data)
    else:
        logging.info(f"No new {title.lower()} updates to notify.")


def fetch_and_notify_fast_food() -> None:
    """Fetches fast food news and sends a notification for unseen items."""
    topics = {"McDonald’s", "KFC", "Popeyes", "Burger King"}
    fast_food_data = [news for news in set(get_eatbook_food_news()) if any(topic in news for topic in topics)]
    filter_and_notify(fast_food_data, fast_food_seen, "Fast Food News", "🍔")

def fetch_and_notify_uniqlo() -> None:
    """Fetches Uniqlo new arrivals and sends a notification for unseen items."""
    uniqlo_data = get_uniqlo_new_arrivals()
    filter_and_notify(uniqlo_data, uniqlo_seen, "Uniqlo New Arrivals", "👕")

def fetch_and_notify_property() -> None:
    """Fetches property listings and sends a notification for unseen items."""
    property_data = get_property_guru_listings()
    filter_and_notify(property_data, property_seen, "Property Listings", "🏠")

def fetch_and_notify_bto() -> None:
    """Fetches BTO releases and sends a notification."""
    bto_data = get_bto_releases()
    
    if bto_data:
        message = "🏢BTO Releases🏢\n" + "\n".join([f"• {release}" for release in bto_data])
        send_telegram_message(message)
    else:
        logging.info("No new BTO releases to notify.")

# Main Function
def fetch_and_notify() -> None:
    """Fetches data from all sources and sends notifications for new items."""
    fetch_and_notify_fast_food()
    fetch_and_notify_uniqlo()
    fetch_and_notify_property()
    fetch_and_notify_bto()
