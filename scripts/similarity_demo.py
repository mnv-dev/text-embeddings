import os
from app.embeddings import EmbeddingGenerator
from app.similarity import cosine_similarity, dot_product_similarity, euclidean_distance


def load_sentences(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
    return [ln for ln in lines if ln]

def find_top_k_similar(query_vector, sentence_embeddings, sentences, top_k=3):
    similarities = []
    sort_desc = None
    for i, embedding in enumerate(sentence_embeddings):
        # Cosine
        sim_score = cosine_similarity(query_vector, embedding)
        sort_desc=True

        # Dot-Product
        # sim_score = dot_product_similarity(query_vector, embedding)
        # sort_desc = True

        # Euclidean
        # sim_score = euclidean_distance(query_vector, embedding)
        # sort_desc = False

        similarities.append((sentences[i], sim_score))

    similarities.sort(key=lambda x: x[1], reverse=sort_desc)
    return similarities[:top_k]

def main():
    embedder = EmbeddingGenerator()

    base_dir = os.path.dirname(os.path.dirname(__file__))
    sentences_file = os.path.join(base_dir, "sample_sentences.txt")
    sentences = load_sentences(sentences_file)
    print(f"Loaded {len(sentences)} sentences")

    print("Generating embeddings..")
    sentence_embeddings = embedder.generate_embeddings(sentences)
    print("Embeddings generated successfully!!")

    while True:
        query = input("\nEnter your query sentence or type exit to quit:: ").strip()
        if query.lower() == "exit":
            print("bye!!!")
            break

        if not query:
            print("Please enter a valid sentence!!")
            continue

        query_embedding = embedder.generate_embedding(query)
        top_results = find_top_k_similar(query_embedding, sentence_embeddings, sentences, top_k=3)

        print("\nTop 3 most similar sentences:")
        for i, (text, score) in enumerate(top_results, start=1):
            print(f"{i}. {text}  (score = {score:.4f})")

if __name__ == "__main__":
    main()
