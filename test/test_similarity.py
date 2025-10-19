import math
from app.similarity import cosine_similarity

def test_cosine_identical_is_one():
    a = [1, 2, 3]
    assert math.isclose(cosine_similarity(a, a), 1.0, rel_tol=1e-9, abs_tol=1e-12)

def test_cosine_orthogonal_is_zero():
    a = [1, 0]
    b = [0, 1]
    assert math.isclose(cosine_similarity(a, b), 0.0, rel_tol=1e-9, abs_tol=1e-12)

def test_cosine_opposite_is_minus_one():
    a = [1, 0]
    b = [-1, 0]
    assert math.isclose(cosine_similarity(a, b), -1.0, rel_tol=1e-9, abs_tol=1e-12)

def test_cosine_zero_vector_guard():
    a = [0, 0, 0]
    b = [1, 2, 3]
    assert math.isclose(cosine_similarity(a, b), 0.0, rel_tol=1e-9, abs_tol=1e-12)
    assert math.isclose(cosine_similarity(b, a), 0.0, rel_tol=1e-9, abs_tol=1e-12)

def test_cosine_scale_invariance_and_symmetry():
    a = [1, 2, 3]
    b = [4, 5, 6]
    k = -3.7
    cos_ab = cosine_similarity(a, b)
    cos_ba = cosine_similarity(b, a)
    cos_scaled = cosine_similarity([k*x for x in a], [k*y for y in b])
    assert math.isclose(cos_ab, cos_ba, rel_tol=1e-9, abs_tol=1e-12)
    assert math.isclose(cos_ab, cos_scaled, rel_tol=1e-9, abs_tol=1e-12)