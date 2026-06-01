# 05 — 统计基础（Statistical Foundations for ML）

> 机器学习（Machine Learning）的核心任务是从数据中学习规律，而**统计（Statistics）** 提供了描述不确定性（Uncertainty）和从样本推断总体（Inference from Samples）的理论框架。本章聚焦于 ML 中最常用的统计概念：偏差-方差权衡（Bias-Variance Tradeoff）、参数估计（Parameter Estimation）、假设检验基础（Hypothesis Testing）和 Bootstrap 重采样（Bootstrap Resampling）。**偏差-方差权衡是本章的重中之重**，它是理解过拟合（Overfitting）与欠拟合（Underfitting）的统计根源。

---

## 1. 偏差-方差权衡（Bias-Variance Tradeoff）

### 1.1 动机：为什么模型会犯错？

假设我们有一个真实的数据生成过程（Data Generating Process, DGP）：

$$Y = f(X) + \varepsilon, \quad \varepsilon \sim \mathcal{N}(0, \sigma^2)$$

其中 $\varepsilon$ 是**不可约减的噪声（Irreducible Error）**——即使我们知道了真实的 $f(X)$，预测依然会有 $\sigma^2$ 的误差。我们的目标是学到一个 $\hat{f}(X)$ 来近似 $f(X)$。

对于一个新样本 $x_0$，期望的预测误差（Expected Test Error）可以分解为三个部分：

### 1.2 数学推导

我们使用**均方误差（Mean Squared Error, MSE）** 作为损失函数。对于固定的 $x_0$：

$$
\begin{aligned}
\text{MSE}(x_0) &= \mathbb{E}\left[\bigl(Y_0 - \hat{f}(x_0)\bigr)^2 \mid X = x_0\right] \\
&= \mathbb{E}\left[\bigl(f(x_0) + \varepsilon - \hat{f}(x_0)\bigr)^2\right] \\
&= \underbrace{\bigl(f(x_0) - \mathbb{E}[\hat{f}(x_0)]\bigr)^2}_{\text{Bias}^2}
+ \underbrace{\mathbb{E}\bigl[\bigl(\hat{f}(x_0) - \mathbb{E}[\hat{f}(x_0)]\bigr)^2\bigr]}_{\text{Variance}}
+ \underbrace{\sigma^2}_{\text{Irreducible Error}}
\end{aligned}
$$

**推导要点**：令 $\bar{f}(x_0) = \mathbb{E}[\hat{f}(x_0)]$，则：

$$
\begin{aligned}
\mathbb{E}[(Y - \hat{f})^2] &= \mathbb{E}[(f + \varepsilon - \hat{f})^2] \\
&= \mathbb{E}[(f - \bar{f} + \bar{f} - \hat{f} + \varepsilon)^2] \\
&= \mathbb{E}[(f - \bar{f})^2] + \mathbb{E}[(\bar{f} - \hat{f})^2] + \mathbb{E}[\varepsilon^2] \\
&\quad + 2\mathbb{E}[(f - \bar{f})(\bar{f} - \hat{f})] + 2\mathbb{E}[(f - \bar{f})\varepsilon] + 2\mathbb{E}[(\bar{f} - \hat{f})\varepsilon]
\end{aligned}
$$

交叉项消去（$\mathbb{E}[\bar{f} - \hat{f}] = 0$，$\varepsilon$ 独立于 $\hat{f}$），我们得到：

$$\text{Expected Test Error} = \text{Bias}^2 + \text{Variance} + \text{Irreducible Error}$$

### 1.3 三种成分的含义

| 成分 | 含义 | 来源 |
|:---|:---|:---|
| **Bias²（偏差）** | 模型预测的期望值与真实值的差距 | 模型假设过于简单（如用线性模型拟合非线性数据） |
| **Variance（方差）** | 模型对不同训练集的敏感程度 | 模型过于复杂（对训练数据的噪声也"记住"了） |
| **Irreducible Error（不可约误差）** | 数据本身固有的噪声 | 无法通过任何模型消除 |

### 1.4 多项式回归示例

用一个经典例子来说明：假设真实函数为 $f(x) = \sin(x)$，我们分别用**一次（线性）**、**三次**和**十次**多项式进行拟合：

- **度=1（欠拟合，Underfitting）**：模型太简单，无法捕捉 $\sin(x)$ 的波动 → **高偏差（High Bias）**，预测与真实值系统性偏离。
- **度=3（适中）**：较好地平衡了偏差和方差。
- **度=10（过拟合，Overfitting）**：模型完美拟合了训练点，但极度不稳定 → **高方差（High Variance）**，稍微改变训练集，预测曲线就会剧烈变化。

```
预测误差随模型复杂度的变化趋势：

Error
  ↑
  |   Total Error (测试误差)
  |      ╱╲
  |     ╱  ╲         Variance² (方差)
  |    ╱    ╲       ╱
  |   ╱      ╲     ╱
  |  ╱        ╲   ╱
  | ╱          ╲ ╱
  |╱            Bias² (偏差²)
  └──────────────────────→ 模型复杂度
```

> **核心直觉（Key Intuition）**：偏差和方差之间存在**权衡（Tradeoff）**。降低偏差通常会升高方差，反之亦然。最优模型处于两者平衡点。这是为什么我们既不能选过简单的模型（高偏差/欠拟合），也不能选过复杂的模型（高方差/过拟合）。

### 1.5 与正则化的联系

**正则化（Regularization）**（如 L1/L2 正则化）的本质就是在偏差-方差权衡中主动引入**少量偏差**来换取**方差的大幅下降**：

$$ \text{Loss} = \text{MSE} + \lambda \|\theta\|^2 $$

当 $\lambda$ 增大时，参数被往 0 方向压缩（增加偏差），但模型对训练集的波动更不敏感（降低方差）。

---

## 2. 参数估计（Parameter Estimation）

### 2.1 点估计（Point Estimation）

点估计的目标是用样本数据估计总体分布的某个参数 $\theta$（如均值 $\mu$、方差 $\sigma^2$）。

最常用的方法是**极大似然估计（Maximum Likelihood Estimation, MLE）**：

$$\hat{\theta}_{\text{MLE}} = \arg\max_{\theta} \prod_{i=1}^{n} p(x_i \mid \theta)$$

对于正态分布 $\mathcal{N}(\mu, \sigma^2)$，MLE 给出：

$$\hat{\mu} = \frac{1}{n}\sum_{i=1}^{n} x_i = \bar{x}, \quad \hat{\sigma}^2 = \frac{1}{n}\sum_{i=1}^{n} (x_i - \bar{x})^2$$

> ⚠️ 注意：$\hat{\sigma}^2_{\text{MLE}}$ 是有偏的（Biased）。无偏估计使用 $n-1$ 作为分母（Bessel's correction）：
> $$s^2 = \frac{1}{n-1}\sum_{i=1}^{n} (x_i - \bar{x})^2$$

### 2.2 估计量的性质

一个好的估计量通常满足：

| 性质 | 定义 | 公式 |
|:---|:---|:---|
| **无偏性（Unbiasedness）** | 期望值等于真实参数 | $\mathbb{E}[\hat{\theta}] = \theta$ |
| **一致性（Consistency）** | 样本量增大时依概率收敛到真实值 | $\hat{\theta} \xrightarrow{p} \theta$ |
| **有效性（Efficiency）** | 在所有无偏估计中方差最小 | $\text{Var}(\hat{\theta}) \leq \text{Var}(\tilde{\theta})$ |

### 2.3 抽样分布（Sampling Distribution）

**样本均值的抽样分布**是大数定律（Law of Large Numbers）和中心极限定理（Central Limit Theorem, CLT）的直接结果：

$$\bar{X} \sim \mathcal{N}\left(\mu, \frac{\sigma^2}{n}\right) \quad \text{（当 $n$ 足够大时）}$$

这意味着：
- 样本均值 $\bar{x}$ 是总体均值 $\mu$ 的无偏估计量
- 估计的不确定性随 $\frac{1}{\sqrt{n}}$ 衰减——要减半误差区间，需要四倍样本量
- **标准误（Standard Error）**：$\text{SE}(\bar{x}) = \frac{\sigma}{\sqrt{n}}$

### 2.4 置信区间（Confidence Interval）

**置信区间（Confidence Interval, CI）** 给出了参数估计的范围。一个 $95\%$ 的置信区间意味着：如果重复采样并计算区间很多次，大约 $95\%$ 的区间会包含真实参数。

对于总体均值 $\mu$，当 $\sigma$ 已知时：

$$95\%\ \text{CI} = \bar{x} \pm 1.96 \times \frac{\sigma}{\sqrt{n}}$$

当 $\sigma$ 未知时（更常见），使用 **t 分布（t-Distribution）**：

$$95\%\ \text{CI} = \bar{x} \pm t_{n-1, 0.025} \times \frac{s}{\sqrt{n}}$$

> **直觉**：置信区间回答了"我们的估计有多靠谱？"这个问题。区间越窄，估计越精确。

---

## 3. 假设检验基础（Hypothesis Testing）

> 本节仅提供直觉理解，不做数理统计课的全面展开。

### 3.1 基本框架

假设检验（Hypothesis Testing）是一个决策框架：

1. **原假设（Null Hypothesis, $H_0$）**：通常代表"无效果"或"无差异"的默认立场。例如：$\mu = 0$
2. **备择假设（Alternative Hypothesis, $H_1$）**：代表我们试图证明的结论。例如：$\mu \neq 0$
3. **检验统计量（Test Statistic）**：从样本计算的一个数值，用于衡量数据与原假设的偏离程度
4. **p 值（p-value）**：在原假设成立的前提下，观察到当前或更极端结果的概率

### 3.2 p 值的含义

**p 值**是最被广泛使用也最容易被误解的统计概念之一：

- ✅ **正确理解**：p 值是在 $H_0$ 为真的条件下，观测到当前结果的概率。
- ❌ **常见误解**：p 值是 $H_0$ 为真的概率。（这是错误的！）

**判断规则**：当 p 值小于显著性水平（Significance Level）$\alpha$（通常为 0.05）时，我们**拒绝原假设（Reject $H_0$）**。

### 3.3 两类错误

| 决策 | $H_0$ 为真 | $H_0$ 为假 |
|:---|:---|:---|
| 不拒绝 $H_0$ | ✅ 正确 | ❌ **Type II Error（$\beta$）**：漏报（False Negative） |
| 拒绝 $H_0$ | ❌ **Type I Error（$\alpha$）**：误报（False Positive） | ✅ 正确 |

- **Type I Error（第一类错误 / 误报）**："假阳性"。你声称发现了效果，但实际没有。例如：新药测试说有效，其实无效。
- **Type II Error（第二类错误 / 漏报）**："假阴性"。你没发现真实存在的效果。例如：新药测试说无效，其实有效。

> **机器学习视角**：在 ML 中，我们很少做正式的假设检验，但**交叉验证（Cross-Validation）** 本质上承担了类似角色——检验模型在未见数据上是否有显著的表现。

---

## 4. Bootstrap 重采样（Bootstrap Resampling）

### 4.1 什么是 Bootstrap？

**Bootstrap（自助法）** 是一种通过**有放回重采样（Resampling with Replacement）** 来估计统计量不确定性的方法。它由 Bradley Efron 在 1979 年提出，是现代统计学的一大突破。

**核心思想**：如果样本是总体的良好代表，那么**从样本中有放回地反复抽样**可以模拟"从总体中反复采样"的过程。

### 4.2 Bootstrap 算法

给定样本 $X = \{x_1, x_2, \dots, x_n\}$，我们要估计某个统计量 $\theta$（如均值、中位数、方差）的分布：

1. 从 $X$ 中有放回地抽取 $n$ 个样本，得到 Bootstrap 样本 $X^{*1}$
2. 计算该样本的统计量 $\hat{\theta}^{*1}$
3. 重复 B 次（通常 B = 1000 或 10000），得到 $\{\hat{\theta}^{*1}, \hat{\theta}^{*2}, \dots, \hat{\theta}^{*B}\}$
4. 用这些值的分布来估计 $\hat{\theta}$ 的不确定性

```python
# Bootstrap 伪代码
import numpy as np

def bootstrap_ci(data, statistic=np.mean, n_bootstrap=10000, ci=95):
    boot_stats = []
    n = len(data)
    for _ in range(n_bootstrap):
        sample = np.random.choice(data, size=n, replace=True)
        boot_stats.append(statistic(sample))
    
    lower = (100 - ci) / 2
    upper = 100 - lower
    return np.percentile(boot_stats, [lower, upper])
```

### 4.3 Bootstrap 置信区间

用 Bootstrap 估计均值的置信区间：

1. 计算 B 个 Bootstrap 样本的均值
2. 取这些均值的 $\alpha/2$ 和 $1-\alpha/2$ 分位数作为置信上下限

这被称为**百分位 Bootstrap 区间（Percentile Bootstrap Interval）**，无需对数据分布做任何假设（非参数化，Non-parametric）。

### 4.4 Bootstrap 的优势

| 特性 | Bootstrap | 传统方法 |
|:---|:---|:---|
| **分布假设** | 不需要（非参数） | 需要正态性假设 |
| **适用统计量** | 任意（均值、中位数、方差、分位数……） | 仅限有解析解的统计量 |
| **样本量要求** | 可以较小 | 需要足够大的样本（CLT 生效） |
| **计算成本** | 高（B 次重采样计算） | 低（一次计算） |

### 4.5 与 ML 的联系

Bootstrap 在 ML 中有直接的应用：

- **Bagging（Bootstrap Aggregating）**：用 Bootstrap 生成多个训练集，训练多个模型，然后平均它们的预测。这正是**随机森林（Random Forest）** 的核心机制。
- **评估模型稳定性**：Bootstrap 可以评估同一个模型在不同训练集上的预测方差。
- **超参数选择**：Bootstrap 可以用来估计不同超参数配置下模型性能的置信区间。

> **从 Bootstrap 到 Bagging 的跨越**：Bootstrap 估计的是"统计量的不确定性"，Bagging 估计的是"模型预测的不确定性"。后者正是下一卷（经典机器学习）中集成方法（Ensemble Methods）的起点。

---

## 本章小结

| 概念 | 要点 |
|:---|:---|
| **Bias-Variance Tradeoff** | 期望测试误差 = Bias² + Variance + Irreducible Error；过拟合 ↔ 高方差，欠拟合 ↔ 高偏差 |
| **参数估计** | MLE 是核心方法；样本均值的标准误 $\text{SE} = \sigma/\sqrt{n}$；置信区间量化不确定性 |
| **假设检验** | p 值不是 $H_0$ 为真的概率；Type I = 误报，Type II = 漏报 |
| **Bootstrap** | 有放回重采样 + B 次计算 → 任意统计量的经验分布；直接引向 Bagging/Random Forest |

---

## 进一步阅读

- [《An Introduction to Statistical Learning》—— Gareth James 等（ISLR 第 2 章：偏差-方差权衡）](https://www.statlearning.com/)
- [《The Elements of Statistical Learning》—— Hastie, Tibshirani, Friedman（第 7 章：模型评估与选择）](https://hastie.su.domains/ElemStatLearn/)
- [Efron 的 Bootstrap 原始论文：Bootstrap Methods: Another Look at the Jackknife (1979)](https://projecteuclid.org/journals/annals-of-statistics/volume-7/issue-1/Bootstrap-Methods-Another-Look-at-the-Jackknife/10.1214/aos/1176344552.full)
- [scikit-learn 文档：偏差-方差权衡](https://scikit-learn.org/stable/modules/learning_curve.html)

---

*下一章：[06 — 概率论基础](./06-probability-basics.md)*
