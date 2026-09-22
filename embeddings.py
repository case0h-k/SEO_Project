import pandas as pd
from sentence_transformers import SentenceTransformer

df= pd.read_csv("Data/pages.csv")

# This is a pretrained embedding model 
model= SentenceTransformer("all-MiniLM-L6-v2")

texts=(
    df["title"].fillna("")
    + "\n"
    + df["content"].fillna("")
)

# Generate embeddings
embeddings= model.encode(
    texts.tolist(),
    show_progress_bar=True
)

print("Number of pages:", len(df))
print("Embedding shape:",embeddings.shape)

import numpy as np

np.save(
    "Data/processed/embeddings.npy",
    embeddings
)

print("Saved embeddings to embeddings.npy")
