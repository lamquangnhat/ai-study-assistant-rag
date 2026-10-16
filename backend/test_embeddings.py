from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")


text = "Inheritance allows a class to inherit attributes and methods from another class."


embedding = model.encode(text)


print("Text:")
print(text)

print("\nEmbedding:")
print(embedding)

print("\nEmbedding dimensions:")
print(len(embedding))