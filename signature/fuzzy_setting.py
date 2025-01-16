import numpy as np
from linear_sketch.linear_sketch import LinearSketch

class FuzzyKeySetting:
    def __init__(self, acceptance_radius=15.0, error_tolerance=0.01):
        """
        Initializes the fuzzy key setting.
        
        Parameters:
        - acceptance_radius (float): The radius defining the acceptance region AR.
        - error_tolerance (float): The error tolerance for FNMR calculation.
        """
        self.acceptance_radius = acceptance_radius
        self.error_tolerance = error_tolerance
        self.linear_sketch = LinearSketch(acceptance_radius=acceptance_radius)

    def generate_sketch(self, fingerprint_vector):
        """
        Generates a linear sketch for a given fingerprint vector.
        
        Parameters:
        - fingerprint_vector (numpy array): The input fingerprint vector.
        
        Returns:
        - sketch (numpy array): The generated sketch.
        """
        return self.linear_sketch.generate_sketch(fingerprint_vector)

    def is_within_acceptance_region(self, sketch_1, sketch_2):
        """
        Checks if one sketch is within the acceptance region of another.
        
        Parameters:
        - sketch_1 (numpy array): The base sketch.
        - sketch_2 (numpy array): The sketch to test against the base sketch.
        
        Returns:
        - within_region (bool): True if sketch_2 is within the acceptance region of sketch_1.
        """
        return self.linear_sketch.is_within_acceptance_region(sketch_1, sketch_2)

    def calculate_fnmr(self, sketches, perturbed_sketches):
        """
        Calculates the False Non-Matching Rate (FNMR) for a set of sketches and their perturbed versions.
        
        Parameters:
        - sketches (list of numpy arrays): The original sketches.
        - perturbed_sketches (list of numpy arrays): The perturbed versions of the sketches.
        
        Returns:
        - fnmr (float): The calculated FNMR.
        """
        mismatches = 0
        total = len(sketches)
        for original, perturbed in zip(sketches, perturbed_sketches):
            if not self.is_within_acceptance_region(original, perturbed):
                mismatches += 1
        return mismatches / total

    def calculate_confmr(self, sketches):
        """
        Calculates the Conditional False Matching Rate (ConFMR) for a set of sketches.
        
        Parameters:
        - sketches (list of numpy arrays): The input sketches.
        
        Returns:
        - confmr (float): The calculated ConFMR.
        """
        matches = 0
        total = 0
        for i in range(len(sketches)):
            for j in range(i + 1, len(sketches)):
                total += 1
                if self.is_within_acceptance_region(sketches[i], sketches[j]):
                    matches += 1
        return matches / total if total > 0 else 0.0
