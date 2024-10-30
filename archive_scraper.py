from bs4 import BeautifulSoup
import requests


def fetch_articles():
    base_url = "https://scholar.archive.org/search?q=*&offset={}"
    offset = 0
    articles_per_page = 15
    articles_found = set()

    try:
        while True:
            internet_archive_scholar = requests.get(base_url.format(offset))
            internet_archive_scholar.raise_for_status()

            soup = BeautifulSoup(internet_archive_scholar.text, "html.parser")

            current_page_articles = 0

            for a in soup.find_all("a"):
                if 'title' in a.attrs and (a['title'] == 'read fulltext microfilm' or a[
                    'title'] == 'fulltext access') and 'href' in a.attrs:
                    url = a['href']
                    if url not in articles_found:
                        articles_found.add(url)
                        current_page_articles += 1

            if current_page_articles == 0:
                print(f"No new articles found on page with offset {offset}. Stopping.")
                break

            if current_page_articles < articles_per_page:
                print(f"Less than {articles_per_page} articles found on page with offset {offset}, likely last page.")
                break

            # Move to the next page
            offset += articles_per_page

        return articles_found

    except requests.exceptions.ConnectionError:
        print("Connection Error")
    except requests.exceptions.Timeout:
        print("The request timed out.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def fetch_full_text(url_list):
    title_to_link = {}

    for url in url_list:
        article = requests.get(url)
        soup = BeautifulSoup(article.text, "html.parser")

        for a in soup.find_all('a'):
            anchor_text = a.get_text().strip()

            if anchor_text.replace(" ", "") == "FULLTEXTdownload":
                if 'href' in a.attrs:
                    url = "https://archive.org" + a['href']
                    author = soup.find("span", itemprop="publisher").get_text()
                    title = soup.find("span", itemprop="name").get_text()

                    title_to_link[(title, author)] = url

    return title_to_link

def update_value(article_map):
    for key in article_map:
        url = article_map[key]

        if not url.startswith("http"):
            article_map[key] = 'INVALID URL'
            continue

        try:
            full_text = requests.get(url)
            soup = BeautifulSoup(full_text.text, "html.parser")

            try:
                text_content = soup.find('pre')

                if text_content:
                    cleaned_text = ' '.join(text_content.get_text().split())
                    article_map[key] = cleaned_text
                else:
                    article_map[key] = 'FULL TEXT NOT AVAILABLE'

            except AttributeError:
                article_map[key] = 'FULL TEXT NOT AVAILABLE'

        except requests.exceptions.RequestException as e:
            article_map[key] = 'REQUEST FAILED'

article_urls = fetch_articles()

article_map = fetch_full_text(article_urls)

update_value(article_map)

for key, value in article_map.items():
    print(f"Title: {key[0]}, Author: {key[1]}")
    print(f"Text: {value}\n")
    break