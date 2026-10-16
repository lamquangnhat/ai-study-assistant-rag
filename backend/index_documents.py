from app.ingestion import process_pdf
from app.embedding_service import create_embeddings
from app.vector_store import add_chunks


PDF_PATH = "../data/documents/Week01_AI_Study_Assistant_Lecture.pdf"


print("Processing PDF...")

chunks = process_pdf(PDF_PATH)

print(f"Total chunks: {len(chunks)}")


texts = [chunk["text"] for chunk in chunks]


print("Creating embeddings...")

embeddings = create_embeddings(texts)

print(f"Created {len(embeddings)} embeddings")


print("Storing data in ChromaDB...")

add_chunks(
    chunks=chunks,
    embeddings=embeddings,
)


print("Documents successfully indexed!")