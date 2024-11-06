from bs4 import BeautifulSoup
import requests
import json
import time

def fetch_articles():
    base_url = "https://scholar.archive.org/search?q=*&filter_availability=microfilm&offset={}"
    offset = 0
    articles_per_page = 15
    articles_found = set()

    try:
        while offset < 2000000:
            response = requests.get(base_url.format(offset), timeout=10)
            response.raise_for_status()  # Raise HTTP errors if any
            soup = BeautifulSoup(response.text, "html.parser")

            current_page_articles = 0
            for a in soup.find_all("a"):
                if 'title' in a.attrs and 'href' in a.attrs:
                    if (a['title'] == 'read fulltext microfilm' or a['title'] == 'fulltext access'):
                        url = a['href']
                        if url not in articles_found:
                            articles_found.add(url)
                            current_page_articles += 1
                    elif a['title'] == 'fulltext PDF download':
                        current_page_articles += 1

            if current_page_articles == 0:
                print(f"No new articles found on page with offset {offset}. Stopping.")
                break

            if current_page_articles < articles_per_page:
                print(f"Less than {articles_per_page} articles found on page with offset {offset}, likely last page.")
                break

            offset += articles_per_page
            time.sleep(1)  # Delay between requests to avoid rate limiting

        return list(articles_found) if articles_found else []

    except requests.exceptions.ConnectionError:
        print("Connection Error")
        return []
    except requests.exceptions.Timeout:
        print("The request timed out.")
        return []
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []


def fetch_full_text(url_list):
    if not url_list:
        print("No URLs found to fetch full text.")
        return {}

    title_to_link = {}
    unique_counter = 1

    for url in url_list:
        try:
            article = requests.get(url, timeout=10)
            article.raise_for_status()
            soup = BeautifulSoup(article.text, "html.parser")

            for a in soup.find_all('a'):
                anchor_text = a.get_text().strip()
                if anchor_text.replace(" ", "") == "FULLTEXTdownload" and 'href' in a.attrs:
                    url = "https://archive.org" + a['href']
                    try:
                        identifier = soup.find('span', itemprop="identifier").get_text()
                        if not identifier:
                            identifier = f"unique-{unique_counter}"
                            unique_counter += 1
                    except AttributeError:
                        identifier = f"unique-{unique_counter}"
                        unique_counter += 1

                    title_to_link[identifier] = url
                    break

        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch article: {url}, error: {e}")

    return title_to_link


def update_value(article_map):
    for key in article_map:
        url = article_map[key]
        if not url.startswith("http"):
            article_map[key] = 'INVALID URL'
            continue

        try:
            full_text = requests.get(url, timeout=10)
            full_text.raise_for_status()
            soup = BeautifulSoup(full_text.text, "html.parser")
            text_content = soup.find('pre')

            if text_content:
                cleaned_text = ' '.join(text_content.get_text().split())
                article_map[key] = cleaned_text
            else:
                article_map[key] = 'FULL TEXT NOT AVAILABLE'

        except requests.exceptions.RequestException:
            article_map[key] = 'REQUEST FAILED'


# Main Execution
article_urls = fetch_articles()

# Check if we have article URLs to process
if article_urls:
    article_map = fetch_full_text(article_urls)
    update_value(article_map)

    with open("data.json", "w") as f:
        json.dump(article_map, f, indent=2)
else:
    print("No articles found.")
