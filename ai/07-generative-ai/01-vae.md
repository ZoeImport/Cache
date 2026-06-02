# 第1章 变分自编码器 (VAE)
# Chapter 1: Variational Autoencoder (VAE)

> **变分（variational /ˌveəriˈeɪʃənl/）自编码器（autoencoder /ˈɔːtoʊənˈkoʊdər/） (VAE)** 是生成模型领域的基石方法，首次将**概率推断**与**深度学习**有机结合。与标准自编码器（encoder /ɪnˈkoʊdər/）将输入压缩为确定性的潜在（latent /ˈleɪtənt/）编码不同，VAE 将输入编码为**概率分布**（均值和方差），从而能够生成全新的数据样本。VAE 的核（kernel /ˈkɜːrnl/）心是**重参数（parameter /pəˈræmɪtər/）化技巧 (Reparameterization Trick)** 和**证据下界 (ELBO)** 的推导。本章还介绍了 VQ-VAE——一种将潜在空间离散化的扩展，有效解决了 VAE 的后验崩塌问题。
> > **时间线**:
> > - **2013**: Kingma & Welling 提出 VAE（变分自编码器）
> > - **2014**: Goodfellow et al. 提出 GAN
> > - **2017**: van den Oord et al. 提出 VQ-VAE
> > - **2020**: Ho, Jain & Abbeel 提出 DDPM
> > - **2021**: Song, Meng & Ermon 提出 DDIM
> - **2022**: Rombach et al. 提出 Stable Diffusion
>
> **The Variational Autoencoder (VAE)** is a cornerstone of generative modeling, being the first method to organically combine **probabilistic inference（/ˈɪnfərəns/）** with **deep learning**. Unlike standard autoencoders that compress inputs into deterministic latent codes, VAEs encode inputs into **probability distributions** (means and variances), enabling the generation of novel data samples. At the heart of VAEs are the **Reparameterization Trick** and the derivation of the **Evidence Lower Bound (ELBO)**. This chapter also introduces VQ-VAE — an extension that discretizes the latent space, effectively addressing the posterior collapse problem.

**前置知识 (Prerequisites):** 概率论（高斯分布、条件概率、KL 散度）、变分推断基础、标准自编码器、PyTorch 基础
**依赖库 (Dependencies):** `torch>=2.1.0`, `torchvision>=0.16.0`, `numpy>=1.24.0`, `matplotlib>=3.7.0`
**Code companion:** [`code/vae.py`](code/vae.py)

---

## 目录 (Table of Contents)

1. [自编码器的局限](#1-自编码器的局限-limitations-of-autoencoders)
2. [潜在变量模型](#2-潜在变量模型-latent-variable-models)
3. [ELBO 推导 ⭐](#3-elbo-推导-elbo-derivation)
4. [重参数化技巧](#4-重参数化技巧-reparameterization-trick)
5. [VAE 损失函数](#5-vae-损失函数-vae-loss-function)
6. [VQ-VAE: 离散潜在空间](#6-vq-vae-离散潜在空间-discrete-latent-space)
7. [代码实战: VAE on MNIST](#7-代码实战-vae-on-mnist)

---

## 1. 自编码器的局限 (Limitations of Autoencoders)

### 1.1 标准自编码器回顾 (Standard Autoencoder Review)

标准自编码器由一个编码器和一个解码器（decoder /diːˈkoʊdər/）组成：

$$ z = f_\phi(x), \quad \hat{x} = g_\theta(z) $$

其中编码器 $f_\phi$ 将输入 $x$ 映射为一个**确定性的潜在编码** $z$，解码器 $g_\theta$ 从 $z$ 重建 $\hat{x}$。

```
Input x  -->  [Encoder]  -->  z (deterministic)  -->  [Decoder]  -->  Reconstructed x̂
```

训练目标是最小化重建误差 $\|x - \hat{x}\|^2$。

### 1.2 关键缺陷 (Key Flaw)

标准自编码器的潜在空间是**非结构化的 (unstructured)**：

- 每一个输入 $x^{(i)}$ 被映射为潜在空间中的一个**点** $z^{(i)}$
- 这些点之间**没有连续性保证**——两个相近的输入可能在潜在空间中相距甚远
- 潜在空间中两个点之间的**插值**往往产生无意义的输出
- **无法从潜在空间采样来生成新数据**——因为不知道哪些区域对应有效的输出

```
Latent Space (Standard AE):
    ·       ·           ← scattered points, no structure
       ·   ·
    ·           ·
         ·       ·
```

**本质问题:** 标准自编码器学习的是一个**确定性映射** $x \to z$，而不是一个**概率分布** $p(z|x)$。没有分布的约束，潜在空间就没有"形状"，无法支持生成。

> **Standard AEs learn a deterministic mapping $x \to z$, not a distribution $p(z|x)$. Without distributional constraints, the latent space has no "shape" and cannot support generation.**

---

## 2. 潜在变量模型 (Latent Variable Models)

### 2.1 核心直觉 (Core Intuition)

潜在变量模型的核心思想是：我们观测到的数据 $x$ 是由一些**未观测到的潜在变量 (latent variables)** $z$ 生成的。$z$ 是 $x$ 的"底层原因 (underlying cause)"。

**生成过程 (Generative Process):**

$$ z \sim p(z), \quad x \sim p(x|z) $$

- $p(z)$: **先验分布 (prior distribution)** — 通常设为标准正态 $\mathcal{N}(0, I)$
- $p(x|z)$: **似然 (likelihood)** — 解码器定义的分布
- $p(z|x)$: **后验分布 (posterior distribution)** — 给定 $x$ 时 $z$ 的条件分布

```
          z (latent cause)
         ↙           ↘
    p(z)              p(x|z)
    (prior)           (likelihood)
                         ↓
                      x (observation)
```

### 2.2 推断问题 (The Inference Problem)

我们需要计算后验 $p(z|x)$，根据贝叶斯定理：

$$ p(z|x) = \frac{p(x|z) \, p(z)}{p(x)} $$

其中**证据 (evidence)** $p(x) = \int p(x|z) \, p(z) \, dz$ 需要对所有可能的 $z$ 积分——这在连续高维空间中通常是**难以处理的 (intractable)**。

**VAE 的解决方案:** 使用一个**推断网络 (inference network)** $q_\phi(z|x)$ 来近似真实后验 $p(z|x)$。这就是**变分推断 (Variational Inference)** 的思路。

---

## 3. ELBO 推导 ⭐ (ELBO Derivation)

这是 VAE 最核心的数学部分。我们一步步推导**证据下界 (Evidence Lower Bound, ELBO)**。

### 3.1 目标: 最大化对数似然 (Goal: Maximize Log-Likelihood)

我们希望最大化观测数据的对数边际似然 $\log p(x)$。对于单个数据点 $x^{(i)}$：

$$ \log p(x^{(i)}) = \log \int p(x^{(i)}|z) \, p(z) \, dz $$

直接优化这个积分是困难的。我们引入一个变分后验 $q_\phi(z|x)$ 来近似真实后验 $p(z|x)$。

### 3.2 引入变分后验 (Introducing the Variational Posterior)

从恒等式开始，将 $\log p(x)$ 分解为两项：

$$ \log p(x) = \mathbb{E}_{z \sim q_\phi(z|x)} \left[ \log \frac{p(x, z)}{q_\phi(z|x)} \right] + \text{KL}(q_\phi(z|x) \parallel p(z|x)) $$

**逐步推导:**

**Step 1:** 将 $p(x)$ 写成对 $z$ 的积分：

$$ p(x) = \int p(x, z) \, dz = \int \frac{p(x, z)}{q_\phi(z|x)} \, q_\phi(z|x) \, dz $$

**Step 2:** 两边取对数：

$$ \log p(x) = \log \int \frac{p(x, z)}{q_\phi(z|x)} \, q_\phi(z|x) \, dz $$

**Step 3:** 利用 **Jensen 不等式** $\log \mathbb{E}[X] \ge \mathbb{E}[\log X]$（因为 $\log$ 是凹函数）：

$$ \log p(x) \ge \int q_\phi(z|x) \log \frac{p(x, z)}{q_\phi(z|x)} \, dz = \mathbb{E}_{z \sim q_\phi(z|x)} \left[ \log \frac{p(x, z)}{q_\phi(z|x)} \right] $$

这就是 **ELBO**。此时我们得到 $\log p(x) \ge \text{ELBO}$。

**Step 4:** 为了得到完整的分解形式，将 $\log p(x)$ 写为 ELBO 与 KL 散度之和：

$$ \begin{aligned}
\log p(x) &= \log p(x) \cdot 1 \\
&= \log p(x) \int q_\phi(z|x) \, dz \\
&= \int q_\phi(z|x) \log p(x) \, dz \\
&= \int q_\phi(z|x) \log \frac{p(x) \, q_\phi(z|x)}{q_\phi(z|x)} \, dz \\
&= \int q_\phi(z|x) \log \frac{p(x, z)}{q_\phi(z|x)} \, dz + \int q_\phi(z|x) \log \frac{q_\phi(z|x)}{p(z|x)} \, dz \\
&= \underbrace{\mathbb{E}_{z \sim q_\phi(z|x)} \left[ \log \frac{p(x, z)}{q_\phi(z|x)} \right]}_{\text{ELBO}} + \underbrace{\text{KL}(q_\phi(z|x) \parallel p(z|x))}_{\ge 0}
\end{aligned} $$

**关键观察:**
- 由于 $\text{KL}(q \parallel p) \ge 0$（KL 散度非负），我们有 $\log p(x) \ge \text{ELBO}$
- 最大化 ELBO 等价于**最大化对数似然的下界**
- 同时，最大化 ELBO 等价于**最小化 $\text{KL}(q_\phi(z|x) \parallel p(z|x))$**，使近似后验逼近真实后验

```
log p(x) = ELBO + KL(q(z|x) || p(z|x))
                ╰── maximizable ──╯   ╰── ≥ 0, unknown ──╯
                
So:  maximize ELBO  →  log p(x) increases (indirectly)
                     + q(z|x) gets closer to p(z|x)
```

### 3.3 ELBO 的两种等价形式 (Two Equivalent Forms of ELBO)

**形式 1 — 从联合分布出发:**

$$ \text{ELBO} = \mathbb{E}_{z \sim q_\phi(z|x)} \left[ \log \frac{p(x, z)}{q_\phi(z|x)} \right] $$

**形式 2 — 分解为重建项 + KL 正则项（最常用）:**

$$ \begin{aligned}
\text{ELBO} &= \mathbb{E}_{z \sim q_\phi(z|x)} \left[ \log \frac{p_\theta(x|z) \, p(z)}{q_\phi(z|x)} \right] \\
&= \mathbb{E}_{z \sim q_\phi(z|x)} \left[ \log p_\theta(x|z) \right] - \text{KL}(q_\phi(z|x) \parallel p(z))
\end{aligned} $$

其中：
- $\mathbb{E}_{z \sim q_\phi(z|x)} \left[ \log p_\theta(x|z) \right]$: **重建项 (Reconstruction Term)** — 衡量解码器从 $z$ 重建 $x$ 的能力
- $\text{KL}(q_\phi(z|x) \parallel p(z))$: **KL 正则项 (KL Regularization（/ˌreɡjələraɪˈzeɪʃən/） Term)** — 约束 $q_\phi(z|x)$ 接近先验 $p(z)$

**推导过程:**

$$ \begin{aligned}
\text{ELBO} &= \int q_\phi(z|x) \log \frac{p_\theta(x|z) \, p(z)}{q_\phi(z|x)} \, dz \\
&= \int q_\phi(z|x) \log p_\theta(x|z) \, dz + \int q_\phi(z|x) \log \frac{p(z)}{q_\phi(z|x)} \, dz \\
&= \mathbb{E}_{z \sim q_\phi(z|x)} \left[ \log p_\theta(x|z) \right] - \text{KL}(q_\phi(z|x) \parallel p(z))
\end{aligned} $$

---

## 4. 重参数化技巧 (Reparameterization Trick)

### 4.1 问题: 采样不可微 (The Problem: Sampling is Non-Differentiable)

编码器输出 $\mu_\phi(x)$ 和 $\sigma_\phi(x)$，然后我们从 $\mathcal{N}(\mu, \sigma^2)$ 采样得到 $z$：

$$ z \sim \mathcal{N}(\mu_\phi(x), \sigma_\phi^2(x)) $$

这个采样操作是**随机（stochastic /stəˈkæstɪk/）的 (stochastic)**，梯度（gradient /ˈɡreɪdiənt/）无法通过采样节点回传。如果我们直接把 $z$ 写成 $\mu + \sigma \cdot \epsilon$ 的形式，这个操作就是可微的。

**错误方式 (采样不可微):**
```
Encoder → μ, σ
       ↓
   Sample z ←─── 随机节点，梯度无法穿过
       ↓
  Decoder → x̂
```

### 4.2 解决方案: 重参数化 (The Solution: Reparameterization)

将随机采样过程分解为：
1. 从标准正态分布采样一个**噪声** $\epsilon \sim \mathcal{N}(0, I)$
2. 通过**确定性变换**得到 $z$：

$$ z = \mu_\phi(x) + \sigma_\phi(x) \odot \epsilon, \quad \epsilon \sim \mathcal{N}(0, I) $$

其中 $\odot$ 表示逐元素乘法 (element-wise multiplication)。

**正确方式 (重参数化后可微):**
```
Encoder → μ, σ
       ↓
   z = μ + σ · ε  ←─── 确定性变换，梯度可穿过
       ↓               ↑
  Decoder → x̂       ε ~ N(0, I)  ←─── 外部噪声
```

**关键点:** 现在 $z$ 对 $\mu$ 和 $\sigma$ 的偏导可以计算：

$$ \frac{\partial z}{\partial \mu} = 1, \quad \frac{\partial z}{\partial \sigma} = \epsilon $$

梯度可以通过 $z$ 回传到编码器的 $\mu$ 和 $\sigma$ 参数。

### 4.3 为什么这样可行？ (Why Does This Work?)

数学上，$\mathcal{N}(\mu, \sigma^2)$ 分布的样本可以通过**位置-尺度变换 (location-scale transform)** 从 $\mathcal{N}(0, 1)$ 生成：

若 $\epsilon \sim \mathcal{N}(0, I)$，则 $z = \mu + \sigma \odot \epsilon \sim \mathcal{N}(\mu, \text{diag}(\sigma^2))$

这种变换将**随机性来源**从模型参数中分离出来，使模型参数 $\mu, \sigma$ 的路径变得确定且可微。

```
Without Reparameterization:    With Reparameterization:
     μ,σ                              μ,σ    ε (external noise)
      |                                |     |
      v                                v     v
   [Sample] ←─ stochastic       z = μ + σ · ε
      |                                |
      v                                v
   [Decoder]                       [Decoder]
   ❌ Gradient blocked              ✅ Gradient flows
```

---

## 5. VAE 损失函数 (VAE Loss Function)

### 5.1 损失定义 (Loss Definition)

VAE 的损失函数直接来自负 ELBO：

$$ \mathcal{L}_{\text{VAE}} = -\text{ELBO} = \underbrace{-\mathbb{E}_{z \sim q_\phi(z|x)} \left[ \log p_\theta(x|z) \right]}_{\text{Reconstruction Loss}} + \underbrace{\text{KL}(q_\phi(z|x) \parallel p(z))}_{\text{KL Loss}} $$

### 5.2 重建损失 (Reconstruction Loss)

对于不同的数据类型，重建损失有不同的形式：

**二值数据 (Binary Data):** 使用伯努利似然，即二元交叉熵（entropy /ˈentrəpi/）

$$ -\log p_\theta(x|z) = -\sum_{i} \left[ x_i \log \hat{x}_i + (1 - x_i) \log (1 - \hat{x}_i) \right] $$

**连续数据 (Continuous Data):** 使用高斯似然，即 MSE

$$ -\log p_\theta(x|z) = \frac{1}{2} \| x - \hat{x} \|^2 + \text{const} $$

对于 MNIST，我们通常将像素值视为 $[0, 1]$ 区间的连续值，使用二元交叉熵（因为像素值可以被解释为"该像素被激活的概率"），或 MSE。

### 5.3 KL 损失 (KL Loss)

当 $q_\phi(z|x) = \mathcal{N}(\mu, \sigma^2 I)$ 且 $p(z) = \mathcal{N}(0, I)$ 时，KL 散度有**闭式解 (closed-form solution)**：

$$ \begin{aligned}
\text{KL}(\mathcal{N}(\mu, \sigma^2) \parallel \mathcal{N}(0, 1)) 
&= \frac{1}{2} \sum_{j=1}^{d} \left( \mu_j^2 + \sigma_j^2 - \log \sigma_j^2 - 1 \right)
\end{aligned} $$

其中 $d$ 是潜在空间的维度。

**推导:**

单个维度 $j$ 的 KL 散度：

$$ \begin{aligned}
\text{KL}(q \parallel p) &= \int q(z) \log \frac{q(z)}{p(z)} \, dz \\
&= \int \frac{1}{\sqrt{2\pi\sigma^2}} e^{-\frac{(z-\mu)^2}{2\sigma^2}} \log \frac{\frac{1}{\sqrt{2\pi\sigma^2}} e^{-\frac{(z-\mu)^2}{2\sigma^2}}}{\frac{1}{\sqrt{2\pi}} e^{-\frac{z^2}{2}}} \, dz \\
&= -\frac{1}{2} \log \sigma^2 - \frac{1}{2} + \frac{1}{2} \mu^2 + \frac{1}{2} \sigma^2 \\
&= \frac{1}{2} (\mu^2 + \sigma^2 - \log \sigma^2 - 1)
\end{aligned} $$

### 5.4 损失函数的作用 (Roles of Each Loss Term)

| 损失项 | 作用 | 影响 |
|--------|------|------|
| **Reconstruction Loss** | 确保 $z$ 保留足够信息以重建 $x$ | 鼓励编码器使用更大的方差来覆盖所有可能的 $z$ |
| **KL Loss** | 约束 $q(z|x)$ 接近 $\mathcal{N}(0, I)$ | 正则化潜在空间，使其结构化和连续 |
| **平衡** | 两者之间的权衡决定了生成质量和重建质量的平衡 | $\beta$-VAE 通过权重 $\beta$ 控制这一平衡 |

---

## 6. VQ-VAE: 离散潜在空间 (Discrete Latent Space)

### 6.1 动机 (Motivation)

标准 VAE 使用连续的潜在空间 $\mathbb{R}^d$，但许多真实数据具有**离散的底层结构 (discrete underlying structure)**：

- 语音中的音素 (phonemes)
- 图像中的物体类别 (object categories)
- 文本中的词 (words)

除此之外，连续 VAE 面临一个严重问题——**后验崩塌 (Posterior Collapse)**：

> **后验崩塌 (Posterior Collapse):** 当解码器足够强大时，它可能学会完全忽略潜在变量 $z$，退化为标准自编码器。此时 $q(z|x) \approx p(z)$，KL 散度趋近于零，潜在空间失去意义。

### 6.2 VQ-VAE 的核心思想 (Core Idea of VQ-VAE)

**VQ-VAE (Vector Quantized VAE)** 使用**离散的潜在空间**，通过**向量量化（quantize /ˈkwɒntaɪz/） (Vector Quantization)** 将编码器输出映射到最近邻的嵌入（embedding /ɪmˈbedɪŋ/）向量。

**架构:**

```
Input x  →  Encoder  →  z_e(x)  (continuous)
                            ↓
                   Nearest-neighbor lookup
                            ↓
              z_q(x) = e_k  where k = argmin_j ||z_e(x) - e_j||
                            ↓
                        Decoder  →  x̂
```

其中 $\{e_1, e_2, \ldots, e_K\}$ 是一个**可学习的嵌入表 (codebook / embedding table)**，$K$ 是离散编码的数量。

### 6.3 VQ-VAE 的训练 (Training VQ-VAE)

VQ-VAE 的损失函数包含三个部分：

$$ \mathcal{L} = \underbrace{\|\text{sg}[z_e(x)] - e\|_2^2}_{\text{codebook loss}} + \underbrace{\beta \|z_e(x) - \text{sg}[e]\|_2^2}_{\text{commitment loss}} + \underbrace{-\log p(x|z_q)}_{\text{reconstruction loss}} $$

其中：
- $\text{sg}[\cdot]$ 表示**停止梯度 (stop-gradient)** 操作
- **codebook loss:** 将嵌入向量 $e$ 拉向编码器输出 $z_e(x)$
- **commitment loss:** 约束编码器输出 $z_e(x)$ 靠近其分配的嵌入向量 $e$
- $\beta$ 控制 commitment 的强度（通常设为 $0.25$）

**前向传播 (Forward Pass):** $z_e(x) \to \text{argmin} \to z_q(x)$（离散选择）

**梯度回传 (Backward Pass):** 梯度直接复制从 $z_q(x)$ 到 $z_e(x)$（直通估计器, straight-through estimator）

```
Forward:    z_e(x)  ----→  argmin  ----→  z_q(x)
                                  ╱
Backward:   z_e(x)  ←---  copy gradient  ←---  z_q(x)
```

### 6.4 VAE vs VQ-VAE 对比 (Comparison)

| 特性 | VAE | VQ-VAE |
|------|-----|--------|
| **潜在空间** | 连续 $\mathbb{R}^d$ | 离散 $\{e_1, \ldots, e_K\}$ |
| **重参数化** | $z = \mu + \sigma \odot \epsilon$ | Straight-through estimator |
| **先验** | $\mathcal{N}(0, I)$ | 离散均匀分布 |
| **后验崩塌** | 常见 | 极少（离散化强制使用潜在变量） |
| **生成的样本质量** | 通常模糊 | 更清晰 |
| **典型应用** | 生成、插值、表示学习 | 图像生成、语音合成、视频生成 |

---

## 7. 代码实战: VAE on MNIST (Code in Action)

完整的 VAE 实现见 [`code/vae.py`](code/vae.py)，涵盖以下功能：

| 功能 | 描述 |
|------|------|
| **VAE 模型** | 编码器 → 重参数化 → 解码器 |
| **训练循环** | 完整训练与日志打印 |
| **潜在空间可视化** | 2D 潜在空间按数字类别着色 |
| **潜在空间插值** | 在两个随机采样之间线性插值生成过渡图像 |
| **先验采样生成** | 从 $\mathcal{N}(0, I)$ 采样并解码 |
| **损失曲线** | Reconstruction Loss / KL Loss / Total Loss 曲线 |

运行方式 (How to Run):

```bash
python code/vae.py                  # 默认训练 20 个 epoch
python code/vae.py --epochs 5       # 训练 5 个 epoch
python code/vae.py --latent-dim 2   # 2 维潜在空间
```

### 实际运行输出 (Actual Console Output)

使用 2 维潜在空间，在 CPU 上训练 5 个 epoch 的输出如下：

```
Using device: cpu
PyTorch version: 2.12.0+cpu

============================================================
VAE Training on MNIST
============================================================
  Epochs:        5
  Batch size:    128
  Latent dim:    2
  Learning rate: 0.001
  Device:        cpu
============================================================

Train samples: 60000
Test samples:  10000

Model parameters: 631,188

Starting training...
------------------------------------------------------------------------
 Epoch |  Train Total |  Train Recon |     Train KL |   Test Total
------------------------------------------------------------------------
     1 |       190.53 |       184.71 |         5.83 |       171.51
     2 |       168.95 |       163.67 |         5.28 |       165.59
     3 |       164.48 |       159.10 |         5.38 |       162.62
     4 |       161.81 |       156.37 |         5.44 |       160.55
     5 |       160.09 |       154.58 |         5.51 |       159.47
------------------------------------------------------------------------
Training complete!

Generating visualizations...
All figures saved to code/output/

============================================================
Final Results
============================================================
  Train Total Loss:  160.09
  Train Recon Loss:  154.58
  Train KL Loss:     5.51
  Test Total Loss:   159.47
============================================================
```

输出文件位于 `code/output/` 目录下：

| 文件 | 描述 |
|------|------|
| `latent_space_epoch_001.png` | 第 1 epoch 后的潜在空间分布 |
| `latent_space_epoch_005.png` | 第 5 epoch 后的潜在空间分布 |
| `interpolation.png` | 潜在空间中两个随机点之间的插值过渡 |
| `generated_samples.png` | 从先验 $\mathcal{N}(0, I)$ 采样生成的 25 张图像 |
| `reconstructions.png` | 原始图像与重建图像的对比 |
| `loss_curves.png` | 训练过程中的损失曲线（Total / Recon / KL） |

## 参考文献 (References)

1. **Kingma, D. P. & Welling, M.** (2014). Auto-encoding variational bayes. *ICLR*.
2. **Goodfellow, I. et al.** (2014). Generative adversarial nets. *NeurIPS*.
3. **Ho, J., Jain, A. & Abbeel, P.** (2020). Denoising diffusion probabilistic models. *NeurIPS*.
4. **Rombach, R. et al.** (2022). High-resolution image synthesis with latent diffusion models. *CVPR*.
