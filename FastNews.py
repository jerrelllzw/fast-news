import requests
from bs4 import BeautifulSoup

def get_food_news():
    url = 'https://eatbook.sg/category/news/'  # URL to scrape

    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the URL: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all <div> elements with the class 'post-header' and extract <h2> tags with <a> tags
    item_names = [
        a_tag.get_text(strip=True)
        for post_header in soup.find_all('div', class_='post-header')
        for h2_tag in post_header.find_all('h2')
        for a_tag in h2_tag.find_all('a')
    ]

    return item_names

# Example usage
food_news = get_food_news()
for item in food_news:
    print(item)
