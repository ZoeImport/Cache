"""
attention_mechanism.py -- Scaled Dot-Product Attention from Scratch
===================================================================

Demonstrates:
  1. QKV projection from input embeddings
  2. Attention score computation: S = Q @ K^T / sqrt(d_k)
  3. Attention weight matrix: A = softmax(S, axis=-1)
  4. Context output: Z = A @ V
  5. Step-by-step trace on a tiny example (3 tokens, d_k=4)
  6. Attention heatmap visualization
  7. Verification: each query's attention weights sum to 1

Dependencies: numpy, matplotlib

Usage:
    python attention_mechanism.py

Expected output: console trace of every calculation step
    + attention_heatmap.png showing the 3x3 weight matrix.
"""

import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(precision=4, suppress=True)

# =========================================================================
# 1. Tiny example: 3 tokens, each with a 4-dimensional embedding
# =========================================================================
# Suppose we have a sentence with 3 words, each mapped to a d_model=4 vector.
# In real Transformers these come from learned embeddings; here we hand-craft
# them so the attention patterns are interpretable.

n_tokens = 3
d_model = 4
d_k = 4  # keep equal to d_model for this tiny demo (no projection needed)

# Token 0: "I"       — strong subject, likely to query the whole sentence
# Token 1: "love"    — verb, likely to look at "I" and "NN"
# Token 2: "NN"      — direct object, likely to look at "love"
X = np.array([
    [1.0, 0.0, 0.0, 0.0],   # "I"
    [0.0, 1.0, 0.0, 0.0],   # "love"
    [0.0, 0.0, 1.0, 0.0],   # "NN"
], dtype=float)

print("=" * 65)
print("STEP 0: Input embeddings (3 tokens, d_model=4)")
print("=" * 65)
print(f"X shape: {X.shape}")
for i, row in enumerate(X):
    print(f"  Token {i}: {row}")

# =========================================================================
# 2. Compute Q, K, V via linear projections
# =========================================================================
# In real Transformers, Q = X @ W_Q, K = X @ W_K, V = X @ W_V.
# For this demo we use identity weights so Q = K = V = X for clarity.
# The full derivation with learned weights is identical in form.

W_Q = np.eye(d_model, d_k)
W_K = np.eye(d_model, d_k)
W_V = np.eye(d_model, d_k)

Q = X @ W_Q
K = X @ W_K
V = X @ W_V

print("\n" + "=" * 65)
print("STEP 1: Linear projections Q, K, V")
print("=" * 65)
print(f"Q shape: {Q.shape}")
print(f"K shape: {K.shape}")
print(f"V shape: {V.shape}")
print("\nQ (Query) matrix:")
print(Q)
print("\nK (Key) matrix:")
print(K)
print("\nV (Value) matrix:")
print(V)

# =========================================================================
# 3. Attention scores: S = Q @ K^T
# =========================================================================
S_raw = Q @ K.T  # (n_tokens, n_tokens)

print("\n" + "=" * 65)
print("STEP 2: Raw attention scores  S = Q @ K^T")
print("=" * 65)
print(f"S_raw shape: {S_raw.shape}")
print("\nS_raw (unnormalized scores):")
print(S_raw)

# =========================================================================
# 4. Scaling: divide by sqrt(d_k)
# =========================================================================
scale = np.sqrt(d_k)
S_scaled = S_raw / scale

print("\n" + "=" * 65)
print("STEP 3: Scaled scores  S_scaled = S_raw / sqrt(d_k)")
print("=" * 65)
print(f"sqrt(d_k) = {scale:.4f}")
print("\nS_scaled (scores ÷ √d_k):")
print(S_scaled)
print("\n(Why scale? For large d_k, dot products grow large pushing "
      "softmax into regions of extremely small gradients. "
      "Dividing by √d_k keeps the scale controlled.)")

# =========================================================================
# 5. Softmax along the last axis (over keys for each query)
# =========================================================================
def softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    """Numerically stable softmax."""
    x_max = np.max(x, axis=axis, keepdims=True)
    exp_x = np.exp(x - x_max)
    return exp_x / np.sum(exp_x, axis=axis, keepdims=True)

A = softmax(S_scaled, axis=-1)  # attention weights

print("\n" + "=" * 65)
print("STEP 4: Attention weights  A = softmax(S_scaled, axis=-1)")
print("=" * 65)
print(f"A shape: {A.shape}")
print("\nAttention weight matrix (row = query, col = key):")
print(A)

# Verify: each row sums to 1
row_sums = A.sum(axis=-1)
print("\nRow sums (should all be 1.0):")
print(row_sums)
assert np.allclose(row_sums, 1.0), "Attention weights must sum to 1 per query!"
print("  ✓ All rows sum to 1 — each query distributes 100% attention across keys.")

# =========================================================================
# 6. Context output: Z = A @ V
# =========================================================================
Z = A @ V

print("\n" + "=" * 65)
print("STEP 5: Context output  Z = A @ V")
print("=" * 65)
print(f"Z shape: {Z.shape}")
print("\nZ (context vectors, one per token):")
print(Z)

# =========================================================================
# 7. Detailed trace for Query 0 ("I")
# =========================================================================
print("\n" + "=" * 65)
print("DETAILED TRACE: Query 0 ('I')")
print("=" * 65)
print("\n  Attention weights for Query 0:")
for j in range(n_tokens):
    print(f"    → Key {j} ({['I','love','NN'][j]}): weight = {A[0, j]:.4f} "
          f"({A[0, j]*100:.1f}%)")

print(f"\n  Context vector Z[0] = Σ_j A[0,j] * V[j]:")
print(f"    = {A[0,0]:.4f} × {V[0]} +")
print(f"      {A[0,1]:.4f} × {V[1]} +")
print(f"      {A[0,2]:.4f} × {V[2]}")
print(f"    = {Z[0]}")

# =========================================================================
# 8. Attention heatmap visualization
# =========================================================================
fig, axes = plt.subplots(1, 3, figsize=(12, 3.5))

labels = ["I", "love", "NN"]

# --- Panel 1: Raw scores ---
im0 = axes[0].imshow(S_raw, cmap="Blues", vmin=0, vmax=S_raw.max())
axes[0].set_xticks(range(n_tokens))
axes[0].set_yticks(range(n_tokens))
axes[0].set_xticklabels(labels)
axes[0].set_yticklabels(labels)
axes[0].set_title("Raw Scores\n$S = QK^T$", fontsize=11)
axes[0].set_xlabel("Key")
axes[0].set_ylabel("Query")
for i in range(n_tokens):
    for j in range(n_tokens):
        axes[0].text(j, i, f"{S_raw[i, j]:.2f}", ha="center", va="center",
                     fontsize=10, color="white" if S_raw[i, j] > 1.5 else "black")
fig.colorbar(im0, ax=axes[0], fraction=0.046)

# --- Panel 2: Scaled scores ---
im1 = axes[1].imshow(S_scaled, cmap="Blues", vmin=0, vmax=S_scaled.max())
axes[1].set_xticks(range(n_tokens))
axes[1].set_yticks(range(n_tokens))
axes[1].set_xticklabels(labels)
axes[1].set_yticklabels(labels)
axes[1].set_title(f"Scaled Scores\n$S / \\sqrt{{d_k}}$ ($\\sqrt{{d_k}}={scale:.0f}$)",
                  fontsize=11)
axes[1].set_xlabel("Key")
axes[1].set_ylabel("Query")
for i in range(n_tokens):
    for j in range(n_tokens):
        axes[1].text(j, i, f"{S_scaled[i, j]:.2f}", ha="center", va="center",
                     fontsize=10, color="white" if S_scaled[i, j] > 0.8 else "black")
fig.colorbar(im1, ax=axes[1], fraction=0.046)

# --- Panel 3: Attention weights ---
im2 = axes[2].imshow(A, cmap="YlOrRd", vmin=0, vmax=1)
axes[2].set_xticks(range(n_tokens))
axes[2].set_yticks(range(n_tokens))
axes[2].set_xticklabels(labels)
axes[2].set_yticklabels(labels)
axes[2].set_title("Attention Weights\n$A = \\text{softmax}(S_{\\text{scaled}})$",
                  fontsize=11)
axes[2].set_xlabel("Key")
axes[2].set_ylabel("Query")
for i in range(n_tokens):
    for j in range(n_tokens):
        axes[2].text(j, i, f"{A[i, j]:.2f}", ha="center", va="center",
                     fontsize=10,
                     color="white" if A[i, j] > 0.5 else "black")
fig.colorbar(im2, ax=axes[2], fraction=0.046)

plt.tight_layout()
plt.savefig("ai/05-transformer/code/attention_heatmap.png", dpi=150,
            bbox_inches="tight")
print(f"\n[SAVED] attention_heatmap.png")

print("\n" + "=" * 65)
print("SUMMARY")
print("=" * 65)
print(f"""
  Q (Query)   = X @ W_Q   — \"What am I looking for?\"
  K (Key)     = X @ W_K   — \"What do I contain?\"
  V (Value)   = X @ W_V   — \"What do I return?\"
  S           = Q @ K^T    — Pairwise similarity scores
  S_scaled    = S / √d_k   — Prevent softmax saturation
  A           = softmax(S_scaled, axis=-1) — Normalized attention weights
  Z           = A @ V      — Weighted sum of values (context output)
""")
print("[DONE] Scaled Dot-Product Attention complete.")
