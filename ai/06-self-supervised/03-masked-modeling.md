# 第3章：掩码建模 — BERT 与 MAE
# Chapter 3: Masked Modeling — BERT & MAE

> **"填空"是最优雅的自监督学习方式。BERT 通过 Masked Language Model（MLM）在 NLP 领域掀起革命，MAE（Masked Autoencoder（/ˈɔːtoʊənˈkoʊdər/））则将同样的思想推广到计算机视觉。两个方法的核（kernel /ˈkɜːrnl/）心理念高度一致：遮挡输入的一部分，让模型学会预测被遮挡的内容——这个简单的过程迫使模型学习到深层的语义理解。**
> > **时间线**:
> > - **2018**: Devlin et al. 提出 BERT（Masked Language Model）
> - **2022**: He et al. 提出 MAE（Masked Autoencoder）
>
> **"Fill in the blank" is arguably the most elegant form of self-supervised learning. BERT revolutionized NLP with the Masked Language Model (MLM), while MAE (Masked Autoencoder) brought the same idea to computer vision. Both share a core philosophy: occlude part of the input and let the model learn to predict what's missing — a simple process that forces deep semantic understanding.**

**前置知识 (Prerequisites):** Transformer（/trænsˈfɔːrmər/） Encoder（/ɪnˈkoʊdər/） (第5章第2节)、自监督学习基本概念 (第6章第1节)
**Code companion:** [`code/masked_modeling.py`](code/masked_modeling.py)

---

## 1. BERT — 双向 Encoder 的掩码语言模型
## BERT — Bidirectional Encoder's Masked Language Model

BERT（Bidirectional Encoder Representations from Transformers）由 Google 在 2018 年提出（Devlin et al., 2018），是 NLP 领域里程碑式的工作。它的核心创新在于用 **Masked Language Model（MLM）** 实现深度双向预训练。

### 1.1 输入表示
### Input Representation

BERT 的输入由三个嵌入（embedding /ɪmˈbedɪŋ/）相加构成，每个 token 最终表示为：

$$ \text{input}_i = \text{TokenEmbedding}(t_i) + \text{SegmentEmbedding}(s_i) + \text{PositionEmbedding}(p_i) $$

**输入格式：**
```
Input:  [CLS] The man went to [MASK] store [SEP] He bought milk [SEP]
Token:  [CLS]  the  man  went   to  [MASK] store [SEP]  he  bought  milk [SEP]
Seg:      0     0    0    0    0     0      0     0    1     1      1     1
```

- **[CLS]**: 分类（classification /ˌklæsɪfɪˈkeɪʃən/）标记，其最后一层输出用作整个序列的表示（用于 NSP 和下游分类任务）
- **[SEP]**: 分隔标记，分隔两个句子
- **Segment Embedding**: 区分句子 A 和句子 B（0 和 1）
- **Position Embedding**: 可学习的位置编码，最大 512 个位置

### 1.2 Masked Language Model (MLM)
### Masked Language Model

MLM 的核心操作是随机（stochastic /stəˈkæstɪk/）遮挡 15% 的 token，然后让模型预测它们。但 BERT 使用了一种**精心设计的掩码策略**：

对于被选中的 15% token：
- **80%** 替换为 `[MASK]`
- **10%** 替换为随机 token
- **10%** 保持不变

**为什么不用 100% `[MASK]`？** 因为 `[MASK]` 在微调阶段不会出现，导致预训练-微调不一致。加入随机替换和保持不变迫使模型学习到**每个 token 的上下文表示**，而不是单纯记忆 `[MASK]` 模式。

**训练目标：** 交叉熵（entropy /ˈentrəpi/）损失，只计算被 mask 的位置：

$$ \mathcal{L}_{\text{MLM}} = -\sum_{i \in \mathcal{M}} \log P(\hat{y}_i = y_i \mid \text{context}) $$

其中 $\mathcal{M}$ 是被 mask 的位置集合。

### 1.3 Next Sentence Prediction (NSP)
### Next Sentence Prediction

除了 MLM，BERT 还使用 NSP 作为辅助训练任务：

- **正样本：** 连续的两个句子（50%）
- **负样本：** 随机拼接的两个句子（50%）
- **输入：** `[CLS]` 位置的输出经过一个分类头，判断是否为连续句子
- **意义：** 帮助模型理解句子间的关系，对 QA、NLI 等任务至关重要

后续研究（如 RoBERTa）发现去掉 NSP 不影响甚至提升性能，但原始的 BERT 设计中 NSP 是重要的组成部分。

### 1.4 架构细节
### Architecture Details

| 配置 | BERT-Base | BERT-Large |
|:---|:---:|:---:|
| Transformer 层数 | 12 | 24 |
| 隐藏维度 $d_{\text{model}}$ | 768 | 1024 |
| 注意力（attention /əˈtenʃən/）头数 | 12 | 16 |
| 参数（parameter /pəˈræmɪtər/）量 | 110M | 340M |
| 训练数据 | BookCorpus + Wikipedia (3.3B tokens) | 同左 |

BERT 使用 **Transformer Encoder**——每个 block 包含 Multi-Head Self-Attention + Feed-Forward Network，每个子层后接残差连接和 Layer Normalization（/ˌnɔːrmələˈzeɪʃən/）。

---

## 2. 为什么"填空"能学到语义？
## Why "Fill in the Blank" Learns Semantics

### 2.1 上下文聚合的要求
### Context Aggregation Requirement

要准确预测被 mask 的 token，模型必须同时理解左右两侧的上下文：

```
Input: "The [MASK] is shining brightly in the sky."
```

要预测 `[MASK]` 是 "sun"：
- **左侧** "The"、"is" 提示这是一个单数名词
- **右侧** "shining brightly"、"in the sky" 提示这是发光天体
- 模型需要**同时关注两侧**才能准确预测

**这与单向语言模型 (如 GPT) 有本质区别：** 单向模型只能看到左侧上下文，看不到右侧信息。

### 2.2 双向理解的数学含义
### Mathematical Meaning of Bidirectional Understanding

对于掩码位置 $i$，BERT 的条件概率为：

$$ P(x_i \mid \text{context}) = P(x_i \mid x_1, \ldots, x_{i-1}, x_{i+1}, \ldots, x_n) $$

而单向语言模型的条件概率为：

$$ P(x_i \mid \text{context}) = P(x_i \mid x_1, \ldots, x_{i-1}) $$

双向上下文的优势在于，模型在表示每个 token 时聚合了**整个序列**的信息，而不是仅前缀信息。

### 2.3 多层抽象的形成
### Formation of Multi-layer Abstractions

Transformer Encoder 的层数堆叠使得 BERT 可以学到从浅层到深层的抽象：

| 层数 | 学到的内容 | 示例 |
|:---|:---|:---|
| 浅层 (1-4) | 词法和句法特征 | 词性、短语边界 |
| 中层 (5-8) | 语义特征 | 语义角色、指代 |
| 深层 (9-12) | 上下文语义 | 主题、情感、全局关系 |

掩码任务在每一层都提供监督信号——浅层需要理解"什么词性"才能预测，深层需要理解"什么语义"才能预测。这种**多层级监督**使得 BERT 学到丰富的分层表示。

### 2.4 降噪自编码视角
### Denoising Autoencoder Perspective

MLM 本质上是一种**降噪自编码器 (Denoising Autoencoder)**：

1. **加噪：** 用 `[MASK]`、随机 token 或原 token 替换 15% 的输入 token
2. **编码：** Transformer Encoder 处理被破坏的序列
3. **解码：** 预测头（线性层 + softmax（/sɒftˈmæks/））恢复原始 token

这种"破坏-恢复"范式迫使模型学习数据的**内在结构和分布**，而不是简单的记忆。

---

## 3. MAE — Masked Autoencoder for Images
## MAE — Masked Autoencoder for Images

MAE（He et al., 2021）由 FAIR（Facebook AI Research）提出，将掩码建模的思想推广到计算机视觉领域。

### 3.1 核心设计
### Core Design

MAE 的核心设计极其简单且不对称：

1. **掩码：** 随机遮挡图像 75% 的 patches（如将 224×224 图像分割为 16×16 blocks，遮挡其中 75%）
2. **编码：** 只对可见的 25% patches 进行编码（Encoder 是 ViT）
3. **解码：** 用轻量级 Decoder（/diːˈkoʊdər/） 从编码特征和可学习的 mask tokens 中重建完整图像
4. **损失：** 仅计算被 mask 的 patches 的像素级 MSE 损失

**为什么 75% 的掩码比例如此重要？**

- 这远高于 BERT 的 15% 掩码率
- 图像有高度的空间冗余——相邻像素高度相关
- 75% 的掩码几乎消除了所有"简单"线索（如颜色扩散（diffusion /dɪˈfjuːʒən/）、纹理延拓），迫使模型理解**高阶语义**
- 如果一个模型能仅从 25% 的 patches 重建整张图像，它必然学会了物体的形状、结构和上下文关系

### 3.2 架构细节
### Architecture Details

```
                                                       Pixel 1
                                                        ...
+------------+    Visible     +-----------+    +--->  Pixel N
| Input      |    Patches     |  ViT      |    |
| Image      |  ----------->  |  Encoder  |  ----   Decoder
| (224×224)  |    (25%)      |           |    |   (Transformer)
+------------+               +-----------+    +--->  [MASK] Token 1
      |                                               ...
  Patch Embed                                        [MASK] Token N
  (16×16)                                             (75%)
```

**关键洞察：不对称设计**

| 组件 | 参数 | 作用 |
|:---|:---:|:---|
| Encoder | ViT-Large (304M) | 对可见 patches 做高维语义编码 |
| Decoder | 轻量 Transformer (~1%) | 从语义特征重建像素 |
| Mask ratio | 75% | 消除空间冗余，强制学习语义 |

**为什么 Decoder 可以很轻？** 因为重建像素是"低层次"任务，只需要从高层语义特征映射回像素空间。而 Encoder 需要学习"高的语义理解"才是困难的部分。

### 3.3 效率优势
### Efficiency Advantage

MAE 的计算效率远高于标准 ViT 训练：

- Encoder 只处理 25% 的 patches → $\sim$4$\times$ 加速
- 不需要对比学习中的负样本对
- 不需要复杂的数据增强（MAE 使用最简单的随机裁剪 + 水平翻转）

这使得 MAE 可以用 $8\times$ 更少的训练时间达到或超越对比学习方法（如 MoCo v3、CLIP）。

### 3.4 损失函数
### Loss Function

MAE 对每个 mask 的 patch 计算像素空间的 MSE 损失：

$$ \mathcal{L}_{\text{MAE}} = \frac{1}{|\mathcal{M}|} \sum_{i \in \mathcal{M}} \frac{1}{p^2} \| \hat{\mathbf{x}}_i - \mathbf{x}_i \|_2^2 $$

其中 ${p}$ 是 patch 大小（如 16×16 图像块），$\mathcal{M}$ 是 mask 的 patch 集合，$\hat{\mathbf{x}}_i$ 和 $\mathbf{x}_i$ 分别是重建和原始像素。

---

## 4. MLM vs Autoregressive — 双向 vs 单向
## MLM vs Autoregressive — Bidirectional vs Unidirectional

### 4.1 核心对比
### Core Comparison

| 特性 | BERT (MLM) | GPT (Autoregressive) |
|:---|:---|:---|
| **方向** | 双向 (Bidirectional) | 单向 (Unidirectional, Left-to-Right) |
| **训练目标** | 预测被 mask 的 token | 预测下一个 token |
| **生成能力** | 弱（需特殊处理） | 强（原生生成） |
| **表征能力** | 强（考虑全部上下文） | 较弱（仅左侧上下文） |
| **下游任务** | 分类、标注、QA 为主 | 生成、对话、代码为主 |
| **损失计算** | 仅 mask 位置 | 所有位置 |
| **per-step 计算** | 编码器模式（并行） | 解码器模式（顺序） |

### 4.2 数学对比
### Mathematical Comparison

**BERT (MLM) — 联合概率建模：**

BERT 建模的是**条件分布**——给定被破坏的序列 $\tilde{X}$，预测被 mask 的位置：

$$ P(\tilde{X}_m \mid \tilde{X}_{-m}; \theta) = \prod_{i \in m} P(x_i \mid \tilde{X}_{-m}; \theta) $$

被 mask 的位置在输出层**相互独立**（给定输入）。

**GPT (Autoregressive) — 链式概率分解：**

GPT 建模的是**序列的联合概率**通过链式法则：

$$ P(X; \theta) = \prod_{t=1}^n P(x_t \mid x_{<t}; \theta) $$

每个位置的条件概率依赖于其左侧的所有 token。

### 4.3 各自的优势与劣势
### Strengths and Weaknesses

**BERT 的优势：**

- 每个 token 的表示包含完整的上下文信息 → 更好的**理解能力**
- 编码端可并行计算 → 训练效率高
- 在分类、推理（inference /ˈɪnfərəns/）、阅读理解等理解型任务上历来领先

**BERT 的劣势：**

- 不能自然生成文本（需用 masked LM 逐步生成，效率低）
- 训练中的 `[MASK]` 与微调/推理时不匹配（discrepancy）
- 每个 token 的预测相互独立（忽略输出依赖）

**GPT 的优势：**

- 原生支持生成任务
- 训练和推理目标一致（都是预测下一个 token）
- 可以扩展到超大规模（得益于因果掩码的高效实现）

**GPT 的劣势：**

- 每个 token 只能看到左侧信息 → 理解任务上性能偏低
- 推理时需顺序生成 → 延迟较高
- 长距离依赖时可能丢失信息

### 4.4 融合趋势
### Convergence Trends

现代 NLP 模型开始融合两者的优势：

- **T5 (Text-to-Text Transfer Transformer):** 将一切任务都转化为 text-to-text 格式，使用 Encoder-Decoder 架构，Encoder 双向、Decoder 自回归（regression /rɪˈɡreʃən/）
- **XLNet:** 使用排列语言模型（Permutation Language Model），在自回归框架下实现双向上下文
- **BART:** 类似 T5，使用双向 Encoder + 自回归 Decoder
- **UniLM:** 共享 Transformer，通过不同的 attention mask 实现单向/双向
- **Electra:** 引入判别式预训练（替换 token 检测），更高效

---

## 5. 总结与展望
## Summary and Outlook

### 5.1 掩码建模的统一视角
### Unified View of Masked Modeling

BERT（文本）和 MAE（图像）的方法论高度一致：

| 步骤 | BERT | MAE |
|:---|:---|:---|
| 输入单元 | Token | Image Patch |
| 掩码比例 | 15% | 75% |
| 掩码方式 | `[MASK]`/随机/不变 | 随机遮挡 patches |
| 编码器 | Transformer Encoder | ViT Encoder |
| 解码器 | MLP 分类头 | 轻量 Transformer |
| 损失 | Cross-Entropy | MSE |
| 重建目标 | Token ID | Pixel Values |

### 5.2 关键洞察
### Key Insights

1. **掩码是通用的自监督信号**：不管输入模态是什么，"遮挡-预测"都是一个有效的预训练任务
2. **高掩码率强制语义学习**：MAE 75% 的高掩码率证明，消除低级线索才能迫使模型理解高级语义
3. **不对称编码器-解码器设计**：编码器专注于语义理解（大而深），解码器专注于任务重建（小而轻）
4. **双向 > 单向（理解任务）**：对需要深度理解的任务，双向上下文是更优的选择
5. **生成任务需要单向**：对需要生成的任务，自回归仍然是不可替代的范式

### 5.3 后续发展
### Subsequent Developments

- **掩码语言模型的方向演进：** BERT → RoBERTa（更大、去掉 NSP）→ ALBERT（参数共享）→ DeBERTa（解耦注意力）
- **图像方向的演进：** MAE → ConvMAE（混合 CNN-ViT）→ MaskFeat（不使用 mask tokens）
- **多模态掩码建模：** MaskCLIP、BEiT-3、MaskVLM 等将掩码思想推广到多模态场景

---

> **进一步阅读 (Further Reading):**
> - [BERT: Pre-training of Deep Bidirectional Transformers](https://arxiv.org/abs/1810.04805) (Devlin et al., 2018)
> - [MAE: Masked Autoencoders Are Scalable Vision Learners](https://arxiv.org/abs/2111.06377) (He et al., 2021)
> - [RoBERTa: A Robustly Optimized BERT Pretraining Approach](https://arxiv.org/abs/1907.11692) (Liu et al., 2019)
> - [T5: Exploring the Limits of Transfer Learning](https://arxiv.org/abs/1910.10683) (Raffel et al., 2020)
