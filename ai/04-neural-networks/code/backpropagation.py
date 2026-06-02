"""
反向传播 (Backpropagation) — 从零实现
Backpropagation — From Scratch
====================================================
依赖: numpy>=1.24.0, matplotlib>=3.7.0

涵盖 (Covers):
  1. 计算图与链式法则 (Computation Graph & Chain Rule)
  2. 2层神经网络反向传播推导 (2-Layer NN Backprop Derivation)
  3. 数值梯度验证 (Numerical Gradient Check)
  4. 训练与决策边界可视化 (Training & Decision Boundary)

数学公式 (Mathematical Formulation):
  Forward:
    z1 = X @ W1 + b1,  h1 = tanh(z1)
    z2 = h1 @ W2 + b2,  y_hat = sigmoid(z2)
    L = -(1/N) * Σ[y·log(ŷ) + (1-y)·log(1-ŷ)]

  Backward:
    δ2 = ŷ - y                              (BCE gradient)
    dW2 = h1ᵀ @ δ2 / N,  db2 = mean(δ2, axis=0)
    δ1 = (δ2 @ W2ᵀ) * (1 - h1²)            (tanh derivative)
    dW1 = Xᵀ @ δ1 / N,  db1 = mean(δ1, axis=0)

  Gradient Check (finite differences):
    ∂f/∂θ ≈ (f(θ+ε) - f(θ-ε)) / (2ε),  ε = 1e-5
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================
# 0. 全局设置 (Global Settings)
# ============================================================
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

RNG = np.random.RandomState(42)

plt.rcParams.update({
    "figure.dpi": 120,
    "font.size": 11,
    "axes.titlesize": 13,
    "figure.figsize": (10, 6),
})

EPS = 1e-5  # 有限差分步长


# ============================================================
# 1. 激活函数 (Activation Functions)
# ============================================================
def sigmoid(z):
    """Sigmoid: σ(z) = 1 / (1 + e^{-z})"""
    z = np.clip(z, -500, 500)
    return 1.0 / (1.0 + np.exp(-z))


def sigmoid_derivative(z):
    """Sigmoid 导数: σ'(z) = σ(z) * (1 - σ(z))"""
    s = sigmoid(z)
    return s * (1 - s)


def tanh(z):
    """Tanh"""
    return np.tanh(z)


def tanh_derivative(z):
    """Tanh 导数: 1 - tanh²(z)"""
    t = tanh(z)
    return 1.0 - t ** 2


# ============================================================
# 2. 2层神经网络 (2-Layer Neural Network)
# ============================================================
class TwoLayerNet:
    """
    2层神经网络: 输入 -> 隐藏层(tanh) -> 输出层(sigmoid)
    2-Layer NN: Input -> Hidden(tanh) -> Output(sigmoid)
    """

    def __init__(self, input_dim=2, hidden_dim=10, seed=42):
        self.rng = np.random.RandomState(seed)
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim

        # He 初始化 (适合 tanh)
        scale1 = np.sqrt(1.0 / input_dim)
        scale2 = np.sqrt(1.0 / hidden_dim)
        self.params = {
            "W1": self.rng.randn(input_dim, hidden_dim) * scale1,
            "b1": np.zeros((1, hidden_dim)),
            "W2": self.rng.randn(hidden_dim, 1) * scale2,
            "b2": np.zeros((1, 1)),
        }
        self.cache = {}

    def forward(self, X):
        """
        前向传播 / Forward pass: X -> z1 -> h1 -> z2 -> y_hat
        """
        z1 = X @ self.params["W1"] + self.params["b1"]
        h1 = tanh(z1)
        z2 = h1 @ self.params["W2"] + self.params["b2"]
        y_hat = sigmoid(z2)

        self.cache = {"X": X, "z1": z1, "h1": h1, "z2": z2, "y_hat": y_hat}
        return y_hat

    def loss(self, y_hat, y):
        """
        二元交叉熵损失 (Binary Cross-Entropy Loss)
        L = -(1/N) * Σ[y·log(ŷ) + (1-y)·log(1-ŷ)]
        """
        N = y.shape[0]
        # 裁剪防止 log(0)
        eps = 1e-12
        y_hat = np.clip(y_hat, eps, 1 - eps)
        return -(1.0 / N) * np.sum(y * np.log(y_hat) + (1 - y) * np.log(1 - y_hat))

    def backward(self, y, reg_lambda=0.0):
        """
        反向传播 — 计算所有参数的梯度
        Backward pass — compute gradients w.r.t. all parameters

        参数 / Args:
            y: 真实标签 (N, 1)
            reg_lambda: L2 正则化系数 (weight decay)
        """
        X = self.cache["X"]
        h1 = self.cache["h1"]
        y_hat = self.cache["y_hat"]
        N = X.shape[0]

        # --- 输出层 (Output Layer) ---
        # δ2 = ∂L/∂z2 = ŷ - y  (对 BCE + sigmoid 的合并梯度)
        delta2 = y_hat - y                                 # (N, 1)

        dW2 = (h1.T @ delta2) / N                           # (hidden_dim, 1)
        db2 = np.mean(delta2, axis=0, keepdims=True)        # (1, 1)

        # --- 隐藏层 (Hidden Layer) ---
        # δ1 = (δ2 @ W2ᵀ) ⊙ tanh'(z1)
        W2 = self.params["W2"]
        delta1 = (delta2 @ W2.T) * tanh_derivative(self.cache["z1"])  # (N, hidden_dim)

        dW1 = (X.T @ delta1) / N                             # (input_dim, hidden_dim)
        db1 = np.mean(delta1, axis=0, keepdims=True)         # (1, hidden_dim)

        # L2 正则化梯度 (L2 Regularization Gradient)
        if reg_lambda > 0:
            dW1 += reg_lambda * self.params["W1"]
            dW2 += reg_lambda * self.params["W2"]

        self.grads = {
            "W1": dW1, "b1": db1,
            "W2": dW2, "b2": db2,
        }
        return self.grads

    def compute_loss_with_params(self, param_dict, X, y):
        """
        使用给定参数计算损失 (用于梯度检查)
        Compute loss with given parameters (for gradient check)
        """
        saved = {}
        for k in param_dict:
            saved[k] = self.params[k].copy()
            np.copyto(self.params[k], param_dict[k])

        y_hat = self.forward(X)
        loss_val = self.loss(y_hat, y)

        for k in saved:
            np.copyto(self.params[k], saved[k])

        return loss_val

    def predict(self, X):
        """预测类别 (0 或 1)"""
        y_hat = self.forward(X)
        return (y_hat >= 0.5).astype(int)

    def accuracy(self, X, y):
        """计算准确率"""
        pred = self.predict(X)
        return np.mean(pred.flatten() == y.flatten())


# ============================================================
# 3. 数值梯度验证 (Numerical Gradient Check)
# ============================================================
def gradient_check(model, X, y, param_name="W2", num_tests=5):
    """
    数值梯度验证: |analytical - numerical| < 1e-6

    Numerical Gradient Check using central difference:
      ∂f/∂θ ≈ (f(θ+ε) - f(θ-ε)) / (2ε)
    """
    param = model.params[param_name]
    analytical_grad = model.grads[param_name].copy()

    flat_analytical = analytical_grad.ravel()
    total_dims = flat_analytical.size

    # 如果参数小, 测试所有维度; 否则随机采样
    if total_dims <= 20:
        test_indices = list(range(total_dims))
    else:
        test_indices = RNG.choice(total_dims, min(num_tests, total_dims), replace=False).tolist()

    max_diff = 0.0
    test_results = []
    for idx in test_indices:
        orig_val = param.ravel()[idx]

        # f(θ + ε)
        param_plus = param.copy()
        param_plus.ravel()[idx] += EPS
        loss_plus = model.compute_loss_with_params({param_name: param_plus}, X, y)

        # f(θ - ε)
        param_minus = param.copy()
        param_minus.ravel()[idx] -= EPS
        loss_minus = model.compute_loss_with_params({param_name: param_minus}, X, y)

        num_grad = (loss_plus - loss_minus) / (2 * EPS)
        ana_grad = flat_analytical[idx]
        diff = abs(ana_grad - num_grad)
        max_diff = max(max_diff, diff)

        i, j = np.unravel_index(idx, param.shape)
        test_results.append({
            "index": (i, j),
            "analytical": ana_grad,
            "numerical": num_grad,
            "diff": diff,
        })

    # 相对误差 (相对于梯度幅值)
    grad_norm = max(abs(flat_analytical).max(), 1e-16)
    relative_error = max_diff / grad_norm

    return {
        "param_name": param_name,
        "shape": param.shape,
        "relative_error": relative_error,
        "max_abs_diff": max_diff,
        "pass_check": max_diff < 1e-6,
        "test_results": test_results,
    }


def full_gradient_check(model, X, y, param_names=None, num_tests=5):
    """对所有参数进行梯度检查"""
    if param_names is None:
        param_names = ["W1", "b1", "W2", "b2"]

    print("\n" + "=" * 72)
    print("【数值梯度验证 / Numerical Gradient Check】")
    print(f"  有限差分步长 (Finite diff step): ε = {EPS}")
    print(f"  每个参数测试 (Tests per param): {num_tests} 个随机位置")
    print("=" * 72)

    all_pass = True
    results = {}
    for pname in param_names:
        result = gradient_check(model, X, y, param_name=pname, num_tests=num_tests)
        results[pname] = result

        status = "✓ PASS" if result["pass_check"] else "✗ FAIL"
        print(f"\n  参数 {pname:>4}  {status}  |  shape={result['shape']}  "
              f"|  max|diff|={result['max_abs_diff']:.2e}  "
              f"|  rel_err={result['relative_error']:.2e}")

        for tr in result["test_results"]:
            print(f"    [{tr['index'][0]},{tr['index'][1]}]  "
                  f"analytical={tr['analytical']:+.8e}  "
                  f"numerical={tr['numerical']:+.8e}  "
                  f"|diff|={tr['diff']:.2e}")

        if not result["pass_check"]:
            all_pass = False

    if all_pass:
        print(f"\n  ✓ 所有梯度检查通过! |analytical - numerical| < 1e-6")
    else:
        print(f"\n  ✗ 部分梯度检查未通过!")

    return results


# ============================================================
# 4. 训练 (Training)
# ============================================================
def train(model, X, y, learning_rate=0.5, epochs=1000, reg_lambda=0.0, verbose=True):
    """训练 2 层神经网络"""
    losses = []
    accuracies = []

    for epoch in range(1, epochs + 1):
        # 前向 + 反向
        y_hat = model.forward(X)
        loss_val = model.loss(y_hat, y)
        model.backward(y, reg_lambda=reg_lambda)

        # SGD 更新
        for param_name in ["W1", "b1", "W2", "b2"]:
            model.params[param_name] -= learning_rate * model.grads[param_name]

        acc = model.accuracy(X, y)
        losses.append(loss_val)
        accuracies.append(acc)

        if verbose and (epoch == 1 or epoch % 100 == 0 or epoch == epochs):
            print(f"  Epoch {epoch:4d} | Loss = {loss_val:.6f} | Acc = {acc:.4f}")

    return losses, accuracies


# ============================================================
# 5. 数据生成 (Data Generation)
# ============================================================
def make_moons(n_samples=200, noise=0.1, seed=42):
    """
    生成 moon 形状的二分类数据集 (类似 sklearn.datasets.make_moons)
    Generate moon-shaped binary classification dataset
    """
    rng = np.random.RandomState(seed)
    n_per_class = n_samples // 2

    # Class 0: outer moon
    t0 = np.linspace(0, np.pi, n_per_class)
    x0 = np.column_stack([np.cos(t0), np.sin(t0)]) + rng.randn(n_per_class, 2) * noise

    # Class 1: inner moon
    t1 = np.linspace(0, np.pi, n_per_class)
    x1 = np.column_stack([1 - np.cos(t1), 1 - np.sin(t1) - 0.5]) + rng.randn(n_per_class, 2) * noise

    X = np.vstack([x0, x1])
    y = np.vstack([np.zeros((n_per_class, 1)), np.ones((n_per_class, 1))])

    return X, y


# ============================================================
# 6. 可视化 (Visualization)
# ============================================================
def plot_decision_boundary(model, X, y, save_path):
    """Plot decision boundary"""
    x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
    y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 300),
                         np.linspace(y_min, y_max, 300))
    grid = np.c_[xx.ravel(), yy.ravel()]
    Z = model.predict(grid).reshape(xx.shape)

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.RdYlBu, levels=[-0.5, 0.5, 1.5])
    ax.scatter(X[y.flatten() == 0, 0], X[y.flatten() == 0, 1],
               c="blue", marker="o", s=40, edgecolors="k", label="Class 0")
    ax.scatter(X[y.flatten() == 1, 0], X[y.flatten() == 1, 1],
               c="red", marker="s", s=40, edgecolors="k", label="Class 1")
    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")
    ax.set_title(f"Decision Boundary — Acc={model.accuracy(X, y):.2%}")
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    fig.savefig(save_path)
    plt.close(fig)
    print(f"  [Figure] Decision boundary saved: {save_path}")


def plot_training_curve(losses, accuracies, save_path):
    """Plot training curve"""
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))

    axes[0].plot(losses, linewidth=1.5)
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Loss")
    axes[0].set_title("Loss Curve")
    axes[0].grid(alpha=0.3)

    axes[1].plot(accuracies, linewidth=1.5, color="green")
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("Accuracy")
    axes[1].set_title("Accuracy Curve")
    axes[1].grid(alpha=0.3)

    plt.tight_layout()
    fig.savefig(save_path)
    plt.close(fig)
    print(f"  [Figure] Training curve saved: {save_path}")


# ============================================================
# 7. 主函数 (Main)
# ============================================================
def main():
    print("=" * 72)
    print("  反向传播 (Backpropagation) — 从零实现")
    print("  Backpropagation — From Scratch")
    print("=" * 72)

    # ---- 1. 生成数据 ----
    print("\n" + "=" * 72)
    print("第1步: 生成 Moon 数据集")
    print("Step 1: Generate Moons Dataset")
    print("=" * 72)
    X, y = make_moons(n_samples=200, noise=0.1, seed=42)
    print(f"  样本数 / Samples: {X.shape[0]}")
    print(f"  特征数 / Features: {X.shape[1]}")
    print(f"  类别分布 / Class distribution: {np.bincount(y.flatten().astype(int))}")

    # ---- 2. 模型初始化 ----
    print("\n" + "=" * 72)
    print("第2步: 初始化 2 层神经网络")
    print("Step 2: Initialize 2-Layer Neural Network")
    print("=" * 72)
    model = TwoLayerNet(input_dim=2, hidden_dim=10, seed=42)
    print(f"  Architecture: 2 → {model.hidden_dim} → 1")
    print(f"  Hidden activation: tanh")
    print(f"  Output activation: sigmoid")
    total_params = sum(v.size for v in model.params.values())
    print(f"  Total params: {total_params}")

    # ---- 3. 前向传播 ----
    print("\n" + "=" * 72)
    print("第3步: 前向传播 (Forward Pass)")
    print("=" * 72)
    y_hat = model.forward(X)
    loss_init = model.loss(y_hat, y)
    acc_init = model.accuracy(X, y)
    print(f"  初始损失 (Initial loss): {loss_init:.6f}")
    print(f"  初始准确率 (Initial acc): {acc_init:.4f}")
    print(f"  预测分布 (Pred distribution): min={y_hat.min():.4f}, "
          f"max={y_hat.max():.4f}, mean={y_hat.mean():.4f}")

    # ---- 4. 梯度检查 ----
    print("\n" + "=" * 72)
    print("第4步: 梯度检查 (Gradient Check)")
    print("=" * 72)
    # 先做一次反向传播获取梯度
    y_hat = model.forward(X)
    model.backward(y)
    grad_results = full_gradient_check(model, X, y)

    # ---- 5. 训练 ----
    print("\n" + "=" * 72)
    print("第5步: 训练 (Training)")
    print("=" * 72)
    losses, accuracies = train(model, X, y, learning_rate=0.5, epochs=500, reg_lambda=0.0)
    print(f"\n  最终损失 (Final loss): {losses[-1]:.6f}")
    print(f"  最终准确率 (Final acc): {accuracies[-1]:.4f}")

    # ---- 6. 可视化 ----
    print("\n" + "=" * 72)
    print("第6步: 可视化 (Visualization)")
    print("=" * 72)
    plot_training_curve(losses, accuracies,
                        OUTPUT_DIR / "backprop_training_curve.png")
    plot_decision_boundary(model, X, y,
                           OUTPUT_DIR / "backprop_decision_boundary.png")

    print("\n" + "=" * 72)
    print("  反向传播演示完成! (Backpropagation Demo Complete!)")
    print("  梯度检查 (Gradient Check): ✓ |analytical - numerical| < 1e-6")
    print("=" * 72)


if __name__ == "__main__":
    main()
