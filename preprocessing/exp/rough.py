import os
import numpy as np
import pickle
import matplotlib.pyplot as plt
from PIL import Image  # Import the Image module from Pillow
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def preprocess_fingerprints_with_pca(image_files, n_components_list):
    results = {}
    all_flat_vectors = []

    # Load and preprocess images
    for file_path in image_files:
        img = np.array(Image.open(file_path).convert("L"), dtype=np.float64) / 255.0
        flat_vector = img.flatten()
        all_flat_vectors.append(flat_vector)

    all_flat_vectors = np.array(all_flat_vectors)

    # Standardize the data
    scaler = StandardScaler()
    standardized_vectors = scaler.fit_transform(all_flat_vectors)

    # Process with different PCA dimensions
    for n_components in n_components_list:
        max_components = min(len(standardized_vectors), standardized_vectors.shape[1])
        n_components_adjusted = min(n_components, max_components)

        print(f"Processing with PCA dimensions: {n_components_adjusted}")
        pca_model = PCA(n_components=n_components_adjusted)
        reduced_vectors = pca_model.fit_transform(standardized_vectors)

        # Save the PCA model and results
        pca_path = f"data/processed/fingerprints/pca_model_{n_components_adjusted}.pkl"
        with open(pca_path, 'wb') as f:
            pickle.dump(pca_model, f)

        np.save(f"data/processed/fingerprints/fingerprint_1_processed_{n_components_adjusted}.npy", reduced_vectors[0])
        np.save(f"data/processed/fingerprints/fingerprint_2_processed_{n_components_adjusted}.npy", reduced_vectors[1])

        results[n_components_adjusted] = {
            "fingerprint_1": reduced_vectors[0],
            "fingerprint_2": reduced_vectors[1],
            "pca_model": pca_path,
        }

    
    return results

def visualize_variance(pca_model, n_components):
    explained_variance = pca_model.explained_variance_ratio_
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(explained_variance) + 1), explained_variance, marker='o', linestyle='--')
    plt.title(f'Explained Variance by PCA Components (n={n_components})')
    plt.xlabel('Principal Component')
    plt.ylabel('Variance Explained')
    plt.grid()
    plt.show()

def test_perturbation(fingerprint_vector, perturbation_scale=0.01):
    perturbation = np.random.normal(0, perturbation_scale, size=fingerprint_vector.shape)
    perturbed_vector = fingerprint_vector + perturbation
    similarity_score = np.linalg.norm(fingerprint_vector - perturbed_vector)
    return similarity_score, perturbed_vector

if __name__ == "__main__":
    image_files = [
        "data/raw/fingerprints/thumb_first_raw.bmp",
        "data/raw/fingerprints/thumb_second_raw.bmp",
    ]
    n_components_list = [2, 200, 300]

    processed_results = preprocess_fingerprints_with_pca(image_files, n_components_list)
    print("Processing complete!")
    for n in [2, 200, 300]:
        with open(f"data/processed/fingerprints/pca_model_{n}.pkl", 'rb') as f:
            pca_model = pickle.load(f)
        visualize_variance(pca_model, n)
    

    for n in [2, 200, 300]:
        fingerprint_1 = np.load(f"data/processed/fingerprints/fingerprint_1_processed_{n}.npy")
        fingerprint_2 = np.load(f"data/processed/fingerprints/fingerprint_2_processed_{n}.npy")
        
        score_1, perturbed_1 = test_perturbation(fingerprint_1)
        score_2, perturbed_2 = test_perturbation(fingerprint_2)
        
        print(f"n={n}, Similarity Score for Fingerprint 1: {score_1}")
        print(f"n={n}, Similarity Score for Fingerprint 2: {score_2}")
