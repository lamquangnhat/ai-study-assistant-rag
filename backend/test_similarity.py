from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer("all-MiniLM-L6-v2")


sentences = [
    "Inheritance allows a class to inherit methods from another class.",
    "A child class can receive behaviour from its parent class.",
    "The weather is very hot today.",
]


embeddings = model.encode(sentences)


similarity_1 = cosine_similarity(
    [embeddings[0]],
    [embeddings[1]],
)[0][0]


similarity_2 = cosine_similarity(
    [embeddings[0]],
    [embeddings[2]],
)[0][0]


print("Similarity between sentence 1 and sentence 2:")
print(similarity_1)

print("\nSimilarity between sentence 1 and sentence 3:")
print(similarity_2)