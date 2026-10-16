from app.chunker import chunk_text


text = """
Object-oriented programming is a programming paradigm
based on objects and classes.

Inheritance allows a class to inherit attributes and
methods from another class.

Polymorphism allows objects of different classes to be
treated through a common interface.

Encapsulation is the bundling of data and methods
within a class.
"""


chunks = chunk_text(
    text,
    chunk_size=150,
    chunk_overlap=30,
)


print(f"Total chunks: {len(chunks)}")

for index, chunk in enumerate(chunks, start=1):
    print("\n==============================")
    print(f"Chunk {index}")
    print("==============================")
    print(chunk)