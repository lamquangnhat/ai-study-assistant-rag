from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def create_embedding(text: str) -> list[float]:
    """
    Convert text into an embedding vector.
    """

    embedding = model.encode(text)

    return embedding.tolist()


def create_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Convert multiple texts into embedding vectors.
    """

    embeddings = model.encode(texts)

    return embeddings.tolist()