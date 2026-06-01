# 04 — SVM & Kernel Methods / 支持向量机与核方法

> 支持向量机（Support Vector Machine, SVM）是经典机器学习的巅峰之一。它的核心思想简洁而优美：**找到一个能将两类数据分开且间隔最大的超平面**。而核技巧（Kernel Trick）更让 SVM 能够在不显式计算高维映射的情况下处理非线性分类问题——这一思想深刻影响了后来的核方法（Kernel Methods）乃至高斯过程（Gaussian Processes）。

---

## 1. 最大间隔分类器（Maximum Margin Classifier）

### 1.1 问题设定

假设我们有一个二分类数据集 $\{(\mathbf{x}_i, y_i)\}_{i=1}^n$，其中 $y_i \in \{-1, +1\}$。我们想找到一个**超平面（Hyperplane）**将两类样本分开：

$$w^T \mathbf{x} + b = 0$$

决策规则为：

$$
\hat{y} = \begin{cases}
+1, & w^T \mathbf{x} + b > 0 \\
-1, & w^T \mathbf{x} + b < 0
\end{cases}
$$

### 1.2 什么是间隔？

直观上，可以分开两类的超平面有无数个。但哪一个最好？

```
    两类数据点及多个候选超平面：

    ○ ○ ○           ● ● ●
        \       /
    ○   \  (1) /     ●
      ○   \   /   ●
           \ /
            ×      ← 超平面 (2) 似乎更"居中"
           / \
      ○   /   \   ●
        /       \
    ○ ○ ○           ● ● ●
```

**间隔（Margin）** 定义为：到超平面最近的样本点（即**支持向量，Support Vectors**）到超平面的距离。

- **函数间隔（Functional Margin）**：$\hat{\gamma}_i = y_i (w^T \mathbf{x}_i + b)$，符号表示分类是否正确，绝对值表示"确信度"。
- **几何间隔（Geometric Margin）**：$\gamma_i = \frac{y_i (w^T \mathbf{x}_i + b)}{\|w\|}$，即函数间隔除以 $\|w\|$，表示样本到超平面的**实际欧氏距离**。

最大间隔分类器就是在所有能将数据正确分类的超平面中，选择**几何间隔最大**的那个。

### 1.3 为什么最大化间隔能带来更好的泛化？

这是 SVM 最深刻的理论洞见之一：

1. **结构风险最小化（Structural Risk Minimization）**：大间隔意味着超平面两侧有更大的"缓冲带"，对小扰动更鲁棒。一个小的输入变化不太可能使样本越过决策边界。

2. **VC 维（Vapnik-Chervonenkis Dimension）**：间隔 $\gamma$ 与 VC 维之间存在关系：
   
   $$
   \text{VC-dim} \leq \frac{R^2}{\gamma^2} + 1
   $$
   
   其中 $R$ 是数据分布的半径。间隔越大，VC 维越小，模型的**容量（Capacity）**越低，泛化误差上界越小。

3. **直观理解**：想象两块紧挨着的不同颜色的磁铁——如果你只要求它们被隔开，可以有一万种方式。但如果你要求"隔得越远越好"，这个分隔方案就唯一确定了，而且对新的磁铁位置最不敏感。

> 这是奥卡姆剃刀原则（Occam's Razor）在分类问题上的体现：**在能正确分类所有样本的超平面中，间隔最大的那个是最简单的**。

### 1.4 形式化定义

最大间隔分类器的目标函数：

$$
\max_{w, b} \frac{1}{\|w\|} \quad \text{s.t.} \quad y_i (w^T \mathbf{x}_i + b) \geq 1, \; \forall i
$$

等价地（更方便优化）：

$$
\min_{w, b} \frac{1}{2} \|w\|^2 \quad \text{s.t.} \quad y_i (w^T \mathbf{x}_i + b) \geq 1, \; \forall i
$$

> 这里的约束条件将函数间隔归一化为 1。因为缩放 $w$ 和 $b$ 不会改变超平面本身，我们可以固定 $\hat{\gamma} = 1$ 来简化问题。

---

## 2. 对偶问题（Dual Problem）

### 2.1 为什么要转对偶？

上述优化问题是一个**凸二次规划（Convex Quadratic Programming）**，可以直接求解。但转成对偶形式有两个关键好处：

1. **对偶问题只涉及数据点的内积（Dot Product）**——这为核技巧铺平了道路
2. **对偶形式自然引入了稀疏性**——只有支持向量对应的拉格朗日乘子非零

### 2.2 简要推导（Primal → Lagrangian → Dual）

**Step 1 — 构造拉格朗日函数（Lagrangian）**：

为每个约束引入拉格朗日乘子 $\alpha_i \geq 0$：

$$
\mathcal{L}(w, b, \alpha) = \frac{1}{2} \|w\|^2 - \sum_{i=1}^n \alpha_i \big[y_i (w^T \mathbf{x}_i + b) - 1\big]
$$

**Step 2 — 对原始变量求极小**：

令 $\frac{\partial \mathcal{L}}{\partial w} = 0$ 和 $\frac{\partial \mathcal{L}}{\partial b} = 0$：

$$
w = \sum_{i=1}^n \alpha_i y_i \mathbf{x}_i, \quad \sum_{i=1}^n \alpha_i y_i = 0
$$

**Step 3 — 回代得到对偶问题**：

将 $w$ 的表达式代回 $\mathcal{L}$，消去 $w$ 和 $b$，得到**对偶问题（Dual Problem）**：

$$
\max_{\alpha} \sum_{i=1}^n \alpha_i - \frac{1}{2} \sum_{i=1}^n \sum_{j=1}^n \alpha_i \alpha_j y_i y_j \langle \mathbf{x}_i, \mathbf{x}_j \rangle
$$

$$
\text{s.t.} \quad \alpha_i \geq 0, \; \sum_{i=1}^n \alpha_i y_i = 0
$$

### 2.3 核心洞察

注意对偶问题中，数据点 $\mathbf{x}_i$ 和 $\mathbf{x}_j$ 只以**内积** $\langle \mathbf{x}_i, \mathbf{x}_j \rangle = \mathbf{x}_i^T \mathbf{x}_j$ 的形式出现。这个观察至关重要—它直接引出了核技巧。

此外，KKT 条件（Karush-Kuhn-Tucker Conditions）告诉我们：

$$
\alpha_i \big[y_i (w^T \mathbf{x}_i + b) - 1\big] = 0, \quad \forall i
$$

这意味着 $\alpha_i > 0$ **仅当** $y_i (w^T \mathbf{x}_i + b) = 1$，即样本 $\mathbf{x}_i$ **恰好位于间隔边界上**。这些样本就是**支持向量（Support Vectors）**。其他所有样本的 $\alpha_i = 0$，对模型没有任何影响。

> 这就是 SVM 的**稀疏性（Sparsity）**：最终的决策函数仅由少数支持向量决定。

### 2.4 软间隔（Soft Margin）

当数据不可分时，我们引入**松弛变量（Slack Variable）** $\xi_i \geq 0$ 和惩罚参数 $C$：

$$
\min_{w, b, \xi} \frac{1}{2} \|w\|^2 + C \sum_{i=1}^n \xi_i, \quad \text{s.t.} \quad y_i (w^T \mathbf{x}_i + b) \geq 1 - \xi_i
$$

- $C$ 越大 → 对误分类的惩罚越重 → 决策边界越复杂（可能过拟合）
- $C$ 越小 → 允许更多误分类 → 决策边界更平滑（可能欠拟合）

---

## 3. 核技巧（Kernel Trick）⭐

### 3.1 核心问题

现实世界的数据很少是线性可分的。传统的做法是：将数据映射到高维特征空间 $\phi(\mathbf{x})$，希望在高维空间中数据变得线性可分。

```
  原始空间 (2D)              特征空间 (3D)
  
     ○    ●                    ○
   ○   ○   ●  ●              ○   ○
     ○   ●   ●           →      ○    ●  ●
       ○ ●  ●                    ○ ●   ●
         ●                          ●
        
  两类交织在一起           高维投影后线性可分
```

但直接计算 $\phi(\mathbf{x})$ 可能有三个问题：
1. $\phi$ 的维度可能极高（甚至无穷维）
2. 显式计算和存储高维向量开销巨大
3. 我们其实只关心高维空间中的**内积**，而不是坐标本身

### 3.2 核函数的定义

**核技巧（Kernel Trick）** 的核心洞察是：

> 我们不需要显式地计算 $\phi(\mathbf{x})$，只需要定义一个**核函数（Kernel Function）** $K(\mathbf{x}_i, \mathbf{x}_j) = \langle \phi(\mathbf{x}_i), \phi(\mathbf{x}_j) \rangle$，它直接给出了两个数据点在高维特征空间中的内积。

回想对偶问题的目标函数，只需将内积替换为核函数：

$$
\max_{\alpha} \sum_{i=1}^n \alpha_i - \frac{1}{2} \sum_{i=1}^n \sum_{j=1}^n \alpha_i \alpha_j y_i y_j \; K(\mathbf{x}_i, \mathbf{x}_j)
$$

决策函数也相应地变为：

$$
f(\mathbf{x}) = \sum_{i=1}^n \alpha_i y_i K(\mathbf{x}_i, \mathbf{x}) + b
$$

> **这是整个 SVM 中最重要的公式**。注意我们从头到尾都没有计算 $\phi(\mathbf{x})$，只计算了 $K(\mathbf{x}_i, \mathbf{x}_j)$。

### 3.3 常用核函数

| 核函数 | 公式 | 关键参数 | 特点 |
|:---|:---|:---:|:---|
| **线性核（Linear）** | $K(\mathbf{x}_i, \mathbf{x}_j) = \mathbf{x}_i^T \mathbf{x}_j$ | 无 | 相当于无映射，用于线性可分数据 |
| **多项式核（Polynomial）** | $K(\mathbf{x}_i, \mathbf{x}_j) = (\mathbf{x}_i^T \mathbf{x}_j + c)^d$ | $d$（次数）, $c$（偏置） | 有限维映射，$d$ 控制复杂度 |
| **RBF 核（高斯核）** | $K(\mathbf{x}_i, \mathbf{x}_j) = \exp(-\gamma \|\mathbf{x}_i - \mathbf{x}_j\|^2)$ | $\gamma$ | 映射到无穷维，最常用 |
| **Sigmoid 核** | $K(\mathbf{x}_i, \mathbf{x}_j) = \tanh(\kappa \mathbf{x}_i^T \mathbf{x}_j + \theta)$ | $\kappa, \theta$ | 类似两层神经网络的激活 |

### 3.4 RBF 核详解

**RBF（Radial Basis Function）核**，也称为**高斯核（Gaussian Kernel）**，是实践中使用最广泛的核函数：

$$
K(\mathbf{x}_i, \mathbf{x}_j) = \exp\left(-\gamma \|\mathbf{x}_i - \mathbf{x}_j\|^2\right)
$$

**参数 $\gamma$ 的影响**：
- $\gamma$ **小** → 核函数随距离衰减慢 → 每个样本的影响范围大 → 决策边界平滑 → **欠拟合风险**
- $\gamma$ **大** → 核函数随距离衰减快 → 每个样本只影响其附近区域 → 决策边界曲折 → **过拟合风险**

```
不同 γ 下的决策边界（详见配套代码 svm_demo.py）：

γ = 0.1 (欠拟合)     γ = 1.0 (合适)        γ = 10 (过拟合)
  ╱╲                     ╱ ╲               ╱╱╱╲╲╲
 ╱  ╲    ○  ●          ╱   ╲              ╱╱ ╲╲  ╲
╱    ╲  ○  ●  ●      ╱   ○ ╲ ●          ╱ ○ ╲ ● ╲
╲    ╱  ○ ●  ●       ╲  ○○ ●╱           ╲ ○● ●╱
 ╲  ╱    ●  ○         ╲  ●  ╱            ╲● ○ ╱
  ╲╱                     ╲ ╱               ╲╱╲╱

边界过于平滑，       边界较好地分离          边界紧紧包住
误分类较多           两类数据                每个样本，过拟合
```

**为什么 RBF 核映射到无穷维空间？**

将指数展开：

$$
\exp(-\gamma \|x - x'\|^2) = \exp(-\gamma x^2) \cdot \exp(-\gamma x'^2) \cdot \sum_{k=0}^\infty \frac{(2\gamma x x')^k}{k!}
$$

这意味着 $\phi(x)$ 实际上是一个**无穷维向量**：$\phi(x) = \exp(-\gamma x^2) \cdot \left[1, \sqrt{2\gamma}\, x, \frac{2\gamma}{\sqrt{2!}}\, x^2, \ldots \right]$。

> 这就是核技巧的威力：我们在原始空间中用一行代码计算 $K(\mathbf{x}_i, \mathbf{x}_j)$，却等价于在无穷维空间中计算了两个向量的内积。

### 3.5 Mercer 条件

什么样的函数可以作为核函数？**Mercer 条件（Mercer's Condition）** 给出了答案：对于任意有限个数据点 $\{\mathbf{x}_1, \ldots, \mathbf{x}_n\}$，核矩阵（Kernel Matrix, Gram Matrix）$K_{ij} = K(\mathbf{x}_i, \mathbf{x}_j)$ 必须是**半正定（Positive Semi-definite）**的。

这保证了存在某个特征空间 $\phi$ 使得 $K(\mathbf{x}_i, \mathbf{x}_j) = \langle \phi(\mathbf{x}_i), \phi(\mathbf{x}_j) \rangle$。

### 3.6 核技巧的应用范围

核技巧**不限于 SVM**。任何算法如果其计算只依赖于样本间的内积（即可以写成 $\mathbf{x}_i^T \mathbf{x}_j$ 的形式），就可以用核函数替换内积来实现"核化"（Kernelization）：

- **核感知机（Kernel Perceptron）**
- **核 PCA（Kernel PCA）**
- **核岭回归（Kernel Ridge Regression）**
- **核 K-means（Kernel K-means）**

> 核技巧是"将线性算法推广到非线性"的通用框架。

---

## 4. SVM vs 神经网络（Neural Networks）

### 4.1 哲学对比

| 维度 | SVM | 神经网络 |
|:---|:---|:---|
| **核心思想** | 最大化间隔 + 核技巧 | 层次化特征学习 |
| **优化目标** | 凸优化（保证全局最优） | 非凸优化（可能局部最优） |
| **特征工程** | 依赖核函数的设计 | 自动学习特征表示 |
| **数据效率** | 小样本下表现优异 | 通常需要大量数据 |
| **可解释性** | 支持向量直观可解释 | 黑箱，难以解释 |
| **计算复杂度** | $O(n^2 \sim n^3)$，训练随样本量增长慢 | 可大规模并行，GPU 加速 |

### 4.2 什么时候用 SVM？

- **小样本**（$n < 10^4$）：SVM 通常优于或不输神经网络
- **特征维度高**（$d \gg n$）：如文本分类，SVM 天然擅长
- **需要可解释性**：支持向量提供了模型决策的依据
- **数据量巨大**（$n > 10^5$）：此时 SVM 的二次规划开销过高，神经网络的 minibatch 训练更具优势

### 4.3 有趣的联系

- **SVM 使用 hinge loss + 最大间隔**；神经网络通常使用 cross-entropy loss
- **现代深度学习中的"权重衰减（Weight Decay）"** 本质上就是 SVM 的最大间隔思想的延续
- **最后一个隐藏层的输出**可以看作神经网络学习的特征表示 $\phi(\mathbf{x})$，而输出层则类似于线性 SVM

> 2012 年之前，SVM 是机器学习的主导范式。深度学习崛起后，SVM 在大规模任务上被取代，但它在小样本场景、核方法理论以及可解释性方面的价值仍然不可替代。

---

## 5. 本章小结

| 概念 | 要点 |
|:---|:---|
| **最大间隔分类器** | 找到几何间隔最大的超平面，泛化误差有理论保证 |
| **支持向量** | 仅位于间隔边界上的样本点决定决策边界，其余样本不影响模型 |
| **对偶问题** | 将原始优化转对偶，目标只依赖数据点的内积 |
| **核技巧 ⭐** | 不计算 $\phi(\mathbf{x})$，只计算 $K(\mathbf{x}_i, \mathbf{x}_j)$，等价于高维空间内积 |
| **RBF 核** | $K(\mathbf{x}_i, \mathbf{x}_j) = \exp(-\gamma\|\mathbf{x}_i - \mathbf{x}_j\|^2)$，最常用的核函数 |
| **$\gamma$ 参数** | 小 → 欠拟合（边界平滑）；大 → 过拟合（边界曲折） |
| **$C$ 参数** | 小 → 更大间隔但可能误分类；大 → 更严格分类但可能过拟合 |
| **SVM vs NN** | 小样本选 SVM，大样本选 NN；SVM 凸优化保证全局最优 |

---

## 6. 进一步阅读

- [The Kernel Trick — 直观解释 (YouTube)](https://www.youtube.com/watch?v=Q7vT0--5VII)
- [Support Vector Machines — 3Blue1Brown 可视化讲解](https://www.youtube.com/watch?v=_PwhiWxHK8o)
- [A Tutorial on Support Vector Machines for Pattern Recognition — Burges, 1998](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/svmtutorial.pdf)
- [LIBSVM: A Library for Support Vector Machines — Chih-Chung Chang & Chih-Jen Lin](https://www.csie.ntu.edu.tw/~cjlin/libsvm/)
- [Pattern Recognition and Machine Learning — Christopher Bishop, Chapter 7](https://www.springer.com/gp/book/9780387310732)
- [Scikit-learn SVM 文档 — RBF 参数详解](https://scikit-learn.org/stable/auto_examples/svm/plot_rbf_parameters.html)

---

*下一章：[05 — 树模型与集成方法](./05-tree-and-ensemble.md)*

---

*配套代码：[`svm_demo.py`](./code/svm_demo.py) — SVM 核函数对比实验，RBF 参数 $\gamma$ 的影响可视化，支持向量标注*
