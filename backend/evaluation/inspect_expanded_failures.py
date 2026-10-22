import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

RESULTS_PATH = (
    BASE_DIR / "expanded_evaluation_results.json"
)


with RESULTS_PATH.open(
    "r",
    encoding="utf-8",
) as file:
    data = json.load(file)


print("\n==============================")
print("StudyMate AI")
print("Expanded Evaluation Failures")
print("==============================\n")


failures = []

for result in data["results"]:

    status = result["status"]
    correct = result["correct"]

    if status != "completed" or not correct:

        failures.append(result)


print(
    f"Total failures/errors: "
    f"{len(failures)}\n"
)


for result in failures:

    print("------------------------------")

    print(
        f"ID: {result['id']}"
    )

    print(
        f"Category: "
        f"{result['category']}"
    )

    print(
        f"Status: "
        f"{result['status']}"
    )

    print(
        f"Correct: "
        f"{result['correct']}"
    )

    print(
        f"Question: "
        f"{result['question']}"
    )

    print(
        f"Sources: "
        f"{result.get('sources')}"
    )

    if result.get("answer"):

        print("\nAnswer:")

        print(
            result["answer"]
        )

    if result.get("error"):

        print("\nError:")

        print(
            result["error"]
        )

    print()


print("==============================")
print("End of Failure Report")
print("==============================")