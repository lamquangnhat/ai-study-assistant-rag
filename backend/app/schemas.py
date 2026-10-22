from pydantic import BaseModel
from typing import Literal


# ============================================================
# Conversation / Chat
# ============================================================

class ChatMessage(BaseModel):
    """
    Represents one message in the conversation history.
    """
    role: Literal["user", "assistant"]
    content: str


# ============================================================
# Question / RAG
# ============================================================

class QuestionRequest(BaseModel):
    """
    Request sent to the /ask endpoint.
    """
    question: str
    conversation_history: list[ChatMessage] = []


class Source(BaseModel):
    """
    Represents one source chunk retrieved from the vector database.
    """
    source: str
    page_number: int
    chunk_index: int
    distance: float


class QuestionResponse(BaseModel):
    """
    Response returned by the /ask endpoint.
    """
    question: str
    answer: str
    sources: list[Source]


# ============================================================
# Upload
# ============================================================

class UploadResponse(BaseModel):
    """
    Response returned after uploading and processing a document.
    """
    filename: str
    total_chunks: int
    message: str


# ============================================================
# Documents
# ============================================================

class DocumentSummary(BaseModel):
    """
    Summary information about an uploaded document.
    """
    filename: str
    total_chunks: int