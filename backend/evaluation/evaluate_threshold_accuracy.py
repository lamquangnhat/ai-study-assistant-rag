from app.embedding_service import create_embedding
from app.vector_store import search_chunks


TEST_CASES = [
    {
        "question": "What is Retrieval-Augmented Generation?",
        "answerable": True,
    },
    {
        "question": "What is the purpose of chunking documents?",
        "answerable": True,
    },
    {
        "question": "What are embeddings used for in a RAG system?",
        "answerable": True,
    },
    {
        "question": "What is a vector database?",
        "answerable": True,
    },
    {
        "question": "What is the capital of France?",
        "answerable": False,
    },
    {
        "question": "Who is the president of the United States?",
        "answerable": False,
    },
    {
        "question": "What is the tallest mountain in the world?",
        "answerable": False,
    },
]


THRESHOLDS = [
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
print("Threshold Accuracy Evaluation")
print("==============================\n")


# ---------------------------------
# Retrieve best distance for each question
# ---------------------------------

question_results = []


for test_case in TEST_CASES:

    question = test_case["question"]

    answerable = test_case["answerable"]

    query_embedding = create_embedding(
        question
    )

    results = search_chunks(
        query_embedding=query_embedding,
        top_k=3,
    )

    distances = results["distances"][0]

    best_distance = distances[0]

    question_results.append(
        {
            "question": question,
            "answerable": answerable,
            "best_distance": best_distance,
        }
    )


# ---------------------------------
# Evaluate every threshold
# ---------------------------------

best_threshold = None
best_accuracy = -1


print(
    "Threshold | TP | TN | FP | FN | Accuracy"
)

print(
    "----------|----|----|----|----|---------"
)


for threshold in THRESHOLDS:

    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0

    for result in question_results:

        predicted_answerable = (
            result["best_distance"]
            <= threshold
        )

        actual_answerable = (
            result["answerable"]
        )

        if (
            actual_answerable
            and predicted_answerable
        ):
            true_positive += 1

        elif (
            not actual_answerable
            and not predicted_answerable
        ):
            true_negative += 1

        elif (
            not actual_answerable
            and predicted_answerable
        ):
            false_positive += 1

        elif (
            actual_answerable
            and not predicted_answerable
        ):
            false_negative += 1

    total = (
        true_positive
        + true_negative
        + false_positive
        + false_negative
    )

    accuracy = (
        (
            true_positive
            + true_negative
        )
        / total
        if total > 0
        else 0
    )

    print(
        f"{threshold:8.1f} | "
        f"{true_positive:2d} | "
        f"{true_negative:2d} | "
        f"{false_positive:2d} | "
        f"{false_negative:2d} | "
        f"{accuracy:8.2%}"
    )

    if accuracy > best_accuracy:

        best_accuracy = accuracy

        best_threshold = threshold


print("\n==============================")
print("Best Threshold")
print("==============================")

print(
    f"Threshold: {best_threshold:.1f}"
)

print(
    f"Accuracy: {best_accuracy:.2%}"
)