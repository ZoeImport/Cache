# 02 — 概率论与机器学习（Probability Theory for ML）

> 概率论（Probability Theory）是机器学习的核心语言。几乎所有 ML 算法——从线性回归的损失函数到贝叶斯推断，从随机梯度下降到生成模型——都建立在概率论的基础之上。本章从概率分布出发，逐步展开贝叶斯定理、最大似然估计（MLE）、最大后验估计（MAP）以及期望与方差等核心概念，为后续理解各类 ML 模型打下坚实的数学基础。

---

## 1. 概率分布（Probability Distributions）

### 1.1 随机变量（Random Variable）

**随机变量（Random Variable）** 是将随机试验的结果映射为数值的函数，分为两类：

| 类型 | 取值 | 示例 |
|:---|:---|:---|
| **离散型（Discrete）** | 可数有限个或可数无限个 | 硬币正面次数、骰子点数 |
| **连续型（Continuous）** | 某个区间内的任意实数 | 身高、温度、房价 |

### 1.2 概率质量函数（PMF）与概率密度函数（PDF）

- **PMF（Probability Mass Function）**：描述离散随机变量取某个特定值的概率，满足 $p(x) \ge 0$ 且 $\sum_x p(x) = 1$。
- **PDF（Probability Density Function）**：描述连续随机变量在某个点处的"密度"，满足 $f(x) \ge 0$ 且 $\int_{-\infty}^{\infty} f(x) \, dx = 1$。某区间内的概率为 PDF 在该区间上的积分：$P(a \le X \le b) = \int_a^b f(x) \, dx$。

### 1.3 伯努利分布（Bernoulli Distribution）

**伯努利分布（Bernoulli Distribution）** 建模**单次二值试验**的结果，如抛一次硬币是否正面朝上。

**参数**：$p \in [0, 1]$ —— 正面（$x=1$）的概率。

**PMF**：

$$p(x \mid p) = p^x (1 - p)^{1 - x}, \quad x \in \{0, 1\}$$

- 当 $x = 1$ 时，$p(1) = p$
- 当 $x = 0$ 时，$p(0) = 1 - p$

**期望与方差**：$\mathbb{E}[X] = p$, $\text{Var}[X] = p(1 - p)$

### 1.4 二项分布（Binomial Distribution）

**二项分布（Binomial Distribution）** 建模 $n$ 次独立同分布的伯努利试验中**成功次数**的分布。

**参数**：$n \in \mathbb{N}^+$（试验次数）, $p \in [0, 1]$（单次成功概率）。

**PMF**：

$$p(k \mid n, p) = \binom{n}{k} p^k (1 - p)^{n - k}, \quad k = 0, 1, \dots, n$$

其中 $\binom{n}{k} = \frac{n!}{k!(n-k)!}$ 是组合数（二项式系数）。

**期望与方差**：$\mathbb{E}[X] = np$, $\text{Var}[X] = np(1 - p)$

> **直觉**：二项分布是伯努利分布的"重复版本"。当 $n=1$ 时，二项分布退化为伯努利分布。

### 1.5 正态分布 / 高斯分布（Normal / Gaussian Distribution）

**正态分布（Normal Distribution）**，也称**高斯分布（Gaussian Distribution）**，是概率论中最核心的连续分布。中心极限定理（Central Limit Theorem）保证了大量独立随机变量之和趋近于正态分布，因此它在自然界和 ML 中无处不在。

**参数**：$\mu \in \mathbb{R}$（均值，Mean）, $\sigma^2 > 0$（方差，Variance），常记作 $\mathcal{N}(\mu, \sigma^2)$。

**PDF**：

$$f(x \mid \mu, \sigma^2) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left( -\frac{(x - \mu)^2}{2\sigma^2} \right)$$

**性质**：
- PDF 关于 $x = \mu$ 对称
- $\mu$ 控制分布的中心位置，$\sigma$ 控制分布的宽度（标准差，Standard Deviation）
- **68-95-99.7 法则**：约 68% 的数据落在 $\mu \pm \sigma$ 内，95% 在 $\mu \pm 2\sigma$ 内，99.7% 在 $\mu \pm 3\sigma$ 内

> **联系与区别**：伯努利和二项分布是**离散分布**，用于分类问题中的标签建模；正态分布是**连续分布**，广泛用于回归任务中的误差建模和参数初始化。

### 1.6 类别分布 / 多项分布（Categorical / Multinomial Distribution）

**类别分布（Categorical Distribution）** 是伯努利分布从 2 类到 $K$ 类的推广，建模单次 $K$ 值试验的结果（如掷 $K$ 面骰子）。**多项分布（Multinomial Distribution）** 则是 $n$ 次独立类别试验的联合分布。

**类别分布参数**：$\boldsymbol{\pi} = (\pi_1, \dots, \pi_K)$，满足 $\pi_k \ge 0$ 且 $\sum_{k=1}^K \pi_k = 1$。

**类别分布 PMF**：

$$p(x \mid \boldsymbol{\pi}) = \prod_{k=1}^K \pi_k^{\mathbb{I}[x = k]}$$

其中 $\mathbb{I}[\cdot]$ 是指示函数（Indicator Function）。

**多项分布 PMF**（$n$ 次试验，第 $k$ 类出现 $n_k$ 次）：

$$p(n_1, \dots, n_K \mid n, \boldsymbol{\pi}) = \frac{n!}{n_1! \cdots n_K!} \prod_{k=1}^K \pi_k^{n_k}$$

> 多项分布在 ML 中用于建模文本的词袋表示（Bag-of-Words）和分类问题的标签分布。

---

## 2. 条件概率与贝叶斯定理（Bayes' Theorem）

### 2.1 条件概率（Conditional Probability）

**条件概率** $P(A \mid B)$ 表示在事件 $B$ 已发生的条件下事件 $A$ 发生的概率：

$$P(A \mid B) = \frac{P(A \cap B)}{P(B)}, \quad P(B) > 0$$

**乘法定理**（Multiplication Rule）由上式直接可得：

$$P(A \cap B) = P(A \mid B) \, P(B) = P(B \mid A) \, P(A)$$

### 2.2 全概率公式（Law of Total Probability）

若事件 $B_1, B_2, \dots, B_K$ 构成样本空间的一个**划分**（即互不相交且并集为全集），则对任意事件 $A$：

$$P(A) = \sum_{k=1}^K P(A \mid B_k) \, P(B_k)$$

### 2.3 贝叶斯定理（Bayes' Theorem）

贝叶斯定理将**先验知识**与**观测数据**结合，得到**后验概率**：

$$P(B_i \mid A) = \frac{P(A \mid B_i) \, P(B_i)}{P(A)} = \frac{P(A \mid B_i) \, P(B_i)}{\sum_{j=1}^K P(A \mid B_j) \, P(B_j)}$$

在 ML 中，我们通常写成以下形式：

$$P(\theta \mid \mathcal{D}) = \frac{P(\mathcal{D} \mid \theta) \, P(\theta)}{P(\mathcal{D})}$$

其中：

| 符号 | 名称 | 含义 |
|:---|:---|:---|
| $P(\theta)$ | **先验（Prior）** | 观测数据之前，我们对参数 $\theta$ 的信念 |
| $P(\mathcal{D} \mid \theta)$ | **似然（Likelihood）** | 在参数 $\theta$ 下，数据 $\mathcal{D}$ 出现的概率 |
| $P(\mathcal{D})$ | **证据（Evidence）** | 数据出现的总概率（归一化常数） |
| $P(\theta \mid \mathcal{D})$ | **后验（Posterior）** | 观测数据之后，我们对 $\theta$ 更新的信念 |

> **推导**：由乘法定理，$P(\theta \cap \mathcal{D}) = P(\mathcal{D} \mid \theta) P(\theta) = P(\theta \mid \mathcal{D}) P(\mathcal{D})$，两边除以 $P(\mathcal{D})$ 即得上式。

### 2.4 经典案例：医学检测（Medical Test）

设某种疾病的患病率 $P(\text{病}) = 0.01$（先验）。检测方法的**灵敏度（Sensitivity）** $P(\text{+} \mid \text{病}) = 0.99$，**特异度（Specificity）** $P(\text{-} \mid \text{无病}) = 0.95$。

若一个人检测结果为阳性（+），其真正患病的概率是多少？

$$P(\text{病} \mid \text{+}) = \frac{P(\text{+} \mid \text{病}) \, P(\text{病})}{P(\text{+} \mid \text{病}) P(\text{病}) + P(\text{+} \mid \text{无病}) P(\text{无病})} = \frac{0.99 \times 0.01}{0.99 \times 0.01 + 0.05 \times 0.99} \approx 0.167$$

> **直觉**：即使检测灵敏度很高，由于患病率很低（1%），阳性结果的实际患病概率只有约 16.7%。这就是为什么大规模筛查中假阳性率不可忽视。

---

## 3. 最大似然估计 MLE（Maximum Likelihood Estimation）

### 3.1 核心思想

**最大似然估计（MLE, Maximum Likelihood Estimation）** 的核心问题是：给定观测数据 $\mathcal{D} = \{x_1, \dots, x_n\}$，**哪个参数 $\theta$ 最有可能生成这些数据？**

MLE 选择使**似然函数（Likelihood Function）** $P(\mathcal{D} \mid \theta)$ 最大的 $\theta$：

$$\hat{\theta}_{\text{MLE}} = \arg\max_\theta P(\mathcal{D} \mid \theta)$$

### 3.2 似然函数 vs 概率密度函数

两者在数学形式上相同，但视角不同：

- **PDF/PMF**：给定 $\theta$，描述数据 $x$ 的分布 —— 是 $x$ 的函数
- **似然**：给定观测数据 $\mathcal{D}$，描述参数 $\theta$ 的"解释能力" —— 是 $\theta$ 的函数

$$\mathcal{L}(\theta \mid \mathcal{D}) = P(\mathcal{D} \mid \theta)$$

### 3.3 MLE 实例：估计高斯分布的均值与方差

假设数据 $\{x_1, \dots, x_n\}$ 独立同分布（i.i.d.）于 $\mathcal{N}(\mu, \sigma^2)$。

**Step 1：写出似然函数**

$$P(\mathcal{D} \mid \mu, \sigma^2) = \prod_{i=1}^n \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left( -\frac{(x_i - \mu)^2}{2\sigma^2} \right)$$

**Step 2：取对数（Log-Likelihood）** —— 将乘积变为求和，便于求导

$$\ell(\mu, \sigma^2) = \log P(\mathcal{D} \mid \mu, \sigma^2) = -\frac{n}{2} \log(2\pi) - \frac{n}{2} \log(\sigma^2) - \frac{1}{2\sigma^2} \sum_{i=1}^n (x_i - \mu)^2$$

**Step 3：对 $\mu$ 求偏导并令其为零**

$$\frac{\partial \ell}{\partial \mu} = \frac{1}{\sigma^2} \sum_{i=1}^n (x_i - \mu) = 0 \quad \Rightarrow \quad \sum_{i=1}^n x_i - n\mu = 0 \quad \Rightarrow \quad \hat{\mu}_{\text{MLE}} = \frac{1}{n} \sum_{i=1}^n x_i$$

MLE 对均值的估计就是**样本均值（Sample Mean）**。

**Step 4：对 $\sigma^2$ 求偏导并令其为零**

$$\frac{\partial \ell}{\partial \sigma^2} = -\frac{n}{2} \cdot \frac{1}{\sigma^2} + \frac{1}{2(\sigma^2)^2} \sum_{i=1}^n (x_i - \mu)^2 = 0$$

$$\Rightarrow \quad \hat{\sigma}^2_{\text{MLE}} = \frac{1}{n} \sum_{i=1}^n (x_i - \hat{\mu}_{\text{MLE}})^2$$

> **注意**：$\hat{\sigma}^2_{\text{MLE}}$ 是**有偏估计（Biased Estimator）**，分母为 $n$ 而非 $n-1$。样本方差（Sample Variance）常用无偏估计 $S^2 = \frac{1}{n-1}\sum (x_i - \bar{x})^2$，分母 $n-1$ 来自自由度修正。

### 3.4 MLE 的一般步骤

1. 假设数据服从某个参数化分布 $P(x \mid \theta)$
2. 写出似然函数 $\mathcal{L}(\theta \mid \mathcal{D}) = \prod_{i=1}^n P(x_i \mid \theta)$
3. 取对数得到 Log-Likelihood $\ell(\theta)$
4. 对参数 $\theta$ 求偏导，令导数为零
5. 解出 $\hat{\theta}_{\text{MLE}}$（可能需要数值优化）

---

## 4. 最大后验估计 MAP（Maximum A Posteriori Estimation）

### 4.1 从 MLE 到 MAP

MLE 只关注数据拟合，但**当数据量少时，MLE 容易过拟合（Overfitting）**。MAP 引入**先验（Prior）** $P(\theta)$，结合数据的似然，最大化**后验概率**：

$$\hat{\theta}_{\text{MAP}} = \arg\max_\theta P(\theta \mid \mathcal{D}) = \arg\max_\theta \frac{P(\mathcal{D} \mid \theta) P(\theta)}{P(\mathcal{D})}$$

由于 $P(\mathcal{D})$ 与 $\theta$ 无关，等价于：

$$\hat{\theta}_{\text{MAP}} = \arg\max_\theta P(\mathcal{D} \mid \theta) P(\theta)$$

取对数形式：

$$\hat{\theta}_{\text{MAP}} = \arg\max_\theta \left[ \underbrace{\log P(\mathcal{D} \mid \theta)}_{\text{Log-Likelihood}} + \underbrace{\log P(\theta)}_{\text{Log-Prior}} \right]$$

### 4.2 MAP vs MLE

| 方面 | MLE | MAP |
|:---|:---|:---|
| 优化目标 | $\max \log P(\mathcal{D} \mid \theta)$ | $\max \big[ \log P(\mathcal{D} \mid \theta) + \log P(\theta) \big]$ |
| 先验信息 | 不使用 | 使用 |
| 数据量少时 | 容易过拟合 | 更稳健（Regularized） |
| 当先验为均匀分布 | — | MAP = MLE |
| 计算复杂度 | 较低 | 略高（需要额外乘先验） |

### 4.3 MAP 与正则化（Regularization）的联系

取高斯先验 $\theta \sim \mathcal{N}(0, \lambda^{-1})$，其对数形式为 $\log P(\theta) = -\frac{\lambda}{2} \theta^2 + \text{const}$。

MAP 的优化目标变为：

$$\hat{\theta}_{\text{MAP}} = \arg\max_\theta \left[ \log P(\mathcal{D} \mid \theta) - \frac{\lambda}{2} \theta^2 \right]$$

等价于最小化带 **L2 正则化（L2 Regularization）** 的负对数似然（Negative Log-Likelihood）：

$$\hat{\theta}_{\text{MAP}} = \arg\min_\theta \left[ -\log P(\mathcal{D} \mid \theta) + \frac{\lambda}{2} \|\theta\|^2 \right]$$

这正是**岭回归（Ridge Regression）** 的损失函数！类似地，拉普拉斯先验（Laplace Prior）对应 **L1 正则化（Lasso）**。

> **核心 insight**：从贝叶斯角度看，正则化不是人为的技巧，而是对参数施加先验分布的自然结果。

---

## 5. 期望、方差与协方差（Expectation, Variance, Covariance）

### 5.1 期望（Expectation / Expected Value）

**期望**是随机变量在概率意义上的"加权平均"。

| 类型 | 定义 | 公式 |
|:---|:---|:---|
| 离散型 | $\mathbb{E}[X] = \sum_{x} x \, p(x)$ | 每个可能值乘以其概率后求和 |
| 连续型 | $\mathbb{E}[X] = \int_{-\infty}^{\infty} x \, f(x) \, dx$ | 对 PDF 进行加权积分 |

**期望的线性性质（Linearity of Expectation）** —— 非常强大且常用：

$$\mathbb{E}[aX + bY] = a\,\mathbb{E}[X] + b\,\mathbb{E}[Y]$$

无论 $X$ 和 $Y$ 是否独立，这一性质都成立。

对函数的期望（Law of the Unconscious Statistician, LOTUS）：

$$\mathbb{E}[g(X)] = \begin{cases} \sum_x g(x) \, p(x), & \text{离散} \\ \int_{-\infty}^{\infty} g(x) \, f(x) \, dx, & \text{连续} \end{cases}$$

### 5.2 方差（Variance）

**方差**衡量随机变量围绕其均值的**离散程度**：

$$\text{Var}[X] = \mathbb{E}\left[ (X - \mathbb{E}[X])^2 \right] = \mathbb{E}[X^2] - (\mathbb{E}[X])^2$$

**标准差（Standard Deviation）**：$\sigma_X = \sqrt{\text{Var}[X]}$，与 $X$ 量纲相同。

**性质**：
- $\text{Var}[aX + b] = a^2 \, \text{Var}[X]$（常数平移不影响方差）
- $\text{Var}[X + Y] = \text{Var}[X] + \text{Var}[Y] + 2\,\text{Cov}[X, Y]$

### 5.3 协方差与相关系数（Covariance & Correlation）

**协方差（Covariance）** 衡量两个随机变量**共同变化**的程度：

$$\text{Cov}[X, Y] = \mathbb{E}\left[ (X - \mathbb{E}[X])(Y - \mathbb{E}[Y]) \right] = \mathbb{E}[XY] - \mathbb{E}[X] \mathbb{E}[Y]$$

**性质**：
- $\text{Cov}[X, X] = \text{Var}[X]$
- 若 $X$ 与 $Y$ 独立，则 $\text{Cov}[X, Y] = 0$（但反之不成立）
- $\text{Cov}[aX + b, cY + d] = ac \, \text{Cov}[X, Y]$

**相关系数（Correlation Coefficient）** 将协方差归一化到 $[-1, 1]$ 区间：

$$\rho_{X,Y} = \frac{\text{Cov}[X, Y]}{\sigma_X \sigma_Y}$$

- $\rho = 1$：完全正相关；$\rho = -1$：完全负相关；$\rho = 0$：不相关

### 5.4 协方差矩阵（Covariance Matrix）

对于 $D$ 维随机向量 $\mathbf{X} = (X_1, \dots, X_D)^\top$，协方差矩阵 $\Sigma$ 是一个 $D \times D$ 的对称半正定矩阵：

$$\Sigma_{ij} = \text{Cov}[X_i, X_j]$$

$$\Sigma = \mathbb{E}\left[ (\mathbf{X} - \mathbb{E}[\mathbf{X}])(\mathbf{X} - \mathbb{E}[\mathbf{X}])^\top \right]$$

协方差矩阵在 ML 中无处不在：
- **多元高斯分布（Multivariate Gaussian）** 的 PDF 直接使用 $\Sigma$
- **PCA** 对协方差矩阵做特征值分解
- **线性判别分析（LDA）** 使用类内协方差矩阵

### 5.5 全期望公式（Law of Total Expectation）

**全期望公式（Law of Total Expectation / Law of Iterated Expectations）** 是一个经常用到但容易被忽视的有用公式：

$$\mathbb{E}[X] = \mathbb{E}\big[ \mathbb{E}[X \mid Y] \big]$$

**含义**：整体期望 = 条件期望的期望。即先对每个 $Y$ 取值求条件期望，再对 $Y$ 的分布求加权平均。

**推导**（离散情况）：

$$\mathbb{E}\big[ \mathbb{E}[X \mid Y] \big] = \sum_y \mathbb{E}[X \mid Y=y] \, P(Y=y) = \sum_y \sum_x x \, P(X=x \mid Y=y) \, P(Y=y) = \sum_x x \sum_y P(X=x, Y=y) = \sum_x x \, P(X=x) = \mathbb{E}[X]$$

---

## 6. 本章小结

| 概念 | 要点 | ML 中的典型用途 |
|:---|:---|:---|
| **伯努利分布** | 单次二值试验，参数 $p$ | 二分类标签建模 |
| **二项分布** | $n$ 次独立伯努利试验的成功次数 | 评估指标（Accuracy 的分布） |
| **正态分布** | $\mathcal{N}(\mu, \sigma^2)$，中心极限定理 | 误差项、参数初始化、特征归一化 |
| **贝叶斯定理** | $P(\theta \mid \mathcal{D}) \propto P(\mathcal{D} \mid \theta) P(\theta)$ | 贝叶斯推断、朴素贝叶斯分类器 |
| **MLE** | $\max \log P(\mathcal{D} \mid \theta)$ | 线性回归、逻辑回归的参数估计 |
| **MAP** | $\max [\log \text{Likelihood} + \log \text{Prior}]$ | 带正则化的模型训练 |
| **期望** | 概率加权平均 $\mathbb{E}[X]$ | 损失函数（风险）的定义 |
| **方差/协方差** | 离散度 / 共变程度 | PCA、特征选择、正态分布参数 |

---

## 7. 进一步阅读

- [*Pattern Recognition and Machine Learning* — Christopher Bishop, Ch. 1-2](https://www.microsoft.com/en-us/research/uploads/prod/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf)
- [*The Elements of Statistical Learning* — Hastie et al., Ch. 2](https://hastie.su.domains/ElemStatLearn/)
- [scipy.stats 官方文档（Probability Distributions）](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [3Blue1Brown 贝叶斯定理可视化](https://www.youtube.com/watch?v=HZGCoVF3YvM)

---

*下一章：[03 — 信息论基础（Information Theory for ML）](./03-information-theory.md)*

*配套代码：[`probability_demo.py`](./code/probability_demo.py) — 分布可视化、贝叶斯计算、MLE 数值验证*
