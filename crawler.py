import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import trafilatura
import pandas as pd
from collections import deque


# ==========================================
# SETTINGS
# ==========================================

START_URL = "https://web-scraping.dev/"

MAX_PAGES = 20

HEADERS = {
    "User-Agent": "SemanticSiteArchitectureCrawler/1.0"
}


# ==========================================
# CRAWL ONE PAGE
# ==========================================

def crawl_page(url):

    try:

        response = requests.get(
            url,
            timeout=10,
            headers=HEADERS
        )

        response.raise_for_status()

    except requests.RequestException as e:

        print(f"Failed: {url}")
        print(e)

        return None


    html = response.text

    soup = BeautifulSoup(
        html,
        "html.parser"
    )


    # ------------------------------
    # Title
    # ------------------------------

    title = ""

    if soup.title:

        title = soup.title.get_text(
            strip=True
        )


    # ------------------------------
    # Main text
    # ------------------------------

    content = trafilatura.extract(
        html
    )

    if content is None:

        content = ""


    # ------------------------------
    # Internal links
    # ------------------------------

    internal_links = []

    domain = urlparse(
        url
    ).netloc


    for link in soup.find_all(
        "a",
        href=True
    ):

        target = urljoin(
            url,
            link["href"]
        )

        parsed_target = urlparse(
            target
        )


        # Only HTTP/HTTPS
        if parsed_target.scheme not in [
            "http",
            "https"
        ]:

            continue


        # Only same-domain links
        if parsed_target.netloc != domain:

            continue


        # Remove fragments
        target = target.split("#")[0]


        anchor_text = link.get_text(
            " ",
            strip=True
        )


        internal_links.append({
            "url": target,
            "anchor_text": anchor_text
        })


    return {
        "url": url,
        "title": title,
        "content": content,
        "links": internal_links
    }


# ==========================================
# WEBSITE CRAWLER
# ==========================================

def crawl_website(start_url, max_pages=20):

    domain = urlparse(
        start_url
    ).netloc


    queue = deque([
        start_url
    ])

    visited = set()

    pages = []

    links = []


    while queue and len(visited) < max_pages:

        url = queue.popleft()


        if url in visited:

            continue


        print(
            f"Crawling ({len(visited) + 1}/{max_pages}): {url}"
        )


        page = crawl_page(
            url
        )


        visited.add(
            url
        )


        if page is None:

            continue


        # ------------------------------
        # Save page
        # ------------------------------

        pages.append({
            "url": page["url"],
            "title": page["title"],
            "content": page["content"]
        })


        # ------------------------------
        # Save links
        # ------------------------------

        for link in page["links"]:

            links.append({
                "source": url,
                "target": link["url"],
                "anchor_text": link["anchor_text"]
            })


            # Add new pages to queue
            if (
                link["url"] not in visited
                and link["url"] not in queue
                and urlparse(link["url"]).netloc == domain
            ):

                queue.append(
                    link["url"]
                )


    return pages, links


# ==========================================
# RUN CRAWLER
# ==========================================

pages, links = crawl_website(
    START_URL,
    MAX_PAGES
)


# ==========================================
# SAVE RESULTS
# ==========================================

pages_df = pd.DataFrame(
    pages
)

links_df = pd.DataFrame(
    links
)


pages_df.to_csv(
    "data/pages.csv",
    index=False
)


links_df.to_csv(
    "data/links.csv",
    index=False
)


print("\n================================")
print("CRAWLING COMPLETE")
print("================================")

print(
    f"Pages crawled: {len(pages_df)}"
)

print(
    f"Internal links found: {len(links_df)}"
)

print(
    "\nSaved:"
)

print(
    "data/pages.csv"
)

print(
    "data/links.csv"
)