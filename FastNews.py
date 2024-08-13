import requests
from bs4 import BeautifulSoup

topics = {"McDonald’s", 'KFC', 'Popeyes', 'Burger King'}
seen_news_file = 'seen_news.txt'

# Scrape
def get_eatbook_food_news():
    try:
        response = requests.get('https://eatbook.sg/category/news/')
        response.raise_for_status()  # Check if the request was successful
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the URL: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract titles from post headers
    titles = [
        a_tag.get_text(strip=True)
        for post_header in soup.find_all('div', class_='post-header')
        for h2_tag in post_header.find_all('h2')
        for a_tag in h2_tag.find_all('a')
    ]

    return titles

def parse_news(newsList):
    parsed_news = set()
    for news in newsList:
        if any(topic in news for topic in topics):
            parsed_news.add(news)
    return list(parsed_news)

# File I/O
def load_seen_news(file_path):
    try:
        with open(file_path, 'r') as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def save_seen_news(file_path, newsList):
    with open(file_path, 'a') as f:
        for news in newsList:
            f.write(news + '\n')

# Main
def main():
    seen_news = load_seen_news(seen_news_file)
    food_news = parse_news(get_eatbook_food_news())

    # Find new news
    new_news = [news for news in food_news if news not in seen_news]

    if new_news:
        print("New food news:")
        print("\n".join(new_news))
        # Update the seen titles file
        save_seen_news(seen_news_file, new_news)
    else:
        print("No new food news found.")

if __name__ == "__main__":
    main()
