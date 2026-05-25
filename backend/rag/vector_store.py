import chromadb
import os

from sentence_transformers import SentenceTransformer
from ingest import process_all_pdfs


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


# Create collection

collection = client.get_or_create_collection(
    name="college_notes"
)


def create_embeddings_and_store():

    chunks = process_all_pdfs()

    print(f"Total chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks):

        if len(chunk.strip()) < 50:
            continue

        embedding = embedding_model.encode(
            chunk
        ).tolist()

        collection.add(

            ids=[str(i)],

            embeddings=[embedding],

            documents=[chunk]
        )

        print(f"Stored chunk {i}")


if __name__ == "__main__":

    create_embeddings_and_store()