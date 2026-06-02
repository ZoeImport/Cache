# 第4章 动手实现 Transformer
# Chapter 4: Implement a Transformer from Scratch

> **理论指导实践。本章引导你从零实现一个 decoder-only Transformer（GPT 风格），在 tiny Shakespeare 数据集上训练一个字符级语言模型，并用它生成莎士比亚风格的文本。** 每一段代码都标注了与之对应的 Transformer 架构概念。
>
> **Theory guides practice. This chapter walks you through implementing a decoder-only Transformer (GPT-style) from scratch, training a character-level language model on tiny Shakespeare, and generating Shakespeare-style text.** Every block of code is annotated with the corresponding Transformer architecture concept.

**前置知识 (Prerequisites):** Transformer 架构概览（第1章），自注意力机制（第2章），PyTorch 基础
**依赖库 (Dependencies):** `torch>=2.1.0`, `numpy`
**Code companion:** [`code/04-implement-transformer.py`](code/04-implement-transformer.py)

---

## 目录 (Table of Contents)

1. [代码总览 (Code Overview)](#1-代码总览-code-overview)
2. [Token Embedding + Positional Encoding](#2-token-embedding--positional-encoding)
3. [Multi-Head Self-Attention](#3-multi-head-self-attention)
4. [Feed-Forward Network](#4-feed-forward-network)
5. [Transformer Block](#5-transformer-block)
6. [完整模型 (Full Model)](#6-完整模型-full-model)
7. [训练循环 (Training Loop)](#7-训练循环-training-loop)
8. [文本生成 (Text Generation)](#8-文本生成-text-generation)
9. [完整代码-概念映射表](#9-完整代码-概念映射表)

---

## 1. 代码总览 (Code Overview)

整个实现文件 `code/04-implement-transformer.py` 约 280 行，结构如下：

| 代码块 | 行号 | 对应的 Transformer 架构概念 |
|:-------|:-----|:---------------------------|
| 超参数 | 40-53 | 模型配置：`d_model=64`, `n_head=4`, `n_layer=2` |
| 数据加载 | 59-100 | 字符级 tokenization |
| `TokenEmbedding` | 107-118 | Transformer Ch.1: Token Embedding |
| `PositionalEncoding` | 120-143 | Transformer Ch.1: Positional Encoding (正弦波) |
| `MultiHeadSelfAttention` | 149-200 | Transformer Ch.2: Scaled Dot-Product Attention + Multi-Head |
| `FeedForward` | 206-219 | Transformer Ch.2: Position-wise FFN |
| `TransformerBlock` | 225-240 | Transformer Ch.2: 完整的 Block (Add & Norm) |
| `TransformerLM` | 248-275 | 完整的 decoder-only 语言模型 |
| `generate` | 278-293 | Transformer Ch.4: 自回归生成 |
| 训练循环 | 310-345 | 交叉熵损失 + AdamW 优化 |

---

## 2. Token Embedding + Positional Encoding

**文件位置:** `code/04-implement-transformer.py`, 第 107-143 行

### TokenEmbedding (行 107-118)

```python
class TokenEmbedding(nn.Module):
    def __init__(self):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, EMBED_DIM)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.embed(x)
```

**概念映射:** Transformer 论文 Section 3.4 — "Embeddings and Softmax"

词汇表中的每个 token（这里是一个字符）被映射到一个 `d_model` 维的连续向量。这个嵌入矩阵在训练过程中学习，最终会捕获字符之间的语义相似性。

> 在原始 Transformer 论文中，嵌入层与 softmax 前的线性层**共享权重**（weight tying）。我们的实现也采用了这一技巧（第 265 行）。

### PositionalEncoding (行 120-143)

```python
class PositionalEncoding(nn.Module):
    def __init__(self):
        super().__init__()
        pe = torch.zeros(CONTEXT_LENGTH, EMBED_DIM)
        position = torch.arange(0, CONTEXT_LENGTH, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(
            torch.arange(0, EMBED_DIM, 2).float() *
            (-math.log(10000.0) / EMBED_DIM)
        )
        pe[:, 0::2] = torch.sin(position * div_term)   # 偶数维度
        pe[:, 1::2] = torch.cos(position * div_term)   # 奇数维度
        pe = pe.unsqueeze(0)
        self.register_buffer("pe", pe)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x + self.pe[:, : x.size(1), :]
```

**概念映射:** Transformer 论文 Section 3.5 — "Positional Encoding"

公式:

$$PE_{(pos,2i)} = \sin\left(\frac{pos}{10000^{2i/d_{\text{model}}}}\right)$$
$$PE_{(pos,2i+1)} = \cos\left(\frac{pos}{10000^{2i/d_{\text{model}}}}\right)$$

**为什么需要 Positional Encoding？**

Self-attention 是**排列等变 (permutation equivariant)** 的——它将输入集视为无序集合。如果没有位置信息，句子 "I eat fish" 和 "fish eat I" 会产生相同的表示。

正弦波编码比可学习编码的优势在于：
1. 可以外推到比训练时更长的序列
2. 不同频率的组合让模型可以容易地通过相对位置来学习

**代码中发生了什么？**
- 每个位置 `pos` 得到一个 `d_model` 维的向量，其每个维度是一个不同频率的正弦/余弦波
- 这个向量与 token embedding **相加**（而非拼接），因此总维度保持 `d_model`

---

## 3. Multi-Head Self-Attention

**文件位置:** `code/04-implement-transformer.py`, 第 149-200 行

这是 Transformer 最核心的组件。

```python
class MultiHeadSelfAttention(nn.Module):
    def __init__(self):
        super().__init__()
        assert EMBED_DIM % N_HEAD == 0
        self.head_dim = EMBED_DIM // N_HEAD    # d_k = 64/4 = 16
        self.qkv = nn.Linear(EMBED_DIM, 3 * EMBED_DIM, bias=False)
        self.proj = nn.Linear(EMBED_DIM, EMBED_DIM, bias=False)
        self.dropout = nn.Dropout(DROPOUT)

        # Causal mask: 下三角矩阵
        mask = torch.tril(torch.ones(CONTEXT_LENGTH, CONTEXT_LENGTH))
        self.register_buffer("mask", mask)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        B, T, C = x.shape
        # 1. 融合投影 Q, K, V
        qkv = self.qkv(x)                      # (B, T, 3*d_model)
        q, k, v = qkv.chunk(3, dim=-1)

        # 2. 拆分为多头
        q = q.view(B, T, N_HEAD, self.head_dim).transpose(1, 2)
        k = k.view(B, T, N_HEAD, self.head_dim).transpose(1, 2)
        v = v.view(B, T, N_HEAD, self.head_dim).transpose(1, 2)

        # 3. Scaled dot-product attention
        attn = (q @ k.transpose(-2, -1)) * (1.0 / math.sqrt(self.head_dim))
        attn = attn.masked_fill(self.mask[:T, :T] == 0, float("-inf"))
        attn = F.softmax(attn, dim=-1)
        attn = self.dropout(attn)

        # 4. 加权求和
        out = attn @ v

        # 5. 拼接多头 & 投影回 d_model
        out = out.transpose(1, 2).contiguous().view(B, T, C)
        out = self.proj(out)
        return out
```

### 概念映射: Transformer 论文 Section 3.2 — "Attention"

#### Scaled Dot-Product Attention

$$ \text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right) V $$

对应代码第 182-185 行：

- `q @ k.transpose(-2, -1)` — 计算所有位置对之间的**注意力分数**（相似度矩阵）
- `* (1.0 / math.sqrt(self.head_dim))` — **缩放因子** $\frac{1}{\sqrt{d_k}}$，防止点积过大导致 softmax 梯度消失
- `masked_fill(...)` — 应用**因果掩码 (causal mask)**，确保位置 $i$ 只能关注到位置 $\leq i$
- `softmax` — 将分数归一化为概率分布（注意力权重）
- `attn @ v` — 按照注意力权重对 value 加权求和

#### Multi-Head Attention

$$ \text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, ..., \text{head}_h) W^O $$
$$ \text{where head}_i = \text{Attention}(QW_i^Q, KW_i^K, VW_i^V) $$

对应代码第 172-196 行：

- 第 172-173 行：将 `d_model` 拆分为 `N_HEAD` 个 `d_k` 维的子空间
- 第 182-186 行：每个头独立计算注意力
- 第 193-196 行：拼接所有头并用 `proj` 投影回 `d_model`

**为什么需要多头？**

多头注意力允许模型在不同**表示子空间**中同时关注不同位置的信息。例如，一个头可能学习语法依赖（主语-动词），另一个头学习语义关系（实体-属性）。

#### 因果掩码 (Causal Mask)

对于 decoder-only 语言模型，每个 token 只能关注到它**之前**（包括自身）的 token。这通过一个**下三角掩码**实现：

```
Token 1: [1, 0, 0, 0, 0]
Token 2: [1, 1, 0, 0, 0]
Token 3: [1, 1, 1, 0, 0]
Token 4: [1, 1, 1, 1, 0]
Token 5: [1, 1, 1, 1, 1]
```

被掩码的位置在 softmax 之前被设为 $-\infty$，从而注意力权重为 0。

---

## 4. Feed-Forward Network

**文件位置:** `code/04-implement-transformer.py`, 第 206-219 行

```python
class FeedForward(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(EMBED_DIM, FFN_HIDDEN),
            nn.GELU(),
            nn.Linear(FFN_HIDDEN, EMBED_DIM),
            nn.Dropout(DROPOUT),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)
```

### 概念映射: Transformer 论文 Section 3.3 — "Position-wise Feed-Forward Networks"

$$ \text{FFN}(x) = \max(0, xW_1 + b_1)W_2 + b_2 $$

每个位置**独立地**应用同一个 FFN（但参数共享所有位置）。

- 第一个线性层从 `d_model=64` 扩展到 `FFN_HIDDEN=256`（4 倍扩展）
- GELU 激活函数（比 ReLU 更平滑的变体）
- 第二个线性层投影回 `d_model`

**为什么需要 FFN？**

注意力层主要负责**在不同位置之间交换信息**，而 FFN 在每个位置独立地进行**非线性变换**，增加模型的表达能力。可以理解为：注意力层是"通信"步骤，FFN 是"计算"步骤。

> "Attention is the communication channel; FFN is the computation."
> — 引自 Transformer 理解社区格言

---

## 5. Transformer Block

**文件位置:** `code/04-implement-transformer.py`, 第 225-240 行

```python
class TransformerBlock(nn.Module):
    def __init__(self):
        super().__init__()
        self.attn = MultiHeadSelfAttention()
        self.ffn  = FeedForward()
        self.ln1  = nn.LayerNorm(EMBED_DIM)
        self.ln2  = nn.LayerNorm(EMBED_DIM)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x + self.attn(self.ln1(x))   # Self-Attention + Residual
        x = x + self.ffn(self.ln2(x))    # FFN + Residual
        return x
```

### 概念映射: Transformer 论文 Section 3.1 — "Encoder and Decoder Stacks"

#### 残差连接 (Residual Connection)

$$ \text{output} = x + \text{SubLayer}(x) $$

每个子层（注意力或 FFN）都包裹在残差连接中。这有几个关键作用：

1. **梯度传播**：梯度可以直接通过残差路径流动，避免深层网络中的梯度消失
2. **信息保留**：原始输入信息始终可直接访问
3. **训练稳定性**：即使子层输出很小，主路径仍保持信息

#### 层归一化 (Layer Normalization)

我们的实现使用 **Pre-LayerNorm** 结构（在子层**之前**应用 LayerNorm），这是 GPT-2 及后续模型的标准做法，已被证明比原始 Transformer 的 Post-LayerNorm **训练更稳定**。

LayerNorm 的作用：

$$ \text{LayerNorm}(x) = \gamma \odot \frac{x - \mu}{\sqrt{\sigma^2 + \epsilon}} + \beta $$

其中 $\mu$ 和 $\sigma$ 是每个 token 的均值和标准差，$\gamma, \beta$ 是可学习的缩放和偏移参数。

#### 一个 Block 的完整数据流

```
输入 x (B, T, d_model)
    │
    ├──→ LayerNorm → Multi-Head Self-Attention → + (残差) → x'
    │
    └──→ LayerNorm → Feed-Forward Network → + (残差) → 输出
```

---

## 6. 完整模型 (Full Model)

**文件位置:** `code/04-implement-transformer.py`, 第 248-275 行

```python
class TransformerLM(nn.Module):
    def __init__(self):
        super().__init__()
        self.token_embed = TokenEmbedding()
        self.pos_embed   = PositionalEncoding()
        self.blocks      = nn.ModuleList([
            TransformerBlock() for _ in range(N_LAYER)
        ])
        self.ln_final    = nn.LayerNorm(EMBED_DIM)
        self.lm_head     = nn.Linear(EMBED_DIM, vocab_size)

        # Weight tying
        self.token_embed.embed.weight = self.lm_head.weight

    def forward(self, idx):
        x = self.token_embed(idx)       # (B, T) → (B, T, d_model)
        x = self.pos_embed(x)           # 添加位置信息
        for block in self.blocks:
            x = block(x)                # N 个 Transformer Block
        x = self.ln_final(x)            # 最终 LayerNorm
        logits = self.lm_head(x)        # 投影到词汇表
        return logits
```

### 概念映射: 完整的 Transformer 架构

| 组件 | 代码位置 | 概念来源 |
|:-----|:---------|:---------|
| TokenEmbedding | 第 107 行 | Transformer §3.4 |
| PositionalEncoding | 第 120 行 | Transformer §3.5 |
| MultiHeadSelfAttention | 第 149 行 | Transformer §3.2 |
| FeedForward | 第 206 行 | Transformer §3.3 |
| Residual + LayerNorm | 第 233-234 行 | Transformer §3.1 |
| Weight Tying | 第 265 行 | Press & Wolf 2017 |

#### 整体架构图

```
 字符序列: "R O M E O : \n"
     ↓                                                         (B, T)
 TokenEmbedding (vocab_size → d_model)
     ↓                                                         (B, T, d_model)
 PositionalEncoding (sin/cos added)
     ↓                                                         (B, T, d_model)
 ┌──────────────────────────────────────────────────────────┐
 │  TransformerBlock 1                                       │
 │  ┌─────────────────┐   ┌──────────────────┐              │
 │  │ Self-Attention   │   │  FFN             │              │
 │  │ (4 heads, d_k=16)│   │  d_model→256→64  │              │
 │  │ + Residual + LN  │   │  + Residual + LN │              │
 │  └─────────────────┘   └──────────────────┘              │
 ├──────────────────────────────────────────────────────────┤
 │  TransformerBlock 2                                       │
 │  ┌─────────────────┐   ┌──────────────────┐              │
 │  │ Self-Attention   │   │  FFN             │              │
 │  │ (4 heads, d_k=16)│   │  d_model→256→64  │              │
 │  │ + Residual + LN  │   │  + Residual + LN │              │
 │  └─────────────────┘   └──────────────────┘              │
 └──────────────────────────────────────────────────────────┘
     ↓                                                         (B, T, d_model)
 LayerNorm (final)
     ↓                                                         (B, T, d_model)
 Linear (d_model → vocab_size) = LM Head
     ↓                                                         (B, T, vocab_size)
 softmax (per position)
     ↓                                                         (B, T, vocab_size)
 下一个字符的概率分布
```

---

## 7. 训练循环 (Training Loop)

**文件位置:** `code/04-implement-transformer.py`, 第 310-346 行

```python
for epoch in range(1, NUM_EPOCHS + 1):
    model.train()
    for _ in range(50):            # 每 epoch 50 个 batch
        x, y = get_batch("train")   # x: 输入序列, y: 目标序列（右移一位）
        logits = model(x)
        loss = criterion(logits.view(-1, vocab_size), y.view(-1))

        optimizer.zero_grad()
        loss.backward()
        clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
```

### 概念映射

#### 语言建模目标

我们训练模型预测**下一个 token**（字符级语言模型）。每个输入序列 $x_{1:T}$ 的目标 $y_{1:T}$ 是相同序列右移一位：

```
输入:  [R, O, M, E, O, :, \n]
目标:  [O, M, E, O, :, \n, ...]
```

这通过交叉熵损失优化：

$$ \mathcal{L} = -\frac{1}{T}\sum_{t=1}^{T} \log P(y_t | x_{1:t}) $$

#### 为什么用因果掩码？

在训练时，我们需要确保模型在预测位置 $t$ 的 token 时，不能"偷看"位置 $>t$ 的 token。因果掩码强制了这一点，使得训练和推理时模型的行为一致。

#### Gradient Clipping

梯度裁剪（第 337 行）将梯度的总范数限制在 `max_norm=1.0`，这是训练 Transformer 的关键技巧，防止因梯度爆炸导致的训练崩溃。

#### 验证集 (Validation)

我们每 `EVAL_EVERY` 个 epoch 在验证集上计算损失，以监控过拟合。验证集是训练集最后 10% 的数据。

---

## 8. 文本生成 (Text Generation)

**文件位置:** `code/04-implement-transformer.py`, 第 278-293 行

```python
@torch.no_grad()
def generate(self, idx, max_new_tokens, temperature=1.0):
    for _ in range(max_new_tokens):
        idx_cond = idx[:, -CONTEXT_LENGTH:]
        logits = self(idx_cond)                  # 前向传播
        logits = logits[:, -1, :] / temperature  # 取最后一步 + 温度缩放
        probs  = F.softmax(logits, dim=-1)
        next_idx = torch.multinomial(probs, num_samples=1)  # 采样
        idx = torch.cat((idx, next_idx), dim=1)
    return idx
```

### 概念映射: Transformer §4 — "Why Self-Attention" + 自回归生成

#### 自回归生成流程

1. **种子上下文**: 用一段文本（如 "ROMEO:\n"）作为初始上下文
2. **前向传播**: 将当前序列送入模型，获取最后一个位置的 logits
3. **温度采样**: 对 logits 应用温度缩放后采样下一个 token
4. **拼接**: 将采样的 token 拼接到序列末尾
5. **重复步骤 2-4**: 直到生成足够长度的文本

> 注意：每次生成只使用最近的 `CONTEXT_LENGTH` 个 token（第 281 行），因为模型的注意力范围受限于上下文窗口。

#### Temperature Sampling

温度参数 $T$ 控制生成文本的"创造性"：

$$ P_i = \frac{\exp(z_i / T)}{\sum_j \exp(z_j / T)} $$

| 温度 | 效果 |
|:-----|:-----|
| $T \to 0$ | 退化为贪心解码（总是选概率最大的 token）— 重复、确定性 |
| $T = 1.0$ | 使用原始概率分布采样 |
| $T > 1$ | 分布更均匀 — 更多创造性、更多错误 |
| $T < 1$ | 分布更尖锐 — 更保守、更安全 |

在训练过程中，我们以三种温度（0.5, 0.8, 1.2）生成样本来展示不同效果。

---

## 9. 完整代码-概念映射表

以下是从代码行号到 Transformer 论文概念的完整映射：

| 代码行 | 组件 | 论文引用 | 说明 |
|:-------|:-----|:---------|:-----|
| 40-53 | 超参数 | §3.1 | `d_model=64`, `h=4`, `N=2` |
| 59-100 | 数据 & Tokenization | — | 字符级 tokenization |
| 107-118 | `TokenEmbedding` | §3.4 | 将离散 token 映射为连续向量 |
| 120-143 | `PositionalEncoding` | §3.5 | 正弦波位置编码 |
| 157-161 | `MultiHeadSelfAttention.__init__` | §3.2 | QKV 投影 + 因果掩码 |
| 175-177 | QKV 拆分 | §3.2.2 | `q = xW_Q`, `k = xW_K`, `v = xW_V` |
| 179-181 | Multi-Head 重塑 | §3.2.2 | `d_model → h × d_k` |
| 183 | 缩放点积注意力 | §3.2.1 | $\text{softmax}(QK^T/\sqrt{d_k})$ |
| 184 | 因果掩码 | §3.1 | 下三角矩阵，确保自回归性 |
| 193-196 | 多头拼接 + 投影 | §3.2.2 | $\text{Concat(head}_i)W^O$ |
| 206-219 | `FeedForward` | §3.3 | $\text{FFN}(x) = \text{GELU}(xW_1)W_2$ |
| 225-240 | `TransformerBlock` | §3.1 | 残差连接 $\oplus$ 层归一化 |
| 231 | Pre-LayerNorm | §3.1 | 子层前的 LayerNorm（GPT 风格） |
| 257-274 | `TransformerLM` | §3.1 | 完整架构：嵌入 → N×Block → LN → 线性 |
| 265 | Weight Tying | §3.4 | 嵌入与输出层共享权重 |
| 280-293 | `generate` | — | 自回归采样生成 |
| 295-296 | AdamW | — | 带权重衰减的 Adam |
| 337 | Gradient Clipping | — | 防止梯度爆炸 |
| 357-360 | Temperature Sampling | — | 控制生成多样性 |

---

## 小结 (Summary)

1. **Transformer 的实现可以分解为 4 个核心组件**：嵌入（Embedding + Positional Encoding）、自注意力（Multi-Head Self-Attention）、前馈网络（FFN）、以及将它们组合在一起的 Block（残差连接 + LayerNorm）。

2. **自注意力是 Transformer 的心脏**——它允许序列中的每个位置与所有其他位置直接通信，通过因果掩码确保自回归性。

3. **训练是通过下一个 token 预测（语言建模）进行的**——模型学习在给定上下文条件下预测下一个字符的概率分布。

4. **生成是通过自回归采样进行的**——模型一次生成一个 token，将新生成的 token 作为下一步的输入。

5. **所有组件协同工作**：
   - Token Embedding 将离散符号变为连续向量
   - Positional Encoding 注入序列顺序信息
   - Multi-Head Attention 在不同子空间中捕获不同的关系模式
   - FFN 在每个位置进行非线性变换
   - Residual Connections 确保深层网络的梯度流动
   - LayerNorm 稳定训练过程

---

**进一步阅读 (Further Reading):**
- Vaswani et al. (2017). "Attention Is All You Need." — 原始 Transformer 论文
- Karpathy. "nanoGPT" (https://github.com/karpathy/nanoGPT) — 本实现的灵感来源
- Press & Wolf (2017). "Using the Output Embedding to Improve Language Models." — Weight Tying 论文
- Phuong & Hutter (2022). "Formal Algorithms for Transformers." — Transformer 的严谨数学描述
