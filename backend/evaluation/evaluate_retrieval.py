from app.embedding_service import create_embedding
from app.vector_store import search_chunks


questions = [
    "What is Retrieval-Augmented Generation?",
    "What is the purpose of chunking documents?",
    "What are embeddings used for in a RAG system?",
    "What is a vector database?",
    "What is the capital of France?",
    "Who is the president of the United States?",
    "What is the tallest mountain in the world?",
]


print("\n==============================")
print("StudyMate AI - Retrieval Evaluation")
print("==============================\n")


for question in questions:

    print("------------------------------")
    print(f"Question: {question}")

    query_embedding = create_embedding(question)

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

        print(f"\n--- Result #{index} ---")

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

        print(document[:500])

        if len(document) > 500:
            print("...")
