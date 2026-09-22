import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import umap

df=pd.read_csv("Data/processed/pages_with_clusters.csv")
embeddings=np.load("Data/processed/embeddings.npy")

reducer= umap.UMAP(
    n_components=2,
    random_state=42
)

coordinates=reducer.fit_transform(embeddings)

plt.figure(figsize=(10,7))
plt.scatter(
    coordinates[:,0],
    coordinates[:,1],
    c=df["cluster"]
)

for i, row in df.iterrows():
    plt.annotate(
        row["title"],
        (
            coordinates[i,0],
            coordinates[i,1]
        )
    )
plt.xlabel("UMAP 1")
plt.ylabel("UMAP 2")
plt.title("Semantic Page Clusters")
plt.show()