"""
梯度下降从零实现 —— 线性回归演示
(Gradient Descent from Scratch — Linear Regression Demo)
=========================================================
依赖：numpy>=1.24.0, matplotlib>=3.7.0

展示：
1. 从零实现梯度下降拟合 y = wx + b
2. 损失曲线（Loss Curve）
3. 参数轨迹等高图（Parameter Trajectory on Contour Plot）
4. 不同学习率对比（Learning Rate Comparison）

使用 MSE 损失: L = 1/(2n) * Σ (y - (wx + b))²
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")  # 无 GUI 后端，避免 Gtk 警告
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================
# 0. 全局设置
# ============================================================
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# 随机种子：确保结果可复现
RNG = np.random.RandomState(42)


# ============================================================
# 1. 生成合成数据（Synthetic Data）
# ============================================================
def generate_data(n_samples: int = 100, w_true: float = 2.5, b_true: float = 1.0,
                  noise_std: float = 0.5) -> tuple:
    """生成线性数据 y = w_true * x + b_true + 噪声"""
    x = RNG.rand(n_samples) * 10 - 5  # [-5, 5]
    y = w_true * x + b_true + RNG.randn(n_samples) * noise_std
    return x, y


# ============================================================
# 2. 模型与损失函数
# ============================================================
def predict(x: np.ndarray, w: float, b: float) -> np.ndarray:
    """线性预测: y_pred = w * x + b"""
    return w * x + b


def mse_loss(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """均方误差 MSE = 1/(2n) * Σ (y - y_pred)²

    除以 2 是为了求导时消去系数，使梯度表达式更简洁。
    """
    return np.mean((y_true - y_pred) ** 2) / 2


# ============================================================
# 3. 梯度计算（链式法则的产物）
# ============================================================
def compute_gradients(x: np.ndarray, y_true: np.ndarray, w: float, b: float) -> tuple:
    """计算 dL/dw 和 dL/db

    链式法则推导:
      L = 1/(2n) * Σ (y - (wx + b))²
      ∂L/∂w = 1/n * Σ (y_pred - y) * x  = (1/n) * Σ (残差 * x)
      ∂L/∂b = 1/n * Σ (y_pred - y)       = (1/n) * Σ 残差
    """
    y_pred = predict(x, w, b)
    residual = y_pred - y_true  # 残差: y_pred - y

    dw = np.mean(residual * x)  # ∂L/∂w
    db = np.mean(residual)      # ∂L/∂b
    return dw, db


# ============================================================
# 4. 梯度下降核心算法
# ============================================================
def gradient_descent(x: np.ndarray, y: np.ndarray, w_init: float, b_init: float,
                     lr: float, n_iter: int) -> dict:
    """从零实现批量梯度下降（Batch Gradient Descent）

    参数:
        x, y: 数据
        w_init, b_init: 参数初始值
        lr: 学习率（learning rate）
        n_iter: 迭代次数

    返回:
        dict 包含历史记录: w, b, loss
    """
    w, b = w_init, b_init
    history = {"w": [w], "b": [b], "loss": [mse_loss(y, predict(x, w, b))]}

    for i in range(n_iter):
        # 1. 计算梯度
        dw, db = compute_gradients(x, y, w, b)

        # 2. 沿负梯度方向更新参数
        w -= lr * dw
        b -= lr * db

        # 3. 记录历史
        history["w"].append(w)
        history["b"].append(b)
        history["loss"].append(mse_loss(y, predict(x, w, b)))

    return history


# ============================================================
# 5. 可视化函数
# ============================================================
def plot_loss_curve(history: dict, lr: float, ax: plt.Axes):
    """绘制损失曲线"""
    ax.plot(history["loss"], lw=2)
    ax.set_xlabel("Iteration / 迭代次数")
    ax.set_ylabel("MSE Loss / 损失")
    ax.set_title(f"Loss Curve (lr={lr}) / 损失曲线")
    ax.grid(True, alpha=0.3)


def plot_parameter_trajectory(history: dict, w_true: float, b_true: float,
                              w_range: tuple, b_range: tuple, ax: plt.Axes,
                              x_data: np.ndarray = None, y_data: np.ndarray = None):
    """在等高线上绘制参数更新轨迹"""
    if x_data is None or y_data is None:
        x_data = np.linspace(-5, 5, 100)
        y_data = 2.5 * x_data + 1.0

    # 创建网格用于绘制等高线（使用向量化计算，避免嵌套循环）
    n_grid = 80  # 低分辨率以加快计算
    ws = np.linspace(w_range[0], w_range[1], n_grid)
    bs = np.linspace(b_range[0], b_range[1], n_grid)

    # 向量化计算: 所有 (w, b) 组合的损失
    # x_data: (n,),  ws: (n_w,),  bs: (n_b,)
    # y_pred: (n, n_w, n_b) 通过广播
    y_pred = x_data[:, np.newaxis, np.newaxis] * ws[np.newaxis, :, np.newaxis] + bs[np.newaxis, np.newaxis, :]
    residual = y_data[:, np.newaxis, np.newaxis] - y_pred
    Z = np.mean(residual ** 2, axis=0) / 2  # (n_w, n_b)

    W, B = np.meshgrid(ws, bs)
    Z = Z.T  # 转置以匹配 meshgrid 的 (n_b, n_w) 形状

    # 绘制等高线
    levels = np.logspace(-1, 2, 20)
    ax.contour(W, B, Z, levels=levels, cmap="viridis", alpha=0.7, linewidths=0.8)

    # 绘制参数轨迹
    ax.plot(history["w"], history["b"], "r.-", markersize=4, linewidth=1.5,
            label="GD path / 梯度下降路径")
    ax.plot(history["w"][0], history["b"][0], "go", markersize=8,
            label="Start / 起点")
    ax.plot(history["w"][-1], history["b"][-1], "r*", markersize=12,
            label="End / 终点")
    ax.plot(w_true, b_true, "y*", markersize=12, label="Truth / 真实值")

    ax.set_xlabel("w (weight / 权重)")
    ax.set_ylabel("b (bias / 偏置)")
    ax.set_title("Parameter Trajectory / 参数轨迹")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)


def plot_lr_comparison(x: np.ndarray, y: np.ndarray, lrs: list[float],
                       w_true: float, b_true: float):
    """对比不同学习率的收敛行为"""
    n_lrs = len(lrs)
    fig, axes = plt.subplots(2, n_lrs, figsize=(5 * n_lrs, 8))

    if n_lrs == 1:
        axes = axes.reshape(2, 1)

    colors = plt.cm.viridis(np.linspace(0.2, 0.9, n_lrs))

    for idx, lr in enumerate(lrs):
        w_init = -3.0
        b_init = -4.0

        history = gradient_descent(x, y, w_init, b_init, lr=lr, n_iter=50)

        # 损失曲线
        ax_loss = axes[0, idx]
        ax_loss.plot(history["loss"], color=colors[idx], lw=2)
        ax_loss.set_xlabel("Iteration / 迭代次数")
        ax_loss.set_ylabel("Loss / 损失")
        ax_loss.set_title(f"Loss Curve (lr={lr})")

        # 在损失曲线上标注最终损失
        final_loss = history["loss"][-1]
        ax_loss.axhline(y=final_loss, color="gray", linestyle="--", alpha=0.5)
        ax_loss.text(len(history["loss"]) * 0.7, final_loss * 1.1,
                     f"Final: {final_loss:.4f}", fontsize=9)
        ax_loss.grid(True, alpha=0.3)

    # 参数轨迹
    ax_traj = axes[1, idx]
    plot_parameter_trajectory(
        history, w_true, b_true,
        w_range=(-4, 4), b_range=(-5, 5),
        ax=ax_traj, x_data=x, y_data=y
    )

    plt.suptitle("Learning Rate Comparison / 学习率对比", fontsize=14, y=1.01)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "lr_comparison.png", dpi=150, bbox_inches="tight")
    print(f"[Saved] lr_comparison.png -> {OUTPUT_DIR / 'lr_comparison.png'}")
    plt.close()


# ============================================================
# 6. 主流程
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("梯度下降从零实现 —— 线性回归演示")
    print("Gradient Descent from Scratch — Linear Regression Demo")
    print("=" * 60)

    # --- 6.1 生成数据 ---
    print("\n[1/4] 生成合成数据...")
    w_true, b_true = 2.5, 1.0
    x, y = generate_data(n_samples=100, w_true=w_true, b_true=b_true,
                         noise_std=0.5)
    print(f"    真实参数: w = {w_true}, b = {b_true}")
    print(f"    样本数: {len(x)}")

    # --- 6.2 单次梯度下降演示 ---
    print("\n[2/4] 运行梯度下降（lr=0.1, 50 次迭代）...")
    history = gradient_descent(x, y, w_init=-3.0, b_init=-4.0,
                               lr=0.1, n_iter=50)

    final_w, final_b = history["w"][-1], history["b"][-1]
    print(f"    初始参数: w = -3.0, b = -4.0")
    print(f"    最终参数: w = {final_w:.4f}, b = {final_b:.4f}")
    print(f"    真实参数: w = {w_true}, b = {b_true}")
    print(f"    初始损失: {history['loss'][0]:.4f}")
    print(f"    最终损失: {history['loss'][-1]:.4f}")

    # --- 6.3 可视化单次运行 ---
    print("\n[3/4] 生成可视化...")
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # 损失曲线
    plot_loss_curve(history, lr=0.1, ax=axes[0])

    # 参数轨迹
    plot_parameter_trajectory(history, w_true, b_true,
                              w_range=(-4, 4), b_range=(-5, 5),
                              ax=axes[1], x_data=x, y_data=y)

    plt.suptitle(
        f"Gradient Descent: y = {w_true:.1f}x + {b_true:.1f}  "
        f"| Final: w={final_w:.2f}, b={final_b:.2f}",
        fontsize=13
    )
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "gradient_descent_demo.png", dpi=150,
                bbox_inches="tight")
    print(f"    [Saved] gradient_descent_demo.png -> "
          f"{OUTPUT_DIR / 'gradient_descent_demo.png'}")
    plt.close()

    # --- 6.4 学习率对比 ---
    print("\n[4/4] 对比不同学习率...")
    lrs_to_test = [0.01, 0.1, 0.5]
    print(f"    学习率: {lrs_to_test}")
    plot_lr_comparison(x, y, lrs_to_test, w_true, b_true)

    # --- 验证收敛 ---
    print("\n" + "=" * 60)
    print("验证: 不同学习率的最终损失对比")
    print("-" * 60)
    for lr in [0.001, 0.01, 0.05, 0.1, 0.5, 1.0]:
        hist = gradient_descent(x, y, w_init=-3.0, b_init=-4.0,
                                lr=lr, n_iter=50)
        final_loss = hist["loss"][-1]
        marker = " ✓" if final_loss < 0.5 else " ✗"
        print(f"    lr={lr:.3f}:  final_loss={final_loss:.6f}{marker}")
    print("=" * 60)
    print("\n所有图片已保存到:", OUTPUT_DIR)
    print("All figures saved to:", OUTPUT_DIR)
