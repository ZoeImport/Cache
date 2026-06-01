"""
线性模型从零实现 — Linear & Logistic Regression
(Linear Models from Scratch — Regression & Classification)
==========================================================
依赖：numpy>=1.24.0, matplotlib>=3.7.0, scikit-learn>=1.3.0

涵盖 (Covers):
  1. 线性回归 (Linear Regression)
     - 闭式解 (Normal Equations / OLS)
     - 批量梯度下降 (Batch Gradient Descent)
     - 损失曲面与参数轨迹可视化
  2. 逻辑回归 (Logistic Regression)
     - Sigmoid 函数
     - 交叉熵损失 (Cross-Entropy Loss)
     - 梯度下降优化
     - 决策边界可视化
  3. 正则化 (Regularization)
     - Ridge (L2) 闭式解
  4. 与 sklearn 对比验证

数学公式 (Mathematical Formulation):
  Linear Regression:    y = wx + b,  L = (1/2n) * Σ(y - ŷ)²
  Normal Equations:     w* = (X^T X)^{-1} X^T y
  Logistic Regression:  ŷ = σ(w^T x),  L = -1/n Σ[y log ŷ + (1-y) log(1-ŷ)]
  Ridge (L2):           L + λ||w||₂²
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from pathlib import Path
from sklearn.linear_model import LinearRegression as SklearnLinearRegression
from sklearn.linear_model import LogisticRegression as SklearnLogisticRegression
from sklearn.preprocessing import StandardScaler

# ============================================================
# 0. 全局设置 (Global Settings)
# ============================================================
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

RNG = np.random.RandomState(42)

# 可视化风格
plt.rcParams.update({
    "figure.dpi": 120,
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
})


# ============================================================
# 第1部分：线性回归 (Linear Regression)
# ============================================================

class LinearRegression:
    """线性回归 — 支持闭式解和梯度下降 (Linear Regression with OLS + GD)"""

    def __init__(self, method="closed_form"):
        self.method = method          # "closed_form" or "gradient_descent"
        self.w = None                 # 权重 (weights)
        self.b = None                 # 偏置 (bias)
        self.loss_history = []        # 损失历史 (loss curve)

    def _add_bias(self, X: np.ndarray) -> np.ndarray:
        """在特征矩阵前加一列1，用于合并偏置"""
        return np.c_[np.ones(X.shape[0]), X]

    def fit_closed_form(self, X: np.ndarray, y: np.ndarray):
        """闭式解：w* = (X^T X)^{-1} X^T y"""
        X_b = self._add_bias(X)
        # 正规方程
        w_star = np.linalg.inv(X_b.T @ X_b) @ X_b.T @ y
        self.b = w_star[0]
        self.w = w_star[1:]
        self.loss_history = [self._mse(X, y)]
        return self

    def fit_gradient_descent(self, X: np.ndarray, y: np.ndarray,
                             lr: float = 0.01, epochs: int = 1000,
                             batch_size: int = None, verbose: bool = False):
        """梯度下降求解
        Args:
            lr: 学习率 (learning rate)
            epochs: 迭代次数
            batch_size: None=批梯度, 1=SGD, >1=mini-batch
        """
        n, d = X.shape
        # 初始化参数
        self.w = RNG.randn(d) * 0.1
        self.b = 0.0
        self.loss_history = []

        for epoch in range(epochs):
            # 梯度计算
            if batch_size is None or batch_size >= n:
                # 批量梯度下降
                y_pred = self.predict(X)
                grad_w = (1 / n) * X.T @ (y_pred - y)
                grad_b = (1 / n) * np.sum(y_pred - y)
            elif batch_size == 1:
                # SGD：随机选一个样本
                idx = RNG.randint(n)
                xi, yi = X[idx:idx+1], y[idx:idx+1]
                y_pred = self.predict(xi)
                grad_w = xi.T @ (y_pred - yi)
                grad_b = np.sum(y_pred - yi)
            else:
                # Mini-batch
                indices = RNG.choice(n, batch_size, replace=False)
                Xb, yb = X[indices], y[indices]
                y_pred = self.predict(Xb)
                m = batch_size
                grad_w = (1 / m) * Xb.T @ (y_pred - yb)
                grad_b = (1 / m) * np.sum(y_pred - yb)

            # 参数更新
            self.w -= lr * grad_w
            self.b -= lr * grad_b

            # 记录损失
            loss = self._mse(X, y)
            self.loss_history.append(loss)

            if verbose and (epoch + 1) % 200 == 0:
                print(f"  Epoch {epoch+1}/{epochs}, MSE = {loss:.6f}")

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """线性预测 ŷ = Xw + b"""
        return X @ self.w + self.b

    def _mse(self, X: np.ndarray, y: np.ndarray) -> float:
        """均方误差 (Mean Squared Error)"""
        return float(np.mean((self.predict(X) - y) ** 2))

    def get_params(self) -> tuple:
        """返回 (权重, 偏置)"""
        return self.w, self.b

    def coef_(self):
        """兼容 sklearn 接口"""
        return self.w

    def intercept_(self):
        """兼容 sklearn 接口"""
        return self.b

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """R² 决定系数 (coefficient of determination)"""
        y_pred = self.predict(X)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        return 1 - ss_res / ss_tot


def demo_linear_regression():
    """线性回归完整演示 (Full Demo)"""
    print("=" * 60)
    print("1. 线性回归演示 (Linear Regression Demo)")
    print("=" * 60)

    # ---- 1a. 生成合成数据 ----
    n_samples = 100
    w_true, b_true = 2.5, 1.0
    noise_std = 0.8

    X = RNG.rand(n_samples, 1) * 6 - 3  # [-3, 3]
    y = w_true * X.flatten() + b_true + RNG.randn(n_samples) * noise_std

    print(f"\n真实参数 (True params): w={w_true}, b={b_true}")
    print(f"样本数 (Samples): {n_samples}")

    # ---- 1b. 闭式解 (Normal Equations) ----
    print("\n--- 闭式解 (Closed-Form / Normal Equations) ---")
    lr_cf = LinearRegression(method="closed_form")
    lr_cf.fit_closed_form(X, y)
    w_cf, b_cf = lr_cf.get_params()
    print(f"  结果: w={w_cf.item():.4f}, b={b_cf:.4f}")
    print(f"  R² = {lr_cf.score(X, y):.4f}")

    # ---- 1c. 梯度下降 ----
    print("\n--- 梯度下降 (Gradient Descent) ---")
    lr_gd = LinearRegression(method="gradient_descent")
    lr_gd.fit_gradient_descent(X, y, lr=0.1, epochs=500, verbose=True)
    w_gd, b_gd = lr_gd.get_params()
    print(f"  结果: w={w_gd.item():.4f}, b={b_gd:.4f}")
    print(f"  R² = {lr_gd.score(X, y):.4f}")

    # ---- 1d. sklearn 对比 ----
    print("\n--- sklearn 对比 ---")
    sk_lr = SklearnLinearRegression()
    sk_lr.fit(X, y)
    print(f"  sklearn: w={sk_lr.coef_[0]:.4f}, b={sk_lr.intercept_:.4f}")
    print(f"  R² = {sk_lr.score(X, y):.4f}")

    # ---- 1e. 可视化 ----
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # 图1: 拟合结果 (Fitting Result)
    ax = axes[0, 0]
    ax.scatter(X, y, alpha=0.6, label="Data", s=30)
    x_plot = np.linspace(X.min(), X.max(), 100)
    ax.plot(x_plot, w_cf * x_plot + b_cf, 'r-', linewidth=2, label="OLS (Closed-form)")
    ax.plot(x_plot, w_gd * x_plot + b_gd, 'g--', linewidth=2, label="GD")
    ax.plot(x_plot, w_true * x_plot + b_true, 'k:', linewidth=2, label="Ground truth")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_title("Linear Regression Fit")
    ax.legend()
    ax.grid(alpha=0.3)

    # 图2: 损失下降曲线 (Loss Curve)
    ax = axes[0, 1]
    ax.plot(lr_gd.loss_history, 'b-', linewidth=1.5)
    ax.axhline(y=lr_cf.loss_history[0], color='r', linestyle='--',
               label=f"Closed-form MSE = {lr_cf.loss_history[0]:.4f}")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("MSE")
    ax.set_title("Gradient Descent — Loss Curve")
    ax.legend()
    ax.grid(alpha=0.3)

    # 图3: 参数轨迹 (Parameter Trajectory on Loss Surface)
    ax = axes[1, 0]
    # 构建损失曲面网格
    w_range = np.linspace(-1, 5, 100)
    b_range = np.linspace(-3, 5, 100)
    W, B = np.meshgrid(w_range, b_range)
    # 对网格每点计算 MSE
    Z = np.zeros_like(W)
    for i in range(len(w_range)):
        for j in range(len(b_range)):
            y_pred = X.flatten() * W[j, i] + B[j, i]
            Z[j, i] = np.mean((y - y_pred) ** 2) / 2

    contour = ax.contour(W, B, Z, levels=30, cmap="viridis", alpha=0.7)
    plt.colorbar(contour, ax=ax, label="MSE / 2")

    # 勾画梯度下降路径 —— 每10步取一点
    # 需要从 fit_gradient_descent 捕捉参数路径
    # 这里我们做一个小演示：在已训练好的参数上标注最终点
    ax.scatter([w_cf], [b_cf], color='red', s=120, marker='x', zorder=5,
               label=f"Closed-form (w={w_cf.item():.2f}, b={b_cf:.2f})")
    ax.scatter([w_gd], [b_gd], color='green', s=120, marker='o', zorder=5,
               label=f"GD final (w={w_gd.item():.2f}, b={b_gd:.2f})")
    ax.set_xlabel("$w$ (slope)")
    ax.set_ylabel("$b$ (intercept)")
    ax.set_title("Loss Surface (Contour) & Parameter Solutions")
    ax.legend()

    # 图4: 不同学习率对比 (LR Comparison)
    ax = axes[1, 1]
    lrs = [0.01, 0.05, 0.1, 0.5]
    for lr_val in lrs:
        lr_tmp = LinearRegression(method="gradient_descent")
        lr_tmp.fit_gradient_descent(X, y, lr=lr_val, epochs=200)
        ax.plot(lr_tmp.loss_history, label=f"lr={lr_val}", linewidth=1.5)

    ax.set_xlabel("Epoch")
    ax.set_ylabel("MSE")
    ax.set_title("Learning Rate Comparison")
    ax.legend()
    ax.grid(alpha=0.3)

    plt.tight_layout()
    fig_path = OUTPUT_DIR / "linear_regression_demo.png"
    plt.savefig(fig_path, bbox_inches="tight")
    print(f"\n  图形保存至 (Figure saved): {fig_path}")
    plt.close()

    return lr_cf, lr_gd


# ============================================================
# 第2部分：逻辑回归 (Logistic Regression)
# ============================================================

def sigmoid(z: np.ndarray) -> np.ndarray:
    """Sigmoid 函数 σ(z) = 1 / (1 + e^{-z})"""
    # 防止 exp 溢出
    z = np.clip(z, -500, 500)
    return 1.0 / (1.0 + np.exp(-z))


class LogisticRegression:
    """逻辑回归 — 从零实现 (Logistic Regression from Scratch)"""

    def __init__(self, lr: float = 0.1, epochs: int = 1000):
        self.lr = lr
        self.epochs = epochs
        self.w = None
        self.b = None
        self.loss_history = []

    def fit(self, X: np.ndarray, y: np.ndarray, verbose: bool = False):
        """使用梯度下降训练 (Train using Gradient Descent)"""
        n, d = X.shape
        self.w = RNG.randn(d) * 0.01
        self.b = 0.0

        for epoch in range(self.epochs):
            # 前向传播 (Forward)
            logits = X @ self.w + self.b
            y_pred = sigmoid(logits)

            # 梯度 (Gradient) — 与线性回归形式相同！
            grad_w = (1 / n) * X.T @ (y_pred - y)
            grad_b = (1 / n) * np.sum(y_pred - y)

            # 更新 (Update)
            self.w -= self.lr * grad_w
            self.b -= self.lr * grad_b

            # 交叉熵损失 (Cross-Entropy Loss)
            loss = self._cross_entropy(y, y_pred)
            self.loss_history.append(loss)

            if verbose and (epoch + 1) % 200 == 0:
                acc = self._accuracy(y, self.predict(X))
                print(f"  Epoch {epoch+1}/{self.epochs}, Loss={loss:.6f}, Acc={acc:.4f}")

        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """预测概率 P(y=1|x)"""
        return sigmoid(X @ self.w + self.b)

    def predict(self, X: np.ndarray) -> np.ndarray:
        """预测类别标签 {0, 1}"""
        return (self.predict_proba(X) >= 0.5).astype(int)

    def _cross_entropy(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """交叉熵损失 (避免 log(0))"""
        eps = 1e-12
        y_pred = np.clip(y_pred, eps, 1 - eps)
        return float(-np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred)))

    def _accuracy(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """分类准确率"""
        return float(np.mean(y_true == y_pred))

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """准确率 (Accuracy)"""
        return self._accuracy(y, self.predict(X))

    def coef_(self):
        return self.w

    def intercept_(self):
        return self.b


def demo_logistic_regression():
    """逻辑回归完整演示 (Full Demo)"""
    print("\n" + "=" * 60)
    print("2. 逻辑回归演示 (Logistic Regression Demo)")
    print("=" * 60)

    # ---- 2a. 生成合成二分类数据 ----
    n_samples = 200
    # 两个高斯簇 (linearly separable)
    X0 = RNG.randn(n_samples // 2, 2) * 0.5 + np.array([-1.5, -1.5])
    X1 = RNG.randn(n_samples // 2, 2) * 0.5 + np.array([1.5, 1.5])
    X = np.vstack([X0, X1])
    y = np.hstack([np.zeros(n_samples // 2), np.ones(n_samples // 2)])

    # 混洗数据
    shuffle_idx = RNG.permutation(n_samples)
    X, y = X[shuffle_idx], y[shuffle_idx]

    print(f"样本数 (Samples): {n_samples}")
    print(f"类别分布 (Class distribution): 0={np.sum(y==0)}, 1={np.sum(y==1)}")

    # ---- 2b. 训练逻辑回归 ----
    print("\n--- 训练 (Training) ---")
    logreg = LogisticRegression(lr=0.5, epochs=2000)
    logreg.fit(X, y, verbose=True)

    # ---- 2c. sklearn 对比 ----
    print("\n--- sklearn 对比 ---")
    sk_lr = SklearnLogisticRegression(C=1e10, solver="lbfgs")  # C很大 ≈ 无正则化
    sk_lr.fit(X, y)
    sk_pred = sk_lr.predict(X)
    sk_acc = np.mean(sk_pred == y)
    print(f"  sklearn 准确率 (Accuracy): {sk_acc:.4f}")
    print(f"  自实现准确率 (Ours): {logreg.score(X, y):.4f}")

    # ---- 2d. 可视化 ----
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # 构建网格用于绘制决策边界
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200),
                         np.linspace(y_min, y_max, 200))
    grid = np.c_[xx.ravel(), yy.ravel()]

    # 图1: 决策边界 (Decision Boundary)
    ax = axes[0, 0]
    Z = logreg.predict_proba(grid).reshape(xx.shape)
    contour = ax.contourf(xx, yy, Z, levels=20, cmap="RdYlBu", alpha=0.6)
    plt.colorbar(contour, ax=ax, label="$P(y=1)$")
    # 决策边界等高线 (P=0.5)
    ax.contour(xx, yy, Z, levels=[0.5], colors='k', linewidths=2)
    # 数据点
    ax.scatter(X[y == 0, 0], X[y == 0, 1], c="blue", edgecolors='k',
               label="Class 0", s=40)
    ax.scatter(X[y == 1, 0], X[y == 1, 1], c="red", edgecolors='k',
               label="Class 1", s=40)
    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")
    ax.set_title("Decision Boundary (Ours)")
    ax.legend()
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    # 图2: sklearn 决策边界
    ax = axes[0, 1]
    Z_sk = sk_lr.predict_proba(grid)[:, 1].reshape(xx.shape)
    contour = ax.contourf(xx, yy, Z_sk, levels=20, cmap="RdYlBu", alpha=0.6)
    ax.contour(xx, yy, Z_sk, levels=[0.5], colors='k', linewidths=2)
    ax.scatter(X[y == 0, 0], X[y == 0, 1], c="blue", edgecolors='k',
               label="Class 0", s=40)
    ax.scatter(X[y == 1, 0], X[y == 1, 1], c="red", edgecolors='k',
               label="Class 1", s=40)
    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")
    ax.set_title("Decision Boundary (sklearn)")
    ax.legend()
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    # 图3: Sigmoid 概率曲面 (3D)
    ax = axes[1, 0]
    # 在一维切片上展示 Sigmoid
    # 沿着垂直于决策边界的方向取切片
    w = logreg.w
    b = logreg.b
    scores = grid @ w + b
    probas = sigmoid(scores)

    # 用网格点的决策得分来显示 Sigmoid 形状
    scatter = ax.scatter(scores, probas, c=probas, cmap="RdYlBu",
                         s=1, alpha=0.5)
    # 绘制理论 Sigmoid 曲线
    z_line = np.linspace(scores.min(), scores.max(), 500)
    ax.plot(z_line, sigmoid(z_line), 'k-', linewidth=2, label=r"$\sigma(z) = 1/(1+e^{-z})$")
    ax.axvline(x=0, color='gray', linestyle='--', alpha=0.5, label="Decision boundary (z=0)")
    ax.axhline(y=0.5, color='gray', linestyle=':', alpha=0.5)
    ax.set_xlabel("$z = w^T x + b$ (logit)")
    ax.set_ylabel(r"$\sigma(z)$")
    ax.set_title("Sigmoid — Probability Calibration")
    ax.legend()
    ax.grid(alpha=0.3)

    # 图4: 损失下降曲线 (Loss Curve)
    ax = axes[1, 1]
    ax.plot(logreg.loss_history, 'b-', linewidth=1.5)
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Cross-Entropy Loss")
    ax.set_title("Logistic Regression — Loss Curve")
    ax.grid(alpha=0.3)

    plt.tight_layout()
    fig_path = OUTPUT_DIR / "logistic_regression_demo.png"
    plt.savefig(fig_path, bbox_inches="tight")
    print(f"\n  图形保存至 (Figure saved): {fig_path}")
    plt.close()

    return logreg


# ============================================================
# 第3部分：正则化演示 (Regularization Demo)
# ============================================================

class RidgeRegression:
    """Ridge 回归 (L2 正则化) — 闭式解"""

    def __init__(self, alpha=1.0):
        self.alpha = alpha
        self.w = None
        self.b = None

    def fit(self, X: np.ndarray, y: np.ndarray):
        """Ridge 闭式解: w* = (X^T X + n*α*I)^{-1} X^T y"""
        n, d = X.shape
        X_b = np.c_[np.ones(n), X]  # 加偏置列

        # Ridge 修正正规方程 (不对偏置正则化，所以第一行/列不动)
        I_mod = np.eye(d + 1)
        I_mod[0, 0] = 0  # 不对偏置做正则化
        w_star = np.linalg.inv(X_b.T @ X_b + n * self.alpha * I_mod) @ X_b.T @ y

        self.b = w_star[0]
        self.w = w_star[1:]
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        return X @ self.w + self.b

    def get_params(self):
        return self.w, self.b


def demo_regularization():
    """正则化演示：展示 Ridge 如何控制过拟合"""
    print("\n" + "=" * 60)
    print("3. 正则化演示 (Regularization Demo)")
    print("=" * 60)

    # 生成高次多项式数据 (过拟合场景)
    n_samples = 30
    X = np.linspace(-3, 3, n_samples)
    y_true = np.sin(X)
    y = y_true + RNG.randn(n_samples) * 0.3

    # 使用多项式特征 (最高 9 次)
    from sklearn.preprocessing import PolynomialFeatures
    poly = PolynomialFeatures(degree=9, include_bias=False)
    X_poly = poly.fit_transform(X.reshape(-1, 1))

    print(f"样本数: {n_samples}, 特征维度: {X_poly.shape[1]}")

    # 不同 α 的 Ridge
    alphas = [0, 1e-3, 0.1, 10]
    colors = ['red', 'orange', 'green', 'purple']

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.scatter(X, y, alpha=0.7, label="Data", s=40, zorder=5)
    ax.plot(X, y_true, 'k-', linewidth=2, label=r"True $\sin(x)$", zorder=4)

    x_plot = np.linspace(-3, 3, 300)
    X_plot_poly = poly.transform(x_plot.reshape(-1, 1))

    for alpha, color in zip(alphas, colors):
        if alpha == 0:
            # 普通线性回归 (无正则化) = 过拟合
            lr = LinearRegression(method="closed_form")
            lr.fit_closed_form(X_poly, y)
            w, b = lr.get_params()
            label = "OLS (α=0, overfitting)"
        else:
            ridge = RidgeRegression(alpha=alpha)
            ridge.fit(X_poly, y)
            w, b = ridge.get_params()
            label = f"Ridge α={alpha}"

        y_plot = X_plot_poly @ w + b
        ax.plot(x_plot, y_plot, color=color, linewidth=1.5,
                label=label, linestyle='--' if alpha == 0 else '-')

        # 打印权重稀疏性
        n_nonzero = np.sum(np.abs(w) > 1e-6)
        print(f"  α={alpha:.0e}: max|w|={np.max(np.abs(w)):.4f}, "
              f"nonzero={n_nonzero}/{len(w)}")

    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_title("Ridge Regularization — Controlling Overfitting\n"
                 "(Polynomial degree=9)")
    ax.legend()
    ax.grid(alpha=0.3)

    plt.tight_layout()
    fig_path = OUTPUT_DIR / "regularization_demo.png"
    plt.savefig(fig_path, bbox_inches="tight")
    print(f"\n  图形保存至 (Figure saved): {fig_path}")
    plt.close()


# ============================================================
# 第4部分：核心概念可视化 (Core Concepts Visualization)
# ============================================================

def demo_core_concepts():
    """参数-损失-梯度 核心概念可视化"""
    print("\n" + "=" * 60)
    print("4. 核心概念可视化 (Core Concepts)")
    print("=" * 60)

    # 用一个简单的 1D 线性回归 (仅斜率 w) 来展示
    # 数据: y = 2x + noise
    X = np.array([-2, -1, 0, 1, 2]).reshape(-1, 1)
    y = 2 * X.flatten() + RNG.randn(5) * 0.5

    w_range = np.linspace(-1, 5, 200)
    losses = []
    gradients = []

    for w in w_range:
        y_pred = X.flatten() * w
        loss = np.mean((y - y_pred) ** 2) / 2
        grad = np.mean((y_pred - y) * X.flatten())  # dL/dw = mean((ŷ - y) * x)
        losses.append(loss)
        gradients.append(grad)

    losses = np.array(losses)
    gradients = np.array(gradients)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # 图1: 损失曲线 + 梯度箭头
    ax = axes[0]
    ax.plot(w_range, losses, 'b-', linewidth=2, label=r"$\mathcal{L}(w)$")
    ax.set_xlabel("$w$ (parameter)")
    ax.set_ylabel(r"Loss $\mathcal{L}(w)$")
    ax.set_title("Loss Function — How 'bad' is a given $w$?")
    ax.grid(alpha=0.3)

    # 在几个点画梯度方向
    pts = [-0.5, 1.0, 2.0, 3.5]
    for w_pt in pts:
        idx = np.argmin(np.abs(w_range - w_pt))
        grad_at_pt = gradients[idx]
        loss_at_pt = losses[idx]
        # 梯度方向箭头（长=梯度大小*缩放）
        scale = 3.0
        dx = -grad_at_pt * scale  # 负梯度方向（下降方向）
        ax.arrow(w_pt, loss_at_pt, dx, 0,
                 head_width=0.3, head_length=0.15,
                 fc='red', ec='red', alpha=0.7)
        ax.plot(w_pt, loss_at_pt, 'ro', markersize=6)

    ax.legend()

    # 图2: 梯度随 w 变化
    ax = axes[1]
    ax.plot(w_range, gradients, 'r-', linewidth=2,
            label=r"$\nabla_w \mathcal{L}(w)$")
    ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax.set_xlabel("$w$ (parameter)")
    ax.set_ylabel(r"Gradient $\partial \mathcal{L} / \partial w$")
    ax.set_title("Gradient — Which direction decreases loss?")
    ax.grid(alpha=0.3)
    ax.legend()

    # 标注最优 w*
    w_opt_idx = np.argmin(losses)
    w_opt = w_range[w_opt_idx]
    ax.axvline(x=w_opt, color='green', linestyle=':', alpha=0.7,
               label=f"$w^*$ = {w_opt:.2f}")
    ax.legend()

    plt.tight_layout()
    fig_path = OUTPUT_DIR / "core_concepts.png"
    plt.savefig(fig_path, bbox_inches="tight")
    print(f"  图形保存至 (Figure saved): {fig_path}")
    plt.close()

    print(f"  最优 w* = {w_opt:.2f} (最小损失)")
    print(f"  在 w* 处梯度 ≈ {gradients[w_opt_idx]:.6f} (应为 0)")


# ============================================================
# 主入口 (Main)
# ============================================================

if __name__ == "__main__":
    print("线性模型从零实现 (Linear Models from Scratch)")
    print("=" * 60)

    # 1. 线性回归
    lr_cf, lr_gd = demo_linear_regression()

    # 2. 逻辑回归
    logreg = demo_logistic_regression()

    # 3. 正则化
    demo_regularization()

    # 4. 核心概念
    demo_core_concepts()

    print("\n" + "=" * 60)
    print("全部演示完成! (All demos complete!)")
    print(f"输出目录 (Output dir): {OUTPUT_DIR}")
    print("=" * 60)
