import logging
from scraper import get_eatbook_food_news, parse_news
from utils import send_telegram_message

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# In-Memory Storage
seen = set()

def main():
    food_news = parse_news(get_eatbook_food_news())
    unseen = [news for news in food_news if news not in seen]

    if unseen:
        message = "New food news:\n" + "\n".join(unseen)
        send_telegram_message(message)
        seen.update(unseen)

if __name__ == "__main__":
    main()
