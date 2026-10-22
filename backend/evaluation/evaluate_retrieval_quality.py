import json
from pathlib import Path

from app.embedding_service import create_embedding
from app.vector_store import search_chunks


BASE_DIR = Path(__file__).resolve().parent

DATASET_PATH = (
    BASE_DIR / "evaluation_dataset.json"
)


with DATASET_PATH.open(
    "r",
    encoding="utf-8",
) as file:
    dataset = json.load(file)


print("\n==============================")
print("StudyMate AI")
print("Retrieval Quality Evaluation")
print("==============================\n")


total_questions = len(dataset)

correct_questions = 0

results = []


for item in dataset:

    question = item["question"]

    expected_type = item["expected_type"]

    expected_keywords = [
        keyword.lower()
        for keyword in item[
            "expected_context_keywords"
        ]
    ]

    print("------------------------------")
    print(f"Question: {question}")
    print(f"Expected type: {expected_type}")

    query_embedding = create_embedding(
        question
    )

    search_results = search_chunks(
        query_embedding=query_embedding,
        top_k=3,
    )

    documents = (
        search_results["documents"][0]
    )

    metadatas = (
        search_results["metadatas"][0]
    )

    distances = (
        search_results["distances"][0]
    )

    combined_context = "\n".join(
        documents
    ).lower()

    matched_keywords = [
        keyword
        for keyword in expected_keywords
        if keyword in combined_context
    ]

    missing_keywords = [
        keyword
        for keyword in expected_keywords
        if keyword not in combined_context
    ]

    if expected_type == "answerable":

        keyword_coverage = (
            len(matched_keywords)
            / len(expected_keywords)
            if expected_keywords
            else 0
        )

        retrieval_correct = (
            keyword_coverage >= 0.5
        )

    else:

        keyword_coverage = 0

        retrieval_correct = True

    if retrieval_correct:
        correct_questions += 1

    print(
        f"Top-K results: {len(documents)}"
    )

    print(
        f"Matched keywords: "
        f"{matched_keywords}"
    )

    print(
        f"Missing keywords: "
        f"{missing_keywords}"
    )

    print(
        f"Keyword coverage: "
        f"{keyword_coverage:.2%}"
    )

    print(
        f"Retrieval quality: "
        f"{retrieval_correct}"
    )

    print("\nDistances:")

    for index, distance in enumerate(
        distances,
        start=1,
    ):
        print(
            f"  Result #{index}: "
            f"{distance:.4f}"
        )

    results.append(
        {
            "id": item["id"],
            "question": question,
            "expected_type": expected_type,
            "matched_keywords": matched_keywords,
            "missing_keywords": missing_keywords,
            "keyword_coverage": keyword_coverage,
            "retrieval_correct": retrieval_correct,
            "distances": distances,
        }
    )


retrieval_quality = (
    correct_questions / total_questions
    if total_questions > 0
    else 0
)


print("\n==============================")
print("Retrieval Quality Summary")
print("==============================")

print(
    f"Total questions: "
    f"{total_questions}"
)

print(
    f"Retrieval quality: "
    f"{retrieval_quality:.2%}"
)


output_path = (
    BASE_DIR
    / "retrieval_quality_results.json"
)


with output_path.open(
    "w",
    encoding="utf-8",
) as file:

    json.dump(
        {
            "total_questions": total_questions,
            "retrieval_quality": retrieval_quality,
            "results": results,
        },
        file,
        indent=2,
        ensure_ascii=False,
    )


print(
    "\nResults saved to:"
)

print(output_path)