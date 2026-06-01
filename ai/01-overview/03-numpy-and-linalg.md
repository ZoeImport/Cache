# 03 — NumPy 与线性代数基础（NumPy & Linear Algebra for ML）

> 机器学习（Machine Learning）本质上是对数据的数学变换。**NumPy** 是 Python 生态中最核心的数值计算库（Numerical Computing Library），它为 ML 提供了高效的 **多维数组（ndarray）** 和 **线性代数（Linear Algebra）** 操作。本章从 ndarray 基础出发，深入广播机制（Broadcasting）和常用线性代数运算，最终用 NumPy 手写一个 KNN 分类器。

---

## 1. ndarray 基础

### 1.1 什么是 ndarray？

**ndarray**（N-dimensional Array，N 维数组）是 NumPy 的核心数据结构。与 Python 原生列表相比：

| 特性 | Python list | NumPy ndarray |
|:---|:---|:---|
| 元素类型 | 任意（可混合） | **同质**（同一类型） |
| 内存布局 | 分散的 Python 对象 | **连续内存块** |
| 计算速度 | 慢（Python 解释器逐元素迭代） | **快**（C 语言实现，向量化） |
| 广播（Broadcasting） | 不支持 | 原生支持 |

### 1.2 创建数组

```python
import numpy as np

# 从 Python 列表创建
a = np.array([1, 2, 3])           # 1D: shape (3,)
b = np.array([[1, 2], [3, 4]])    # 2D: shape (2, 2)

# 特殊数组
zeros = np.zeros((3, 4))           # 全零矩阵
ones = np.ones((2, 3))             # 全一矩阵
eye = np.eye(3)                    # 单位矩阵（Identity Matrix）
empty = np.empty((2, 2))           # 未初始化（垃圾值）

# 序列
arange = np.arange(0, 10, 2)       # [0, 2, 4, 6, 8]
linspace = np.linspace(0, 1, 5)    # [0. , 0.25, 0.5 , 0.75, 1. ]

# 随机数
rand = np.random.rand(3, 3)        # [0, 1) 均匀分布（Uniform Distribution）
randn = np.random.randn(1000)      # 标准正态分布（Standard Normal Distribution）
randint = np.random.randint(0, 10, size=(2, 3))  # 随机整数
```

### 1.3 Shape、Reshape 与 Axis

**shape** 定义了数组在每个维度上的大小，**reshape** 可以在不改变数据的前提下重新编排维度，**axis** 则指定了操作沿哪个方向进行。

```python
arr = np.arange(12)                # shape (12,)
arr_2d = arr.reshape(3, 4)         # shape (3, 4)
arr_3d = arr.reshape(2, 3, 2)      # shape (2, 3, 2)

# axis=0 表示沿着"行"方向（跨列）
# axis=1 表示沿着"列"方向（跨行）
print(arr_2d.sum(axis=0))          # 每列求和: [12 15 18 21]
print(arr_2d.sum(axis=1))          # 每行求和: [ 6 22 38]
```

> **理解 axis**：axis=0 是"垂直向下"的方向，压缩行；axis=1 是"水平向右"的方向，压缩列。对于高维数组，这个直觉也成立。

### 1.4 向量化（Vectorization）—— 为什么 NumPy 快

**向量化（Vectorization）** 是指用数组表达式替代显式循环。NumPy 的底层用 C/Fortran 实现，避免了 Python 循环的逐元素解释开销。

```python
# Python 循环版本 —— 慢
def py_square(x):
    result = []
    for i in range(len(x)):
        result.append(x[i] ** 2)
    return result

# NumPy 向量化版本 —— 快约 50-100x
def np_square(x):
    return x ** 2
```

> 详见配套代码 `numpy_basics.py` 中的性能对比（Performance Comparison）。

---

## 2. 广播机制（Broadcasting）

### 2.1 什么是广播？

**广播（Broadcasting）** 是 NumPy 在不同 shape 的数组之间进行算术运算的规则。它"自动扩展"较小的数组，使其 shape 与较大的数组兼容，**无需复制数据**。

### 2.2 广播规则

从**最右边的维度**开始向左对齐，每个维度满足以下条件之一即可兼容：

1. 两个维度大小相等
2. 其中一个维度大小为 1
3. 其中一个维度不存在（视为 1）

```
Shape A:       (3,)           (3, 1)          (3, 1)           (2, 1, 3)
Shape B:       (1,)    →      (1, 4)    →     (4,)       →     (5, 4, 3)
Result:        (3,)           (3, 4)          (3, 4)           (5, 4, 3)
               ✔              ✔               ✔                ✔
```

### 2.3 可视化示例

```python
# 例 1: 标量 + 向量
a = np.array([1, 2, 3])        # shape (3,)
b = 10                         # shape () → 广播为 (3,)
print(a + b)                   # [11 12 13]

# 例 2: 列向量 + 行向量
col = np.array([[1], [2], [3]])   # shape (3, 1)
row = np.array([10, 20, 30, 40])  # shape (4,) → 广播为 (1, 4)
result = col + row                 # result shape (3, 4)
# 每一步:
# col:  (3,1) → (3,4)  每列复制 4 次
# row:  (4,)  → (1,4) → (3,4)  每行复制 3 次
```

### 2.4 常见陷阱（Gotchas）

```python
# 陷阱 1: shape 不兼容
a = np.ones((3, 2))
b = np.ones((2, 3))
# a + b  →  ValueError: shape (3,2) 与 (2,3) 在 axis=0 和 axis=1 都不匹配

# 陷阱 2: 忘记添加尾部维度
a = np.ones((3, 4))
b = np.array([1, 2, 3])          # shape (3,)
# a + b  →  shape (3,4) vs (3,)  →  右对齐后 (3,4) vs (3,) 不兼容!
# 正确做法: b = b.reshape(3, 1)  或  b = b[:, np.newaxis]
```

---

## 3. 线性代数运算（Linear Algebra Operations）

NumPy 的 `np.linalg` 子模块提供了完整的线性代数工具集。

### 3.1 点积与矩阵乘法

```python
# 向量点积（Dot Product）
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
dot = np.dot(a, b)          # 1*4 + 2*5 + 3*6 = 32

# 矩阵乘法（Matrix Multiplication）
X = np.array([[1, 2], [3, 4]])
Y = np.array([[5, 6], [7, 8]])
mat_mul = X @ Y              # 等价于 np.matmul(X, Y)
# [[1*5+2*7, 1*6+2*8],
#  [3*5+4*7, 3*6+4*8]]
```

> `@` 运算符是 Python 3.5+ 引入的矩阵乘法（Matrix Multiplication）专用操作符，在 ML 代码中非常常用。

### 3.2 转置、逆与行列式

```python
# 转置（Transpose）
X = np.array([[1, 2], [3, 4]])
print(X.T)                   # [[1, 3], [2, 4]]

# 逆矩阵（Matrix Inverse）
X_inv = np.linalg.inv(X)    # X @ X_inv ≈ I

# 行列式（Determinant）
det = np.linalg.det(X)      # 1*4 - 2*3 = -2.0
```

### 3.3 特征值分解（Eigen Decomposition）

**特征值分解（Eigen Decomposition）** 将方阵分解为特征向量（Eigenvectors）和特征值（Eigenvalues）：

$$A = Q \Lambda Q^{-1}$$

其中 $\Lambda$ 是对角矩阵，对角线元素是特征值；$Q$ 的列是特征向量。

```python
A = np.array([[4, -2], [1, 1]])
eigenvalues, eigenvectors = np.linalg.eig(A)
# eigenvalues:  [3., 2.]
# eigenvectors: 列向量为对应的特征向量
```

> **应用**：PCA（主成分分析，Principal Component Analysis）的核心就是对协方差矩阵（Covariance Matrix）做特征值分解。

### 3.4 SVD 分解（Singular Value Decomposition）

**奇异值分解（SVD, Singular Value Decomposition）** 是线性代数中最强大、最通用的矩阵分解方法，适用于**任意矩阵**（不要求方阵）：

$$A = U \Sigma V^T$$

```python
A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=float)
U, S, Vt = np.linalg.svd(A)
# U:   左奇异向量（Left Singular Vectors）
# S:   奇异值（Singular Values）—— 一维数组，非零奇异值按降序排列
# Vt:  右奇异向量的转置（Right Singular Vectors, transposed）
```

> **应用**：SVD 是推荐系统（Recommender Systems）、矩阵补全（Matrix Completion）、数据压缩（Data Compression）和主成分分析（PCA）的数学基础。

---

## 4. 编码项目：从零实现 KNN（K-Nearest Neighbors）

### 4.1 算法原理

**K 近邻（K-Nearest Neighbors, KNN）** 是一种基于实例的学习方法（Instance-based Learning）：

1. 给定一个待预测的样本点，计算它与所有训练样本的距离（通常使用欧氏距离 Euclidean Distance）
2. 选取距离最近的 K 个邻居
3. 对于分类任务，用 K 个邻居的标签进行**多数投票（Majority Voting）**
4. 对于回归任务，取 K 个邻居的目标值的**均值（Mean）**

### 4.2 KNN 中的 NumPy 力量

- **广播（Broadcasting）**：计算一个点与所有点的距离时，利用广播自动扩展
- **向量化（Vectorization）**：整个距离矩阵一次计算完成，无 Python 循环
- **索引（Indexing）**：`np.argsort` 排序索引，花式索引取标签

### 4.3 代码位置

完整实现见配套代码 [`linalg_demo.py`](./code/linalg_demo.py) 中的 `KNN` 类。

核心逻辑提炼：

```python
class KNN:
    def predict(self, X):
        # 欧氏距离: ||x - x_i||² 利用广播
        diffs = X[:, np.newaxis, :] - self.X_train  # shape (n_test, n_train, n_features)
        dists = np.sqrt((diffs ** 2).sum(axis=2))    # shape (n_test, n_train)

        # 取最近 K 个邻居
        nearest = np.argsort(dists, axis=1)[:, :self.k]

        # 多数投票
        labels = self.y_train[nearest]
        predictions = np.array([np.bincount(row).argmax() for row in labels])
        return predictions
```

> 以上代码展示了 **广播（Broadcasting）**、**向量化距离计算**、**argsort 排序** 和 **花式索引（Fancy Indexing）** 的综合运用。

---

## 5. 本章小结

| 概念 | 要点 |
|:---|:---|
| **ndarray** | 同质、连续内存、支持向量化操作 |
| **Broadcasting** | 从右向左对齐，维度为 1 或缺失时可扩展 |
| **dot / @** | 向量点积和矩阵乘法，ML 中最频繁的操作 |
| **Eigen / SVD** | 特征值分解（方阵）和 SVD（任意矩阵）是降维和矩阵分解的基石 |
| **KNN** | 利用广播快速计算距离矩阵，用 argsort 和 bincount 完成投票 |

---

## 6. 进一步阅读

- [NumPy 官方快速入门（NumPy Quickstart Tutorial）](https://numpy.org/doc/stable/user/quickstart.html)
- [NumPy 广播文档（NumPy Broadcasting Documentation）](https://numpy.org/doc/stable/user/basics.broadcasting.html)
- [《线性代数及其应用》—— David C. Lay（经典教材）](https://www.pearson.com/en-us/subject-catalog/p/linear-algebra-and-its-applications/P200000006240)

---

*下一章：[04 — Pandas 与数据处理基础](./04-pandas-and-data-processing.md)*
