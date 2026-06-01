# 第1章 线性模型 — 机器学习的基石
# Chapter 1: Linear Models — The Foundation of Machine Learning

> **线性模型是机器学习的起点。** 从最简单的线性回归到逻辑回归，再到支撑向量机，线性模型构成了理解和构建更复杂模型的基础。本章的核心是理解 **参数 (Parameters)、损失 (Loss)、梯度 (Gradient)** 这三个概念——它们将贯穿本书所有后续模型。
>
> **Linear models are where Machine Learning begins.** From the simplest linear regression to logistic regression and beyond, linear models form the foundation for understanding and building more complex models. The core of this chapter is understanding three concepts — **Parameters, Loss, Gradient** — that will appear in every single model throughout this book.

**前置知识 (Prerequisites):** 高中数学（导数、偏导数），矩阵基本运算，概率基础（贝努利分布、似然）
**依赖库 (Dependencies):** `numpy`, `scipy`, `matplotlib`, `scikit-learn`

**Code companion:** [`code/linear_models.py`](code/linear_models.py)

---

## 目录 (Table of Contents)

1. [线性回归 (Linear Regression)](#1-线性回归-linear-regression)
   - 1.1 [问题定义](#11-问题定义-problem-formulation)
   - 1.2 [MSE 损失函数](#12-mse-损失函数-mse-loss-function)
   - 1.3 [最小二乘与正规方程](#13-最小二乘与正规方程-ols-and-normal-equations)
   - 1.4 [梯度下降解法](#14-梯度下降解法-gradient-descent-solution)
   - 1.5 [实现与可视化](#15-实现与可视化-implementation--visualization)
2. [逻辑回归 (Logistic Regression)](#2-逻辑回归-logistic-regression)
   - 2.1 [从线性回归到分类](#21-从线性回归到分类-from-linear-regression-to-classification)
   - 2.2 [Sigmoid 函数](#22-sigmoid-函数-sigmoid-function)
   - 2.3 [似然与交叉熵损失](#23-似然与交叉熵损失-likelihood--cross-entropy-loss)
   - 2.4 [决策边界](#24-决策边界-decision-boundary)
   - 2.5 [实现与可视化](#25-实现与可视化-implementation--visualization)
3. [正则化 (Regularization)](#3-正则化-regularization)
   - 3.1 [过拟合与欠拟合](#31-过拟合与欠-fitting-vs-overfitting)
   - 3.2 [L2 正则化 / Ridge](#32-l2-正则化--ridge-ridge-regression)
   - 3.3 [L1 正则化 / Lasso](#33-l1-正则化--lasso-lasso-regression)
   - 3.4 [L1 vs L2 — 稀疏性的几何直觉](#34-l1-vs-l2--稀疏性的几何直觉-geometric-intuition-for-sparsity)
4. [三个核心概念 (Three Core Concepts)](#4-三个核心概念-three-core-concepts)
5. [小结 (Summary)](#5-小结-summary)

---

## 1. 线性回归 (Linear Regression)

### 1.1 问题定义 (Problem Formulation)

线性回归是**监督学习**中最基本的模型。给定 $n$ 个样本 $\{(x_i, y_i)\}_{i=1}^n$，其中 $x_i \in \mathbb{R}^d$ 是 $d$ 维特征向量，$y_i \in \mathbb{R}$ 是连续目标值，我们希望找到 $x$ 与 $y$ 的线性关系：

$$ y = w_1 x_1 + w_2 x_2 + \cdots + w_d x_d + b + \epsilon $$

用向量形式简洁表示为：

$$ y = \mathbf{w}^T \mathbf{x} + b + \epsilon $$

其中 $\mathbf{w} \in \mathbb{R}^d$ 是权重向量，$b \in \mathbb{R}$ 是偏置，$\epsilon$ 是噪声项（通常假设为高斯分布 $\epsilon \sim \mathcal{N}(0, \sigma^2)$）。

**为了符号简洁**，我们通常将偏置 $b$ 合并进权重向量：令 $\tilde{\mathbf{x}} = [1, x_1, x_2, \dots, x_d]^T \in \mathbb{R}^{d+1}$，$\tilde{\mathbf{w}} = [b, w_1, \dots, w_d]^T$，则：

$$ y = \tilde{\mathbf{w}}^T \tilde{\mathbf{x}} + \epsilon $$

对于全部 $n$ 个样本，写作矩阵形式：

$$ \mathbf{y} = X \mathbf{w} + \boldsymbol{\epsilon} $$

其中 $X \in \mathbb{R}^{n \times (d+1)}$ 是设计矩阵（每行一个样本，第一列全1），$\mathbf{y} \in \mathbb{R}^n$，$\boldsymbol{\epsilon} \in \mathbb{R}^n$。

### 1.2 MSE 损失函数 (MSE Loss Function)

**我们的目标：** 找到最优的 $\mathbf{w}$，使得预测值 $\hat{y} = X\mathbf{w}$ 尽可能接近真实值 $\mathbf{y}$。

**最常用的损失函数：均方误差（MSE, Mean Squared Error）：**

$$ \mathcal{L}(\mathbf{w}) = \frac{1}{n} \sum_{i=1}^n (y_i - \hat{y}_i)^2 = \frac{1}{n} \| \mathbf{y} - X\mathbf{w} \|_2^2 $$

> **为什么用 MSE？** 最小化 MSE 等价于 **极大似然估计（MLE）** 在噪声服从高斯分布下的解。详细推导见《AI 数学基础》第5章。

### 1.3 最小二乘与正规方程 (OLS and Normal Equations)

#### 推导：从 MSE 到正规方程

令损失函数为（为了求导方便，有时也写作 $\frac{1}{2n}$ 或 $\frac{1}{2}$，不影响最优解位置）：

$$ \mathcal{L}(\mathbf{w}) = \frac{1}{n} (\mathbf{y} - X\mathbf{w})^T (\mathbf{y} - X\mathbf{w}) $$

**第1步：展开损失函数**

$$ \begin{aligned}
\mathcal{L}(\mathbf{w}) &= \frac{1}{n} \left( \mathbf{y}^T\mathbf{y} - 2\mathbf{w}^T X^T \mathbf{y} + \mathbf{w}^T X^T X \mathbf{w} \right)
\end{aligned} $$

**第2步：对 $\mathbf{w}$ 求梯度，设为0**

回忆矩阵微积分公式：
- $\frac{\partial}{\partial \mathbf{w}} (\mathbf{a}^T \mathbf{w}) = \mathbf{a}$
- $\frac{\partial}{\partial \mathbf{w}} (\mathbf{w}^T A \mathbf{w}) = (A + A^T) \mathbf{w}$，若 $A$ 对称则 $= 2A\mathbf{w}$

所以：

$$ \frac{\partial \mathcal{L}}{\partial \mathbf{w}} = \frac{1}{n} \left( -2X^T \mathbf{y} + 2 X^T X \mathbf{w} \right) = 0 $$

**第3步：令梯度为0，求解 $\mathbf{w}$**

$$ -2X^T \mathbf{y} + 2 X^T X \mathbf{w} = 0 $$

$$ X^T X \mathbf{w} = X^T \mathbf{y} $$

这就是**正规方程 (Normal Equations)**。当 $X^T X$ 可逆时：

$$ \boxed{ \mathbf{w}^* = (X^T X)^{-1} X^T \mathbf{y} } $$

这就是**最小二乘法 (Ordinary Least Squares, OLS)** 的闭式解。

> **几何解释：** $\hat{\mathbf{y}} = X\mathbf{w}^* = X(X^T X)^{-1}X^T \mathbf{y}$ 是 $\mathbf{y}$ 在 $X$ 的列空间上的正交投影。$P = X(X^T X)^{-1}X^T$ 被称为**投影矩阵**。

**第4步：验证最优性**

$\mathcal{L}(\mathbf{w})$ 的海森矩阵为 $\frac{2}{n} X^T X$，当 $X$ 列满秩时，$X^T X$ 是正定矩阵 → 损失函数是凸函数 → $\mathbf{w}^*$ 是全局最小值。

#### 何时使用闭式解 vs 梯度下降？

| 方法 | 优点 | 缺点 |
|------|------|------|
| **闭式解 (Normal Equations)** | 一步得到精确解 | $O(n d^2 + d^3)$，$d$ 大时不可行 |
| **梯度下降 (Gradient Descent)** | 可扩展到大 $d$，通用 | 需要调学习率，迭代收敛 |

> **经验法则：** $d < 10^4$ 时闭式解 OK，$d > 10^4$ 或 $n$ 极大时用梯度下降。

### 1.4 梯度下降解法 (Gradient Descent Solution)

梯度下降是**迭代优化**中最常用的方法。其核心思想很简单：

> **沿着损失函数梯度的反方向走，就能下降到局部（这里是全局）最低点。**

#### 算法步骤

1. 初始化 $\mathbf{w}^{(0)}$
2. 对 $t = 0, 1, 2, \dots$ 直到收敛：
   $$ \mathbf{w}^{(t+1)} = \mathbf{w}^{(t)} - \eta \cdot \nabla \mathcal{L}(\mathbf{w}^{(t)}) $$
   其中 $\eta$ 是**学习率 (learning rate)**。

#### 线性回归的梯度

$$ \nabla \mathcal{L}(\mathbf{w}) = \frac{2}{n} X^T (X\mathbf{w} - \mathbf{y}) $$

**物理意义：** 梯度的每个分量告诉我们在对应方向上的调整幅度——残差 $(X\mathbf{w} - \mathbf{y})$ 越大，调整步长越大。

#### 三种变体

- **批量梯度下降 (Batch GD):** 每次用所有 $n$ 个样本计算梯度 → 准确但慢
- **随机梯度下降 (SGD):** 每次用 1 个样本 → 快但波动大
- **小批量梯度下降 (Mini-batch GD):** 每次用 $m$ 个样本（实用中最常见）

### 1.5 实现与可视化 (Implementation & Visualization)

请运行 `code/linear_models.py` 中的 `demo_linear_regression()` 函数，查看：

1. **损失下降曲线** — 随着迭代次数增加，MSE 单调递减
2. **拟合结果** — 回归线穿过数据点云
3. **参数轨迹等高图** — 参数 $(w, b)$ 在损失曲面上的优化路径
4. **闭式解 vs GD 比较** — 两者最终收敛到相同位置

---

## 2. 逻辑回归 (Logistic Regression)

### 2.1 从线性回归到分类 (From Linear Regression to Classification)

线性回归预测**连续值**。但如果我们想预测**类别**（如 "是猫/不是猫"、"良性/恶性"）怎么办？

一个朴素的想法：对线性输出加一个阈值：

$$ y = \begin{cases} 1 & \text{if } \mathbf{w}^T\mathbf{x} + b > 0 \\ 0 & \text{otherwise} \end{cases} $$

但这样做的问题是：
- 不可导 → 无法用梯度下降优化
- 对远离决策边界的数据过于"自信"
- 对极端值敏感

**逻辑回归 (Logistic Regression)** 解决这个问题——它名为"回归"，实为**分类**算法。

### 2.2 Sigmoid 函数 (Sigmoid Function)

逻辑回归的核心是 **Sigmoid 函数**（也称 Logistic 函数）：

$$ \sigma(z) = \frac{1}{1 + e^{-z}} $$

**关键性质：**

| 性质 | 说明 |
|------|------|
| **输出范围** | $\sigma(z) \in (0, 1)$ |
| **对称性** | $\sigma(-z) = 1 - \sigma(z)$ |
| **单调性** | 严格单调递增 |
| **导数** | $\sigma'(z) = \sigma(z)(1 - \sigma(z))$ — 这个性质使梯度计算非常简洁 |
| **概率解释** | 输出值可以解释为 $P(y=1 | \mathbf{x})$ |

**Sigmoid 的导数推导：**

$$ \begin{aligned}
\sigma'(z) &= \frac{d}{dz} \left( \frac{1}{1 + e^{-z}} \right) \\
&= \frac{e^{-z}}{(1 + e^{-z})^2} \\
&= \frac{1}{1 + e^{-z}} \cdot \frac{e^{-z}}{1 + e^{-z}} \\
&= \sigma(z) \left( 1 - \sigma(z) \right)
\end{aligned} $$

这个优雅的导数形式使得后续梯度计算变得非常简单。

### 2.3 似然与交叉熵损失 (Likelihood & Cross-Entropy Loss)

#### 模型定义

逻辑回归模型假设：

$$ P(y=1 | \mathbf{x}; \mathbf{w}) = \sigma(\mathbf{w}^T \mathbf{x} + b) $$
$$ P(y=0 | \mathbf{x}; \mathbf{w}) = 1 - \sigma(\mathbf{w}^T \mathbf{x} + b) $$

统一写成：

$$ P(y | \mathbf{x}; \mathbf{w}) = \sigma(\mathbf{w}^T \mathbf{x})^y \cdot (1 - \sigma(\mathbf{w}^T \mathbf{x}))^{1-y} $$

其中 $y \in \{0, 1\}$。

#### 从似然到损失函数

对于 $n$ 个独立样本，**似然函数 (Likelihood Function)** 为：

$$ \mathcal{L}(\mathbf{w}) = \prod_{i=1}^n P(y^{(i)} | \mathbf{x}^{(i)}; \mathbf{w}) = \prod_{i=1}^n \sigma(\mathbf{w}^T \mathbf{x}^{(i)})^{y^{(i)}} (1 - \sigma(\mathbf{w}^T \mathbf{x}^{(i)}))^{1 - y^{(i)}} $$

取负对数（最大化似然 = 最小化负对数似然）：

$$ \begin{aligned}
-\log \mathcal{L}(\mathbf{w}) &= -\sum_{i=1}^n \left[ y^{(i)} \log \sigma(\mathbf{w}^T \mathbf{x}^{(i)}) + (1 - y^{(i)}) \log (1 - \sigma(\mathbf{w}^T \mathbf{x}^{(i)})) \right]
\end{aligned} $$

这就是**交叉熵损失 (Cross-Entropy Loss)**：

$$ \boxed{ \mathcal{L}_{\text{CE}}(\mathbf{w}) = -\frac{1}{n} \sum_{i=1}^n \left[ y^{(i)} \log \hat{y}^{(i)} + (1 - y^{(i)}) \log (1 - \hat{y}^{(i)}) \right] } $$

其中 $\hat{y}^{(i)} = \sigma(\mathbf{w}^T \mathbf{x}^{(i)})$。

> **交叉熵 vs MSE for 分类：** 交叉熵在错误预测时产生更大的梯度（因为 $\log$ 在接近0时趋向 $-\infty$），训练更高效。MSE + Sigmoid 会在预测极端错误时梯度趋近0（sigmoid 饱和区），导致学习停滞。

#### 梯度推导

令 $z_i = \mathbf{w}^T \mathbf{x}^{(i)}$，$\hat{y}_i = \sigma(z_i)$。

对单个样本的损失 $l_i = -[y_i \log \hat{y}_i + (1-y_i)\log(1-\hat{y}_i)]$ 求梯度：

$$ \begin{aligned}
\frac{\partial l_i}{\partial \mathbf{w}} &= -\left[ y_i \frac{1}{\hat{y}_i} \cdot \hat{y}_i (1 - \hat{y}_i) \cdot \mathbf{x}_i + (1-y_i) \frac{1}{1-\hat{y}_i} \cdot (-\hat{y}_i (1 - \hat{y}_i)) \cdot \mathbf{x}_i \right] \\
&= -\left[ y_i (1 - \hat{y}_i) \mathbf{x}_i - (1-y_i) \hat{y}_i \mathbf{x}_i \right] \\
&= -\left[ y_i \mathbf{x}_i - y_i \hat{y}_i \mathbf{x}_i - \hat{y}_i \mathbf{x}_i + y_i \hat{y}_i \mathbf{x}_i \right] \\
&= - (y_i - \hat{y}_i) \mathbf{x}_i
\end{aligned} $$

惊人地简洁！整体梯度为：

$$ \boxed{ \nabla \mathcal{L}_{\text{CE}}(\mathbf{w}) = \frac{1}{n} \sum_{i=1}^n (\hat{y}_i - y_i) \mathbf{x}_i } $$

**这与线性回归的梯度形式完全一致！** 唯一的区别是 $\hat{y}$ 的计算方式不同（线性回归：$\hat{y} = \mathbf{w}^T\mathbf{x}$；逻辑回归：$\hat{y} = \sigma(\mathbf{w}^T\mathbf{x})$）。

### 2.4 决策边界 (Decision Boundary)

逻辑回归的决策边界是 **$\mathbf{w}^T \mathbf{x} + b = 0$** 对应的超平面：

- $\sigma(\mathbf{w}^T \mathbf{x}) > 0.5 \iff \mathbf{w}^T \mathbf{x} > 0$ → 预测 $y=1$
- $\sigma(\mathbf{w}^T \mathbf{x}) < 0.5 \iff \mathbf{w}^T \mathbf{x} < 0$ → 预测 $y=0$
- $\sigma(\mathbf{w}^T \mathbf{x}) = 0.5$ → 决策边界（分界线）

对于二维特征，决策边界是一条直线。扩展到高维就是超平面。

> **线性可分 vs 非线性：** 逻辑回归的决策边界在特征空间中是线性的。但通过特征变换（如多项式特征），可以拟合非线性边界——这引出了"核方法"的思想。

### 2.5 实现与可视化 (Implementation & Visualization)

请运行 `code/linear_models.py` 中的 `demo_logistic_regression()` 函数，查看：

1. **合成分类数据** — 两类数据点
2. **决策边界** — 模型学到的分类线
3. **Sigmoid 概率曲面** — 决策边界附近的概率变化
4. **损失下降曲线** — 交叉熵随迭代单调递减
5. **scikit-learn 比较** — 自实现与 sklearn 结果一致

---

## 3. 正则化 (Regularization)

### 3.1 过拟合与欠拟合 (Under-fitting vs Over-fitting)

| 状态 | 训练误差 | 测试误差 | 原因 |
|------|---------|---------|------|
| **欠拟合 (Under-fitting)** | 高 | 高 | 模型太简单，无法捕捉数据模式 |
| **恰好 (Just right)** | 低 | 低 | 模型复杂度与数据匹配 |
| **过拟合 (Over-fitting)** | 极低 | 高 | 模型过于复杂，学到了噪声 |

**正则化 (Regularization)** 是防止过拟合的核心技术。它的本质是：**在损失函数中加入对模型复杂度的惩罚项**。

### 3.2 L2 正则化 / Ridge (Ridge Regression)

Ridge 回归的损失函数：

$$ \mathcal{L}_{\text{Ridge}}(\mathbf{w}) = \underbrace{\frac{1}{n} \| \mathbf{y} - X \mathbf{w} \|_2^2}_{\text{数据拟合项}} + \lambda \underbrace{\| \mathbf{w} \|_2^2}_{\text{正则化项}} $$

其中 $\lambda > 0$ 是**正则化系数**，控制惩罚力度。

#### 正规方程修正

$$ \frac{\partial \mathcal{L}_{\text{Ridge}}}{\partial \mathbf{w}} = -\frac{2}{n} X^T(\mathbf{y} - X\mathbf{w}) + 2\lambda \mathbf{w} = 0 $$

$$ \boxed{ \mathbf{w}_{\text{Ridge}}^* = (X^T X + n\lambda I)^{-1} X^T \mathbf{y} } $$

> **数值稳定性：** $X^T X + n\lambda I$ 总是可逆的（即使 $X$ 不是列满秩），这保证了解的存在性。$X^T X$ 本身可能奇异（特征数 > 样本数时），加上 $\lambda I$ 使其正定。

#### L2 正则化的效果

- **权重收缩：** 所有权重都向0收缩，但不会精确为0
- **方差减小，偏差增加：** 以少量偏差为代价大幅降低方差 → 整体测试误差降低
- **降低多重共线性影响：** 使相关特征间的权重分配更稳定

### 3.3 L1 正则化 / Lasso (Lasso Regression)

Lasso 回归的损失函数：

$$ \mathcal{L}_{\text{Lasso}}(\mathbf{w}) = \frac{1}{n} \| \mathbf{y} - X \mathbf{w} \|_2^2 + \lambda \| \mathbf{w} \|_1 $$

其中 $\| \mathbf{w} \|_1 = \sum_{j=1}^d |w_j|$。

#### L1 正则化的关键特性：稀疏性

Lasso 的一个重要特性是它能使**部分权重精确为0**，从而实现**特征选择**。

> **为什么 L1 产生稀疏解而 L2 不？** 这源于 L1 范数的几何形状——详见下节。

由于 L1 范数在 $w_j=0$ 处不可导，优化通常使用**坐标下降 (Coordinate Descent)** 或**近端梯度下降 (Proximal Gradient Descent)**，而非普通梯度下降。

### 3.4 L1 vs L2 — 稀疏性的几何直觉 (Geometric Intuition for Sparsity)

**核心直觉：约束优化视角**

正则化等价于在约束条件下最小化原始损失：

- **Lasso:** $\min \frac{1}{n}\|\mathbf{y} - X\mathbf{w}\|_2^2$ s.t. $\|\mathbf{w}\|_1 \leq t$
- **Ridge:** $\min \frac{1}{n}\|\mathbf{y} - X\mathbf{w}\|_2^2$ s.t. $\|\mathbf{w}\|_2^2 \leq t$

在二维 ($w_1, w_2$) 空间中：
- L2 约束区域是**圆形**
- L1 约束区域是**菱形（顶点在坐标轴上）**

损失函数的等高线（椭圆）与约束区域的切点位置决定了最优解：

| 约束 | 形状 | 切点位置 | 特性 |
|------|------|---------|------|
| **L2 (Ridge)** | 圆 | 大概率不在坐标轴上 | 权重收缩但非零 |
| **L1 (Lasso)** | 菱形 | 顶点（坐标轴上）概率大 | 部分权重精确为0 |

**更精确的论证：** L1 正则化的近端算子 (proximal operator) 是**软阈值 (soft-thresholding)**：

$$ \text{prox}_{\lambda \|\cdot\|_1}(w_j) = \text{sign}(w_j) \cdot \max(|w_j| - \lambda, 0) $$

当 $|w_j| < \lambda$ 时，该算子直接将其置0。而 L2 的近端算子是收缩但不置0：

$$ \text{prox}_{\lambda \|\cdot\|_2^2}(w_j) = \frac{w_j}{1 + 2\lambda} $$

### 3.5 弹性网 (Elastic Net) — 两个世界的优点

结合 L1 和 L2：

$$ \mathcal{L}_{\text{ElasticNet}}(\mathbf{w}) = \frac{1}{n} \| \mathbf{y} - X \mathbf{w} \|_2^2 + \lambda_1 \| \mathbf{w} \|_1 + \lambda_2 \| \mathbf{w} \|_2^2 $$

当特征之间存在**分组相关**时，弹性网通常优于 Lasso（Lasso 在组相关中只随机选一个）。

### 3.6 实践指南 (Practical Guide)

```python
from sklearn.linear_model import LinearRegression, Ridge, Lasso

# 普通线性回归
lr = LinearRegression().fit(X_train, y_train)

# Ridge（L2）
ridge = Ridge(alpha=1.0).fit(X_train, y_train)

# Lasso（L1）  
lasso = Lasso(alpha=0.1).fit(X_train, y_train)
```

> **调参建议：** $\lambda$ (sklearn 中为 `alpha`) 通常用交叉验证选择：`RidgeCV` 和 `LassoCV`。

---

## 4. 三个核心概念 (Three Core Concepts)

本章是本书理解所有后续模型的基石。我们反复使用了三个核心概念，它们将贯穿全书：

### 4.1 参数 (Parameters)

**模型需要学习的"旋钮"。**

| 模型 | 参数 |
|------|------|
| 线性回归 | $\mathbf{w}, b$ — 权重和偏置 |
| 逻辑回归 | $\mathbf{w}, b$ — 同上，只是经过 Sigmoid |
| 神经网络 | 每层的权重矩阵 $W^{[l]}$ 和偏置 $b^{[l]}$ |
| CNN | 卷积核权重 + 全连接层权重 |
| Transformer | $W_Q, W_K, W_V, W_O$ 以及 MLP 权重 |

**核心洞察：** 几乎所有机器学习模型的结构都可以概括为：

$$ \hat{y} = f(\mathbf{x}; \boldsymbol{\theta}) $$

其中 $\boldsymbol{\theta}$ 是参数集，$f$ 是模型函数，$\mathbf{x}$ 是输入。**"学习"就是找到最优的 $\boldsymbol{\theta}$。**

### 4.2 损失 (Loss)

**衡量预测有多"差"的标尺。**

| 任务 | 损失函数 | 公式 |
|------|---------|------|
| 回归 | MSE | $\frac{1}{n}\sum (y_i - \hat{y}_i)^2$ |
| 二分类 | 交叉熵 | $-\frac{1}{n}\sum [y\log\hat{y} + (1-y)\log(1-\hat{y})]$ |
| 多分类 | 交叉熵 | $-\frac{1}{n}\sum\sum y_{ik}\log\hat{y}_{ik}$ |
| 聚类 | K-means 损失 | $\sum \|x_i - \mu_{c_i}\|^2$ |

**核心洞察：** 损失函数的选择取决于任务类型和**数据分布假设**。MSE 假设高斯噪声，交叉熵假设分类分布。选择正确的损失函数比选择模型架构有时候更重要。

### 4.3 梯度 (Gradient)

**指引参数更新方向的信息源。**

> **优化 = 跟随梯度下山**

$$ \boldsymbol{\theta}^{(t+1)} = \boldsymbol{\theta}^{(t)} - \eta \cdot \nabla_{\boldsymbol{\theta}} \mathcal{L}(\boldsymbol{\theta}^{(t)}) $$

这个简单的公式是所有深度学习训练的核心。在后续章节中，我们会看到：
- **反向传播 (Backpropagation)** 如何高效计算深度网络的梯度
- **动量 (Momentum)**、**Adam** 等如何改进梯度下降
- **学习率调度**如何影响收敛

### 4.4 三者的关系

```
参数 θ → 模型预测 ŷ = f(x; θ) → 损失 L(ŷ, y) → 梯度 ∇θL → 更新 θ
   ↑                                                           |
   └────────────────────── 循环 (Epoch) ────────────────────────┘
```

**理解这3个概念 = 理解了机器学习优化的 90%。** 后续所有章节都只是在这个框架上增加：更复杂的参数结构（深度）、更巧妙的损失函数（对比学习、GAN）、更高效的梯度计算方法（自动微分、重参数化）。

---

## 5. 小结 (Summary)

### 5.1 关键公式回顾

| 概念 | 公式 |
|------|------|
| 线性回归模型 | $\hat{y} = \mathbf{w}^T \mathbf{x} + b$ |
| MSE 损失 | $\mathcal{L} = \frac{1}{n} \sum (y_i - \hat{y}_i)^2$ |
| 正规方程 | $\mathbf{w}^* = (X^T X)^{-1} X^T \mathbf{y}$ |
| Sigmoid | $\sigma(z) = \frac{1}{1 + e^{-z}}$ |
| 交叉熵损失 | $\mathcal{L} = -\frac{1}{n}\sum [y\log\hat{y} + (1-y)\log(1-\hat{y})]$ |
| 梯度下降更新 | $\mathbf{w}^{(t+1)} = \mathbf{w}^{(t)} - \eta \nabla \mathcal{L}$ |
| Ridge (L2) | $\mathcal{L} + \lambda \|\mathbf{w}\|_2^2$ |
| Lasso (L1) | $\mathcal{L} + \lambda \|\mathbf{w}\|_1$ |
| 弹性网 | $\mathcal{L} + \lambda_1 \|\mathbf{w}\|_1 + \lambda_2 \|\mathbf{w}\|_2^2$ |

### 5.2 与后续章节的联系

| 后续章节 | 联系 |
|---------|------|
| SVM | 用 hinge loss 替代交叉熵，加入最大间隔思想 |
| 决策树 / 随机森林 | 非线性模型，不使用梯度 |
| 神经网络 | 多层逻辑回归 + 非线性激活函数 |
| CNN | 用卷积核替代全连接权重 |
| Transformer | 自注意力机制 + 位置编码 |
| 生成模型 (GAN/VAE) | 更复杂的参数结构和损失函数 |

### 5.3 动手练习

1. **推导练习：** 从零推导多项式回归（在线性回归中加入 $x^2, x^3$ 特征），写出正规方程
2. **代码练习：** 在 `linear_models.py` 中加入 Elastic Net 正则化的梯度下降实现
3. **直觉练习：** 为什么逻辑回归的梯度形式与线性回归相同？核心区别在哪里？
4. **实验练习：** 在真实数据集（如 sklearn 的 `diabetes`）上比较 LinearRegression, Ridge, Lasso 的性能

---

> **下章预告：** 第2章将介绍**支撑向量机 (SVM)**，在线性模型的基础上引入"最大间隔"的思想，并看到"核技巧"如何让线性模型处理非线性数据。

---

*Last updated: 2026-06-01*
