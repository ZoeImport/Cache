"""
statistics_demo.py — 统计基础配套代码（Statistical Foundations for ML）
========================================================================
演示内容：
  1. 偏差-方差权衡（Bias-Variance Tradeoff）：用多项式回归拟合 sin(x)
     观察不同程度（1, 3, 10）下的拟合行为
  2. Bootstrap 置信区间（Bootstrap Confidence Interval）：估计样本均值的置信区间

依赖：numpy, scipy, sklearn, matplotlib (见 ai/requirements.txt)
运行：python statistics_demo.py
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline

# ============================================================================
# 全局设置
# ============================================================================
np.random.seed(42)
plt.rcParams["figure.dpi"] = 120
plt.rcParams["font.size"] = 11


# ============================================================================
# 第一部分：偏差-方差权衡（Bias-Variance Tradeoff）
# ============================================================================
def true_function(x):
    """真实数据生成过程：f(x) = sin(x)"""
    return np.sin(x)


def generate_data(n_samples=30, noise_std=0.25):
    """从真实函数生成带噪声的训练数据。

    参数
    ----------
    n_samples : int
        样本数量。
    noise_std : float
        高斯噪声的标准差。

    返回
    -------
    X : ndarray, shape (n_samples, 1)
        输入特征。
    y : ndarray, shape (n_samples,)
        含噪声的目标值。
    """
    X = np.linspace(0, 2 * np.pi, n_samples)
    y = true_function(X) + np.random.normal(0, noise_std, size=n_samples)
    return X.reshape(-1, 1), y


def fit_polynomial(X, y, degree):
    """用指定次数的多项式回归拟合数据。

    参数
    ----------
    X : ndarray, shape (n_samples, 1)
        输入特征。
    y : ndarray, shape (n_samples,)
        目标值。
    degree : int
        多项式的次数。

    返回
    -------
    model : sklearn.pipeline.Pipeline
        拟合后的模型。
    """
    model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
    model.fit(X, y)
    return model


def part1_bias_variance_demo():
    """偏差-方差权衡可视化。

    用 sin(x) 作为真实函数，分别用 1 次、3 次、10 次多项式拟合，
    直观展示欠拟合（高偏差）与过拟合（高方差）的行为差异。
    """
    print("=" * 60)
    print("第一部分：偏差-方差权衡（Bias-Variance Tradeoff）")
    print("=" * 60)

    # ---- 生成并拟合数据 ----
    X_train, y_train = generate_data(n_samples=15, noise_std=0.3)
    X_plot = np.linspace(0, 2 * np.pi, 200).reshape(-1, 1)
    y_true = true_function(X_plot)

    degrees = [1, 3, 10]
    colors = ["#E74C3C", "#2ECC71", "#3498DB"]
    labels = [f"Degree={d}" for d in degrees]

    # ---- 绘制 ----
    fig, axes = plt.subplots(1, 3, figsize=(14, 4), sharey=True)

    for idx, (deg, color, label) in enumerate(zip(degrees, colors, labels)):
        model = fit_polynomial(X_train, y_train, deg)
        y_pred = model.predict(X_plot)

        ax = axes[idx]
        # 训练数据散点
        ax.scatter(X_train, y_train, color="gray", alpha=0.6, s=20, label="Training data")
        # 真实函数
        ax.plot(X_plot, y_true, "k--", linewidth=1.5, label="True $f(x) = \\sin(x)$")
        # 模型预测
        ax.plot(X_plot, y_pred, color=color, linewidth=2, label=label)

        # 计算训练集上的 MSE
        train_pred = model.predict(X_train)
        mse = np.mean((y_train - train_pred) ** 2)
        ax.set_title(f"{label}\nTrain MSE = {mse:.4f}", fontsize=11)
        ax.set_xlim(0, 2 * np.pi)
        ax.set_ylim(-2.2, 2.2)
        ax.set_xlabel("x")
        if idx == 0:
            ax.set_ylabel("y")
        ax.legend(fontsize=8)
        ax.grid(alpha=0.3)

    fig.suptitle("Bias-Variance Tradeoff: Polynomial Fitting of $\\sin(x)$", fontsize=13, y=1.02)
    plt.tight_layout()
    plt.savefig("bias_variance_demo.png", bbox_inches="tight")
    plt.close()
    print("  → 图像已保存至 bias_variance_demo.png\n")

    # ---- 打印解读 ----
    print("  【观察结果】")
    print(
        "  度=1 (一图):  模型是一条直线，无法捕捉 sin(x) 的波动 → 高偏差 (Underfitting)"
    )
    print(
        "  度=3 (中图):  较好地拟合了曲线形状，偏差和方差较为均衡"
    )
    print(
        "  度=10 (右图): 模型精确穿过每个训练点，但曲线剧烈振荡"
    )
    print(
        "                 → 高方差 (Overfitting)，对新数据泛化能力差"
    )
    print()


# ============================================================================
# 第二部分：Bootstrap 置信区间（Bootstrap Confidence Interval）
# ============================================================================
def bootstrap_ci(data, statistic=np.mean, n_bootstrap=10000, ci_level=95):
    """用 Bootstrap 方法计算统计量的置信区间。

    参数
    ----------
    data : ndarray
        原始样本数据。
    statistic : callable
        要计算不确定性的统计量函数（如 np.mean, np.median）。
    n_bootstrap : int
        Bootstrap 重采样次数。
    ci_level : float
        置信水平（百分比），默认 95。

    返回
    -------
    ci_lower : float
        置信区间下限。
    ci_upper : float
        置信区间上限。
    boot_stats : ndarray, shape (n_bootstrap,)
        Bootstrap 样本的统计量值。
    """
    n = len(data)
    boot_stats = np.zeros(n_bootstrap)

    for i in range(n_bootstrap):
        # 有放回重采样（Resampling with Replacement）
        sample = np.random.choice(data, size=n, replace=True)
        boot_stats[i] = statistic(sample)

    # 百分位 Bootstrap 区间（Percentile Bootstrap Interval）
    lower = (100 - ci_level) / 2
    upper = 100 - lower
    ci_lower, ci_upper = np.percentile(boot_stats, [lower, upper])
    return ci_lower, ci_upper, boot_stats


def part2_bootstrap_demo():
    """Bootstrap 置信区间演示。

    从指数分布（偏态分布，非正态）中采样，
    用 Bootstrap 估计样本均值的置信区间，
    并与理论正态区间进行对比。
    """
    print("=" * 60)
    print("第二部分：Bootstrap 置信区间（Bootstrap Resampling）")
    print("=" * 60)

    # ---- 从偏态分布（指数分布）中采样 ----
    np.random.seed(123)
    population_mean = 5.0  # 指数分布的真实均值 λ=0.2 → μ=5
    n = 50
    data = np.random.exponential(scale=population_mean, size=n)

    sample_mean = np.mean(data)
    sample_std = np.std(data, ddof=1)
    se = sample_std / np.sqrt(n)  # 标准误（Standard Error）

    print(f"  总体真实均值 (True μ)  = {population_mean}")
    print(f"  样本均值 (Sample Mean) = {sample_mean:.3f}")
    print(f"  样本标准差 (Sample σ)  = {sample_std:.3f}")
    print(f"  标准误 SE              = {se:.3f}")
    print(f"  样本量 n               = {n}")
    print()

    # ---- Bootstrap ----
    ci_low_boot, ci_high_boot, boot_means = bootstrap_ci(
        data, statistic=np.mean, n_bootstrap=10000, ci_level=95
    )

    # ---- 理论正态区间（t 分布） ----
    from scipy import stats as sp_stats

    t_val = sp_stats.t.ppf(0.975, df=n - 1)
    ci_low_theory = sample_mean - t_val * se
    ci_high_theory = sample_mean + t_val * se

    print(f"  95% Bootstrap 置信区间: [{ci_low_boot:.3f}, {ci_high_boot:.3f}]")
    print(f"  95% t-分布 置信区间:    [{ci_low_theory:.3f}, {ci_high_theory:.3f}]")
    print()

    # 由于指数分布是偏态的，Bootstrap 区间通常更准确
    # （t 分布区间假设数据来自正态分布，对于偏态数据会偏移）
    print(
        "  【说明】指数分布是右偏态分布（Right-Skewed），"
    )
    print(
        "  因此 Bootstrap 区间往往比 t-分布区间更可靠。"
    )
    print()

    # ---- 可视化 ----
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    # 左图：原始数据分布
    ax0 = axes[0]
    ax0.hist(data, bins=15, color="steelblue", edgecolor="white", alpha=0.7)
    ax0.axvline(sample_mean, color="red", linewidth=2, label=f"Sample mean = {sample_mean:.2f}")
    ax0.axvline(population_mean, color="black", ls="--", linewidth=1.5, label=f"Population mean = {population_mean}")
    ax0.set_xlabel("Value")
    ax0.set_ylabel("Frequency")
    ax0.set_title("Original Data (Exponential Distribution)")
    ax0.legend(fontsize=9)
    ax0.grid(alpha=0.3)

    # 右图：Bootstrap 样本均值的分布
    ax1 = axes[1]
    ax1.hist(boot_means, bins=40, color="coral", edgecolor="white", alpha=0.7)
    ax1.axvline(sample_mean, color="red", linewidth=2, label=f"Sample mean = {sample_mean:.2f}")
    ax1.axvline(ci_low_boot, color="darkgreen", ls="--", linewidth=1.5,
                label=f"CI lower = {ci_low_boot:.2f}")
    ax1.axvline(ci_high_boot, color="darkgreen", ls="--", linewidth=1.5,
                label=f"CI upper = {ci_high_boot:.2f}")
    ax1.set_xlabel("Bootstrap sample mean")
    ax1.set_ylabel("Frequency")
    ax1.set_title("Bootstrap Sampling Distribution (B=10000)")
    ax1.legend(fontsize=9)
    ax1.grid(alpha=0.3)

    plt.suptitle(f"Bootstrap: 95% CI of the Sample Mean", fontsize=13)
    plt.tight_layout()
    plt.savefig("bootstrap_ci_demo.png", bbox_inches="tight")
    plt.close()
    print("  → 图像已保存至 bootstrap_ci_demo.png\n")


# ============================================================================
# 第三部分：Bias-Variance 的蒙特卡洛模拟（Monte Carlo Simulation）
# ============================================================================
def part3_bias_variance_mc():
    """用蒙特卡洛模拟定量计算偏差和方差。

    多次生成不同的训练集，训练同一模型，计算预测的偏差和方差。
    直观展示 Bias² + Variance 如何随模型复杂度变化。
    """
    print("=" * 60)
    print("第三部分：偏差-方差的蒙特卡洛模拟")
    print("=" * 60)

    np.random.seed(42)
    n_repeats = 200  # 生成 200 个不同的训练集
    n_train = 30
    noise_std = 0.2

    # 在固定测试点上评估
    X_test = np.linspace(0, 2 * np.pi, 100)
    y_test_true = true_function(X_test)
    degrees = [1, 2, 3, 5, 8, 12]

    results = {"degree": [], "bias2": [], "variance": [], "total_error": []}

    for deg in degrees:
        # 存储每个训练集在该测试点上的预测
        preds = np.zeros((n_repeats, len(X_test)))

        for i in range(n_repeats):
            X_tr, y_tr = generate_data(n_train, noise_std)
            model = fit_polynomial(X_tr, y_tr, deg)
            preds[i, :] = model.predict(X_test.reshape(-1, 1)).flatten()

        # 计算偏差和方差（对每个测试点）
        pred_mean = np.mean(preds, axis=0)  # 所有模型的平均预测
        bias2 = np.mean((pred_mean - y_test_true) ** 2)
        variance = np.mean(np.var(preds, axis=0, ddof=1))
        total_error = np.mean((preds - y_test_true) ** 2)

        results["degree"].append(deg)
        results["bias2"].append(bias2)
        results["variance"].append(variance)
        results["total_error"].append(total_error)

        print(f"  度={deg:2d}  |  Bias²={bias2:.4f}  |  Variance={variance:.4f}  "
              f"|  Total={total_error:.4f}")

    print()

    # ---- 绘制误差分解 ----
    fig, ax = plt.subplots(figsize=(8, 5))
    x = results["degree"]

    ax.bar(x, results["bias2"], label="Bias²", color="#E74C3C", alpha=0.8)
    ax.bar(x, results["variance"], bottom=results["bias2"],
           label="Variance", color="#3498DB", alpha=0.8)

    # 标注总误差
    ax.plot(x, results["total_error"], "ko-", linewidth=2, label="Total Error (MSE)")
    ax.set_xlabel("Polynomial Degree")
    ax.set_ylabel("Error")
    ax.set_title("Bias² + Variance vs Model Complexity")
    ax.legend(fontsize=10)
    ax.set_xticks(x)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig("bias_variance_mc.png", bbox_inches="tight")
    plt.close()
    print("  → 图像已保存至 bias_variance_mc.png\n")


# ============================================================================
# 主函数
# ============================================================================
if __name__ == "__main__":
    part1_bias_variance_demo()   # ① 多项式拟合可视化
    part2_bootstrap_demo()       # ② Bootstrap 置信区间
    part3_bias_variance_mc()     # ③ 蒙特卡洛偏差-方差分解
    print("全部完成! 请查看生成的 .png 图像。")
