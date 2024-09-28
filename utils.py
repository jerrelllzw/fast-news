import logging
import requests
from scraper import get_eatbook_food_news, get_uniqlo_new_arrivals, get_property_guru_listings, get_bto_releases
from config import TELEGRAM_TOKEN, CHAT_ID

# In-Memory Storage
fast_food_seen = set()
uniqlo_seen = set()
property_seen = set()
bto_seen = set()

# Helper Functions
def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': message}
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"An error occurred while sending the Telegram message: {e}")

def fetch_and_notify_fast_food():
    fast_food_data = [news for news in set(get_eatbook_food_news()) if any(topic in news for topic in {"McDonald’s", 'KFC', 'Popeyes', 'Burger King'})]
    fast_food_unseen = [news for news in fast_food_data if news not in fast_food_seen]

    if fast_food_unseen:
        message = "Fast Food News:\n" + "\n".join(fast_food_unseen)
        send_telegram_message(message)
        fast_food_seen.update(fast_food_unseen)

def fetch_and_notify_uniqlo():
    uniqlo_data = get_uniqlo_new_arrivals()
    uniqlo_unseen = [arrivals for arrivals in uniqlo_data if arrivals not in uniqlo_seen]

    if uniqlo_unseen:
        message = "Uniqlo New Arrivals:\n" + "\n".join(uniqlo_unseen)
        send_telegram_message(message)
        uniqlo_seen.update(uniqlo_unseen)

def fetch_and_notify_property():
    property_data = get_property_guru_listings()
    property_unseen = [listings for listings in property_data if listings not in property_seen]

    if property_unseen:
        message = "Property Listings:\n" + "\n".join(property_unseen)
        send_telegram_message(message)
        uniqlo_seen.update(property_unseen)

def fetch_and_notify_bto():
    bto_data = get_bto_releases()
    bto_unseen = [releases for releases in bto_data if releases not in bto_seen]

    if bto_unseen:
        message = "BTO Releases:\n" + "\n".join(bto_unseen)
        send_telegram_message(message)
        bto_seen.update(bto_unseen)


# Main Function
def fetch_and_notify():
    # fetch_and_notify_fast_food()
    # fetch_and_notify_uniqlo()
    # fetch_and_notify_property()
    fetch_and_notify_bto()