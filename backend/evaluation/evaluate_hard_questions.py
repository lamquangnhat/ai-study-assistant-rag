import json
import time
from pathlib import Path

from google.genai.errors import ServerError

from app.rag_pipeline import answer_question


BASE_DIR = Path(__file__).resolve().parent

DATASET_PATH = (
    BASE_DIR / "evaluation_dataset.json"
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
print("Hard Question Evaluation")
print("==============================\n")


correct = 0
llm_errors = 0
total = len(dataset)

results = []


for item in dataset:

    question = item["question"]
    expected_type = item["expected_type"]

    print("------------------------------")
    print(f"Question: {question}")
    print(f"Expected: {expected_type}")

    result = None
    llm_error = None

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

            llm_error = str(error)

            print(
                f"\nGemini 503 error."
                f" Attempt "
                f"{attempt}/{MAX_RETRIES}"
            )

            if attempt < MAX_RETRIES:

                print(
                    f"Waiting "
                    f"{RETRY_DELAY_SECONDS} "
                    f"seconds before retry..."
                )

                time.sleep(
                    RETRY_DELAY_SECONDS
                )


    # Gemini failed after all retries
    if result is None:

        llm_errors += 1

        print("\nLLM Error")
        print(
            "Gemini was unavailable "
            "after all retry attempts."
        )

        results.append(
            {
                "id": item["id"],
                "question": question,
                "expected_type": expected_type,
                "status": "llm_error",
                "sources": None,
                "correct": None,
                "answer": None,
                "error": llm_error,
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

    print("\nDistances:")

    for source in sources:

        print(
            f"  Page "
            f"{source['page_number']} "
            f"| Distance "
            f"{source['distance']:.4f}"
        )


    results.append(
        {
            "id": item["id"],
            "question": question,
            "expected_type": expected_type,
            "status": "completed",
            "sources": len(sources),
            "correct": is_correct,
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
print("Hard Question Summary")
print("==============================")

print(
    f"Total questions: {total}"
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
    f"Accuracy among completed: "
    f"{accuracy:.2%}"
)


output_path = (
    BASE_DIR
    / "hard_question_results.json"
)


with output_path.open(
    "w",
    encoding="utf-8",
) as file:

    json.dump(
        {
            "total_questions": total,
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