from app.rag_pipeline import answer_question


def test_conversation_follow_up_question():
    """
    Test whether StudyMate AI can use conversation history
    to understand a follow-up question.
    """

    conversation_history = [
        {
            "role": "user",
            "content": "What is RAG?",
        },
        {
            "role": "assistant",
            "content": (
                "RAG stands for Retrieval-Augmented Generation. "
                "It is a system that retrieves relevant information "
                "from a knowledge base and provides that context "
                "to a language model."
            ),
        },
        {
            "role": "user",
            "content": (
                "Why is RAG useful for a study assistant?"
            ),
        },
        {
            "role": "assistant",
            "content": (
                "RAG is useful because it allows a study assistant "
                "to retrieve information from the student's own "
                "study materials before generating an answer."
            ),
        },
    ]

    result = answer_question(
        question="What are its main components?",
        conversation_history=conversation_history,
        top_k=3,
    )

    # The pipeline should return a valid answer.
    assert result["question"] == (
        "What are its main components?"
    )

    assert isinstance(
        result["answer"],
        str,
    )

    assert len(
        result["answer"].strip()
    ) > 0

    # The answer should not be the fallback response.
    assert (
        result["answer"]
        != "I could not find the answer in the "
        "provided study materials."
    )

    # The system should retrieve at least one source.
    assert len(
        result["sources"]
    ) > 0

    # The retrieved source should contain
    # the lecture PDF used by this project.
    assert any(
        source["source"]
        == "Week01_AI_Study_Assistant_Lecture.pdf"
        for source in result["sources"]
    )