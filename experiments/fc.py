import hashlib
import numpy as np
from reedsolo import RSCodec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.backends import default_backend
from linear_sketch.linear_sketch import LinearSketch


def derive_aes_key(sketch, key_length=32):
    """
    Derive AES key from sketch using HKDF.
    :param sketch: Sketch (secret) used for key derivation.
    :param key_length: Length of the derived key in bytes.
    :return: AES key.
    """
    hkdf = HKDF(
        algorithm=SHA256(),
        length=key_length,
        salt=None,
        info=b"fuzzy-commitment",
        backend=default_backend()
    )
    sketch_bytes = sketch.tobytes() if isinstance(sketch, np.ndarray) else bytes(sketch)
    aes_key = hkdf.derive(sketch_bytes)
    return aes_key


def fuzzy_commitment_register(linear_sketch, biometric, ecc_bytes=10):
    """
    Registration phase of fuzzy commitment using the sketch as the secret.
    :param linear_sketch: Instance of LinearSketch.
    :param biometric: Biometric feature vector (numpy array).
    :param ecc_bytes: Error-correcting capability of the code.
    :return: Commitment (v), hash of AES key.
    """
    # Generate sketch from biometric
    sketch, _ = linear_sketch.sketch(biometric)

    # Encode sketch using error-correcting code
    rsc = RSCodec(ecc_bytes)
    codeword = rsc.encode(sketch.astype(np.uint8))

    # Store the commitment (encoded sketch)
    commitment = codeword

    # Derive AES key and store its hash
    aes_key = derive_aes_key(sketch)
    key_hash = hashlib.sha256(aes_key).hexdigest()

    return commitment, key_hash


def fuzzy_commitment_login(linear_sketch, biometric, commitment, key_hash, ecc_bytes=10):
    """
    Login phase of fuzzy commitment using the sketch as the secret.
    :param linear_sketch: Instance of LinearSketch.
    :param biometric: Biometric feature vector (numpy array).
    :param commitment: Commitment from registration (encoded sketch).
    :param key_hash: Hash of the AES key from registration.
    :param ecc_bytes: Error-correcting capability of the code.
    :return: AES key or None if verification fails.
    """
    # Generate sketch from biometric
    sketch, _ = linear_sketch.sketch(biometric)

    # Decode sketch using error-correcting code
    rsc = RSCodec(ecc_bytes)
    try:
        recovered_sketch = rsc.decode(commitment)
    except Exception as e:
        print(f"Error in decoding: {e}")
        return None

    # Derive AES key from recovered sketch
    aes_key = derive_aes_key(recovered_sketch)

    # Verify key hash
    reconstructed_key_hash = hashlib.sha256(aes_key).hexdigest()
    if reconstructed_key_hash == key_hash:
        print("Key verification successful!")
        return aes_key
    else:
        print("Key verification failed.")
        return None

def main():
    # Initialize LinearSketch
    basis_vectors = [[1, 0], [0.5, np.sqrt(3) / 2]]
    modulus = 7
    linear_sketch = LinearSketch(basis_vectors, modulus)

    # Example biometric data
    biometric_register = np.array([0.8, 0.6, 0.9, 1.0])  # Registration biometric
    biometric_login = biometric_register + np.random.normal(0, 0.01, biometric_register.shape)  # Slightly noisy biometric

    # Registration
    commitment, key_hash = fuzzy_commitment_register(linear_sketch, biometric_register)
    print(f"Commitment: {commitment}")
    print(f"Key Hash: {key_hash}")

    # Login
    recovered_key = fuzzy_commitment_login(linear_sketch, biometric_login, commitment, key_hash)
    if recovered_key is not None:
        print(f"Recovered AES Key: {recovered_key.hex()}")

if __name__ == "__main__":
    main()
