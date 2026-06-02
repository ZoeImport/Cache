# 第4章 大语言模型 — 预训练、对齐与推理
# Chapter 4: Large Language Models — Pretraining, Alignment, and Inference

> **大语言模型（LLM）是过去五年人工智能领域最具变革性的技术。本章从数据管道和分词开始，逐步深入到对齐技术（RLHF/DPO）、推理增强（CoT/RAG），最后剖析 KV Cache、投机解码、量化等核心系统架构——覆盖从"让模型学会说话"到"让模型说有用的话"的完整链路。**
>
> **Large Language Models (LLMs) are the most transformative technology in AI over the past five years. This chapter walks through the full pipeline — from data pipelines and tokenization, through alignment techniques (RLHF/DPO) and inference enhancement (CoT/RAG), to core system architecture (KV Cache, speculative decoding, quantization) — covering the journey from "teaching a model to speak" to "making it say useful things."**

**前置知识 (Prerequisites):** Transformer 架构 (Chapter 5 of Vol 4), 自监督学习 (Vol 6), 基本的概率论
**依赖库 (Dependencies):** `torch>=2.1.0`, `transformers>=4.36.0`, `numpy>=1.24.0`
**Code companion:** [`code/llm_inference.py`](code/llm_inference.py)

---

## 目录 (Table of Contents)

1. [预训练 (Pretraining)](#1-预训练-pretraining)
2. [对齐 (Alignment)](#2-对齐-alignment)
3. [推理增强 (Inference Enhancement)](#3-推理增强-inference-enhancement)
4. [LLM 系统架构 (System Architecture)](#4-llm-系统架构-system-architecture)

---

## 1. 预训练 (Pretraining)

### 1.1 数据管道 (Data Pipeline)

LLM 的预训练数据主要来自公共互联网爬取。以下是在 CommonCrawl 上构建高质量数据集的典型流程：

```
Raw Web Crawl (CommonCrawl ~PB级)
    │
    ├──→ 1. Heuristic Filtering（规则过滤）
    │       ├── Language detection (langid, FastText) → 保留目标语言
    │       ├── Length filter → 丢弃 < 50 tokens 的文档
    │       ├── Symbol/word ratio → 过滤垃圾内容
    │       └── Perplexity filtering → 用 LM 打分，过滤低质量文档
    │
    ├──→ 2. Deduplication（去重）
    │       ├── Exact dedup (MinHash + LSH) → 精确重复
    │       └── Near-dedup (SimHash, n-gram overlap) → 近似重复
    │
    ├──→ 3. PII Removal（隐私移除）
    │       ├── Email, phone, SSN, IP addresses → 替换为占位符
    │       └── Coarse removal (正则) + Fine-grained (NER模型)
    │
    └──→ 4. Toxicity & Safety Filtering
            └── Blocklist + classifier-based filtering

Final Training Corpus (~万亿 token 级别)
```

- **RefinedWeb** (TII, 2023): 基于 CommonCrawl，经过严格过滤后获得 5T tokens，仅保留原始数据的 ~2-3%
- **Dolma** (AI2, 2024): 开放 3T token，涵盖 CommonCrawl、Reddit、StackExchange、学术论文

### 1.2 分词 (Tokenization)

分词将文本转换为模型可处理的 token 序列。现代 LLM 主要使用两种方法：

#### BPE (Byte-Pair Encoding, Sennrich et al., 2016)

BPE 是一种数据压缩算法，通过迭代合并最频繁的字符对来构建词汇表：

```
Vocabulary: {"a", "b", "c", "d", "e"}
Corpus:     "a b c d e a b c d e a b c a b c"

Step 1: 统计相邻 pair 频率 → ("a", "b"): 3, ("b", "c"): 3, ("c", "d"): 2...
Step 2: 合并最频繁 pair "ab" → 加入词汇表
Step 3: 重复直到词汇表达到目标大小 (e.g., 50,257 for GPT-2)
```

**字节级 BPE (Byte-Level BPE):** GPT-2 采用的方法，在最底层单元使用字节而非字符。这确保：
- **任意输入都可编码**：无 OOV (out-of-vocabulary) 问题
- **语言无关**：Unicode 字符统一处理
- **词汇表大小恒定**：GPT-2 使用 50,257，覆盖所有 UTF-8 序列

```python
# Simplified BPE illustration
from collections import Counter
import re

def get_stats(vocab):
    pairs = Counter()
    for word, freq in vocab.items():
        symbols = word.split()
        for i in range(len(symbols) - 1):
            pairs[symbols[i], symbols[i+1]] += freq
    return pairs

def merge_vocab(pair, vocab):
    new_vocab = {}
    bigram = ' '.join(pair)
    replacement = ''.join(pair)
    for word, freq in vocab.items():
        new_word = word.replace(bigram, replacement)
        new_vocab[new_word] = freq
    return new_vocab
```

#### SentencePiece (Kudo & Richardson, 2018)

SentencePiece 将分词视为一个统一的子词分割问题，直接处理原始文本（无需预分词）：

| 特征 | BPE | SentencePiece (Unigram) |
|:-----|:---:|:----------------------:|
| 是否需要预分词 | 是 (Moses tokenizer) | 否 (直接处理原始文本) |
| 训练算法 | 贪心合并 | EM 算法 + 正则化 |
| 词汇表优化 | 无 | 基于似然的子词剪枝 |
| 典型使用者 | GPT-2, GPT-3, GPT-4 | LLaMA, Mistral, Gemma |
| 处理多语言 | 字节级好，纯字符级差 | 原生支持 |

**LLaMA 的分词方案：** LLaMA 使用 SentencePiece BPE，但关键改进是**不分割数字**并将**空白符视为独立 token**——这显著提升了数学和代码性能。

### 1.3 训练稳定性 (Training Stability)

大语言模型的训练充满不稳定因素。以下是最常见的问题和缓解措施：

#### Loss Spikes (损失尖峰)

Loss spikes 指训练过程中损失函数突然跳升几个数量级的现象：

```
Loss
│
│   ████████████████████████████████████████████████████
│                     ↑                              ██
│                     │ spike (loss × 10-100x)      ██
│   ██████████████████████████████████████████████████  ██
│                                                     ████████
└───────────────────────────────────────────────────────────→ Steps
```

**主要原因：**
1. **梯度爆炸 (Gradient Explosion):** 某些 batch 产生异常大的梯度
2. **Attention 坍塌 (Attention Collapse):** Softmax 数值溢出导致注意力分布失效
3. **数据异常 (Data Anomaly):** batch 中包含异常数据点

**缓解措施：**

| 方法 | 描述 | 效果 |
|:-----|:-----|:----:|
| **Gradient Clipping** | $\text{grad} \gets \text{grad} \times \min(1, \frac{\text{max\_norm}}{\|\text{grad}\|_2})$ | 最直接有效 |
| **Z-Loss** | $\mathcal{L}_z = \alpha \cdot \log(1 + z^2)$，约束 logits 范围 | 防止 logits 发散 |
| **QK LayerNorm** | 在 Attention 的 Q 和 K 之后加 LayerNorm | 稳定注意力分布 |
| **Warmup** | LR 从 0 线性增加到目标值 (通常 2k-10k steps) | 避免初始阶段不稳定 |
| **Activation Checkpointing** | 用重计算减少内存，间接允许更大 batch | 改善梯度统计 |

**PaLM 的经验法则：** PaLM 540B 论文发现，约 0.1-1% 的训练步骤会出现 loss spike，其中约一半自行恢复，另一半需要回滚 checkpoint。

#### Weight Decay (权重衰减)

权重衰减是一种正则化技术，在优化器的更新步骤中额外减去权重的一部分：

$$ \theta_{t+1} = \theta_t - \eta \nabla \mathcal{L}(\theta_t) - \eta \lambda \theta_t $$

- 在 AdamW 中，weight decay 与学习率解耦：$\theta_{t+1} = \theta_t - \eta \nabla \mathcal{L}(\theta_t) - \lambda \theta_t$
- 典型值：$\lambda = 0.1$ (LLaMA), $\lambda = 0.01$ (GPT-3)
- **实际作用：** 在 LLM 训练中，weight decay 主要施加于**未参与 LayerNorm 的权重**和**偏置项**之外的所有参数。对 embedding 层通常不使用 weight decay。

#### Learning Rate Schedule

```
LR
│   ██████████████████████████████
│   │  Warmup  │  Cosine Decay   │
│   │          │                  │
│   │          │   ███████████    │
│   │          │  █           █   │
│   │    ████████              ███│████ Minimal LR
│   └─────────────────────────────→ Steps
        ↑                  ↑
     2k-10k steps      ~10-100× warmup steps
```

$$ \text{LR}(t) = \text{LR}_{\text{max}} \cdot \frac{1}{2} \left(1 + \cos\left(\frac{t - t_{\text{warmup}}}{T - t_{\text{warmup}}} \pi\right)\right) $$

### 1.4 Scaling Laws 回顾 (Recap from Vol 6)

从 Volume 6 我们知道，模型性能与三个关键维度遵循幂律关系：

$$ L(N, D) \approx \left(\frac{N_c}{N}\right)^{\alpha_N} + \left(\frac{D_c}{D}\right)^{\alpha_D} $$

其中 $N$ 是参数量，$D$ 是数据量。

**Chinchilla 最优分配 (Hoffmann et al., 2022):**
对于计算预算 $C$，最优分配为：
- $N_{\text{opt}} \propto C^{0.50}$
- $D_{\text{opt}} \propto C^{0.50}$

这意味着参数和数据应该等比例增长——"数据和模型一样重要"。

---

## 2. 对齐 (Alignment)

预训练后的 LLM 能生成流畅文本，但它不"听话"——因为它只学会了预测下一个 token，而非遵循用户意图。**对齐 (Alignment)** 的目标是让模型生成符合人类偏好的输出。

### 2.1 Instruction Tuning (指令微调)

**Instruction Tuning** 是最直接的对齐方法：收集 (instruction, response) 配对数据，在预训练模型上进行监督微调 (SFT)。

```
数据集格式:
{
  "instruction": "解释什么是机器学习",
  "input": "",
  "output": "机器学习是人工智能的一个分支，它让计算机能够从数据中学习和改进..."
}

训练:
ℒ_SFT(θ) = -𝔼_{(x,y)∼D} [ log π_θ(y|x) ]
```

- **FLAN (Wei et al., 2022):** 将 62 个 NLP 数据集转化为指令格式，微调后显著提升零样本性能
- **LLaMA-2-Chat:** SFT 使用了 27,540 个高质量 annotation
- **关键发现：** 指令数据质量 >> 数量。少量精心标注的数据胜过大量噪声数据

### 2.2 RLHF (Reinforcement Learning from Human Feedback)

RLHF 由三阶段组成：

```
Phase 1: SFT                    Phase 2: Reward Model          Phase 3: PPO
┌──────────────────┐           ┌──────────────────┐           ┌──────────────────┐
│                  │           │                  │           │                  │
│  (x, y) pairs    │           │  (y₁ > y₂ > y₃)  │           │  x → π_θ → y     │
│       ↓          │           │       ↓          │           │       ↓          │
│  SFT on π_ref    │           │  Train r_φ(y|x)  │           │  y scored by r_φ │
│       ↓          │           │                  │           │       ↓          │
│  → π_SFT         │           │  → r_φ(x,y) ∈ ℝ  │           │  PPO update π_θ  │
│                  │           │                  │           │                  │
└──────────────────┘           └──────────────────┘           └──────────────────┘
```

#### Reward Model Training (奖励模型训练)

奖励模型 $r_\phi(x, y)$ 输出一个标量，表示输出 $y$ 在给定输入 $x$ 下的"质量"。

**训练数据：** 人工标注者对同一 prompt 的多个输出进行排序：

$$ \mathcal{L}_{RM}(\phi) = -\mathbb{E}_{(x, y_w, y_l) \sim D} \left[ \log \sigma(r_\phi(x, y_w) - r_\phi(x, y_l)) \right] $$

其中 $y_w$ 是赢得比较的响应，$y_l$ 是输掉的响应。这等价于 Bradley-Terry 偏好模型：

$$ P(y_w \succ y_l \mid x) = \frac{\exp(r_\phi(x, y_w))}{\exp(r_\phi(x, y_w)) + \exp(r_\phi(x, y_l))} = \sigma(r_\phi(x, y_w) - r_\phi(x, y_l)) $$

**InstructGPT 的数据规模：**
- 标注者: 40 人
- 比较对: ~50,000 (prompt, 多个模型输出, 人工排序)
- 质量校验: 标注者一致性 > 80%

#### PPO (Proximal Policy Optimization)

PPO 使用奖励模型 $r_\phi$ 的信号来更新策略 $\pi_\theta$：

$$ \mathcal{L}^{\text{CLIP}}(\theta) = \mathbb{E}_{x \sim D, y \sim \pi_\theta(\cdot|x)} \left[ \min\left( \frac{\pi_\theta(y|x)}{\pi_{\text{old}}(y|x)} A, \ \text{clip}\!\left(\frac{\pi_\theta(y|x)}{\pi_{\text{old}}(y|x)}, 1-\epsilon, 1+\epsilon\right) A \right) \right] $$

其中：
- $A$ 是优势函数（advantage），简化为 $A = r_\phi(x, y) - b(x)$（$b$ 是基线）
- $\epsilon$ 是裁剪范围（通常 0.2），防止更新步长过大
- 概率比例 $r_t(\theta) = \pi_\theta(a_t|s_t) / \pi_{\text{old}}(a_t|s_t)$

**裁剪机制的作用：**

```
Objective
│
│   A > 0 (good action)        A < 0 (bad action)
│   ┌─────────────┐            ┌─────────────┐
│   │ Keep pushing│            │  Ignored:   │
│   │ but clipped │            │ gradient=0  │
│   │ at 1+ε     │            │ beyond 1-ε  │
│   └─────────────┘            └─────────────┘
│
└────────────────────────────────────────→ r_t(θ)
    1-ε  1  1+ε
```

**完整 PPO 目标（包含 KL 惩罚）：**

$$ \mathcal{L}_{\text{PPO}}(\theta) = \mathcal{L}^{\text{CLIP}}(\theta) - \beta \cdot \mathbb{KL}(\pi_\theta \parallel \pi_{\text{ref}}) $$

KL 惩罚项防止策略与初始 SFT 模型偏离太远 —— 避免了"奖励黑客"（reward hacking）。

### 2.3 DPO (Direct Preference Optimization)

DPO (Rafailov et al., 2023) 巧妙地将 RLHF 的两阶段（训练 RM + PPO 更新）合并为一步，**不需要显式的奖励模型**。

**核心洞察：** 最优策略 $\pi^*$ 可以表示为奖励函数的闭式解：

$$ \pi^*(y|x) = \frac{1}{Z(x)} \pi_{\text{ref}}(y|x) \exp\left(\frac{1}{\beta} r(x, y)\right) $$

重新排列得到奖励函数：

$$ r(x, y) = \beta \log\frac{\pi^*(y|x)}{\pi_{\text{ref}}(y|x)} + \beta \log Z(x) $$

代入 Bradley-Terry 偏好模型，$Z(x)$ 消去，得到 DPO 损失：

$$ \mathcal{L}_{\text{DPO}}(\theta) = -\mathbb{E}_{(x, y_w, y_l) \sim D} \left[ \log \sigma\left( \beta \log\frac{\pi_\theta(y_w|x)}{\pi_{\text{ref}}(y_w|x)} - \beta \log\frac{\pi_\theta(y_l|x)}{\pi_{\text{ref}}(y_l|x)} \right) \right] $$

| 对比 | RLHF (PPO) | DPO |
|:-----|:-----------:|:---:|
| 训练阶段 | 3 (SFT → RM → PPO) | 1 (直接优化偏好) |
| 需要奖励模型 | 是 | 否 |
| 内存消耗 | 高 (4个模型: policy, ref, reward, value) | 低 (2个模型: policy, ref) |
| 稳定性 | 需要 careful tuning | 相对稳定 |
| 性能 | SOTA (LLaMA-2, GPT-4) | 接近或持平 SOTA |

---

## 3. 推理增强 (Inference Enhancement)

### 3.1 Chain-of-Thought (CoT, Wei et al., 2022)

**Chain-of-Thought** 通过在 prompt 中添加中间推理步骤来提升 LLM 的复杂推理能力：

```
Standard Prompt:
Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls.
Each can has 3 balls. How many balls does he have now?
A: The answer is 11. ✗ (Wrong!)

Chain-of-Thought Prompt:
Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls.
Each can has 3 balls. How many balls does he have now?
A: Roger starts with 5 balls. 2 cans of 3 balls each = 2×3 = 6.
Total = 5 + 6 = 11. The answer is 11. ✓ (Correct!)
```

**关键发现：** CoT 的效果在模型规模超过约 100B 参数时才显著显现 —— 这是一个 **emergent ability**（涌现能力）。

**CoT 的数学直觉：** 对于需要 $k$ 步推理的问题，直接输出答案需要模型在一步中完成整个推理链，其"有效计算深度"受限于单次前向传播。CoT 将推理过程分解为 $k$ 步，每次前向传播只需要完成一步推理，复杂度从 $O(d^k)$ 降为 $O(k \cdot d)$。

### 3.2 Tree-of-Thought (ToT, Yao et al., 2023)

ToT 扩展了 CoT，允许探索多条推理路径并回溯：

```
Standard CoT:                  Tree-of-Thought:
                              ┌───→ Path 1a → ...
                              │
Start → Step 1 → Step 2 →... ┼───→ Path 2a → Path 2b → ...
(one path, linear)            │
                              └───→ Path 3a → ... (pruned)
                              (multiple paths, search)

ToT 搜索策略:
├── BFS (Breadth-First): 每步保留 Top-k 个中间思考
├── DFS (Depth-First): 深入一条路径，失败则回溯
└── MCTS (Monte Carlo Tree Search): 评估-选择-扩展-回传
```

### 3.3 RAG (Retrieval-Augmented Generation)

RAG 将外部知识检索与 LLM 生成结合，解决 LLM 的知识截断和幻觉问题：

```
Query: "2024 Nobel Prize winners"
    │
    ├──→ 1. Retrieve (检索)
    │       │
    │       ├── Embed query → vector search → Top-k documents
    │       └── Dense retriever (e.g., Contriever, BGE) or Sparse (BM25)
    │
    ├──→ 2. Augment (增强)
    │       │
    │       └── Prompt = [Instruction] + [Retrieved docs] + [Query]
    │
    └──→ 3. Generate (生成)
            │
            └── LLM reads augmented prompt → generates grounded answer

RAG 流程示例 Prompt:
"You are a helpful assistant. Use the following documents to answer the query.

Document 1: The 2024 Nobel Prize in Physics was awarded to John Hopfield...
Document 2: The 2024 Nobel Prize in Chemistry went to David Baker...

Query: Who won the 2024 Nobel Prize in Physics?
Answer:"
```

**RAG 关键设计决策：**

| 决策 | 选项 | 影响 |
|:-----|:-----|:----:|
| Chunk size | 128-1024 tokens | 小 → 精确；大 → 上下文丰富 |
| Top-k | 3-20 documents | 少 → 可能遗漏；多 → 噪音 + 成本 |
| Embedding model | BGE, E5, OpenAI ada-002 | 质量直接影响检索准确性 |
| Reranking | Cross-encoder after retrieval | 可提升 5-10% 准确率 |

### 3.4 Long-Context (长上下文)

扩展 Transformer 的上下文长度是一个核心工程挑战，因为标准注意力机制的计算是 $O(n^2)$。

#### RoPE (Rotary Position Embedding, Su et al., 2021)

RoPE 是当前最流行的位置编码方法。它将位置信息编码为旋转矩阵：

$$ \text{RoPE}(x_m, m) = R_{\Theta, m} \cdot x_m $$

其中 $R_{\Theta, m}$ 是对角块为 $\begin{pmatrix} \cos m\theta_i & -\sin m\theta_i \\ \sin m\theta_i & \cos m\theta_i \end{pmatrix}$ 的稀疏矩阵。

**RoPE 的优势：**
1. **相对位置偏好：** $Q_m \cdot K_n$ 只依赖于 $m-n$
2. **长程衰减：** 长距离 token 的 attention 自然衰减
3. **天然可外推：** 理论上可扩展到训练时未见过的位置

#### RoPE Extrapolation 方法

| 方法 | 描述 | 可扩展长度 |
|:-----|:------|:----------:|
| **PI (Position Interpolation)** | 线性压缩位置索引到训练范围 | 32× |
| **NTK-aware scaling** | 非线性频率缩放，保持高频细节 | 64× |
| **YaRN (Yet another RoPE Nification)** | NTK + 注意力温度调整 | 128× |
| **ALiBi (Press et al., 2021)** | 注意力偏置而非位置编码 | 2× (无微调) |

#### YaRN 原理

YaRN 修改 RoPE 的基频 $\theta_i$ 和注意力 softmax 的温度 $t$：

$$ \theta_i^{\text{YaRN}} = \theta_i \cdot s^{\frac{2i}{d-2}} \quad\text{and}\quad t = \sqrt{\frac{1}{s}} $$

其中 $s$ 是扩展比例（如 $s=32$ 表示扩展到 32 倍长度）。这使得模型能有效处理 128K 甚至更长的上下文。

---

## 4. LLM 系统架构 (System Architecture)

### 4.1 KV Cache

**KV Cache** 是 LLM 推理中最基础的加速技术。在自回归生成中，每个新 token 的注意力计算需要关注所有之前的 token。如果不缓存，每次都要重新计算所有之前的 Key 和 Value。

```
Without KV Cache (O(n² · d) per step):
Step t: Compute K₁,V₁ ... Kₜ,Vₜ from scratch → O(t · d)
Step t+1: Compute K₁,V₁ ... Kₜ₊₁,Vₜ₊₁ from scratch → O((t+1) · d)
Total: O(n² · d)

With KV Cache (O(n · d) per step):
Step 1: Compute K₁,V₁ → Cache
Step t: Compute Kₜ,Vₜ only → Append to cache → O(d)
Step t+1: Compute Kₜ₊₁,Vₜ₊₁ only → Append to cache → O(d)
Total: O(n · d)
```

从实际运行可以看到明显的加速效果：

```
$ python llm_inference.py

=================================================================
2. KV CACHE ANALYSIS -- With vs. Without Cache
=================================================================

  Prompt: "In the beginning, the universe was"
  Target new tokens: ~50

  Method               Avg Time     Avg Tokens   Tok/s
  -------------------- ------------ ------------ ----------
  No KV Cache          6.483       s 50           7.7
  With KV Cache        1.769       s 50           28.3

  Speedup from KV cache: 3.7x
```

**KV Cache 的内存挑战：**

对于 LLaMA-2-70B（80 层，$d=8192$，16 个 KV heads），KV cache 每 token 占用：
$$ \text{Memory per token} = 2 \times 80 \times 8192 \times 128 \times 2\text{ bytes} \approx 320\text{ MB} $$

对于 4096 token 的序列，KV cache 需要约 **1.3 TB** 内存。这催生了 vLLM 的 PagedAttention 等技术。

### 4.2 Speculative Decoding (投机解码)

投机解码通过"小模型草稿，大模型验证"的方式来加速推理，在不改变输出分布的前提下获得 2-3× 加速：

```
  Step 1: Draft (草稿)
  ┌─────────────────────────────────────────┐
  │  Small draft model M_draft (e.g., 7B)   │
  │  Quickly generates k candidate tokens    │
  │  y₁, y₂, ..., y_k (greedy)              │
  └─────────────────────────────────────────┘
                      ↓
  Step 2: Verify (验证)
  ┌─────────────────────────────────────────┐
  │  Large target model M_target (e.g., 70B)│
  │  Forward pass on [prompt, y₁, ..., y_k] │
  │  Obtain logits for each position         │
  │                                          │
  │  For each position i:                    │
  │    if M_target(y_i) == M_draft(y_i):     │
  │      → accept y_i (continue)             │
  │    else:                                 │
  │      → reject at i, resample from        │
  │        M_target's corrected distribution  │
  │      → stop                              │
  └─────────────────────────────────────────┘

  Acceptance rate: 0.7-0.9 (depending on task and model similarity)
  Speedup: k × acceptance_rate (typically 2-3×)
```

**关键约束：** 草稿模型的输出分布必须与目标模型充分接近，否则接受率会大幅下降。

### 4.3 Quantization (量化)

量化将模型权重从高精度格式（FP16/BF16）压缩到低精度格式（INT8/INT4），大幅减少内存占用和推理延迟。

#### 量化级别对比

| 格式 | 比特数 | 内存 (70B) | 精度损失 | 典型方法 |
|:-----|:------:|:----------:|:--------:|:--------:|
| FP16/BF16 | 16 | ~140 GB | 无 | 基线 |
| INT8 | 8 | ~70 GB | < 1% | GPTQ, LLM.int8() |
| INT4 | 4 | ~35 GB | 1-3% | GPTQ, AWQ, GGUF |
| NF4 (QLoRA) | 4 | ~35 GB | < 2% | NormalFloat |

#### GPTQ (Frantar et al., 2023)

GPTQ 使用**后训练量化 (PTQ)**，基于 Hessian 矩阵进行最优量化：

$$ \hat{W} = \arg\min_{\hat{W}} \| WX - \hat{W}X \|_2^2 $$

算法步骤：
1. 从校准数据（如 128 个样本）计算 Hessian $H = 2XX^T$
2. 逐列量化权重，对未被量化的列补偿量化误差
3. 使用 Cholesky 分解高效求解

#### AWQ (Activation-Aware Weight Quantization, Lin et al., 2024)

AWQ 的核心洞察：**权重中只有一小部分对精度至关重要**——这些权重对应于高激活值的通道。AWQ 不直接保留这些权重的精度，而是通过缩放来保护它们：

$$ \text{AWQ: } \hat{W} = \text{quantize}(W \cdot s) \cdot s^{-1} $$

其中 $s$ 是基于激活幅度学习的逐通道缩放因子。AWQ 在 INT4 下通常优于 GPTQ。

#### GGUF / GGML

GGUF (GPT-Generated Unified Format) 是 llama.cpp 使用的格式，特别优化了 CPU 推理。它包含：
- 权重的多种量化方案（Q2_K, Q3_K, Q4_K, Q5_K, Q6_K, Q8_0）
- 性能-精度 tradeoff 清晰分层

```
Q4_K_M: 4-bit, ~4.5 bits/weight (median quality-size tradeoff)
Q5_K_M: 5-bit, ~5.5 bits/weight (higher quality)
Q8_0:   8-bit, ~8.5 bits/weight (near-lossless)
```

### 4.4 vLLM & PagedAttention (Kwon et al., 2023)

**vLLM** 是目前最流行的 LLM 推理引擎。其核心创新 **PagedAttention** 解决了 KV Cache 的内存碎片问题。

#### 问题: KV Cache 的内存碎片

传统系统中，KV cache 被预先分配为一个连续的张量：
```
传统 KV Cache 分配:
┌──────────────────────────────────────────────┐
│  K_cache (pre-allocated contiguous block)     │
│  ████████████████████░░░░░░░░░░░░░░░░░░░░░░  │
│  ↑ used tokens        ↑ unused (wasted)      │
│                        │                      │
│  内部碎片: 预分配但未使用的内存               │
└──────────────────────────────────────────────┘
```

这意味着：
- **内部碎片：** 预分配但未使用的内存（因为不知道最终长度）
- **外部碎片：** 不同请求之间的预留内存无法共享
- **利用率低：** 实际使用通常只有 20-40%

#### PagedAttention 的解决方案

PagedAttention 借鉴操作系统虚拟内存的概念，将 KV Cache 分页管理：

```
PagedAttention KV Cache:
┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐
│Page1│ │Page2│ │Page3│ │Page4│
│ K,V │ │ K,V │ │ K,V │ │ K,V │
└──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘
   │        │        │        │
   └────────┴────────┴────────┘
        Block Table (逻辑→物理映射)
              │
    ┌─────────┴─────────┐
    │ Block 0 → Page 3  │
    │ Block 1 → Page 1  │
    │ Block 2 → Page 7  │
    └───────────────────┘
```

**优势：**
1. **零内部碎片：** 几乎完全避免浪费
2. **按需分配：** 仅分配实际使用的页面
3. **内存共享：** 并行采样、beam search 等场景可共享相同前缀的 KV cache 页面
4. **吞吐量提升：** vLLM 相比基准实现可获得 **2-4× 吞吐量提升**

```
vLLM Throughput Comparison (LLaMA-7B, A100-80G):

  Throughput (requests/s)
  │
 8│                           ████████
  │                           ██ vLLM ██
 6│                           ████████
  │          ████████         ████████
 4│          ██ Base ██       ████████
  │          ████████         ████████
 2│          ████████         ████████
  │   ████████████████████████████████████
  └────────────────────────────────────────→ Batch Size
       1          4          16         64
```

---

## 代码实战 (Code Companion)

详见配套代码文件 [`code/llm_inference.py`](code/llm_inference.py)，涵盖以下四个演示：

1. **解码策略对比** — Greedy, Temperature, Top-k, Top-p, 组合策略
2. **KV Cache 分析** — 计算有/无 cache 时的推理速度和复杂度对比
3. **Prompt 格式化** — ChatML 和 LLaMA-2 风格的指令模板
4. **简化 RLHF 仿真** — SFT → 奖励模型 → PPO 更新

运行输出摘要：

```text
$ python llm_inference.py
[INFO] Device: cpu
[INFO] PyTorch version: 2.10.0+cpu

1. TEXT GENERATION -- Decoding Strategies
  --- 1a. Greedy Decoding (T->0) ---
  Speed: 27.2 tok/s
  Output: The future of AI is uncertain. But it's not clear that AI
  will ever be the dominant force in the world.
  ...
  --- 1b. Temperature Sampling (T=0.8) ---
  Output: The future of AI is already in its infancy. But what is
  more important is how AI is affecting the way we think and behave.
  ...
  --- 1c. High Temperature (T=1.5) ---
  Output: The future of AI is rising wondrous! Not fortunate
  prognosticators or winners fight scientists who give insulting...

2. KV CACHE ANALYSIS
  No KV Cache:  6.48s (7.7 tok/s)
  With KV Cache: 1.77s (28.3 tok/s)
  Speedup from KV cache: 3.7x

3. PROMPT FORMATTING
  ChatML: <|im_start|>system\nYou are a helpful assistant.<|im_end|>...
  LLaMA-2: <s>[INST] Explain what a neural network is [/INST]

4. RLHF SIMULATION
  SFT loss (1 epoch): 2.3242
  Reward model params: 124,440,577
  PPO update: loss=-0.0023, KL=-0.2342, ratio=1.1568
```

---

## 小结 (Summary)

1. **预训练构建基础能力**：从网络爬虫到高质量语料的管道是 LLM 成功的第一步。BPE/SentencePiece 分词需要精心设计。训练稳定性（gradient clipping, warmup, weight decay）决定了训练是否收敛。

2. **对齐让模型"听话"**：Instruction Tuning 提供基础指令遵循能力，RLHF 通过奖励模型和 PPO 将人类偏好注入模型。DPO 提供了更简洁的替代方案。

3. **推理增强扩展能力**：CoT/ToT 提升了推理任务的性能，RAG 解决了知识更新和幻觉问题，长上下文技术（YaRN, ALiBi）将有效上下文窗口扩展到 100K+ token。

4. **系统架构决定部署效率**：KV Cache 是推理加速的基石，投机解码提供 2-3× 额外加速，量化（GPTQ, AWQ, GGUF）使大模型能在消费级硬件上运行，vLLM 的 PagedAttention 解决了 KV Cache 的内存碎片问题。

---

**进一步阅读 (Further Reading):**
- Wei et al. (2022). "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." — CoT
- Ouyang et al. (2022). "Training language models to follow instructions with human feedback." — InstructGPT / RLHF
- Rafailov et al. (2023). "Direct Preference Optimization: Your Language Model is Secretly a Reward Model." — DPO
- Kwon et al. (2023). "Efficient Memory Management for Large Language Model Serving with PagedAttention." — vLLM
- Frantar et al. (2023). "GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers." — GPTQ
- Lin et al. (2024). "AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration." — AWQ
- Su et al. (2021). "RoFormer: Enhanced Transformer with Rotary Position Embedding." — RoPE
- Leviathan et al. (2023). "Fast Inference from Transformers via Speculative Decoding." — Speculative Decoding
