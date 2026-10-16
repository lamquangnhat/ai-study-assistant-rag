from app.ingestion import process_pdf


PDF_PATH = "../data/documents/Week01_AI_Study_Assistant_Lecture.pdf"


chunks = process_pdf(PDF_PATH)

print(f"Total chunks: {len(chunks)}")

for index, chunk in enumerate(chunks[:5], start=1):
    print("\n==============================")
    print(f"Chunk {index}")
    print("==============================")
    print(f"Source: {chunk['source']}")
    print(f"Page: {chunk['page_number']}")
    print(f"Chunk index: {chunk['chunk_index']}")
    print(f"Text: {chunk['text'][:500]}")