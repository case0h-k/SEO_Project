from crawler import crawl_website
from embeddings import generate_embeddings
from similarity import calculate_similarity
from clustering import cluster_pages
from graph import build_link_graph
from analysis import find_link_opportunities


def main():

    # --------------------------------
    # 1. INPUT
    # --------------------------------

    website_url = input(
        "Enter website URL: "
    )


    # --------------------------------
    # 2. CRAWL WEBSITE
    # --------------------------------

    print(
        "\nCrawling website..."
    )

    pages = crawl_website(
        website_url,
        max_pages=50
    )

    print(
        f"Found {len(pages)} pages."
    )


    # --------------------------------
    # 3. GENERATE EMBEDDINGS
    # --------------------------------

    print(
        "\nGenerating embeddings..."
    )

    embeddings = generate_embeddings(
        pages
    )

    print(
        "Embeddings generated:",
        embeddings.shape
    )


    # --------------------------------
    # 4. CALCULATE SIMILARITY
    # --------------------------------

    print(
        "\nCalculating semantic similarity..."
    )

    similarity_matrix = calculate_similarity(
        embeddings
    )

    print(
        "Similarity matrix:",
        similarity_matrix.shape
    )


    # --------------------------------
    # 4A. EMBEDDING DIAGNOSTIC
    # --------------------------------

    print(
        "\n===== EMBEDDING DIAGNOSTIC ====="
    )

    found_high_similarity = False

    for i in range(
        len(embeddings)
    ):

        for j in range(
            i + 1,
            len(embeddings)
        ):

            similarity = similarity_matrix[i][j]

            if similarity >= 0.999:

                found_high_similarity = True

                content_a = pages[i]["content"]
                content_b = pages[j]["content"]


                # Compare exact extracted content
                content_identical = (
                    content_a == content_b
                )


                # Count matching characters
                min_length = min(
                    len(content_a),
                    len(content_b)
                )

                matching_characters = sum(
                    1
                    for k in range(min_length)
                    if content_a[k] == content_b[k]
                )


                print(
                    f"\nVery high similarity: "
                    f"{similarity:.6f}"
                )

                print(
                    "\nPage A:",
                    pages[i]["url"]
                )

                print(
                    "Page B:",
                    pages[j]["url"]
                )

                print(
                    "\nTitle A:",
                    pages[i]["title"]
                )

                print(
                    "Title B:",
                    pages[j]["title"]
                )

                print(
                    "\nContent lengths:",
                    len(content_a),
                    len(content_b)
                )

                print(
                    "Content identical:",
                    content_identical
                )

                print(
                    "Matching character positions:",
                    matching_characters,
                    "/",
                    min_length
                )

                if min_length > 0:

                    match_percentage = (
                        matching_characters
                        / min_length
                    ) * 100

                    print(
                        f"Character match percentage: "
                        f"{match_percentage:.2f}%"
                    )


                print(
                    "\nContent A preview:"
                )

                print(
                    content_a[:500]
                )

                print(
                    "\nContent B preview:"
                )

                print(
                    content_b[:500]
                )


    if not found_high_similarity:

        print(
            "No page pairs with similarity >= 0.999 found."
        )


    # --------------------------------
    # 5. CLUSTER PAGES
    # --------------------------------

    print(
        "\nFinding topical clusters..."
    )

    clusters = cluster_pages(
        embeddings,
        number_of_clusters=5
    )

    print(
        "Clusters generated."
    )


    # --------------------------------
    # 6. BUILD INTERNAL-LINK GRAPH
    # --------------------------------

    print(
        "\nBuilding internal-link graph..."
    )

    graph = build_link_graph(
        pages
    )

    print(
        "Nodes:",
        graph.number_of_nodes()
    )

    print(
        "Edges:",
        graph.number_of_edges()
    )


    # --------------------------------
    # 6A. DEBUG GRAPH NODES
    # --------------------------------

    crawled_urls = {
        page["url"]
        for page in pages
    }

    graph_urls = set(
        graph.nodes
    )

    extra_nodes = (
        graph_urls - crawled_urls
    )


    print(
        "\nPage records:",
        len(pages)
    )

    print(
        "Unique crawled URLs:",
        len(crawled_urls)
    )

    print(
        "Graph nodes:",
        len(graph_urls)
    )


    print(
        "\nGraph nodes not in crawled pages:"
    )


    if extra_nodes:

        for url in extra_nodes:

            print(url)

    else:

        print(
            "None"
        )


    # --------------------------------
    # 7. FIND LINK OPPORTUNITIES
    # --------------------------------

    print(
        "\nFinding link opportunities..."
    )

    opportunities = (
        find_link_opportunities(
            pages,
            similarity_matrix,
            graph,
            threshold=0.70
        )
    )


    # --------------------------------
    # 8. OUTPUT
    # --------------------------------

    print(
        "\n===== LINK OPPORTUNITIES ====="
    )


    print(
        f"\nTotal opportunities found: "
        f"{len(opportunities)}"
    )


    if not opportunities:

        print(
            "No link opportunities found."
        )

    else:

        print(
            "\nTop 10 opportunities:"
        )


        for opportunity in opportunities[:10]:

            print(
                f"\nSource: "
                f"{opportunity['source']}"
            )

            print(
                f"Target: "
                f"{opportunity['target']}"
            )

            print(
                f"Similarity: "
                f"{opportunity['similarity']:.3f}"
            )


if __name__ == "__main__":

    main()