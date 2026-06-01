#!/usr/bin/env python3
"""
Unsupervised Learning — Companion Code
无监督学习 — 配套代码

Demonstrates:
  1. K-Means on synthetic blobs — with convergence visualization
  2. PCA on Iris dataset — 2D projection with SVD connection
  3. t-SNE comparison with PCA on Iris

Requirements: numpy>=1.24.0, scikit-learn>=1.3.0, matplotlib>=3.7.0
"""

import numpy as np
from sklearn.datasets import make_blobs, load_iris
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
import matplotlib
matplotlib.use("Agg")  # non-interactive backend for headless environments
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import warnings

warnings.filterwarnings("ignore")
np.random.seed(42)

print("=" * 72)
print("Unsupervised Learning — Code Demos")
print("无监督学习 — 代码演示")
print("=" * 72)


# =============================================================================
# SECTION 1: K-MEANS CLUSTERING — convergence visualization
# =============================================================================
print("\n" + "=" * 72)
print("SECTION 1: K-Means Clustering (K-Means 聚类)")
print("=" * 72)

# --- 1.1 Generate synthetic blobs ---
print("\n--- 1.1 Generating synthetic blobs (生成合成数据) ---")
X_blobs, y_true = make_blobs(
    n_samples=300, centers=4, cluster_std=1.2, random_state=42
)
print(f"Data shape: {X_blobs.shape}  (300 samples, 2 features)")
print(f"True cluster centers (hidden from K-Means):")
true_centers = [
    [-5.0, 2.0],
    [-2.0, -4.0],
    [3.0, 3.0],
    [5.0, -3.0],
]
for i, c in enumerate(true_centers):
    print(f"  Cluster {i}: ({c[0]:.1f}, {c[1]:.1f})")

# --- 1.2 Run K-Means with visualization of intermediate steps ---
print("\n--- 1.2 K-Means convergence visualization (K-Means 收敛过程) ---")


def kmeans_iterations(X, k, n_init=1, max_iter=10, random_state=42):
    """Run K-Means and record centroid positions at each iteration."""
    rng = np.random.RandomState(random_state)
    # Initialize: pick k random samples as centroids
    idx = rng.choice(len(X), k, replace=False)
    centroids = X[idx].copy()
    all_centroids = [centroids.copy()]

    for iteration in range(max_iter):
        # Assignment step
        distances = np.linalg.norm(X[:, np.newaxis] - centroids, axis=2)
        labels = np.argmin(distances, axis=1)

        # Update step
        new_centroids = np.array([
            X[labels == j].mean(axis=0) if np.any(labels == j) else centroids[j]
            for j in range(k)
        ])

        all_centroids.append(new_centroids.copy())

        # Check convergence
        if np.allclose(centroids, new_centroids):
            centroids = new_centroids
            break
        centroids = new_centroids

    return labels, centroids, all_centroids


# Run custom K-Means for visualization
labels_custom, final_centroids, centroid_history = kmeans_iterations(
    X_blobs, k=4, max_iter=10
)
print(f"Converged in {len(centroid_history) - 1} iterations")
print(f"Final inertia (manual calc): {KMeans(n_clusters=4, init='random', n_init=1, max_iter=10, random_state=42).fit(X_blobs).inertia_:.2f}")

# --- 1.3 Plot: K-Means convergence ---
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.ravel()

n_show = min(len(centroid_history), 6)
for i in range(n_show):
    ax = axes[i]
    # Show data points colored by current assignment
    centroids_i = centroid_history[i]
    distances_i = np.linalg.norm(
        X_blobs[:, np.newaxis] - centroids_i, axis=2
    )
    labels_i = np.argmin(distances_i, axis=1)

    scatter = ax.scatter(
        X_blobs[:, 0], X_blobs[:, 1], c=labels_i, cmap="viridis",
        s=30, alpha=0.6, edgecolors="k", linewidths=0.3
    )
    # Plot centroids
    ax.scatter(
        centroids_i[:, 0], centroids_i[:, 1],
        c="red", marker="X", s=200, edgecolors="black", linewidths=2,
        zorder=5, label="Centroids"
    )
    # Draw lines showing centroid movement
    if i > 0:
        prev = centroid_history[i - 1]
        for j in range(len(centroids_i)):
            ax.plot(
                [prev[j, 0], centroids_i[j, 0]],
                [prev[j, 1], centroids_i[j, 1]],
                "r--", alpha=0.5, lw=1
            )
    ax.set_title(f"Iteration {i}", fontsize=13)
    ax.set_xlabel("Feature 1")
    ax.set_ylabel("Feature 2")

# Final iteration (last subplot or overlay on last)
ax = axes[-1]
ax.scatter(
    X_blobs[:, 0], X_blobs[:, 1], c=labels_custom,
    cmap="viridis", s=30, alpha=0.6, edgecolors="k", linewidths=0.3
)
ax.scatter(
    final_centroids[:, 0], final_centroids[:, 1],
    c="red", marker="X", s=200, edgecolors="black", linewidths=2,
    zorder=5, label="Final Centroids"
)
# Mark true centers
true_ctrs = np.array(true_centers)
ax.scatter(
    true_ctrs[:, 0], true_ctrs[:, 1],
    c="none", marker="o", s=250, edgecolors="green", linewidths=2,
    label="True Centers"
)
ax.set_title("Final Clustering (vs True Centers)", fontsize=13)
ax.set_xlabel("Feature 1")
ax.set_ylabel("Feature 2")
ax.legend()

fig.suptitle("K-Means Convergence — Centroid Movement Across Iterations", fontsize=15)
plt.tight_layout()
plt.savefig("/tmp/kmeans_convergence.png", dpi=150)
print("\n  → Saved /tmp/kmeans_convergence.png (K-Means convergence visualization)")

# --- 1.4 Elbow Method ---
print("\n--- 1.3 Elbow Method (肘部法则) ---")
inertias = []
k_range = range(1, 11)
for k in k_range:
    kmeans = KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=42)
    kmeans.fit(X_blobs)
    inertias.append(kmeans.inertia_)

print("k → Inertia")
for k, inert in zip(k_range, inertias):
    arrow = " ← elbow (k=4)" if k == 4 else ""
    print(f"  {k} → {inert:.2f}{arrow}")

fig2, ax2 = plt.subplots(figsize=(8, 5))
ax2.plot(k_range, inertias, "bo-", linewidth=2, markersize=8)
ax2.axvline(x=4, color="red", linestyle="--", alpha=0.7, label="k=4 (elbow)")
ax2.set_xlabel("Number of clusters (k)", fontsize=12)
ax2.set_ylabel("Inertia", fontsize=12)
ax2.set_title("Elbow Method for Optimal k", fontsize=14)
ax2.legend()
ax2.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("/tmp/kmeans_elbow.png", dpi=150)
print("  → Saved /tmp/kmeans_elbow.png (Elbow method)")


# =============================================================================
# SECTION 2: PCA on Iris — SVD connection explicit
# =============================================================================
print("\n" + "=" * 72)
print("SECTION 2: PCA on Iris Dataset (PCA 鸢尾花数据集)")
print("=" * 72)

iris = load_iris()
X_iris = iris.data        # 150 × 4
y_iris = iris.target      # 0, 1, 2
feature_names = iris.feature_names
target_names = iris.target_names

print(f"\nData shape: {X_iris.shape}")
print(f"Features: {feature_names}")
print(f"Classes: {target_names}")

# --- 2.1 Standardize (for PCA, centering is essential) ---
scaler = StandardScaler(with_std=False)  # center only (we want covariance-based PCA)
X_center = scaler.fit_transform(X_iris)

print("\n--- 2.1 PCA via SVD (SVD 实现 PCA) ---")
print("Step 1: Center data  X_centered = X - μ")
print(f"  μ = {scaler.mean_}")

# Step 2: SVD
U, S, Vt = np.linalg.svd(X_center, full_matrices=False)
print(f"\nStep 2: SVD  X = U Σ V^T")
print(f"  U shape: {U.shape}")
print(f"  Σ (singular values): {S}")
print(f"  V^T shape: {Vt.shape}")
print(f"  V^T (principal components as rows):")
for i in range(Vt.shape[0]):
    print(f"    PC{i+1}: {Vt[i]}")

# Step 3: Principal components = Vt's rows (= V's columns)
n_components = 2
W_pca = Vt[:n_components].T  # first k columns of V
print(f"\nStep 3: Take top-{n_components} components W = V[:, :{n_components}]")
print(f"  W shape: {W_pca.shape}")

# Step 4: Project data
Z_svd = X_center @ W_pca  # = U_k Σ_k
print(f"\nStep 4: Project  Z = X_centered @ W")
print(f"  Z shape: {Z_svd.shape}")

# --- 2.2 Compare with sklearn PCA ---
print("\n--- 2.2 Comparing with sklearn PCA (与 sklearn PCA 对比) ---")
pca_sklearn = PCA(n_components=n_components)
Z_sklearn = pca_sklearn.fit_transform(X_center)

print(f"  sklearn PCA components:\n    {pca_sklearn.components_}")
print(f"  Our SVD components (V^T rows):\n    {Vt[:2]}")

# Verify they match (up to sign flip)
for i in range(n_components):
    dot = np.abs(np.dot(pca_sklearn.components_[i], Vt[i]))
    print(f"  PC{i+1} alignment: {dot:.6f}  (should be ~1.0)")

print(f"\n  Explained variance ratio (sklearn): {pca_sklearn.explained_variance_ratio_}")
print(f"  Explained variance ratio (manual):  {S[:2]**2 / np.sum(S**2)}")

# Check that transform matches
Z_diff = np.abs(Z_svd) - np.abs(Z_sklearn)
print(f"  Max absolute difference in scores: {np.max(np.abs(Z_diff)):.2e}")

# --- 2.3 Plot: PCA 2D projection ---
fig3, ax3 = plt.subplots(figsize=(9, 7))
colors = ["navy", "darkorange", "forestgreen"]
markers = ["o", "s", "^"]
for i, (name, color, marker) in enumerate(zip(target_names, colors, markers)):
    mask = y_iris == i
    ax3.scatter(
        Z_sklearn[mask, 0], Z_sklearn[mask, 1],
        c=color, marker=marker, s=60, alpha=0.8,
        edgecolors="k", linewidths=0.5, label=name
    )
ax3.set_xlabel(f"PC1 ({pca_sklearn.explained_variance_ratio_[0]:.1%})", fontsize=12)
ax3.set_ylabel(f"PC2 ({pca_sklearn.explained_variance_ratio_[1]:.1%})", fontsize=12)
ax3.set_title("PCA on Iris Dataset — 2D Projection via SVD", fontsize=14)
ax3.legend(fontsize=11)
ax3.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("/tmp/pca_iris.png", dpi=150)
print("\n  → Saved /tmp/pca_iris.png (PCA 2D projection)")


# =============================================================================
# SECTION 3: t-SNE vs PCA comparison
# =============================================================================
print("\n" + "=" * 72)
print("SECTION 3: t-SNE vs PCA Comparison (t-SNE 与 PCA 对比)")
print("=" * 72)

print("\n--- 3.1 Running t-SNE (perplexity=30) ---")
tsne = TSNE(n_components=2, perplexity=30, random_state=42, learning_rate="auto")
X_tsne = tsne.fit_transform(X_center)
print(f"  t-SNE embedding shape: {X_tsne.shape}")

print("\n--- 3.2 Running PCA (2 components, for comparison) ---")
pca_for_compare = PCA(n_components=2)
X_pca_compare = pca_for_compare.fit_transform(X_center)

# --- 3.3 Side-by-side plot ---
fig4, (ax4a, ax4b) = plt.subplots(1, 2, figsize=(14, 6))
for i, (name, color, marker) in enumerate(zip(target_names, colors, markers)):
    mask = y_iris == i
    ax4a.scatter(
        X_pca_compare[mask, 0], X_pca_compare[mask, 1],
        c=color, marker=marker, s=60, alpha=0.8,
        edgecolors="k", linewidths=0.5, label=name
    )
    ax4b.scatter(
        X_tsne[mask, 0], X_tsne[mask, 1],
        c=color, marker=marker, s=60, alpha=0.8,
        edgecolors="k", linewidths=0.5, label=name
    )

ax4a.set_title("PCA (linear)", fontsize=13)
ax4a.set_xlabel("PC1")
ax4a.set_ylabel("PC2")
ax4a.legend(fontsize=10)
ax4a.grid(True, alpha=0.3)

ax4b.set_title("t-SNE (non-linear, perplexity=30)", fontsize=13)
ax4b.set_xlabel("t-SNE dim 1")
ax4b.set_ylabel("t-SNE dim 2")
ax4b.legend(fontsize=10)
ax4b.grid(True, alpha=0.3)

fig4.suptitle("PCA vs t-SNE on Iris Dataset", fontsize=15)
plt.tight_layout()
plt.savefig("/tmp/tsne_vs_pca.png", dpi=150)
print("  → Saved /tmp/tsne_vs_pca.png (PCA vs t-SNE comparison)")


# =============================================================================
# SECTION 4: GMM quick demo
# =============================================================================
print("\n" + "=" * 72)
print("SECTION 4: Gaussian Mixture Model (GMM 快速演示)")
print("=" * 72)

from sklearn.mixture import GaussianMixture

# Fit GMM on the blobs data (same as K-Means)
gmm = GaussianMixture(n_components=4, random_state=42)
gmm.fit(X_blobs)
gmm_labels = gmm.predict(X_blobs)
gmm_probs = gmm.predict_proba(X_blobs)

print(f"\n  GMM converged: {gmm.converged_}")
print(f"  Number of iterations: {gmm.n_iter_}")
print(f"  Log-likelihood: {gmm.score(X_blobs):.2f}")
print(f"\n  Sample responsibilities (first 5 points):")
print(f"  {'Point':>8} {'Cluster0':>10} {'Cluster1':>10} {'Cluster2':>10} {'Cluster3':>10}")
for i in range(5):
    probs_str = " ".join(f"{p:>10.4f}" for p in gmm_probs[i])
    print(f"  {i:>8} {probs_str}")

# Find "soft" points (those with uncertain assignment)
entropy = -np.sum(gmm_probs * np.log(gmm_probs + 1e-10), axis=1)
most_uncertain = np.argmax(entropy)
print(f"\n  Most uncertain point: #{most_uncertain}")
print(f"  Its probabilities: {gmm_probs[most_uncertain]}")
print(f"  Its assigned cluster: {gmm_labels[most_uncertain]}")

# GMM vs K-Means comparison plot
fig5, (ax5a, ax5b) = plt.subplots(1, 2, figsize=(14, 6))

# K-Means
ax5a.scatter(
    X_blobs[:, 0], X_blobs[:, 1], c=labels_custom,
    cmap="viridis", s=30, alpha=0.6, edgecolors="k", linewidths=0.3
)
ax5a.scatter(
    final_centroids[:, 0], final_centroids[:, 1],
    c="red", marker="X", s=200, edgecolors="black", linewidths=2, zorder=5
)
ax5a.set_title("K-Means (hard clustering)", fontsize=13)
ax5a.set_xlabel("Feature 1")
ax5a.set_ylabel("Feature 2")

# GMM with covariance ellipses
ax5b.scatter(
    X_blobs[:, 0], X_blobs[:, 1], c=gmm_labels,
    cmap="viridis", s=30, alpha=0.6, edgecolors="k", linewidths=0.3
)
for i in range(gmm.n_components):
    # Draw 2σ ellipse for each component
    evals, evecs = np.linalg.eigh(gmm.covariances_[i])
    angle = np.degrees(np.arctan2(evecs[1, 0], evecs[0, 0]))
    width, height = 2 * np.sqrt(evals) * 2  # 2 standard deviations
    ellipse = Ellipse(
        xy=gmm.means_[i], width=width, height=height,
        angle=angle, edgecolor="red", facecolor="none",
        linewidth=2, linestyle="--"
    )
    ax5b.add_patch(ellipse)
ax5b.scatter(
    gmm.means_[:, 0], gmm.means_[:, 1],
    c="red", marker="X", s=200, edgecolors="black", linewidths=2, zorder=5
)
ax5b.set_title("GMM (soft clustering, with covariances)", fontsize=13)
ax5b.set_xlabel("Feature 1")
ax5b.set_ylabel("Feature 2")

fig5.suptitle("K-Means vs GMM on Blobs Data", fontsize=15)
plt.tight_layout()
plt.savefig("/tmp/gmm_vs_kmeans.png", dpi=150)
print("  → Saved /tmp/gmm_vs_kmeans.png (GMM vs K-Means comparison)")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 72)
print("SUMMARY (总结)")
print("=" * 72)
print("""
  Generated figures:
    1. /tmp/kmeans_convergence.png  — K-Means centroid movement across iterations
    2. /tmp/kmeans_elbow.png         — Elbow method for selecting k
    3. /tmp/pca_iris.png             — PCA 2D projection (via SVD) of Iris
    4. /tmp/tsne_vs_pca.png          — t-SNE vs PCA side-by-side on Iris
    5. /tmp/gmm_vs_kmeans.png        — GMM (with covariance ellipses) vs K-Means

  Key takeaways:
    - K-Means: hard clustering, converges monotonically, sensitive to init
    - PCA: linear dim reduction, uses SVD (X = UΣV^T), PC = V columns
    - t-SNE: non-linear, visualization only, distances NOT meaningful
    - GMM: soft clustering via EM, captures elliptical cluster shapes
""")
print("Done. All visualizations saved to /tmp/")
