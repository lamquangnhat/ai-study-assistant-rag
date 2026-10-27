from pathlib import Path
import shutil

from fastapi import (
    FastAPI,
    HTTPException,
    UploadFile,
    File,
)
from fastapi.middleware.cors import CORSMiddleware

from app.rag_pipeline import answer_question

from app.schemas import (
    QuestionRequest,
    QuestionResponse,
    UploadResponse,
    DocumentSummary,
)

from app.ingestion import process_pdf
from app.embedding_service import create_embeddings

from app.vector_store import (
    add_chunks,
    get_documents,
    delete_chunks_by_source,
)


# =========================
# FastAPI App
# =========================

app = FastAPI(
    title="StudyMate AI",
    description=(
        "AI Study Assistant using "
        "Retrieval-Augmented Generation"
    ),
    version="0.4.0",
)


# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# Directories
# =========================

DOCUMENTS_DIR = Path(
    "/app/data/documents"
)

DOCUMENTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# =========================
# Root
# =========================

@app.get("/")
def root():
    return {
        "message": (
            "StudyMate AI is ready to learn!"
        ),
        "version": "0.4.0",
    }


# =========================
# Ask Question
# =========================

@app.post(
    "/ask",
    response_model=QuestionResponse,
)
def ask_question(
    request: QuestionRequest,
):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    result = answer_question(
        question=request.question,
        top_k=3,
        conversation_history=[
            message.model_dump()
            for message in request.conversation_history
        ],
    )

    return result


# =========================
# Upload PDF
# =========================

@app.post(
    "/upload",
    response_model=UploadResponse,
)
def upload_pdf(
    file: UploadFile = File(...),
):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected.",
        )

    if not file.filename.lower().endswith(
        ".pdf"
    ):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed.",
        )

    # Keep only the filename.
    # This prevents accidental path traversal.
    safe_filename = Path(
        file.filename
    ).name

    file_path = (
        DOCUMENTS_DIR / safe_filename
    )

    # Save PDF
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer,
        )

    # Extract + chunk
    chunks = process_pdf(
        str(file_path)
    )

    if not chunks:
        raise HTTPException(
            status_code=400,
            detail=(
                "Could not extract text "
                "from the PDF."
            ),
        )

    # Create embeddings
    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = create_embeddings(
        texts
    )

    # Store in ChromaDB.
    # Existing chunks from the same
    # source are removed first.
    add_chunks(
        chunks=chunks,
        embeddings=embeddings,
    )

    return {
        "filename": safe_filename,
        "total_chunks": len(chunks),
        "message": (
            "PDF uploaded and indexed successfully."
        ),
    }


# =========================
# Get Documents
# =========================

@app.get(
    "/documents",
    response_model=list[DocumentSummary],
)
def list_documents():

    documents = get_documents()

    return documents


# =========================
# Delete Document
# =========================

@app.delete(
    "/documents/{filename}",
)
def delete_document(
    filename: str,
):

    # Only keep the filename.
    # Never accept or use a local path
    # from the user's computer.
    safe_filename = Path(
        filename
    ).name

    documents = get_documents()

    document_exists = any(
        document["filename"]
        == safe_filename
        for document in documents
    )

    if not document_exists:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    # =================================
    # Remove StudyMate's indexed data
    # =================================

    delete_chunks_by_source(
        safe_filename
    )

    # =================================
    # Remove StudyMate's PDF copy
    # =================================

    file_path = (
        DOCUMENTS_DIR / safe_filename
    )

    if file_path.exists():
        file_path.unlink()

    # =================================
    # Important:
    # The original PDF on the user's
    # computer is never accessed or deleted.
    # =================================

    return {
        "filename": safe_filename,
        "message": (
            "Document removed from "
            "StudyMate AI. "
            "Your original PDF was not affected."
        ),
    }