import numpy as np
from hashlib import sha256
from Crypto.PublicKey import ECC
from linear_sketch.linear_sketch import LinearSketch


def fuzzy_key_setting(sketch, lattice_basis):
    """
    Derive a deterministic private key using the fuzzy sketch and lattice basis.
    Args:
        sketch (numpy array): The linear sketch of the biometric data.
        lattice_basis (numpy array): Basis for the triangular lattice.
    Returns:
        int: Deterministic private key.
    """
    # Concatenate sketch and lattice basis
    combined_data = np.concatenate((sketch, lattice_basis.flatten()))
    combined_string = ",".join(map(str, combined_data))

    # Hash the concatenated string and reduce modulo ECC order
    hashed = sha256(combined_string.encode()).hexdigest()
    ecc_order = int(ECC._curves['P-256'].order)  # Convert to standard Python integer
    private_key_int = int(hashed, 16) % ecc_order
    return private_key_int

def generate_key_pair(sketch, lattice_basis):
    """
    Generate an ECC key pair using the fuzzy sketch and lattice basis.
    Args:
        sketch (numpy array): The linear sketch of the biometric data.
        lattice_basis (numpy array): Basis for the triangular lattice.
    Returns:
        dict: A dictionary containing the private and public keys.
    """
    # Generate the private key
    private_key_int = fuzzy_key_setting(sketch, lattice_basis)
    private_key = ECC.construct(curve="P-256", d=private_key_int)
    public_key = private_key.public_key()

    return {
        "private_key": private_key,
        "public_key": public_key,
    }


