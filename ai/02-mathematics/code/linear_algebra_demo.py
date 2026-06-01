#!/usr/bin/env python3
"""
Linear Algebra for Machine Learning — Companion Code
线性代数机器学习篇 — 配套代码

This script demonstrates every concept from Chapter 1 of the AI/ML Encyclopedia
using NumPy. Each section is self-contained and verifiable.

Requirements: numpy>=1.24.0, scipy, matplotlib
"""

import numpy as np
from numpy.linalg import norm, det, eig, svd, inv, matrix_rank
from scipy.linalg import lu
import warnings
warnings.filterwarnings("ignore")

print("=" * 72)
print("📐 Linear Algebra for Machine Learning — NumPy Verification")
print("📐 线性代数机器学习篇 — NumPy 验证")
print("=" * 72)


# =============================================================================
# SECTION 1: VECTORS & VECTOR SPACES
# =============================================================================
print("\n" + "=" * 72)
print("SECTION 1: VECTORS & VECTOR SPACES")
print("第1节: 向量与向量空间")
print("=" * 72)

# --- 1.1 Vector Creation ---
print("\n--- 1.1 Vector Creation (向量创建) ---")
v = np.array([3, 2])
u = np.array([1, 4])
w = np.array([-2, 3])
print(f"v = {v}, u = {u}, w = {w}")

# --- 1.2 Dot Product ---
print("\n--- 1.2 Dot Product (点积) ---")
dot_uv = np.dot(u, v)
dot_vw = np.dot(v, w)
dot_uw = np.dot(u, w)
print(f"u·v = {dot_uv}")
print(f"v·w = {dot_vw}")
print(f"u·w = {dot_uw}")

# Geometric interpretation: cos(theta) = dot / (||u|| * ||v||)
cos_theta = dot_uv / (norm(u) * norm(v))
angle_rad = np.arccos(cos_theta)
angle_deg = np.degrees(angle_rad)
print(f"cos(θ) = {cos_theta:.4f}")
print(f"angle(u, v) = {angle_rad:.4f} rad = {angle_deg:.2f}°")

# Verifying: orthogonal vectors have dot = 0
e1 = np.array([1, 0])
e2 = np.array([0, 1])
print(f"e1·e2 (orthogonal, should be 0) = {np.dot(e1, e2)}")

# --- 1.3 Norms ---
print("\n--- 1.3 Norms (范数) ---")
print(f"||v||_2 (Euclidean) = {norm(v):.4f}")
print(f"||v||_1 (Manhattan)  = {norm(v, ord=1):.4f}")
print(f"||v||_inf (Max)      = {norm(v, ord=np.inf):.4f}")

# Verify: L2 norm = sqrt(sum of squares)
l2_manual = np.sqrt(np.sum(v**2))
print(f"||v||_2 manual calc  = {l2_manual:.4f}  (matches NumPy: {np.isclose(norm(v), l2_manual)})")

# --- 1.4 Triangle Inequality ---
print("\n--- 1.4 Triangle Inequality (三角不等式) ---")
print(f"||u + v|| = {norm(u + v):.4f}")
print(f"||u|| + ||v|| = {norm(u) + norm(v):.4f}")
print(f"Triangle holds: {norm(u + v) <= norm(u) + norm(v)}")

# --- 1.5 Cauchy-Schwarz Inequality ---
print("\n--- 1.5 Cauchy-Schwarz (柯西-施瓦茨不等式) ---")
lhs = abs(dot_uv)
rhs = norm(u) * norm(v)
print(f"|u·v| = {lhs:.4f}")
print(f"||u||·||v|| = {rhs:.4f}")
print(f"Cauchy-Schwarz holds: {lhs <= rhs + 1e-10}")

# --- 1.6 Linear Independence ---
print("\n--- 1.6 Linear Independence (线性无关) ---")
A = np.array([[1, 2, 1],
              [2, 4, 0],
              [3, 6, 1]])
rank = matrix_rank(A)
print(f"Matrix A =\n{A}")
print(f"Rank of A = {rank}")
print(f"Columns are {'linearly independent' if rank == A.shape[1] else 'linearly dependent'}")

# Example of linear dependence: v3 = 2*v1
B = np.array([[1, 2],
              [2, 4]])  # columns are linearly dependent (col2 = 2*col1)
print(f"\nMatrix B =\n{B}")
print(f"Rank of B = {matrix_rank(B)}")
print(f"Columns are {'linearly independent' if matrix_rank(B) == 2 else 'linearly dependent'}")


# =============================================================================
# SECTION 2: MATRIX OPERATIONS
# =============================================================================
print("\n" + "=" * 72)
print("SECTION 2: MATRIX OPERATIONS")
print("第2节: 矩阵及其运算")
print("=" * 72)

# --- 2.1 Matrix Creation ---
print("\n--- 2.1 Matrix Creation (矩阵创建) ---")
A = np.array([[1, 2],
              [3, 4]])
B = np.array([[5, 6],
              [7, 8]])
print(f"A =\n{A}")
print(f"B =\n{B}")

# --- 2.2 Matrix Multiplication ---
print("\n--- 2.2 Matrix Multiplication (矩阵乘法) ---")
C = A @ B  # or np.matmul(A, B)
print(f"A @ B =\n{C}")

# Manual calculation for verification
C_manual = np.zeros((2, 2))
for i in range(2):
    for j in range(2):
        C_manual[i, j] = sum(A[i, k] * B[k, j] for k in range(2))
print(f"A @ B (manual) =\n{C_manual}")
print(f"Match: {np.allclose(C, C_manual)}")

# Matrix-vector multiplication
x = np.array([1, 2])
print(f"A @ x = {A @ x}")  # [5, 11]

# --- 2.3 Transpose ---
print("\n--- 2.3 Transpose (转置) ---")
print(f"A^T =\n{A.T}")
print(f"(AB)^T = B^T A^T (verify):")
print(f"(A @ B).T =\n{(A @ B).T}")
print(f"B^T @ A^T =\n{B.T @ A.T}")
print(f"Match: {np.allclose((A @ B).T, B.T @ A.T)}")

# --- 2.4 Inverse ---
print("\n--- 2.4 Matrix Inverse (逆矩阵) ---")
A_inv = inv(A)
print(f"A^{-1} =\n{A_inv}")
print(f"A @ A^{-1} =\n{A @ A_inv}")
print(f"Close to identity: {np.allclose(A @ A_inv, np.eye(2))}")

# Singular matrix (no inverse)
singular = np.array([[1, 2],
                     [2, 4]])
try:
    inv(singular)
    print("ERROR: Should have raised LinAlgError")
except np.linalg.LinAlgError as e:
    print(f"Singular matrix correctly rejected: {e}")

# --- 2.5 Determinant ---
print("\n--- 2.5 Determinant (行列式) ---")
det_A = det(A)
print(f"det(A) = {det_A:.4f}")
print(f"det(singular) = {det(singular):.4f} (zero → singular)")

# Verify: det(AB) = det(A)det(B)
det_AB = det(A @ B)
det_A_det_B = det(A) * det(B)
print(f"det(AB) = {det_AB:.4f}")
print(f"det(A)det(B) = {det_A_det_B:.4f}")
print(f"det(AB) = det(A)det(B): {np.allclose(det_AB, det_A_det_B)}")

# --- 2.6 Solving Linear Systems ---
print("\n--- 2.6 Linear Systems (线性方程组) ---")
# Solve Ax = b
b = np.array([5, 11])
x_solved = np.linalg.solve(A, b)
print(f"Ax = b, where b = {b}")
print(f"x = {x_solved}")
print(f"A @ x = {A @ x_solved} (should equal b)")

# --- 2.7 Special Matrices ---
print("\n--- 2.7 Special Matrices (特殊矩阵) ---")
I = np.eye(3)
print(f"Identity (单位矩阵) I_3 =\n{I}")

D = np.diag([1, 2, 3])
print(f"Diagonal (对角矩阵):\n{D}")

S = np.array([[1, 2],
              [2, 1]])  # Symmetric matrix (A = A^T)
print(f"Symmetric (对称矩阵):\n{S}")
print(f"S == S^T: {np.allclose(S, S.T)}")

# Positive definite check (all eigenvalues > 0)
eigvals_S = np.linalg.eigvalsh(S)
print(f"Eigenvalues of S: {eigvals_S}")
print(f"Positive definite: {np.all(eigvals_S > 0)}")


# =============================================================================
# SECTION 3: EIGENVALUES & EIGENVECTORS
# =============================================================================
print("\n" + "=" * 72)
print("SECTION 3: EIGENVALUES & EIGENVECTORS")
print("第3节: 特征值与特征向量")
print("=" * 72)

# --- 3.1 Eigendecomposition ---
print("\n--- 3.1 Eigendecomposition (特征分解) ---")
A = np.array([[2, 1],
              [1, 2]])
print(f"A =\n{A}")

eigvals, eigvecs = eig(A)
print(f"Eigenvalues λ:\n{eigvals}")
print(f"Eigenvectors V:\n{eigvecs}")

# Verify: A @ v = λ @ v for each eigenvector
for i in range(len(eigvals)):
    v = eigvecs[:, i]
    l = eigvals[i]
    lhs = A @ v
    rhs = l * v
    print(f"\nEigenvector {i}:")
    print(f"  A·v = {lhs}")
    print(f"  λ·v = {rhs}")
    print(f"  Match: {np.allclose(lhs, rhs)}")

# --- 3.2 Eigendecomposition Reconstruction ---
print("\n--- 3.2 Eigendecomposition Reconstruction (特征分解重构) ---")
# A = V @ diag(λ) @ V^{-1}
V = eigvecs
Lambda = np.diag(eigvals)
A_reconstructed = V @ Lambda @ inv(V)
print(f"A reconstructed:\n{A_reconstructed}")
print(f"Match: {np.allclose(A, A_reconstructed)}")

# --- 3.3 Symmetric Matrix Eigendecomposition ---
print("\n--- 3.3 Symmetric Matrix (对称矩阵特征分解) ---")
A_sym = np.array([[3, 1, 0],
                  [1, 2, 1],
                  [0, 1, 3]])
print(f"A_sym =\n{A_sym}")
eigvals_sym, eigvecs_sym = eig(A_sym)
print(f"Eigenvalues (all real): {np.real(eigvals_sym)}")
print(f"Eigenvectors are orthogonal:")
print(f"  v0·v1 = {np.dot(eigvecs_sym[:, 0], eigvecs_sym[:, 1]):.10f}")
print(f"  v0·v2 = {np.dot(eigvecs_sym[:, 0], eigvecs_sym[:, 2]):.10f}")
print(f"  v1·v2 = {np.dot(eigvecs_sym[:, 1], eigvecs_sym[:, 2]):.10f}")

# --- 3.4 Geometric Interpretation ---
print("\n--- 3.4 Geometric Interpretation (几何解释) ---")
# Show that Av = λv means only scaling, no rotation
theta = np.pi / 6  # 30 degrees
R = np.array([[np.cos(theta), -np.sin(theta)],
              [np.sin(theta),  np.cos(theta)]])  # Rotation matrix
print(f"Rotation matrix (30°):\n{R}")
eigvals_R, eigvecs_R = eig(R)
print(f"Rotation eigenvalues (complex): {eigvals_R}")
print(f"(Rotation has complex eigenvalues — no real eigenvectors)")

# Stretch matrix (has real eigenvectors)
S = np.array([[3, 0],
              [0, 0.5]])  # Stretch x by 3x, y by 0.5x
eigvals_S2, eigvecs_S2 = eig(S)
print(f"\nStretch matrix diag(3, 0.5):\n{S}")
print(f"Eigenvalues: {eigvals_S2}")
print(f"Eigenvectors:\n{eigvecs_S2}")


# =============================================================================
# SECTION 4: SINGULAR VALUE DECOMPOSITION (SVD)
# =============================================================================
print("\n" + "=" * 72)
print("SECTION 4: SINGULAR VALUE DECOMPOSITION (SVD)")
print("第4节: 奇异值分解")
print("=" * 72)

# --- 4.1 Full SVD ---
print("\n--- 4.1 Full SVD ---")
A = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]],
             dtype=float)
print(f"A =\n{A}")

U, S, Vt = svd(A, full_matrices=True)
print(f"U shape: {U.shape}")
print(f"S (singular values): {S}")
print(f"Vt shape: {Vt.shape}")

# Reconstruct
Sigma = np.zeros((U.shape[1], Vt.shape[0]))
Sigma[:len(S), :len(S)] = np.diag(S)
A_reconstructed = U @ Sigma @ Vt
print(f"\nSVD Reconstruction error: {np.linalg.norm(A - A_reconstructed):.2e}")
print(f"Reconstruction match: {np.allclose(A, A_reconstructed)}")

# Verify properties: U and V are orthogonal
print(f"\nU^T @ U ≈ I: {np.allclose(U.T @ U, np.eye(U.shape[1]), atol=1e-14)}")
print(f"V @ V^T ≈ I: {np.allclose(Vt @ Vt.T, np.eye(Vt.shape[0]), atol=1e-14)}")

# --- 4.2 Economy SVD ---
print("\n--- 4.2 Economy SVD (经济型 SVD) ---")
U_econ, S_econ, Vt_econ = svd(A, full_matrices=False)
print(f"U_econ shape: {U_econ.shape}")
print(f"S_econ: {S_econ}")
print(f"Vt_econ shape: {Vt_econ.shape}")

A_recon_econ = U_econ @ np.diag(S_econ) @ Vt_econ
print(f"Economy reconstruction match: {np.allclose(A, A_recon_econ)}")

# --- 4.3 Low-rank Approximation ---
print("\n--- 4.3 Low-rank Approximation (低秩逼近) ---")
print(f"Original matrix rank: {matrix_rank(A)}")
print(f"Singular values: {S_econ}")

for k in [1, 2]:
    # Truncated SVD: keep only top k singular values
    U_k = U_econ[:, :k]
    S_k = S_econ[:k]
    Vt_k = Vt_econ[:k, :]
    A_k = U_k @ np.diag(S_k) @ Vt_k

    error_fro = np.linalg.norm(A - A_k, 'fro')
    error_rel = error_fro / np.linalg.norm(A, 'fro')
    print(f"\nk={k} low-rank approximation:")
    print(f"A_{k} =\n{A_k}")
    print(f"Frobenius error: {error_fro:.4f}")
    print(f"Relative error: {error_rel:.4f} ({error_rel*100:.2f}%)")

    # Verify that error = sqrt(sum of squared dropped singular values)
    dropped = S_econ[k:]
    expected_error = np.sqrt(np.sum(dropped**2))
    print(f"Expected error (sqrt(Σ_{i>k} σ_i²)): {expected_error:.4f}")
    print(f"Match: {np.allclose(error_fro, expected_error)}")

# --- 4.4 SVD for Image Compression Demo (conceptual) ---
print("\n--- 4.4 SVD Compression Ratio (压缩比演示) ---")
m, n = A.shape
k_values = [1, 2]
for k in k_values:
    original_size = m * n
    compressed_size = k * (m + n + 1)  # U: m*k, Σ: k, Vt: k*n
    ratio = compressed_size / original_size
    print(f"k={k}: original={original_size}, compressed={compressed_size}, ratio={ratio:.2%}")

# --- 4.5 Relationship: SVD vs Eigendecomposition ---
print("\n--- 4.5 SVD vs Eigendecomposition (SVD 与特征分解的关系) ---")
# A^T A = V Σ^T Σ V^T (right singular vectors = eigenvectors of A^T A)
# A A^T = U Σ Σ^T U^T (left singular vectors = eigenvectors of A A^T)
print("SVD vs Eigendecomposition verification:")

ATA = A.T @ A
eigvals_ATA, eigvecs_ATA = eig(ATA)

# Sort eigenvectors by eigenvalue (descending)
idx = np.argsort(eigvals_ATA)[::-1]
eigvecs_ATA_sorted = eigvecs_ATA[:, idx]

# V from SVD should match eigenvectors of A^T A
print(f"V from SVD:\n{Vt_econ.T}")
print(f"Eigenvectors of A^T A:\n{eigvecs_ATA_sorted}")
# Note: signs may differ (eigenvectors are determined up to sign)
print(f"Directions match (ignoring sign): "
      f"{np.allclose(np.abs(Vt_econ.T), np.abs(eigvecs_ATA_sorted))}")

# --- 4.6 SVD for PCA (概念演示) ---
print("\n--- 4.6 SVD for PCA (PCA 的 SVD 实现) ---")
np.random.seed(42)
X = np.random.randn(100, 5)  # 100 samples, 5 features

# Center the data
X_centered = X - X.mean(axis=0)

# PCA via SVD (more numerically stable than covariance eigendecomposition)
U_pca, S_pca, Vt_pca = svd(X_centered, full_matrices=False)
principal_components = Vt_pca.T  # columns are PCs
explained_variance = S_pca**2 / (X_centered.shape[0] - 1)
explained_variance_ratio = explained_variance / explained_variance.sum()

print(f"Explained variance ratio (前5个主成分):")
for i, ratio in enumerate(explained_variance_ratio):
    print(f"  PC{i+1}: {ratio:.4f} ({ratio*100:.2f}%)")
print(f"  Cumulative top-2: {explained_variance_ratio[:2].sum():.4f}")

# Project to 2D
X_2d = X_centered @ principal_components[:, :2]
print(f"Projected data shape: {X_2d.shape}")


# =============================================================================
# SECTION 5: MATRIX CALCULUS
# =============================================================================
print("\n" + "=" * 72)
print("SECTION 5: MATRIX CALCULUS")
print("第5节: 矩阵微积分")
print("=" * 72)

# --- 5.1 Numerical Gradient Verification ---
print("\n--- 5.1 Numerical Gradient Verification (数值梯度验证) ---")

def f_linear(x, a):
    """f(x) = a^T x"""
    return a @ x

def f_quadratic(x, A):
    """f(x) = x^T A x"""
    return x @ A @ x

def f_squared_norm(x):
    """f(x) = ||x||^2 = x^T x"""
    return x @ x

def numerical_gradient(f, x, eps=1e-6):
    """Compute gradient using finite differences (有限差分法)"""
    grad = np.zeros_like(x)
    for i in range(len(x)):
        x_plus = x.copy()
        x_minus = x.copy()
        x_plus[i] += eps
        x_minus[i] -= eps
        grad[i] = (f(x_plus) - f(x_minus)) / (2 * eps)
    return grad

x_test = np.array([2.0, 3.0])

# Formula 1: f(x) = a^T x → gradient = a
a = np.array([1.0, 4.0])
f_lin = lambda x: f_linear(x, a)
grad_num = numerical_gradient(f_lin, x_test)
grad_analytic = a
print(f"Formula 1 — f(x) = a^T x, a = {a}")
print(f"  Numerical gradient: {grad_num}")
print(f"  Analytic gradient: {grad_analytic}")
print(f"  Match: {np.allclose(grad_num, grad_analytic, atol=1e-4)}")

# Formula 2: f(x) = x^T A x → gradient = (A + A^T)x
A_test_sym = np.array([[3.0, 1.0],
                       [1.0, 2.0]])
# For symmetric A: gradient = 2Ax
f_quad = lambda x: f_quadratic(x, A_test_sym)
grad_num = numerical_gradient(f_quad, x_test)
grad_analytic = (A_test_sym + A_test_sym.T) @ x_test
print(f"\nFormula 2 — f(x) = x^T A x, A symmetric:\n{A_test_sym}")
print(f"  Numerical gradient: {grad_num}")
print(f"  Analytic gradient (A+A^T)x: {grad_analytic}")
print(f"  For symmetric A, 2Ax: {2 * A_test_sym @ x_test}")
print(f"  Match: {np.allclose(grad_num, grad_analytic, atol=1e-4)}")

# Formula 3: f(x) = ||x||^2 = x^T x → gradient = 2x
f_norm = lambda x: f_squared_norm(x)
grad_num = numerical_gradient(f_norm, x_test)
grad_analytic = 2 * x_test
print(f"\nFormula 3 — f(x) = ||x||²")
print(f"  Numerical gradient: {grad_num}")
print(f"  Analytic gradient: {grad_analytic}")
print(f"  Match: {np.allclose(grad_num, grad_analytic, atol=1e-4)}")

# --- 5.2 Linear Regression Gradient ---
print("\n--- 5.2 Linear Regression Gradient (线性回归梯度) ---")
np.random.seed(42)
m_samples = 50
n_features = 3

# Generate synthetic data
X = np.random.randn(m_samples, n_features)
true_w = np.array([2.0, -1.5, 0.5])
y = X @ true_w + 0.1 * np.random.randn(m_samples)  # add noise

def mse_loss(w, X, y):
    """Mean squared error loss"""
    residual = X @ w - y
    return residual @ residual / m_samples

def mse_gradient(w, X, y):
    """Analytic gradient: (2/m) X^T (Xw - y)"""
    return (2.0 / m_samples) * X.T @ (X @ w - y)

def numerical_loss_gradient(w, X, y, eps=1e-6):
    """Numerical gradient of MSE loss"""
    grad = np.zeros_like(w)
    for i in range(len(w)):
        w_plus = w.copy()
        w_minus = w.copy()
        w_plus[i] += eps
        w_minus[i] -= eps
        grad[i] = (mse_loss(w_plus, X, y) - mse_loss(w_minus, X, y)) / (2 * eps)
    return grad

w_test = np.array([0.0, 0.0, 0.0])
grad_num = numerical_loss_gradient(w_test, X, y)
grad_analytic = mse_gradient(w_test, X, y)

print(f"Gradient at w=0:")
print(f"  Numerical: {grad_num}")
print(f"  Analytic:  {grad_analytic}")
print(f"  Match: {np.allclose(grad_num, grad_analytic, atol=1e-4)}")

# --- 5.3 Gradient Descent Step ---
print("\n--- 5.3 Gradient Descent Demo (梯度下降演示) ---")
w = np.zeros(n_features)
learning_rate = 0.1
n_iterations = 100

loss_history = []
for i in range(n_iterations):
    loss = mse_loss(w, X, y)
    grad = mse_gradient(w, X, y)
    w = w - learning_rate * grad
    loss_history.append(loss)

print(f"Initial loss: {loss_history[0]:.6f}")
print(f"Final loss:   {loss_history[-1]:.6f}")
print(f"Learned w: {w}")
print(f"True w:    {true_w}")
print(f"Recovery error: {np.linalg.norm(w - true_w):.6f}")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 72)
print("✅ ALL VERIFICATIONS COMPLETE")
print("✅ 所有验证完成")
print("=" * 72)
print("\nChapter companion code executed successfully.")
print("Each linear algebra concept has been verified with NumPy.")
print("下一章预告: 概率论与信息论 → ai/02-mathematics/02-probability.md")
