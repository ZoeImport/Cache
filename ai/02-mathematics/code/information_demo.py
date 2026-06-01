"""
04 — 信息论与机器学习配套代码（Information Theory for ML Companion Code）

功能列表 (Features):
  1. demo_self_information()  — 自信息曲线可视化
  2. demo_entropy_coin()      — 抛硬币熵曲线（最大熵在 p=0.5）
  3. demo_kl_gaussian()       — 两个高斯分布之间的 KL 散度
  4. demo_cross_entropy()     — 交叉熵 vs KL 散度对比
  5. demo_mutual_info_selection() — 互信息特征选择示例

依赖: numpy, scipy, matplotlib, sklearn
运行: python information_demo.py
"""

import numpy as np
from scipy.stats import multivariate_normal, entropy
from sklearn.feature_selection import mutual_info_classif
from sklearn.datasets import make_classification
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")


# ============================================================
# 1. 自信息（Self-Information）
# ============================================================
def demo_self_information():
    """
    演示自信息 I(x) = -log P(x) 如何随概率变化。
    小概率事件携带高信息量。
    """
    print("=" * 60)
    print("1. 自信息 (Self-Information)")
    print("=" * 60)

    p_values = np.linspace(0.001, 0.999, 100)
    info_bits = -np.log2(p_values)
    info_nats = -np.log(p_values)

    print(f"P=0.5   → I = {-np.log2(0.5):.2f} bit  (一次公平抛硬币的结果)")
    print(f"P=0.1   → I = {-np.log2(0.1):.2f} bit  (小概率事件 → 高信息量)")
    print(f"P=0.9   → I = {-np.log2(0.9):.2f} bit  (高概率事件 → 低信息量)")
    print()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # 左图: 自信息 vs 概率
    ax1.plot(p_values, info_bits, "b-", linewidth=2)
    ax1.axvline(0.5, color="gray", linestyle="--", alpha=0.5)
    ax1.axhline(1.0, color="gray", linestyle="--", alpha=0.5)
    ax1.set_xlabel("Probability P(x)")
    ax1.set_ylabel("Self-Information (bits)")
    ax1.set_title("Self-Information vs Probability\n自信息随概率变化")
    ax1.grid(alpha=0.3)
    ax1.set_xlim(0, 1)

    # 右图: 信息量对比
    example_ps = [0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99]
    example_infos = [-np.log2(p) for p in example_ps]
    colors = plt.cm.Reds(np.linspace(0.3, 0.9, len(example_ps)))
    bars = ax2.bar(range(len(example_ps)), example_infos, color=colors, width=0.6)
    ax2.set_xticks(range(len(example_ps)))
    ax2.set_xticklabels([f"P={p}" for p in example_ps], rotation=45)
    ax2.set_ylabel("Self-Information (bits)")
    ax2.set_title("Information Carried by Events of Different Probability\n不同概率事件携带的信息量")
    ax2.grid(alpha=0.3, axis="y")

    # 在柱子上标注数值
    for bar, val in zip(bars, example_infos):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                 f"{val:.1f}", ha="center", va="bottom", fontsize=9)

    plt.tight_layout()
    plt.savefig("ai/02-mathematics/code/self_information.png", dpi=150)
    plt.close()
    print("[Saved] self_information.png")


# ============================================================
# 2. 熵（Entropy）—— 抛硬币示例
# ============================================================
def demo_entropy_coin():
    """
    伯努利分布的熵 H(p) = -p log p - (1-p) log(1-p)
    在 p=0.5 时取最大值 1 bit。
    """
    print("=" * 60)
    print("2. 抛硬币的熵 (Entropy of a Coin Flip)")
    print("=" * 60)

    p = np.linspace(0.001, 0.999, 500)
    # 伯努利熵: H = -p*log2(p) - (1-p)*log2(1-p)
    h = -p * np.log2(p) - (1 - p) * np.log2(1 - p)

    print(f"p=0.0   → H = 0.00 bit  (完全确定)")
    print(f"p=0.5   → H = {h[np.argmin(np.abs(p - 0.5))]:.2f} bit  (最大不确定性)")
    print(f"p=0.9   → H = {h[np.argmin(np.abs(p - 0.9))]:.2f} bit  (偏向确定)")
    print()

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(p, h, "r-", linewidth=2.5, label="Entropy H(p)")
    # 标注最大值点
    ax.plot(0.5, 1.0, "go", markersize=10, label="Max entropy at p=0.5\n最大熵 (p=0.5)")
    ax.axvline(0.5, color="green", linestyle="--", alpha=0.4)
    ax.axhline(1.0, color="green", linestyle="--", alpha=0.4)

    # 标注低熵区域
    ax.fill_between(p, h, alpha=0.1, color="red", label="High uncertainty (高不确定性)")
    ax.fill_between(p[p < 0.2], h[p < 0.2], alpha=0.2, color="blue",
                     label="Low uncertainty (低不确定性)")
    ax.fill_between(p[p > 0.8], h[p > 0.8], alpha=0.2, color="blue")

    ax.set_xlabel("Probability of Heads P(Heads)")
    ax.set_ylabel("Entropy H(p) (bits)")
    ax.set_title("Entropy of a Bernoulli Distribution (Coin Flip)\n伯努利分布（抛硬币）的熵")
    ax.legend(loc="upper left")
    ax.grid(alpha=0.3)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.1)

    plt.tight_layout()
    plt.savefig("ai/02-mathematics/code/entropy_coin.png", dpi=150)
    plt.close()
    print("[Saved] entropy_coin.png")


# ============================================================
# 3. KL 散度（KL Divergence）—— 两个高斯分布
# ============================================================
def kl_divergence_gaussian(mu1, sigma1, mu2, sigma2):
    """
    计算两个多元高斯分布之间的 KL 散度。

    公式:
    D_KL(P||Q) = 0.5 * [ log(|Σ2|/|Σ1|) - d + tr(Σ2^{-1} Σ1)
                        + (μ2-μ1)^T Σ2^{-1} (μ2-μ1) ]
    """
    d = mu1.shape[0]
    sigma2_inv = np.linalg.inv(sigma2)

    term1 = np.log(np.linalg.det(sigma2) / np.linalg.det(sigma1))
    term2 = -d
    term3 = np.trace(sigma2_inv @ sigma1)
    diff = mu2 - mu1
    term4 = diff.T @ sigma2_inv @ diff

    return 0.5 * (term1 + term2 + term3 + term4)


def demo_kl_gaussian():
    """
    演示两个高斯分布之间的 KL 散度。
    展示 D_KL(P||Q) 的不对称性。
    """
    print("=" * 60)
    print("3. 高斯分布的 KL 散度 (KL Divergence between Gaussians)")
    print("=" * 60)

    # 构造两个一维高斯分布
    # P ~ N(0, 1)   标准正态
    # Q1 ~ N(1, 1)  均值偏移 1
    # Q2 ~ N(0, 2)  方差放大
    # Q3 ~ N(2, 0.5) 均值偏移 2, 缩方差

    mu_p = np.array([0.0])
    sigma_p = np.array([[1.0]])

    distributions = {
        "Q1: N(1, 1)": (np.array([1.0]), np.array([[1.0]])),
        "Q2: N(0, 2)": (np.array([0.0]), np.array([[2.0]])),
        "Q3: N(2, 0.5)": (np.array([2.0]), np.array([[0.5]])),
    }

    print(f"{'Distribution':<20} {'D_KL(P||Q)':<15} {'D_KL(Q||P)':<15}")
    print("-" * 50)
    for name, (mu_q, sigma_q) in distributions.items():
        kl_pq = kl_divergence_gaussian(mu_p, sigma_p, mu_q, sigma_q)
        kl_qp = kl_divergence_gaussian(mu_q, sigma_q, mu_p, sigma_p)
        print(f"{name:<20} {kl_pq:<15.4f} {kl_qp:<15.4f}")

    print()
    print("观察: D_KL(P||Q) ≠ D_KL(Q||P) — KL 散度不对称!")
    print()

    # 可视化: 展示 P 和 Q 的分布 + KL 散度值
    x = np.linspace(-4, 6, 500)
    pdf_p = multivariate_normal.pdf(x, mean=mu_p, cov=sigma_p)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    for idx, (name, (mu_q, sigma_q)) in enumerate(distributions.items()):
        ax = axes[idx]
        pdf_q = multivariate_normal.pdf(x, mean=mu_q, cov=sigma_q)
        kl = kl_divergence_gaussian(mu_p, sigma_p, mu_q, sigma_q)

        ax.plot(x, pdf_p, "b-", linewidth=2, label="P ~ N(0,1)")
        ax.plot(x, pdf_q, "r--", linewidth=2, label=name)
        ax.fill_between(x, pdf_p, pdf_q, alpha=0.15, color="purple",
                         label=f"D_KL={kl:.2f}")
        ax.set_xlabel("x")
        ax.set_ylabel("Probability Density")
        ax.set_title(f"D_KL(P||Q) = {kl:.3f}")
        ax.legend(fontsize=8)
        ax.grid(alpha=0.3)

    fig.suptitle("KL Divergence between Gaussian Distributions (高斯分布之间的 KL 散度)",
                 fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig("ai/02-mathematics/code/kl_divergence_gaussian.png", dpi=150)
    plt.close()
    print("[Saved] kl_divergence_gaussian.png")


# ============================================================
# 4. 交叉熵（Cross-Entropy）vs KL 散度
# ============================================================
def demo_cross_entropy():
    """
    演示 H(P,Q) = H(P) + D_KL(P||Q)。
    当 P 是 one-hot 分布时，H(P)=0，交叉熵 = KL 散度。
    这解释了为什么分类损失使用交叉熵。
    """
    print("=" * 60)
    print("4. 交叉熵与 KL 散度 (Cross-Entropy vs KL Divergence)")
    print("=" * 60)

    # 场景: 三分类问题
    # 真实分布 P (one-hot): 类别 0 是正确类别
    p_true = np.array([1.0, 0.0, 0.0])

    # 模型预测分布 Q: 各种不同的预测质量
    predictions = {
        "Perfect (完美)":       np.array([0.98, 0.01, 0.01]),
        "Decent (还不错)":      np.array([0.80, 0.15, 0.05]),
        "Confident Wrong (自信错)": np.array([0.05, 0.90, 0.05]),
        "Uniform (均匀分布)":   np.array([1/3, 1/3, 1/3]),
        "Terrible (极差)":      np.array([0.01, 0.49, 0.50]),
    }

    print(f"{'Prediction':<25} {'H(P,Q)':<12} {'D_KL(P||Q)':<12} {'H(P)':<10}")
    print("-" * 59)

    h_p = entropy(p_true, base=2)

    for name, q in predictions.items():
        # 交叉熵: H(P,Q) = -sum P log Q
        cross_ent = -np.sum(p_true * np.log2(q + 1e-15))
        # KL 散度
        kl = np.sum(p_true * np.log2((p_true + 1e-15) / (q + 1e-15)))
        print(f"{name:<25} {cross_ent:<12.4f} {kl:<12.4f} {h_p:<10.4f}")

    print()
    print("关键观察: 当 P 是 one-hot 时, H(P)=0, 所以 H(P,Q) = D_KL(P||Q)")
    print("这就是为什么: 最小化交叉熵 = 最小化 KL 散度 = 让模型匹配数据分布")
    print()

    # 可视化: 展示不同预测的交叉熵
    names = list(predictions.keys())
    values = [-np.sum(p_true * np.log2(predictions[n] + 1e-15)) for n in names]
    colors = ["green" if v < 1 else ("orange" if v < 3 else "red") for v in values]

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.barh(names, values, color=colors, height=0.6)
    ax.axvline(values[0], color="green", linestyle="--", alpha=0.5,
               label=f"Perfect={values[0]:.2f}")

    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2,
                f"{val:.2f}", ha="left", va="center", fontsize=10)

    ax.set_xlabel("Cross-Entropy H(P, Q) (bits)")
    ax.set_title("Cross-Entropy for Different Model Predictions\n不同模型预测的交叉熵")
    ax.legend()
    ax.grid(alpha=0.3, axis="x")

    plt.tight_layout()
    plt.savefig("ai/02-mathematics/code/cross_entropy_demo.png", dpi=150)
    plt.close()
    print("[Saved] cross_entropy_demo.png")


# ============================================================
# 5. 互信息特征选择（Mutual Information for Feature Selection）
# ============================================================
def demo_mutual_info_selection():
    """
    用互信息进行特征选择:
    - 生成一个包含有用/无用特征的分类数据集
    - 计算每个特征与标签的互信息
    - 对比互信息与相关系数的区别
    """
    print("=" * 60)
    print("5. 互信息特征选择 (Mutual Information for Feature Selection)")
    print("=" * 60)

    # 生成合成数据: 20 个特征中只有 5 个是有信息的
    np.random.seed(42)
    n_samples = 500
    n_features = 20
    n_informative = 5

    X, y = make_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_informative=n_informative,
        n_redundant=3,
        n_repeated=0,
        n_classes=2,
        random_state=42,
    )

    # 添加一个完全随机的列作为噪声基准
    X = np.column_stack([X, np.random.randn(n_samples)])

    # 1) 互信息法
    mi_scores = mutual_info_classif(X, y, random_state=42)
    mi_ranking = np.argsort(mi_scores)[::-1]

    # 2) 相关系数法（绝对值）
    corr_scores = np.abs([np.corrcoef(X[:, i], y)[0, 1] for i in range(X.shape[1])])
    corr_ranking = np.argsort(corr_scores)[::-1]

    print(f"数据集: {n_samples} 个样本, {n_features+1} 个特征 (含 1 个纯噪声)")
    print(f"真实有信息特征数: {n_informative}")
    print()
    print(f"{'Rank':<8} {'MI Score':<12} {'Feature #':<12} {'Corr Score':<12} {'Feature #':<12}")
    print("-" * 56)

    for rank in range(10):
        fi = mi_ranking[rank]
        ci = corr_ranking[rank]
        print(f"{rank+1:<8} {mi_scores[fi]:<12.4f} {fi:<12d} {corr_scores[ci]:<12.4f} {ci:<12d}")

    print()
    print("观察: 互信息能识别出非线性相关的有用特征，而皮尔逊相关系数可能漏掉")
    print()

    # 可视化: 互信息分数 vs 相关系数
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # 互信息柱状图
    feat_indices = np.arange(X.shape[1])
    mi_colors = ["green" if i < n_informative else "red" for i in range(X.shape[1])]
    ax1.bar(feat_indices, mi_scores, color=mi_colors, width=0.6, edgecolor="black", linewidth=0.5)
    ax1.axhline(np.median(mi_scores), color="purple", linestyle="--",
                label=f"Median MI = {np.median(mi_scores):.3f}")
    ax1.set_xlabel("Feature Index")
    ax1.set_ylabel("Mutual Information (nats)")
    ax1.set_title("Mutual Information with Target\n特征与目标的互信息")
    ax1.legend()
    ax1.grid(alpha=0.3, axis="y")

    # 相关系数柱状图
    ax2.bar(feat_indices, corr_scores, color=mi_colors, width=0.6, edgecolor="black", linewidth=0.5)
    ax2.axhline(np.median(corr_scores), color="purple", linestyle="--",
                label=f"Median |r| = {np.median(corr_scores):.3f}")
    ax2.set_xlabel("Feature Index")
    ax2.set_ylabel("|Pearson Correlation|")
    ax2.set_title("Absolute Pearson Correlation with Target\n特征与目标的 |皮尔逊相关系数|")
    ax2.legend()
    ax2.grid(alpha=0.3, axis="y")

    fig.suptitle("Feature Selection: Mutual Information vs Correlation\n特征选择: 互信息 vs 相关系数",
                 fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig("ai/02-mathematics/code/mutual_info_selection.png", dpi=150)
    plt.close()
    print("[Saved] mutual_info_selection.png")


# ============================================================
# 主函数
# ============================================================
if __name__ == "__main__":
    print()
    print("╔" + "═" * 58 + "╗")
    print("║   信息论与机器学习 — 配套演示代码                    ║")
    print("║   Information Theory for ML — Companion Demo         ║")
    print("╚" + "═" * 58 + "╝")
    print()

    demo_self_information()
    demo_entropy_coin()
    demo_kl_gaussian()
    demo_cross_entropy()
    demo_mutual_info_selection()

    print("=" * 60)
    print("全部演示完成！(All demos completed!)")
    print("=" * 60)
    print()
    print("生成的图片 (Generated figures):")
    print("  - self_information.png")
    print("  - entropy_coin.png")
    print("  - kl_divergence_gaussian.png")
    print("  - cross_entropy_demo.png")
    print("  - mutual_info_selection.png")
    print()
    print("推导链核心总结 (Core Derivation Chain):")
    print("  I(x) → H(X) → D_KL(P||Q) → H(P,Q) → CrossEntropyLoss")
    print("  自信息 → 熵 → KL散度 → 交叉熵 → ML损失函数")
