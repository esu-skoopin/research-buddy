import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json

async def fetch_page(session, url, semaphore):
    async with semaphore:
        retries = 3  # Number of retries if 429 error occurs
        delay = 2  # Initial delay time for backoff
        for attempt in range(retries):
            try:
                async with session.get(url, timeout=10) as response:
                    if response.status == 429:
                        print(f"Rate limit hit for {url}. Retrying in {delay} seconds...")
                        await asyncio.sleep(delay)
                        delay *= 2  # Exponential backoff
                        continue
                    response.raise_for_status()
                    return await response.text()
            except aiohttp.ClientResponseError as e:
                print(f"Error fetching {url}: {e}")
                if response.status == 429 and attempt < retries - 1:
                    await asyncio.sleep(delay)  # Wait and retry
                    delay *= 2
                else:
                    return None
            except Exception as e:
                print(f"Unexpected error fetching {url}: {e}")
                return None

async def fetch_articles():
    base_url = "https://scholar.archive.org/search?q=*&offset={}"
    articles_per_page = 15
    max_offset = 2000000
    offsets = list(range(0, max_offset, articles_per_page))
    articles_found = {"microtext": set(), "pdf": set()}
    semaphore = asyncio.Semaphore(5)  # Adjust concurrency to prevent rate limits

    async with aiohttp.ClientSession() as session:
        tasks = []
        for offset in offsets:
            url = base_url.format(offset)
            tasks.append(fetch_page(session, url, semaphore))
            await asyncio.sleep(0.1)  # Add a slight delay between task creation

        for future in asyncio.as_completed(tasks):
            text = await future
            if text:
                soup = BeautifulSoup(text, "html.parser")
                new_articles = 0
                for a in soup.find_all("a"):
                    if 'title' in a.attrs and 'href' in a.attrs:
                        if a['title'] == 'read fulltext microfilm' or a['title'] == 'fulltext access':
                            url = a['href']
                            if url not in articles_found["microtext"]:
                                articles_found["microtext"].add(url)
                                new_articles += 1
                        elif a['title'] == 'fulltext PDF download':
                            pdf_url = a['href']
                            if pdf_url not in articles_found["pdf"]:
                                articles_found["pdf"].add(pdf_url)
                                new_articles += 1
                if new_articles == 0:
                    print("Reached the last page with no new articles.")
                    break

    # Convert sets to lists for JSON serialization
    articles_found["microtext"] = list(articles_found["microtext"])
    articles_found["pdf"] = list(articles_found["pdf"])
    return articles_found

async def fetch_article(session, url, semaphore, unique_counter):
    async with semaphore:
        try:
            async with session.get(url, timeout=10) as response:
                response.raise_for_status()
                text = await response.text()
                soup = BeautifulSoup(text, "html.parser")
                for a in soup.find_all('a'):
                    anchor_text = a.get_text().strip()
                    if anchor_text.replace(" ", "") == "FULLTEXTdownload":
                        if 'href' in a.attrs:
                            fulltext_url = "https://archive.org" + a['href']
                            identifier = soup.find('span', itemprop="identifier")
                            if identifier and identifier.get_text():
                                id_text = identifier.get_text()
                            else:
                                id_text = f"unique-{unique_counter}"
                            return id_text, fulltext_url
        except Exception as e:
            print(f"Failed to fetch article: {url}, error: {e}")
        return None

async def fetch_full_text(url_list):
    if not url_list:
        print("No URLs found to fetch full text.")
        return {}

    article_map = {}
    semaphore = asyncio.Semaphore(5)  # Adjust concurrency
    unique_counter = 1

    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in url_list:
            tasks.append(fetch_article(session, url, semaphore, unique_counter))
            unique_counter += 1

        for future in asyncio.as_completed(tasks):
            result = await future
            if result:
                identifier, fulltext_url = result
                article_map[identifier] = fulltext_url

    return article_map

async def fetch_full_text_content(session, key_url, semaphore):
    key, url = key_url
    if not url.startswith("http"):
        return key, 'INVALID URL'

    async with semaphore:
        try:
            async with session.get(url, timeout=10) as response:
                response.raise_for_status()
                text = await response.text()
                soup = BeautifulSoup(text, "html.parser")
                text_content = soup.find('pre')
                if text_content:
                    cleaned_text = ' '.join(text_content.get_text().split())
                    return key, cleaned_text
                else:
                    return key, 'FULL TEXT NOT AVAILABLE'
        except Exception as e:
            return key, f'REQUEST FAILED: {e}'

async def update_value(article_map):
    semaphore = asyncio.Semaphore(5)  # Adjust concurrency
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_full_text_content(session, item, semaphore) for item in article_map.items()]

        for future in asyncio.as_completed(tasks):
            key, value = await future
            article_map[key] = value

async def main():
    article_urls = await fetch_articles()

    if article_urls:
        print(f"Found {len(article_urls['microtext'])} microtext articles.")
        print(f"Found {len(article_urls['pdf'])} PDF articles.")

        # Fetch full text for microtext articles
        article_map = await fetch_full_text(article_urls["microtext"])
        await update_value(article_map)

        # Save microtext articles to JSON with identifiers as keys and full text as values
        with open("microtext_data.json", "w") as f:
            json.dump(article_map, f, indent=2)

        # Save PDF links to JSON
        with open("pdf_links.json", "w") as f:
            json.dump(article_urls["pdf"], f, indent=2)
    else:
        print("No articles found.")

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
