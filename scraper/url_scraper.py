import requests
from bs4 import BeautifulSoup

def fetch_url_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        if 'pdf' in url.lower():
            return 'PDF is still not supported!'

        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = soup.find('pre')  # Assuming text is in a <pre> tag
        if text_content:
            cleaned_text = ' '.join(text_content.get_text().split())
            return cleaned_text

        return "No text content available."

    except requests.exceptions.RequestException as e:
        return f"Error fetching content from {url}: {e}"