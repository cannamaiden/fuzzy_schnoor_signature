import numpy as np
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.backends import default_backend
from linear_sketch.linear_sketch import LinearSketch

def derive_aes_key_from_proxy_key(proxy_key):
    """
    Derive AES key from a proxy key using HKDF.
    
    :param proxy_key: The proxy key (integer) to derive the AES key from.
    :return: AES key (hexadecimal string).
    """
    hkdf = HKDF(
        algorithm=SHA256(),
        length=32,
        salt=None,
        info=b"fingerprint-key",
        backend=default_backend()
    )
    proxy_key_bytes = int(proxy_key).to_bytes(32, byteorder="big")
    aes_key = hkdf.derive(proxy_key_bytes)
    return aes_key.hex()

def main():
    # Initialize LinearSketch
    basis_vectors = [[1, 0], [0.5, np.sqrt(3) / 2]]
    modulus = 7
    linear_sketch = LinearSketch(basis_vectors, modulus)

    # Load processed fingerprints
    fingerprint_1 = np.load("data/processed/fingerprints/fingerprint_1_processed.npy")
    fingerprint_2 = np.load("data/processed/fingerprints/fingerprint_2_processed.npy")

    # Generate sketches for both fingerprints
    sketch_1, proxy_key_1 = linear_sketch.sketch(fingerprint_1)
    sketch_2, proxy_key_2 = linear_sketch.sketch(fingerprint_2)

    print(f"Proxy Key 1 (a1): {proxy_key_1}")
    print(f"Proxy Key 2 (a2): {proxy_key_2}")

    # Use DiffRec to recover Δa
    delta_a = linear_sketch.diff_rec(sketch_1, sketch_2)
    print(f"Recovered Δa: {delta_a}")

    # Recalculate proxy key for fingerprint 2
    recalculated_proxy_key = (proxy_key_2 - delta_a + modulus) % modulus
    print(f"Recalculated Proxy Key for Second Fingerprint: {recalculated_proxy_key}")

    # Derive AES key using original proxy key 1
    aes_key_1 = derive_aes_key_from_proxy_key(proxy_key_1)
    print(f"AES Key from Proxy Key 1: {aes_key_1}")

    # Derive AES key using recalculated proxy key
    aes_key_2 = derive_aes_key_from_proxy_key(recalculated_proxy_key)
    print(f"AES Key from Recalculated Proxy Key: {aes_key_2}")

    # Compare AES keys
    if aes_key_1 == aes_key_2:
        print("Success: AES keys derived from proxy keys match!")
    else:
        print("Failure: AES keys derived from proxy keys do not match!")

if __name__ == "__main__":
    main()
