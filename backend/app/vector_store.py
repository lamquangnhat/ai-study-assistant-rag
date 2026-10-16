import chromadb


DB_PATH = "../chroma_db"

client = chromadb.PersistentClient(path=DB_PATH)

collection = client.get_or_create_collection(
    name="lecture_documents"
)


def add_chunks(
    chunks: list[dict],
    embeddings: list[list[float]],
) -> None:
    """
    Store document chunks and their embeddings in ChromaDB.
    """

    ids = []

    documents = []

    metadatas = []

    for index, chunk in enumerate(chunks):
        ids.append(f"{chunk['source']}_{chunk['page_number']}_{chunk['chunk_index']}_{index}")

        documents.append(chunk["text"])

        metadatas.append(
            {
                "source": chunk["source"],
                "page_number": chunk["page_number"],
                "chunk_index": chunk["chunk_index"],
            }
        )

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )


def search_chunks(
    query_embedding: list[float],
    top_k: int = 3,
) -> dict:
    """
    Search ChromaDB for the most relevant chunks.
    """

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    return results