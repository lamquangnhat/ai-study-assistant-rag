from app.embedding_service import create_embedding
from app.vector_store import search_chunks


question = (
    "Why are retrieved chunks provided to the "
    "language model instead of asking the model "
    "to answer without them?"
)


print("\n==============================")
print("StudyMate AI")
print("ID 14 Retrieval Inspection")
print("==============================\n")


print(f"Question:\n{question}")


query_embedding = create_embedding(
    question
)


results = search_chunks(
    query_embedding=query_embedding,
    top_k=3,
)


documents = results["documents"][0]
metadatas = results["metadatas"][0]
distances = results["distances"][0]


for index, (
    document,
    metadata,
    distance,
) in enumerate(
    zip(
        documents,
        metadatas,
        distances,
    ),
    start=1,
):

    print("\n------------------------------")

    print(
        f"Result #{index}"
    )

    print(
        f"Source: "
        f"{metadata['source']}"
    )

    print(
        f"Page: "
        f"{metadata['page_number']}"
    )

    print(
        f"Chunk: "
        f"{metadata['chunk_index']}"
    )

    print(
        f"Distance: "
        f"{distance:.4f}"
    )

    print("\nContent:")

    print(document)