# 05 — 无监督学习（Unsupervised Learning）

> **无监督学习（Unsupervised Learning）** 是在没有标签（labels）的情况下，从数据中发现隐藏结构的一类方法。与监督学习不同，我们只有输入 $X$，没有输出 $y$。目标可以是聚类（clustering）、降维（dimensionality reduction）或密度估计（density estimation）。
> > **时间线**:
> > - **1901**: Pearson 提出 PCA（主成分分析）
> > - **1957**: Lloyd 提出 K-Means 聚类算法（1982 年正式发表）
> - **2008**: van der Maaten & Hinton 提出 t-SNE 可视化算法
>
> **Unsupervised Learning** discovers hidden structure in data without labels. Unlike supervised learning, we only have inputs $X$ but no outputs $y$. Goals include clustering, dimensionality reduction, and density estimation.

**前置知识 (Prerequisites):** Vol 2 线性代数（SVD、特征分解）、概率论基础
**依赖库 (Dependencies):** `numpy`, `scikit-learn`, `matplotlib`

---

## 目录 (Table of Contents)

1. [K-Means 聚类 (K-Means Clustering)](#1-k-means-聚类-k-means-clustering)
2. [PCA 主成分分析 (Principal Component Analysis)](#2-pca-主成分分析-principal-component-analysis) 📐
3. [t-SNE 与 UMAP](#3-t-sne-与-umap)
4. [高斯混合模型 GMM (Gaussian Mixture Models)](#4-高斯混合模型-gmm-gaussian-mixture-models)

---

## 1. K-Means 聚类 (K-Means Clustering)

### 1.1 问题定义 (Problem Definition)

给定数据集 $\{\mathbf{x}_1, \mathbf{x}_2, \ldots, \mathbf{x}_m\}$，其中 $\mathbf{x}_i \in \mathbb{R}^n$，K-Means 的目标是将数据划分成 $k$ 个簇（clusters），使得每个点属于离它最近的簇中心（centroid）。

### 1.2 算法 (The Algorithm)

K-Means 是一个迭代式算法：

---

**Algorithm 1: K-Means 聚类**

1. **初始化**：随机（stochastic /stəˈkæstɪk/）选择 $k$ 个样本作为初始质心 $\{\boldsymbol{\mu}_1, \boldsymbol{\mu}_2, \ldots, \boldsymbol{\mu}_k\}$
2. **分配步骤 (Assignment Step)**：每个点分配给最近的质心

   $$c^{(i)} = \arg\min_j \|\mathbf{x}^{(i)} - \boldsymbol{\mu}_j\|_2^2$$

3. **更新步骤 (Update Step)**：重新计算每个簇的质心

   $$\boldsymbol{\mu}_j = \frac{1}{|\mathcal{C}_j|} \sum_{\mathbf{x}^{(i)} \in \mathcal{C}_j} \mathbf{x}^{(i)}$$

4. 重复步骤 2-3，直到收敛（质心不再变化或达到最大迭代次数）

---

**为什么 K-Means 保证收敛？** 算法的目标是最小化**惯性（inertia）**，即所有点到其所属簇中心的平方距离之和：

$$J = \sum_{j=1}^{k} \sum_{\mathbf{x}^{(i)} \in \mathcal{C}_j} \|\mathbf{x}^{(i)} - \boldsymbol{\mu}_j\|_2^2$$

- **分配步骤**中，每个点被分配给最近的质心 → $J$ **单调不增**
- **更新步骤**中，质心被更新为簇内所有点的均值 → 凸优化问题，$J$ **单调不增**

由于 $J$ 有下界（≥ 0），且每次迭代 $J$ 都不增加，所以算法一定收敛。

> **💡 理解收敛性:** 但 K-Means 只能保证收敛到**局部最优（local optimum）**，而非全局最优。不同的初始质心可能导致不同的最终结果。

### 1.3 局限性与改进 (Limitations & Improvements)

| 局限性 | 说明 | 改进方法 |
|:---|:---|:---|
| **假设球形簇** | K-Means 假设簇是各向同性的（isotropic） | 使用 GMM（见第 4 节） |
| **对初始值敏感** | 不同的初始值可能导致不同结果 | K-Means++ 初始化 |
| **需要指定 $k$** | 必须预先设定簇的数量 | 肘部法则（Elbow Method） |
| **对异常值敏感** | 均值对异常值不鲁棒 | 使用 K-Medoids |

### 1.4 肘部法则 (Elbow Method)

如何选择 $k$？肘部法则绘制不同 $k$ 对应的 inertia，寻找"肘部"：

$$\text{inertia}(k) = \sum_{j=1}^{k} \sum_{\mathbf{x} \in \mathcal{C}_j} \|\mathbf{x} - \boldsymbol{\mu}_j\|_2^2$$

随着 $k$ 增大，inertia 单调下降。当下降速度突然变缓时，对应的 $k$ 就是"肘部"——再增加簇数量收益很小。

```python
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=3, init='k-means++', n_init=10, random_state=42)
kmeans.fit(X)
labels = kmeans.labels_          # 每个点的簇分配
centroids = kmeans.cluster_centers_  # 质心坐标
inertia = kmeans.inertia_        # 最终 inertia 值
```

---

## 2. PCA 主成分分析 (Principal Component Analysis)

### 2.1 核心思想 (Core Idea)

PCA 寻找数据中**方差最大的方向（directions of maximum variance）**，将高维数据投影到低维子空间，同时尽可能保留数据的变异信息。

::: details 🔍 完整演算：协方差矩阵手算 — 4×3 数据集

**📐 公式**

协方差矩阵 (Covariance Matrix) 衡量数据集中每对特征之间的线性关系：

$$ \mathbf{C} = \frac{1}{n-1} \tilde{\mathbf{X}}^\top \tilde{\mathbf{X}} $$

其中 $\tilde{\mathbf{X}} = \mathbf{X} - \boldsymbol{\mu}$ 是中心化后的数据矩阵，$n$ 是样本数。

矩阵形式的完整定义：

$$ \mathbf{C} = \frac{1}{n-1} \sum_{i=1}^{n} (\mathbf{x}^{(i)} - \boldsymbol{\mu})(\mathbf{x}^{(i)} - \boldsymbol{\mu})^\top $$

即每个样本的外积（outer product）之和除以 $(n-1)$。

---

**📖 参数含义**

| 符号 | 名称 | 含义 |
|:---|:---|:---|
| $\mathbf{X} \in \mathbb{R}^{n \times d}$ | 数据矩阵 | $n$ 个样本，$d$ 个特征，本例 $n=4, d=3$ |
| $\tilde{\mathbf{X}}$ | 中心化数据矩阵 | 每列减去该列均值后的结果 |
| $\boldsymbol{\mu} \in \mathbb{R}^{d}$ | 均值向量 | 每个特征的样本均值 |
| $\mathbf{C} \in \mathbb{R}^{d \times d}$ | 协方差矩阵 | $C_{ij} = \text{Cov}(X_i, X_j)$，对称半正定矩阵 |
| $C_{ij}$ | 协方差 | 特征 $i$ 与特征 $j$ 之间的协方差；$i=j$ 时为方差 |

---

**📝 公式来源**

协方差矩阵的定义来自方差概念的推广。单个特征的方差为：

$$ \text{Var}(X) = E[(X - \mu)^2] = \frac{1}{n-1}\sum_{i=1}^{n}(x_i - \mu)^2 $$

将其推广到多个特征，就得到协方差矩阵：

$$ \text{Var}(\mathbf{X}) = E[(\mathbf{X} - \boldsymbol{\mu})(\mathbf{X} - \boldsymbol{\mu})^\top] $$

矩阵 $\tilde{\mathbf{X}}^\top \tilde{\mathbf{X}}$ 的每个元素 $(i,j)$ 恰好是特征 $i$ 和特征 $j$ 的中心化观测值的点积，除以 $(n-1)$ 后即为协方差。

> **协方差矩阵是 PCA 的起点**——它的特征向量指明了数据方差最大的方向，这是全书第一次出现这一核心概念。

---

**✏️ 手算演示**

给定数据集 $\mathbf{X} = \begin{bmatrix} 1 & 2 & 3 \\ 2 & 4 & 6 \\ 3 & 6 & 9 \\ 4 & 8 & 12 \end{bmatrix}$（4 个样本，3 个特征）

**Step 1: 计算列均值**

$$ \mu_1 = \frac{1+2+3+4}{4} = 2.5,\quad \mu_2 = \frac{2+4+6+8}{4} = 5,\quad \mu_3 = \frac{3+6+9+12}{4} = 7.5 $$

**Step 2: 中心化数据**（每列减去对应均值）

$$ \tilde{\mathbf{X}} = \begin{bmatrix}
-1.5 & -3 & -4.5 \\
-0.5 & -1 & -1.5 \\
0.5 & 1 & 1.5 \\
1.5 & 3 & 4.5
\end{bmatrix} $$

验证：每列之和为 $0$ ✓

**Step 3: 计算 $\tilde{\mathbf{X}}^\top \tilde{\mathbf{X}}$（外积和）**

$\tilde{\mathbf{X}}^\top \tilde{\mathbf{X}}$ 是 $3 \times 3$ 矩阵，第 $(i,j)$ 个元素是第 $i$ 列与第 $j$ 列的内积：

$$ \tilde{\mathbf{X}}^\top \tilde{\mathbf{X}}_{11} = (-1.5)^2 + (-0.5)^2 + 0.5^2 + 1.5^2 = 2.25 + 0.25 + 0.25 + 2.25 = 5 $$

$$ \tilde{\mathbf{X}}^\top \tilde{\mathbf{X}}_{12} = (-1.5)(-3) + (-0.5)(-1) + 0.5(1) + 1.5(3) = 4.5 + 0.5 + 0.5 + 4.5 = 10 $$

$$ \tilde{\mathbf{X}}^\top \tilde{\mathbf{X}}_{13} = (-1.5)(-4.5) + (-0.5)(-1.5) + 0.5(1.5) + 1.5(4.5) = 6.75 + 0.75 + 0.75 + 6.75 = 15 $$

$$ \tilde{\mathbf{X}}^\top \tilde{\mathbf{X}}_{22} = (-3)^2 + (-1)^2 + 1^2 + 3^2 = 9 + 1 + 1 + 9 = 20 $$

$$ \tilde{\mathbf{X}}^\top \tilde{\mathbf{X}}_{23} = (-3)(-4.5) + (-1)(-1.5) + 1(1.5) + 3(4.5) = 13.5 + 1.5 + 1.5 + 13.5 = 30 $$

$$ \tilde{\mathbf{X}}^\top \tilde{\mathbf{X}}_{33} = (-4.5)^2 + (-1.5)^2 + 1.5^2 + 4.5^2 = 20.25 + 2.25 + 2.25 + 20.25 = 45 $$

由对称性得 $\tilde{\mathbf{X}}^\top \tilde{\mathbf{X}}_{21} = \tilde{\mathbf{X}}^\top \tilde{\mathbf{X}}_{12} = 10$，$\tilde{\mathbf{X}}^\top \tilde{\mathbf{X}}_{31} = 15$，$\tilde{\mathbf{X}}^\top \tilde{\mathbf{X}}_{32} = 30$。因此：

$$ \tilde{\mathbf{X}}^\top \tilde{\mathbf{X}} = \begin{bmatrix} 5 & 10 & 15 \\ 10 & 20 & 30 \\ 15 & 30 & 45 \end{bmatrix} $$

**Step 4: 除以 $(n-1)$ 得到协方差矩阵**

$$ \mathbf{C} = \frac{1}{3} \tilde{\mathbf{X}}^\top \tilde{\mathbf{X}} =
\begin{bmatrix}
5/3 & 10/3 & 5 \\
10/3 & 20/3 & 10 \\
5 & 10 & 15
\end{bmatrix}
\approx
\begin{bmatrix}
1.667 & 3.333 & 5 \\
3.333 & 6.667 & 10 \\
5 & 10 & 15
\end{bmatrix} $$

**验证**：本例中 $X_2 = 2X_1$、$X_3 = 3X_1$，因此 $\text{Cov}(X_1,X_2) = 2 \times \text{Var}(X_1) = 2 \times \frac{5}{3} = \frac{10}{3}$ ✓，且 $\text{Cov}(X_1,X_3) = 3 \times \text{Var}(X_1) = 3 \times \frac{5}{3} = 5$ ✓。

---

**🌍 实际意义**

- **PCA 的基石**：协方差矩阵的特征分解直接给出主成分方向。特征值最大的特征向量对应数据方差最大的方向，这就是**全书第一次出现协方差矩阵**的原因——它是后续所有降维技术的数学起点
- **对角化**：PCA 的本质就是找到一组正交基，使得协方差矩阵在这组基下变为对角矩阵（各特征不再相关）
- **与 SVD 的关系**：$\mathbf{C} = \frac{1}{n-1} \mathbf{V} \boldsymbol{\Sigma}^\top \boldsymbol{\Sigma} \mathbf{V}^\top$，右奇异向量 $\mathbf{V}$ 就是特征向量，奇异值的平方对应特征值

:::

### 2.2 数学推导 (Mathematical Derivation) 📐

假设数据矩阵 $\mathbf{X} \in \mathbb{R}^{m \times n}$（$m$ 个样本，$n$ 个特征）。

**第一步：中心化（Center the data）**

$$\tilde{\mathbf{X}} = \mathbf{X} - \boldsymbol{\mu}, \quad \text{其中 } \boldsymbol{\mu}_j = \frac{1}{m}\sum_{i=1}^{m} \mathbf{X}_{ij}$$

**第二步：找到最大方差方向**

第一主成分 $\mathbf{w}_1$ 是单位向量，使得投影后的方差最大：

$$\mathbf{w}_1 = \arg\max_{\|\mathbf{w}\|=1} \frac{1}{m} \sum_{i=1}^{m} (\tilde{\mathbf{x}}^{(i)} \cdot \mathbf{w})^2 = \arg\max_{\|\mathbf{w}\|=1} \mathbf{w}^\top \mathbf{C} \mathbf{w}$$

其中 $\mathbf{C} = \frac{1}{m} \tilde{\mathbf{X}}^\top \tilde{\mathbf{X}}$ 是协方差矩阵。

可以证明：$\mathbf{w}_1$ 是 $\mathbf{C}$ 的最大特征值对应的**特征向量**。

**第三步：通过 SVD 实现（Connection to SVD）**

使用 SVD（参见 Vol 2 第 1 章第 4 节），我们**不需要显式构造协方差矩阵**：

$$\tilde{\mathbf{X}} = \mathbf{U} \boldsymbol{\Sigma} \mathbf{V}^\top$$

其中：
- $\mathbf{U} \in \mathbb{R}^{m \times m}$：左奇异向量
- $\boldsymbol{\Sigma} \in \mathbb{R}^{m \times n}$：奇异值矩阵（$\sigma_1 \geq \sigma_2 \geq \cdots \geq \sigma_r > 0$）
- $\mathbf{V} \in \mathbb{R}^{n \times n}$：右奇异向量

那么协方差矩阵为：

$$\mathbf{C} = \frac{1}{m} \tilde{\mathbf{X}}^\top \tilde{\mathbf{X}} = \frac{1}{m} \mathbf{V} \boldsymbol{\Sigma}^\top \boldsymbol{\Sigma} \mathbf{V}^\top$$

**PCA 的关键等价关系：**

| SVD 中的量 | PCA 中的含义 |
|:---|:---|
| 右奇异向量 $\mathbf{V}$ 的列 | **主成分方向（principal components）** |
| 奇异值 $\sigma_i$ | 对应方向的标准差（乘以 $\sqrt{m}$） |
| 矩阵 $\mathbf{U} \boldsymbol{\Sigma}$ | **主成分得分（principal component scores）** |

> **💡 为什么用 SVD 而不是协方差矩阵？** 计算 $\tilde{\mathbf{X}}^\top \tilde{\mathbf{X}}$ 会平方条件数（condition number），导致数值不稳定。SVD 直接作用于 $\tilde{\mathbf{X}}$，数值更稳定，且不需要在样本数很大时计算 $n \times n$ 的协方差矩阵。

### 2.3 PCA 算法步骤 (Algorithm Steps) 📐

1. 中心化数据 $\tilde{\mathbf{X}} = \mathbf{X} - \boldsymbol{\mu}$
2. 对 $\tilde{\mathbf{X}}$ 计算 SVD：$\tilde{\mathbf{X}} = \mathbf{U} \boldsymbol{\Sigma} \mathbf{V}^\top$
3. 取 $\mathbf{V}$ 的前 $k$ 列作为主成分方向：$\mathbf{W}_k = \mathbf{V}_{[:, :k]}$
4. 投影数据：$\mathbf{Z} = \tilde{\mathbf{X}} \mathbf{W}_k = \mathbf{U}_k \boldsymbol{\Sigma}_k$




### 2.4 应用场景 (Applications)

- **降维（Dimensionality Reduction）：** 用更少的特征训练模型，减少过拟合（overfitting /ˈoʊvərˈfɪtɪŋ/）
- **可视化（Visualization）：** 将高维数据投影到 2D/3D 平面
- **去噪（Noise Reduction）：** 丢弃小奇异值对应的成分可以滤除噪声
- **特征工程（Feature Engineering）：** PCA 成分可以作为新特征

### 2.5 保留方差比例 (Explained Variance Ratio) 📐

第 $i$ 个主成分解释的方差比例为：

$$r_i = \frac{\sigma_i^2}{\sum_{j=1}^{r} \sigma_j^2}$$

前 $k$ 个主成分累计解释的方差比例为 $\sum_{i=1}^{k} r_i$。通常选择 $k$ 使得累计方差比例达到 95%。

```python
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)           # 投影到 2D
explained_ratio = pca.explained_variance_ratio_  # 每个成分解释的方差比例
components = pca.components_            # 主成分方向（V 的列）
```

::: details 🔍 完整演算：保留方差比例手算

**📐 公式**

第 $i$ 个主成分解释的方差比例（Explained Variance Ratio）：

$$ r_i = \frac{\sigma_i^2}{\sum_{j=1}^{r} \sigma_j^2} $$

其中 $\sigma_i$ 是第 $i$ 个奇异值，$r = \min(m, n)$ 是非零奇异值的个数。

前 $k$ 个主成分的**累计方差比例**（Cumulative Explained Variance Ratio）：

$$ R_k = \sum_{i=1}^{k} r_i = \frac{\sum_{i=1}^{k} \sigma_i^2}{\sum_{j=1}^{r} \sigma_j^2} $$

---

**📖 参数含义**

| 符号 | 名称 | 含义 |
|:---|:---|:---|
| $\sigma_i$ | 第 $i$ 个奇异值 | 来自 $\tilde{\mathbf{X}} = \mathbf{U}\boldsymbol{\Sigma}\mathbf{V}^\top$，$\sigma_1 \geq \sigma_2 \geq \cdots$ |
| $\sigma_i^2$ | 特征值 | 等于协方差矩阵 $\mathbf{C}$ 的第 $i$ 大特征值 $\lambda_i$ |
| $r_i$ | 单成分方差比例 | 第 $i$ 个主成分解释的方差占总方差的比例 |
| $R_k$ | 累计方差比例 | 前 $k$ 个主成分累计解释的方差比例 |
| $r$ | 矩阵的秩 | 非零奇异值的个数（最多 $\min(m,n)$） |

---

**📝 公式来源**

协方差矩阵的迹（trace）等于总方差：

$$ \text{tr}(\mathbf{C}) = \sum_{i=1}^{n} C_{ii} = \sum_{i=1}^{n} \text{Var}(X_i) $$

由于协方差矩阵的特征值之和等于迹（$\sum \lambda_i = \text{tr}(\mathbf{C})$），且 $\lambda_i = \sigma_i^2$（忽略 $n-1$ 因子），因此：

$$ \text{总方差} = \sum \sigma_j^2 $$

第 $i$ 个主成分贡献的方差比例即为 $\sigma_i^2 / \sum \sigma_j^2$。

> **95% 经验法则**：通常选择最小的 $k$ 使得 $R_k \geq 0.95$，即保留 95% 以上的方差信息。这个阈值是降维中最常用的经验规则。

---

**✏️ 手算演示**

从 Box B 中我们已经得到奇异值：

$$ \sigma_1 = \sqrt{14} \approx 3.742,\quad \sigma_2 = 1 $$

**Step 1: 计算总方差**

$$ \sigma_1^2 + \sigma_2^2 = 14 + 1 = 15 $$

**Step 2: 计算各成分的方差比例**

第一主成分：

$$ r_1 = \frac{\sigma_1^2}{\sigma_1^2 + \sigma_2^2} = \frac{14}{15} \approx 0.933 \;(93.3\%) $$

第二主成分：

$$ r_2 = \frac{\sigma_2^2}{\sigma_1^2 + \sigma_2^2} = \frac{1}{15} \approx 0.067 \;(6.7\%) $$

**Step 3: 计算累计方差比例**

$$ R_1 = r_1 = \frac{14}{15} \approx 0.933 \;(93.3\%) $$

$$ R_2 = r_1 + r_2 = \frac{14}{15} + \frac{1}{15} = 1 \;(100\%) $$

**Step 4: 降维决策**

- 若按 **95% 阈值**：$R_1 = 93.3\% < 95\%$，需要保留 $k = 2$ 个主成分
- 若按 **90% 阈值**：$R_1 = 93.3\% > 90\%$，仅需保留 $k = 1$ 个主成分

---

**🌍 实际意义**

- **降维决策**：保留方差比例是选择 $k$ 的主要依据。典型阈值 95% 意味着我们接受 5% 的信息损失来换取维度的大幅降低
- **Scree Plot**：绘制 $r_i$ 的降序条形图（Scree Plot），寻找"肘部"——拐点之后的主成分贡献很小，可视为噪声
- **低秩数据**：如果前几个奇异值远大于其余，说明数据本质上是低秩的（low-rank），可以用很少的维度近似表示

:::

## 3. t-SNE 与 UMAP

### 3.1 为什么需要非线性降维？(Why Non-linear Dimensionality Reduction?)

PCA 是**线性**降维方法——它假设数据的主要变化方向是线性的。但现实数据往往位于复杂的**非线性流形（non-linear manifold）**上。例如，MNIST 手写数字在 784 维空间中位于一个高度弯曲的流形上，PCA 无法将其展开。

### 3.2 t-SNE (t-Distributed Stochastic Neighbor Embedding)

t-SNE 是一种**非线性**降维方法，特别擅长**可视化高维数据**。

**核（kernel /ˈkɜːrnl/）心思想：** 在高维空间中定义点之间的概率相似度，然后在低维空间中找到一个分布，使两者之间的 KL 散度（KL divergence）最小。

$$P_{j|i} = \frac{\exp(-\|\mathbf{x}_i - \mathbf{x}_j\|^2 / 2\sigma_i^2)}{\sum_{k \neq i} \exp(-\|\mathbf{x}_i - \mathbf{x}_k\|^2 / 2\sigma_i^2)}$$

在低维空间中，使用 **t-分布（Student's t-distribution）** 定义相似度（t-分布有更重的尾巴，可以避免"拥挤问题"）：

$$Q_{ij} = \frac{(1 + \|\mathbf{y}_i - \mathbf{y}_j\|^2)^{-1}}{\sum_{k \neq l} (1 + \|\mathbf{y}_k - \mathbf{y}_l\|^2)^{-1}}$$

优化目标（最小化 KL 散度）：

$$C = \sum_{i} \sum_{j} P_{j|i} \log \frac{P_{j|i}}{Q_{ij}}$$

### 3.3 UMAP (Uniform Manifold Approximation and Projection)

UMAP 是一个更新的方法，比 t-SNE 更快，且能更好地保留**全局结构（global structure）**。

| 特性 | t-SNE | UMAP |
|:---|:---|:---|
| **速度** | 较慢 ($O(n^2)$) | 更快（基于图论优化） |
| **全局结构** | 主要保留局部邻域 | 更好地保留全局结构 |
| **距离意义** | ❌ 簇间距离无意义 | ❌ 同样无意义 |
| **可扩展性** | 不适合大数据集 | 可扩展到百万级样本 |
| **理论基础** | 概率模型 | 基于黎曼几何和拓扑学 |

### 3.4 ⚠️ 重要警告 (Important Warnings)

**t-SNE 和 UMAP 仅用于可视化（visualization ONLY），不能用于特征提取或下游模型训练。** 原因：

1. **非确定性映射：** 每次运行结果不同
2. **距离无意义：** 特别是 t-SNE 中，簇之间的距离**不代表**高维空间中的真实距离
3. **无法泛化到新样本：** 需要重新运行整个算法
4. **超参数（hyperparameter /ˈhaɪpərpəˈræmɪtər/）敏感：** perplexity（/pərˈpleksəti/） 等参数（parameter /pəˈræmɪtər/）对结果影响很大

```python
from sklearn.manifold import TSNE

tsne = TSNE(n_components=2, perplexity=30, random_state=42)
X_tsne = tsne.fit_transform(X)  # 仅用于可视化！
```

---

## 4. 高斯混合模型 GMM (Gaussian Mixture Models)

### 4.1 从硬聚类到软聚类 (From Hard to Soft Clustering)

K-Means 是**硬聚类（hard clustering）**——每个点**唯一地**属于一个簇。但有时一个点可能"部分属于"多个簇。

**高斯混合模型（Gaussian Mixture Model, GMM）** 是**软聚类（soft clustering）**：每个点以不同的概率属于所有簇，这些概率之和为 1。

### 4.2 模型定义 (Model Definition)

GMM 假设数据由 $k$ 个高斯分布混合生成：

$$p(\mathbf{x}) = \sum_{j=1}^{k} \pi_j \, \mathcal{N}(\mathbf{x} \mid \boldsymbol{\mu}_j, \boldsymbol{\Sigma}_j)$$

其中：
- $\pi_j$ 是**混合权重（mixing coefficient）**，满足 $\sum_{j=1}^{k} \pi_j = 1$
- $\mathcal{N}(\boldsymbol{\mu}_j, \boldsymbol{\Sigma}_j)$ 是第 $j$ 个高斯分布的密度函数：
  
  $$\mathcal{N}(\mathbf{x} \mid \boldsymbol{\mu}, \boldsymbol{\Sigma}) = \frac{1}{(2\pi)^{n/2} |\boldsymbol{\Sigma}|^{1/2}} \exp\left(-\frac{1}{2} (\mathbf{x} - \boldsymbol{\mu})^\top \boldsymbol{\Sigma}^{-1} (\mathbf{x} - \boldsymbol{\mu})\right)$$

### 4.3 EM 算法直觉 (EM Algorithm Intuition)

GMM 的参数 $\{\pi_j, \boldsymbol{\mu}_j, \boldsymbol{\Sigma}_j\}_{j=1}^{k}$ 通过**期望最大化（Expectation-Maximization, EM）** 算法学习。

EM 是处理**隐变量（latent（/ˈleɪtənt/） variables）** 问题的一般框架。在 GMM 中，隐变量 $z^{(i)}$ 表示样本 $\mathbf{x}^{(i)}$ 来自哪个高斯成分。

**E 步（E-step）：** 估计每个点属于每个簇的概率（责任，responsibility）

$$\gamma_{ij} = p(z^{(i)} = j \mid \mathbf{x}^{(i)}) = \frac{\pi_j \, \mathcal{N}(\mathbf{x}^{(i)} \mid \boldsymbol{\mu}_j, \boldsymbol{\Sigma}_j)}{\sum_{l=1}^{k} \pi_l \, \mathcal{N}(\mathbf{x}^{(i)} \mid \boldsymbol{\mu}_l, \boldsymbol{\Sigma}_l)}$$

**M 步（M-step）：** 用加权最大似然估计更新参数

$$\boldsymbol{\mu}_j = \frac{\sum_{i=1}^{m} \gamma_{ij} \mathbf{x}^{(i)}}{\sum_{i=1}^{m} \gamma_{ij}}, \quad \boldsymbol{\Sigma}_j = \frac{\sum_{i=1}^{m} \gamma_{ij} (\mathbf{x}^{(i)} - \boldsymbol{\mu}_j)(\mathbf{x}^{(i)} - \boldsymbol{\mu}_j)^\top}{\sum_{i=1}^{m} \gamma_{ij}}, \quad \pi_j = \frac{1}{m} \sum_{i=1}^{m} \gamma_{ij}$$

> **💡 EM 迭代直觉:** E 步做"软分配"（就像 K-Means 的分配步骤，但这里是概率形式的），M 步用加权数据更新参数（就像 K-Means 更新质心，但每个点的贡献被加权）。

### 4.4 GMM vs K-Means

| 特性 | K-Means | GMM |
|:---|:---|:---|
| **聚类类型** | 硬聚类 | 软聚类（概率） |
| **簇形状** | 球形（各向同性） | 椭圆（任意协方差） |
| **参数** | 仅质心位置 | 均值、协方差、权重 |
| **算法** | Lloyd 迭代 | EM 算法 |
| **复杂度** | 简单快速 | 更慢但更灵活 |

```python
from sklearn.mixture import GaussianMixture

gmm = GaussianMixture(n_components=3, random_state=42)
gmm.fit(X)
probs = gmm.predict_proba(X)   # 每个点属于每个簇的概率 (m × k)
labels = gmm.predict(X)         # 最可能的簇分配
means = gmm.means_              # 每个成分的均值
covars = gmm.covariances_       # 每个成分的协方差矩阵
```

### 4.5 如何选择 $k$?

对于 GMM，可以使用**赤池信息量准则（AIC）** 或**贝叶斯信息量准则（BIC）** 来选择成分数量：

$$\text{AIC} = -2 \ln \hat{L} + 2d, \quad \text{BIC} = -2 \ln \hat{L} + d \ln m$$

其中 $d$ 是参数数量，$\hat{L}$ 是最大化似然值。AIC/BIC 越小越好。

---

## 本章总结 (Chapter Summary)

| 方法 | 类型 | 核心思想 | 输出 | 主要应用 |
|:---|:---|:---|:---|:---|
| **K-Means** | 聚类（硬） | 最小化 inertia | 簇分配 | 客户分群、图像分割 |
| **PCA** | 降维（线性） | 最大化方差方向 | 主成分 | 可视化、去噪、特征提取 |
| **t-SNE / UMAP** | 降维（非线性） | 保留邻域结构 | 2D/3D 嵌入（embedding /ɪmˈbedɪŋ/） | 🔍 仅用于可视化 |
| **GMM** | 聚类（软） | 概率混合模型 | 概率分配 | 密度估计、异常检测 |

### 关键概念速查 (Key Concepts)

| 概念 | 含义 |
|:---|:---|
| **Inertia** | 各点到所属簇中心的平方距离之和 |
| **Elbow Method** | 绘制 inertia-$k$ 曲线，选择拐点处的 $k$ |
| **K-Means++** | 智能初始化（让初始质心尽可能分散） |
| **Explained Variance Ratio** | 每个主成分解释的方差占比 $\sigma_i^2 / \sum \sigma_j^2$ |
| **KL 散度** | t-SNE 的优化目标，衡量两个分布之间的差异 |
| **Responsibility** | GMM 中一个点属于某个成分的后验概率 |
| **AIC / BIC** | 模型选择准则，平衡拟合度与复杂度 |

## 本章演算盒索引

| 位置 | 演算盒 | 跳转 |
|:---|:---|:---:|
| §2.2 | 🔍 协方差矩阵手算 — 4×3 数据集 | [跳转](#22-数学推导-mathematical-derivation) |
| §2.3 | 🔍 PCA via SVD 手算 — 4×2→1D | [跳转](#23-pca-算法步骤-algorithm-steps) |
| §2.5 | 🔍 保留方差比例手算 | [跳转](#25-保留方差比例-explained-variance-ratio) |

## 进一步阅读 (Further Reading)

- [scikit-learn: K-Means 文档](https://scikit-learn.org/stable/modules/clustering.html#k-means)
- [scikit-learn: PCA 文档](https://scikit-learn.org/stable/modules/decomposition.html#pca)
- [How to Use t-SNE Effectively (Distill.pub)](https://distill.pub/2016/misread-tsne/)
- [UMAP 论文 (McInnes et al., 2018)](https://arxiv.org/abs/1802.03426)
- [EM 算法深入理解 (Bishop PRML Ch 9)](https://www.microsoft.com/en-us/research/uploads/prod/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf)

---

<details>
<summary>🔍 完整演算：PCA via SVD 手算 - 4x2 到 1D 降维</summary>

**📐 公式**

PCA 通过对中心化数据矩阵的 SVD 实现降维：

$$ \tilde{\mathbf{X}} = \mathbf{U} \boldsymbol{\Sigma} \mathbf{V}^\top $$

其中 $\tilde{\mathbf{X}} \in \mathbb{R}^{m \times n}$。取前 $k$ 个右奇异向量作为主成分方向：

$$ \mathbf{W}_k = \mathbf{V}_{[:, :k]} $$

将数据投影到 $k$ 维子空间：

$$ \mathbf{Z} = \tilde{\mathbf{X}} \mathbf{W}_k = \mathbf{U}_k \boldsymbol{\Sigma}_k $$

---

**📖 参数含义**

| 符号 | 名称 | 含义 |
|:---|:---|:---|
| $\tilde{\mathbf{X}}$ | 中心化数据矩阵 | 每列减去均值后的 $m \times n$ 矩阵，本例 $m=4, n=2$ |
| $\mathbf{U} \in \mathbb{R}^{m \times m}$ | 左奇异向量矩阵 | 每列是 $\tilde{\mathbf{X}}\tilde{\mathbf{X}}^\top$ 的特征向量，反映样本在主方向上的关系 |
| $\boldsymbol{\Sigma} \in \mathbb{R}^{m \times n}$ | 奇异值矩阵 | 对角元素 $\sigma_i$ 为奇异值，$\sigma_1 \geq \sigma_2 \geq \cdots \geq 0$ |
| $\mathbf{V} \in \mathbb{R}^{n \times n}$ | 右奇异向量矩阵 | 每列是 $\tilde{\mathbf{X}}^\top\tilde{\mathbf{X}}$ 的特征向量 = **主成分方向** |
| $\mathbf{W}_k$ | 投影矩阵 | 前 $k$ 个主成分方向组成的 $n \times k$ 矩阵 |
| $\mathbf{Z} \in \mathbb{R}^{m \times k}$ | 主成分得分 | 数据在 $k$ 维子空间中的表示 |

---

**📝 公式来源**

SVD 与 PCA 的等价关系来自协方差矩阵的分解：

$$ \tilde{\mathbf{X}}^\top \tilde{\mathbf{X}} = (\mathbf{U}\boldsymbol{\Sigma}\mathbf{V}^\top)^\top(\mathbf{U}\boldsymbol{\Sigma}\mathbf{V}^\top) = \mathbf{V} \boldsymbol{\Sigma}^\top \boldsymbol{\Sigma} \mathbf{V}^\top $$

因此 $\tilde{\mathbf{X}}^\top \tilde{\mathbf{X}}$ 的特征分解等价于 $\mathbf{V} \boldsymbol{\Sigma}^2 \mathbf{V}^\top$，其中 $\boldsymbol{\Sigma}^2$ 由奇异值的平方（即特征值）构成。

**核心等价关系**：
- $\mathbf{V}$ 的列 = $\tilde{\mathbf{X}}^\top \tilde{\mathbf{X}}$ 的特征向量 = 主成分方向
- $\sigma_i^2$ = 第 $i$ 个主成分方向上的特征值（方差贡献）
- $\mathbf{U}\boldsymbol{\Sigma}$ 的列 = 主成分得分（投影后的坐标）

> **为什么用 SVD 更好？** 直接计算 $\tilde{\mathbf{X}}^\top \tilde{\mathbf{X}}$ 会平方条件数（condition number），导致数值不稳定。SVD 直接作用于 $\tilde{\mathbf{X}}$，数值更稳定且更高效。

---

**✏️ 手算演示**

给定数据集 $\mathbf{X} = \begin{bmatrix} 1 & 2 \\ 2 & 3 \\ 4 & 5 \\ 5 & 4 \end{bmatrix}$（4 个样本，2 个特征），目标：降至 1 维。

**Step 1: 中心化数据**

$$ \mu_1 = \frac{1+2+4+5}{4} = 3,\quad \mu_2 = \frac{2+3+5+4}{4} = 3.5 $$

$$ \tilde{\mathbf{X}} = \begin{bmatrix} -2 & -1.5 \\ -1 & -0.5 \\ 1 & 1.5 \\ 2 & 0.5 \end{bmatrix} $$

**Step 2: 计算 $\tilde{\mathbf{X}}^\top \tilde{\mathbf{X}}$**

$$ \tilde{\mathbf{X}}^\top \tilde{\mathbf{X}} = \begin{bmatrix} 4+1+1+4 & 3+0.5+1.5+1 \\ 3+0.5+1.5+1 & 2.25+0.25+2.25+0.25 \end{bmatrix} = \begin{bmatrix} 10 & 6 \\ 6 & 5 \end{bmatrix} $$

**Step 3: 求解特征值和特征向量**

特征方程：

$$ \det(\tilde{\mathbf{X}}^\top \tilde{\mathbf{X}} - \lambda \mathbf{I}) = \det\begin{bmatrix} 10-\lambda & 6 \\ 6 & 5-\lambda \end{bmatrix} = (10-\lambda)(5-\lambda) - 36 = 0 $$

$$ \lambda^2 - 15\lambda + 14 = 0 \implies (\lambda - 14)(\lambda - 1) = 0 $$

$$ \lambda_1 = 14,\quad \lambda_2 = 1 $$

奇异值：$\sigma_1 = \sqrt{14} \approx 3.742$，$\sigma_2 = 1$

**Step 4: 求右奇异向量（主成分方向）**

对于 $\lambda_1 = 14$：

$$ \begin{bmatrix} -4 & 6 \\ 6 & -9 \end{bmatrix} \begin{bmatrix} v_{11} \\ v_{21} \end{bmatrix} = \mathbf{0} \;\Longrightarrow\; -4v_{11} + 6v_{21} = 0 \;\Longrightarrow\; v_{11} = 1.5v_{21} $$

取 $v_{21} = 2$，得 $v_{11} = 3$。归一化：$\|\mathbf{v}_1\| = \sqrt{9 + 4} = \sqrt{13} \approx 3.606$

$$ \mathbf{v}_1 = \begin{bmatrix} 3/\sqrt{13} \\ 2/\sqrt{13} \end{bmatrix} \approx \begin{bmatrix} 0.832 \\ 0.555 \end{bmatrix} $$

对于 $\lambda_2 = 1$：

$$ \begin{bmatrix} 9 & 6 \\ 6 & 4 \end{bmatrix} \begin{bmatrix} v_{12} \\ v_{22} \end{bmatrix} = \mathbf{0} \;\Longrightarrow\; 9v_{12} + 6v_{22} = 0 \;\Longrightarrow\; v_{12} = -\frac{2}{3}v_{22} $$

取 $v_{22} = 3$，得 $v_{12} = -2$。归一化：$\|\mathbf{v}_2\| = \sqrt{4 + 9} = \sqrt{13}$

$$ \mathbf{v}_2 = \begin{bmatrix} -2/\sqrt{13} \\ 3/\sqrt{13} \end{bmatrix} \approx \begin{bmatrix} -0.555 \\ 0.832 \end{bmatrix} $$

因此：

$$ \mathbf{V} = \begin{bmatrix} 3/\sqrt{13} & -2/\sqrt{13} \\ 2/\sqrt{13} & 3/\sqrt{13} \end{bmatrix} $$

**Step 5: 取第一主成分（$k=1$）投影到 1 维子空间**

$$ \mathbf{w}_1 = \mathbf{v}_1 = \begin{bmatrix} 3/\sqrt{13} \\ 2/\sqrt{13} \end{bmatrix} $$

$$ \mathbf{Z} = \tilde{\mathbf{X}} \mathbf{w}_1 = \begin{bmatrix} -2 & -1.5 \\ -1 & -0.5 \\ 1 & 1.5 \\ 2 & 0.5 \end{bmatrix} \begin{bmatrix} 3/\sqrt{13} \\ 2/\sqrt{13} \end{bmatrix} = \frac{1}{\sqrt{13}} \begin{bmatrix} -9 \\ -4 \\ 6 \\ 7 \end{bmatrix} \approx \begin{bmatrix} -2.497 \\ -1.110 \\ 1.664 \\ 1.942 \end{bmatrix} $$

验证：$\mathbf{Z} = \mathbf{U}_1 \sigma_1$，其中 $\mathbf{U}_1$ 是 $\mathbf{U}$ 的第一列：

$$ \mathbf{U}_1 = \frac{\tilde{\mathbf{X}} \mathbf{v}_1}{\sigma_1} = \frac{1}{\sqrt{14}} \begin{bmatrix} -9/\sqrt{13} \\ -4/\sqrt{13} \\ 6/\sqrt{13} \\ 7/\sqrt{13} \end{bmatrix} = \begin{bmatrix} -9/\sqrt{182} \\ -4/\sqrt{182} \\ 6/\sqrt{182} \\ 7/\sqrt{182} \end{bmatrix} $$

---

**🌍 实际意义**

- **降维**：PCA 通过 SVD 将 $n$ 维数据投影到 $k$ 维子空间，保留最大方差方向（$k \ll n$）
- **去噪**：丢弃小奇异值对应的成分相当于滤除噪声——噪声通常在各方向上均匀分布，而信号集中在大奇异值方向
- **可视化的桥梁**：SVD 分解清晰地展示了"方向"（$\mathbf{V}$）、"强度"（$\boldsymbol{\Sigma}$）和"样本坐标"（$\mathbf{U}\boldsymbol{\Sigma}$）三个核心元素

</details>

> **下一章预告:** [模型评估与选择](./06-model-evaluation.md) — 交叉验证、偏差-方差权衡、ROC 曲线，用严谨的方法论评估 ML 模型。

## 参考文献 (References)

1. **Pearson, K.** (1901). On lines and planes of closest fit to systems of points in space. *Philosophical Magazine*, 2(11), 559–572. — PCA 的首次提出。
2. **Lloyd, S. P.** (1982). Least squares quantization in PCM. *IEEE Trans. Inform. Theory*, 28(2), 129–137. — K-Means 算法。
3. **van der Maaten, L. & Hinton, G.** (2008). Visualizing data using t-SNE. *JMLR*, 9, 2579–2605. — t-SNE 的提出。
