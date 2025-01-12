import requests
from bs4 import BeautifulSoup


def get_latest_news():
    response = requests.get("https://fmi-plovdiv.org/news.jsp?ln=1&id=2")
    soup = BeautifulSoup(response.text, 'html.parser')
    a_tags = soup.find_all('a')
    links = [{'text': tag.get_text(strip=True), 'href': tag.get('href')}
             for tag in a_tags if tag.get('href') and
             tag.get('href').startswith('news.jsp') and 'newsPageNumber' in tag.get('href')]
    print("Response JSON:", links)
    return links