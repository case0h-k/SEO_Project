import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

df=pd.read_csv("Data/pages.csv")

embeddings=np.load("Data/processed/embeddings.npy")

similarity_matrix=cosine_similarity(embeddings)


def get_similar_pages(page_index, top_k=3):

    scores=similarity_matrix[page_index]

    indices= np.argsort(scores)[::-1]
    results=[]

    for index in indices:
        if index==page_index:
            continue

        results.append({
            "title": df.iloc[index]["title"],
            "url": df.iloc[index]["url"],
            "similarity": scores[index]
        })

        if len(results)==top_k:
            break
    return results
    
page_index=0

print(f"\nPages similar to:"
f"{df.iloc[page_index]['title']}")

for result in get_similar_pages(page_index):

    print(
        result["title"],
        "->",
        round(result["similarity"],3)
    )