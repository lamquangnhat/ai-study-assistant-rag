import json
from pathlib import Path
import time

from google.genai.errors import ServerError

from app.rag_pipeline import answer_question


BASE_DIR = Path(__file__).resolve().parent

DATASET_PATH = (
    BASE_DIR / "evaluation_dataset_expanded.json"
)


with DATASET_PATH.open(
    "r",
    encoding="utf-8",
) as file:
    dataset = json.load(file)


MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 5


print("\n==============================")
print("StudyMate AI")
print("Expanded RAG Evaluation")
print("==============================\n")


results = []

correct = 0
llm_errors = 0


for item in dataset:

    question = item["question"]
    expected_type = item["expected_type"]
    category = item["category"]

    print("------------------------------")
    print(f"ID: {item['id']}")
    print(f"Category: {category}")
    print(f"Question: {question}")
    print(f"Expected: {expected_type}")

    result = None
    error_message = None


    for attempt in range(
        1,
        MAX_RETRIES + 1,
    ):

        try:

            result = answer_question(
                question=question,
                top_k=3,
            )

            break

        except ServerError as error:

            error_message = str(error)

            print(
                f"Gemini 503 error "
                f"({attempt}/{MAX_RETRIES})"
            )

            if attempt < MAX_RETRIES:

                time.sleep(
                    RETRY_DELAY_SECONDS
                )


    if result is None:

        llm_errors += 1

        print("LLM Error")

        results.append(
            {
                "id": item["id"],
                "category": category,
                "question": question,
                "expected_type": expected_type,
                "status": "llm_error",
                "correct": None,
                "sources": None,
                "answer": None,
                "error": error_message,
            }
        )

        continue


    answer = result["answer"]
    sources = result["sources"]

    answer_lower = answer.lower()

    has_sources = len(sources) > 0


    if expected_type == "answerable":

        is_correct = (
            has_sources
            and
            "could not find the answer"
            not in answer_lower
        )

    else:

        is_correct = (
            not has_sources
            and
            "could not find the answer"
            in answer_lower
        )


    if is_correct:

        correct += 1


    print(
        f"Sources: {len(sources)}"
    )

    print(
        f"Correct: {is_correct}"
    )

    print("\nAnswer:")
    print(answer)


    results.append(
        {
            "id": item["id"],
            "category": category,
            "question": question,
            "expected_type": expected_type,
            "status": "completed",
            "correct": is_correct,
            "sources": len(sources),
            "answer": answer,
        }
    )


completed_results = [
    result
    for result in results
    if result["status"] == "completed"
]


completed_total = len(
    completed_results
)


accuracy = (
    correct / completed_total
    if completed_total > 0
    else 0
)


print("\n==============================")
print("Overall Summary")
print("==============================")


print(
    f"Total questions: {len(dataset)}"
)

print(
    f"Completed: {completed_total}"
)

print(
    f"LLM errors: {llm_errors}"
)

print(
    f"Correct: {correct}"
)

print(
    f"Accuracy: {accuracy:.2%}"
)


print("\n==============================")
print("Category Summary")
print("==============================")


categories = sorted(
    set(
        item["category"]
        for item in dataset
    )
)


for category in categories:

    category_results = [
        result
        for result in completed_results
        if result["category"]
        == category
    ]

    category_correct = sum(
        result["correct"]
        for result in category_results
    )

    category_total = len(
        category_results
    )

    category_accuracy = (
        category_correct
        / category_total
        if category_total > 0
        else 0
    )

    print(
        f"{category:15} "
        f"{category_correct}/"
        f"{category_total} "
        f"({category_accuracy:.2%})"
    )


output_path = (
    BASE_DIR
    / "expanded_evaluation_results.json"
)


with output_path.open(
    "w",
    encoding="utf-8",
) as file:

    json.dump(
        {
            "total_questions": len(dataset),
            "completed": completed_total,
            "llm_errors": llm_errors,
            "correct": correct,
            "accuracy": accuracy,
            "results": results,
        },
        file,
        indent=2,
        ensure_ascii=False,
    )


print("\nResults saved to:")

print(output_path)