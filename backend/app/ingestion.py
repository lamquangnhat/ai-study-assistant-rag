from pathlib import Path

from app.chunker import chunk_text
from app.document_processor import extract_text_from_pdf


def process_pdf(file_path: str) -> list[dict]:
    """
    Extract text from a PDF and split it into chunks.

    Each chunk keeps its source page number.
    """

    pages = extract_text_from_pdf(file_path)

    chunks = []

    for page in pages:
        page_chunks = chunk_text(page["text"])

        for chunk_index, chunk in enumerate(page_chunks, start=1):
            chunks.append(
                {
                    "text": chunk,
                    "page_number": page["page_number"],
                    "chunk_index": chunk_index,
                    "source": Path(file_path).name,
                }
            )

    return chunks