"""
感知机 (Perceptron) 与多层感知机 (MLP) — 从零实现
(Perceptron & Multi-Layer Perceptron — From Scratch)
=========================================================
依赖: numpy>=1.24.0, matplotlib>=3.7.0

涵盖 (Covers):
  1. 感知机学习算法 (Perceptron Learning Algorithm)
     - 2D 线性可分数据集, 决策边界演化
     - 收敛性验证 (Rosenblatt 1958)
  2. 激活函数 (Activation Functions)
     - Sigmoid, Tanh, ReLU, GELU, 及其导数
     - 函数图像与数值对比
  3. MLP 前向传播 (Forward Pass)
     - 逐层矩阵计算, 隐藏层激活可视化
  4. XOR 问题 — 单层感知机的局限 vs MLP
  5. 万能近似定理演示 (用 MLP 拟合正弦波)

数学公式 (Mathematical Formulation):
  Perceptron update:   w ← w + η(y_i - ŷ_i)x_i
  MLP Forward:         a^{(l)} = σ(W^{(l)} a^{(l-1)} + b^{(l)})
  Sigmoid:             σ(z) = 1 / (1 + e^{-z})
  Tanh:                tanh(z) = (e^{z} - e^{-z}) / (e^{z} + e^{-z})
  ReLU:                relu(z) = max(0, z)
  GELU:                gelu(z) = z * Φ(z),  Φ = standard normal CDF
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


# ============================================================
# 1. 激活函数 (Activation Functions) 及其导数
# ============================================================
def sigmoid(z):
    """Sigmoid 激活函数: σ(z) = 1 / (1 + e^{-z})"""
    z = np.clip(z, -500, 500)  # 防止溢出
    return 1.0 / (1.0 + np.exp(-z))


def sigmoid_derivative(z):
    """Sigmoid 导数: σ'(z) = σ(z) * (1 - σ(z))"""
    s = sigmoid(z)
    return s * (1 - s)


def tanh(z):
    """双曲正切: tanh(z) = (e^{z} - e^{-z}) / (e^{z} + e^{-z})"""
    return np.tanh(z)


def tanh_derivative(z):
    """Tanh 导数: tanh'(z) = 1 - tanh^2(z)"""
    t = tanh(z)
    return 1.0 - t ** 2


def relu(z):
    """ReLU: max(0, z)"""
    return np.maximum(0, z)


def relu_derivative(z):
    """ReLU 导数: 1 if z > 0 else 0"""
    return (z > 0).astype(float)


def gelu(z):
    """GELU (Gaussian Error Linear Unit): z * Φ(z)"""
    # Φ(z) ≈ 0.5 * (1 + tanh(sqrt(2/π) * (z + 0.044715 * z^3)))
    return z * 0.5 * (1.0 + np.tanh(np.sqrt(2.0 / np.pi) * (z + 0.044715 * z ** 3)))


def gelu_derivative(z):
    """GELU 导数 (近似)"""
    c = np.sqrt(2.0 / np.pi)
    inner = c * (z + 0.044715 * z ** 3)
    tanh_inner = np.tanh(inner)
    # d/dz [z * 0.5 * (1 + tanh(inner))]
    # = 0.5 * (1 + tanh(inner)) + 0.5 * z * (1 - tanh(inner)^2) * c * (1 + 3*0.044715*z^2)
    sech2 = 1.0 - tanh_inner ** 2
    return 0.5 * (1.0 + tanh_inner) + 0.5 * z * sech2 * c * (1.0 + 0.134145 * z ** 2)


def swiglu(x, gate):
    """SwiGLU: x * sigmoid(gate) * gate (简化版: Swish(x) * gate)"""
    return x * sigmoid(gate)


# ============================================================
# 2. 激活函数数值评估与可视化
# ============================================================
def demo_activation_functions():
    """演示所有激活函数及其导数的数值输出与图像"""
    print("=" * 72)
    print("第1部分: 激活函数 (Activation Functions)")
    print("Part 1: Activation Functions")
    print("=" * 72)

    z_vals = np.array([-3.0, -2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0, 3.0])

    activations = {
        "Sigmoid": (sigmoid, sigmoid_derivative),
        "Tanh": (tanh, tanh_derivative),
        "ReLU": (relu, relu_derivative),
        "GELU": (gelu, gelu_derivative),
    }

    # --- 数值表 ---
    print("\n【数值对比表 / Numerical Comparison】")
    print(f"{'z':>6} |", end="")
    for name in activations:
        print(f" {name:>8}", end="")
    print()
    print("-" * 6 + "-+-" + "-" * 9 * len(activations))

    for z in z_vals:
        print(f"{z:>6.1f} |", end="")
        for name, (func, _) in activations.items():
            val = func(np.array([z]))[0]
            print(f" {val:>8.5f}", end="")
        print()

    # --- 各激活函数的导数表 ---
    print("\n【导数对比表 / Derivative Comparison】")
    print(f"{'z':>6} |", end="")
    for name in activations:
        print(f" d({name})", end="")
    print()
    print("-" * 6 + "-+-" + "-" * 9 * len(activations))

    for z in z_vals:
        print(f"{z:>6.1f} |", end="")
        for name, (_, deriv) in activations.items():
            val = deriv(np.array([z]))[0]
            print(f" {val:>8.5f}", end="")
        print()

    # --- 关键性质验证 ---
    print("\n【关键性质验证 / Key Properties】")
    print(f"Sigmoid(0) = {sigmoid(np.array([0.0]))[0]:.6f}  (理论值 0.5)")
    print(f"Tanh(0)    = {tanh(np.array([0.0]))[0]:.6f}  (理论值 0.0)")
    print(f"ReLU(-1)   = {relu(np.array([-1.0]))[0]:.6f}  (理论值 0.0)")
    print(f"ReLU(1)    = {relu(np.array([1.0]))[0]:.6f}  (理论值 1.0)")

    # --- GELU vs ReLU 对比 ---
    print("\n【GELU vs ReLU 在 z≈0 附近的平滑行为】")
    for z in [-0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3]:
        r = relu(np.array([z]))[0]
        g = gelu(np.array([z]))[0]
        print(f"  z={z:>5.2f} | ReLU={r:>8.5f} | GELU={g:>8.5f} | 差值={g - r:>+8.5f}")

    # --- 可视化 ---
    z_smooth = np.linspace(-5, 5, 500)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # 左: 函数值
    ax = axes[0]
    for name, (func, _) in activations.items():
        ax.plot(z_smooth, func(z_smooth), label=name, linewidth=2)
    ax.axhline(0, color="gray", linestyle="--", alpha=0.3)
    ax.axhline(1, color="gray", linestyle="--", alpha=0.3)
    ax.set_xlabel("z")
    ax.set_ylabel("σ(z)")
    ax.set_title("激活函数 (Activation Functions)")
    ax.legend()
    ax.grid(alpha=0.3)

    # 右: 导数
    ax = axes[1]
    for name, (_, deriv) in activations.items():
        ax.plot(z_smooth, deriv(z_smooth), label=f"d({name})/dz", linewidth=2)
    ax.axhline(0, color="gray", linestyle="--", alpha=0.3)
    ax.set_xlabel("z")
    ax.set_ylabel("σ'(z)")
    ax.set_title("导数 (Derivatives)")
    ax.legend()
    ax.grid(alpha=0.3)

    plt.tight_layout()
    path = OUTPUT_DIR / "activation_functions.png"
    fig.savefig(path)
    plt.close(fig)
    print(f"\n[图] 激活函数图像已保存: {path}")

    return activations


# ============================================================
# 3. 感知机 (Perceptron) 学习算法
# ============================================================
class Perceptron:
    """
    感知机: 二分类线性模型
    Rosenblatt (1958)
    """

    def __init__(self, learning_rate=0.1, max_epochs=100):
        self.lr = learning_rate
        self.max_epochs = max_epochs
        self.w = None
        self.b = None
        self.history = []  # 记录每次更新的权重

    def fit(self, X, y):
        """
        感知机学习算法
        更新规则: w ← w + η(y_i - ŷ_i)x_i
        """
        n_samples, n_features = X.shape
        self.w = np.zeros(n_features)
        self.b = 0.0
        self.history = []

        print(f"\n{'=' * 72}")
        print(f"第2部分: 感知机学习算法")
        print(f"Part 2: Perceptron Learning Algorithm")
        print(f"{'=' * 72}")
        print(f"数据集: {n_samples} 个样本, {n_features} 个特征")
        print(f"学习率 η = {self.lr}, 最大迭代 = {self.max_epochs}")

        for epoch in range(1, self.max_epochs + 1):
            errors = 0
            for i in range(n_samples):
                # 线性预测
                linear_output = np.dot(X[i], self.w) + self.b
                y_pred = 1 if linear_output >= 0 else -1

                # 感知机更新规则
                update = self.lr * (y[i] - y_pred)
                if update != 0:
                    self.w += update * X[i]
                    self.b += update * 1  # 总是乘以 1
                    errors += 1
                    self.history.append((epoch, self.w.copy(), self.b, y_pred, y[i]))

            if epoch <= 3 or epoch % 10 == 0 or errors == 0:
                print(f"  Epoch {epoch:3d}: 误分类数 (misclassifications) = {errors}  "
                      f"| w = [{self.w[0]:+.4f}, {self.w[1]:+.4f}]  b = {self.b:+.4f}")

            if errors == 0:
                print(f"\n  ✓ 第 {epoch} 轮收敛! 所有样本正确分类。")
                print(f"  ✓ Converged at epoch {epoch}! All samples correctly classified.\n")
                break

        return self

    def predict(self, X):
        linear = np.dot(X, self.w) + self.b
        return np.where(linear >= 0, 1, -1)

    def decision_boundary(self, X, y, epoch_info=""):
        """绘制决策边界"""
        x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
        y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
        xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200),
                             np.linspace(y_min, y_max, 200))
        Z = self.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)

        fig, ax = plt.subplots(figsize=(7, 6))
        ax.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.RdYlBu, levels=[-2, 0, 2])
        ax.scatter(X[y == 1, 0], X[y == 1, 1], c="blue", marker="o", s=60,
                   edgecolors="k", label="Class +1")
        ax.scatter(X[y == -1, 0], X[y == -1, 1], c="red", marker="s", s=60,
                   edgecolors="k", label="Class -1")
        ax.set_xlabel("$x_1$")
        ax.set_ylabel("$x_2$")
        ax.set_title(f"感知机决策边界 {epoch_info}\n(Perceptron Decision Boundary)")
        ax.legend()
        ax.grid(alpha=0.3)
        plt.tight_layout()
        return fig


def demo_perceptron():
    """演示感知机学习过程"""
    print("\n" + "=" * 72)
    print("第2.1节: 线性可分数据 — 感知机收敛")
    print("Section 2.1: Linearly Separable Data — Perceptron Converges")
    print("=" * 72)

    # 生成 2D 线性可分数据
    X = np.array([
        [2.0, 2.0], [1.5, 3.0], [3.0, 1.0], [2.5, 2.5],
        [0.5, 1.0], [1.0, 0.5], [0.0, 0.0], [-0.5, 1.5],
        [3.5, 3.0], [4.0, 2.0],
    ])
    y = np.array([1, 1, 1, 1, 1, -1, -1, -1, -1, -1])

    # 修正: 让数据真正线性可分
    # 类别 +1: 右上区域, 类别 -1: 左下区域
    # 调整 (0.5, 1.0) 和 (1.0, 0.5) 到更明确的区域
    X = np.array([
        # Class +1 (右上)
        [2.5, 2.5], [2.0, 3.0], [3.0, 2.0], [3.5, 1.5], [1.8, 2.8],
        # Class -1 (左下)
        [0.5, 0.5], [1.0, 0.0], [0.0, 1.0], [-0.5, 0.0], [1.2, 0.3],
    ])
    y = np.array([1, 1, 1, 1, 1, -1, -1, -1, -1, -1])

    print(f"训练数据 / Training Data:")
    print(f"{'i':>3} | {'x1':>6} {'x2':>6} | {'y':>3}")
    print("-" * 26)
    for i in range(len(X)):
        print(f"{i:>3} | {X[i, 0]:>6.2f} {X[i, 1]:>6.2f} | {y[i]:>+3d}")

    p = Perceptron(learning_rate=0.1, max_epochs=50)
    p.fit(X, y)

    # 验证预测
    y_pred = p.predict(X)
    accuracy = np.mean(y_pred == y) * 100
    print(f"\n训练准确率 (Training Accuracy): {accuracy:.1f}% ({int(accuracy * len(X) / 100)}/{len(X)})")
    print(f"最终权重 w = [{p.w[0]:.4f}, {p.w[1]:.4f}], b = {p.b:.4f}")
    print(f"决策边界方程: {p.w[0]:.4f} * x1 + {p.w[1]:.4f} * x2 + ({p.b:.4f}) = 0")

    # 保存决策边界图
    fig = p.decision_boundary(X, y, epoch_info=f"(Epoch {p.history[-1][0] if p.history else 0})")
    path = OUTPUT_DIR / "perceptron_decision_boundary.png"
    fig.savefig(path)
    plt.close(fig)
    print(f"[图] 决策边界已保存: {path}")

    # --- 收敛性验证 ---
    print(f"\n【收敛性验证 / Convergence Verification】")
    print(f"总更新次数 (Total updates): {len(p.history)}")
    print(f"更新历史 (前5次 / First 5):")
    for i, (ep, w, b, yp, yt) in enumerate(p.history[:5]):
        print(f"  Update {i + 1}: epoch={ep}, "
              f"Δw=[{w[0]:+.4f},{w[1]:+.4f}], Δb={b:+.4f}, pred={yp}, target={yt}")
    if len(p.history) > 5:
        print(f"  ... 共 {len(p.history)} 次更新 (~{len(p.history) - 5} more)")

    # --- 保存权重演化图 ---
    if len(p.history) > 1:
        w_hist = np.array([h[1] for h in p.history])
        fig, axes = plt.subplots(1, 2, figsize=(11, 4))
        axes[0].plot(w_hist[:, 0], label="$w_1$", linewidth=2)
        axes[0].plot(w_hist[:, 1], label="$w_2$", linewidth=2)
        axes[0].set_xlabel("更新步数 (Update step)")
        axes[0].set_ylabel("权重值 (Weight value)")
        axes[0].set_title("权重收敛过程 (Weight Convergence)")
        axes[0].legend()
        axes[0].grid(alpha=0.3)

        b_hist = np.array([h[2] for h in p.history])
        axes[1].plot(b_hist, linewidth=2, color="green")
        axes[1].set_xlabel("更新步数 (Update step)")
        axes[1].set_ylabel("偏置值 (Bias value)")
        axes[1].set_title("偏置收敛过程 (Bias Convergence)")
        axes[1].grid(alpha=0.3)

        plt.tight_layout()
        path = OUTPUT_DIR / "perceptron_weight_evolution.png"
        fig.savefig(path)
        plt.close(fig)
        print(f"[图] 权重演化已保存: {path}")

    return p


def demo_xor_problem():
    """演示 XOR 问题: 感知机的局限"""
    print("\n" + "=" * 72)
    print("第2.2节: XOR 问题 — 单层感知机的局限")
    print("Section 2.2: XOR Problem — Limitation of Single-Layer Perceptron")
    print("=" * 72)

    # XOR 数据 (非线性可分)
    X_xor = np.array([
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1],
    ], dtype=float)
    y_xor = np.array([-1, 1, 1, -1])

    print("XOR 数据集 / XOR Dataset:")
    print(f"{'x1':>4} {'x2':>4} | {'y':>3}")
    print("-" * 15)
    for i in range(4):
        print(f"{X_xor[i, 0]:>4.0f} {X_xor[i, 1]:>4.0f} | {y_xor[i]:>+3d}")

    p_xor = Perceptron(learning_rate=0.1, max_epochs=100)
    p_xor.fit(X_xor, y_xor)

    y_xor_pred = p_xor.predict(X_xor)
    xor_acc = np.mean(y_xor_pred == y_xor) * 100
    print(f"\nXOR 准确率 (XOR Accuracy): {xor_acc:.1f}%")
    print(f"预测结果 (Predictions): {y_xor_pred}")
    print(f"真实标签 (True labels):  {y_xor}")

    if xor_acc < 100:
        print("\n  ✓ 验证了单层感知机无法解决 XOR 问题!")
        print("  ✓ Verified: Single-layer perceptron cannot solve XOR!")
        print("  原因: XOR 不是线性可分的 (XOR is not linearly separable)")
    else:
        print("  感知机出人意料地解决了 XOR — 但理论上不可能!")

    # 保存 XOR 数据可视化
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.scatter(X_xor[y_xor == 1, 0], X_xor[y_xor == 1, 1],
               c="blue", marker="o", s=200, label="Class +1 (XOR=1)", edgecolors="k")
    ax.scatter(X_xor[y_xor == -1, 0], X_xor[y_xor == -1, 1],
               c="red", marker="s", s=200, label="Class -1 (XOR=0)", edgecolors="k")
    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")
    ax.set_title("XOR 问题 — 非线性可分\n(No linear separator exists)")
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    path = OUTPUT_DIR / "xor_problem.png"
    fig.savefig(path)
    plt.close(fig)
    print(f"[图] XOR 问题可视化已保存: {path}")

    return xor_acc


# ============================================================
# 4. MLP 前向传播 (Forward Pass)
# ============================================================
class MLP:
    """
    多层感知机 (Multi-Layer Perceptron)
    仅实现前向传播 (Forward Pass) — 无反向传播
    """

    def __init__(self, layer_sizes, activation="relu"):
        """
        参数 / Args:
          layer_sizes: 每层神经元数的列表, e.g. [2, 4, 1]
          activation: 激活函数名称 ("relu", "sigmoid", "tanh", "gelu")
        """
        self.layer_sizes = layer_sizes
        self.num_layers = len(layer_sizes) - 1  # 隐藏层+输出层数

        self.activation_name = activation
        self.activation, self.activation_deriv = self._get_activation(activation)

        # 初始化权重和偏置 (He 初始化 / Xavier 初始化)
        self.params = {}
        for l in range(1, len(layer_sizes)):
            if activation in ("relu", "gelu"):
                # He 初始化
                scale = np.sqrt(2.0 / layer_sizes[l - 1])
            else:
                # Xavier 初始化
                scale = np.sqrt(1.0 / layer_sizes[l - 1])
            self.params[f"W{l}"] = RNG.randn(layer_sizes[l - 1], layer_sizes[l]) * scale
            self.params[f"b{l}"] = np.zeros((1, layer_sizes[l]))

        print(f"\n{'=' * 72}")
        print(f"第3部分: MLP 前向传播 (Forward Pass)")
        print(f"{'=' * 72}")
        print(f"网络结构 (Network architecture): {layer_sizes}")
        print(f"激活函数 (Activation): {activation}")
        print(f"参数总量 (Total params): {sum(p.size for p in self.params.values())}")

    def _get_activation(self, name):
        mapping = {
            "relu": (relu, relu_derivative),
            "sigmoid": (sigmoid, sigmoid_derivative),
            "tanh": (tanh, tanh_derivative),
            "gelu": (gelu, gelu_derivative),
        }
        return mapping[name]

    def forward(self, X, verbose=True):
        """
        完整前向传播

        参数 / Args:
          X: 输入 (batch_size, input_dim)
          verbose: 是否打印逐层数值

        返回:
          cache: 包含各层 z 和 a 的字典
        """
        cache = {"a0": X}

        for l in range(1, self.num_layers + 1):
            W = self.params[f"W{l}"]
            b = self.params[f"b{l}"]
            a_prev = cache[f"a{l - 1}"]

            # 线性变换: z = W^T * a_prev + b
            # W shape: (n_in, n_out), a_prev shape: (batch, n_in)
            z = np.dot(a_prev, W) + b

            # 非线性激活: a = σ(z)
            a = self.activation(z)

            cache[f"z{l}"] = z
            cache[f"a{l}"] = a

            if verbose:
                print(f"\n  第{l}层 (Layer {l}): {W.shape[0]} → {W.shape[1]} 个神经元")
                print(f"    W{l} 权重矩阵 (weights) shape: {W.shape}")
                print(f"    b{l} 偏置 (bias) shape: {b.shape}")
                print(f"    z{l} (线性输出) = a(l-1)·W + b")
                if z.shape[1] == 1:
                    print(f"      z{l} = [{z[0, 0]:+.6f}] (每行第一个批次)")
                elif z.shape[1] <= 4:
                    z_vals_str = ", ".join(f"{z[0, j]:+.6f}" for j in range(z.shape[1]))
                    print(f"      z{l} = [{z_vals_str}] (每行第一个批次)")
                else:
                    print(f"      z{l} shape: {z.shape}")
                if a.shape[1] <= 4:
                    print(f"    a{l} ({self.activation_name}) = σ(z{l}) = [{', '.join(f'{x:+.6f}' for x in a[0])}]")

        return cache

    def forward_full(self, X, verbose=True):
        """带输出层 (无激活) 的前向传播"""
        cache = self.forward(X, verbose=verbose)

        # 输出层: 通常不使用激活 (或使用线性激活)
        l_out = self.num_layers
        W_out = self.params[f"W{l_out}"]
        b_out = self.params[f"b{l_out}"]
        a_prev = cache[f"a{l_out}"]

        # 对于输出层, 我们使用线性激活 (回归任务)
        z_out = np.dot(a_prev, W_out) + b_out
        cache[f"z{l_out + 1}"] = z_out
        cache[f"a{l_out + 1}"] = z_out  # 线性激活: a = z

        if verbose:
            print(f"\n  输出层 (Output layer): 线性激活 (linear)")
            print(f"    z_out = {z_out[0]} (第一个样本的预测值)")

        return cache


def demo_mlp_forward():
    """演示 MLP 前向传播逐层计算"""
    print("\n" + "=" * 72)
    print("第3.1节: 逐层前向传播演示")
    print("Section 3.1: Layer-by-Layer Forward Pass")
    print("=" * 72)

    # 小规模网络: 2个输入 → 4个隐藏 → 1个输出
    mlp = MLP(layer_sizes=[2, 4, 1], activation="relu")

    # 打印初始参数
    print("\n初始参数 (Initial Parameters):")
    for l in range(1, mlp.num_layers + 1):
        W = mlp.params[f"W{l}"]
        b = mlp.params[f"b{l}"]
        print(f"\n  W{l} (权重 / weights):")
        print(f"    {W}")
        print(f"  b{l} (偏置 / bias):")
        print(f"    {b}")

    # 制造两个输入样本
    X = np.array([[0.5, -0.3], [0.8, 0.2]])
    print(f"\n输入 / Input X:")
    print(f"  {X}")

    # 前向传播
    print("\n--- 开始前向传播 (Starting Forward Pass) ---")
    cache = mlp.forward(X, verbose=True)

    return mlp, cache


def demo_mlp_xor():
    """用 MLP 解决 XOR 问题"""
    print("\n" + "=" * 72)
    print("第3.2节: MLP 解决 XOR 问题")
    print("Section 3.2: MLP Solves XOR Problem")
    print("=" * 72)

    X_xor = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
    y_xor = np.array([[0], [1], [1], [0]], dtype=float)  # 回归输出

    print(f"XOR 输入 / Input:\n{X_xor}")
    print(f"XOR 目标 / Target:\n{y_xor}")

    # 构建 MLP: 2→4→1, 使用 Sigmoid 输出 (0~1)
    mlp_xor = MLP(layer_sizes=[2, 4, 1], activation="sigmoid")
    cache = mlp_xor.forward(X_xor, verbose=True)

    # 输出预测
    y_pred = cache["a2"]  # 第2层激活 = 输出
    print(f"\nXOR MLP 预测结果 (未经训练 / Untrained):")
    print(f"{'x1':>4} {'x2':>4} | {'ŷ':>8} {'y_true':>8} {'正确?':>6}")
    print("-" * 34)
    for i in range(4):
        correct = "✓" if (y_pred[i, 0] >= 0.5) == (y_xor[i, 0] >= 0.5) else "✗"
        print(f"{X_xor[i, 0]:>4.0f} {X_xor[i, 1]:>4.0f} | "
              f"{y_pred[i, 0]:>8.5f} {y_xor[i, 0]:>8.0f} {correct:>6}")

    print("\n  ✓ MLP 结构上可以表示 XOR（只需训练权重）")
    print("  ✓ MLP can represent XOR in principle（just need to train weights）")

    return mlp_xor


# ============================================================
# 5. 万能近似定理演示 (Universal Approximation Theorem)
# ============================================================
def demo_universal_approximation():
    """
    用 MLP 拟合正弦波，演示万能近似定理
    Universal Approximation Theorem: 一个隐藏层 + 足够多神经元可逼近任意连续函数
    """
    print("\n" + "=" * 72)
    print("第4部分: 万能近似定理 (Universal Approximation Theorem)")
    print("Section 4: Universal Approximation Theorem")
    print("=" * 72)

    # 目标函数: y = sin(x)
    x_train = np.linspace(-np.pi, np.pi, 200).reshape(-1, 1)
    y_train = np.sin(x_train)

    print(f"目标函数 / Target function: y = sin(x),  x ∈ [-π, π]")
    print(f"训练样本数 / Training samples: {len(x_train)}")

    # 构建不同大小的 MLP, 比较拟合能力
    hidden_sizes = [1, 3, 10, 50]
    colors = ["red", "orange", "green", "blue"]

    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    axes = axes.flatten()

    results = {}

    for idx, n_hidden in enumerate(hidden_sizes):
        ax = axes[idx]

        # MLP: 1 → n_hidden → 1, 使用 Tanh 激活
        mlp_approx = MLP(layer_sizes=[1, n_hidden, 1], activation="tanh")

        # 使用随机初始化的权重进行前向传播 (不训练)
        cache = mlp_approx.forward(x_train, verbose=False)
        y_pred = cache["a2"].flatten()

        # 计算拟合误差
        mse = np.mean((y_pred - y_train.flatten()) ** 2)

        # 绘制
        ax.plot(x_train, y_train, "k--", linewidth=2, label="True: sin(x)", alpha=0.7)
        ax.plot(x_train, y_pred, linewidth=2, color=colors[idx],
                label=f"MLP ({n_hidden} hidden)")
        ax.set_title(f"隐藏层神经元数 = {n_hidden}  (MSE = {mse:.4f})")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.legend()
        ax.grid(alpha=0.3)

        results[n_hidden] = {"mse": mse, "pred": y_pred}
        print(f"  隐藏层 {n_hidden:3d} 个神经元 → MSE = {mse:.6f}")

    plt.suptitle("万能近似定理: 不同宽度隐藏层的拟合能力\n"
                 "(Universal Approximation Theorem: Fitting sin(x) with varying width)",
                 fontsize=14)
    plt.tight_layout()
    path = OUTPUT_DIR / "universal_approximation.png"
    fig.savefig(path)
    plt.close(fig)
    print(f"\n[图] 万能近似定理演示已保存: {path}")
    print("  注: 这里使用的是未经训练的随机权重, 所以大的网络不一定拟合更好。")
    print("  训练后的 MLP 才能展示真正的万能近似能力。")

    return results


# ============================================================
# 6. 激活函数对比总结表
# ============================================================
def demo_activation_summary():
    """打印激活函数对比总结"""
    print("\n" + "=" * 72)
    print("第5部分: 激活函数对比总结 (Summary Table)")
    print("=" * 72)

    print("""
┌──────────┬──────────────────────┬──────────────────────┬────────────────────────┐
│ 函数     │ 范围 (Range)         │ 梯度消失?            │ 适用场景               │
│ (Name)   │                      │ (Vanishing Grad?)    │ (Use Case)             │
├──────────┼──────────────────────┼──────────────────────┼────────────────────────┤
│ Sigmoid  │ (0, 1)               │ 是 (|z|>4 时≈0)      │ 二分类输出层           │
│ Tanh     │ (-1, 1)              │ 是 (|z|>4 时≈0)      │ RNN, 归一化特征        │
│ ReLU     │ [0, ∞)               │ 否 (z>0 时恒为1)     │ CNN, Transformer 默认  │
│ GELU     │ (-0.17·|z|, ∞)       │ 否 (z>2 时≈1)        │ BERT, GPT, ViT         │
│ SwiGLU   │ (-0.5·|z|, ∞)        │ 否                   │ PaLM, LLaMA            │
└──────────┴──────────────────────┴──────────────────────┴────────────────────────┘""")

    # 梯度消失的数值展示
    print("\n【梯度消失验证 / Vanishing Gradient Verification】")
    for z in [-5, -10, -20]:
        print(f"  z={z:>4d}: sigmoid'(z)={sigmoid_derivative(np.array([z]))[0]:.3e}, "
              f"tanh'(z)={tanh_derivative(np.array([z]))[0]:.3e}")

    # 计算各函数的输出范围
    z_range = np.linspace(-10, 10, 10001)
    print(f"\n【数值范围验证 / Range Verification】")
    for name, (func, _) in [("Sigmoid", (sigmoid, sigmoid_derivative)),
                              ("Tanh", (tanh, tanh_derivative)),
                              ("ReLU", (relu, relu_derivative)),
                              ("GELU", (gelu, gelu_derivative))]:
        vals = func(z_range)
        print(f"  {name:>8}: 范围 [{vals.min():.4f}, {vals.max():.4f}]")


# ============================================================
# 7. 主函数 (Main)
# ============================================================
if __name__ == "__main__":
    print("=" * 72)
    print("  感知机与多层感知机 (Perceptron & MLP) — 从零实现")
    print("  Perceptron & Multi-Layer Perceptron — From Scratch")
    print("=" * 72)

    # Part 1: 激活函数
    activations = demo_activation_functions()

    # Part 2: 感知机
    perceptron = demo_perceptron()

    # Part 2b: XOR 问题
    xor_acc = demo_xor_problem()

    # Part 3: MLP 前向传播
    mlp, mlp_cache = demo_mlp_forward()

    # Part 3b: MLP 解决 XOR
    mlp_xor = demo_mlp_xor()

    # Part 4: 万能近似定理
    approx_results = demo_universal_approximation()

    # Part 5: 总结表
    demo_activation_summary()

    print("\n" + "=" * 72)
    print("  所有演示完成! (All demonstrations complete!)")
    print("=" * 72)
