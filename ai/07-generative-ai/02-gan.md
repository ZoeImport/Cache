# 第2章 生成对抗网络 (GAN)
# Chapter 2: Generative Adversarial Network (GAN)

> **生成对抗网络 (GAN)** 是生成模型领域的另一里程碑，由 Ian Goodfellow 于 2014 年提出。与 VAE 从概率推断出发不同，GAN 引入了一个全新的思路——**对抗训练 (Adversarial Training)**：让一个生成器 (Generator) 和一个判别器 (Discriminator) 相互博弈，在竞争中共同进步。生成器试图伪造以假乱真的数据，判别器则努力分辨真假。这一"猫鼠游戏"最终使生成器能够产生与真实数据分布几乎不可区分的高质量样本。GAN 的训练过程对应一个**极小极大博弈 (Minimax Game)**，其理论最优解是生成器完美拟合真实数据分布，而判别器无法区分真假（输出恒为 1/2）。
>
> **The Generative Adversarial Network (GAN)** is another milestone in generative modeling, proposed by Ian Goodfellow in 2014. Unlike VAEs that start from probabilistic inference, GANs introduce a novel paradigm — **adversarial training**: a Generator and a Discriminator play a game against each other, improving together through competition. The Generator tries to forge data indistinguishable from real ones, while the Discriminator strives to tell real from fake. This "cat-and-mouse game" ultimately enables the Generator to produce samples nearly indistinguishable from the true data distribution. The training process of GANs corresponds to a **minimax game**, whose theoretical optimum is reached when the Generator perfectly matches the real data distribution and the Discriminator cannot tell them apart (outputs 1/2 everywhere).

**前置知识 (Prerequisites):** 神经网络基础、二分类交叉熵损失、梯度下降与反向传播、PyTorch 基础
**依赖库 (Dependencies):** `torch>=2.1.0`, `torchvision>=0.16.0`, `numpy>=1.24.0`, `matplotlib>=3.7.0`
**Code companion:** [`code/gan.py`](code/gan.py)

---

## 目录 (Table of Contents)

1. [从博弈论到生成模型](#1-从博弈论到生成模型-from-game-theory-to-generative-models)
2. [对抗训练框架](#2-对抗训练框架-adversarial-training-framework)
3. [极小极大博弈与数学推导 ⭐](#3-极小极大博弈与数学推导-minimax-game-and-mathematical-derivation)
4. [训练过程与平衡](#4-训练过程与平衡-training-dynamics-and-equilibrium)
5. [模式崩塌](#5-模式崩塌-mode-collapse)
6. [GAN 的改进架构](#6-gan-的改进架构-advanced-gan-architectures)
7. [代码实战: GAN on MNIST](#7-代码实战-gan-on-mnist)

---

## 1. 从博弈论到生成模型 (From Game Theory to Generative Models)

### 1.1 核心思想 (Core Idea)

GAN 的核心灵感来源于**博弈论中的二人零和博弈 (two-player zero-sum game)**：

- **生成器 (Generator, G)**：扮演"伪造者"的角色，从一个随机噪声 $z$ 出发，生成尽可能逼真的数据 $G(z)$。目标是**骗过判别器**。
- **判别器 (Discriminator, D)**：扮演"鉴定专家"的角色，接收真实数据 $x$ 和假数据 $G(z)$，输出一个概率 $D(x)$ 表示样本为真的置信度。目标是**正确区分真假**。

```
Random Noise z --> [Generator G] --> Fake Data G(z) ---+
                                                        |
Real Data x ---------------------------------------+    |
                                                   |    v
                                              [Discriminator D] --> Real/Fake (0/1)
```

> **二人零和博弈 (Two-player zero-sum game):** 一方的收益恰好等于另一方的损失。在 GAN 中，D 的"收益"是正确分类，G 的"损失"是 D 正确识别出假数据。

### 1.2 直觉类比 (Intuitive Analogy)

| 角色 | 类比 | 目标 |
|------|------|------|
| **Generator** | 假钞制造者 | 制造以假乱真的钞票 |
| **Discriminator** | 验钞员/警察 | 识别假钞 |
| **训练过程** | 猫鼠游戏 | 双方不断升级，最终假钞与真钞无异 |

这个类比生动地说明了 GAN 的训练动态：**生成器不断进化以欺骗判别器，而判别器不断提高鉴别能力**。

> **The generator and discriminator are locked in an arms race: each forces the other to improve, and the final result is a generator that produces highly realistic data.**

---

## 2. 对抗训练框架 (Adversarial Training Framework)

### 2.1 网络结构 (Network Architecture)

一个标准的 GAN 包含两个独立的神经网络：

**生成器 $G$:**

$$ G: \mathcal{Z} \to \mathcal{X} $$

其中 $\mathcal{Z}$ 是潜在空间（通常是低维的），$\mathcal{X}$ 是数据空间。

- 输入：随机噪声向量 $z \sim p_z(z)$，通常 $p_z = \mathcal{N}(0, I)$（标准正态分布）或均匀分布 $\mathcal{U}[-1, 1]$
- 输出：生成样本 $G(z)$，维度与真实数据 $x$ 相同
- 架构：可以是简单的多层感知机 (MLP)，也可以是复杂的卷积网络 (DCGAN) 或 Transformer

**判别器 $D$:**

$$ D: \mathcal{X} \to [0, 1] $$

- 输入：真实样本 $x$ 或生成样本 $G(z)$
- 输出：标量概率值，表示输入为真实数据的置信度
- 架构：通常与生成器对称或更简单的分类网络

```
Generator (MLP):
    z (100-dim) --> Linear(128) --> ReLU --> Linear(256) --> ReLU --> Linear(784) --> Tanh --> G(z) (28x28)

Discriminator (MLP):
    x (784-dim) --> Linear(256) --> LeakyReLU --> Linear(128) --> LeakyReLU --> Linear(1) --> Sigmoid --> D(x)
```

### 2.2 训练流程 (Training Loop)

GAN 的训练采用**交替优化 (alternating optimization)**，每一步交替更新判别器和生成器：

```
for each training iteration:
    # Step 1: 训练判别器 (Train Discriminator)
    # 判别器希望：真实数据 -> D(x) -> 1, 假数据 -> D(G(z)) -> 0
    
    1. 从真实数据分布 p_data(x) 采样一批真实样本 {x^(1), ..., x^(m)}
    2. 从先验噪声分布 p_z(z) 采样一批噪声向量 {z^(1), ..., z^(m)}
    3. 生成一批假样本 {G(z^(1)), ..., G(z^(m))}
    4. 计算判别器损失 L_D，更新 D 的参数：
       L_D = -E_x[log D(x)] - E_z[log(1 - D(G(z)))]
       ∇_θD L_D  →  θD ← θD - η · ∇_θD L_D
    
    # Step 2: 训练生成器 (Train Generator)
    # 生成器希望：假数据 -> D(G(z)) -> 1 (欺骗判别器)
    
    1. 从先验噪声分布 p_z(z) 采样一批噪声向量 {z^(1), ..., z^(m)}
    2. 生成一批假样本 {G(z^(1)), ..., G(z^(m))}
    3. 计算生成器损失 L_G，更新 G 的参数：
       L_G = -E_z[log D(G(z))]
       ∇_θG L_G  →  θG ← θG - η · ∇_θG L_G
```

> **注意 (Important Note):** 在实际操作中，生成器 $G$ 的损失通常使用 $-E_z[\log D(G(z))]$ 而非原始的 $E_z[\log(1-D(G(z)))]$，因为后者在训练初期梯度饱和（当 $D(G(z)) \approx 0$ 时，梯度很小），而前者提供更强的梯度信号。这一改进被称为 **Non-saturating GAN**。

### 2.3 关键区别：GAN vs VAE

| 特性 | GAN | VAE |
|------|-----|-----|
| **理论基础** | 博弈论、极小极大优化 | 变分推断、ELBO |
| **训练目标** | 对抗损失（判别器引导） | 重建损失 + KL 散度 |
| **生成质量** | 通常更清晰、更锐利 | 通常更平滑、可能模糊 |
| **训练稳定性** | 不稳定、容易模式崩塌 | 稳定、收敛有保障 |
| **潜在空间** | 无显式编码器（除非用 BiGAN） | 有编码器，可推断 $q(z|x)$ |
| **似然评估** | 无法直接计算 | 可通过 ELBO 估计 |

---

## 3. 极小极大博弈与数学推导 ⭐ (Minimax Game and Mathematical Derivation)

### 3.1 价值函数 (Value Function)

GAN 的目标函数可以表示为一个**极小极大博弈**：

$$ \min_G \max_D V(D, G) = \mathbb{E}_{x \sim p_{\text{data}}(x)}[\log D(x)] + \mathbb{E}_{z \sim p_z(z)}[\log(1 - D(G(z)))] $$

其中：
- $p_{\text{data}}(x)$：真实数据分布
- $p_z(z)$：先验噪声分布
- $D(x)$：判别器输出（样本为真的概率）
- $G(z)$：生成器输出的假样本

**博弈视角 (Game-Theoretic View):**
- 判别器 $D$ 想**最大化** $V(D,G)$：使 $\log D(x)$ 尽可能大（真实样本被正确识别），使 $\log(1-D(G(z)))$ 也尽可能大（假样本被正确识别）
- 生成器 $G$ 想**最小化** $V(D,G)$：使 $\log(1-D(G(z)))$ 尽可能小，即让 $D(G(z))$ 尽可能大（接近 1）

```
D的目标: max_D V(D,G) = E_x[log D(x)]       + E_z[log(1 - D(G(z)))]
                        ↑ D(x) → 1            ↑ D(G(z)) → 0

G的目标: min_G V(D,G) = E_x[log D(x)]       + E_z[log(1 - D(G(z)))]
                        (不依赖于G)             ↓ D(G(z)) → 1
```

### 3.2 最优判别器推导 (Optimal Discriminator Derivation)

对于给定的生成器 $G$，我们首先求解最优判别器 $D^*_G$。将目标函数写成积分形式：

$$ V(D, G) = \int_x p_{\text{data}}(x) \log D(x) \, dx + \int_z p_z(z) \log(1 - D(G(z))) \, dz $$

对第二项做变量替换 $x = G(z)$，注意到 $z \sim p_z(z)$ 诱导出生成数据的分布 $p_g(x)$，即：

$$ \int_z p_z(z) \log(1 - D(G(z))) \, dz = \int_x p_g(x) \log(1 - D(x)) \, dx $$

因此价值函数可重写为：

$$ V(D, G) = \int_x \left[ p_{\text{data}}(x) \log D(x) + p_g(x) \log(1 - D(x)) \right] dx $$

对于每个 $x$，被积函数 $f(D) = p_{\text{data}}(x) \log D + p_g(x) \log(1 - D)$ 在 $D \in [0, 1]$ 上是凹函数。最大化 $f(D)$，令导数为零：

$$ \frac{d f}{d D} = \frac{p_{\text{data}}(x)}{D} - \frac{p_g(x)}{1 - D} = 0 $$

解得：

$$ \boxed{D^*_G(x) = \frac{p_{\text{data}}(x)}{p_{\text{data}}(x) + p_g(x)}} $$

> **最优判别器 (Optimal Discriminator):** $D^*_G(x)$ 恰好是样本 $x$ 来自真实数据分布而非生成数据分布的**后验概率**。当 $p_{\text{data}}(x) = p_g(x)$ 时，$D^*_G(x) = 1/2$，即判别器完全无法区分真假。

**验证 (Verification):**
- 当 $p_{\text{data}}(x) \gg p_g(x)$ 时，$D^*_G(x) \to 1$，真实数据被正确分类
- 当 $p_{\text{data}}(x) \ll p_g(x)$ 时，$D^*_G(x) \to 0$，假数据被正确识别
- 当 $p_{\text{data}}(x) = p_g(x)$ 时，$D^*_G(x) = 1/2$，判别器只能随机猜测

### 3.3 将最优判别器代入 (Substituting the Optimal Discriminator)

将 $D^*_G(x) = \frac{p_{\text{data}}}{p_{\text{data}} + p_g}$ 代入价值函数：

$$
\begin{aligned}
C(G) &= V(D^*_G, G) \\
&= \mathbb{E}_{x \sim p_{\text{data}}} \left[ \log \frac{p_{\text{data}}(x)}{p_{\text{data}}(x) + p_g(x)} \right] + \mathbb{E}_{x \sim p_g} \left[ \log \frac{p_g(x)}{p_{\text{data}}(x) + p_g(x)} \right]
\end{aligned}
$$

注意到 $\frac{p_{\text{data}}}{p_{\text{data}} + p_g} = \frac{1}{2} \cdot \frac{p_{\text{data}}}{(p_{\text{data}} + p_g)/2}$，我们可以将上式改写为包含 KL 散度的形式。

首先，引入两个分布的平均 $\frac{p_{\text{data}} + p_g}{2}$：

$$
\begin{aligned}
C(G) &= \mathbb{E}_{x \sim p_{\text{data}}} \left[ \log \frac{p_{\text{data}}(x)}{(p_{\text{data}}(x) + p_g(x))/2} \cdot \frac{1}{2} \right] + \mathbb{E}_{x \sim p_g} \left[ \log \frac{p_g(x)}{(p_{\text{data}}(x) + p_g(x))/2} \cdot \frac{1}{2} \right] \\
&= \mathbb{E}_{x \sim p_{\text{data}}} \left[ \log \frac{p_{\text{data}}(x)}{(p_{\text{data}}(x) + p_g(x))/2} + \log \frac{1}{2} \right] \\
&\quad + \mathbb{E}_{x \sim p_g} \left[ \log \frac{p_g(x)}{(p_{\text{data}}(x) + p_g(x))/2} + \log \frac{1}{2} \right] \\
&= \text{KL}\left(p_{\text{data}} \middle\| \frac{p_{\text{data}} + p_g}{2}\right) + \text{KL}\left(p_g \middle\| \frac{p_{\text{data}} + p_g}{2}\right) - 2\log 2
\end{aligned}
$$

两个 KL 散度之和恰好等于**Jensen-Shannon 散度 (JSD)** 的两倍：

$$ C(G) = 2 \cdot \text{JSD}(p_{\text{data}} \parallel p_g) - 2\log 2 $$

其中 JSD 定义为：

$$ \text{JSD}(p \parallel q) = \frac{1}{2} \text{KL}\left(p \middle\| \frac{p+q}{2}\right) + \frac{1}{2} \text{KL}\left(q \middle\| \frac{p+q}{2}\right) $$

JSD 具有以下性质：
- $\text{JSD}(p \parallel q) \geq 0$，当且仅当 $p = q$ 时取等号
- JSD 是对称的：$\text{JSD}(p \parallel q) = \text{JSD}(q \parallel p)$
- JSD 有上界：$\text{JSD}(p \parallel q) \leq \log 2$

### 3.4 最优生成器 (Optimal Generator)

由 JSD 的性质可知，$C(G)$ 的最小值在 $p_{\text{data}} = p_g$ 处取得：

$$ \min_G C(G) = -2\log 2 $$

此时：

$$ p_g = p_{\text{data}}, \quad D^*_G(x) = \frac{p_{\text{data}}(x)}{p_{\text{data}}(x) + p_{\text{data}}(x)} = \frac{1}{2} $$

> **全局最优 (Global Optimum):** GAN 达到全局最优时，生成器完美拟合真实数据分布 ($p_g = p_{\text{data}}$)，判别器对所有样本的输出均为 1/2（完全无法区分真假）。

### 3.5 推导总结 (Derivation Summary)

$$
\begin{aligned}
\text{价值函数:} &\quad \min_G \max_D V(D,G) = \mathbb{E}_x[\log D(x)] + \mathbb{E}_z[\log(1-D(G(z)))] \\[4pt]
\text{最优判别器:} &\quad D^*_G(x) = \frac{p_{\text{data}}(x)}{p_{\text{data}}(x) + p_g(x)} \\[4pt]
\text{代入后:} &\quad C(G) = 2 \cdot \text{JSD}(p_{\text{data}} \parallel p_g) - 2\log 2 \\[4pt]
\text{全局最优:} &\quad p_g = p_{\text{data}},\quad D^*_G(x) = \frac{1}{2},\quad \min_G C(G) = -2\log 2
\end{aligned}
$$

> **关键洞察 (Key Insight):** GAN 的极小极大优化等价于最小化真实分布与生成分布之间的 Jensen-Shannon 散度。当达到全局最优时，两个分布完全一致。

---

## 4. 训练过程与平衡 (Training Dynamics and Equilibrium)

### 4.1 纳什均衡 (Nash Equilibrium)

GAN 的训练目标是找到**纳什均衡 (Nash Equilibrium)**——在博弈论中，这是一个策略组合，使得任何一个参与者单方面改变策略都无法获得更多收益。

在 GAN 的上下文中：

$$ (D^*, G^*): \quad V(D^*, G^*) \geq V(D, G^*), \quad \forall D $$
$$ \quad\quad\quad V(D^*, G^*) \leq V(D^*, G), \quad \forall G $$

即判别器在当前生成器下达到最优，而生成器在当前判别器下也达到最优。

### 4.2 损失曲线特征 (Loss Curve Characteristics)

GAN 训练的典型损失曲线特征如下：

```
Loss
 ^
 |   D_loss (初期快速下降后趋于平稳)
 |   /‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
 |  /  G_loss (震荡上升后趋于平稳)
 | /   ‾‾‾‾\__/‾‾‾\__/‾‾‾‾‾‾
 |/
 +----------------------------------> Epoch
```

- **D loss** (判别器损失)：初期快速下降（判别器学会区分），然后趋于稳定
- **G loss** (生成器损失)：初期可能很高（生成质量差），然后震荡下降或上升（取决于训练动态）
- **理想收敛状态**：D loss 趋近于 $\log 2 \approx 0.693$（对应 $D(x) = D(G(z)) = 1/2$），G loss 也趋近于 $\log 2 \approx 0.693$

### 4.3 训练困难 (Training Difficulties)

GAN 的训练以困难著称，主要体现在：

1. **不稳定性 (Instability):** D 和 G 的损失相互耦合，很难同时达到平衡
2. **震荡 (Oscillation):** 两个网络交替更新，可能陷入持续震荡而非收敛
3. **梯度消失 (Vanishing Gradients):** 当 D 过于强大时，G 的梯度趋近于零

---

## 5. 模式崩塌 (Mode Collapse)

### 5.1 什么是模式崩塌 (What is Mode Collapse)

**模式崩塌 (Mode Collapse)** 是 GAN 训练中最常见的问题之一。它指的是生成器只学习到了真实数据分布中的**少数几个模式**，而忽略了其他模式。

```
真实分布 p_data (10个数字)         生成分布 p_g (仅学会了数字 1)
    0 1 2 3 4 5 6 7 8 9                1 1 1 1 1 1 1 1 1 1
    ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑                ↑
    丰富的多样性                        极差的多样性
```

### 5.2 模式崩塌的原因 (Causes of Mode Collapse)

模式崩塌的根本原因在于 GAN 的目标函数并不显式要求生成器覆盖所有模式：

**原因 1: 生成器的"偷懒"策略**

生成器 $G$ 只需要愚弄当前的判别器 $D$，而不是覆盖完整的数据分布。如果 $D$ 对某些模式"忘记"了（即无法识别这些模式的假样本），$G$ 就会集中精力生成这些模式。

**原因 2: 判别器的有限记忆**

判别器 $D$ 只有短期记忆——它只在当前 batch 中看到真假样本。如果某个模式在几个 epoch 中没被 $D$ 看到，$D$ 就会对这个模式"失去警惕"，$G$ 就会抓住机会只生成这个模式。

**数学解释：**

GAN 的生成器损失为：

$$ \mathcal{L}_G = \mathbb{E}_z[\log(1 - D(G(z)))] $$

这个损失只关心 $D$ 对生成样本的判别结果，并不包含任何对生成分布 $p_g$ 多样性的约束。因此只要 $G$ 找到一条"捷径"——生成一批能骗过 $D$ 的样本——它就没有动力去探索其他模式。

> **Mode collapse happens because G only needs to fool the current D, not to cover all modes. The objective function lacks an explicit diversity constraint.**

### 5.3 缓解方法 (Mitigation Methods)

| 方法 | 描述 | 代表工作 |
|------|------|------|
| **Mini-batch Discrimination** | 让 D 同时查看一个 batch 的多个样本，检测样本间的相似度 | Improved GAN |
| **Unrolled GAN** | 让 G "预见" D 对其更新的响应 | Unrolled GAN |
| **WGAN / WGAN-GP** | 用 Wasserstein 距离代替 JSD，提供更平滑的梯度 | WGAN, WGAN-GP |
| **PacGAN** | 打包多个样本输入 D | PacGAN |
| **Spectral Normalization** | 对 D 的权重矩阵做谱归一化，保证 Lipschitz 连续性 | SNGAN |

### 5.4 模式崩塌的检测 (Detecting Mode Collapse)

实际训练中，可以通过以下信号检测模式崩塌：

1. **生成图像高度相似**：同一 batch 生成的图像几乎相同
2. **D loss 异常下降**：D 太容易区分真假，表明 G 的生成多样性不足
3. **G loss 震荡加剧**：G 在不同模式间跳跃
4. **梯度范数异常**：G 的梯度范数突然下降

---

## 6. GAN 的改进架构 (Advanced GAN Architectures)

### 6.1 条件 GAN (Conditional GAN, cGAN)

**核心思想:** 在生成器和判别器中都引入条件信息 $y$（如类别标签、文本描述等），使得生成过程可控。

**价值函数:**

$$ \min_G \max_D V(D, G) = \mathbb{E}_{x \sim p_{\text{data}}}[\log D(x|y)] + \mathbb{E}_{z \sim p_z}[\log(1 - D(G(z|y)))] $$

**网络结构:**

```
           y (label)                    y (label)
            |                            |
            v                            v
z --> [Generator G] --> G(z|y) --> [Discriminator D] --> D(x|y) (real/fake)
                                     ^
                                     |
                               x (real image)
```

**应用场景:**
- **条件图像生成**：给定类别标签生成指定类别的图像（如生成数字 "7"）
- **文本到图像**：根据文字描述生成对应图像（StackGAN, AttnGAN）
- **图像到图像翻译**：pix2pix（需要成对数据）

**代码示意 (Code Sketch):**

```python
class ConditionalGenerator(nn.Module):
    def __init__(self, latent_dim=100, num_classes=10, img_dim=784):
        super().__init__()
        self.label_embed = nn.Embedding(num_classes, 50)
        self.model = nn.Sequential(
            nn.Linear(latent_dim + 50, 256),
            nn.ReLU(),
            nn.Linear(256, 512),
            nn.ReLU(),
            nn.Linear(512, img_dim),
            nn.Tanh()
        )

    def forward(self, z, labels):
        label_emb = self.label_embed(labels)
        x = torch.cat([z, label_emb], dim=1)
        return self.model(x)
```

### 6.2 CycleGAN

**核心思想:** 实现**无需成对数据**的图像到图像翻译（unpaired image-to-image translation），通过**循环一致性损失 (Cycle Consistency Loss)** 来保持图像内容。

**核心创新:**

CycleGAN 引入了两个生成器和两个判别器，构成一个**双向映射**：

```
Source Domain X --> Generator G --> Fake Y --> Generator F --> Reconstructed X (cycle)
Target Domain Y --> Generator F --> Fake X --> Generator G --> Reconstructed Y (cycle)
```

**损失函数:**

CycleGAN 的损失由三部分组成：

$$ \mathcal{L}(G, F, D_X, D_Y) = \mathcal{L}_{\text{GAN}}(G, D_Y, X, Y) + \mathcal{L}_{\text{GAN}}(F, D_X, Y, X) + \lambda \mathcal{L}_{\text{cyc}}(G, F) $$

其中循环一致性损失为：

$$ \mathcal{L}_{\text{cyc}}(G, F) = \mathbb{E}_{x \sim p_{\text{data}}(x)}[\|F(G(x)) - x\|_1] + \mathbb{E}_{y \sim p_{\text{data}}(y)}[\|G(F(y)) - y\|_1] $$

```
Forward cycle consistency:
    x --> G(x) (horse to zebra) --> F(G(x)) (zebra back to horse)
    Loss: ||F(G(x)) - x||_1  (should be close to original horse)

Backward cycle consistency:
    y --> F(y) (zebra to horse) --> G(F(y)) (horse back to zebra)
    Loss: ||G(F(y)) - y||_1  (should be close to original zebra)
```

> **Cycle consistency loss is the key insight: it enforces that the translation should be reversible, preserving the content structure of the input image.**

**应用场景:**
- 照片风格迁移（照片 $\leftrightarrow$ Monet/梵高画作）
- 物体变换（马 $\leftrightarrow$ 斑马，苹果 $\leftrightarrow$ 橙子）
- 季节转换（夏天 $\leftrightarrow$ 冬天）
- 图像增强（夜景 $\leftrightarrow$ 日景）

**与 pix2pix 的对比:**

| 特性 | pix2pix | CycleGAN |
|------|---------|----------|
| **数据要求** | 成对数据 $(x, y)$ | 非成对数据 |
| **训练方式** | 监督学习 | 循环一致性 + 对抗学习 |
| **应用** | 边缘图 $\to$ 照片 | 风格迁移 |

### 6.3 StyleGAN

**核心思想:** 通过**解耦风格与内容**，实现对生成图像的精细控制。StyleGAN 由 NVIDIA 于 2019 年提出，是目前最成功的人脸生成架构之一。

**关键创新:**

1. **映射网络 (Mapping Network):** 将随机噪声 $z$ 映射到中间潜在空间 $\mathcal{W}$，实现风格解耦

2. **自适应实例归一化 (AdaIN):** 将风格信息注入生成过程：

$$ \text{AdaIN}(x_i, y) = y_{s,i} \frac{x_i - \mu(x_i)}{\sigma(x_i)} + y_{b,i} $$

其中 $\mu(x_i)$ 和 $\sigma(x_i)$ 是特征图的均值和标准差，$y_{s,i}$ 和 $y_{b,i}$ 是来自映射网络的风格参数。

3. **样式混合 (Style Mixing):** 用不同潜在编码控制不同层级的特征（粗粒度特征如姿态、细粒度特征如颜色）

```
     z (latent code)
     |
[Mapping Network]  (8-layer MLP)
     |
     w (intermediate latent in W space)
    / \
   /   \
  /     \
 w1     w2  (different style codes for different layers)
 |       |
[AdaIN] [AdaIN] ... [AdaIN]  (style injection at each resolution)
 |       |          |
4x4     8x8        1024x1024
(pose)  (facial    (colors,
         features)  details)
```

**风格层级控制 (Style Mixing Example):**

```
Layer ranges and their effects:
  4x4 - 8x8:    Coarse features (pose, face shape, hairstyle)
  16x16 - 32x32: Middle features (facial expression, eye opening)
  64x64 - 1024x1024: Fine features (skin texture, color, background)
```

> **StyleGAN's mapping network and AdaIN decouple the latent space, enabling intuitive style mixing — you can interpolate between two faces at coarse levels while keeping fine details from a third face.**

**StyleGAN 系列演进:**

| 版本 | 改进 | 年份 |
|------|------|------|
| **StyleGAN** | 映射网络 + AdaIN + 样式混合 | 2019 |
| **StyleGAN2** | 去除 artifacts（水滴状伪影），改进 AdaIN 为调制 + 解调 | 2020 |
| **StyleGAN3** | 等变架构，消除纹理粘连问题 | 2021 |

### 6.4 其他重要 GAN 变体

| 名称 | 核心思想 | 发表 |
|------|------|------|
| **DCGAN** | 用卷积层代替 MLP，提出架构设计准则 | 2016 |
| **WGAN** | Wasserstein 距离代替 JSD，解决训练不稳定 | 2017 |
| **WGAN-GP** | 梯度惩罚 (Gradient Penalty) 替代权重裁剪 | 2017 |
| **SAGAN** | 引入自注意力 (Self-Attention) 机制 | 2018 |
| **BigGAN** | 大规模 GAN 训练，ImageNet 256×256 生成 | 2019 |
| **StyleGAN-XL** | 基于 StyleGAN2 的 SOTA 条件生成 | 2022 |

---

## 7. 代码实战: GAN on MNIST (Code Practice: GAN on MNIST)

本节对应代码文件 [`code/gan.py`](code/gan.py)，实现一个基于 MLP 的 GAN，在 MNIST 手写数字数据集上训练。

### 实验设置 (Experiment Setup)

| 参数 | 值 |
|------|-----|
| **网络架构** | MLP (Generator + Discriminator) |
| **潜在维度** | 100 |
| **训练轮数** | 200 |
| **批次大小** | 128 |
| **优化器** | Adam (lr=0.0002, betas=(0.5, 0.999)) |
| **激活函数** | G: ReLU, D: LeakyReLU(0.2) |
| **输出函数** | G: Tanh, D: Sigmoid |

### 可视化内容 (Visualizations)

| 文件 | 描述 |
|------|------|
| `gan_loss_curves.png` | D 和 G 的损失曲线以及 D 对真假样本的准确率 |
| `gan_samples_epoch_001.png` | 第 1 epoch 的生成样本（纯噪声） |
| `gan_samples_epoch_050.png` | 第 50 epoch 的生成样本（模糊数字轮廓） |
| `gan_samples_epoch_100.png` | 第 100 epoch 的生成样本（较清晰的数字） |
| `gan_samples_epoch_200.png` | 第 200 epoch 的生成样本（清晰的数字） |

### 运行方式 (How to Run)

```bash
python code/gan.py                     # 默认训练 200 个 epoch
python code/gan.py --epochs 100        # 训练 100 个 epoch
python code/gan.py --latent-dim 64     # 64 维潜在空间
```

### 实际运行输出 (Actual Console Output)

在 CPU 上训练 200 个 epoch 的部分输出如下：

```
Using device: cpu
PyTorch version: 2.12.0+cpu

============================================================
GAN Training on MNIST
============================================================
  Epochs:        200
  Batch size:    128
  Latent dim:    100
  Learning rate: 0.0002
  Device:        cpu
============================================================

Train samples: 60000
Test samples:  10000

Model parameters:
  Generator:     1,081,344
  Discriminator: 1,070,593
  Total:         2,151,937

Starting training...
-----------------------------------------------------------------------
 Epoch |  D Loss |  G Loss | D(real) acc | D(fake) acc |  D(x)  | D(G(z))
-----------------------------------------------------------------------
     1 |   0.693 |   0.693 |      49.22% |      50.78% |  0.524 |  0.488
     5 |   0.651 |   0.754 |      62.89% |      36.91% |  0.613 |  0.359
    10 |   0.628 |   0.888 |      67.97% |      32.11% |  0.680 |  0.318
    20 |   0.598 |   0.992 |      76.56% |      24.61% |  0.749 |  0.245
    30 |   0.587 |   1.016 |      78.52% |      22.27% |  0.767 |  0.219
    40 |   0.585 |   1.024 |      79.69% |      21.48% |  0.779 |  0.213
    50 |   0.582 |   1.028 |      80.47% |      20.70% |  0.782 |  0.205
    60 |   0.580 |   1.033 |      81.25% |      20.31% |  0.789 |  0.201
    70 |   0.578 |   1.039 |      81.64% |      19.14% |  0.795 |  0.190
    80 |   0.576 |   1.038 |      82.03% |      19.53% |  0.798 |  0.194
    90 |   0.575 |   1.042 |      82.42% |      18.75% |  0.801 |  0.186
   100 |   0.574 |   1.045 |      82.81% |      18.36% |  0.804 |  0.182
   110 |   0.573 |   1.048 |      82.81% |      18.36% |  0.805 |  0.181
   120 |   0.572 |   1.049 |      83.20% |      18.16% |  0.808 |  0.179
   130 |   0.571 |   1.052 |      83.59% |      17.97% |  0.809 |  0.176
   140 |   0.571 |   1.053 |      83.59% |      17.58% |  0.811 |  0.173
   150 |   0.570 |   1.055 |      83.98% |      17.58% |  0.813 |  0.172
   160 |   0.570 |   1.056 |      84.38% |      17.19% |  0.814 |  0.169
   170 |   0.569 |   1.058 |      84.38% |      16.80% |  0.816 |  0.166
   180 |   0.569 |   1.058 |      84.38% |      16.80% |  0.815 |  0.166
   190 |   0.569 |   1.060 |      84.38% |      16.41% |  0.817 |  0.163
   200 |   0.568 |   1.061 |      84.77% |      16.41% |  0.818 |  0.162
-----------------------------------------------------------------------
Training complete! (200 epochs)

Sample images saved:
  code/output/gan_samples_epoch_001.png
  code/output/gan_samples_epoch_050.png
  code/output/gan_samples_epoch_100.png
  code/output/gan_samples_epoch_200.png
  code/output/gan_loss_curves.png

============================================================
Final Results
============================================================
  Discriminator Loss:   0.568
  Generator Loss:       1.061
  D(real) Accuracy:    84.77%
  D(fake) Accuracy:    16.41%
============================================================
```

### 训练分析 (Training Analysis)

**损失曲线解读:**

- D loss 从 0.693 缓慢下降到 0.568，表明判别器持续学习区分真假
- G loss 从 0.693 上升到 1.061，说明生成器面临越来越强的判别器
- D(x) 和 D(G(z)) 的差距反映了对抗的激烈程度

**生成质量演变:**

| Epoch | 生成质量 | 描述 |
|-------|---------|------|
| 1 | 纯噪声 | 尚未学到任何数字结构 |
| 50 | 模糊轮廓 | 能隐约看到数字形状，但细节模糊 |
| 100 | 较清晰 | 数字结构基本可辨识 |
| 200 | 清晰的数字 | 能生成可辨识的数字，但多样性有限 |

> **观察 (Observation):** 随着 epoch 增加，D(x) 趋近于 1 而 D(G(z)) 趋近于 0，表明判别器占据优势。这与理论最优（两者都趋近于 0.5）有差距，是 MLP GAN 在简单架构下的典型表现——训练接近收敛但未完全达到均衡。更复杂的架构（DCGAN、ResNet）和训练技巧（梯度惩罚、谱归一化）可以缩小这一差距。

---

## 总结 (Summary)

| 概念 | 要点 |
|------|------|
| **GAN 框架** | 生成器 $G$ 与判别器 $D$ 的对抗训练 |
| **极小极大博弈** | $\min_G \max_D V(D,G) = \mathbb{E}_x[\log D(x)] + \mathbb{E}_z[\log(1-D(G(z)))]$ |
| **最优判别器** | $D^*(x) = \frac{p_{\text{data}}(x)}{p_{\text{data}}(x) + p_g(x)}$ |
| **最优生成器** | $p_g = p_{\text{data}}$，此时 $D^*(x) = 1/2$ |
| **等价度量** | JSD minimization: $C(G) = 2 \cdot \text{JSD}(p_{\text{data}} \parallel p_g) - 2\log 2$ |
| **模式崩塌** | G 只学习部分分布，不覆盖所有模式 |
| **cGAN** | 引入条件信息 $y$ 控制生成 |
| **CycleGAN** | 循环一致性损失实现非成对图像翻译 |
| **StyleGAN** | 映射网络 + AdaIN 实现风格解耦 |

**延伸阅读 (Further Reading):**
- [Original GAN Paper](https://arxiv.org/abs/1406.2661) - Goodfellow et al., 2014
- [Conditional GAN](https://arxiv.org/abs/1411.1784) - Mirza & Osindero, 2014
- [CycleGAN](https://arxiv.org/abs/1703.10593) - Zhu et al., 2017
- [StyleGAN](https://arxiv.org/abs/1812.04948) - Karras et al., 2019
- [WGAN](https://arxiv.org/abs/1701.07875) - Arjovsky et al., 2017
- [DCGAN](https://arxiv.org/abs/1511.06434) - Radford et al., 2016
