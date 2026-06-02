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
2. [PCA 主成分分析 (Principal Component Analysis)](#2-pca-主成分分析-principal-component-analysis)
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

### 2.2 数学推导 (Mathematical Derivation)

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

### 2.3 PCA 算法步骤 (Algorithm Steps)

1. 中心化数据 $\tilde{\mathbf{X}} = \mathbf{X} - \boldsymbol{\mu}$
2. 对 $\tilde{\mathbf{X}}$ 计算 SVD：$\tilde{\mathbf{X}} = \mathbf{U} \boldsymbol{\Sigma} \mathbf{V}^\top$
3. 取 $\mathbf{V}$ 的前 $k$ 列作为主成分方向：$\mathbf{W}_k = \mathbf{V}_{[:, :k]}$
4. 投影数据：$\mathbf{Z} = \tilde{\mathbf{X}} \mathbf{W}_k = \mathbf{U}_k \boldsymbol{\Sigma}_k$

### 2.4 应用场景 (Applications)

- **降维（Dimensionality Reduction）：** 用更少的特征训练模型，减少过拟合（overfitting /ˈoʊvərˈfɪtɪŋ/）
- **可视化（Visualization）：** 将高维数据投影到 2D/3D 平面
- **去噪（Noise Reduction）：** 丢弃小奇异值对应的成分可以滤除噪声
- **特征工程（Feature Engineering）：** PCA 成分可以作为新特征

### 2.5 保留方差比例 (Explained Variance Ratio)

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

---

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

## 进一步阅读 (Further Reading)

- [scikit-learn: K-Means 文档](https://scikit-learn.org/stable/modules/clustering.html#k-means)
- [scikit-learn: PCA 文档](https://scikit-learn.org/stable/modules/decomposition.html#pca)
- [How to Use t-SNE Effectively (Distill.pub)](https://distill.pub/2016/misread-tsne/)
- [UMAP 论文 (McInnes et al., 2018)](https://arxiv.org/abs/1802.03426)
- [EM 算法深入理解 (Bishop PRML Ch 9)](https://www.microsoft.com/en-us/research/uploads/prod/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf)

---

> **下一章预告:** [模型评估与选择](./06-model-evaluation.md) — 交叉验证、偏差-方差权衡、ROC 曲线，用严谨的方法论评估 ML 模型。

## 参考文献 (References)

1. **Pearson, K.** (1901). On lines and planes of closest fit to systems of points in space. *Philosophical Magazine*, 2(11), 559–572. — PCA 的首次提出。
2. **Lloyd, S. P.** (1982). Least squares quantization in PCM. *IEEE Trans. Inform. Theory*, 28(2), 129–137. — K-Means 算法。
3. **van der Maaten, L. & Hinton, G.** (2008). Visualizing data using t-SNE. *JMLR*, 9, 2579–2605. — t-SNE 的提出。
