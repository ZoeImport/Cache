"""
model_evaluation.py — 模型评估与验证演示
Model Evaluation & Validation Demo
=====================================
依赖: numpy>=1.24.0, matplotlib>=3.7.0, scikit-learn>=1.3.0

演示内容（Demonstrates）:
  1. 过拟合 vs 欠拟合——多项式回归（Polynomial Regression）
  2. 学习曲线——训练/验证误差 vs 训练集大小（Learning Curves）
  3. K 折交叉验证（K-Fold Cross-Validation）
  4. ROC 曲线与 AUC 计算（ROC Curve & AUC）
  5. 训练/验证/测试集划分（Train/Val/Test Split）

每个子图都会保存为独立的 PNG 文件到 output/ 目录。
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")  # 非交互后端，无 GUI 依赖
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.model_selection import train_test_split, KFold, learning_curve, cross_val_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.datasets import make_classification
from sklearn.metrics import (roc_curve, auc, accuracy_score, precision_score,
                             recall_score, f1_score, roc_auc_score, confusion_matrix)
import warnings
warnings.filterwarnings("ignore")

# ════════════════════════════════════════════════════════════
# 0. 全局设置
# ════════════════════════════════════════════════════════════
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)
RNG = np.random.RandomState(42)

plt.rcParams.update({
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "figure.dpi": 120,
    "savefig.dpi": 150,
})


# ════════════════════════════════════════════════════════════
# 1. 合成数据生成
# ════════════════════════════════════════════════════════════
def generate_sine_data(n_samples: int = 80, noise_std: float = 0.15) -> tuple:
    """生成正弦波数据 y = sin(2πx) + 噪声，用于多项式过拟合演示"""
    x = RNG.rand(n_samples) * 2 - 1  # [-1, 1]
    y = np.sin(2 * np.pi * x) + RNG.randn(n_samples) * noise_std
    return x, y


# ════════════════════════════════════════════════════════════
# 2. 过拟合 vs 欠拟合演示（多项式回归）
# ════════════════════════════════════════════════════════════
def demo_overfitting_underfitting():
    """
    用 1 阶（欠拟合）、3 阶（适中）、15 阶（过拟合）多项式拟合同一条正弦曲线。
    生成三张子图对比，直观展示高偏差 vs 高方差。
    """
    print("[1/5] 过拟合 vs 欠拟合 — 多项式回归对比...")

    x, y = generate_sine_data(n_samples=40, noise_std=0.12)
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.4, random_state=42
    )

    # 排序用于绘制平滑预测曲线
    x_sorted = np.linspace(-1, 1, 200)

    degrees = [1, 3, 15]
    colors = ["#E74C3C", "#2ECC71", "#3498DB"]
    labels = [
        "Degree 1 (Underfitting — High Bias)",
        "Degree 3 (Good Fit — Balanced)",
        "Degree 15 (Overfitting — High Variance)",
    ]

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), sharey=True)

    for idx, (deg, color, label) in enumerate(zip(degrees, colors, labels)):
        ax = axes[idx]

        # 构造多项式特征 + 线性回归的 Pipeline
        model = Pipeline([
            ("poly", PolynomialFeatures(degree=deg, include_bias=False)),
            ("linear", LinearRegression()),
        ])
        model.fit(x_train.reshape(-1, 1), y_train)

        # 预测
        y_pred = model.predict(x_sorted.reshape(-1, 1))
        train_pred = model.predict(x_train.reshape(-1, 1))
        test_pred = model.predict(x_test.reshape(-1, 1))

        # 计算误差
        train_mse = np.mean((y_train - train_pred) ** 2)
        test_mse = np.mean((y_test - test_pred) ** 2)

        # 绘图
        ax.scatter(x_train, y_train, color="#2C3E50", s=28, alpha=0.8,
                   label="Train", zorder=5)
        ax.scatter(x_test, y_test, color="#E67E22", s=28, alpha=0.6,
                   marker="^", label="Test", zorder=5)
        ax.plot(x_sorted, y_pred, color=color, linewidth=2.5, label=f"Degree {deg}")
        ax.plot(x_sorted, np.sin(2 * np.pi * x_sorted), "k--", linewidth=1.2,
                alpha=0.5, label="True $\\sin(2\\pi x)$")

        ax.set_title(label, fontsize=10.5)
        ax.set_xlabel("x")
        if idx == 0:
            ax.set_ylabel("y")
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1.8, 1.8)
        ax.legend(fontsize=7.5, loc="lower left")
        ax.text(0.95, 0.95, f"Train MSE: {train_mse:.4f}\nTest MSE: {test_mse:.4f}",
                transform=ax.transAxes, va="top", ha="right",
                fontsize=8, bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.6))

    fig.suptitle("Overfitting vs Underfitting — Polynomial Regression on $\\sin(2\\pi x)$",
                 fontsize=14, y=1.03)
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "overfitting_underfitting.png", bbox_inches="tight")
    plt.close(fig)
    print(f"    → 已保存 {OUTPUT_DIR / 'overfitting_underfitting.png'}")


# ════════════════════════════════════════════════════════════
# 3. 学习曲线演示
# ════════════════════════════════════════════════════════════
def demo_learning_curves():
    """
    为欠拟合（deg=1）、过拟合（deg=15）、良好（deg=3）三种模型绘制学习曲线。
    展示训练/验证误差随训练集大小的变化，以及过拟合时的"鸿沟"现象。
    """
    print("[2/5] 学习曲线 — 诊断过拟合与欠拟合...")

    x, y = generate_sine_data(n_samples=200, noise_std=0.15)
    x = x.reshape(-1, 1)

    degrees = [1, 3, 15]
    colors = ["#E74C3C", "#2ECC71", "#3498DB"]
    titles = ["Underfitting (deg=1) — High Bias",
              "Good Fit (deg=3) — Balanced",
              "Overfitting (deg=15) — High Variance"]

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), sharey=True)

    train_sizes = np.linspace(0.1, 0.9, 20)  # 训练集比例

    for idx, (deg, color, title) in enumerate(zip(degrees, colors, titles)):
        ax = axes[idx]

        model = Pipeline([
            ("poly", PolynomialFeatures(degree=deg, include_bias=False)),
            ("linear", LinearRegression()),
        ])

        # scikit-learn 的学习曲线工具
        train_sizes_abs, train_scores, val_scores = learning_curve(
            model, x, y,
            train_sizes=train_sizes,
            cv=5,
            scoring="neg_mean_squared_error",
            random_state=42,
            shuffle=True,
        )

        train_scores_mean = -np.mean(train_scores, axis=1)
        val_scores_mean = -np.mean(val_scores, axis=1)
        train_scores_std = np.std(train_scores, axis=1)
        val_scores_std = np.std(val_scores, axis=1)

        # 绘制训练/验证误差
        ax.plot(train_sizes_abs, train_scores_mean, "o-", color=color,
                linewidth=2, label="Train Error", markersize=4)
        ax.fill_between(train_sizes_abs,
                         train_scores_mean - train_scores_std,
                         train_scores_mean + train_scores_std,
                         alpha=0.15, color=color)
        ax.plot(train_sizes_abs, val_scores_mean, "x--", color="#8E44AD",
                linewidth=2, label="Validation Error", markersize=4)
        ax.fill_between(train_sizes_abs,
                         val_scores_mean - val_scores_std,
                         val_scores_mean + val_scores_std,
                         alpha=0.15, color="#8E44AD")

        # 标注"鸿沟"（过拟合时）
        if deg == 15:
            gap = val_scores_mean[-1] - train_scores_mean[-1]
            ax.annotate(f"Generalization Gap\n≈ {gap:.3f}",
                        xy=(train_sizes_abs[-1], val_scores_mean[-1]),
                        xytext=(train_sizes_abs[-1] * 0.6, (train_scores_mean[-1] + val_scores_mean[-1]) / 2),
                        fontsize=8, color="#C0392B", fontweight="bold",
                        arrowprops=dict(arrowstyle="->", color="#C0392B", lw=1.5))

        ax.set_title(title, fontsize=10.5)
        ax.set_xlabel("Training Set Size")
        if idx == 0:
            ax.set_ylabel("MSE")
        ax.legend(fontsize=8, loc="upper right")

    fig.suptitle("Learning Curves — Train/Validation Error vs Training Size",
                 fontsize=14, y=1.02)
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "learning_curves.png", bbox_inches="tight")
    plt.close(fig)
    print(f"    → 已保存 {OUTPUT_DIR / 'learning_curves.png'}")


# ════════════════════════════════════════════════════════════
# 4. K 折交叉验证演示
# ════════════════════════════════════════════════════════════
def demo_kfold_cv():
    """
    用 K=5 和 K=10 进行交叉验证，对比不同 K 值的得分分布。
    同时展示 Stratified K-Fold 在分类问题中的优势。
    """
    print("[3/5] K 折交叉验证 — 模型稳定性评估...")

    # 使用分类数据：逻辑回归 + 交叉验证
    X, y = make_classification(
        n_samples=200, n_features=10, n_informative=5,
        n_redundant=2, weights=[0.7, 0.3],  # 轻度不平衡
        random_state=42,
    )

    model = LogisticRegression(max_iter=1000, random_state=42)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))

    k_values = [5, 10]
    for idx, k in enumerate(k_values):
        ax = axes[idx]
        cv = KFold(n_splits=k, shuffle=True, random_state=42)
        scores = cross_val_score(model, X, y, cv=cv, scoring="accuracy")

        ax.bar(range(1, k + 1), scores, color="#3498DB", edgecolor="white",
               linewidth=1.2)
        ax.axhline(y=np.mean(scores), color="#E74C3C", linestyle="--",
                   linewidth=2, label=f"Mean: {np.mean(scores):.4f}")
        ax.fill_between(range(1, k + 1),
                         np.mean(scores) - np.std(scores),
                         np.mean(scores) + np.std(scores),
                         alpha=0.15, color="#E74C3C",
                         label=f"±1 Std: {np.std(scores):.4f}")

        ax.set_xlabel("Fold")
        ax.set_ylabel("Accuracy")
        ax.set_title(f"K-Fold CV (K={k}) — {k} Folds, {k} Models", fontsize=11)
        ax.set_xticks(range(1, k + 1))
        ax.set_ylim(0.5, 1.0)
        ax.legend(fontsize=9)

    fig.suptitle("K-Fold Cross-Validation — Accuracy per Fold",
                 fontsize=13, y=1.02)
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "kfold_cv.png", bbox_inches="tight")
    plt.close(fig)
    print(f"    → 已保存 {OUTPUT_DIR / 'kfold_cv.png'}")


# ════════════════════════════════════════════════════════════
# 5. 评估指标计算
# ════════════════════════════════════════════════════════════
def demo_metrics():
    """
    在合成二分类数据集上计算全部评估指标：
    Accuracy, Precision, Recall, F1, Confusion Matrix, ROC-AUC
    展示不平衡场景下指标的巨大差异。
    """
    print("[4/5] 评估指标计算 — 二分类场景...")

    # 生成两个数据集：平衡 vs 不平衡
    X_bal, y_bal = make_classification(
        n_samples=300, n_features=5, n_informative=3,
        weights=[0.5, 0.5], random_state=42,
    )
    X_imb, y_imb = make_classification(
        n_samples=300, n_features=5, n_informative=3,
        weights=[0.9, 0.1], random_state=42,  # 9:1 不平衡
    )

    datasets = [
        ("Balanced (50/50)", X_bal, y_bal),
        ("Imbalanced (90/10)", X_imb, y_imb),
    ]

    fig, axes = plt.subplots(2, 3, figsize=(13, 8))

    for row, (title, X, y) in enumerate(datasets):
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42, stratify=y,
        )

        model = LogisticRegression(max_iter=1000, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]

        # ── 计算指标 ──
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        roc_auc = roc_auc_score(y_test, y_prob)
        cm = confusion_matrix(y_test, y_pred)

        # ── 指标条形图 ──
        ax = axes[row, 0]
        metrics_names = ["Accuracy", "Precision", "Recall", "F1", "AUC"]
        metrics_values = [acc, prec, rec, f1, roc_auc]
        colors_bar = ["#3498DB" if v >= 0.7 else "#E74C3C" for v in metrics_values]
        bars = ax.bar(metrics_names, metrics_values, color=colors_bar, edgecolor="white")
        for bar, val in zip(bars, metrics_values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                    f"{val:.3f}", ha="center", va="bottom", fontsize=8)
        ax.set_ylim(0, 1.15)
        ax.set_ylabel("Score")
        ax.set_title(f"{title} — Metrics Comparison")
        ax.axhline(y=0.5, color="gray", linestyle=":", alpha=0.5)

        # ── 混淆矩阵 ──
        ax = axes[row, 1]
        im = ax.imshow(cm, interpolation="nearest", cmap="Blues")
        ax.set_title(f"{title} — Confusion Matrix")
        ax.set_xlabel("Predicted")
        ax.set_ylabel("True")
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        ax.set_xticklabels(["Neg", "Pos"])
        ax.set_yticklabels(["Neg", "Pos"])
        for i in range(2):
            for j in range(2):
                ax.text(j, i, str(cm[i, j]), ha="center", va="center",
                        fontsize=14, fontweight="bold",
                        color="white" if cm[i, j] > cm.max() / 2 else "black")
        plt.colorbar(im, ax=ax)

        # ── ROC 曲线 ──
        ax = axes[row, 2]
        fpr, tpr, thresholds = roc_curve(y_test, y_prob)
        roc_auc = auc(fpr, tpr)
        ax.plot(fpr, tpr, color="#2ECC71", linewidth=2.5,
                label=f"ROC (AUC = {roc_auc:.3f})")
        ax.plot([0, 1], [0, 1], "k--", linewidth=1, alpha=0.6, label="Random (AUC=0.5)")
        ax.fill_between(fpr, tpr, alpha=0.1, color="#2ECC71")
        ax.set_xlabel("False Positive Rate (FPR)")
        ax.set_ylabel("True Positive Rate (TPR)")
        ax.set_title(f"{title} — ROC Curve")
        ax.legend(loc="lower right", fontsize=9)
        ax.set_xlim(-0.02, 1.02)
        ax.set_ylim(-0.02, 1.02)

    fig.suptitle("Classification Metrics & ROC Curve — Balanced vs Imbalanced",
                 fontsize=14, y=1.01)
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "classification_metrics.png", bbox_inches="tight")
    plt.close(fig)
    print(f"    → 已保存 {OUTPUT_DIR / 'classification_metrics.png'}")


# ════════════════════════════════════════════════════════════
# 6. 验证曲线演示（附加）
# ════════════════════════════════════════════════════════════
def demo_validation_curve():
    """
    验证曲线（Validation Curve）：展示训练/验证误差随多项式阶数的变化。
    帮助我们找到偏差-方差平衡的最优点。
    """
    print("[5/5] 验证曲线 — 选择最优模型复杂度...")

    x, y = generate_sine_data(n_samples=100, noise_std=0.12)
    x = x.reshape(-1, 1)

    degrees = np.arange(1, 16)
    train_errors = []
    val_errors = []

    # 使用单独的验证集
    x_train, x_val, y_train, y_val = train_test_split(
        x, y, test_size=0.3, random_state=42
    )

    for deg in degrees:
        model = Pipeline([
            ("poly", PolynomialFeatures(degree=deg, include_bias=False)),
            ("linear", LinearRegression()),
        ])
        model.fit(x_train, y_train)

        train_pred = model.predict(x_train)
        val_pred = model.predict(x_val)

        train_errors.append(np.mean((y_train - train_pred) ** 2))
        val_errors.append(np.mean((y_val - val_pred) ** 2))

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(degrees, train_errors, "o-", color="#3498DB", linewidth=2,
            label="Train Error", markersize=5)
    ax.plot(degrees, val_errors, "s--", color="#E74C3C", linewidth=2,
            label="Validation Error", markersize=5)

    # 标注最优点
    best_deg = degrees[np.argmin(val_errors)]
    best_val = np.min(val_errors)
    ax.axvline(x=best_deg, color="#2ECC71", linestyle=":", linewidth=1.5,
               alpha=0.8)
    ax.annotate(f"Optimal Degree = {best_deg}",
                xy=(best_deg, best_val),
                xytext=(best_deg + 3, best_val * 1.5),
                fontsize=10, color="#2ECC71", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#2ECC71", lw=1.5))

    # 标注欠拟合/过拟合区域
    ax.axvspan(1, best_deg - 1, alpha=0.1, color="#E74C3C",
               label="Underfitting Region")
    ax.axvspan(best_deg + 1, 15, alpha=0.1, color="#9B59B6",
               label="Overfitting Region")

    ax.set_xlabel("Polynomial Degree (Model Complexity)")
    ax.set_ylabel("MSE")
    ax.set_title("Validation Curve — Finding the Optimal Model Complexity",
                 fontsize=13)
    ax.set_xticks(degrees)
    ax.legend(fontsize=10)
    ax.set_yscale("log")  # 使用对数刻度更好展示差异

    fig.savefig(OUTPUT_DIR / "validation_curve.png", bbox_inches="tight")
    plt.close(fig)
    print(f"    → 已保存 {OUTPUT_DIR / 'validation_curve.png'}")
    print(f"    → 最优多项式阶数: Degree = {best_deg}")


# ════════════════════════════════════════════════════════════
# 7. 主入口
# ════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print("模型评估与验证演示")
    print("Model Evaluation & Validation Demo")
    print("=" * 60)

    demo_overfitting_underfitting()
    demo_learning_curves()
    demo_kfold_cv()
    demo_metrics()
    demo_validation_curve()

    print("=" * 60)
    print("✅ 全部图表已生成到 output/ 目录")
    print(f"   输出路径: {OUTPUT_DIR.resolve()}")
    print("=" * 60)
