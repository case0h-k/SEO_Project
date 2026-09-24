import networkx as nx

def build_link_graph(pages):

    graph = nx.DiGraph()

    # URLs that were actually crawled
    crawled_urls = {
        page["url"]
        for page in pages
    }

    # Add only crawled pages as nodes
    for page in pages:

        source = page["url"]

        graph.add_node(source)

        for link in page["links"]:

            target = link["url"]

            # Only create an edge if target
            # was also crawled
            if target in crawled_urls:

                graph.add_edge(
                    source,
                    target
                )

    return graph