import numpy as np
from signature.key_generation import generate_key_pair
from linear_sketch.linear_sketch import LinearSketch

def test_key_generation_with_fingerprints():
    """
    Test the entire pipeline: generate sketches for fingerprints and then generate keys.
    """
    # Load preprocessed fingerprint data
    fingerprint_1_vector = np.load("data/processed/fingerprints/fingerprint_1_processed.npy")
    fingerprint_2_vector = np.load("data/processed/fingerprints/fingerprint_2_processed.npy")

    # Define lattice basis (example basis, securely generated in a real system)
    lattice_basis = np.array([[3.0, 0.0], [1.5, 2.6]])

    # Instantiate the linear sketch algorithm
    basis_length = 40.0  # You can adjust this parameter as needed
    linear_sketch = LinearSketch(basis_length=40.0)

    # Generate sketches for fingerprints
    fingerprint_1_sketch, fingerprint_1_residue = linear_sketch.project_to_lattice(fingerprint_1_vector)
    fingerprint_2_sketch, fingerprint_2_residue = linear_sketch.project_to_lattice(fingerprint_2_vector)

    print(f"Fingerprint 1 Sketch: {fingerprint_1_sketch}, Residue: {fingerprint_1_residue}")
    print(f"Fingerprint 2 Sketch: {fingerprint_2_sketch}, Residue: {fingerprint_2_residue}")

    # Generate key pair for Fingerprint 1
    key_pair_1 = generate_key_pair(fingerprint_1_sketch, lattice_basis)
    print("\nFingerprint 1 Key Pair:")
    print(f"Private Key: {key_pair_1['private_key'].d}")
    print(f"Public Key: {key_pair_1['public_key'].pointQ}")

    # Generate key pair for Fingerprint 2
    key_pair_2 = generate_key_pair(fingerprint_2_sketch, lattice_basis)
    print("\nFingerprint 2 Key Pair:")
    print(f"Private Key: {key_pair_2['private_key'].d}")
    print(f"Public Key: {key_pair_2['public_key'].pointQ}")

if __name__ == "__main__":
    test_key_generation_with_fingerprints()
