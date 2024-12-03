# Fuzzy Schnorr Signature

## Overview
This project implements a fuzzy Schnorr signature scheme for biometric authentication using linear sketches. The system handles noisy biometric inputs, such as fingerprints, to provide secure and efficient cryptographic signatures.

## Directory Structure
- `data/`: Biometric datasets (raw and processed).
- `preprocessing/`: Scripts for feature extraction and PCA.
- `linear_sketch/`: Implementation of the linear sketch algorithm.
- `signature/`: Fuzzy Schnorr Signature implementation.
- `experiments/`: Benchmarking scripts.
- `results/`: Logs and experimental outputs.
- `notebooks/`: Jupyter notebooks for data analysis and visualization.

## Setup
1. Clone the repository.
2. Install dependencies:
   ```bash
   conda create --name fuzzy_sig_env python=3.9
   conda activate fuzzy_sig_env
   pip install -r requirements.txt

