import numpy as np
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.backends import default_backend

class LinearSketch:
    def __init__(self, basis_vectors, modulus, default_radius=5.0):
        self.basis_vectors = np.array(basis_vectors)
        self.modulus = modulus
        self.default_radius = default_radius

    def g_L(self, vector, tolerance=1e-6):
        lattice_coords = np.linalg.solve(self.basis_vectors.T, vector)
        rounded_coords = np.round(lattice_coords / tolerance) * tolerance
        closest_point = self.basis_vectors.T @ rounded_coords
        return np.abs(closest_point)

    def universal_hash(self, vector, scale=None):
        if scale is None:
            scale = self.modulus * 1e5  # Derive scale from modulus

        scaled_vector = np.round(vector * scale).astype(int)
        normalized_vector = np.abs(scaled_vector)
        hash_value = np.sum(normalized_vector % self.modulus) % self.modulus

        return hash_value

    def sketch(self, vector):
        y = self.g_L(vector)
        c = vector - y
        c = np.abs(c)
        B_inv_y = np.linalg.solve(self.basis_vectors.T, y)
        a = self.universal_hash(B_inv_y)
        return c, a

def derive_aes_key(proxy_key):
    hkdf = HKDF(
        algorithm=SHA256(),
        length=32,
        salt=None,
        info=b"fingerprint-key",
        backend=default_backend()
    )
    proxy_key_bytes = int(proxy_key).to_bytes(32, byteorder="big")
    aes_key = hkdf.derive(proxy_key_bytes)
    return aes_key

def register(fingerprint, linear_sketch):
    sketch, proxy_key = linear_sketch.sketch(fingerprint)
    print(f"Sketch (Registration): {sketch}")
    print(f"Proxy Key (Registration): {proxy_key}")
    aes_key = derive_aes_key(proxy_key)
    print(f"Derived AES Key (Registration): {aes_key.hex()}")
    return aes_key

def login(fingerprint, linear_sketch):
    sketch, _ = linear_sketch.sketch(fingerprint)
    print(f"Sketch (Login): {sketch}")
    proxy_key_reconstructed = linear_sketch.universal_hash(sketch)
    print(f"Reconstructed Proxy Key (Login): {proxy_key_reconstructed}")
    aes_key = derive_aes_key(proxy_key_reconstructed)
    print(f"Reconstructed AES Key (Login): {aes_key.hex()}")
    return aes_key


def main():
    # Initialize LinearSketch
    basis_vectors = [[1, 0], [0.5, np.sqrt(3) / 2]]
    modulus = 7
    linear_sketch = LinearSketch(basis_vectors, modulus)

    # Load real fingerprints
    fingerprint_register = np.load("data/processed/fingerprints/fingerprint_1_processed_2.npy")
    fingerprint_login = np.load("data/processed/fingerprints/fingerprint_2_processed_2.npy")

    # Registration with the first fingerprint
    aes_key_register = register(fingerprint_register, linear_sketch)

    # Login with the second fingerprint
    aes_key_login = login(fingerprint_login, linear_sketch)

    # Verify the keys match
    if aes_key_register == aes_key_login:
        print("Success: AES keys match!")
    else:
        print("Failure: AES keys do not match.")

if __name__ == "__main__":
    main()
