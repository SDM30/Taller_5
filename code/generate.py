import numpy as np
import pandas as pd

rng = np.random.RandomState(42)

n_samples = 200
n_features = 8

# Create a random separating hyperplane (true weights and intercept)
true_coef = rng.normal(scale=1.0, size=n_features)
true_intercept = -0.2  # shift to control class balance

# Generate features
X = rng.normal(size=(n_samples, n_features))

# Make data more separable by scaling projection noise
linear_score = X.dot(true_coef) + true_intercept
# Add small noise to keep near-separable but still numeric-stable
noise = rng.normal(scale=0.1, size=n_samples)
y = (linear_score + noise > 0).astype(int)

# Verify separability (optional)
# If any misclassified by true hyperplane, reduce noise or scale true_coef
mis = np.sum((X.dot(true_coef) + true_intercept > 0) != y)
print(f"Misclassified by true hyperplane: {mis} / {n_samples}")

# Save feature matrix and labels
pd.DataFrame(X).to_csv("X.csv", index=False, header=False)
pd.DataFrame(y, columns=["y"]).to_csv("y.csv", index=False, header=False)

# Save coefficients: first line coefficients, second line intercept
with open("coeffs.txt", "w") as f:
    f.write(" ".join(map(str, true_coef)) + "\n")
    f.write(str(true_intercept) + "\n")

print("Saved X.csv, y.csv, coeffs.txt")
