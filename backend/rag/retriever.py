import chromadb
import os

from sentence_transformers import SentenceTransformer


# Load embedding model

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# Absolute path to ChromaDB

BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)

CHROMA_PATH = os.path.join(
    BASE_DIR,
    "..",
    "vector_db",
    "chroma_db"
)

CHROMA_PATH = os.path.abspath(
    CHROMA_PATH
)

print("Chroma Path:", CHROMA_PATH)


# Connect ChromaDB

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


# Get collection

collection = client.get_or_create_collection(
    name="college_notes"
)


def retrieve_relevant_chunks(query, top_k=5):

    query_embedding = embedding_model.encode(
        query
    ).tolist()

    results = collection.query(

        query_embeddings=[query_embedding],

        n_results=top_k
    )

    documents = results["documents"][0]

    filtered_docs = []

    for doc in documents:

        if len(doc.strip()) > 80:
            filtered_docs.append(doc)

    return filtered_docs


if __name__ == "__main__":

    query = input("Ask Question: ")

    chunks = retrieve_relevant_chunks(query)

    print("\nRelevant Chunks:\n")

    for i, chunk in enumerate(chunks):

        print(f"\nChunk {i+1}:\n")

        print(chunk)