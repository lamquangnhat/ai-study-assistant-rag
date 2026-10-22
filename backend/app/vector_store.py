import chromadb


DB_PATH = "../chroma_db"


client = chromadb.PersistentClient(
    path=DB_PATH
)


collection = client.get_or_create_collection(
    name="lecture_documents"
)


# =========================
# Add / Update Chunks
# =========================

def add_chunks(
    chunks: list[dict],
    embeddings: list[list[float]],
) -> None:
    """
    Store document chunks and their embeddings in ChromaDB.

    If chunks from the same source already exist,
    they will be removed first to prevent stale chunks.
    """

    if not chunks:
        return

    source = chunks[0]["source"]

    # Remove old chunks from this document first.
    delete_chunks_by_source(source)

    ids = []
    documents = []
    metadatas = []

    for index, chunk in enumerate(chunks):

        chunk_id = (
            f"{chunk['source']}_"
            f"{chunk['page_number']}_"
            f"{chunk['chunk_index']}_"
            f"{index}"
        )

        ids.append(chunk_id)

        documents.append(
            chunk["text"]
        )

        metadatas.append(
            {
                "source": chunk["source"],
                "page_number": chunk["page_number"],
                "chunk_index": chunk["chunk_index"],
            }
        )

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )


# =========================
# Search
# =========================

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


# =========================
# Get All Documents
# =========================

def get_documents() -> list[dict]:
    """
    Get a summary of all documents stored in ChromaDB.
    """

    results = collection.get(
        include=["metadatas"]
    )

    metadatas = results.get(
        "metadatas",
        []
    )

    documents = {}

    for metadata in metadatas:

        source = metadata["source"]

        if source not in documents:
            documents[source] = {
                "filename": source,
                "total_chunks": 0,
            }

        documents[source]["total_chunks"] += 1

    return list(documents.values())


# =========================
# Delete Document
# =========================

def delete_chunks_by_source(
    source: str,
) -> None:
    """
    Delete all chunks belonging to a document.
    """

    collection.delete(
        where={
            "source": source
        }
    )