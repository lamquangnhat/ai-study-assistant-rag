import os

from dotenv import load_dotenv
from google import genai


# =========================
# Environment
# =========================

load_dotenv()


api_key = os.getenv(
    "GEMINI_API_KEY"
)

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is not set."
    )


# =========================
# Gemini Client
# =========================

client = genai.Client(
    api_key=api_key
)


MODEL_NAME = (
    "gemini-3.5-flash-lite"
)


# =========================
# Generate Answer
# =========================

def generate_answer(
    question: str,
    context: str,
    conversation_history: list[dict],
) -> str:
    """
    Generate an answer using:

    1. Retrieved study materials
    2. Conversation history
    3. Current user question
    """

    # =========================
    # Build conversation history
    # =========================

    history_text = ""

    for message in conversation_history:

        history_text += (
            f"{message['role']}: "
            f"{message['content']}\n"
        )

    # =========================
    # Prompt
    # =========================

    prompt = f"""
You are StudyMate AI, an AI Study Assistant.

Your job is to answer the user's question using
the provided study materials as evidence.

IMPORTANT RULES:

1. Use the provided study materials as the
   primary and only source of factual information.

2. Use conversation history only to understand
   what the user is referring to.

3. If the user uses words such as:
   "it", "its", "they", "them", "this", or "that",
   use the conversation history to determine what
   those words refer to.

4. You may combine, summarize, and paraphrase
   information from multiple retrieved passages.

5. The answer does NOT need to appear word-for-word
   in the context.

6. If the context contains enough related information
   to answer the question, answer the question directly.

7. If the context does not contain enough information
   to answer the question, say exactly:

"I could not find the answer in the provided study materials."

8. Do not use outside knowledge.

9. Do not invent facts.

10. Keep the answer concise and suitable for a student.

Conversation history:
----------------
{history_text}
----------------

Retrieved study materials:
----------------
{context}
----------------

Current user question:
----------------
{question}
----------------

Answer:
"""

    # =========================
    # Call Gemini
    # =========================

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    return response.text