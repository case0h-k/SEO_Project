def find_link_opportunities(
    pages,
    similarity_matrix,
    graph,
    threshold=0.70
):

    opportunities = []


    for i in range(
        len(pages)
    ):

        source = pages[i]["url"]


        for j in range(
            len(pages)
        ):

            # Don't compare a page
            # with itself
            if i == j:
                continue


            target = pages[j]["url"]


            similarity = (
                similarity_matrix[i][j]
            )


            # Check whether pages are
            # semantically related
            if similarity >= threshold:


                # Check whether an internal
                # link already exists
                if not graph.has_edge(
                    source,
                    target
                ):

                    opportunities.append({

                        "source": source,

                        "target": target,

                        "similarity": float(
                            similarity
                        )

                    })


    # Highest similarity first
    opportunities.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )


    return opportunities