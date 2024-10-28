from utils import fetch_and_notify_fast_food, fetch_and_notify_uniqlo, fetch_and_notify_property, fetch_and_notify_bto

def main():
    """Fetches data from all sources and sends notifications for new items."""
    fetch_and_notify_fast_food()
    fetch_and_notify_uniqlo()
    fetch_and_notify_property()
    # fetch_and_notify_bto()

if __name__ == "__main__":
    main()
