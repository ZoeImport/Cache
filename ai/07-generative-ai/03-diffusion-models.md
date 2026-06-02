# 第3章 扩散模型
# Chapter 3: Diffusion Models

> **扩散模型 (Diffusion Models)** 是一类受非平衡热力学启发的生成模型。它们通过逐步向数据添加噪声（前向过程），然后学习逐步去噪（反向过程）来生成数据。DDPM 奠定了扩散模型的理论基础，DDIM 实现了加速采样，而潜在扩散模型 (LDM) 让扩散模型在图像生成领域大放异彩——Stable Diffusion 正是其代表。
>
> **Diffusion Models** are a class of generative models inspired by non-equilibrium thermodynamics. They generate data by progressively adding noise to data (forward process) and then learning to denoise step by step (reverse process). DDPM laid the theoretical foundation, DDIM achieved accelerated sampling, and Latent Diffusion Models (LDM) brought diffusion models to the forefront of image generation — with Stable Diffusion as their flagship.

**前置知识 (Prerequisites):** 概率论（高斯分布、条件概率、KL 散度）、变分推断、VAE、PyTorch 基础
**依赖库 (Dependencies):** `torch>=2.0.0`, `numpy>=1.21.0`, `matplotlib>=3.4.0`
**Code companion:** [`code/diffusion_demo.py`](code/diffusion_demo.py)

---

## 目录 (Table of Contents)

1. [前向扩散过程](#1-前向扩散过程-forward-diffusion-process)
2. [反向去噪过程](#2-反向去噪过程-reverse-denosing-process)
3. [DDPM 推导](#3-ddpm-推导-ddpm-derivation)
4. [DDIM: 确定性加速采样](#4-ddim-确定性加速采样-deterministic-accelerated-sampling)
5. [潜在扩散模型](#5-潜在扩散模型-latent-diffusion-models)
6. [代码实战: 2D 扩散模型](#6-代码实战-2d-扩散模型-code-in-action)

---

## 1. 前向扩散过程 (Forward Diffusion Process)

### 1.1 定义 (Definition)

前向过程是一个**马尔可夫链 (Markov chain)**，逐步向数据 $x_0 \sim q(x_0)$ 添加高斯噪声，经过 $T$ 步后得到纯噪声 $x_T \sim \mathcal{N}(0, I)$：

$$ q(x_{1:T} \mid x_0) := \prod_{t=1}^{T} q(x_t \mid x_{t-1}) $$

其中每一步的转移核为：

$$ q(x_t \mid x_{t-1}) := \mathcal{N}(x_t; \sqrt{1 - \beta_t} \, x_{t-1}, \beta_t I) $$

**参数：**
- $\beta_t \in (0, 1)$: 每步的噪声调度 (noise schedule)，通常 $T = 1000$
- $\beta_1$ 很小（$\sim 10^{-4}$），$\beta_T$ 较大（$\sim 0.02$），即**线性增长**或**余弦调度**
- 当 $T$ 足够大且 $\beta_t$ 足够小时，$q(x_T) \approx \mathcal{N}(0, I)$

```ascii
Forward Diffusion: x₀ ──→ x₁ ──→ x₂ ──→ ... ──→ x_T
                   q(x₁|x₀)  q(x₂|x₁)         q(x_T|x_{T-1})
                   
x₀ (data)      x_{t/2} (partially noised)    x_T (pure noise)
   ████            ██░░                            ░░░░
   ████     →      ██░░             →              ░░░░
   ████            ██░░                            ░░░░
```

### 1.2 重参数化技巧 (Reparameterization Trick)

利用高斯分布的性质，我们可以直接从 $x_0$ 采样任意 $x_t$，无需迭代 $t$ 步。定义：

$$ \alpha_t := 1 - \beta_t, \quad \bar{\alpha}_t := \prod_{s=1}^{t} \alpha_s $$

则：

$$ x_t = \sqrt{\bar{\alpha}_t} \, x_0 + \sqrt{1 - \bar{\alpha}_t} \, \varepsilon, \quad \varepsilon \sim \mathcal{N}(0, I) $$

**推导：**

$$
\begin{aligned}
x_t &= \sqrt{\alpha_t} x_{t-1} + \sqrt{1 - \alpha_t} \varepsilon_{t-1} \\
    &= \sqrt{\alpha_t}(\sqrt{\alpha_{t-1}} x_{t-2} + \sqrt{1 - \alpha_{t-1}} \varepsilon_{t-2}) + \sqrt{1 - \alpha_t} \varepsilon_{t-1} \\
    &= \sqrt{\alpha_t \alpha_{t-1}} x_{t-2} + \underbrace{\sqrt{\alpha_t(1 - \alpha_{t-1})} \varepsilon_{t-2} + \sqrt{1 - \alpha_t} \varepsilon_{t-1}}_{\text{merge two Gaussians}} \\
    &= \sqrt{\bar{\alpha}_t} x_0 + \sqrt{1 - \bar{\alpha}_t} \, \varepsilon
\end{aligned}
$$

其中合并两个高斯噪声利用了独立高斯分布的可加性：$\mathcal{N}(0, \sigma_1^2 I) + \mathcal{N}(0, \sigma_2^2 I) = \mathcal{N}(0, (\sigma_1^2 + \sigma_2^2) I)$。

**核心性质：** 当 $t \to T$ 时 $\bar{\alpha}_t \to 0$，因此 $x_T \to \mathcal{N}(0, I)$。

### 1.3 后验条件概率 (Posterior Conditional)

在给定 $x_0$ 的条件下，后验 $q(x_{t-1} \mid x_t, x_0)$ 是**高斯分布**，且可以解析计算：

$$ q(x_{t-1} \mid x_t, x_0) = \mathcal{N}(x_{t-1}; \tilde{\mu}_t(x_t, x_0), \tilde{\beta}_t I) $$

其中：

$$ \tilde{\mu}_t(x_t, x_0) = \frac{\sqrt{\bar{\alpha}_{t-1}} \beta_t}{1 - \bar{\alpha}_t} x_0 + \frac{\sqrt{\alpha_t} (1 - \bar{\alpha}_{t-1})}{1 - \bar{\alpha}_t} x_t $$

$$ \tilde{\beta}_t = \frac{1 - \bar{\alpha}_{t-1}}{1 - \bar{\alpha}_t} \beta_t $$

**推导概要：**

$$
\begin{aligned}
q(x_{t-1} \mid x_t, x_0) &= \frac{q(x_t \mid x_{t-1}, x_0) q(x_{t-1} \mid x_0)}{q(x_t \mid x_0)} \\
&\propto \exp\left(-\frac{1}{2}\left[\frac{(x_t - \sqrt{\alpha_t} x_{t-1})^2}{\beta_t} + \frac{(x_{t-1} - \sqrt{\bar{\alpha}_{t-1}} x_0)^2}{1 - \bar{\alpha}_{t-1}} - \frac{(x_t - \sqrt{\bar{\alpha}_t} x_0)^2}{1 - \bar{\alpha}_t}\right]\right)
\end{aligned}
$$

合并 $x_{t-1}$ 的二次项即可得到上述 $\tilde{\mu}_t$ 和 $\tilde{\beta}_t$。这个公式在 DDPM 训练中至关重要。

---

## 2. 反向去噪过程 (Reverse Denosing Process)

### 2.1 定义 (Definition)

反向过程同样是马尔可夫链，从 $x_T \sim \mathcal{N}(0, I)$ 开始，逐步去噪恢复 $x_0$：

$$ p_\theta(x_{0:T}) := p(x_T) \prod_{t=1}^{T} p_\theta(x_{t-1} \mid x_t) $$

其中每一步的转移核由神经网络参数化：

$$ p_\theta(x_{t-1} \mid x_t) := \mathcal{N}(x_{t-1}; \mu_\theta(x_t, t), \Sigma_\theta(x_t, t)) $$

### 2.2 为什么反向过程也是高斯分布？

DDPM 论文的核心洞察：**当 $\beta_t$ 足够小时，前向过程的逆过程也是高斯分布**。

$$ q(x_{t-1} \mid x_t) = \int q(x_{t-1} \mid x_t, x_0) q(x_0 \mid x_t) dx_0 $$

虽然 $q(x_{t-1} \mid x_t)$ 本身不是高斯分布（因为 $q(x_0 \mid x_t)$ 复杂），但 $p_\theta(x_{t-1} \mid x_t)$ 被建模为高斯分布，并训练使其逼近 $q(x_{t-1} \mid x_t, x_0)$。

```ascii
Reverse Denoising: x_T ──→ x_{T-1} ──→ ... ──→ x_0
                   p_θ(x_{T-1}|x_T)         p_θ(x_0|x_1)

x_T (pure noise)   x_{t/2} (partially denoised)    x₀ (generated)
   ░░░░                ░░█░                            ████
   ░░░░     →          ░██░              →             ████
   ░░░░                ░░██                            ████
```

### 2.3 参数化选择

DDPM 做出了两个关键的设计选择：

**1. 固定方差 (Fixed Variance):** $\Sigma_\theta(x_t, t) = \sigma_t^2 I$，其中 $\sigma_t^2 = \beta_t$ 或 $\sigma_t^2 = \tilde{\beta}_t$。实验表明两者效果接近，因此选择更简单的 $\sigma_t^2 = \beta_t$。

**2. 预测噪声 (Predict Noise):** 不直接预测 $\mu_\theta$，而是预测噪声 $\varepsilon_\theta(x_t, t)$：

$$ \mu_\theta(x_t, t) = \frac{1}{\sqrt{\alpha_t}}\left(x_t - \frac{\beta_t}{\sqrt{1 - \bar{\alpha}_t}} \varepsilon_\theta(x_t, t)\right) $$

**采样算法：**

```
Algorithm: DDPM Sampling
──────────────────────────────────────────
1:  x_T ~ N(0, I)
2:  for t = T, T-1, ..., 1 do
3:      z ~ N(0, I)                    (if t > 1, else z = 0)
4:      ε_pred = ε_θ(x_t, t)
5:      x_{t-1} = 1/√α_t · (x_t - β_t/√(1-ᾱ_t) · ε_pred) + σ_t · z
6:  end for
7:  return x_0
```

---

## 3. DDPM 推导 (DDPM Derivation) ⭐

### 3.1 优化目标 (Variational Lower Bound)

DDPM 的训练目标是最大化数据的对数似然，通过 **变分下界 (ELBO)**：

$$ \log p_\theta(x_0) \geq \mathbb{E}_{q(x_{1:T} \mid x_0)}\left[\log \frac{p_\theta(x_{0:T})}{q(x_{1:T} \mid x_0)}\right] =: L $$

展开 ELBO：

$$
\begin{aligned}
L &= \underbrace{D_{\text{KL}}(q(x_T \mid x_0) \parallel p(x_T))}_{L_T \text{ (constant, ignore)}} \\
  &+ \sum_{t=2}^{T} \underbrace{D_{\text{KL}}(q(x_{t-1} \mid x_t, x_0) \parallel p_\theta(x_{t-1} \mid x_t))}_{L_{t-1} \text{ (denoising matching)}} \\
  &+ \underbrace{\mathbb{E}_{q(x_1 \mid x_0)}\left[-\log p_\theta(x_0 \mid x_1)\right]}_{L_0 \text{ (reconstruction)}}
\end{aligned}
$$

### 3.2 简化损失函数 (Simplified Loss)

所有 $L_t$ 项都是**两个高斯分布之间的 KL 散度**。对于 $1 \leq t \leq T-1$：

$$ L_{t-1} = \mathbb{E}_{x_0, \varepsilon}\left[\frac{1}{2\sigma_t^2} \|\tilde{\mu}_t(x_t, x_0) - \mu_\theta(x_t, t)\|^2\right] + C $$

代入 $\tilde{\mu}_t$ 和 $\mu_\theta$ 的表达式：

$$
\begin{aligned}
L_{t-1} &= \mathbb{E}_{x_0, \varepsilon}\left[\frac{1}{2\sigma_t^2} \left\|\frac{1}{\sqrt{\alpha_t}}\left(x_t - \frac{\beta_t}{\sqrt{1 - \bar{\alpha}_t}} \varepsilon\right) - \frac{1}{\sqrt{\alpha_t}}\left(x_t - \frac{\beta_t}{\sqrt{1 - \bar{\alpha}_t}} \varepsilon_\theta(x_t, t)\right)\right\|^2\right] \\
&= \mathbb{E}_{x_0, \varepsilon}\left[\frac{\beta_t^2}{2\sigma_t^2 \alpha_t (1 - \bar{\alpha}_t)} \|\varepsilon - \varepsilon_\theta(x_t, t)\|^2\right]
\end{aligned}
$$

**最终简化损失 (Simplified Loss):** DDPM 发现去掉权重系数后训练更稳定：

$$ L_{\text{simple}}(\theta) := \mathbb{E}_{t, x_0, \varepsilon}\left[\|\varepsilon - \varepsilon_\theta(\sqrt{\bar{\alpha}_t} x_0 + \sqrt{1 - \bar{\alpha}_t} \varepsilon, t)\|^2\right] $$

### 3.3 训练算法 (Training Algorithm)

```
Algorithm: DDPM Training
──────────────────────────────────────────
1:  repeat
2:      x_0 ~ q(x_0)                    // sample data
3:      t ~ Uniform({1, 2, ..., T})      // random timestep
4:      ε ~ N(0, I)                      // random noise
5:      x_t = √ᾱ_t · x_0 + √(1-ᾱ_t) · ε  // forward diffusion
6:      Take gradient step on:
7:          ∇_θ ||ε - ε_θ(x_t, t)||²     // predict noise
8:  until converged
```

**关键洞察：** DDPM 的训练极其简洁——随机采样一个时间步，对数据加噪，然后让网络预测所加的噪声。

### 3.4 网络架构 (Network Architecture)

$\varepsilon_\theta(x_t, t)$ 通常使用 **U-Net** 架构：

```
Input: x_t (e.g., 32×32×3 image at timestep t)
                   │
              [Conv 3×3]
                   │
    ┌────── Down Block 1 ──────┐
    │         │                │
    │    Down Block 2 ──── Skip Connection ────┐
    │         │                               │
    │    Down Block 3 ──── Skip Connection ────┤
    │         │                               │
    │      Bottleneck                         │
    │         │                               │
    │     Up Block 3 ←─── Skip Connection ────┤
    │         │                               │
    │     Up Block 2 ←─── Skip Connection ────┘
    │         │
    └────── Up Block 1 ──────┘
                   │
              [Conv 3×3]
                   │
            Output: ε_pred
```

**时间步编码 (Timestep Embedding):** 使用正弦位置编码 (sinusoidal positional encoding) 将 $t$ 映射到与图像特征相同维度的向量，然后通过 **AdaGN (Adaptive Group Normalization)** 注入：

$$ \text{AdaGN}(h, t) = t_s \cdot \text{GroupNorm}(h) + t_b $$

其中 $t_s, t_b$ 是从时间步编码中学到的缩放和偏移参数。

---

## 4. DDIM: 确定性加速采样 (Deterministic Accelerated Sampling)

### 4.1 动机 (Motivation)

DDPM 的一个主要缺点：**采样速度慢**。生成一张图像需要 1000 次神经网络前向传播。

DDIM (Denoising Diffusion Implicit Models, Song et al., 2021) 提出了**非马尔可夫 (non-Markovian)** 的扩散过程，使得可以使用更少的步骤（10-50 步）生成高质量样本。

### 4.2 核心思想 (Core Idea)

DDIM 的采样过程是**确定性 (Deterministic)** 的：

$$ x_{t-1} = \sqrt{\bar{\alpha}_{t-1}} \underbrace{\left(\frac{x_t - \sqrt{1 - \bar{\alpha}_t} \, \varepsilon_\theta(x_t, t)}{\sqrt{\bar{\alpha}_t}}\right)}_{\text{predicted } x_0} + \sqrt{1 - \bar{\alpha}_{t-1}} \, \varepsilon_\theta(x_t, t) $$

**与 DDPM 的对比：**

| 特性 | DDPM | DDIM |
|:-----|:-----|:-----|
| **采样过程** | 随机（需添加噪声 $\mathbf{z}$） | 确定性（无额外噪声） |
| **马尔可夫性** | 是 | 否 |
| **采样步数** | 1000 步 | 10-50 步 |
| **图像质量** | 高 | 接近 DDPM |
| **一致性** | 无，每次采样不同 | 确定性，给定 $x_T$ 结果确定 |
| **插值能力** | 弱 | 可在潜在空间插值 |

### 4.3 DDIM 的通用形式

DDIM 和 DDPM 可以统一为：

$$ x_{t-1} = \sqrt{\bar{\alpha}_{t-1}} \left(\frac{x_t - \sqrt{1 - \bar{\alpha}_t} \, \varepsilon_\theta^{(t)}}{\sqrt{\bar{\alpha}_t}}\right) + \sqrt{1 - \bar{\alpha}_{t-1} - \sigma_t^2} \, \varepsilon_\theta^{(t)} + \sigma_t \, z_t $$

其中：
- $\sigma_t = 0$: DDIM（确定性采样）
- $\sigma_t = \sqrt{(1 - \bar{\alpha}_{t-1}) / (1 - \bar{\alpha}_t)} \cdot \beta_t$: DDPM（随机采样）
- $0 < \sigma_t < \sigma_{\text{DDPM}}$: 部分随机，折中方案

```ascii
DDPM Sampling (stochastic, 1000 steps):
   x_T → x_{T-1} → ... → x_0
   │ε    │ε+z       │
   random path, each run different

DDIM Sampling (deterministic, 50 steps):
   x_T ──→ x_{T-2} ──→ ... ──→ x_0
   skip steps, same x_T → same x_0
```

### 4.4 加速采样子序列 (Accelerated Subsequence)

DDIM 可以在一个**子序列** $\tau = [\tau_1, \tau_2, \ldots, \tau_S]$ 上进行采样，其中 $S \ll T$：

```
Example: T = 1000, S = 50
Skip strategy: τ_i = ⌊T · (i/S)^p⌋ where p > 1 (more steps at early stage)
Or uniform:    τ_i = i · (T/S)
```

**关键点：** DDIM 使用与 DDPM **完全相同的训练过程**，只是采样不同。因此，一个预训练的 DDPM 模型可以直接用 DDIM 采样。

---

## 5. 潜在扩散模型 (Latent Diffusion Models)

### 5.1 动机 (Motivation)

直接在像素空间运行扩散模型有两大问题：

1. **计算成本高** — 高分辨率图像（$512 \times 512 \times 3$）的扩散过程极其昂贵
2. **冗余** — 像素空间包含大量感知上不重要的细节

**LDM (Latent Diffusion Models, Rombach et al., 2022)** 将扩散过程从像素空间转移到**潜在空间 (Latent Space)**。

### 5.2 架构 (Architecture)

```
┌─────────────────────────────────────────────────────┐
│                   LDM Architecture                    │
│                                                       │
│   ┌──────────┐    ┌──────────────────┐    ┌──────────┐│
│   │          │    │                  │    │          ││
│   │  Image   │───→│  VAE Encoder E   │───→│  Latent  ││
│   │  x ∈ R^HWC│   │                  │    │  z ∈ R^hwc││
│   │          │    │  (downsample)    │    │          ││
│   └──────────┘    └──────────────────┘    └──────────┘│
│                                                │      │
│                                         Diffusion in    │
│                                         Latent Space    │
│                                                │      │
│   ┌──────────┐    ┌──────────────────┐    ┌──────────┐│
│   │          │    │                  │    │          ││
│   │  Image   │←───│  VAE Decoder D   │←───│ Denoised ││
│   │  x̂ ∈ R^HWC│   │  (upsample)     │    │  ẑ       ││
│   │          │    │                  │    │          ││
│   └──────────┘    └──────────────────┘    └──────────┘│
└─────────────────────────────────────────────────────┘
```

**关键优势：**

| 指标 | 像素空间扩散 | 潜在空间扩散 |
|:-----|:-------------|:--------------|
| 空间维度 | $512 \times 512 \times 3 = 786,432$ | $64 \times 64 \times 4 = 16,384$（~48× 压缩）|
| 扩散步数 | 1000 | 1000（但每步计算量小得多）|
| 训练收敛速度 | 慢 | 快 3-5 倍 |
| 高质量生成 | 困难（资源需求高） | 可行（Stable Diffusion 等）|

### 5.3 条件生成 (Conditional Generation)

LDM 通过**交叉注意力 (Cross-Attention)** 注入条件信息（文本、类别、语义图等）：

$$ \text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d}}\right) V $$

$$
\begin{aligned}
Q &= W_Q \cdot \varphi(z_t), \\
K &= W_K \cdot \tau_\theta(c), \\
V &= W_V \cdot \tau_\theta(c)
\end{aligned}
$$

其中 $\varphi(z_t)$ 是 U-Net 的中间特征，$\tau_\theta(c)$ 是条件编码器（如 CLIP text encoder）。

```
Condition Injection via Cross-Attention:
                
   z_t (latent) ──→ φ(z_t) ──→ Q ──┐
                                    ├──→ Attention → Output
   c (text) ──→ τ_θ(c) ──→ K,V ────┘

   "A cute cat sitting on a chair"
         ↓ CLIP Text Encoder
   [0.23, 0.87, ..., 0.12]  ← text embedding
```

### 5.4 Stable Diffusion

**Stable Diffusion** 是基于 LDM 的著名开源图像生成模型：

| 配置 | 数值 |
|:----|:-----|
| 参数量 | ~860M U-Net + ~1.2B 总参数量 |
| 潜在空间 | $64 \times 64 \times 4$（对应 $512 \times 512$ 图像）|
| 条件编码 | CLIP ViT-L/14 text encoder |
| 训练数据 | LAION-5B (5 billion image-text pairs) |
| 训练成本 | ~150,000 GPU hours (A100) |

**SDXL (Stable Diffusion XL)** 进一步改进：

- 更大的 U-Net（~2.6B 参数）
- 双文本编码器（CLIP + OpenCLIP）
- 尺寸条件化（支持不同宽高比）
- Refiner 模型（级联去噪）

### 5.5 其他重要变体 (Other Important Variants)

| 模型 | 特点 | 发表时间 |
|:-----|:-----|:---------|
| **DALL·E 2** | 扩散先验 + 解码器，文本→图像 | 2022 |
| **Imagen** | 级联扩散，文本条件使用 T5-XXL | 2022 |
| **ControlNet** | 在预训练扩散中添加空间控制条件 | 2023 |
| **Sora** | 扩散 Transformer (DiT)，视频生成 | 2024 |
| **Flux** | 整流流 (Rectified Flow)，改进的训练和采样 | 2024 |

---

## 6. 代码实战: 2D 扩散模型 (Code in Action)

详见配套代码文件 [`code/diffusion_demo.py`](code/diffusion_demo.py)，该代码展示了：

1. **前向扩散可视化** — 在 Swiss Roll 2D 数据上一步步添加噪声，展示 $x_0 \to x_T$
2. **训练简单扩散模型** — 一个 MLP 作为 $\varepsilon_\theta(x_t, t)$
3. **反向采样** — 从纯噪声中逐步去噪，生成符合原始数据分布的样本
4. **结果展示** — 打印损失曲线，可视化生成结果

```
Expected output:
═══════════════════════════════════════════════
1. Forward Diffusion Visualization
═══════════════════════════════════════════════

   t=0 (original)    t=100              t=500              t=1000 (noise)
   ╭──────────╮    ╭──────────╮       ╭──────────╮        ╭──────────╮
   │  ╭╮      │    │  ╭╮      │       │  ░░      │        │  ░░░░    │
   │ ╭╯╰╮     │    │ ╭╯░░     │       │ ░░░░     │        │ ░░░░░░   │
   │ ╰╮╭╯     │    │ ╰░░╯     │       │ ░░░░     │        │ ░░░░░░   │
   │  ╰╯      │    │  ░░       │       │ ░░       │        │ ░░░░     │
   ╰──────────╯    ╰──────────╯       ╰──────────╯        ╰──────────╯

   t=0 (original)    t=100             t=500              t=1000

═══════════════════════════════════════════════
2. Training Noise Prediction Network
═══════════════════════════════════════════════

   Epoch 1 | Loss: 0.2345
   Epoch 2 | Loss: 0.1234
   ...
   Epoch 50| Loss: 0.0234

═══════════════════════════════════════════════
3. Reverse Sampling (Generating New Data)
═══════════════════════════════════════════════

   Generated samples match Swiss Roll distribution ✓
```

### 运行方式 (Usage):

```bash
python code/diffusion_demo.py
```

---

## 小结 (Summary)

1. **前向扩散** — 马尔可夫链逐步加噪，$q(x_t \mid x_{t-1}) = \mathcal{N}(\sqrt{1-\beta_t}x_{t-1}, \beta_t I)$，可重参数化为 $x_t = \sqrt{\bar{\alpha}_t}x_0 + \sqrt{1-\bar{\alpha}_t}\varepsilon$。

2. **反向去噪** — 学习预测噪声 $\varepsilon_\theta(x_t, t)$，$p_\theta(x_{t-1} \mid x_t) = \mathcal{N}(\mu_\theta, \sigma_t^2 I)$，通过 $\mu_\theta$ 间接生成数据。

3. **DDPM 核心公式** — $L_{\text{simple}} = \mathbb{E}_{t, x_0, \varepsilon}[\|\varepsilon - \varepsilon_\theta(x_t, t)\|^2]$，极其简洁的训练目标。

4. **DDIM** — 确定性采样，10-50 步生成高质量图像，与 DDPM 共享训练权重。

5. **潜在扩散模型 (LDM)** — 在 VAE 的潜在空间中进行扩散，大幅降低计算成本。Stable Diffusion 是其最成功的应用。

### 对比总结 (Comparison Summary)

| 方法 | 采样步数 | 训练复杂度 | 采样确定性 | 生成质量 |
|:-----|:--------|:-----------|:-----------|:---------|
| **DDPM** | 1000 步 | 低（预测噪声） | 随机 | ★★★★★ |
| **DDIM** | 10-50 步 | 同 DDPM | 确定 | ★★★★☆ |
| **LDM** | 20-50 步 | 中（+ VAE 训练） | 可调 | ★★★★★ |
| **Flow Matching** | 10-50 步 | 中 | 确定 | ★★★★★ |

---

**进一步阅读 (Further Reading):**
- Ho et al. (2020). "Denoising Diffusion Probabilistic Models." — DDPM 原始论文
- Song et al. (2021). "Denoising Diffusion Implicit Models." — DDIM 论文
- Song & Ermon (2019). "Generative Modeling by Estimating Gradients of the Data Distribution." — Score Matching
- Song et al. (2021). "Score-Based Generative Modeling through Stochastic Differential Equations." — SDE 统一框架
- Rombach et al. (2022). "High-Resolution Image Synthesis with Latent Diffusion Models." — LDM / Stable Diffusion 论文
- Peebles & Xie (2023). "Scalable Diffusion Models with Transformers." — DiT (Diffusion Transformer)
- Lipman et al. (2023). "Flow Matching for Generative Modeling." — Flow Matching
