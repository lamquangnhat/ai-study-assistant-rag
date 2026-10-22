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


thresholds = [
    1.0,
    1.1,
    1.2,
    1.3,
    1.4,
    1.5,
    1.6,
    1.7,
    1.8,
    1.9,
    2.0,
]


print("\n==============================")
print("StudyMate AI")
print("Distance Threshold Evaluation")
print("==============================\n")


for question in questions:

    print("------------------------------")
    print(f"Question: {question}")

    query_embedding = create_embedding(
        question
    )

    results = search_chunks(
        query_embedding=query_embedding,
        top_k=3,
    )

    distances = results["distances"][0]

    print("\nDistances:")

    for index, distance in enumerate(
        distances,
        start=1,
    ):
        print(
            f"  Result #{index}: "
            f"{distance:.4f}"
        )

    print("\nChunks included at each threshold:")

    for threshold in thresholds:

        included = sum(
            distance <= threshold
            for distance in distances
        )

        print(
            f"  {threshold:.1f} "
            f"-> {included}/3 chunks"
        )