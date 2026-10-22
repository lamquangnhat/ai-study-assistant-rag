import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def load_json(filename: str):
    path = BASE_DIR / filename

    if not path.exists():
        return None

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


baseline = load_json(
    "evaluation_results.json"
)

retrieval_quality = load_json(
    "retrieval_quality_results.json"
)

hard_questions = load_json(
    "hard_question_results.json"
)

expanded = load_json(
    "expanded_evaluation_results.json"
)


report = {
    "project": "StudyMate AI",

    "evaluation": {
        "baseline": baseline,
        "retrieval_quality": retrieval_quality,
        "hard_questions": hard_questions,
        "expanded_dataset": expanded,
    },

    "findings": {
        "strengths": [
            "Direct questions were answered successfully.",
            "Paraphrased questions were handled successfully.",
            "Out-of-scope questions were rejected correctly.",
            "Semantic retrieval returned relevant lecture chunks.",
            "Duplicate test-document retrieval was removed.",
        ],

        "limitations": [
            "Multi-concept questions can be more difficult.",
            "Hard reasoning questions can cause generation failures.",
            "Gemini availability can affect evaluation through temporary 503 errors.",
            "The evaluation dataset is still relatively small.",
        ],

        "threshold": {
            "production_threshold": 1.5,
            "best_threshold_on_current_small_dataset": 1.2,
            "note": (
                "The production threshold remains 1.5 "
                "because several thresholds performed "
                "perfectly on the small benchmark."
            ),
        },
    },
}


output_path = (
    BASE_DIR
    / "final_evaluation_report.json"
)


with output_path.open(
    "w",
    encoding="utf-8",
) as file:

    json.dump(
        report,
        file,
        indent=2,
        ensure_ascii=False,
    )


print("\n==============================")
print("StudyMate AI")
print("Final Evaluation Report")
print("==============================\n")


print("Project:")
print("StudyMate AI")

print("\nEvaluation files included:")

print(
    f"- Baseline: "
    f"{baseline is not None}"
)

print(
    f"- Retrieval quality: "
    f"{retrieval_quality is not None}"
)

print(
    f"- Hard questions: "
    f"{hard_questions is not None}"
)

print(
    f"- Expanded dataset: "
    f"{expanded is not None}"
)


if expanded:

    print("\nExpanded Dataset:")
    print(
        f"Total: "
        f"{expanded['total_questions']}"
    )

    print(
        f"Completed: "
        f"{expanded['completed']}"
    )

    print(
        f"LLM errors: "
        f"{expanded['llm_errors']}"
    )

    print(
        f"Correct: "
        f"{expanded['correct']}"
    )

    print(
        f"Accuracy: "
        f"{expanded['accuracy']:.2%}"
    )


print("\nFinal report saved to:")

print(output_path)