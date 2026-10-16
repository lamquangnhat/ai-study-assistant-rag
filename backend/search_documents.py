from app.embedding_service import create_embedding
from app.vector_store import search_chunks


query = "What is an embedding?"

print(f"Question: {query}")

print("\nCreating query embedding...")

query_embedding = create_embedding(query)


print("Searching ChromaDB...")

results = search_chunks(
    query_embedding=query_embedding,
    top_k=3,
)


print("\n===== SEARCH RESULTS =====")


documents = results["documents"][0]
metadatas = results["metadatas"][0]
distances = results["distances"][0]


for index, (document, metadata, distance) in enumerate(
    zip(documents, metadatas, distances),
    start=1,
):
    print("\n------------------------------")
    print(f"Result {index}")
    print("------------------------------")

    print(f"Source: {metadata['source']}")
    print(f"Page: {metadata['page_number']}")
    print(f"Chunk: {metadata['chunk_index']}")
    print(f"Distance: {distance}")

    print("\nText:")
    print(document[:500])