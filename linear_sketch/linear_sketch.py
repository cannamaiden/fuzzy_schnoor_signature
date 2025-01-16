import numpy as np

class LinearSketch:
    def __init__(self, basis_vectors, modulus, default_radius=5.0):
        """
        Initialize the linear sketch with the given lattice basis vectors and default acceptance radius.

        :param basis_vectors: Basis for the triangular lattice (e.g., B = [[1, 0], [0.5, np.sqrt(3) / 2]])
        :param modulus: Modulus p for operations in Z_p
        :param default_radius: Default acceptance radius for verifying matches
        """
        self.basis_vectors = np.array(basis_vectors)
        self.modulus = modulus
        self.default_radius = default_radius

    def g_L(self, vector):
        """
        Compute the closest lattice point y = g_L(x) with respect to the basis B.

        :param vector: Input vector
        :return: Closest lattice point y
        """
        lattice_coords = np.linalg.solve(self.basis_vectors.T, vector)
        rounded_coords = np.round(lattice_coords)
        closest_point = self.basis_vectors.T @ rounded_coords
        return closest_point

    def universal_hash(self, vector):
        """
        Universal hash function to map vectors in Z_p^n to Z_p.

        :param vector: Input vector
        :return: Hashed value
        """
        # Convert vector to integers in Z_p
        vector_mod_p = (vector % self.modulus).astype(int)
        return np.sum(vector_mod_p) % self.modulus

    def sketch(self, vector):
        """
        Generate a sketch (c, a) for the given vector x.

        :param vector: Input biometric vector
        :return: (c, a) where c = x - g_L(x) and a = UH(B⁻¹y)
        """
        y = self.g_L(vector)  # Closest lattice point
        c = vector - y  # Sketch c
        B_inv_y = np.linalg.solve(self.basis_vectors.T, y)  # Compute B⁻¹y
        a = self.universal_hash(B_inv_y)  # Compute a using UH
        return c, a

    def diff_rec(self, sketch_c1, sketch_c2):
        """
        Perform DiffRec to recover Δa = a2 - a1 using sketches c1 and c2, including sign determination.

        :param sketch_c1: Sketch c1 of the first fingerprint
        :param sketch_c2: Sketch c2 of the second fingerprint
        :return: Δa (signed difference in proxy keys)
        """
        delta_c = sketch_c2 - sketch_c1  # Difference between sketches
        delta_y = self.g_L(delta_c)  # Projected lattice point

        # Use the direction of delta_c to determine the sign of Δa
        sign = 1 if np.dot(delta_y, delta_c) > 0 else -1

        # Recover Δa (signed difference in proxy keys)
        delta_a = sign * self.universal_hash(np.linalg.solve(self.basis_vectors.T, delta_y))

        # Debugging outputs
        print(f"Sketch c1: {sketch_c1}")
        print(f"Sketch c2: {sketch_c2}")
        print(f"Delta c: {delta_c}")
        print(f"Delta y (lattice projection): {delta_y}")
        print(f"Recovered Δa (signed difference): {delta_a}")

        return delta_a


    def dynamic_radius_adjustment(self, similarity_score, noise_level, min_radius=2.0, max_radius=15.0):
        """
        Adjust the acceptance radius dynamically based on similarity and noise levels.

        :param similarity_score: A score representing fingerprint similarity (higher is better).
        :param noise_level: The level of noise in the data (higher means noisier).
        :param min_radius: Minimum allowable radius.
        :param max_radius: Maximum allowable radius.
        :return: Adjusted radius.
        """
        # Calculate dynamic radius as a weighted function of similarity and noise
        dynamic_radius = self.default_radius + (1 - similarity_score) * (max_radius - min_radius) - noise_level * (max_radius - min_radius)
        return np.clip(dynamic_radius, min_radius, max_radius)

    def verify_acceptance(self, vector1, vector2, similarity_score=None, noise_level=None):
        """
        Verify if two vectors are in the same fundamental parallelepiped (i.e., within the acceptance region).

        :param vector1: First vector
        :param vector2: Second vector
        :param similarity_score: Fingerprint similarity score (optional, required for dynamic radius adjustment).
        :param noise_level: Noise level in data (optional, required for dynamic radius adjustment).
        :return: True if vectors are within the acceptance region, False otherwise
        """
        c1, _ = self.sketch(vector1)
        c2, _ = self.sketch(vector2)

        # Adjust radius dynamically if scores are provided
        if similarity_score is not None and noise_level is not None:
            radius = self.dynamic_radius_adjustment(similarity_score, noise_level)
        else:
            radius = self.default_radius

        distance = np.linalg.norm(c1 - c2)
        return distance <= radius
