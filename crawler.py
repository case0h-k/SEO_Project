import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import trafilatura
from urllib.parse import (
    urljoin,
    urlparse,
    urlunparse
)

def normalize_url(url):

    parsed = urlparse(url)

    # Remove query parameters and fragments
    path = parsed.path.rstrip("/")

    # Root URL should remain /
    if path == "":
        path = "/"

    normalized = parsed._replace(
        path=path,
        query="",
        fragment=""
    )

    return urlunparse(normalized)

def is_crawlable_url(url):

    parsed = urlparse(url)

    # Only crawl HTTP/HTTPS URLs
    if parsed.scheme not in ["http", "https"]:
        return False

    # Ignore common non-page resources
    excluded_extensions = (
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".svg",
        ".pdf",
        ".zip",
        ".mp4",
        ".mp3",
        ".css",
        ".js",
        ".xml",
        ".json"
    )

    if parsed.path.lower().endswith(
        excluded_extensions
    ):
        return False

    return True


def crawl_page(url):

    try:

        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "SemanticSiteCrawler/1.0"
            }
        )

        response.raise_for_status()

    except requests.RequestException as e:

        print(
            f"Skipping {url}: {e}"
        )

        return None


    # Make sure this is actually an HTML page
    content_type = response.headers.get(
        "Content-Type",
        ""
    )

    if "text/html" not in content_type:

        print(
            f"Skipping non-HTML URL: {url}"
        )

        return None


    html = response.text

    soup = BeautifulSoup(
        html,
        "html.parser"
    )


    # --------------------------------
    # Extract title
    # --------------------------------

    title = ""

    if soup.title:

        title = soup.title.get_text(
            strip=True
        )


    # --------------------------------
    # Extract main textual content
    # --------------------------------

    content = trafilatura.extract(
        html
    )

    if content is None:

        content = ""


    # --------------------------------
    # Extract internal links
    # --------------------------------

    links = []

    domain = urlparse(url).netloc


    for a in soup.find_all(
        "a",
        href=True
    ):

        target = urljoin(
            url,
            a["href"]
        )

        # Only keep links belonging to
        # the same website
        if (
            urlparse(target).netloc == domain
            and is_crawlable_url(target)
        ):

            links.append({
                "url": target,
                "anchor_text": a.get_text(
                    strip=True
                )
            })


    # --------------------------------
    # Return page data
    # --------------------------------

    return {
        "url": url,
        "title": title,
        "content": content,
        "links": links
    }


def crawl_website(
    start_url,
    max_pages=50
):
    start_url = normalize_url(
        start_url
    )
    pages = []

    queue = [start_url]

    visited = set()


    while (
        queue
        and len(pages) < max_pages
    ):

        url = queue.pop(0)
        
        url = normalize_url(url)


        # Don't crawl the same URL twice
        if url in visited:
            continue


        visited.add(url)


        print(
            f"Crawling: {url}"
        )


        page = crawl_page(url)


        # If the request failed,
        # don't add it to pages
        if page is None:
            continue


        pages.append(page)


        # Add discovered links
        # to the crawl queue
        for link in page["links"]:

            target = normalize_url(link["url"])

            if target not in visited:

                queue.append(target)


    return pages