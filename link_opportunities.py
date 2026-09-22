import pandas as pd
import numpy as np
import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity

pages= pd.read_csv("Data/pages.csv")
links=pd.read_csv("Data/links.csv")
embeddings=np.load("Data/processed.embeddings.npy")

graph=nx.DiGraph()
for _, row in links.iterrows():
    graph.add_edge(row["source"],row["target"])

# Similarity Matrix
similarity=cosine_similarity(embeddings)

threshold= 0.70

opportunities=[]

for i in range(len(pages)):
    for j in range(len(pages)):
        if i==j:
            continue

        source=pages.iloc[i]["url"]
        target=pages.iloc[j]["url"]

        score=similarity[i][j]

        if score>= threshold:
            if not graph.has_edge(source,target):
                opportunities.append({
                    "source":source,
                    "target": target,
                    "similarity": score
                })

opportunities.sort(
    key=lambda x: x["similarity"],
    reverse=True
)

for opportunity in opportunities:
    print(
        f"{opportunity['source']}"
        f"->"
        f"{opportunity['target']}"
        f" | similarity="
        f"{opportunity['similarity']:.3f}"
    )