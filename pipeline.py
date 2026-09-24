from crawler import crawl_website
from embeddings import generate_embeddings
from similarity import calculate_similarity
from clustering import cluster_pages
from graph import build_link_graph
from analysis import find_link_opportunities


def run_analysis(
    website_url,
    max_pages=50
):

    # --------------------------------
    # 1. CRAWL WEBSITE
    # --------------------------------

    pages = crawl_website(
        website_url,
        max_pages=max_pages
    )


    if not pages:

        raise ValueError(
            "No pages could be crawled from the provided URL."
        )


    # --------------------------------
    # 2. GENERATE EMBEDDINGS
    # --------------------------------

    embeddings = generate_embeddings(
        pages
    )


    # --------------------------------
    # 3. CALCULATE SIMILARITY
    # --------------------------------

    similarity_matrix = calculate_similarity(
        embeddings
    )


    # --------------------------------
    # 4. CLUSTER PAGES
    # --------------------------------

    # KMeans cannot have more clusters
    # than the number of pages.

    number_of_clusters = min(
        5,
        len(pages)
    )

    clusters = cluster_pages(
        embeddings,
        number_of_clusters=number_of_clusters
    )


    # --------------------------------
    # 5. BUILD INTERNAL-LINK GRAPH
    # --------------------------------

    graph = build_link_graph(
        pages
    )


    # --------------------------------
    # 6. FIND LINK OPPORTUNITIES
    # --------------------------------

    opportunities = find_link_opportunities(
        pages,
        similarity_matrix,
        graph,
        threshold=0.70
    )


    # --------------------------------
    # 7. PREPARE PAGE DATA
    # --------------------------------

    page_data = []

    for index, page in enumerate(pages):

        page_data.append({

            "url": page["url"],

            "title": page["title"],

            "content_length": len(
                page["content"]
            ),

            "cluster": int(
                clusters[index]
            )

        })


    # --------------------------------
    # 8. PREPARE CLUSTER DATA
    # --------------------------------

    cluster_data = []

    for cluster_id in range(
        number_of_clusters
    ):

        cluster_pages_list = []

        for index, page in enumerate(pages):

            if clusters[index] == cluster_id:

                cluster_pages_list.append(
                    page["url"]
                )


        cluster_data.append({

            "id": cluster_id,

            "pages": cluster_pages_list,

            "page_count": len(
                cluster_pages_list
            )

        })


    # --------------------------------
    # 9. PREPARE GRAPH DATA
    # --------------------------------

    graph_nodes = []

    for node in graph.nodes:

        # Find the corresponding page
        # so the frontend can display
        # title and cluster information.

        page_index = None

        for index, page in enumerate(pages):

            if page["url"] == node:

                page_index = index
                break


        if page_index is not None:

            graph_nodes.append({

                "id": node,

                "url": node,

                "title": pages[page_index]["title"],

                "cluster": int(
                    clusters[page_index]
                )

            })


    graph_edges = []

    for source, target in graph.edges:

        graph_edges.append({

            "source": source,

            "target": target

        })


    # --------------------------------
    # 10. PREPARE SUMMARY
    # --------------------------------

    summary = {

        "pages": len(pages),

        "internal_links": graph.number_of_edges(),

        "clusters": number_of_clusters,

        "link_opportunities": len(
            opportunities
        )

    }


    # --------------------------------
    # 11. RETURN COMPLETE RESULT
    # --------------------------------

    return {

        "summary": summary,

        "pages": page_data,

        "clusters": cluster_data,

        "opportunities": opportunities,

        "graph": {

            "nodes": graph_nodes,

            "edges": graph_edges

        }

    }