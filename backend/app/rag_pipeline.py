from app.embedding_service import create_embedding
from app.vector_store import search_chunks
from app.llm_service import generate_answer


DISTANCE_THRESHOLD = 1.5


def build_retrieval_query(
    question: str,
    conversation_history: list[dict],
) -> str:
    """
    Build a retrieval query using the current question
    and previous user messages.

    This helps resolve follow-up questions such as:
    "What are its main components?"
    where "its" refers to a topic from earlier
    in the conversation.
    """

    previous_questions = []

    for message in conversation_history:

        if message["role"] == "user":
            previous_questions.append(
                message["content"]
            )

    # Keep only the most recent user questions
    # to avoid making the retrieval query too large.
    previous_questions = previous_questions[-3:]

    if not previous_questions:
        return question

    retrieval_query = "\n".join(
        previous_questions + [question]
    )

    return retrieval_query


def answer_question(
    question: str,
    conversation_history: list[dict],
    top_k: int = 3,
) -> dict:
    """
    Retrieve relevant chunks and generate an answer.

    Conversation history is used to improve retrieval
    for follow-up questions.
    """

    # =========================
    # Step 1: Build retrieval query
    # =========================

    retrieval_query = build_retrieval_query(
        question=question,
        conversation_history=conversation_history,
    )

    # =========================
    # Step 2: Create embedding
    # =========================

    query_embedding = create_embedding(
        retrieval_query
    )

    # =========================
    # Step 3: Search ChromaDB
    # =========================

    results = search_chunks(
        query_embedding=query_embedding,
        top_k=top_k,
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    # =========================
    # Step 4: Check results
    # =========================

    if not documents or not distances:
        return {
            "question": question,
            "answer": (
                "I could not find the answer in the "
                "provided study materials."
            ),
            "sources": [],
        }

    # =========================
    # Step 5: Check relevance
    # =========================

    best_distance = distances[0]

    if best_distance > DISTANCE_THRESHOLD:
        return {
            "question": question,
            "answer": (
                "I could not find the answer in the "
                "provided study materials."
            ),
            "sources": [],
        }

    # =========================
    # Step 6: Build context
    # =========================

    context_parts = []
    sources = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances,
    ):

        if distance <= DISTANCE_THRESHOLD:

            context_parts.append(
                f"[Source: {metadata['source']}, "
                f"Page: {metadata['page_number']}]\n"
                f"{document}"
            )

            sources.append(
                {
                    "source": metadata["source"],
                    "page_number": metadata["page_number"],
                    "chunk_index": metadata["chunk_index"],
                    "distance": distance,
                }
            )

    # =========================
    # Step 7: Combine context
    # =========================

    context = "\n\n".join(
        context_parts
    )

    # =========================
    # Step 8: Generate answer
    # =========================

    answer = generate_answer(
        question=question,
        context=context,
        conversation_history=conversation_history,
    )

    # =========================
    # Step 9: Return result
    # =========================

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
    }