import os
from dotenv import load_dotenv
import logging

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
FAST_FOOD_SEEN_FILE = os.getenv('FAST_FOOD_SEEN_FILE')
UNIQLO_SEEN_FILE = os.getenv('UNIQLO_SEEN_FILE')
PROPERTY_SEEN_FILE = os.getenv('PROPERTY_SEEN_FILE')
