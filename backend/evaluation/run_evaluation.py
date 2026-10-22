import json
from pathlib import Path

from app.rag_pipeline import answer_question


# =========================
# Paths
# =========================

BASE_DIR = Path(__file__).resolve().parent

DATASET_PATH = (
    BASE_DIR / "evaluation_dataset.json"
)


# =========================
# Load Dataset
# =========================

with DATASET_PATH.open(
    "r",
    encoding="utf-8",
) as file:

    dataset = json.load(file)


# =========================
# Evaluation
# =========================

results = []

correct_retrieval = 0
correct_answer_type = 0


print("\n==============================")
print("StudyMate AI - RAG Evaluation")
print("==============================\n")


for item in dataset:

    question = item["question"]

    expected_type = item["expected_type"]

    expected_keywords = [
        keyword.lower()
        for keyword in item["expected_keywords"]
    ]

    print("------------------------------")
    print(f"Question: {question}")
    print(f"Expected: {expected_type}")

    # Run RAG
    result = answer_question(
        question=question,
        top_k=3,
    )

    answer = result["answer"]

    sources = result["sources"]

    answer_lower = answer.lower()

    # =========================
    # Retrieval Evaluation
    # =========================

    has_sources = len(sources) > 0

    if expected_type == "answerable":

        retrieval_correct = has_sources

    else:

        retrieval_correct = not has_sources

    if retrieval_correct:
        correct_retrieval += 1

    # =========================
    # Answer Evaluation
    # =========================

    if expected_type == "answerable":

        keyword_matches = sum(
            keyword in answer_lower
            for keyword in expected_keywords
        )

        answer_correct = (
            keyword_matches
            >= max(
                1,
                len(expected_keywords) // 2,
            )
        )

    else:

        answer_correct = (
            "could not find the answer"
            in answer_lower
        )

    if answer_correct:
        correct_answer_type += 1

    # =========================
    # Result
    # =========================

    print(
        f"Retrieved sources: "
        f"{len(sources)}"
    )

    print(
        f"Retrieval correct: "
        f"{retrieval_correct}"
    )

    print(
        f"Answer correct: "
        f"{answer_correct}"
    )

    print("\nAnswer:")
    print(answer)

    results.append(
        {
            "id": item["id"],
            "question": question,
            "expected_type": expected_type,
            "retrieved_sources": len(sources),
            "retrieval_correct": retrieval_correct,
            "answer_correct": answer_correct,
            "answer": answer,
        }
    )


# =========================
# Metrics
# =========================

total = len(dataset)

retrieval_accuracy = (
    correct_retrieval / total
    if total > 0
    else 0
)

answer_accuracy = (
    correct_answer_type / total
    if total > 0
    else 0
)


# =========================
# Summary
# =========================

print("\n==============================")
print("Evaluation Summary")
print("==============================")

print(
    f"Total questions: {total}"
)

print(
    f"Retrieval accuracy: "
    f"{retrieval_accuracy:.2%}"
)

print(
    f"Answer accuracy: "
    f"{answer_accuracy:.2%}"
)


# =========================
# Save Results
# =========================

output_path = (
    BASE_DIR / "evaluation_results.json"
)

with output_path.open(
    "w",
    encoding="utf-8",
) as file:

    json.dump(
        {
            "total_questions": total,
            "retrieval_accuracy": retrieval_accuracy,
            "answer_accuracy": answer_accuracy,
            "results": results,
        },
        file,
        indent=2,
        ensure_ascii=False,
    )


print(
    f"\nResults saved to:"
    f"\n{output_path}"
)