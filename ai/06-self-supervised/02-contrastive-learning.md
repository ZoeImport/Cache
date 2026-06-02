# 第2章 对比学习 — 无需标签的表征学习
# Chapter 2: Contrastive Learning — Representation Learning Without Labels

> **对比学习 (Contrastive Learning) 是自监督学习的核（kernel /ˈkɜːrnl/）心范式之一。** 它的核心思想极其简洁：在表征空间中拉近相似样本（正样本对），推远不相似样本（负样本对）。本章从这一直觉出发，依次讲解 SimCLR、InfoNCE 损失函数（及其与互信息的深层联系）、MoCo 动量（momentum /məˈmentəm/）编码器（encoder /ɪnˈkoʊdər/），以及里程碑式的 CLIP 模型。
> > **时间线**:
> > - **2020**: Chen et al. 提出 SimCLR; He et al. 提出 MoCo
> - **2021**: Radford et al. 提出 CLIP
>
> **Contrastive Learning is one of the central paradigms of self-supervised learning.** Its core idea is remarkably simple: pull similar samples (positive pairs) together in the embedding（/ɪmˈbedɪŋ/） space while pushing dissimilar samples (negative pairs) apart. This chapter starts from this intuition and progressively covers SimCLR, the InfoNCE loss (with its deep connection to mutual information), the MoCo momentum encoder, and the landmark CLIP model.

**前置知识 (Prerequisites):** 深度学习基础（前向/反向传播）、卷积（convolution /ˌkɒnvəˈluːʃən/）神经网络、信息论基础（详见第 2 卷 第 4 章）

**依赖库 (Dependencies):** `torch>=2.1.0`, `torchvision`, `numpy`, `matplotlib`, `scikit-learn`

**Code companion:** [`code/contrastive_learning.py`](code/contrastive_learning.py)

---

## 目录 (Table of Contents)

1. [核心思想 (Core Idea)](#1-核心思想-core-idea)
   - 1.1 [正样本对与负样本对](#11-正样本对与负样本对-positive--negative-pairs)
   - 1.2 [对比损失的一般形式](#12-对比损失的一般形式-general-form-of-contrastive-loss)
2. [SimCLR](#2-simclr)
   - 2.1 [架构总览](#21-架构总览-architecture-overview)
   - 2.2 [数据增强的关键作用](#22-数据增强的关键作用-crucial-role-of-data-augmentation)
   - 2.3 [投影头为什么重要](#23-投影头为什么重要-why-the-projection-head-matters)
3. [InfoNCE 损失函数](#3-infonce-损失函数-infonce-loss)
   - 3.1 [定义与公式](#31-定义与公式-definition)
   - 3.2 [从互信息的角度理解](#32-从互信息的角度理解-derivation-from-mutual-information)
   - 3.3 [温度参数（parameter /pəˈræmɪtər/） τ 的作用](#33-温度参数-τ-的作用-role-of-temperature)
4. [MoCo：动量对比学习](#4-moco动量对比学习-momentum-contrast)
   - 4.1 [MoCo 的核心挑战](#41-moco-的核心挑战-the-core-challenge)
   - 4.2 [动量编码器与队列](#42-动量编码器与队列-momentum-encoder--queue)
5. [CLIP：图文对比学习的里程碑](#5-clip图文对比学习的里程碑-clip)
   - 5.1 [架构与训练](#51-架构与训练-architecture--training)
   - 5.2 [零样本迁移能力](#52-零样本迁移能力-zero-shot-transfer)
6. [关键总结 (Key Summary)](#6-关键总结-key-summary)

---

## 1. 核心思想 (Core Idea)

### 1.1 正样本对与负样本对 (Positive & Negative Pairs)

对比学习的直觉来自一个非常朴素的问题：**如何在没有标签的情况下学到好的表征？**

答案隐藏在数据本身的结构中。如果我们对同一张图片做不同的数据增强（旋转、裁剪、色彩变换等），得到的两个"视图" (view) 应该共享相同的语义信息。换句话说，它们在表征空间中应该彼此靠近。相反，不同图片的增强视图应该相互远离。

```
                    ┌─── 正样本对 (Positive Pair) ───┐
                    │                                  │
    原始图片 ──→ [增强 A] ──→ 编码器 ──→ 表征 z_i
                    │                        ↑ 拉近
    原始图片 ──→ [增强 B] ──→ 编码器 ──→ 表征 z_j
                    │                        ↓ 推远
    其他图片 ──→ [增强 ...] ──→ 编码器 ──→ 表征 z_k  (负样本 / Negative)
```

形式上，对于一个小批量 (mini-batch) 中的 $N$ 个样本，我们通过数据增强产生 $2N$ 个视图。每个视图 $x_i$ 都有一个正样本对 $x_j$（同一张原始图片的另一个增强视图），以及 $2N-2$ 个负样本对（批次中所有其他视图）。

### 1.2 对比损失的一般形式 (General Form of Contrastive Loss)

对比损失函数的一般形式可以写为：

$$
\mathcal{L}_{\text{contrast}} = \mathbb{E}_{x, x^+, x^-} \left[ -\log \frac{s(x, x^+)}{s(x, x^+) + \sum s(x, x^-)} \right]
$$

其中 $s(\cdot, \cdot)$ 是某种相似度度量（通常是余弦相似度），$x^+$ 是正样本，$x^-$ 是负样本。这个公式的直觉是：**让正样本对的相对相似度最大化**。

---

## 2. SimCLR

SimCLR (Chen et al., 2020) 是对比学习中最具影响力的框架之一。它的优雅之处在于**简洁**——没有特殊架构、没有记忆库、没有动量编码器，纯粹依靠数据增强和对比损失。

### 2.1 架构总览 (Architecture Overview)

SimCLR 的架构可以分解为三个组件：

```
        x ──→ [Aug] ──→ x̃_i ──→ [Encoder f(·)] ──→ h_i ──→ [Proj g(·)] ──→ z_i
  (原始图片)    (增强)        (ResNet)    (表征)     (MLP)    (对比空间)
```

1. **数据增强 (Augmentation)**：对每个输入 $x$ 随机（stochastic /stəˈkæstɪk/）应用两种增强变换，得到正样本对 $(\tilde{x}_i, \tilde{x}_j)$
2. **编码器 (Encoder) $f(\cdot)$**：通常是 ResNet，将增强后的图像映射到表征空间 $h \in \mathbb{R}^{d}$
3. **投影头 (Projection Head) $g(\cdot)$**：一个小型 MLP，将 $h$ 映射到对比损失空间 $z \in \mathbb{R}^{d_p}$，仅在训练时使用

**关键设计决策：** 对比损失应用在投影头 $g(\cdot)$ 的输出 $z$ 上，而非编码器 $f(\cdot)$ 的输出 $h$ 上。实验表明这显著提升了下游任务的迁移效果。

### 2.2 数据增强的关键作用 (Crucial Role of Data Augmentation)

SimCLR 论文最重要的发现之一是：**数据增强的选择对对比学习效果有决定性的影响**。

实验表明，以下增强组合效果最佳：

| 增强策略 | 作用 | 重要性 |
|:--------:|:----:|:------:|
| **随机裁剪 + 缩放** (Random Crop + Resize) | 改变物体在图像中的位置和比例 | ⭐⭐⭐ |
| **色彩扭曲** (Color Distortion) | 改变色调、饱和度、亮度 | ⭐⭐⭐ |
| **高斯模糊** (Gaussian Blur) | 去除高频纹理信息 | ⭐⭐ |
| **水平翻转** (Horizontal Flip) | 增加视角变化 | ⭐ |

> **为什么色彩扭曲如此重要？** 如果不加入色彩扭曲，编码器可能"作弊"：仅凭图像的色彩直方图就能区分正负样本，而无需学习有意义的语义特征。色彩扭曲迫使编码器关注物体的**形状和内容**而非低级的颜色统计信息。

对于 CIFAR-10，典型的增强流程如下：

```python
from torchvision import transforms

simclr_augmentation = transforms.Compose([
    transforms.RandomResizedCrop(32, scale=(0.2, 1.0)),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.ColorJitter(0.4, 0.4, 0.4, 0.1, p=0.8),
    transforms.GaussianBlur(kernel_size=3, sigma=(0.1, 2.0)),
    transforms.ToTensor(),
    transforms.Normalize([0.4914, 0.4822, 0.4465],
                         [0.2470, 0.2435, 0.2616]),
])
```

### 2.3 投影头为什么重要 (Why the Projection Head Matters)

对比学习中的一个重要发现：在编码器 $f(\cdot)$ 之上添加一个投影头 $g(\cdot)$，训练后在投影头的输出 $z$ 上施加对比损失，但**下游任务使用编码器的输出 $h$**。

为什么这么做有效？

$$
\underbrace{h}_{\text{表征}} \xrightarrow{\text{MLP}} \underbrace{z}_{\text{对比空间}} \xrightarrow{\text{InfoNCE}}
$$

直观解释：投影头 $g(\cdot)$ 的作用是**去除表征中与数据增强相关的信息**。在对比过程中，编码器 $f(\cdot)$ 知道"裁剪和色彩变化的是同一物体"，从而学会对这些变换不变的语义特征。投影头在这个过程中充当"缓冲区"，吸收掉增强变换的具体细节，让 $h$ 更加通用和鲁棒。

实验数据：移除投影头（即直接对 $h$ 施加对比损失）会导致 ImageNet 线性评估准确率下降约 **10%** 以上。

---

## 3. InfoNCE 损失函数 (InfoNCE Loss)

InfoNCE (Information Noise-Contrastive Estimation) 是对比学习中最常用的损失函数。

### 3.1 定义与公式 (Definition)

给定正样本对 $(z_i, z_j)$ 和一组负样本 $\{z_k\}_{k=1}^{K}$，InfoNCE 损失定义为：

$$
\boxed{\mathcal{L}_{\text{InfoNCE}} = -\log \frac{\exp(\text{sim}(z_i, z_j) / \tau)}
{\exp(\text{sim}(z_i, z_j) / \tau) + \sum_{k=1}^{K} \exp(\text{sim}(z_i, z_k) / \tau)}}
$$

其中：
- $\text{sim}(u, v) = u^\top v / \|u\| \|v\|$（余弦相似度）
- $\tau$ 是**温度参数 (temperature parameter)**
- $K$ 是负样本的数量

在 SimCLR 的标准实现中，对于批次大小为 $N$ 的数据，每个样本有 $1$ 个正样本和 $2N-2$ 个负样本，因此：

$$
\mathcal{L} = \frac{1}{2N} \sum_{i=1}^{2N} \left[ -\log \frac{\exp(\text{sim}(z_i, z_{p(i)}) / \tau)}
{\sum_{k=1}^{2N} \mathbb{1}_{k \neq i} \exp(\text{sim}(z_i, z_k) / \tau)} \right]
$$

其中 $p(i)$ 是 $i$ 的正样本索引。

### 3.2 从互信息的角度理解 (Derivation from Mutual Information)

InfoNCE 的深刻之处在于它与 **互信息 (Mutual Information)** 的直接联系。回顾第 2 卷第 4 章的内容：

**互信息 (MI)** 衡量两个随机变量之间的依赖程度：

$$
I(X; Y) = \mathbb{E}_{p(x,y)} \left[ \log \frac{p(x,y)}{p(x)p(y)} \right] = D_{KL}(p(x,y) \parallel p(x)p(y))
$$

InfoNCE 损失实际上是**互信息的下界估计器**。具体来说，考虑一个正样本对 $(x, y)$（如图像及其增强视图），我们想要估计 $I(x; y)$：

$$
I(x; y) \ge \log(K) - \mathcal{L}_{\text{InfoNCE}}
$$

其中 $K$ 是负样本数量。

**推导思路**（简化版）：

假设有一个判别器 $f(x, y) = \exp(\text{sim}(z_x, z_y) / \tau)$，其任务是区分正样本对和负样本对。正样本对的联合分布为 $p(x,y)$，负样本对的边缘分布为 $p(x)p(y)$。从 $K+1$ 个候选（1 个正样本 + $K$ 个负样本）中选出正样本的概率为：

$$
p(\text{positive} = y | x, \{y_k\}_1^K) = \frac{f(x, y)}{\sum_{k=1}^K f(x, y_k)}
$$

将这个概率代入交叉熵（entropy /ˈentrəpi/）损失并对期望进行推导，可以得到：

$$
\mathcal{L}_{\text{InfoNCE}} \approx -\mathbb{E} \left[ \log \frac{p(y|x)}{p(y)} \right] = -I(x; y) + \text{const}
$$

> **重要结论：** 最小化 InfoNCE 损失等价于**最大化正样本对之间的互信息下界**。这个联系将对比学习从"启发式技巧"提升为有信息论基础的理论框架。
>
> $$
> \boxed{\mathcal{L}_{\text{InfoNCE}} \downarrow \quad \Longleftrightarrow \quad I(x; y) \uparrow}
> $$

负样本数量 $K$ 越大，这个下界越紧（越接近真实的互信息值）。这正是 SimCLR 和 MoCo 都使用大批次或大队列的原因。

### 3.3 温度参数 τ 的作用 (Role of Temperature)

温度参数 $\tau$ 控制着对比损失对**困难样本 (hard negatives)** 的关注程度：

- **$\tau$ 很小**（如 0.1）：相似度分布变得"尖锐"，模型被迫关注与正样本最相似的负样本（即困难负样本），从而产生更强的判别力
- **$\tau$ 很大**（如 1.0）：相似度分布变得"平滑"，所有负样本被平等对待，模型失去对细节的区分能力

```
  相似度分布随 τ 的变化:
  
  τ=0.1:  ████▁▁▁▁▁▁           (尖锐, 聚焦困难负样本)
  τ=0.5:  ██████▃▁▁▁           (中等)
  τ=1.0:  █████████▅▃▁         (平滑, 平等对待所有负样本)
```

经验上，$\tau = 0.1$ 或 $0.07$ 是 SimCLR 的最佳取值。

---

## 4. MoCo：动量对比学习 (Momentum Contrast)

MoCo (He et al., 2020) 解决了对比学习中的一个核心工程挑战：**如何提供大量且一致的负样本**。

### 4.1 MoCo 的核心挑战 (The Core Challenge)

在 SimCLR 中，负样本来自当前小批量内的其他样本，因此负样本数量受限于批次大小。增加负样本数量意味着：

1. **大规模 GPU 内存开销**：SimCLR 使用 8192 的批次大小需要大量 TPU/GPU
2. **编码器不一致**：不同批次中的样本由不同参数版本的编码器处理，负样本表征不一致

MoCo 提出了两个创新来解决这些问题。

### 4.2 动量编码器与队列 (Momentum Encoder & Queue)

MoCo 的架构包括三个关键组件：

```
                    ┌─── 队列 (Queue): 存储过去批次的表征 ───┐
                    │   [z_{t-100}, z_{t-99}, ..., z_{t-1}]   │
                    └─────────────────────────────────────────┘
                              ↑ 入队 / 出队
  x_q ──→ [Enc_q (f_q)] ──→ z_q     (query, 梯度更新)
  x_k ──→ [Enc_k (f_k)] ──→ z_k     (key,  动量更新, 无梯度)
```

**1. 动量编码器 (Momentum Encoder)：**

key 编码器 $f_k$ 不是直接通过梯度（gradient /ˈɡreɪdiənt/）更新，而是作为 query 编码器 $f_q$ 的**滑动平均**：

$$
\theta_k \leftarrow m \cdot \theta_k + (1 - m) \cdot \theta_q
$$

其中 $m$ 是动量系数（通常 $m = 0.999$）。这意味着 key 编码器变化极其缓慢，从而：
- 队列中的负样本表征由**几乎一致的编码器**产生
- 保证对比学习的训练稳定性

**2. 负样本队列 (Queue)：**

MoCo 维护一个 FIFO 队列来存储过去批次的 key 表征：
- **入队：** 当前批次的 key 表征加入队列
- **出队：** 最旧的批次被移出队列
- **队列大小**可远大于批次大小（如 65536），解耦了负样本数量与批次大小

> **SimCLR vs MoCo 的关键区别：**
>
> | 特性 | SimCLR | MoCo |
> |:----:|:------:|:----:|
> | 负样本来源 | 当前批次 | 队列（历史批次） |
> | 负样本容量 | 受限于批次大小 (2N-2) | 可设任意大（如 65536） |
> | 编码器一致性 | 低（参数每步变化） | 高（动量更新） |
> | GPU 内存需求 | 高（大批次） | 较低 |
>
> 简单记忆：**SimCLR 用大 batch 换多样负样本，MoCo 用队列换大负样本池。**

---

## 5. CLIP：图文对比学习的里程碑 (CLIP)

CLIP (Contrastive Language-Image Pre-training, Radford et al., 2021) 将对比学习从纯视觉推广到了**多模态领域**，是近年来最具影响力的 AI 模型之一。

### 5.1 架构与训练 (Architecture & Training)

CLIP 的核心架构：

```
  [Image] ──→ [Image Encoder] ──→ I_i     ┌───────────────────┐
                                           │  N×N 相似度矩阵   │
  [Text]  ──→ [Text Encoder]  ──→ T_j     │  sim(I_i, T_j)   │
                                           └───────────────────┘
                                               ↓
                                         [对比损失 (InfoNCE)]
```

具体训练过程：

1. 从网络上收集 4 亿个 (图片, 文本) 对
2. 图像编码器（ResNet 或 ViT）将图片编码为 $I \in \mathbb{R}^{d}$
3. 文本编码器（Transformer（/trænsˈfɔːrmər/））将文本编码为 $T \in \mathbb{R}^{d}$
4. 对于一个批次中的 $N$ 对数据，计算 $N \times N$ 的相似度矩阵
5. **对角线元素**是正样本对（匹配的图文对），**非对角线元素**是负样本对
6. 分别对图像和文本两个方向计算 InfoNCE 损失，然后取平均

$$
\mathcal{L} = \frac{1}{2} \left[ \underbrace{-\frac{1}{N}\sum_{i} \log \frac{\exp(I_i \cdot T_i / \tau)}{\sum_j \exp(I_i \cdot T_j / \tau)}}_{\text{image→text}} + \underbrace{-\frac{1}{N}\sum_{j} \log \frac{\exp(T_j \cdot I_j / \tau)}{\sum_i \exp(T_j \cdot I_i / \tau)}}_{\text{text→image}} \right]
$$

### 5.2 零样本迁移能力 (Zero-Shot Transfer)

CLIP 最令人惊叹的特性是其**零样本 (zero-shot) 迁移能力**：训练完成后，无需任何微调，CLIP 可以直接用于各种视觉任务。

**零样本图像分类（classification /ˌklæsɪfɪˈkeɪʃən/）**的工作原理：

1. 准备所有类别名称的文本描述，如 `"a photo of a dog"`, `"a photo of a cat"`
2. 用文本编码器将所有类别文本编码为文本特征
3. 用图像编码器将要分类的图片编码为图像特征
4. 选取与图像特征最相似的文本类别作为预测结果

```
  "a photo of a dog" ──→ [Text Enc] ──→ T_dog ──┐
  "a photo of a cat" ──→ [Text Enc] ──→ T_cat ──┤
  "a photo of a car" ──→ [Text Enc] ──→ T_car ──┤──→ [argmax] → "dog"
  ...                                             │
  输入图片 ──→ [Image Enc] ──→ I ────────────────┘
```

**在 ImageNet 上的零样本 Top-1 准确率达到了 76.2%**（无需任何 ImageNet 训练数据！），在 36 个零样本分类任务中，有 27 个超过了之前的有监督基线。

> **CLIP 的深远影响：**
> - 证明了对齐图像和文本的表征空间是一种强大的学习范式
> - 为后续的视觉语言模型（如 BLIP, LLaVA, GPT-4V）奠定了基础
> - 零样本能力使 AI 系统可以"开箱即用"地处理新任务

---

## 6. 关键总结 (Key Summary)

### 核心公式

| 概念 | 公式 | 含义 |
|:----:|:----:|:----:|
| **InfoNCE 损失** | $\mathcal{L} = -\log \frac{\exp(\text{sim}(z_i,z_j)/\tau)}{\sum_k \exp(\text{sim}(z_i,z_k)/\tau)}$ | 最大化正样本对的相对相似度 |
| **互信息下界** | $I(x;y) \ge \log(K) - \mathcal{L}_{\text{InfoNCE}}$ | 最小化 InfoNCE = 最大化互信息 |
| **MoCo 动量更新** | $\theta_k \leftarrow m \cdot \theta_k + (1-m) \cdot \theta_q$ | 保持负样本编码器的一致性 |
| **CLIP 双向损失** | $\mathcal{L} = \frac{1}{2}(\mathcal{L}_{i \to t} + \mathcal{L}_{t \to i})$ | 对齐图像与文本表征空间 |

### 关键洞察

1. **对比学习的本质是互信息最大化** — InfoNCE 损失就是互信息下界的估计器。正样本对的互信息越大，表征质量越高
2. **数据增强是对比学习的"标签"** — 增强设计决定了模型学习什么类型的语义特征。色彩扭曲防止了"作弊"捷径
3. **投影头剥离增强信息** — 对比训练时使用，下游任务时弃用。它使编码器关注语义而非变换细节
4. **负样本的数量和质量至关重要** — 更多的负样本 → 更紧的互信息下界 → 更好的表征。MoCo 的队列解决了这个问题
5. **对比学习可以跨越模态** — CLIP 证明了这个框架可以扩展到图像-文本的多模态场景

### 三模型对比

| 特性 | SimCLR | MoCo | CLIP |
|:----:|:------:|:----:|:----:|
| 发表年份 | 2020 | 2020 | 2021 |
| 负样本来源 | 当前批次 | 队列 | 当前批次（跨模态） |
| 是否需要特殊架构 | 否 | 动量编码器 | 双塔编码器 |
| 适用范围 | 视觉 | 视觉 | 视觉+语言 |
| 核心贡献 | 简化对比学习框架 | 解耦负样本数量与批次大小 | 多模态对比学习 |

### 动手练习

1. **推导练习：** 写出 CLIP 中 image→text 方向的 InfoNCE 损失的详细梯度推导
2. **代码练习：** 在 `contrastive_learning.py` 中修改温度参数 $\tau$（0.01, 0.1, 0.5, 1.0），观察对收敛速度和表征质量的影响
3. **实验练习：** 实现一个简单的 MoCo 变体，将队列引入 CIFAR-10 的对比学习
4. **延伸思考：** 为什么 BYOL/SimSiam 不需要负样本也能工作？对比学习与非对比式 SSL 的边界在哪里？（提示：它们在隐式地做对比）

---

> **下章预告：** 第 3 章将介绍**非对比式自监督学习 (Non-Contrastive SSL)** — BYOL、SimSiam 和 Barlow Twins 等不需要负样本的表征学习方法。

---

*Last updated: 2026-06-02*
