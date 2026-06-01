# 03 — Calculus & Optimization for ML / 微积分与最优化

> 微积分是机器学习的"引擎"。梯度（Gradient）、链式法则（Chain Rule）和梯度下降（Gradient Descent）共同构成了神经网络反向传播（Backpropagation）的理论基础。本章从偏导数的几何意义出发，逐步深入到优化器的直觉理解，为后续学习神经网络打下坚实的微积分基础。

---

## 1. 偏导数与梯度（Partial Derivatives & Gradient）

### 1.1 为什么要从偏导数开始？

在单变量微积分中，导数（Derivative）描述函数在某个点上的**瞬时变化率**：

$$f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$$

但在机器学习中，函数通常有**多个输入变量**。例如线性回归的损失函数 $L(w, b)$ 同时依赖于权重 $w$ 和偏置 $b$。我们需要知道：**调整 $w$ 会怎样改变 L？调整 $b$ 呢？** 这正是**偏导数（Partial Derivative）**要回答的问题。

### 1.2 偏导数的定义

对于一个多变量函数 $f(x_1, x_2, \ldots, x_n)$，它在 $x_i$ 方向上的偏导数是：固定其他变量不变，只让 $x_i$ 变化，观察函数值的变化率：

$$\frac{\partial f}{\partial x_i} = \lim_{h \to 0} \frac{f(x_1, \ldots, x_i+h, \ldots, x_n) - f(x_1, \ldots, x_n)}{h}$$

**直观理解**：想象你站在一个山坡上（山坡就是损失函数曲面）。偏导数 $\frac{\partial f}{\partial x}$ 告诉你向东走时坡度有多陡，$\frac{\partial f}{\partial y}$ 告诉你向北走时坡度有多陡。

### 1.3 梯度 — 最陡上升方向

**梯度（Gradient）** 是一个向量，它将所有偏导数组合在一起：

$$\nabla f = \left( \frac{\partial f}{\partial x_1}, \frac{\partial f}{\partial x_2}, \ldots, \frac{\partial f}{\partial x_n} \right)$$

梯度有两条核心性质：

1. **方向**：梯度指向函数值**增加最快**的方向（最陡上升方向，Steepest Ascent）
2. **大小**：梯度的模 $|\nabla f|$ 表示该方向上的变化率大小

> **为什么梯度指向最陡上升？** 从方向导数（Directional Derivative）的定义出发：函数 $f$ 在单位方向 $\mathbf{u}$ 上的变化率为 $\nabla f \cdot \mathbf{u} = |\nabla f| \cos\theta$。当 $\theta = 0$（即 $\mathbf{u}$ 与 $\nabla f$ 同向）时，变化率最大，等于 $|\nabla f|$。

### 1.4 梯度的可视化

对于一个二维函数 $f(x, y)$（比如 $f(x, y) = x^2 + 2y^2$），梯度在每个点上都指向"最快的上坡方向"：

```
等高线图（Contour Plot）视野：
  y ^
    |   梯度向量 → 垂直于等高线
    |   → 指向函数值增加最快的方向
    |  ╱╲
    | ╱  ╲   ← 椭圆等高线（$x^2 + 2y^2 = const$）
    |╱    ╲
    └─────────────────> x
```

**关键联系**：在 ML 中我们要**最小化**损失函数，因此我们沿着**梯度的反方向**（负梯度，Negative Gradient）更新参数。这就是梯度下降的核心思想。

> 详见配套代码中的等高线可视化。

---

## 2. 链式法则（Chain Rule）

### 2.1 为什么链式法则是反向传播的关键？

**反向传播（Backpropagation）** 本质上就是反复应用链式法则。神经网络将输入 $x$ 经过多层变换得到输出 $\hat{y}$，每一层都是前一层的函数。要计算损失 $L$ 对第一层参数的梯度，我们需要逐步"链式"地求导。

> 没有链式法则，就没有深度学习。这是整章中最重要的知识点。

### 2.2 标量链式法则（Scalar Chain Rule）

最简单的形式：若 $y = f(u)$，$u = g(x)$，则：

$$\frac{dy}{dx} = \frac{dy}{du} \cdot \frac{du}{dx}$$

**示例**：$y = \sin(x^2)$

令 $u = x^2$，$y = \sin(u)$，则：
$$\frac{dy}{dx} = \cos(u) \cdot 2x = 2x \cdot \cos(x^2)$$

### 2.3 多变量链式法则（Multivariable Chain Rule）

当中间变量有多个时，链式法则需要求和。若 $z = f(u_1, u_2, \ldots, u_m)$，且每个 $u_i = g_i(x_1, x_2, \ldots, x_n)$，则：

$$\frac{\partial z}{\partial x_j} = \sum_{i=1}^{m} \frac{\partial z}{\partial u_i} \cdot \frac{\partial u_i}{\partial x_j}$$

**示例**：$z = f(u, v)$ 其中 $u = x^2 y$，$v = x \sin y$

$$\frac{\partial z}{\partial x} = \frac{\partial z}{\partial u} \cdot \frac{\partial u}{\partial x} + \frac{\partial z}{\partial v} \cdot \frac{\partial v}{\partial x}
= \frac{\partial z}{\partial u} \cdot (2xy) + \frac{\partial z}{\partial v} \cdot \sin y$$

$$\frac{\partial z}{\partial y} = \frac{\partial z}{\partial u} \cdot \frac{\partial u}{\partial y} + \frac{\partial z}{\partial v} \cdot \frac{\partial v}{\partial y}
= \frac{\partial z}{\partial u} \cdot (x^2) + \frac{\partial z}{\partial v} \cdot (x \cos y)$$

### 2.4 向量链式法则（Vector Chain Rule）— 面向 ML

在机器学习中，我们处理的通常是向量和矩阵。记 $\mathbf{x} \in \mathbb{R}^n$，$\mathbf{y} = f(\mathbf{x}) \in \mathbb{R}^m$，$z = g(\mathbf{y}) \in \mathbb{R}$，则：

$$\nabla_{\mathbf{x}} z = \left( \frac{\partial \mathbf{y}}{\partial \mathbf{x}} \right)^T \nabla_{\mathbf{y}} z$$

其中 $\frac{\partial \mathbf{y}}{\partial \mathbf{x}}$ 是 **Jacobian 矩阵（雅可比矩阵）**，大小为 $m \times n$：

$$
\frac{\partial \mathbf{y}}{\partial \mathbf{x}} =
\begin{bmatrix}
\frac{\partial y_1}{\partial x_1} & \frac{\partial y_1}{\partial x_2} & \cdots & \frac{\partial y_1}{\partial x_n} \\
\frac{\partial y_2}{\partial x_1} & \frac{\partial y_2}{\partial x_2} & \cdots & \frac{\partial y_2}{\partial x_n} \\
\vdots & \vdots & \ddots & \vdots \\
\frac{\partial y_m}{\partial x_1} & \frac{\partial y_m}{\partial x_2} & \cdots & \frac{\partial y_m}{\partial x_n}
\end{bmatrix}
$$

**具体到神经网络的一个全连接层**：$\mathbf{h} = W\mathbf{x} + \mathbf{b}$，后续有损失 $L$。

已知 $\frac{\partial L}{\partial \mathbf{h}}$，需要求 $\frac{\partial L}{\partial W}$ 和 $\frac{\partial L}{\partial \mathbf{x}}$：

- $\frac{\partial L}{\partial W} = \frac{\partial L}{\partial \mathbf{h}} \cdot \mathbf{x}^T$  （形状：输出梯度 × 输入转置）
- $\frac{\partial L}{\partial \mathbf{x}} = W^T \cdot \frac{\partial L}{\partial \mathbf{h}}$  （形状：权重转置 × 输出梯度）
- $\frac{\partial L}{\partial \mathbf{b}} = \frac{\partial L}{\partial \mathbf{h}}$  （偏置梯度等于输出梯度）

> 记下这三条公式，它们几乎是所有神经网络反向传播的"积木"。

### 2.5 计算图直观（Computation Graph）

**计算图（Computation Graph）** 将链式法则可视化：

```
输入 x → [线性层] → h → [激活函数] → a → [损失函数] → L
           ↑                      ↑
           W, b                  参数
```

反向传播方向（从右向左）：
```
dL/dW = dL/da · da/dh · dh/dW
dL/dx = dL/da · da/dh · dh/dx      ← 继续往前传
```

每个方块都是"局部导数"的乘积，这就是链式法则的图形化表达。

### 2.6 完整示例：线性回归的梯度

假设我们有 MSE 损失 $L = \frac{1}{2}(y - \hat{y})^2$，其中 $\hat{y} = wx + b$。

1. **正向传播（Forward Pass）**：
   - $\hat{y} = wx + b$
   - $L = \frac{1}{2}(y - \hat{y})^2$

2. **反向传播（Backward Pass）**：
   - $\frac{\partial L}{\partial \hat{y}} = \hat{y} - y$  （残差）
   - $\frac{\partial L}{\partial w} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial w} = (\hat{y} - y) \cdot x$
   - $\frac{\partial L}{\partial b} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial b} = \hat{y} - y$

这正好是下一节梯度下降中要用到的梯度公式。

---

## 3. 梯度下降法（Gradient Descent）

### 3.1 核心思想

**梯度下降（Gradient Descent）** 通过反复沿**负梯度**方向更新参数来最小化目标函数：

$$w_{t+1} = w_t - \eta \cdot \nabla L(w_t)$$

其中 $\eta$ 是**学习率（Learning Rate）**，控制每一步的步长。

> **为什么是负梯度？** 因为梯度指向函数值增加最快的方向（最陡上升），所以向反方向移动就是最陡下降（Steepest Descent）。

### 3.2 从泰勒展开推导（Taylor Expansion Derivation）

**为什么沿负梯度方向能保证损失下降？** 用**一阶泰勒展开（First-order Taylor Expansion）**来理解：

$$L(w + \Delta w) \approx L(w) + \nabla L(w)^T \Delta w$$

我们希望 $L(w + \Delta w) < L(w)$，即需要 $\nabla L(w)^T \Delta w < 0$。

设 $\Delta w = -\eta \nabla L(w$（取负梯度方向），其中 $\eta > 0$：

$$\nabla L(w)^T (-\eta \nabla L(w)) = -\eta \|\nabla L(w)\|^2 \leq 0$$

当 $\|\nabla L(w)\| > 0$（不在极值点）时，上式严格小于 0，即损失**一定下降**。

> 这就是梯度下降的数学保证——前提是学习率 $\eta$ 足够小使得泰勒近似成立。

### 3.3 收敛性证明概要（Convergence Proof Sketch）

对于 **凸函数（Convex Function）**（例如 MSE 损失），梯度下降有收敛性保证。

**假设条件**：
1. $L$ 是凸函数
2. $L$ 的梯度是 **L-Lipschitz 连续的**（梯度变化速度有上限）：$\|\nabla L(w) - \nabla L(v)\| \leq L\|w - v\|$
3. 最优值 $L(w^*)$ 存在且有下界

**证明思路**（核心三步）：

**Step 1 — 二次上界**：由 L-Lipschitz 梯度可推导出：

$$L(w_{t+1}) \leq L(w_t) + \nabla L(w_t)^T(w_{t+1} - w_t) + \frac{L}{2}\|w_{t+1} - w_t\|^2$$

**Step 2 — 代入梯度下降更新**：$w_{t+1} = w_t - \eta \nabla L(w_t)$

$$L(w_{t+1}) \leq L(w_t) - \eta\|\nabla L(w_t)\|^2 + \frac{L\eta^2}{2}\|\nabla L(w_t)\|^2
= L(w_t) - \eta\left(1 - \frac{L\eta}{2}\right)\|\nabla L(w_t)\|^2$$

当 $\eta \leq \frac{1}{L}$ 时，$1 - \frac{L\eta}{2} \geq \frac{1}{2} > 0$，每次迭代损失严格下降。

**Step 3 — 收敛速率**：经过 $T$ 次迭代后：

$$L(w_T) - L(w^*) \leq \frac{\|w_0 - w^*\|^2}{2\eta T}$$

这意味着梯度下降以 **$O(1/T)$** 的速率收敛到最优值。迭代次数越多，离最优解越近。

> **直观理解**：如果你每次都朝最陡的下坡方向走一步，并且步长合适，你最终一定会走到山谷底部。凸函数保证只有一个山谷，不会陷入局部最优。

### 3.4 学习率的关键作用（Learning Rate）

学习率 $\eta$ 是梯度下降最重要的超参数。它的影响可以通过下图理解：

```
损失 L(w)
│
│  ╱
│ ╱   η 太小：收敛慢，需要很多步
│╱    →→→→→→→→→→→→→→→
│
│       η 合适：快速稳定下降
│       →→→→→→→→→→
│
│   η 太大：震荡甚至发散
│   ←→←→←→←→←→←→←→←→
└───────────────────────── w
```

**经验法则**：
- $\eta = 0.01$ 或 $0.001$ 是常见起点
- 观察损失曲线：平稳下降 → 可以尝试更大 $\eta$；震荡或发散 → 需要减小 $\eta$
- 实践中常用**学习率调度（Learning Rate Schedule）**：开始时较大，后期逐步减小

### 3.5 三种梯度下降变体

| 变体 | 每次更新使用的样本数 | 特点 |
|:---|:---:|:---|
| **批量梯度下降（BGD）** | 全部样本 | 稳定但慢，不适合大数据集 |
| **随机梯度下降（SGD）** | 1 个样本 | 快但有噪声，收敛路径曲折 |
| **小批量梯度下降（Mini-batch GD）** | 32/64/128 个样本 | 实践中默认选择，平衡速度与稳定性 |

---

## 4. 常用优化器直觉（Optimizer Intuition）

> 这一节不深入数学推导，只建立直觉。每个优化器用一段话解释：**它解决了什么问题**和**关键超参数**。

### 4.1 SGD（Stochastic Gradient Descent）

**解决的问题**：最基本的梯度下降方法。每次从训练集中随机选一个（或一小批）样本来计算梯度并更新参数。

**直觉**：就像蒙着眼睛下山——你只能通过脚下这一小块地方感受坡度，然后迈一步。路径可能很曲折（因为有噪声），但方向总体是对的。

**关键超参数**：`lr`（学习率）——唯一需要调的参数。

$$w_{t+1} = w_t - \eta \nabla L_i(w_t)$$

其中 $L_i$ 是第 $i$ 个样本的损失。

### 4.2 Momentum（动量法）

**解决的问题**：SGD 在峡谷地形（一个方向陡、另一个方向缓）中会剧烈震荡。动量法通过**累积历史梯度**来平滑更新方向。

**直觉**：想象一个小球从山坡上滚下来——它不会在每个凹凸处都急转弯，而是靠着惯性（动量）继续沿主方向前进。动量项 $\beta$ 控制了保留多少"历史速度"：$\beta = 0.9$ 表示保留 90% 的上一步方向，再加 10% 的当前梯度修正。

**关键超参数**：
- `lr`：学习率
- `momentum`（$\beta$）：通常取 0.9 或 0.99

$$v_{t+1} = \beta v_t + \nabla L(w_t)$$
$$w_{t+1} = w_t - \eta v_{t+1}$$

> Momentum 让 SGD 在"正确的方向"上加速，在"震荡的方向"上抵消。

### 4.3 Adam（Adaptive Moment Estimation）

**解决的问题**：不同参数可能需要不同的学习率——频繁更新的特征应该用小步长，稀疏特征应该用大步长。Adam 为**每个参数自适应地调整学习率**。

**直觉**：Adam = Momentum + RMSProp。它同时维护两样东西：
1. **梯度的一阶矩（均值）** → 相当于动量，判断方向
2. **梯度的二阶矩（方差）** → 判断这个参数的历史梯度波动大小，波动大则缩小步长，波动小则放大步长

这就像一个智能的登山者，不仅知道"该往哪个方向走"（动量），还知道"这个方向的可信度有多高"（自适应学习率）。

**关键超参数**：
- `lr`：学习率（默认 0.001 通常工作良好）
- `betas`：($\beta_1, \beta_2$) —— 一阶和二阶矩的衰减率，默认 (0.9, 0.999)
- `eps`：防止除零的小常数，默认 $10^{-8}$

> Adam 是目前最常用的优化器，**通常不需要调参就能获得不错的结果**。它是深度学习的"默认选项"。

### 4.4 优化器对比总结

| 优化器 | 自适应学习率 | 抗震荡 | 内存开销 | 适用场景 |
|:---|:---:|:---:|:---:|:---|
| **SGD** | 否 | 弱 | 低 | 简单任务、调参高手 |
| **SGD + Momentum** | 否 | 中 | 低 | 大部分 CV 任务 |
| **Adam** | 是 | 强 | 中（2x 参数内存） | **默认首选**，NLP、推荐、多模态 |
| **AdamW** | 是 | 强 | 中 | Adam + 正确的权重衰减，Transformer 首选 |

> **何时用 SGD 而非 Adam？** 当你有足够的调参经验和算力时，精心调优的 SGD + Momentum 在某些任务（如图像分类）上可能略优于 Adam。但对初学者而言，**Adam 永远是更安全的选择**。

---

## 5. 本章小结

| 概念 | 要点 |
|:---|:---|
| **偏导数** | 固定其他变量，只对一个变量求导，衡量该方向的变化率 |
| **梯度** | 所有偏导数组成的向量，指向最陡上升方向 |
| **链式法则** | $\frac{\partial L}{\partial w} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial w}$，反向传播的数学基础 |
| **梯度下降** | $w_{t+1} = w_t - \eta \nabla L(w_t)$，沿负梯度方向更新 |
| **学习率 $\eta$** | 步长控制——太小收敛慢，太大可能发散 |
| **Momentum** | 累积历史梯度，平滑更新方向 |
| **Adam** | 自适应学习率 + 动量，默认首选优化器 |

---

## 6. 进一步阅读

- [Gradient Descent — 3Blue1Brown 可视化讲解](https://www.youtube.com/watch?v=IHZwWFHWa-w)
- [Backpropagation Calculus — 3Blue1Brown 链式法则反向传播](https://www.youtube.com/watch?v=tIeHLnjs5U8)
- [An Overview of Gradient Descent Optimization Algorithms — Sebastian Ruder](https://arxiv.org/abs/1609.04747)
- [Adam: A Method for Stochastic Optimization — Kingma & Ba, 2014](https://arxiv.org/abs/1412.6980)
- [Deep Learning Book — Chapter 4 (Numerical Computation) & Chapter 8 (Optimization)](https://www.deeplearningbook.org/)

---

*下一章：[04 — 概率论与统计学基础]()*

---

*配套代码：[`gradient_descent_demo.py`](./code/gradient_descent_demo.py) — 从零实现梯度下降，可视化损失曲线、参数轨迹和学习率对比*
