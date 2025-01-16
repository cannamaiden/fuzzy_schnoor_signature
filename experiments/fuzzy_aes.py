import numpy as np
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from experiments.hkdf import derive_aes_key_from_proxy_key
from linear_sketch.linear_sketch import LinearSketch

def aes_encrypt(key, plaintext):
    """
    Encrypt a plaintext message using AES.

    :param key: AES key (bytes).
    :param plaintext: The plaintext message (string).
    :return: (ciphertext, iv) where ciphertext is the encrypted message and iv is the initialization vector.
    """
    iv = np.random.bytes(16)  # Generate a random 16-byte IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Add PKCS7 padding to plaintext
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext.encode()) + padder.finalize()

    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return ciphertext, iv

def aes_decrypt(key, ciphertext, iv):
    """
    Decrypt a ciphertext message using AES.

    :param key: AES key (bytes).
    :param ciphertext: The encrypted message (bytes).
    :param iv: The initialization vector (bytes).
    :return: The decrypted plaintext message (string).
    """
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt and remove PKCS7 padding
    unpadder = padding.PKCS7(128).unpadder()
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    plaintext = unpadder.update(decrypted_data) + unpadder.finalize()

    return plaintext.decode()

def main():
    # Initialize LinearSketch
    basis_vectors = [[1, 0], [0.5, np.sqrt(3) / 2]]
    modulus = 7
    linear_sketch = LinearSketch(basis_vectors, modulus)

    # Load processed fingerprints
    fingerprint_1 = np.load("data/processed/fingerprints/fingerprint_1_processed_2.npy")
    fingerprint_2 = np.load("data/processed/fingerprints/fingerprint_2_processed_2.npy")

    # Generate sketches and proxy keys for both fingerprints
    sketch_1, proxy_key_1 = linear_sketch.sketch(fingerprint_1)
    sketch_2, proxy_key_2 = linear_sketch.sketch(fingerprint_2)

    print(f"Proxy Key 1 (a1): {proxy_key_1}")
    print(f"Proxy Key 2 (a2): {proxy_key_2}")

    # Verify acceptance region
    if linear_sketch.verify_acceptance(fingerprint_1, fingerprint_2):
        print("Fingerprints are within the acceptance region.")

        # Use DiffRec to recover delta_a
        delta_a = linear_sketch.diff_rec(sketch_1, sketch_2)
        print(f"Recovered Δa: {delta_a}")

        # Recalculate proxy key from fingerprint 2
        recalculated_proxy_key = (proxy_key_2 - delta_a + modulus) % modulus
        print(f"Recalculated Proxy Key for Second Fingerprint: {recalculated_proxy_key}")

        # Derive AES keys using HKDF
        aes_key_1 = bytes.fromhex(derive_aes_key_from_proxy_key(proxy_key_1))
        print(f"AES Key from Proxy Key 1: {aes_key_1}")
        aes_key_2 = bytes.fromhex(derive_aes_key_from_proxy_key(recalculated_proxy_key))
        print(f"AES Key from Recalculated Proxy Key: {aes_key_2}")
        if aes_key_1 == aes_key_2:
            print("Success: AES keys derived from proxy keys match!")
        else:
            print("Failure: AES keys derived from proxy keys do not match!")

        # Encrypt a sample message using AES key from proxy key 1
        plaintext = "This is a test message for AES encryption."
        ciphertext, iv = aes_encrypt(aes_key_1, plaintext)

        print(f"Ciphertext: {ciphertext.hex()}")

        # Decrypt the message using AES key from proxy key 2
        try:
            decrypted_message = aes_decrypt(aes_key_2, ciphertext, iv)
            print(f"Decrypted Message: {decrypted_message}")
        except Exception as e:
            print(f"Decryption failed: {e}")
    else:
        print("Fingerprints are not within the acceptance region. Decryption cannot proceed.")

if __name__ == "__main__":
    main()
