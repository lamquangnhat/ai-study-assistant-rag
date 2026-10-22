from rag_pipeline import answer_question


question = "What is Retrieval-Augmented Generation?"


result = answer_question(question)


print("\n===== QUESTION =====")
print(result["question"])


print("\n===== ANSWER =====")
print(result["answer"])


print("\n===== SOURCES =====")

for source in result["sources"]:
    print(
        f"- {source['source']} | "
        f"Page {source['page_number']} | "
        f"Chunk {source['chunk_index']}"
    )