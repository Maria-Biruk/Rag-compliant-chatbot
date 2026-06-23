import chromadb
from sentence_transformers import SentenceTransformer


# Load embedding model
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# Load vector database
client = chromadb.PersistentClient(
    path="vector_store"
)


collection = client.get_collection(
    name="complaints"
)


def retrieve(question, k=3):

    # Embed question
    query_embedding = model.encode(
        question
    )


    # Search database
    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=k
    )


    return results