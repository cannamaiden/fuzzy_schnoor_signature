# Tunnel ID

## Overview
**Tunnel ID** is a decentralized identity protocol that eliminates the need to store sensitive data like cryptographic sketches or biometric commitments. It provides robust identity verification by dynamically reconstructing cryptographic secrets using biometric data. Tunnel ID prioritizes user privacy, security, and interoperability within decentralized ecosystems.

---

## Features

1. **Stateless Design**:
   - No storage of biometric sketches, commitments, or cryptographic secrets.
   - Identity verification is performed dynamically during authentication.

2. **Biometric-Driven Identity**:
   - Uses advanced fuzzy signature schemes based on Schnorr’s signatures.
   - Biometric data is transformed into a cryptographic sketch that binds identity to physical attributes.

3. **Decentralized and Secure**:
   - Designed to operate in decentralized environments, leveraging blockchain for integrity and auditability.
   - Uses cryptographic techniques to prevent reliance on centralized identity providers.

4. **Error Resilience**:
   - Handles variability in biometric data using lattice-based error-tolerant cryptographic techniques.
   - Employs techniques like linear sketches and error correction to ensure consistent key reconstruction.

5. **Interoperable with Web3**:
   - Fully compatible with decentralized applications (dApps), smart contracts, and blockchain ecosystems.

6. **Multi-Device Support**:
   - Enables users to authenticate securely across multiple devices without relying on centralized data storage.

---

## Architecture

### Key Components

1. **Biometric Sketch Generator**:
   - Utilizes a lattice-based linear sketch system to derive a unique sketch from biometric data.
   - The sketch dynamically reconstructs cryptographic secrets during authentication.

2. **Fuzzy Schnorr Signature Module**:
   - Modifies traditional Schnorr signatures to support biometric-based key generation.
   - Includes noise tolerance to handle natural variations in biometric inputs.

3. **Stateless Key Recovery**:
   - Dynamically derives cryptographic keys from biometric data during both registration and login phases.
   - No persistent storage of sketches or commitments.

4. **Blockchain Layer**:
   - Provides decentralized and immutable storage for user-related public data (e.g., public keys or identity proofs).
   - Facilitates seamless integration with smart contracts for verifiable identity operations.

---

## Workflow

### Registration

1. **Biometric Data Input**:
   - User provides their biometric data (e.g., fingerprint scan).

2. **Sketch Generation**:
   - The biometric input is transformed into a cryptographic sketch using the **LinearSketch** module.
   - This sketch is used as the basis for all identity-related cryptographic operations.

3. **Key Derivation**:
   - A proxy key is generated from the sketch.
   - An AES key is derived from the proxy key using HKDF (HMAC-based Key Derivation Function).

4. **Public Key Storage**:
   - The user's public key, derived from the proxy key, is optionally stored on the blockchain for decentralized verification.

### Login

1. **Biometric Data Input**:
   - User provides new biometric input (e.g., during login).

2. **Sketch Reconstruction**:
   - A new sketch is generated dynamically from the biometric input using the **LinearSketch** module.

3. **Key Recovery**:
   - The original proxy key is reconstructed by comparing the new sketch to the original using the fuzzy signature mechanism.
   - An AES key is derived from the reconstructed proxy key.

4. **Identity Verification**:
   - The derived AES key is used for authentication or encryption, validating the user's identity in a decentralized ecosystem.

---

## Repository Documentation

### Directory Structure and Description

#### **`data`**
**Purpose**:
Contains raw and processed biometric data (fingerprints) and PCA models for dimensionality reduction.

- **`raw/fingerprints/`**:
  - `thumb_first_raw.bmp` and `thumb_second_raw.bmp`: Raw fingerprint images.
- **`processed/fingerprints/`**:
  - `fingerprint_1_processed.npy`, `fingerprint_2_processed.npy`: Processed fingerprint data used in cryptographic functions.
  - `pca_model.pkl`: PCA model for feature extraction from biometric data.

---

#### **`experiments`**
**Purpose**:
Includes scripts for experimenting with and benchmarking different cryptographic schemes.

- **`fuzzy_aes.py`**:
  Implements fuzzy AES encryption using sketches generated from biometric inputs.
- **`hkdf.py`**:
  Provides key derivation functionality.
- **`faes.py`**:
  Tests fuzzy AES encryption and decryption with real fingerprint data.
- **`fc.py`**:
  Implements a fuzzy commitment scheme for identity binding using sketches.

---

#### **`linear_sketch`**
**Purpose**:
Implements the lattice-based **LinearSketch** algorithm for generating biometric sketches.

- **`linear_sketch.py`**:
  - Key functions for sketch generation and hash computation.

---

## Installation

### Environment Setup
1. Install dependencies:
   ```bash
   conda env create -f environment.yml
   conda activate fuzzy-crypto
   ```
   Or
Install manually with requirements.txt:
```bash
pip install -r experiments/requirements.txt
```
### Usage
1.  Running Preprocessing
   To preprocess raw fingerprint data:
```bash
python preprocessing/preprocess_fingerprints.py
```
2. Running Fuzzy AES Encryption
To test fuzzy AES encryption with real fingerprint data:
```bash
python3 -m experiments.faes
```




























   
