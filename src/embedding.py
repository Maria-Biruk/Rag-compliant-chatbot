import os
import pandas as pd

from sklearn.model_selection import train_test_split
from langchain_text_splitters import RecursiveCharacterTextSplitter

from sentence_transformers import SentenceTransformer

import chromadb

# =========================
# Load Dataset
# =========================

df = pd.read_csv(
    "data/filtered_complaints.csv"
)

print("Dataset Shape:")
print(df.shape)

# =========================
# Stratified Sample
# =========================

sample_df, _ = train_test_split(
    df,
    train_size=12000,
    stratify=df["Product"],
    random_state=42
)

print("\nSample Shape:")
print(sample_df.shape)

# =========================
# Chunking
# =========================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

documents = []
metadatas = []

for _, row in sample_df.iterrows():

    text = str(row["clean_narrative"])

    chunks = text_splitter.split_text(text)

    for i, chunk in enumerate(chunks):

        documents.append(chunk)

        metadatas.append(
            {
                "complaint_id": str(row["Complaint ID"]),
                "product": str(row["Product"]),
                "chunk_index": i
            }
        )

print("\nTotal Chunks:")
print(len(documents))

# =========================
# Embedding Model
# =========================

print("\nLoading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Generating embeddings...")

embeddings = model.encode(
    documents,
    show_progress_bar=True
)

print("Embedding shape:")
print(embeddings.shape)

# =========================
# ChromaDB
# =========================

os.makedirs(
    "vector_store",
    exist_ok=True
)

client = chromadb.PersistentClient(
    path="vector_store"
)

collection = client.get_or_create_collection(
    name="complaints"
)

print("\nStoring vectors...")

batch_size = 1000

for start in range(0, len(documents), batch_size):

    end = min(
        start + batch_size,
        len(documents)
    )

    collection.add(
        documents=documents[start:end],
        embeddings=embeddings[start:end].tolist(),
        metadatas=metadatas[start:end],
        ids=[
            f"chunk_{i}"
            for i in range(start, end)
        ]
    )

print("\nVector Store Created Successfully!")
print("Location: vector_store/")