"""
线性代数与 KNN 实现（Linear Algebra & KNN Demo）
================================================
依赖：numpy>=1.24.0, matplotlib>=3.7.0

展示：
1. 点积 / 矩阵乘法
2. 转置、逆、行列式
3. 特征值分解（Eigen Decomposition）
4. SVD 分解（Singular Value Decomposition）
5. KNN 从零实现（KNN from Scratch）
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


# ============================================================
# 1. 点积与矩阵乘法（Dot Product & Matrix Multiplication）
# ============================================================
print("=" * 60)
print("1. 点积与矩阵乘法（Dot Product & MatMul）")
print("=" * 60)

# 向量点积
a = np.array([1.0, 2.0, 3.0])
b = np.array([4.0, 5.0, 6.0])
dot = np.dot(a, b)
print(f"a · b = {dot}  (check: 1*4 + 2*5 + 3*6 = {1*4 + 2*5 + 3*6})")

# 矩阵乘法
X = np.array([[1, 2], [3, 4]])
Y = np.array([[5, 6], [7, 8]])
print(f"\nX @ Y:\n{X @ Y}")
print(f"\nnp.matmul(X, Y):\n{np.matmul(X, Y)}")


# ============================================================
# 2. 转置、逆、行列式（Transpose, Inverse, Determinant）
# ============================================================
print("\n" + "=" * 60)
print("2. 转置、逆、行列式（Transpose, Inverse, Det）")
print("=" * 60)

X = np.array([[4.0, 7.0], [2.0, 6.0]])
print(f"X 转置（Transpose）:\n{X.T}")

X_inv = np.linalg.inv(X)
print(f"\nX 逆矩阵（Inverse）:\n{X_inv}")

# 验证: X @ X_inv ≈ I
reconstruct = X @ X_inv
print(f"\nX @ X_inv:\n{reconstruct}")
print(f"是否接近单位矩阵（Close to Identity）: {np.allclose(reconstruct, np.eye(2))}")

det = np.linalg.det(X)
print(f"\n行列式（Determinant）: {det:.4f}")


# ============================================================
# 3. 特征值分解（Eigen Decomposition）
# ============================================================
print("\n" + "=" * 60)
print("3. 特征值分解（Eigen Decomposition）")
print("=" * 60)

A = np.array([[4.0, -2.0], [1.0, 1.0]])
eigenvalues, eigenvectors = np.linalg.eig(A)
print(f"特征值（Eigenvalues）: {eigenvalues}")
print(f"特征向量（Eigenvectors）:\n{eigenvectors}")

# 验证: A * v = λ * v
for i in range(len(eigenvalues)):
    v = eigenvectors[:, i]
    lam = eigenvalues[i]
    lhs = A @ v
    rhs = lam * v
    print(f"\nλ = {lam:.4f}:  A·v ≈ λ·v ? {np.allclose(lhs, rhs)}")


# ============================================================
# 4. SVD 分解（Singular Value Decomposition）
# ============================================================
print("\n" + "=" * 60)
print("4. SVD 分解（Singular Value Decomposition）")
print("=" * 60)

A_svd = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])
U, S, Vt = np.linalg.svd(A_svd)
print(f"U shape: {U.shape}")
print(f"S (奇异值, Singular Values): {S}")
print(f"Vt shape: {Vt.shape}")

# 重建验证: A = U @ diag(S) @ Vt
Sigma = np.zeros((A_svd.shape[0], A_svd.shape[1]))
Sigma[:len(S), :len(S)] = np.diag(S)
A_reconstructed = U @ Sigma @ Vt
print(f"\n重建误差（Reconstruction Error）: {np.linalg.norm(A_svd - A_reconstructed):.2e}")

# SVD 降维示例: 用 Top-k 个奇异值近似
k = 2
A_approx = U[:, :k] @ np.diag(S[:k]) @ Vt[:k, :]
print(f"Top-{k} 近似误差（Approximation Error）: {np.linalg.norm(A_svd - A_approx):.4f}")


# ============================================================
# 5. KNN 从零实现（K-Nearest Neighbors from Scratch）
# ============================================================
print("\n" + "=" * 60)
print("5. KNN 从零实现（KNN from Scratch）")
print("=" * 60)


class KNN:
    """K-近邻分类器（K-Nearest Neighbors Classifier）—— 仅用 NumPy 实现"""

    def __init__(self, k: int = 3):
        """
        参数:
            k: 邻居数量（Number of Neighbors）
        """
        self.k = k
        self.X_train = None
        self.y_train = None

    def fit(self, X: np.ndarray, y: np.ndarray):
        """
        训练（实际上只是存储数据，KNN 是惰性学习 Lazy Learner）。

        参数:
            X: 训练特征，shape (n_samples, n_features)
            y: 训练标签，shape (n_samples,)
        """
        self.X_train = X
        self.y_train = y

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        预测多个样本的类别。

        参数:
            X: 测试特征，shape (n_test, n_features)

        返回:
            predictions: 预测标签，shape (n_test,)
        """
        # --------------------------------------------------
        # 步骤 1: 计算所有测试点与所有训练点的欧氏距离（Euclidean Distance）
        #         利用广播（Broadcasting）避免显式循环
        # --------------------------------------------------
        # X[:, np.newaxis, :]   -> shape (n_test, 1, n_features)
        # self.X_train          -> shape (1, n_train, n_features)
        # diffs                 -> shape (n_test, n_train, n_features)  广播自动扩展
        diffs = X[:, np.newaxis, :] - self.X_train[np.newaxis, :, :]

        # 沿特征轴平方求和再开方
        dists = np.sqrt((diffs ** 2).sum(axis=2))  # shape (n_test, n_train)

        # --------------------------------------------------
        # 步骤 2: 对每个测试点，找到 K 个最近邻居的索引
        # --------------------------------------------------
        # argsort 沿 axis=1 排序，取前 k 列
        nearest_indices = np.argsort(dists, axis=1)[:, :self.k]  # shape (n_test, k)

        # --------------------------------------------------
        # 步骤 3: 花式索引获取邻居标签，进行多数投票（Majority Voting）
        # --------------------------------------------------
        nearest_labels = self.y_train[nearest_indices]  # shape (n_test, k)

        predictions = np.array([
            np.bincount(row).argmax()   # bincount 统计每个类别的出现次数
            for row in nearest_labels
        ])
        return predictions

    def predict_one(self, x: np.ndarray) -> int:
        """预测单个样本（方便单点调试）"""
        return self.predict(x.reshape(1, -1))[0]


# ============================================================
# 5.1 生成简单的 2D 数据集（Simple 2D Dataset）
# ============================================================
np.random.seed(42)

# 三个簇（Three Clusters），每个簇 30 个样本
n_per_class = 30
centers = [(2, 2), (6, 6), (8, 2)]
X_list = []
y_list = []

for cls_id, (cx, cy) in enumerate(centers):
    # 以中心为均值，标准差 0.8 的高斯噪声
    x_samples = np.random.randn(n_per_class, 2) * 0.8 + np.array([cx, cy])
    X_list.append(x_samples)
    y_list.append(np.full(n_per_class, cls_id))

X = np.vstack(X_list)
y = np.concatenate(y_list)

print(f"数据集大小（Dataset size）: X shape {X.shape}, y shape {y.shape}")
print(f"类别数（Classes）: {len(np.unique(y))}")


# ============================================================
# 5.2 训练 / 测试拆分（Train/Test Split）
# ============================================================
indices = np.random.permutation(len(X))
split = int(0.7 * len(X))
train_idx, test_idx = indices[:split], indices[split:]

X_train, X_test = X[train_idx], X[test_idx]
y_train, y_test = y[train_idx], y[test_idx]

print(f"\n训练集（Train）: {X_train.shape[0]} 个样本")
print(f"测试集（Test）: {X_test.shape[0]} 个样本")


# ============================================================
# 5.3 训练并评估 KNN（Train & Evaluate KNN）
# ============================================================
k = 5
knn = KNN(k=k)
knn.fit(X_train, y_train)

y_pred = knn.predict(X_test)
accuracy = (y_pred == y_test).mean()
print(f"\nKNN (k={k}) 测试准确率（Test Accuracy）: {accuracy:.2%}")


# ============================================================
# 5.4 可视化决策边界（Visualize Decision Boundary）
# ============================================================
def plot_decision_boundary(knn_model, X, y, title: str, save_path: str = None):
    """绘制 KNN 的决策边界（Decision Boundary）"""
    # 定义网格范围
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200),
                         np.linspace(y_min, y_max, 200))

    # 预测网格上每个点的类别
    Z = knn_model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    # 绘制
    cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
    cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])

    plt.figure(figsize=(8, 6))
    plt.contourf(xx, yy, Z, cmap=cmap_light, alpha=0.6)
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap_bold,
                edgecolor='black', s=40)
    plt.title(title)
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.colorbar(label="Class")

    if save_path:
        plt.savefig(save_path, dpi=100, bbox_inches='tight')
        print(f"决策边界图已保存至（Saved to）: {save_path}")
    plt.show()


# 注释掉绘图以保持脚本无头运行（Uncomment to see the plot）
# plot_decision_boundary(knn, X, y, f"KNN 决策边界 (k={k})")

print("\n✅ 线性代数与 KNN 演示完毕！（Linear Algebra & KNN Demo Complete!）")
