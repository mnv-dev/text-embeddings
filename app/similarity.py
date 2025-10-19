import numpy as np

def cosine_similarity(vec1, vec2):
    # Formula = cos_sim(A, B) = (A . B) / (||A|| * ||B||)
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    dot_product = np.dot(vec1, vec2)
    norm_a = np.linalg.norm(vec1)
    norm_b = np.linalg.norm(vec2)

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)

def euclidean_distance(vec1, vec2):
    vec1, vec2 = np.array(vec1), np.array(vec2)
    return np.linalg.norm(vec1 - vec2)

def dot_product_similarity(vec1, vec2):
    vec1, vec2 = np.array(vec1), np.array(vec2)
    return np.dot(vec1, vec2)


