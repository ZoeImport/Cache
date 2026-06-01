"""
概率论与机器学习演示（Probability Theory for ML — Demo）
=========================================================
依赖：numpy>=1.24.0, scipy>=1.11.0, matplotlib>=3.7.0

展示：
1. 离散分布：伯努利、二项（Bernoulli, Binomial）
2. 连续分布：正态（Normal / Gaussian）
3. 贝叶斯定理计算（Bayes' Theorem）
4. MLE 数值求解（Maximum Likelihood Estimation）
5. 期望、方差的数值验证（Expectation & Variance）
"""

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


# ============================================================
# 1. 离散分布（Discrete Distributions）
# ============================================================
print("=" * 65)
print("1. 离散分布（Discrete Distributions）")
print("=" * 65)

# ----------------------------------------------------------
# 1.1 伯努利分布（Bernoulli Distribution）
# ----------------------------------------------------------
print("\n--- 1.1 伯努利分布（Bernoulli Distribution）---")

p = 0.7  # 成功的概率
bern = stats.bernoulli(p)

# PMF 验证
print(f"伯努利(p={p}) PMF:")
for x in [0, 1]:
    prob = bern.pmf(x)
    formula = p**x * (1 - p)**(1 - x)
    print(f"  P(X={x}) = {prob:.4f}  (公式验证: {formula:.4f})")

# 期望与方差
print(f"\n期望 E[X] = {bern.mean():.4f}  (公式: p = {p})")
print(f"方差 Var[X] = {bern.var():.4f}  (公式: p(1-p) = {p*(1-p):.4f})")

# 采样验证
samples = bern.rvs(size=10000, random_state=42)
print(f"\n采样 10000 次的均值 = {samples.mean():.4f}  (接近理论值 {p})")
print(f"采样 10000 次的方差 = {samples.var():.4f}  (接近理论值 {p*(1-p):.4f})")

# ----------------------------------------------------------
# 1.2 二项分布（Binomial Distribution）
# ----------------------------------------------------------
print("\n--- 1.2 二项分布（Binomial Distribution）---")

n, p_binom = 10, 0.5
binom = stats.binom(n, p_binom)

print(f"二项分布(n={n}, p={p_binom}) PMF:")
for k in [0, 1, 5, 10]:
    prob = binom.pmf(k)
    # 公式验证: C(n,k) * p^k * (1-p)^(n-k)
    from math import comb
    formula = comb(n, k) * (p_binom**k) * ((1 - p_binom)**(n - k))
    print(f"  P(X={k:2d}) = {prob:.4f}  (公式: {formula:.4f})")

print(f"\n期望 E[X] = {binom.mean():.4f}  (公式: n*p = {n * p_binom})")
print(f"方差 Var[X] = {binom.var():.4f}  (公式: n*p*(1-p) = {n * p_binom * (1 - p_binom):.4f})")

samples_binom = binom.rvs(size=10000, random_state=42)
print(f"\n采样 10000 次的均值 = {samples_binom.mean():.4f}")
print(f"采样 10000 次的方差 = {samples_binom.var():.4f}")


# ============================================================
# 2. 连续分布：正态分布（Continuous: Normal / Gaussian）
# ============================================================
print("\n" + "=" * 65)
print("2. 正态分布（Normal / Gaussian Distribution）")
print("=" * 65)

mu, sigma = 5.0, 2.0
norm = stats.norm(mu, sigma)

# PDF 在特定点的值
x_vals = [3.0, 5.0, 7.0]
print(f"正态分布 N(μ={mu}, σ={sigma}) PDF:")
for x in x_vals:
    pdf_val = norm.pdf(x)
    formula = (1 / np.sqrt(2 * np.pi * sigma**2)) * \
              np.exp(-(x - mu)**2 / (2 * sigma**2))
    print(f"  f({x:.1f}) = {pdf_val:.6f}  (公式: {formula:.6f})")

# CDF 验证 68-95-99.7 法则
print("\n68-95-99.7 法则验证:")
for k, label in [(1, "68%"), (2, "95%"), (3, "99.7%")]:
    prob = norm.cdf(mu + k * sigma) - norm.cdf(mu - k * sigma)
    print(f"  P(|X-μ| < {k}σ) = {prob:.4f}  (≈ {label})")

print(f"\n期望 E[X] = {norm.mean():.4f}  (公式: μ = {mu})")
print(f"方差 Var[X] = {norm.var():.4f}  (公式: σ² = {sigma**2})")

samples_norm = norm.rvs(size=100000, random_state=42)
print(f"\n采样 100000 次的均值 = {samples_norm.mean():.4f}  (理论: {mu})")
print(f"采样 100000 次的方差 = {samples_norm.var():.4f}  (理论: {sigma**2})")


# ============================================================
# 3. 贝叶斯定理（Bayes' Theorem）—— 医学检测案例
# ============================================================
print("\n" + "=" * 65)
print("3. 贝叶斯定理（Bayes' Theorem）—— 医学检测")
print("=" * 65)

# 参数设定
prevalence = 0.01       # 患病率 P(病)
sensitivity = 0.99      # 灵敏度  P(+|病)
specificity = 0.95      # 特异度  P(-|无病)

# P(+|无病) = 1 - specificity
false_positive_rate = 1 - specificity  # 假阳性率 = 0.05

# 贝叶斯计算: P(病|+)
p_disease_positive = (sensitivity * prevalence) / (
    sensitivity * prevalence + false_positive_rate * (1 - prevalence)
)

print(f"患病率 P(病)            = {prevalence}")
print(f"灵敏度 P(+|病)          = {sensitivity}")
print(f"特异度 P(-|无病)        = {specificity}")
print(f"假阳性率 P(+|无病)      = {false_positive_rate}")
print(f"\n贝叶斯定理计算结果:")
print(f"  P(病|+) = {p_disease_positive:.4f} ≈ {p_disease_positive:.1%}")
print(f"\n解释: 即使检测阳性，真正患病的概率仅有 {p_disease_positive:.1%}")
print(f"这是因为患病率很低(1%)，大多数阳性结果是假阳性。")

# ============================================================
# 4. MLE 数值求解（MLE for Gaussian Mean & Variance）
# ============================================================
print("\n" + "=" * 65)
print("4. MLE 估计高斯分布的均值与方差")
print("=" * 65)

# 生成已知参数的真实数据
true_mu, true_sigma = 3.5, 1.2
np.random.seed(42)
data = np.random.randn(1000) * true_sigma + true_mu

# MLE 闭式解（对应章节 3.3 中的推导）
mu_mle = data.mean()
var_mle = data.var(ddof=0)  # 注意 ddof=0，即除以 n
sigma_mle = np.sqrt(var_mle)

# 无偏样本方差（分母 n-1）
var_unbiased = data.var(ddof=1)

print(f"真实参数: μ = {true_mu}, σ = {true_sigma}")
print(f"\nMLE 估计（基于 {len(data)} 个样本）:")
print(f"  μ̂_MLE   = {mu_mle:.4f}  (公式: (1/n) Σ x_i)")
print(f"  σ̂²_MLE  = {var_mle:.4f}  (公式: (1/n) Σ (x_i - μ̂)²)")
print(f"  σ̂_MLE   = {sigma_mle:.4f}")
print(f"\n无偏样本方差: S² = {var_unbiased:.4f}  (分母 n-1)")

# 数值 MLE 验证: 用 scipy 的 minimize 负对数似然
from scipy.optimize import minimize

def neg_log_likelihood(params, data):
    """负对数似然函数（Negative Log-Likelihood）"""
    mu, log_sigma = params  # 用 log(sigma) 保证 sigma > 0
    sigma = np.exp(log_sigma)
    n = len(data)
    # 对应推导中的 -ℓ(μ, σ²)
    nll = 0.5 * n * np.log(2 * np.pi) + \
          n * log_sigma + \
          (1 / (2 * sigma**2)) * np.sum((data - mu)**2)
    return nll

# 初始猜测
init_params = [0.0, 0.0]
result = minimize(neg_log_likelihood, init_params, args=(data,),
                  method='Nelder-Mead')

mu_numerical = result.x[0]
sigma_numerical = np.exp(result.x[1])

print(f"\n数值优化 MLE:")
print(f"  μ̂_MLE (数值) = {mu_numerical:.4f}  (闭式解: {mu_mle:.4f})")
print(f"  σ̂_MLE (数值) = {sigma_numerical:.4f}  (闭式解: {sigma_mle:.4f})")
print(f"  两者一致: {np.allclose([mu_numerical, sigma_numerical], [mu_mle, sigma_mle], atol=1e-3)}")

# ============================================================
# 5. 期望、方差、协方差的数值验证
# ============================================================
print("\n" + "=" * 65)
print("5. 期望、方差、协方差（Expectation, Variance, Covariance）")
print("=" * 65)

# 生成二维数据
np.random.seed(42)
n_points = 10000
X = np.random.randn(n_points) * 2.0 + 10.0           # μ_X=10, σ_X=2
Y = 3.0 * X + np.random.randn(n_points) * 1.0 + 5.0  # Y = 3X + 5 + noise

# 期望的线性性质验证: E[aX + bY] = aE[X] + bE[Y]
a, b = 2.0, 3.0
E_X = X.mean()
E_Y = Y.mean()
E_aX_plus_bY = (a * X + b * Y).mean()
formula_value = a * E_X + b * E_Y

print(f"期望的线性性质（Linearity of Expectation）:")
print(f"  E[X] = {E_X:.4f}")
print(f"  E[Y] = {E_Y:.4f}")
print(f"  E[{a}X + {b}Y] = {E_aX_plus_bY:.4f}  (公式: {formula_value:.4f})")
print(f"  验证通过: {np.allclose(E_aX_plus_bY, formula_value)}")

# 方差性质: Var[aX + b] = a² Var[X]
Var_X = X.var()
Var_2X = (2.0 * X).var()
print(f"\n方差性质（Variance Property）:")
print(f"  Var[X] = {Var_X:.4f}")
print(f"  Var[2X] = {Var_2X:.4f}  (公式: 4 * Var[X] = {4 * Var_X:.4f})")
print(f"  验证通过: {np.allclose(Var_2X, 4 * Var_X)}")

# 协方差与相关系数
Cov_XY = np.cov(X, Y, ddof=0)[0, 1]  # 总体协方差
rho = np.corrcoef(X, Y)[0, 1]

# 公式验证: Cov[X, Y] = E[XY] - E[X]E[Y]
Cov_formula = (X * Y).mean() - X.mean() * Y.mean()

print(f"\n协方差与相关系数（Covariance & Correlation）:")
print(f"  Cov[X, Y] = {Cov_XY:.4f}")
print(f"  Cov[X, Y] (公式 E[XY] - E[X]E[Y]) = {Cov_formula:.4f}")
print(f"  验证通过: {np.allclose(Cov_XY, Cov_formula)}")
print(f"  相关系数 ρ = {rho:.4f}  (强正相关，因为 Y ≈ 3X + 5)")

# 独立性 vs 不相关性说明
print(f"\n  注: ρ = {rho:.4f} ≈ 1，说明 X 与 Y 强相关。")
print(f"  反之，若 Cov = 0，则 X 与 Y 不相关，但不一定独立。")

# 全期望公式验证（Law of Total Expectation）
print("\n全期望公式（Law of Total Expectation）:")

# 构造一个分组数据集: 设 Z 为离散变量 {0, 1}
Z = np.random.binomial(1, 0.4, size=n_points)
# X 的分布依赖于 Z: Z=0 时 N(8,1), Z=1 时 N(12,1.5)
X_given_Z = np.where(Z == 0,
                     np.random.randn(n_points) * 1.0 + 8.0,
                     np.random.randn(n_points) * 1.5 + 12.0)

E_X_overall = X_given_Z.mean()

# E[X | Z=0] 和 E[X | Z=1]
E_X_given_Z0 = X_given_Z[Z == 0].mean()
E_X_given_Z1 = X_given_Z[Z == 1].mean()
p_Z0 = (Z == 0).mean()
p_Z1 = (Z == 1).mean()

# 全期望: E[X] = E[E[X|Z]] = E[X|Z=0]P(Z=0) + E[X|Z=1]P(Z=1)
E_total_expectation = E_X_given_Z0 * p_Z0 + E_X_given_Z1 * p_Z1

print(f"  E[X|Z=0] = {E_X_given_Z0:.4f},  P(Z=0) = {p_Z0:.4f}")
print(f"  E[X|Z=1] = {E_X_given_Z1:.4f},  P(Z=1) = {p_Z1:.4f}")
print(f"  整体 E[X] (直接)    = {E_X_overall:.4f}")
print(f"  整体 E[X] (全期望)  = {E_total_expectation:.4f}")
print(f"  验证通过: {np.allclose(E_X_overall, E_total_expectation)}")


# ============================================================
# 6. 可视化（Visualization）
# ============================================================
print("\n" + "=" * 65)
print("6. 可视化（Visualization）—— 分布 PDF / PMF 图")
print("=" * 65)
print("图形将自动弹出（如未弹出，检查后端设置）\n")

# 创建 2×2 的子图布局
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# --- 图 1: 伯努利分布 PMF ---
ax = axes[0, 0]
p_vis = 0.7
bern_vis = stats.bernoulli(p_vis)
x_discrete = [0, 1]
ax.bar(x_discrete, bern_vis.pmf(x_discrete), width=0.4, color='steelblue', alpha=0.8)
ax.set_title(f'伯努利分布 PMF (Bernoulli, p={p_vis})', fontsize=12)
ax.set_xlabel('x')
ax.set_ylabel('Probability')
ax.set_xticks([0, 1])
ax.set_ylim(0, 1)

# --- 图 2: 二项分布 PMF ---
ax = axes[0, 1]
n_vis, pn_vis = 10, 0.5
binom_vis = stats.binom(n_vis, pn_vis)
k_vals = np.arange(0, n_vis + 1)
ax.bar(k_vals, binom_vis.pmf(k_vals), width=0.6, color='coral', alpha=0.8)
ax.set_title(f'二项分布 PMF (Binomial, n={n_vis}, p={pn_vis})', fontsize=12)
ax.set_xlabel('k (成功次数)')
ax.set_ylabel('Probability')

# --- 图 3: 正态分布 PDF ---
ax = axes[1, 0]
mu_vis, s_vis = 5.0, 2.0
norm_vis = stats.norm(mu_vis, s_vis)
x_cont = np.linspace(mu_vis - 4*s_vis, mu_vis + 4*s_vis, 500)
ax.plot(x_cont, norm_vis.pdf(x_cont), 'b-', linewidth=2, label=f'N({mu_vis}, {s_vis}²)')
# 标注 μ ± σ, μ ± 2σ 区域
for k, color, label in [(1, 'red', '68%'), (2, 'green', '95%')]:
    ax.axvline(mu_vis - k*s_vis, color=color, linestyle='--', alpha=0.5)
    ax.axvline(mu_vis + k*s_vis, color=color, linestyle='--', alpha=0.5, label=f'μ±{k}σ ({label})')
ax.set_title('正态分布 PDF (Normal Distribution)', fontsize=12)
ax.set_xlabel('x')
ax.set_ylabel('Density')
ax.legend(fontsize=9)

# --- 图 4: 采样直方图 vs 理论 PDF ---
ax = axes[1, 1]
samples_vis = norm_vis.rvs(size=5000, random_state=42)
ax.hist(samples_vis, bins=50, density=True, alpha=0.6, color='purple', label='采样直方图')
ax.plot(x_cont, norm_vis.pdf(x_cont), 'k-', linewidth=2, label='理论 PDF')
ax.set_title('正态分布: 采样 vs 理论 PDF', fontsize=12)
ax.set_xlabel('x')
ax.set_ylabel('Density')
ax.legend(fontsize=9)

plt.tight_layout()
plt.savefig('/tmp/probability_distributions.png', dpi=100, bbox_inches='tight')
print(f"[保存] 分布图已保存至 /tmp/probability_distributions.png")
plt.show()

print("\n✅ 概率论演示完毕！（Probability Theory Demo Complete!）")
