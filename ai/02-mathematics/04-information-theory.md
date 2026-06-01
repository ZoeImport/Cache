# 04 — 信息论与机器学习（Information Theory for ML）

> 信息论（Information Theory）由 Claude Shannon 于 1948 年创立，最初用于解决通信工程中的信息量化问题。但它的核心工具——熵（Entropy）、KL 散度（KL Divergence）、互信息（Mutual Information）——如今已经成为机器学习中不可或缺的理论基石。本章从"信息量"的直觉出发，推导出熵、KL 散度与交叉熵之间的逻辑链条，最终揭示为什么分类问题的损失函数（Cross-Entropy Loss）本质上就是一个信息论问题。
>
> 本章的层层递进路线：**自信息 → 熵 → KL 散度 → 交叉熵 → ML 损失函数 → 互信息**

---

## 1. 自信息与熵（Self-Information & Entropy）

### 1.1 自信息：衡量"惊讶程度"

直觉上，一个**小概率事件**发生时，我们获得的"信息量"更大——因为它更出乎意料。反之，一个几乎必然发生的事件几乎不传递信息。比如：

- "明天太阳会升起" → 几乎不传递信息（概率 ≈ 1）
- "明天有日食" → 传递了大量信息（概率很小）

Shannon 将**自信息（Self-Information）** 定义为：

$$I(x) = -\log P(x)$$

其中 $P(x)$ 是事件 $x$ 发生的概率。对数底数通常取 2（单位为 **比特，bit**）或 $e$（单位为 **奈特，nat**）。

**为什么取负对数？**
- **单调性**：概率越小，信息量越大（$\lim_{P\to 0^+} I(x) = \infty$）
- **可加性**：独立事件的信息量相加：$I(x,y) = -\log[P(x)P(y)] = I(x) + I(y)$
- **非负性**：$P(x) \in [0,1]$，所以 $-\log P(x) \ge 0$

```python
import numpy as np

def self_info(p, base=2):
    """计算自信息（Self-Information）"""
    return -np.log(p) / np.log(base)

# 例子
print(f"P=0.5  → I = {self_info(0.5):.2f} bit")    # 1 bit
print(f"P=0.1  → I = {self_info(0.1):.2f} bit")    # 3.32 bit
print(f"P=0.9  → I = {self_info(0.9):.2f} bit")    # 0.15 bit
```

> 详见配套代码 `information_demo.py` 中的 `demo_self_information()`。

### 1.2 熵：分布的平均不确定性

**熵（Entropy）** 是自信息的期望值，它衡量一个随机变量 $X$ 的**平均不确定性**：

$$H(X) = \mathbb{E}_{x \sim P}[I(x)] = -\sum_{x} P(x) \log P(x)$$

对于连续随机变量，求和变为积分：

$$H(X) = -\int P(x) \log P(x) \, dx$$

**直觉**：熵越大，分布越"随机"；熵越小，分布越"确定"。

| 分布 | 熵大小 | 直觉 |
|:---|:---:|:---|
| 确定性分布 $P=[1,0,0,\dots]$ | $H=0$ | 毫无不确定性 |
| 均匀分布（$n$ 个取值） | $H=\log n$ | 最大不确定性 |
| 偏斜分布（接近 0 或 1） | 较小 | 比较确定 |

**抛硬币的例子**：考虑一枚参数为 $p$ 的伯努利分布硬币：

$$H(p) = -p\log p - (1-p)\log(1-p)$$

- $p=0$ 或 $p=1$ 时，$H=0$ —— 结果完全确定
- $p=0.5$ 时，$H=1$ bit —— 不确定性最大

```python
def entropy_binary(p):
    """二值分布的熵"""
    if p == 0 or p == 1:
        return 0.0
    return -p * np.log2(p) - (1-p) * np.log2(1-p)
```

> 详见配套代码 `information_demo.py` 中的 `demo_entropy_coin()`，该函数绘制了熵随 $p$ 变化的曲线——呈现漂亮的倒 U 形，在 $p=0.5$ 处取最大值。

---

## 2. KL 散度（Kullback–Leibler Divergence）

### 2.1 定义与直觉

**KL 散度**，又称**相对熵（Relative Entropy）**，用于衡量两个概率分布 $P$ 和 $Q$ 之间的**差异**：

$$D_{KL}(P \parallel Q) = \sum_{x} P(x) \log \frac{P(x)}{Q(x)}$$

**直觉解读**："如果用分布 $Q$ 来近似 $P$，平均需要额外多少信息量（以 bit 为单位）？"

换成编码的视角：若真实分布是 $P$，但你用 $Q$ 来设计最优编码，那么 $D_{KL}(P \parallel Q)$ 就是平均每条消息多出来的编码长度。

### 2.2 重要性质

1. **非负性**：$D_{KL}(P \parallel Q) \ge 0$，等号成立当且仅当 $P=Q$（**Gibbs 不等式**）
2. **不对称性**：$D_{KL}(P \parallel Q) \neq D_{KL}(Q \parallel P)$ —— 所以它不是"距离度量"
3. **无上界**：当 $Q(x)=0$ 但 $P(x)>0$ 时，$D_{KL}(P \parallel Q)=\infty$

**非对称性的直观理解**：
- $D_{KL}(P \parallel Q)$：以 $P$ 为"真相"，衡量 $Q$ 的近似代价
- $D_{KL}(Q \parallel P)$：以 $Q$ 为"真相"，衡量 $P$ 的近似代价

在机器学习中，我们通常最小化 $D_{KL}(P_{\text{data}} \parallel P_{\text{model}})$，即让模型分布尽量接近数据分布。

### 2.3 两个高斯分布之间的 KL 散度

对于两个 $d$ 维高斯分布 $P = \mathcal{N}(\mu_1, \Sigma_1)$ 和 $Q = \mathcal{N}(\mu_2, \Sigma_2)$，有闭式解：

$$
\begin{aligned}
D_{KL}(P \parallel Q) &= \frac{1}{2}\Big[ \log\frac{|\Sigma_2|}{|\Sigma_1|} - d + \text{tr}(\Sigma_2^{-1}\Sigma_1) \\
&\quad + (\mu_2 - \mu_1)^\top \Sigma_2^{-1} (\mu_2 - \mu_1) \Big]
\end{aligned}
$$

当 $\Sigma_1 = \Sigma_2 = I$（单位矩阵）时简化为：

$$D_{KL}(P \parallel Q) = \frac{1}{2} \|\mu_1 - \mu_2\|^2$$

即对称的欧氏距离的一半。

> 详见配套代码 `information_demo.py` 中的 `demo_kl_gaussian()`。

---

## 3. 交叉熵（Cross-Entropy）

### 3.1 定义

**交叉熵（Cross-Entropy）** $H(P, Q)$ 定义为：

$$H(P, Q) = -\sum_{x} P(x) \log Q(x)$$

### 3.2 与熵和 KL 散度的关系——核心推导

这是信息论与 ML 之间最关键的一环：

$$
\begin{aligned}
H(P, Q) &= -\sum_x P(x) \log Q(x) \\
&= -\sum_x P(x) \log P(x) \;+\; \sum_x P(x) \log \frac{P(x)}{Q(x)} \\
&= H(P) \;+\; D_{KL}(P \parallel Q)
\end{aligned}
$$

即：

$$\boxed{H(P, Q) = H(P) + D_{KL}(P \parallel Q)}$$

**含义**：交叉熵 = 真实分布的熵 + 用 $Q$ 近似 $P$ 的额外代价（KL 散度）。

### 3.3 为什么分类损失函数是交叉熵？

在分类任务中：
- $P$ = **真实数据分布**（one-hot 标签分布，$y$）
- $Q$ = **模型预测分布**（$\hat{y}$ 或 $p$）

由于 $P$ 是 one-hot（如 $[1,0,0]$），$H(P) = -1\cdot\log 1 = 0$，因此：

$$
H(P, Q) = \underbrace{H(P)}_{=0} + D_{KL}(P \parallel Q) = D_{KL}(P \parallel Q)
$$

但更重要的是：**最小化交叉熵等价于最小化 KL 散度**。

$$
\arg\min_{Q} H(P, Q) \; \equiv \; \arg\min_{Q} D_{KL}(P \parallel Q)
$$

因为 $H(P)$ 仅由真实分布决定，与模型参数无关。所以：

> **最小化交叉熵 = 最小化 KL 散度 = 让模型分布匹配数据分布**

这就是为什么在 PyTorch/TensorFlow 中，分类损失都使用 `nn.CrossEntropyLoss` —— 它本质上是信息论在 ML 中的直接应用。

对于一个样本 $i$ 的交叉熵损失：

$$\mathcal{L}_i = -\sum_{c=1}^{C} y_{i,c} \log(p_{i,c})$$

其中 $C$ 是类别数，$y_{i,c} \in \{0,1\}$ 是标签，$p_{i,c}$ 是模型预测的概率。

---

## 4. 互信息（Mutual Information）

### 4.1 定义与直觉

**互信息（Mutual Information, MI）** 衡量两个随机变量 $X$ 和 $Y$ 之间的**相互依赖程度**：

$$I(X; Y) = H(X) - H(X \mid Y)$$

其中 $H(X \mid Y)$ 是给定 $Y$ 后 $X$ 的**条件熵（Conditional Entropy）**。

**直觉**："知道 $Y$ 能在多大程度上减少对 $X$ 的不确定性。"

- $I(X; Y) = 0$ 当且仅当 $X$ 和 $Y$ **独立**
- $I(X; Y)$ 越大，$X$ 和 $Y$ 的关联越强

### 4.2 等价形式

互信息可以等价地表示为 KL 散度的形式：

$$I(X; Y) = D_{KL}\big(P(X,Y) \parallel P(X)P(Y)\big)$$

即"联合分布与独立分布乘积之间的 KL 散度"。如果 $X$ 和 $Y$ 独立，则 $P(X,Y) = P(X)P(Y)$，KL 散度为 0。

还可以写成对称形式：

$$I(X; Y) = H(X) + H(Y) - H(X, Y)$$

### 4.3 在特征选择中的应用

互信息在 ML 中的一个经典应用是**特征选择（Feature Selection）**。思路：

1. 计算每个特征 $f_i$ 与目标标签 $y$ 的互信息 $I(f_i; y)$
2. 互信息越大的特征越"有用"（包含更多关于标签的信息）
3. 选择 Top-k 个互信息最大的特征

**对比相关系数**：
| 方法 | 能捕捉非线性关系？ | 适用范围 |
|:---|:---:|:---|
| 皮尔逊相关系数 | ❌ 只能捕捉线性 | 连续变量 |
| 互信息 | ✅ 任意关系 | 任意变量 |

```python
from sklearn.feature_selection import mutual_info_classif

# X: 特征矩阵, y: 标签
mi_scores = mutual_info_classif(X, y)
top_features = np.argsort(mi_scores)[-5:]  # Top-5 特征
```

> 详见配套代码 `information_demo.py` 中的 `demo_mutual_info_selection()`。

---

## 5. 核心推导链总结

整个章节的逻辑可以概括为一条推导链：

$$
\boxed{
\begin{aligned}
&\text{自信息: } I(x)=-\log P(x) \\
&\xrightarrow{\text{期望}} \text{熵: } H(X)=-\sum P(x)\log P(x) \\
&\xrightarrow{\text{两个分布}} \text{KL 散度: } D_{KL}(P\|Q)=\sum P(x)\log\frac{P(x)}{Q(x)} \\
&\xrightarrow{H(P,Q)=H(P)+D_{KL}(P\|Q)} \text{交叉熵: } H(P,Q)=-\sum P(x)\log Q(x) \\
&\xrightarrow{H(P)=0\text{ (one-hot)}} \text{ML 损失: } \mathcal{L}=-\sum y_i\log\hat{y}_i \\
&\xrightarrow{\text{扩展到联合分布}} \text{互信息: } I(X;Y)=H(X)-H(X|Y)
\end{aligned}
}
$$

**核心结论**：机器学习中的分类损失函数（Cross-Entropy Loss）本质上是让模型分布逼近数据分布——这正是信息论中最小化 KL 散度的过程。

---

## 6. 关键术语与符号对照

| 符号 | 名称 | 公式 | ML 对应含义 |
|:---|:---|:---|:---|
| $I(x)$ | 自信息 (Self-Information) | $-\log P(x)$ | 单个预测的"惊讶度" |
| $H(X)$ | 熵 (Entropy) | $-\sum P(x)\log P(x)$ | 数据集的固有不确定性 |
| $D_{KL}(P\|Q)$ | KL 散度 (KL Divergence) | $\sum P(x)\log\frac{P(x)}{Q(x)}$ | 模型与数据的"距离" |
| $H(P,Q)$ | 交叉熵 (Cross-Entropy) | $-\sum P(x)\log Q(x)$ | 分类损失函数 |
| $I(X;Y)$ | 互信息 (Mutual Information) | $H(X)-H(X\|Y)$ | 特征与标签的关联强度 |

---

## 参考文献

1. Shannon, C. E. (1948). *A Mathematical Theory of Communication*. Bell System Technical Journal.
2. Cover, T. M. & Thomas, J. A. (2006). *Elements of Information Theory* (2nd ed.). Wiley-Interscience.
3. MacKay, D. J. C. (2003). *Information Theory, Inference, and Learning Algorithms*. Cambridge University Press.
4. Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer.
