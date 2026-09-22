import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

df=pd.read_csv("Data/pages.csv")
embeddings=np.load("Data/processed/embeddings.npy")

# number of clusters
number_of_clusters=2

model= KMeans(
    n_clusters=number_of_clusters,
    random_state=42,
    n_init=10
)

labels=model.fit_predict(embeddings)

df["cluster"]=labels

for cluster_id in sorted(df["cluster"].unique()):
    print(f"\n ====Cluster {cluster_id}====")

    cluster_pages= df[df["cluster"]==cluster_id]

    for _, page in cluster_pages.iterrows():
        print(page["title"])


df.to_csv(
    "Data/processed/pages_with_clusters.csv",
    index=False
)