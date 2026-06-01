# 第1章 线性代数 — 机器学习之基石
# Chapter 1: Linear Algebra — The Foundation of Machine Learning

> **线性代数是机器学习的数学语言。** 从数据表示（向量/矩阵）到模型训练（梯度/优化），再到高级技术（PCA/降维），线性代数贯穿始终。本章只讲 **ML 最必需的** 主题，确保你理解几何直觉之后再接触数学公式，并用 NumPy 逐一验证。

> **Linear Algebra is the language of Machine Learning.** From data representation (vectors/matrices) to model training (gradients/optimization) and advanced techniques (PCA/dimensionality reduction), linear algebra is everywhere. This chapter covers only **ML-essential** topics — geometric intuition first, mathematics second, NumPy verification always.

**前置知识 (Prerequisites):** 高中数学（向量基本概念、函数求导）
**依赖库 (Dependencies):** `numpy`, `scipy`, `matplotlib`

---

## 目录 (Table of Contents)

1. [向量与向量空间 (Vectors & Vector Spaces)](#1-向量与向量空间-vectors--vector-spaces)
2. [矩阵及其运算 (Matrix Operations)](#2-矩阵及其运算-matrix-operations)
3. [特征值与特征向量 (Eigenvalues & Eigenvectors)](#3-特征值与特征向量-eigenvalues--eigenvectors)
4. [奇异值分解 SVD (Singular Value Decomposition)](#4-奇异值分解-svd-singular-value-decomposition)
5. [矩阵微积分 (Matrix Calculus)](#5-矩阵微积分-matrix-calculus)

---

## 1. 向量与向量空间 (Vectors & Vector Spaces)

### 1.1 几何直觉 (Geometric Intuition)

向量是**既有大小又有方向的量**。在二维平面上，一个向量可以看作从原点指向某点的箭头：

$$ \mathbf{v} = \begin{bmatrix} 3 \\ 2 \end{bmatrix} $$

这个箭头在 $x$ 方向走了 3 步，在 $y$ 方向走了 2 步。三维及以上同理。

**为什么 ML 需要向量？** 在机器学习中，**每个样本（sample）就是一个向量**。例如：
- 房价预测：`[面积, 卧室数, 楼层, 房龄]` → 4 维向量
- 图像识别：一张 28×28 像素的灰度图 → 784 维向量
- NLP：一个词 "apple" → 300 维词向量 (word embedding)

### 1.2 数学定义 (Mathematical Definition)

**定义 1 (向量):** 向量 $\mathbf{v} \in \mathbb{R}^n$ 是 $n$ 个有序实数的元组：

$$ \mathbf{v} = \begin{bmatrix} v_1 \\ v_2 \\ \vdots \\ v_n \end{bmatrix} $$

**定义 2 (向量空间):** 向量空间 $\mathbb{R}^n$ 是所有 $n$ 维向量的集合，在加法和数乘下封闭：
- 加法封闭：$\mathbf{u} + \mathbf{v} \in \mathbb{R}^n$
- 数乘封闭：$c \cdot \mathbf{v} \in \mathbb{R}^n$ (对任意 $c \in \mathbb{R}$)

### 1.3 点积 (Dot Product)

两个同维度向量的点积是 ML 中最基本的运算之一：

$$ \mathbf{u} \cdot \mathbf{v} = \sum_{i=1}^{n} u_i v_i = u_1 v_1 + u_2 v_2 + \cdots + u_n v_n $$

**几何意义:** $\mathbf{u} \cdot \mathbf{v} = \|\mathbf{u}\| \|\mathbf{v}\| \cos \theta$，其中 $\theta$ 是两个向量间的夹角。

- $\mathbf{u} \cdot \mathbf{v} > 0$ → 夹角 < 90° (方向相近)
- $\mathbf{u} \cdot \mathbf{v} = 0$ → 夹角 = 90° (正交/垂直)
- $\mathbf{u} \cdot \mathbf{v} < 0$ → 夹角 > 90° (方向相反)

**在 ML 中的应用:** 注意力机制 (Attention) 的核心就是计算 query 与 key 的点积来衡量相似度。

### 1.4 范数 (Norm)

**定义 3 ($L^p$ 范数):** 向量 $\mathbf{v}$ 的 $L^p$ 范数定义为：

$$ \|\mathbf{v}\|_p = \left( \sum_{i=1}^{n} |v_i|^p \right)^{1/p} $$

最常用的两种：

**$L^2$ 范数（欧几里得范数）:** 就是向量的"长度"：

$$ \|\mathbf{v}\|_2 = \sqrt{v_1^2 + v_2^2 + \cdots + v_n^2} $$

**$L^1$ 范数（曼哈顿范数）:** 各分量绝对值之和：

$$ \|\mathbf{v}\|_1 = \sum_{i=1}^{n} |v_i| $$

**在 ML 中的应用:**
- $L^2$ 范数用于权重衰减 (weight decay / ridge regression)
- $L^1$ 范数用于稀疏化 (Lasso regression)

```python
import numpy as np

u = np.array([3, 2])
v = np.array([1, 4])

dot_product = np.dot(u, v)          # 3*1 + 2*4 = 11
norm_l2 = np.linalg.norm(u)         # sqrt(3^2 + 2^2) ≈ 3.606
norm_l1 = np.linalg.norm(u, ord=1)  # |3| + |2| = 5
```

### 1.5 线性无关与基 (Linear Independence & Basis)

**定义 4 (线性无关):** 一组向量 $\{\mathbf{v}_1, \mathbf{v}_2, ..., \mathbf{v}_k\}$ 线性无关，当且仅当：

$$ c_1 \mathbf{v}_1 + c_2 \mathbf{v}_2 + \cdots + c_k \mathbf{v}_k = \mathbf{0} $$

的唯一解是 $c_1 = c_2 = \cdots = c_k = 0$。

**基 (Basis):** $\mathbb{R}^n$ 的一组基是 $n$ 个线性无关的向量，它们能张成整个空间。最常用的是**标准正交基**：

$$ \mathbf{e}_1 = \begin{bmatrix}1\\0\\\vdots\\0\end{bmatrix},\;
   \mathbf{e}_2 = \begin{bmatrix}0\\1\\\vdots\\0\end{bmatrix},\;
   \ldots,\;
   \mathbf{e}_n = \begin{bmatrix}0\\0\\\vdots\\1\end{bmatrix} $$

> **关键洞察: 选择不同的基，就选择了不同的表示方式。** 这正是 PCA 和特征分解的核心思想。

---

## 2. 矩阵及其运算 (Matrix Operations)

### 2.1 矩阵的定义 (Definition)

矩阵是二维数组，可以理解为"排列在一起的多个列向量"或"多个行向量"：

$$ \mathbf{A}_{m \times n} = \begin{bmatrix}
a_{11} & a_{12} & \cdots & a_{1n} \\
a_{21} & a_{22} & \cdots & a_{2n} \\
\vdots & \vdots & \ddots & \vdots \\
a_{m1} & a_{m2} & \cdots & a_{mn}
\end{bmatrix} $$

$m$ = 行数，$n$ = 列数。如果 $m = n$，称为**方阵 (square matrix)**。

**在 ML 中的应用:**
- **数据集 (Dataset):** 一个 $m \times n$ 的矩阵，$m$ 个样本，每个样本 $n$ 个特征
- **权重矩阵 (Weight Matrix):** 神经网络的每一层都是一个矩阵乘法 $\mathbf{W}\mathbf{x}$
- **协方差矩阵 (Covariance Matrix):** 衡量特征间的关系

### 2.2 矩阵乘法 (Matrix Multiplication)

给定 $\mathbf{A}_{m \times n}$ 和 $\mathbf{B}_{n \times p}$，乘积 $\mathbf{C} = \mathbf{AB}$ 是 $m \times p$ 矩阵：

$$ c_{ij} = \sum_{k=1}^{n} a_{ik} b_{kj} $$

**几何意义:** 矩阵乘法可以看作**线性变换的复合**。矩阵 $\mathbf{A}$ 作用于向量 $\mathbf{x}$ 得到 $\mathbf{A}\mathbf{x}$，相当于对空间做了一个变换（旋转、缩放、剪切等）。

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
C = A @ B  # 或 np.matmul(A, B)
# [[19, 22],
#  [43, 50]]
```

### 2.3 转置 (Transpose)

将矩阵的行和列互换：

$$ (\mathbf{A}^\top)_{ij} = a_{ji} $$

重要性质：$(\mathbf{AB})^\top = \mathbf{B}^\top \mathbf{A}^\top$

### 2.4 逆矩阵 (Matrix Inverse)

**定义 5 (逆矩阵):** 对方阵 $\mathbf{A}$，如果存在矩阵 $\mathbf{A}^{-1}$ 使得：

$$ \mathbf{A} \mathbf{A}^{-1} = \mathbf{A}^{-1} \mathbf{A} = \mathbf{I} $$

则 $\mathbf{A}$ 称为**可逆** (invertible) 或**非奇异** (non-singular)。

**何时不可逆?** 当矩阵的行或列线性相关时（行列式为 0）。

```python
A = np.array([[1, 2], [3, 4]])
A_inv = np.linalg.inv(A)
# [[-2. ,  1. ],
#  [ 1.5, -0.5]]

# 验证: A @ A_inv ≈ I
np.allclose(A @ A_inv, np.eye(2))  # True
```

### 2.5 行列式 (Determinant)

方阵 $\mathbf{A}$ 的行列式 $\det(\mathbf{A})$ 是一个标量，衡量线性变换的**缩放因子**：

- $|\det(\mathbf{A})| > 1$：变换后空间被放大
- $|\det(\mathbf{A})| < 1$：变换后空间被压缩
- $\det(\mathbf{A}) = 0$：变换将空间压扁到低维（矩阵奇异，不可逆）
- $\det(\mathbf{A}) < 0$：变换改变了空间定向（镜像翻转）

```python
det_A = np.linalg.det(A)  # -2.0
```

---

## 3. 特征值与特征向量 (Eigenvalues & Eigenvectors)

### 3.1 几何直觉 (Geometric Intuition)

矩阵 $\mathbf{A}$ 作用于向量 $\mathbf{x}$，通常既改变方向又改变长度。但**存在一些特殊向量，$\mathbf{A}$ 只改变它们的长度，不改变方向**：

$$ \mathbf{A} \mathbf{v} = \lambda \mathbf{v} $$

- $\mathbf{v}$ 是**特征向量 (eigenvector)** — 方向不变
- $\lambda$ 是**特征值 (eigenvalue)** — 缩放倍数

> **想象一下:** 把一个矩形图片拉伸。大多数方向上的线段会改变方向，但沿长轴和短轴的方向只改变长度——这些就是特征向量方向。

### 3.2 如何求解 (How to Solve)

从定义出发：

$$ \mathbf{A} \mathbf{v} = \lambda \mathbf{v} $$
$$ \mathbf{A} \mathbf{v} - \lambda \mathbf{v} = \mathbf{0} $$
$$ (\mathbf{A} - \lambda \mathbf{I}) \mathbf{v} = \mathbf{0} $$

要求非零解 $\mathbf{v}$，必须有：

$$ \det(\mathbf{A} - \lambda \mathbf{I}) = 0 $$

这个方程称为**特征方程 (characteristic equation)**，是一个关于 $\lambda$ 的 $n$ 次多项式。

### 3.3 特征分解 (Eigendecomposition)

如果 $\mathbf{A}$ 有 $n$ 个线性无关的特征向量，可以写成：

$$ \mathbf{A} = \mathbf{V} \boldsymbol{\Lambda} \mathbf{V}^{-1} $$

其中 $\mathbf{V}$ 的列是特征向量，$\boldsymbol{\Lambda}$ 是对角矩阵（对角线上是特征值）。

**对对称矩阵的特殊性质:** 若 $\mathbf{A} = \mathbf{A}^\top$，则：
- 所有特征值为**实数**
- 特征向量可以选为**正交**的
- $\mathbf{A} = \mathbf{Q} \boldsymbol{\Lambda} \mathbf{Q}^\top$，其中 $\mathbf{Q}$ 是正交矩阵 ($\mathbf{Q}^\top = \mathbf{Q}^{-1}$)

```python
A = np.array([[2, 1], [1, 2]])
eigvals, eigvecs = np.linalg.eig(A)

print(eigvals)  # [3., 1.]
print(eigvecs)  # [[ 0.707, -0.707],
                #  [ 0.707,  0.707]]

# 验证: A @ v = λ v
v = eigvecs[:, 0]
l = eigvals[0]
np.allclose(A @ v, l * v)  # True
```

### 3.4 在 ML 中的应用

1. **主成分分析 (PCA):** 数据协方差矩阵的最大特征值对应的特征向量就是第一主成分方向
2. **谱聚类 (Spectral Clustering):** 利用图 Laplacian 矩阵的特征向量进行聚类
3. **PageRank:** 网页排名本质上是一个特征向量问题
4. **动力系统:** 特征值决定系统的稳定性（所有 $|\lambda| < 1$ 则系统稳定）

---

## 4. 奇异值分解 SVD (Singular Value Decomposition)

### 4.1 为什么需要 SVD?

特征分解**要求矩阵是方阵**。但现实中的数据矩阵几乎都是非方阵（$m$ 个样本 $\times n$ 个特征）。SVD 是特征分解对任意矩阵的推广，被誉为"线性代数的瑞士军刀"。

### 4.2 SVD 的定义 (Definition)

任意矩阵 $\mathbf{A}_{m \times n}$ 可以分解为：

$$ \mathbf{A} = \mathbf{U} \boldsymbol{\Sigma} \mathbf{V}^\top $$

- $\mathbf{U}_{m \times m}$：左奇异向量 (left singular vectors)，**正交矩阵**
- $\boldsymbol{\Sigma}_{m \times n}$：奇异值矩阵 (singular values)，**对角线上** $\sigma_1 \geq \sigma_2 \geq \cdots \geq \sigma_r > 0$，其余为 0
- $\mathbf{V}_{n \times n}$：右奇异向量 (right singular vectors)，**正交矩阵**

### 4.3 几何直觉 (Geometric Intuition)

SVD 将一个线性变换分解为三个步骤：

1. **旋转/反射** $(\mathbf{V}^\top)$ — 在原始空间中对输入进行旋转
2. **缩放** $(\boldsymbol{\Sigma})$ — 沿新坐标轴拉伸/压缩
3. **旋转/反射** $(\mathbf{U})$ — 在输出空间中对结果旋转

> **关键洞察:** 奇异值 $\sigma_i$ 衡量了该方向上的"重要性"。最大的奇异值对应数据方差最大的方向。

### 4.4 SVD 与 PCA 的关系

PCA 可以完全通过 SVD 实现，**不需要计算协方差矩阵**：

1. 中心化数据矩阵 $\mathbf{X}$（每列减去均值）
2. 计算 SVD: $\mathbf{X} = \mathbf{U} \boldsymbol{\Sigma} \mathbf{V}^\top$
3. 主成分 = $\mathbf{V}$ 的列（右奇异向量）
4. 投影后数据 = $\mathbf{U} \boldsymbol{\Sigma}$（主成分得分）

**为什么 SVD 更稳定?** 计算协方差矩阵 $\mathbf{X}^\top \mathbf{X}$ 会平方条件数（condition number），导致数值不稳定。直接对 $\mathbf{X}$ 做 SVD 避免了这个问题。

### 4.5 低秩近似 (Low-rank Approximation)

SVD 最重要的应用之一：用前 $k$ 个最大的奇异值来近似原矩阵：

$$ \mathbf{A} \approx \mathbf{A}_k = \sum_{i=1}^{k} \sigma_i \mathbf{u}_i \mathbf{v}_i^\top $$

```python
# 低秩近似示例: 用前 2 个奇异值近似 4×4 矩阵
A = np.random.randn(4, 4)
U, S, Vt = np.linalg.svd(A, full_matrices=False)

k = 2
A_k = U[:, :k] @ np.diag(S[:k]) @ Vt[:k, :]

# 检查近似误差
error = np.linalg.norm(A - A_k, 'fro')
print(f"k={k} 近似误差: {error:.4f}")
```

**在 ML 中的应用:**
- **图像压缩:** 保留最大的奇异值，丢弃小奇异值
- **推荐系统:** 矩阵分解 (Matrix Factorization) 基于 SVD
- **降维:** 用 SVD 实现 PCA，将数据降到 $k$ 维
- **去噪:** 小奇异值通常对应噪声，截断后可去噪

---

## 5. 矩阵微积分 (Matrix Calculus)

### 5.1 为什么需要矩阵微积分?

机器学习中，我们的目标函数通常是**标量函数 $f$ 对向量或矩阵参数 $\mathbf{w}$ 的求导**。这是反向传播 (backpropagation) 的数学基础。

### 5.2 标量对向量的导数 (Gradient)

给定 $f: \mathbb{R}^n \rightarrow \mathbb{R}$，梯度 $\nabla f$ 是 $n$ 维向量：

$$ \nabla f(\mathbf{x}) = \begin{bmatrix} \frac{\partial f}{\partial x_1} \\ \frac{\partial f}{\partial x_2} \\ \vdots \\ \frac{\partial f}{\partial x_n} \end{bmatrix} $$

**几何意义:** 梯度指向函数 $f$ 在点 $\mathbf{x}$ 处**增长最快**的方向。这正是梯度上升/下降的理论基础。

### 5.3 三个关键公式 (Three Essential Formulas)

在 ML 中，你只需要记住以下三个公式（记熟它们，反向传播不再神秘）：

#### 公式 1: 线性函数
$$ f(\mathbf{x}) = \mathbf{a}^\top \mathbf{x} = a_1 x_1 + a_2 x_2 + \cdots + a_n x_n $$
$$ \nabla f(\mathbf{x}) = \mathbf{a} $$

#### 公式 2: 二次型 (Quadratic Form)
$$ f(\mathbf{x}) = \mathbf{x}^\top \mathbf{A} \mathbf{x} $$
$$ \nabla f(\mathbf{x}) = (\mathbf{A} + \mathbf{A}^\top) \mathbf{x} $$

**特例** — 若 $\mathbf{A}$ 是对称矩阵 ($\mathbf{A} = \mathbf{A}^\top$)：
$$ \nabla f(\mathbf{x}) = 2\mathbf{A} \mathbf{x} $$

#### 公式 3: 平方范数 (Squared Norm)
$$ f(\mathbf{x}) = \|\mathbf{x}\|_2^2 = \mathbf{x}^\top \mathbf{x} $$
$$ \nabla f(\mathbf{x}) = 2\mathbf{x} $$

> **💡 这些公式为什么重要?** 线性回归的损失函数 $L(\mathbf{w}) = \|\mathbf{X}\mathbf{w} - \mathbf{y}\|_2^2$ 展开后就是一个二次型。用公式 2 求梯度再令其为 0，就能推导出**正规方程 (normal equation)** $\mathbf{w}^* = (\mathbf{X}^\top \mathbf{X})^{-1} \mathbf{X}^\top \mathbf{y}$。

### 5.4 链式法则 (Chain Rule)

若 $f(g(\mathbf{x}))$ 且 $g: \mathbb{R}^n \rightarrow \mathbb{R}^m$，则：

$$ \nabla_{\mathbf{x}} f(g(\mathbf{x})) = \mathbf{J}_g(\mathbf{x})^\top \nabla_{g} f $$

其中 $\mathbf{J}_g \in \mathbb{R}^{m \times n}$ 是 Jacobian 矩阵：

$$ \mathbf{J}_g = \begin{bmatrix}
\frac{\partial g_1}{\partial x_1} & \cdots & \frac{\partial g_1}{\partial x_n} \\
\vdots & \ddots & \vdots \\
\frac{\partial g_m}{\partial x_1} & \cdots & \frac{\partial g_m}{\partial x_n}
\end{bmatrix} $$

**这就是反向传播的理论基础 ❤️**

### 5.5 示例: 线性回归的梯度推导

损失函数：$L(\mathbf{w}) = \frac{1}{m} \|\mathbf{X}\mathbf{w} - \mathbf{y}\|_2^2$

展开：
$$ L(\mathbf{w}) = \frac{1}{m} (\mathbf{X}\mathbf{w} - \mathbf{y})^\top (\mathbf{X}\mathbf{w} - \mathbf{y}) $$

令 $\mathbf{z} = \mathbf{X}\mathbf{w} - \mathbf{y}$，则 $L = \frac{1}{m} \mathbf{z}^\top \mathbf{z}$

$$ \frac{\partial L}{\partial \mathbf{w}} = \frac{1}{m} \cdot 2 \mathbf{z}^\top \frac{\partial \mathbf{z}}{\partial \mathbf{w}} = \frac{2}{m} \mathbf{z}^\top \mathbf{X} $$

所以梯度为：
$$ \nabla L(\mathbf{w}) = \frac{2}{m} \mathbf{X}^\top (\mathbf{X}\mathbf{w} - \mathbf{y}) $$

---

## 本章总结 (Chapter Summary)

| 概念 | 数学表达 | ML 应用 | NumPy 关键函数 |
|:---|:---|:---|:---|
| 向量 | $\mathbf{v} \in \mathbb{R}^n$ | 样本表示、词嵌入 | `np.array()` |
| 点积 | $\mathbf{u} \cdot \mathbf{v} = \sum u_i v_i$ | 注意力机制、相似度 | `np.dot()` |
| 范数 | $\|\mathbf{v}\|_p$ | 正则化 (L1/L2) | `np.linalg.norm()` |
| 矩阵乘法 | $\mathbf{C} = \mathbf{AB}$ | 神经网络前向传播 | `@`, `np.matmul()` |
| 逆矩阵 | $\mathbf{A}^{-1}$ | 正规方程 | `np.linalg.inv()` |
| 行列式 | $\det(\mathbf{A})$ | 特征值计算 | `np.linalg.det()` |
| 特征分解 | $\mathbf{A} = \mathbf{V}\boldsymbol{\Lambda}\mathbf{V}^{-1}$ | PCA、谱聚类 | `np.linalg.eig()` |
| SVD | $\mathbf{A} = \mathbf{U}\boldsymbol{\Sigma}\mathbf{V}^\top$ | PCA、降维、压缩 | `np.linalg.svd()` |
| 梯度 | $\nabla f(\mathbf{x})$ | 梯度下降、反向传播 | 手动推导 |

## 进一步阅读 (Further Reading)

- [Gilbert Strang - Linear Algebra for Everyone](https://math.mit.edu/~gs/everyone/)
- [3Blue1Brown - Essence of Linear Algebra (YouTube)](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab)
- [NumPy Linear Algebra Documentation](https://numpy.org/doc/stable/reference/routines.linalg.html)

---

> **下一章预告:** [概率论与信息论](./02-probability.md) — 不确定性、熵、KL 散度，为理解交叉熵损失和信息论打下基础。
