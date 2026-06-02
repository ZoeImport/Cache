# 第5章 LoRA 与模型微调
# Chapter 5: LoRA and Model Fine-Tuning

> **大语言模型（LLM）的"通识教育"使其具备广泛能力，但要让模型在特定任务（如法律问答、医疗诊断、代码生成）上表现出色，**微调 (Fine-Tuning)** 是关键步骤。本章从全量微调的高昂成本出发，引出参数（parameter /pəˈræmɪtər/）高效微调 (PEFT) 方法，深入讲解 LoRA 的数学原理、QLoRA 的量化（quantize /ˈkwɒntaɪz/）技巧，以及 Adapter / Prefix Tuning 等经典方案，并辅以完整代码实现。**
> > **时间线**:
> > - **2021**: Hu et al. 在 *ICLR* 提出 LoRA
> - **2023**: Dettmers et al. 提出 QLoRA
>
> **Large Language Models (LLMs) receive a "general education" that equips them with broad capabilities. However, to excel at specific tasks (e.g., legal QA, medical diagnosis, code generation), **fine-tuning** is essential. This chapter starts from the prohibitive cost of full fine-tuning, introduces Parameter-Efficient Fine-Tuning (PEFT), dives into the mathematics of LoRA, the quantization techniques of QLoRA, and classic approaches like Adapter / Prefix Tuning — all accompanied by a complete code implementation.**

**前置知识 (Prerequisites):** Transformer（/trænsˈfɔːrmər/） 架构 (Chapter 1, 2), PyTorch 基础, 基本的线性代数 (矩阵乘法、秩)
**依赖库 (Dependencies):** `torch>=2.1.0`, `transformers>=4.36.0`, `peft>=0.7.0`, `datasets>=2.14.0`, `bitsandbytes>=0.41.0`
**Code companion:** [`code/lora_finetuning.py`](code/lora_finetuning.py)

---

## 目录 (Table of Contents)

1. [全量微调 vs PEFT](#1-全量微调-vs-peft)
2. [LoRA 数学原理](#2-lora-数学原理)
3. [QLoRA: 4-bit 量化 LoRA](#3-qlora-4-bit-量化-lora)
4. [Adapter / Prefix Tuning](#4-adapter--prefix-tuning)
5. [代码实战: LoRA Fine-Tuning with PEFT](#5-代码实战-lora-fine-tuning-with-peft)
6. [LoRA 变体与前沿进展](#6-lora-变体与前沿进展)

---

## 1. 全量微调 vs PEFT

### 1.1 全量微调 (Full Fine-Tuning)

在**全量微调 (Full Fine-Tuning)** 中，预训练模型的所有参数都被更新以适应下游任务：

$$ \theta^* = \arg\min_{\theta} \mathcal{L}(\theta; \mathcal{D}_{\text{task}}) \quad\text{where}\quad \theta = \{\theta_1, \theta_2, \dots, \theta_{|\theta|}\} $$

**问题 (The Problem):** 现代 LLM 参数量巨大：

| Model | Parameters | Memory (FP16) |
|:------|-----------:|--------------:|
| GPT-2 Small | 124M | ~250 MB |
| LLaMA-7B | 7B | ~14 GB |
| LLaMA-65B | 65B | ~130 GB |
| GPT-3 175B | 175B | ~350 GB |

全量微调需要：
1. **存储完整优化器状态** (Adam 需 2× 额外内存：动量（momentum /məˈmentəm/）和方差)
2. **存储梯度（gradient /ˈɡreɪdiənt/）** (又 1× 参数量)
3. **存储模型参数** (至少 1×)
4. **反向传播（backpropagation /ˌbækprəpəˈɡeɪʃən/）通过全部层** (计算量巨大)

> 对于 175B 模型，全量微调至少需要 **~700 GB** GPU 内存（仅参数+梯度+优化器），实际需要多卡并行。

每个下游任务都需要一份完整模型副本，导致部署成本线性增长。

### 1.2 参数高效微调 (PEFT)

**PEFT (Parameter-Efficient Fine-Tuning)** 的核（kernel /ˈkɜːrnl/）心思想：**冻结预训练模型的大部分参数，只更新少量新增或选中的参数**。

$$ \theta^* = \theta_0 + \Delta\theta \quad\text{where}\quad |\Delta\theta| \ll |\theta_0| $$

| Aspect | Full Fine-Tuning | PEFT |
|:-------|:----------------:|:----:|
| Updated params | 100% | ~0.1% -- 1% |
| Memory (7B model) | ~56 GB | ~1 -- 4 GB |
| Per-task storage | Full model copy | Small adapter (< 100 MB) |
| Training speed | Slow | Fast |
| Quality on high-resource tasks | Excellent | Comparable |
| Quality on low-resource tasks | Overfitting（/ˈoʊvərˈfɪtɪŋ/） risk | More robust |

**PEFT 三大类方法:**

```
PEFT Methods
│
├── Adapter-based     — Insert small bottleneck layers in Transformer blocks
│   ├── Adapter (Houlsby et al., 2019)
│   ├── AdapterFusion (Pfeiffer et al., 2021)
│   └── Compacter (Mahabadi et al., 2021)
│
├── Prefix/Prompt-based — Prepend learnable "virtual tokens"
│   ├── Prefix Tuning (Li & Liang, 2021)
│   └── Prompt Tuning (Lester et al., 2021)
│
└── LoRA-family      — Low-rank decomposition of weight updates
    ├── LoRA (Hu et al., 2021)
    ├── QLoRA (Dettmers et al., 2023)
    ├── AdaLoRA (Zhang et al., 2023)
    └── DoRA (Liu et al., 2024)
```

---

## 2. LoRA 数学原理

### 2.1 核心思想

**LoRA (Low-Rank Adaptation)** 由 Hu et al. (2021) 提出，基于一个重要发现：

> **预训练语言模型在微调时，其权重更新的"内在秩" (intrinsic rank) 是很低的。**

换言之，虽然权重矩阵 $W \in \mathbb{R}^{d \times k}$ 很大，但微调所需的更新 $\Delta W$ 可以用低秩矩阵来近似：

$$ W' = W_0 + \Delta W = W_0 + BA \quad\text{where}\quad B \in \mathbb{R}^{d \times r}, A \in \mathbb{R}^{r \times k} $$

**关键参数:**
- $r$: 秩 (rank)，$r \ll \min(d, k)$（通常 $r = 4, 8, 16, 64$ 等小值）
- $d$: 输入维度（如 hidden size = 768 或 4096）
- $k$: 输出维度（如 FFN intermediate size = 3072 或 11008）

### 2.2 训练过程

```
Training Mode:                       Inference Mode:
┌─────────────────────────┐          ┌─────────────────────────┐
│                         │          │                         │
│   X                     │          │   X                     │
│   │                     │          │   │                     │
│   ├──→ W₀ (frozen) ──→ + ──→ Y   │   ├──→ W₀ ──────────→ + ──→ Y
│   │                     │   ▲      │   │                  ▲   │
│   └──→ B ──→ A ────────┘   │      │   └──→ BA ───────────┘   │
│         ↑     ↑              │      │         ↑                │
│       train  train           │      │    merged into W₀       │
│       only    only           │      │                         │
└─────────────────────────┘          └─────────────────────────┘
```

**前向传播 (Forward pass):**

$$ h = W_0 x + \Delta W x = W_0 x + BA x $$

其中:
- $W_0 \in \mathbb{R}^{d \times k}$ 是冻结的预训练权重
- $B \in \mathbb{R}^{d \times r}$, $A \in \mathbb{R}^{r \times k}$ 是可训练的低秩矩阵
- 初始化: $A \sim \mathcal{N}(0, \sigma^2)$, $B = 0$（保证训练开始时 $\Delta W = 0$）

### 2.3 为何低秩有效 (Why Low-Rank Works)

Hu et al. 通过实验发现：

1. **微调的本质是"重新聚焦"而非"重新学习"**: 预训练模型已学到通用特征，微调只需对特定任务方向做小幅调整。
2. **内在维度 (Intrinsic Dimension)** 很小: Li et al. (2018) 发现，存在一个低维子空间，在该子空间内优化就能达到接近全量微调的性能。
3. **奇异值分解实验**: 对微调前后的权重差 $\Delta W$ 做 SVD，发现其奇异值迅速衰减——大部分信息集中在少数最大的奇异值上。

```
Singular Value Spectrum of ΔW
│
│   ██
│   ████
│   ██████
│   ████████
│   ██████████
│   ████████████████████████████████████... (long tail)
└──────────────────────────────────────
   1   2   3   4   5   ...     min(d,k)
   ↑
   r=4 or 8 captures most of the useful signal
```

### 2.4 应用于 Transformer 的哪些部分？

LoRA 论文建议将低秩更新应用于 **注意力（attention /əˈtenʃən/）机制中的投影矩阵**：

$$ W_q, W_k, W_v, W_o \in \mathbb{R}^{d_{\text{model}} \times d_{\text{model}}} $$

对于每个被应用的矩阵，我们学习两小组参数：

$$ B_q A_q, B_k A_k, B_v A_v, B_o A_o $$

**为什么不作用于 FFN?** 实验表明，FFN 层的权重更新在奇异值分解后信息更分散，低秩近似的效率较低。关注注意力层的 $\Delta W$ 已经足够。

### 2.5 参数量对比

以 GPT-2 Small ($d_{\text{model}}=768$, $d_{\text{ffn}}=3072$, 12 layers, 12 heads) 为例：

| Component | Full FT params | LoRA params ($r=8$) | Reduction |
|:----------|:--------------:|:-------------------:|:---------:|
| Per $W_q$ | $768 \times 768 = 589,824$ | $768 \times 8 + 8 \times 768 = 12,288$ | 48× |
| Per layer (Q,K,V,O) | $4 \times 589,824 = 2,359,296$ | $4 \times 12,288 = 49,152$ | 48× |
| All 12 layers | $12 \times 2,359,296 = 28,311,552$ | $12 \times 49,152 = 589,824$ | 48× |
| **Total model** | **124,439,808** (124M) | **~589,824** (0.6M) | **211×** |

$$ \text{Trainable ratio} = \frac{589,824}{124,439,808} \approx 0.47\% $$

### 2.6 推理时的零额外开销

LoRA 的一个关键优势：训练完成后，可以将 $BA$ 合并到 $W_0$ 中：

$$ W' = W_0 + \alpha \cdot BA $$

其中 $\alpha$ 是缩放超参数（hyperparameter /ˈhaɪpərpəˈræmɪtər/）（通常 $\alpha = 2r$ 或 $\alpha = 16$）。

推理（inference /ˈɪnfərəns/）时使用 $W'$ 替代 $W_0$，**完全不需要额外计算或内存开销**：

```
Before merge:  Y = XW₀ + XBA          (2 matrix multiplications)
After merge:   Y = X(W₀ + BA) = XW'   (1 matrix multiplication)
```

---

## 3. QLoRA: 4-bit 量化 LoRA

### 3.1 动机 (Motivation)

即使使用 LoRA，加载一个 65B 模型仍需要 ~130 GB 内存（FP16）。QLoRA 通过 **4-bit 量化** 将模型内存降低到原来的 1/4：

| Model | FP16 | 4-bit NF4 + LoRA |
|:------|:----:|:-----------------:|
| LLaMA-7B | 14 GB | ~4.5 GB |
| LLaMA-13B | 26 GB | ~8.5 GB |
| LLaMA-65B | 130 GB | ~35 GB (fits on 1×48GB GPU!) |
| GPT-3 175B | 350 GB | ~48 GB (fits on 1×48GB GPU!) |

### 3.2 三大技术贡献

QLoRA (Dettmers et al., 2023) 结合了三种技术：

#### 1) 4-bit NormalFloat (NF4) 量化

**NormalFloat** 是专为正态分布数据设计的 4-bit 数据类型：

$$ \text{NF4}(x) = \text{round}\left(\frac{\text{clip}(x / \sigma, -1, 1) + 1}{2} \times 15\right) $$

其中 $\sigma$ 是权重的标准差，将 16 个量化级别均匀分布在正态分布的分位数上，使得每个级别承载的信息量相等：

```
FP16 weights (float):  -3.2,  2.1, -1.5,  0.8,  0.1, ...
                           ↓ NF4 quantization
NF4 indices (4-bit):     3    14    5    10    8    ...
```

| NF4 Index | Quantile | Represented Value |
|:----------|:---------|:-----------------:|
| 0 | $-\infty$ | -1.0 |
| 1 | $(0, 1/15)$ | -0.848 |
| 2 | $(1/15, 2/15)$ | -0.656 |
| ... | ... | ... |
| 7 | $(7/15, 8/15)$ | 0.0 |
| ... | ... | ... |
| 15 | $(14/15, \infty)$ | 1.0 |

#### 2) 双重量化 (Double Quantization)

对量化常数本身再进行量化。常规量化中，每 64 或 256 个权重共享一个 FP32 的量化常数（scale factor）。双重量化将这些量化常数进一步量化到 8-bit：

$$ \text{DQ}(x) = \text{quantize}(\text{quantize}(x, \text{bits}=4), \text{bits}=8) $$

- 常规量化: 每 64 个权重需 1 个 FP32 常数 → 额外 0.5 bit/weight
- 双重量化: 每 64 个权重需 1 个 FP8 常数，再每 256 个常数共享 1 个 FP32 → 额外 0.127 bit/weight

节约: ~0.373 bit/weight，对于 65B 模型约 **3 GB** 内存。

#### 3) 分页优化器 (Paged Optimizers)

利用 CPU 内存作为 GPU 内存的"交换空间"。当 GPU 内存不足时，优化器状态被分页到 CPU 内存，在需要时自动换入。这使得 **单卡 48GB GPU 微调 65B 模型** 成为可能。

### 3.3 QLoRA 训练流程

```
1. Load pre-trained model
   ├──→ Quantize all weights to NF4 (4-bit)
   └──→ Store quantization constants (double quantized)

2. Add LoRA adapters
   ├──→ Insert low-rank matrices A, B (FP16/FP32)
   └──→ Freeze all NF4 weights

3. Training loop
   ├──→ Dequantize NF4 → FP16 on-the-fly during forward pass
   ├──→ Compute loss (FP16)
   ├──→ Backprop through LoRA adapters only
   └──→ Update A, B with paged AdamW optimizer

4. Inference
   ├──→ Keep base weights in NF4
   └──→ LoRA adapters can be merged or kept separate
```

### 3.4 性能对比

| Method | Memory (65B) | Training Time | Performance (MMLU) |
|:-------|:------------:|:-------------:|:------------------:|
| Full FT | > 780 GB | Baseline | 63.4 |
| LoRA (FP16) | ~260 GB | ~0.8× FT | 63.0 |
| QLoRA (NF4) | ~35 GB | ~1.2× LoRA | 62.8 |

QLoRA 使用不到 5% 的内存，实现了与全量微调相差不到 1% 的性能。

---

## 4. Adapter / Prefix Tuning

### 4.1 Adapter (Houlsby et al., 2019)

**Adapter** 在 Transformer 的每个层中插入小型瓶颈网络：

```
Original Transformer Block:
    X → Self-Attention → Add&Norm → FFN → Add&Norm → Output

With Adapter:
    X → Self-Attention → Add&Norm → Adapter → Add&Norm → FFN → Add&Norm → Adapter → Output
```

**Adapter 结构:**

```python
class Adapter(nn.Module):
    def __init__(self, d_model, bottleneck_dim=64):
        super().__init__()
        self.down = nn.Linear(d_model, bottleneck_dim)  # 降维
        self.up   = nn.Linear(bottleneck_dim, d_model)   # 升维
        self.activation = nn.ReLU()

    def forward(self, x):
        return x + self.up(self.activation(self.down(x)))  # 残差连接
```

**特点:**
- 每个 Adapter 增加参数量: $2 \times d_{\text{model}} \times r$（$r$ 是 bottleneck 维度）
- 通常 $r = 64$，每个 Adapter 约 $2 \times 768 \times 64 \approx 98K$ 参数（GPT-2 Small）
- 串联在 Attention 和 FFN 之后，以残差形式接入

### 4.2 Prefix Tuning (Li & Liang, 2021)

**Prefix Tuning** 不修改模型结构，而是在输入序列前添加一组可学习的"虚拟 token"：

```
Original Input:  [x₁, x₂, ..., xₙ]
                     ↓
Prefix Tuning:  [P₁, P₂, ..., Pₖ, x₁, x₂, ..., xₙ]
                 ↑_____________↑
                   learnable prefix (k tokens)
```

**数学形式:**

对于 Transformer 的每一层，我们学习一组前缀 key 和 value：

$$ Z = [P_K, P_V, X] $$

Attention 计算变为：

$$ \text{head}_i = \text{Attention}(XW_i^Q, [P_K; XW_i^K], [P_V; XW_i^V]) $$

其中 $P_K \in \mathbb{R}^{k \times d_k}$, $P_V \in \mathbb{R}^{k \times d_v}$ 是可学习的参数，$k$ 是 prefix length（通常 10--200）。

**与 Prompt Tuning 的区别:**

| Approach | Where | How many params | Quality |
|:---------|:------|:---------------:|:-------:|
| Prompt Tuning | Only input embedding（/ɪmˈbedɪŋ/） layer | $k \times d_{\text{model}}$ | Lower |
| Prefix Tuning | Every layer's K,V | $2 \times k \times d_{\text{model}} \times \text{n\_layers}$ | Higher |

### 4.3 方法对比总结

| Method | Trainable Params | Extra Inference Cost | When to Use |
|:-------|:----------------:|:--------------------:|:------------|
| Full FT | 100% | None | Unlimited compute, high-resource task |
| Adapter | ~1--3% | Small (extra FF) | Moderate resource, need modularity |
| Prefix Tuning | ~0.1--1% | None (prefix cached) | Low resource, input-conditioned tasks |
| LoRA | ~0.1--1% | None (mergeable) | Default choice — best balance |
| QLoRA | ~0.1--1% | Slight (dequant) | Single GPU, large model (> 7B) |

---

## 5. 代码实战: LoRA Fine-Tuning with PEFT

详见配套代码文件 [`code/lora_finetuning.py`](code/lora_finetuning.py)，关键步骤：

1. **加载基础模型** — 使用 GPT-2 (124M) 作为示例
2. **配置 LoRA** — 通过 PEFT 库的 `LoraConfig` 指定 rank $r=8$，应用到 $W_q, W_v$
3. **对比参数量** — 打印 full FT 和 LoRA 的可训练参数数量
4. **加载数据集** — 使用 `datasets` 加载文本数据
5. **训练** — 标准 Transformer 训练循环
6. **生成对比** — 分别用基础模型和微调后模型生成文本

```
LoRA trainable params: 589,824 / 124,439,808 = 0.47%
Full FT trainable params: 124,439,808 / 124,439,808 = 100.00%
```

---

## 6. LoRA 变体与前沿进展

### 6.1 AdaLoRA (Zhang et al., 2023)

**自适应秩分配**: 不同层、不同权重矩阵的重要性不同，AdaLoRA 通过 SVD 形式的参数化和重要性评分，动态分配参数量：

$$ W = W_0 + P \Lambda Q \quad\text{where}\quad \Lambda = \text{diag}(\sigma_1, \sigma_2, \dots, \sigma_r) $$

重要性低的奇异值被"修剪"（设为 0），从而实现不同层使用不同秩。

### 6.2 DoRA (Weight-Decomposed LoRA, Liu et al., 2024)

将预训练权重分解为**方向 (direction)** 和**幅度 (magnitude)**，仅对方向部分应用 LoRA：

$$ W' = \frac{W_0 + BA}{\|W_0 + BA\|_c} \cdot m $$

其中 $m$ 是学习的幅度向量。这更接近全量微调的学习模式。

### 6.3 Delta-LoRA (Zi et al., 2023)

在训练过程中**同步更新** $A$ 和 $B$ 的梯度（而非冻结其一），但通过参数重参数化保证 $BA$ 的低秩性。

---

## 小结 (Summary)

1. **全量微调成本高**: 175B 模型需 350 GB+ 内存，PEFT 只需 1--5%。

2. **LoRA 的核心公式**: $W' = W_0 + BA$，通过低秩分解将可训练参数减少 100×+。

3. **LoRA 有效的根本原因**: 微调权重的内在秩很低（4-64 即可捕获主要信息）。

4. **QLoRA 使单卡大模型微调成为可能**: 4-bit NF4 量化 + 双重量化 + 分页优化器。

5. **Adapter 插入瓶颈层**: Prefix Tuning 添加虚拟 token，各有优劣。

6. **推理零开销**: LoRA 的 $BA$ 可以合并到 $W_0$ 中，推理时无额外计算。

---

**进一步阅读 (Further Reading):**
- Hu et al. (2021). "LoRA: Low-Rank Adaptation of Large Language Models." — 原始 LoRA 论文
- Dettmers et al. (2023). "QLoRA: Efficient Finetuning of Quantized Language Models." — QLoRA 论文
- Houlsby et al. (2019). "Parameter-Efficient Transfer Learning for NLP." — Adapter 论文
- Li & Liang (2021). "Prefix-Tuning: Optimizing Continuous Prompts for Generation." — Prefix Tuning 论文
- Zhang et al. (2023). "AdaLoRA: Adaptive Budget Allocation for Parameter-Efficient Fine-Tuning." — AdaLoRA
- Liu et al. (2024). "DoRA: Weight-Decomposed Low-Rank Adaptation." — DoRA

## 参考文献 (References)

1. **Hu, E. J. et al.** (2021). LoRA: Low-rank adaptation of large language models. *ICLR*.
2. **Dettmers, T. et al.** (2023). QLoRA: Efficient finetuning of quantized language models. *NeurIPS*.
