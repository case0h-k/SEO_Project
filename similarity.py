from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(embeddings):

    matrix = cosine_similarity(
        embeddings
    )

    return matrix