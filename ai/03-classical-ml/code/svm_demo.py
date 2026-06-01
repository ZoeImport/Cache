"""
SVM 核函数对比实验 — 非线性分类演示
(SVM Kernel Comparison — Non-linear Classification Demo)
==========================================================
依赖：scikit-learn>=1.3.0, numpy>=1.24.0, matplotlib>=3.7.0

展示内容：
1. 线性核 vs RBF 核在高斯形数据集上的对比
2. RBF 核参数 γ（gamma）对决策边界的影响（小→欠拟合，大→过拟合）
3. 支持向量（Support Vectors）在决策边界中的角色可视化
4. 不同 γ 值对应的分类准确率与支持向量数量

数据集：make_moons（半月形，经典非线性数据集）
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")  # 无 GUI 后端
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.svm import SVC
from sklearn.datasets import make_moons
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# ============================================================
# 0. 全局设置
# ============================================================
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

RNG = np.random.RandomState(42)


# ============================================================
# 1. 生成 & 预处理数据
# ============================================================
def generate_dataset(n_samples: int = 300, noise: float = 0.15) -> tuple:
    """生成半月形非线性二分类数据集"""
    X, y = make_moons(n_samples=n_samples, noise=noise, random_state=RNG)
    return X, y


def preprocess(X, y, test_size: float = 0.3):
    """标准化特征并划分训练/测试集"""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y,
    )
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    return X_train, X_test, y_train, y_test, scaler


# ============================================================
# 2. 训练 SVM 模型
# ============================================================
def train_svm(X_train, y_train, kernel: str = "rbf", gamma: str | float = "scale",
              C: float = 1.0):
    """训练 SVM 分类器并返回模型"""
    model = SVC(kernel=kernel, gamma=gamma, C=C, random_state=42)
    model.fit(X_train, y_train)
    return model


# ============================================================
# 3. 可视化工具函数
# ============================================================
def plot_decision_boundary(ax, model, X, y, title: str, show_sv: bool = True):
    """
    在给定 ax 上绘制 SVM 决策边界。
    - 背景色表示决策区域
    - 等高线表示决策函数值（到超平面的带符号距离）
    - 圈出支持向量
    """
    # 构建网格
    x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
    y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 300),
                         np.linspace(y_min, y_max, 300))

    # 预测网格点的类别和决策函数值
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    D = model.decision_function(np.c_[xx.ravel(), yy.ravel()])
    D = D.reshape(xx.shape)

    # 绘制填充的决策区域
    ax.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.coolwarm, levels=[-0.5, 0.5, 1.5])
    # 绘制决策边界 (decision_function = 0) 和间隔边界 (±1)
    ax.contour(xx, yy, D, levels=[-1, 0, 1], linestyles=["--", "-", "--"],
               colors=["grey", "k", "grey"], linewidths=[1, 2, 1])

    # 绘制数据点
    ax.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.coolwarm, edgecolors="k",
               s=30, alpha=0.8)

    # 圈出支持向量
    if show_sv and hasattr(model, "support_vectors_"):
        sv = model.support_vectors_
        ax.scatter(sv[:, 0], sv[:, 1], s=150, linewidth=1.5,
                   facecolors="none", edgecolors="gold", alpha=0.9,
                   label="Support Vectors")

    ax.set_title(title, fontsize=12)
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.legend(loc="upper right", fontsize=8)


# ============================================================
# 4. 主实验
# ============================================================
def main():
    print("=" * 60)
    print("SVM 核函数对比实验 (SVM Kernel Comparison Demo)")
    print("=" * 60)

    # 4.1 生成数据
    print("\n[1/3] 生成半月形数据集...")
    X, y = generate_dataset(n_samples=300, noise=0.15)
    X_train, X_test, y_train, y_test, scaler = preprocess(X, y)

    # ============================================================
    # 实验 A: Linear vs RBF Kernel
    # ============================================================
    print("\n[2/3] 实验 A: 线性核 vs RBF 核...")
    models_a = {
        "Linear Kernel": train_svm(X_train, y_train, kernel="linear"),
        "RBF Kernel (gamma=1.0)": train_svm(X_train, y_train, kernel="rbf", gamma=1.0),
    }

    fig_a, axes_a = plt.subplots(1, 2, figsize=(12, 5))
    for ax, (name, model) in zip(axes_a, models_a.items()):
        train_acc = accuracy_score(y_train, model.predict(X_train))
        test_acc = accuracy_score(y_test, model.predict(X_test))
        n_sv = len(model.support_vectors_) if hasattr(model, "support_vectors_") else 0
        title = f"{name}\nTrain Acc: {train_acc:.3f} | Test Acc: {test_acc:.3f}\n#SV: {n_sv}"
        plot_decision_boundary(ax, model, X_test, y_test, title)

    plt.tight_layout()
    path_a = OUTPUT_DIR / "svm_linear_vs_rbf.png"
    fig_a.savefig(path_a, dpi=150, bbox_inches="tight")
    print(f"  → 已保存: {path_a}")
    plt.close(fig_a)

    # ============================================================
    # 实验 B: 不同 γ 值对比 (RBF Kernel)
    # ============================================================
    print("\n[3/3] 实验 B: RBF 核 γ 参数对比...")

    gamma_values = [0.01, 0.1, 1.0, 5.0, 20.0, 100.0]
    fig_b, axes_b = plt.subplots(2, 3, figsize=(16, 10))
    axes_b = axes_b.flatten()

    results = []
    for ax, gamma in zip(axes_b, gamma_values):
        model = train_svm(X_train, y_train, kernel="rbf", gamma=gamma, C=1.0)
        train_acc = accuracy_score(y_train, model.predict(X_train))
        test_acc = accuracy_score(y_test, model.predict(X_test))
        n_sv = len(model.support_vectors_)

        results.append((gamma, train_acc, test_acc, n_sv))
        title = f"γ = {gamma}\nTrain: {train_acc:.3f} | Test: {test_acc:.3f}\n#SV: {n_sv}"
        plot_decision_boundary(ax, model, X_test, y_test, title)

    plt.tight_layout()
    path_b = OUTPUT_DIR / "svm_rbf_gamma_comparison.png"
    fig_b.savefig(path_b, dpi=150, bbox_inches="tight")
    print(f"  → 已保存: {path_b}")
    plt.close(fig_b)

    # ============================================================
    # 实验 C: 性能指标随 γ 变化
    # ============================================================
    print("\n  → 生成性能指标随 γ 变化图...")

    fig_c, axes_c = plt.subplots(1, 3, figsize=(14, 4))

    gammas = [r[0] for r in results]
    train_accs = [r[1] for r in results]
    test_accs = [r[2] for r in results]
    sv_counts = [r[3] for r in results]

    # 子图 1: 准确率
    ax1 = axes_c[0]
    ax1.semilogx(gammas, train_accs, "o-", label="Train Accuracy", color="navy")
    ax1.semilogx(gammas, test_accs, "s--", label="Test Accuracy", color="crimson")
    ax1.set_xlabel("γ (gamma)")
    ax1.set_ylabel("Accuracy")
    ax1.set_title("Accuracy vs γ")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 子图 2: 支持向量数量
    ax2 = axes_c[1]
    ax2.semilogx(gammas, sv_counts, "D-", color="darkorange")
    ax2.set_xlabel("γ (gamma)")
    ax2.set_ylabel("# Support Vectors")
    ax2.set_title("Support Vectors vs γ")
    ax2.grid(True, alpha=0.3)

    # 子图 3: 过拟合程度 (Train - Test gap)
    ax3 = axes_c[2]
    gap = [t - s for t, s in zip(train_accs, test_accs)]
    ax3.semilogx(gammas, gap, "^-", color="purple")
    ax3.axhline(y=0, color="grey", linestyle="--", alpha=0.5)
    ax3.set_xlabel("γ (gamma)")
    ax3.set_ylabel("Train - Test Gap")
    ax3.set_title("Overfitting Indicator (Gap)")
    ax3.grid(True, alpha=0.3)

    plt.tight_layout()
    path_c = OUTPUT_DIR / "svm_gamma_metrics.png"
    fig_c.savefig(path_c, dpi=150, bbox_inches="tight")
    print(f"  → 已保存: {path_c}")
    plt.close(fig_c)

    # ============================================================
    # 汇总打印
    # ============================================================
    print("\n" + "=" * 60)
    print("实验结果汇总 (Experiment Summary)")
    print("=" * 60)
    print(f"{'γ':>8} | {'Train Acc':>10} | {'Test Acc':>10} | {'#SV':>6} | {'Gap':>8}")
    print("-" * 52)
    for gamma, tr, te, n in results:
        gap_str = f"{tr - te:+.4f}"
        print(f"{gamma:>8} | {tr:>10.4f} | {te:>10.4f} | {n:>6} | {gap_str:>8}")

    print("\n结论 (Conclusions):")
    print("  • γ 太小 (如 0.01) → 核函数太平滑 → 欠拟合 (决策边界接近线性)")
    print("  • γ 适中 (如 1.0)  → 较好地拟合非线性结构 → 泛化性能最佳")
    print("  • γ 太大 (如 100)  → 核函数仅捕捉局部信息 → 过拟合 (决策边界过度曲折)")
    print("  • 支持向量数量随 γ 增大先减后增：γ 过大时每个样本都可能成为支持向量")
    print("=" * 60)


if __name__ == "__main__":
    main()
