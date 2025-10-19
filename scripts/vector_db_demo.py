import os

from app.embeddings import EmbeddingGenerator
from app.qdrant_utils import initialize_collection

def load_sentences(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
    return [ln for ln in lines if ln]

def main():
    print("Starting Qdrant Vector DB Demo")

    embedder = EmbeddingGenerator()
    store = initialize_collection()

    base_dir = os.path.dirname(os.path.dirname(__file__))
    sentences_file = os.path.join(base_dir, "sample_sentences.txt")

    sentences = load_sentences(sentences_file)
    print(f"Loaded {len(sentences)} sentences from file")

    print("Generating embeddings (this may take a minute)..")
    embeddings = embedder.generate_embeddings(sentences)
    print(f"Generated {len(embeddings)} embeddings")

    print("Inserting embeddings into Qdrant collection..")
    store.insert_embeddings(texts=sentences, embeddings=embeddings)
    print("Embeddings inserted successfully!")

    print("\nEnter a query to find similar sentences (type 'exit' to quit)")
    while True:
        query = input("\nEnter your query: ").strip()
        if query.lower() == "exit":
            print("Exiting demo.")
            break

        if not query:
            print("Please enter a non-empty query.")
            continue

        query_embedding = embedder.generate_embedding(query)

        print(f"Searching for top 3 most similar sentences..")
        results = store.search_similar_texts(query_vector=query_embedding, top_k=3)

        if not results:
            print("⚠No results found.")
            continue

        print("\nTop 3 similar sentences:")
        for i, hit in enumerate(results, start=1):
            print(f"{i}. {hit['text']}  (score={hit['score']:.4f})")

if __name__ == "__main__":
    main()
