import requests
from bs4 import BeautifulSoup
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters

# Constants
TOPICS = {"McDonald’s", 'KFC', 'Popeyes', 'Burger King'}
SEEN_NEWS_FILE = 'seen_news.txt'
TELEGRAM_TOKEN = ''

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Store user chat IDs
user_chat_ids = set()

# Scrape
def get_eatbook_food_news():
    try:
        response = requests.get('https://eatbook.sg/category/news/')
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"An error occurred while fetching the URL: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract titles from post headers
    titles = []
    for post_header in soup.find_all('div', class_='post-header'):
        for h2_tag in post_header.find_all('h2'):
            for a_tag in h2_tag.find_all('a'):
                titles.append(a_tag.get_text(strip=True))

    return titles

def parse_news(news_list):
    return [news for news in set(news_list) if any(topic in news for topic in TOPICS)]

# File I/O
def load_seen_news(file_path):
    try:
        with open(file_path, 'r') as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def save_seen_news(file_path, news_list):
    try:
        with open(file_path, 'a') as f:
            for news in news_list:
                f.write(news + '\n')
    except IOError as e:
        logging.error(f"An error occurred while writing to the file: {e}")

# Send Telegram message to all users
async def send_telegram_message(application: Application, message: str):
    for chat_id in user_chat_ids:
        try:
            await application.bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            logging.error(f"An error occurred while sending the Telegram message: {e}")

# Handle /start command
async def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    user_chat_ids.add(chat_id)
    await update.message.reply_text("Welcome! You're now subscribed to food news updates.")

# Handle new messages
async def handle_message(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    user_chat_ids.add(chat_id)
    await update.message.reply_text("You're now subscribed to food news updates.")

# Main
async def main():
    global user_chat_ids
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Load seen news and start updates loop
    seen_news = load_seen_news(SEEN_NEWS_FILE)
    food_news = parse_news(get_eatbook_food_news())
    new_news = [news for news in food_news if news not in seen_news]

    if new_news:
        message = "New food news:\n" + "\n".join(new_news)
        await send_telegram_message(application, message)
        save_seen_news(SEEN_NEWS_FILE, new_news)
    else:
        await send_telegram_message(application, "No new food news found.")

    # Run the bot
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
