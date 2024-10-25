import requests
from bs4 import BeautifulSoup


def get_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        text = text.replace("\t", "").replace("\n", "")
        if text:
            return text
        else:
            return -1

    except Exception as e:
        return -1



