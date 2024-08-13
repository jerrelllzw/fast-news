import requests
from bs4 import BeautifulSoup

topics = {"McDonald's", 'KFC', 'Popeyes', 'Burger King'}

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

def parse_food_news(food_news):
    parsed_food_news = set()
    for news in food_news:
        if any(topic in news for topic in topics):
            parsed_food_news.add(news)
    return list(parsed_food_news)

# Main
food_news = get_eatbook_food_news()
parsed_food_news = parse_food_news(food_news)
print(parsed_food_news)