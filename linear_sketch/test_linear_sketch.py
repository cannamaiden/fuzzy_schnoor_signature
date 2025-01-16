import numpy as np
from linear_sketch import LinearSketch

# Test LinearSketch with real fingerprint data
def test_dynamic_radius_with_real_fingerprints():
    """
    Test the LinearSketch implementation with real fingerprint data
    and dynamic radius adjustment logic.
    """
    # Load processed fingerprints
    fingerprint_1 = np.load("../data/processed/fingerprints/fingerprint_1_processed.npy")
    fingerprint_2 = np.load("../data/processed/fingerprints/fingerprint_2_processed.npy")

    # Initialize LinearSketch with basis vectors and modulus
    basis_vectors = [[1, 0], [0.5, np.sqrt(3) / 2]]
    modulus = 7
    default_radius = 5.0

    linear_sketch = LinearSketch(basis_vectors, modulus, default_radius)

    # Generate sketches for the fingerprints
    sketch_1, proxy_key_1 = linear_sketch.sketch(fingerprint_1)
    sketch_2, proxy_key_2 = linear_sketch.sketch(fingerprint_2)

    print(f"Fingerprint 1 Sketch (c1): {sketch_1}, Proxy Key (a1): {proxy_key_1}")
    print(f"Fingerprint 2 Sketch (c2): {sketch_2}, Proxy Key (a2): {proxy_key_2}")

    # Verify acceptance with dynamic radius adjustment
    similarity_score = 0.8  # Example similarity score (higher is better)
    noise_level = 0.1  # Example noise level (higher means noisier)

    is_accepted = linear_sketch.verify_acceptance(
        fingerprint_1, fingerprint_2, similarity_score=similarity_score, noise_level=noise_level
    )

    print(f"Fingerprint 2 Within Acceptance Region of Fingerprint 1: {is_accepted}")

    # Test dynamic radius adjustment
    dynamic_radius = linear_sketch.dynamic_radius_adjustment(
        similarity_score, noise_level, min_radius=2.0, max_radius=15.0
    )

    print(f"Dynamically Adjusted Radius: {dynamic_radius}")

    # Test DiffRec functionality
    delta_a = linear_sketch.diff_rec(sketch_1, sketch_2)
    print(f"Recovered \u0394a (Difference in Proxy Keys): {delta_a}")

if __name__ == "__main__":
    test_dynamic_radius_with_real_fingerprints()
