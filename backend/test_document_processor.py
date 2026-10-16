from app.document_processor import extract_text_from_pdf


PDF_PATH = "../data/documents/Week01_AI_Study_Assistant_Lecture.pdf"


pages = extract_text_from_pdf(PDF_PATH)

print(f"Total pages: {len(pages)}")

for page in pages[:3]:
    print("\n==============================")
    print(f"Page: {page['page_number']}")
    print("==============================")
    print(page["text"][:1000])