"""
visualization_demo.py — Matplotlib 数据可视化演示（ML 场景）
Data Visualization Demo for Machine Learning with Matplotlib

生成以下图表（Generates the following plots）：
  1. line_curve.png       — 训练损失曲线（Loss Curve）
  2. scatter.png          — 二维特征空间散点图（2D Feature Scatter）
  3. bar_chart.png        — 模型精度对比条形图（Model Comparison）
  4. histogram.png        — 特征值分布直方图（Feature Histogram）
  5. confusion_matrix.png — 混淆矩阵热力图（Confusion Matrix Heatmap）
  6. correlation.png      — 相关系数矩阵热力图（Correlation Heatmap）
  7. roc_curve.png        — ROC 曲线（ROC Curve + AUC）
  8. normalization.png    — 归一化前后对比（Before/After Normalization）

依赖：matplotlib >= 3.7.0, numpy
运行：python visualization_demo.py
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")  # 非交互后端，无 GUI 依赖
import matplotlib.pyplot as plt
from pathlib import Path

# ── 输出目录 ──────────────────────────────────────────────
OUT_DIR = Path(__file__).resolve().parent
print(f"📂 输出目录: {OUT_DIR}")

# 全局字体设置（支持中英文混排）
plt.rcParams.update({
    "font.size": 12,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "figure.dpi": 120,
    "savefig.dpi": 150,
})


# ═══════════════════════════════════════════════════════════
# 1. 训练损失曲线（Line Plot — Loss Curve）
# ═══════════════════════════════════════════════════════════
def plot_loss_curve():
    """绘制训练损失曲线"""
    epochs = np.arange(1, 51)
    train_loss = 2.0 / (1 + 0.08 * epochs) + 0.05 * np.random.randn(50)
    val_loss = 2.0 / (1 + 0.06 * epochs) + 0.08 * np.random.randn(50)
    train_loss = np.clip(train_loss, 0, None)
    val_loss = np.clip(val_loss, 0, None)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(epochs, train_loss, "b-", linewidth=2, label="Train Loss")
    ax.plot(epochs, val_loss, "r--", linewidth=2, label="Validation Loss")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Loss")
    ax.set_title("Training & Validation Loss Curve\n训练与验证损失曲线")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "line_curve.png")
    plt.close(fig)
    print("  ✅ line_curve.png")


# ═══════════════════════════════════════════════════════════
# 2. 二维特征散点图（Scatter Plot — 2D Feature Space）
# ═══════════════════════════════════════════════════════════
def plot_scatter():
    """绘制二分类二维特征分布"""

    def _gen_data(center, n, label):
        x = center[0] + 0.6 * np.random.randn(n)
        y = center[1] + 0.6 * np.random.randn(n)
        return x, y, np.full(n, label)

    np.random.seed(42)
    x0, y0, c0 = _gen_data((2, 2), 80, 0)
    x1, y1, c1 = _gen_data((5, 5), 80, 1)

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.scatter(x0, y0, c="steelblue", label="Class 0", alpha=0.7, edgecolors="k", linewidths=0.5)
    ax.scatter(x1, y1, c="coral", label="Class 1", alpha=0.7, edgecolors="k", linewidths=0.5)
    ax.set_xlabel("Feature 1 特征1")
    ax.set_ylabel("Feature 2 特征2")
    ax.set_title("2D Feature Space (Binary Classification)\n二维特征空间（二分类）")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "scatter.png")
    plt.close(fig)
    print("  ✅ scatter.png")


# ═══════════════════════════════════════════════════════════
# 3. 模型对比条形图（Bar Chart — Model Comparison）
# ═══════════════════════════════════════════════════════════
def plot_bar_chart():
    """绘制模型精度对比条形图"""
    models = ["Logistic\nRegression", "Decision\nTree", "Random\nForest", "SVM", "MLP\n(2-layer)"]
    accuracies = [85.2, 78.6, 92.3, 88.1, 91.0]
    colors = ["#4C72B0", "#55A868", "#C44E52", "#8172B2", "#CCB974"]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(models, accuracies, color=colors, edgecolor="white", linewidth=1.2, width=0.6)
    for bar, acc in zip(bars, accuracies):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                f"{acc}%", ha="center", va="bottom", fontsize=11, fontweight="bold")
    ax.set_ylabel("Accuracy (%)  精度")
    ax.set_title("Model Comparison on Test Set\n测试集模型精度对比")
    ax.set_ylim(0, 100)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "bar_chart.png")
    plt.close(fig)
    print("  ✅ bar_chart.png")


# ═══════════════════════════════════════════════════════════
# 4. 特征值分布直方图（Histogram — Feature Distribution）
# ═══════════════════════════════════════════════════════════
def plot_histogram():
    """绘制特征值分布直方图"""
    np.random.seed(2024)
    age = np.concatenate([
        np.random.normal(25, 5, 200),
        np.random.normal(45, 6, 200),
        np.random.normal(65, 5, 100),
    ])

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(age, bins=30, color="steelblue", edgecolor="white", alpha=0.8, density=True)
    ax.set_xlabel("Age 年龄")
    ax.set_ylabel("Density 密度")
    ax.set_title("Feature Distribution (Age)\n特征值分布（年龄）")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "histogram.png")
    plt.close(fig)
    print("  ✅ histogram.png")


# ═══════════════════════════════════════════════════════════
# 5. 混淆矩阵热力图（Heatmap — Confusion Matrix）
# ═══════════════════════════════════════════════════════════
def plot_confusion_matrix():
    """绘制混淆矩阵热力图"""
    cm = np.array([[85, 10], [8, 97]])
    classes = ["Negative", "Positive"]

    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(cm, cmap="Blues", aspect="auto", vmin=0)

    # 在每个格子中标注数值
    for i in range(2):
        for j in range(2):
            color = "white" if cm[i, j] > cm.max() / 2 else "black"
            ax.text(j, i, str(cm[i, j]), ha="center", va="center", fontsize=16, color=color, fontweight="bold")

    ax.set_xticks(range(2))
    ax.set_yticks(range(2))
    ax.set_xticklabels(classes)
    ax.set_yticklabels(classes)
    ax.set_xlabel("Predicted Label 预测标签")
    ax.set_ylabel("True Label 真实标签")
    ax.set_title("Confusion Matrix\n混淆矩阵")
    fig.colorbar(im, ax=ax, fraction=0.046)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "confusion_matrix.png")
    plt.close(fig)
    print("  ✅ confusion_matrix.png")


# ═══════════════════════════════════════════════════════════
# 6. 相关系数矩阵热力图（Heatmap — Correlation Matrix）
# ═══════════════════════════════════════════════════════════
def plot_correlation():
    """绘制相关系数矩阵热力图"""
    np.random.seed(123)
    n, k = 200, 5
    data = np.random.randn(n, k)
    # 人为引入一些相关关系
    data[:, 1] = 0.7 * data[:, 0] + 0.3 * np.random.randn(n)
    data[:, 3] = -0.6 * data[:, 2] + 0.4 * np.random.randn(n)
    cov = np.corrcoef(data.T)

    labels = ["Feature A", "Feature B", "Feature C", "Feature D", "Feature E"]

    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(cov, cmap="RdBu_r", aspect="auto", vmin=-1, vmax=1)

    # 标注数值
    for i in range(k):
        for j in range(k):
            color = "white" if abs(cov[i, j]) > 0.5 else "black"
            ax.text(j, i, f"{cov[i, j]:.2f}", ha="center", va="center", fontsize=10, color=color)

    ax.set_xticks(range(k))
    ax.set_yticks(range(k))
    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)
    ax.set_title("Feature Correlation Matrix\n特征相关系数矩阵")
    fig.colorbar(im, ax=ax, fraction=0.046, label="Pearson r")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "correlation.png")
    plt.close(fig)
    print("  ✅ correlation.png")


# ═══════════════════════════════════════════════════════════
# 7. ROC 曲线（ROC Curve + AUC）
# ═══════════════════════════════════════════════════════════
def plot_roc_curve():
    """绘制 ROC 曲线并标注 AUC"""
    np.random.seed(7)
    n = 200
    y_true = np.array([0] * 100 + [1] * 100)
    # 模拟两种模型的预测概率（更好的模型有更高的区分度）
    y_score_better = np.concatenate([np.random.beta(2, 5, 100), np.random.beta(5, 2, 100)])
    y_score_worse = np.concatenate([np.random.beta(3, 4, 100), np.random.beta(4, 3, 100)])

    def _roc(y_true, y_score, n_thresh=100):
        thresholds = np.linspace(1, 0, n_thresh)
        tpr, fpr = [], []
        for t in thresholds:
            pred = (y_score >= t).astype(int)
            tp = ((pred == 1) & (y_true == 1)).sum()
            fn = ((pred == 0) & (y_true == 1)).sum()
            fp = ((pred == 1) & (y_true == 0)).sum()
            tn = ((pred == 0) & (y_true == 0)).sum()
            tpr.append(tp / (tp + fn + 1e-10))
            fpr.append(fp / (fp + tn + 1e-10))
        return np.array(fpr), np.array(tpr)

    def _auc(fpr, tpr):
        # trapezoidal integration (compatible with numpy >= 2.0)
        return -np.sum((fpr[1:] - fpr[:-1]) * (tpr[1:] + tpr[:-1]) / 2)

    fpr1, tpr1 = _roc(y_true, y_score_better)
    fpr2, tpr2 = _roc(y_true, y_score_worse)
    auc1, auc2 = _auc(fpr1, tpr1), _auc(fpr2, tpr2)

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.plot(fpr1, tpr1, "b-", linewidth=2, label=f"Model A (AUC = {auc1:.3f})")
    ax.plot(fpr2, tpr2, "r--", linewidth=2, label=f"Model B (AUC = {auc2:.3f})")
    ax.plot([0, 1], [0, 1], "k:", alpha=0.5, label="Random (AUC = 0.5)")
    ax.set_xlabel("False Positive Rate (FPR)  假正率")
    ax.set_ylabel("True Positive Rate (TPR)  真正率")
    ax.set_title("ROC Curve Comparison\nROC 曲线对比")
    ax.legend(loc="lower right")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "roc_curve.png")
    plt.close(fig)
    print("  ✅ roc_curve.png")


# ═══════════════════════════════════════════════════════════
# 8. 归一化前后对比（Bar Chart — Before / After Normalization）
# ═══════════════════════════════════════════════════════════
def plot_normalization():
    """绘制归一化前后特征分布对比"""
    np.random.seed(42)
    raw = np.random.exponential(scale=2, size=(500, 2))
    raw[:, 0] += 10  # feature 1 均值 > feature 2
    raw[:, 1] *= 3

    # Min-Max 归一化
    normed = (raw - raw.min(axis=0)) / (raw.max(axis=0) - raw.min(axis=0))

    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=False)

    # 归一化前
    axes[0].hist(raw[:, 0], bins=25, alpha=0.7, label="Feature 1", color="steelblue", edgecolor="white")
    axes[0].hist(raw[:, 1], bins=25, alpha=0.7, label="Feature 2", color="coral", edgecolor="white")
    axes[0].set_title("Before Normalization\n归一化前")
    axes[0].set_xlabel("Value 数值")
    axes[0].set_ylabel("Frequency 频次")
    axes[0].legend()
    axes[0].grid(axis="y", alpha=0.3)

    # 归一化后
    axes[1].hist(normed[:, 0], bins=25, alpha=0.7, label="Feature 1", color="steelblue", edgecolor="white")
    axes[1].hist(normed[:, 1], bins=25, alpha=0.7, label="Feature 2", color="coral", edgecolor="white")
    axes[1].set_title("After Min-Max Normalization\n归一化后")
    axes[1].set_xlabel("Value 数值")
    axes[1].set_ylabel("Frequency 频次")
    axes[1].legend()
    axes[1].grid(axis="y", alpha=0.3)

    fig.suptitle("Feature Distribution — Before vs After Normalization\n特征分布 — 归一化前后对比",
                 fontsize=14, fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "normalization.png")
    plt.close(fig)
    print("  ✅ normalization.png")


# ═══════════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("🚀 开始生成可视化图表...\n")
    plot_loss_curve()
    plot_scatter()
    plot_bar_chart()
    plot_histogram()
    plot_confusion_matrix()
    plot_correlation()
    plot_roc_curve()
    plot_normalization()
    print("\n🎉 所有图表生成完毕！")
    print(f"📁 输出目录: {OUT_DIR}")
    for f in sorted(OUT_DIR.glob("*.png")):
        print(f"   📊 {f.name}")
