import numpy as np
import matplotlib.pyplot as plt
from linear_sketch import LinearSketch

def fine_tune_acceptance_radius(fingerprint_1, fingerprint_2, perturbations, radii):
    results = {"radius": [], "FMR": [], "FNMR": []}
    linear_sketch = LinearSketch(basis_length=40.0)

    for radius in radii:
        false_matches = 0
        false_non_matches = 0
        total_matches = 0

        # Generate sketches for original fingerprints
        sketch_1, _ = linear_sketch.project_to_lattice(fingerprint_1)
        sketch_2, _ = linear_sketch.project_to_lattice(fingerprint_2)

        # Test perturbed fingerprints
        for perturbation in perturbations:
            perturbed_fingerprint = fingerprint_1 + perturbation
            perturbed_sketch, _ = linear_sketch.project_to_lattice(perturbed_fingerprint)

            if not linear_sketch.within_acceptance_region(sketch_1, perturbed_fingerprint, threshold=radius):
                false_non_matches += 1
            total_matches += 1

        # Test distinct fingerprints
        if linear_sketch.within_acceptance_region(fingerprint_1, fingerprint_2, threshold=radius):
            false_matches += 1

        # Record metrics
        fnmr = false_non_matches / total_matches
        fmr = false_matches / 1  # Only one pair of different fingerprints in this example
        results["radius"].append(radius)
        results["FMR"].append(fmr)
        results["FNMR"].append(fnmr)

    return results

# Example execution
fingerprint_1 = np.load("/home/canna/Documents/learning/fuzzy_schnoor_signature/data/processed/fingerprints/fingerprint_1_processed_2.npy")
fingerprint_2 = np.load("/home/canna/Documents/learning/fuzzy_schnoor_signature/data/processed/fingerprints/fingerprint_2_processed_2.npy")
perturbations = [np.random.normal(0, 0.01, fingerprint_1.shape) for _ in range(10)]
radii = np.linspace(1, 20, 10)  # Test radii from 1 to 20

results = fine_tune_acceptance_radius(fingerprint_1, fingerprint_2, perturbations, radii)

# Plot results
plt.plot(results["radius"], results["FMR"], label="False Match Rate (FMR)")
plt.plot(results["radius"], results["FNMR"], label="False Non-Match Rate (FNMR)")
plt.xlabel("Acceptance Radius")
plt.ylabel("Rate")
plt.title("FMR and FNMR vs. Acceptance Radius")
plt.legend()
plt.grid()
plt.show()
