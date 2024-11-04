import requests
from bs4 import BeautifulSoup
import time
import os

# Full list of arXiv categories as per your requirement
arxiv_categories = [
    "cs.AI", "cs.AR", "cs.CC", "cs.CE", "cs.CG", "cs.CL", "cs.CR", "cs.CV",
    "cs.CY", "cs.DB", "cs.DC", "cs.DL", "cs.DM", "cs.DS", "cs.ET", "cs.FL",
    "cs.GL", "cs.GR", "cs.GT", "cs.HC", "cs.IR", "cs.IT", "cs.LG", "cs.LO",
    "cs.MA", "cs.MM", "cs.MS", "cs.NA", "cs.NE", "cs.NI", "cs.OH", "cs.OS",
    "cs.PF", "cs.PL", "cs.RO", "cs.SC", "cs.SD", "cs.SE", "cs.SI", "cs.SY",
    "econ.EM", "econ.GN", "econ.TH", "eess.AS", "eess.IV", "eess.SP", "eess.SY",
    "math.AC", "math.AG", "math.AP", "math.AT", "math.CA", "math.CO", "math.CT",
    "math.CV", "math.DG", "math.DS", "math.FA", "math.GM", "math.GN", "math.GR",
    "math.GT", "math.HO", "math.IT", "math.KT", "math.LO", "math.MG", "math.MP",
    "math.NA", "math.NT", "math.OA", "math.OC", "math.PR", "math.QA", "math.RA",
    "math.RT", "math.SG", "math.SP", "math.ST", "astro-ph", "astro-ph.CO",
    "astro-ph.EP", "astro-ph.GA", "astro-ph.HE", "astro-ph.IM", "astro-ph.SR",
    "cond-mat.dis-nn", "cond-mat.mes-hall", "cond-mat.mtrl-sci", "cond-mat.other",
    "cond-mat.quant-gas", "cond-mat.soft", "cond-mat.stat-mech", "cond-mat.str-el",
    "cond-mat.supr-con", "gr-qc", "hep-ex", "hep-lat", "hep-ph", "hep-th",
    "math-ph", "nlin.AO", "nlin.CD", "nlin.CG", "nlin.PS", "nlin.SI", "nucl-ex",
    "nucl-th", "physics.acc-ph", "physics.ao-ph", "physics.app-ph", "physics.atm-clus",
    "physics.atom-ph", "physics.bio-ph", "physics.chem-ph", "physics.class-ph",
    "physics.comp-ph", "physics.data-an", "physics.ed-ph", "physics.flu-dyn",
    "physics.gen-ph", "physics.geo-ph", "physics.hist-ph", "physics.ins-det",
    "physics.med-ph", "physics.optics", "physics.plasm-ph", "physics.pop-ph",
    "physics.soc-ph", "physics.space-ph", "quant-ph", "q-bio.BM", "q-bio.CB",
    "q-bio.GN", "q-bio.MN", "q-bio.NC", "q-bio.OT", "q-bio.PE", "q-bio.QM",
    "q-bio.SC", "q-bio.TO", "q-fin.CP", "q-fin.EC", "q-fin.GN", "q-fin.MF",
    "q-fin.PM", "q-fin.PR", "q-fin.RM", "q-fin.ST", "q-fin.TR", "stat.AP",
    "stat.CO", "stat.ME", "stat.ML", "stat.OT", "stat.TH"
]


def get_arxiv_articles(query, start=0, max_results=10):
    base_url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"cat:{query}",
        "start": start,
        "max_results": max_results
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve articles for category {query}. Status code: {response.status_code}")
        return None


def parse_article_links(xml_data):
    soup = BeautifulSoup(xml_data, "xml")
    entries = soup.find_all("entry")
    articles = []
    for entry in entries:
        article_id = entry.id.text.split('/')[-1]
        abstract_link = entry.find("link", rel="alternate")["href"]
        articles.append({"id": article_id, "abstract_link": abstract_link})
    return articles


def extract_html_content(article_url):
    response = requests.get(article_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        # Attempt to extract HTML content
        content = soup.find("blockquote", class_="abstract")
        if content:
            return content.get_text(strip=True)

        # Check for full-text HTML link
        full_text_link = soup.find("a", text="Full-text")
        if full_text_link and "format=html" in full_text_link.get("href", ""):
            full_text_url = "https://arxiv.org" + full_text_link["href"]
            full_text_response = requests.get(full_text_url)
            full_text_soup = BeautifulSoup(full_text_response.content, "html.parser")
            return full_text_soup.get_text(strip=True)
    return None


def save_article_text(category, article_id, content):
    directory = os.path.join("arxiv_articles", category)
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, f"{article_id}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Saved article {article_id} in category {category} to {file_path}")


def process_category(category, total_articles=50):
    articles_per_batch = 10
    for start in range(0, total_articles, articles_per_batch):
        xml_data = get_arxiv_articles(query=category, start=start, max_results=articles_per_batch)
        if xml_data:
            articles = parse_article_links(xml_data)
            for article in articles:
                print(f"Processing article {article['id']} in category {category}...")
                html_content = extract_html_content(article["abstract_link"])
                if html_content:
                    save_article_text(category, article["id"], html_content)
                else:
                    print(f"No HTML content found for article {article['id']} in category {category}")
                time.sleep(3)  # Respect arXiv's rate limit to avoid being blocked


def main():
    for category in arxiv_categories:
        print(f"Starting category: {category}")
        process_category(category, total_articles=50)
        print(f"Finished category: {category}")


if __name__ == "__main__":
    main()
