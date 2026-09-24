from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

def generate_embeddings(pages):

    texts = []

    for page in pages:

        text = (
            page["title"]
            + "\n"
            + page["content"]
        )

        texts.append(text)


    # Diagnostic information
    print("\n===== EMBEDDING INPUT CHECK =====")

    for i, page in enumerate(pages[:5]):

        print(
            f"\nPage {i + 1}:"
        )

        print(
            "URL:",
            page["url"]
        )

        print(
            "Title:",
            page["title"]
        )

        print(
            "Content length:",
            len(page["content"])
        )

        print(
            "Content preview:"
        )

        print(
            page["content"][:300]
        )


    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )


    return embeddings