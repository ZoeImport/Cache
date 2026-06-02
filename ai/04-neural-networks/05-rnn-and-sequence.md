# 第5章 循环神经网络与序列模型
# Chapter 5: Recurrent Neural Networks and Sequence Models

> **序列数据无处不在：文本、语音、时间序列、基因序列……RNN 是第一个真正为序列建模而设计的神经网络架构。** 本章推导 RNN 的核（kernel /ˈkɜːrnl/）心机制——循环计算图与随时间反向传播（backpropagation /ˌbækprəpəˈɡeɪʃən/）（BPTT），并深入 LSTM 的门控机制如何解决长程依赖问题。最后，我们分析 RNN 的固有瓶颈，并以此为桥梁引出注意力（attention /əˈtenʃən/）机制（Attention），为后续 Transformer（/trænsˈfɔːrmər/） 的学习做好铺垫。
> > **时间线**:
> > - **1982**: Hopfield 提出 Hopfield 网络
> > - **1990**: Elman 提出简单循环网络（SRN）
> - **1997**: Hochreiter & Schmidhuber 发表 LSTM
>
> **Sequential data is everywhere: text, speech, time series, gene sequences... RNN is the first neural architecture truly designed for sequence modeling.** This chapter derives RNN's core mechanism — the recurrent computation graph and Backpropagation Through Time (BPTT) — and dives into how LSTM's gating mechanism solves long-term dependency problems. Finally, we analyze RNN's inherent bottleneck, building a bridge to the Attention mechanism that follows in Volume 5.

**前置知识 (Prerequisites):** 前馈神经网络基础（第4章第1-2节），矩阵求导（AI数学基础第3章），反向传播（第4章第3节）
**依赖库 (Dependencies):** `torch>=2.1.0`, `numpy`
**Code companion:** [`code/rnn_lstm.py`](code/rnn_lstm.py)

---

## 目录 (Table of Contents)

1. [RNN 循环计算图 (RNN Recurrent Computation Graph)](#1-rnn-循环计算图-rnn-recurrent-computation-graph)
   - 1.1 [问题定义：为什么需要"循环"？](#11-问题定义为什么需要循环)
   - 1.2 [RNN 基本公式](#12-rnn-基本公式)
   - 1.3 [展开的计算图 (Unrolled Graph)](#13-展开的计算图-unrolled-graph)
   - 1.4 [随时间反向传播 (BPTT)](#14-随时间反向传播-bptt)
   - 1.5 [梯度（gradient /ˈɡreɪdiənt/）消失与梯度爆炸](#15-梯度消失与梯度爆炸)

2. [LSTM (Long Short-Term Memory)](#2-lstm-long-short-term-memory)
   - 2.1 [核心思想：信息高速公路](#21-核心思想信息高速公路)
   - 2.2 [遗忘门 (Forget Gate)](#22-遗忘门-forget-gate)
   - 2.3 [输入门 (Input Gate)](#23-输入门-input-gate)
   - 2.4 [细胞状态更新 (Cell State Update)](#24-细胞状态更新-cell-state-update)
   - 2.5 [输出门 (Output Gate)](#25-输出门-output-gate)
   - 2.6 [为什么 LSTM 能缓解梯度消失？](#26-为什么-lstm-能缓解梯度消失)
   - 2.7 [完整 LSTM 前向传播总结](#27-完整-lstm-前向传播总结)

3. [GRU (Gated Recurrent Unit)](#3-gru-gated-recurrent-unit)
   - 3.1 [GRU 的设计动机](#31-gru-的设计动机)
   - 3.2 [GRU 公式推导](#32-gru-公式推导)
   - 3.3 [LSTM vs GRU](#33-lstm-vs-gru)

4. [编码器（encoder /ɪnˈkoʊdər/）-解码器（decoder /diːˈkoʊdər/）架构 (Encoder-Decoder Architecture)](#4-编码器-解码器架构-encoder-decoder-architecture)
   - 4.1 [固定维度的上下文向量](#41-固定维度的上下文向量)
   - 4.2 [编码器-解码器的信息瓶颈](#42-编码器-解码器的信息瓶颈)

5. [为什么需要 Attention？](#5-为什么需要-attention)
   - 5.1 [从瓶颈到查阅](#51-从瓶颈到查阅)
   - 5.2 [Attention 的直觉](#52-attention-的直觉)

6. [小结 (Summary)](#6-小结-summary)

---

## 1. RNN 循环计算图 (RNN Recurrent Computation Graph)

### 1.1 问题定义：为什么需要"循环"？

前馈网络（FNN）有一个根本性限制：**输入长度必须固定**。

对于一条句子，例如 "I love neural networks"，我们无法预先知道句子的长度。更重要的是，词与词之间有**顺序依赖关系**——"love" 的语义受到前面的 "I" 的影响。如果只是把每个词独立地送入一个全连接层，前后信息就被割裂了。

**RNN 的解决方案**：引入一个**隐藏状态 (hidden state)** $h_t$，它在每个时间步更新，并携带过去的信息：

$$ h_t = f(h_{t-1}, x_t) $$

### 1.2 RNN 基本公式

最简单的 RNN（有时称为 Elman RNN）定义如下：

**隐藏状态更新 (Hidden State Update):**

$$ h_t = \tanh(W_{hh} h_{t-1} + W_{xh} x_t + b_h) $$

**输出 (Output):**

$$ y_t = W_{hy} h_t + b_y $$

其中：
- $x_t \in \mathbb{R}^{d}$ — 在时间步 $t$ 的输入向量（如词嵌入（embedding /ɪmˈbedɪŋ/））
- $h_{t-1} \in \mathbb{R}^{d_h}$ — 上一个时间步的隐藏状态
- $h_t \in \mathbb{R}^{d_h}$ — 当前时间步的隐藏状态
- $W_{hh} \in \mathbb{R}^{d_h \times d_h}$ — **循环权重矩阵**（RNN 的核心——连接前后时间步）
- $W_{xh} \in \mathbb{R}^{d_h \times d}$ — 输入权重矩阵
- $W_{hy} \in \mathbb{R}^{d_y \times d_h}$ — 输出权重矩阵
- $b_h, b_y$ — 偏置项
- $\tanh$ — 激活函数（将值压缩到 $(-1, 1)$，给非线性以稳定梯度）

> **关键观察**：$W_{hh}$ 在所有时间步**共享**。这意味着无论序列多长，RNN 都在使用同一组参数（parameter /pəˈræmɪtər/）处理每一个时间步——这就是"循环"的含义。

### 1.3 展开的计算图 (Unrolled Graph)

将循环结构"展开"成时间维度的前馈图，有助于理解 RNN 的计算流：

```
        y_1         y_2         y_3         y_T
        ↑           ↑           ↑           ↑
        W_hy        W_hy        W_hy        W_hy
    ┌───┴───┐   ┌───┴───┐   ┌───┴───┐   ┌───┴───┐
h_0→│ h_1  │→→→│ h_2  │→→→│ h_3  │→⋯→│ h_T  │
    └───┬───┘   └───┬───┘   └───┬───┘   └───┬───┘
        ↑           ↑           ↑           ↑
       x_1         x_2         x_3         x_T
```

> **图 5.1:** RNN 展开后的计算图。注意 $W_{hh}$ 在所有时间步是同一个矩阵——虚箭头代表循环连接，展开后变成从左到右的实心传递。

**展开后的视角**：RNN 等价于一个**极深的"前馈"网络**，其深度等于序列长度 $T$。每一层的权重都相同（参数共享）。这使得 BPTT 在概念上就是普通 BP 在展开图上的直接应用。

### 1.4 随时间反向传播 (BPTT)

BPTT (Backpropagation Through Time) 就是在**展开后的计算图上应用反向传播**。

#### 损失函数

定义在 $T$ 个时间步上的总损失为每个时间步损失的累加：

$$ \mathcal{L} = \sum_{t=1}^{T} \mathcal{L}_t(y_t, \hat{y}_t) $$

以 MSE 为例：$\mathcal{L}_t = \frac{1}{2} \|y_t - \hat{y}_t\|_2^2$。

#### 对 $W_{hy}$ 的梯度

$W_{hy}$ 直接影响输出 $y_t$，梯度可以直接从每个时间步反向传播回来：

$$ \frac{\partial \mathcal{L}}{\partial W_{hy}} = \sum_{t=1}^{T} \frac{\partial \mathcal{L}_t}{\partial W_{hy}} = \sum_{t=1}^{T} \frac{\partial \mathcal{L}_t}{\partial y_t} \cdot h_t^T $$

#### 对 $W_{hh}$ 的梯度（关键）

$W_{hh}$ 的梯度**需要沿时间方向传播**，因为 $h_t$ 依赖于 $h_{t-1}$。考虑一个具体时间步 $t$ 对 $W_{hh}$ 的影响：

$$ \frac{\partial \mathcal{L}_t}{\partial W_{hh}} = \sum_{k=1}^{t} \frac{\partial \mathcal{L}_t}{\partial h_t} \frac{\partial h_t}{\partial h_k} \frac{\partial h_k}{\partial W_{hh}} $$

核心在于 $\frac{\partial h_t}{\partial h_k}$ — 这是从时间 $k$ 到时间 $t$ 的梯度链：

$$ \frac{\partial h_t}{\partial h_k} = \prod_{j=k+1}^{t} \frac{\partial h_j}{\partial h_{j-1}} = \prod_{j=k+1}^{t} \text{diag}\left(1 - h_j^2\right) \cdot W_{hh} $$

其中 $\text{diag}(1 - h_j^2)$ 来自 $\tanh$ 的导数：$\frac{d}{dx}\tanh(x) = 1 - \tanh^2(x)$。

**最终，对 $W_{hh}$ 的梯度是所有路径的总和：**

$$ \frac{\partial \mathcal{L}}{\partial W_{hh}} = \sum_{t=1}^{T} \sum_{k=1}^{t} \frac{\partial \mathcal{L}_t}{\partial h_t} \left( \prod_{j=k+1}^{t} \frac{\partial h_j}{\partial h_{j-1}} \right) \frac{\partial h_k}{\partial W_{hh}} $$

### 1.5 梯度消失与梯度爆炸

从上面的推导，我们得到：

$$ \frac{\partial h_j}{\partial h_{j-1}} = \text{diag}\left(1 - h_j^2\right) \cdot W_{hh} $$

这是一个**连乘**结构。假设我们定义矩阵谱范数 $\|W_{hh}\|_2$：

- **如果 $\|W_{hh}\|_2 < 1$**：连乘项 $\prod \frac{\partial h_j}{\partial h_{j-1}} \to 0$ 当 $t-k$ 很大时 ⟹ **梯度消失 (Vanishing Gradient)**
- **如果 $\|W_{hh}\|_2 > 1$**：连乘项 $\prod \frac{\partial h_j}{\partial h_{j-1}} \to \infty$ 当 $t-k$ 很大时 ⟹ **梯度爆炸 (Exploding Gradient)**

> **为什么这是致命问题？**
>
> **梯度消失**意味着距离较远的时间步对当前参数的更新几乎没有贡献。RNN 无法学习"长程依赖"——例如在句子 "I grew up in France... I speak **French**" 中，最后一个词需要记忆前面的 "France"。如果距离太远，梯度消失使得这种学习几乎不可能。
>
> **梯度爆炸**意味着参数更新过大，训练不稳定（NaN 损失）。解决办法：**梯度裁剪 (Gradient Clipping)** — 将梯度的模控制在阈值以内。
>
> $$ \text{if } \|g\| > \text{threshold: } g \leftarrow \frac{\text{threshold}}{\|g\|} \cdot g $$

**核心洞察：** 梯度消失的根本原因是**连乘结构**。LSTM 的核心贡献就是通过**加性**的细胞状态来替代乘性的梯度传递路径。

---

## 2. LSTM (Long Short-Term Memory)

LSTM 由 Hochreiter & Schmidhuber 于 1997 年提出，后来经过多次改进（尤其是 forget gate 的加入）。它是解决 RNN 梯度消失问题最具影响力的方案。

### 2.1 核心思想：信息高速公路

LSTM 引入了一个新的内部状态——**细胞状态 (Cell State)** $C_t$，作为信息传递的"高速公路"。与 $h_t$ 不同，$C_t$ 上的信息流受到精心设计的**三个门**的调控：

```
                    ┌──────────────────────────────────────┐
                    │           LSTM Cell                   │
                    │                                      │
    h_{t-1} ────────┼─────────────────────────────────┐    │
                    │                ┌─────┐           │    │
                    │    ┌─────┐     │tanh │     ┌───┐ │    │
    x_t ────────────┼────┤σ    │     │    │      │σ  │ │    │
                    │    │     │────▶│    │─────▶│   │─┼────┤───▶ h_t
                    │    │forget     │input│      │output │    │
                    │    └─────┘     │    │      │   │ │    │
                    │                └─────┘      └───┘ │    │
                    │                   │              │ │    │
                    │         ┌─────┐   │              │ │    │
                    │         │ σ   │  │              │ │    │
                    │         │     │──┘              │ │    │
                    │         │input gate             │ │    │
                    │         └─────┘                  │    │
                    │                                  │    │
                    │  C_{t-1} ────────────⊕───────────┘    │
                    │                         │             │
                    │                         └────▶ C_t    │
                    └──────────────────────────────────────┘
```

> **图 5.2:** LSTM 细胞内部结构示意图。三条"门"控制信息的流入、保持和流出。细胞状态 $C_t$ 如同传送带贯穿整个链式结构，只有少量的线性交互。

### 2.2 遗忘门 (Forget Gate)

**功能**：决定从旧细胞状态 $C_{t-1}$ 中丢弃哪些信息。

**为什么需要？** 当网络进入新的上下文时，旧信息可能不再相关。例如在 "她**开始**阅读一本书... 她**合上**了它" 中，"阅读"的动词形态完成后，关于"正在阅读"的信息应该被遗忘门清除。

**公式：**

$$ f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f) $$

其中 $[h_{t-1}, x_t] \in \mathbb{R}^{d_h + d}$ 是将隐藏状态和输入拼接后的向量，$W_f \in \mathbb{R}^{d_h \times (d_h + d)}$。

输出 $f_t \in (0, 1)^{d_h}$ 是一个**逐元素**的掩码 —— 值为 0 表示"完全遗忘"，1 表示"完全保留"。

### 2.3 输入门 (Input Gate)

**功能**：决定在细胞状态中存储哪些新信息。

**为什么需要？** 不是所有的新输入都值得被记住。输入门充当"筛选器"，让重要的新信息进入细胞状态。

输入门由两部分组成：

**a) 输入门控制信号**（决定更新哪些值）：

$$ i_t = \sigma(W_i \cdot [h_{t-1}, x_t] + b_i) $$

**b) 候选细胞状态**（生成新的候选值）：

$$ \tilde{C}_t = \tanh(W_C \cdot [h_{t-1}, x_t] + b_C) $$

这里 $\tanh$ 将候选值压缩到 $(-1, 1)$ 范围，$i_t$ 控制哪些候选值被采纳。

### 2.4 细胞状态更新 (Cell State Update)

**这是 LSTM 中最关键的一步：**

$$ C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t $$

其中 $\odot$ 表示**逐元素乘法 (Hadamard Product)**。

**直观理解**：
- $f_t \odot C_{t-1}$ — 遗忘门决定保留多少旧记忆
- $i_t \odot \tilde{C}_t$ — 输入门决定写入多少新信息
- 两者相加得到新的细胞状态

> **核心洞察**：从 $C_{t-1}$ 到 $C_t$ 的梯度路径是 **加法** 而非乘法。即使遗忘门接近 1，梯度也能完好无损地沿 $C_t$ 路径向后传播。

### 2.5 输出门 (Output Gate)

**功能**：基于细胞状态 $C_t$ 生成当前时间步的隐藏状态 $h_t$（输出给上层和下一时间步）。

**公式：**

$$ o_t = \sigma(W_o \cdot [h_{t-1}, x_t] + b_o) $$

$$ h_t = o_t \odot \tanh(C_t) $$

$\tanh(C_t)$ 将细胞状态压缩到 $(-1, 1)$，$o_t$ 控制输出哪些部分。

### 2.6 为什么 LSTM 能缓解梯度消失？

这是本章最重要的问题之一。让我们比较 RNN 和 LSTM 的梯度路径。

**RNN 的梯度路径（纯乘性）：**

$$ \frac{\partial h_t}{\partial h_{t-1}} = \text{diag}(1 - h_t^2) \cdot W_{hh} $$

这是一个**矩阵乘法**。链式法则使得远距离的梯度趋于 0（或无穷大）。

**LSTM 的梯度路径（加性为主）：**

考虑从 $C_t$ 到 $C_{t-1}$ 的梯度：

$$ C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t $$

$$ \frac{\partial C_t}{\partial C_{t-1}} = \text{diag}(f_t) + \text{(其他项，来自 }i_t, \tilde{C}_t\text{ 对 }C_{t-1}\text{ 的依赖)} $$

**关键观察**：

1. **主导项 $\text{diag}(f_t)$**：细胞状态的梯度通过遗忘门直接向后传递，这是一个**逐元素缩放**而非矩阵乘法。
2. **当 $f_t \approx 1$** 时，梯度项 $\approx 1$，远距离梯度信号几乎无损传递。
3. **加法结构**：$C_t$ 的更新是加法（$C_{t-1} + \Delta$），而非乘法（$W \cdot C_{t-1}$），梯度不会在每一步被压缩。

即使 $f_t$ 变小（忘记旧信息），梯度路径也可以通过输入门 $i_t$ 获得新的通路。

> **简洁表述**：RNN 的误差信号在时间上必须连续穿越 $W_{hh}$ 矩阵（乘性），而 LSTM 的误差信号可以选择一条"高速公路"——通过 $C_t$ 路径的加法捷径，几乎无损地传播到远处。

### 2.7 完整 LSTM 前向传播总结

将以上所有公式汇总：

$$
\begin{aligned}
f_t &= \sigma(W_f \cdot [h_{t-1}, x_t] + b_f) & \text{(遗忘门)} \\
i_t &= \sigma(W_i \cdot [h_{t-1}, x_t] + b_i) & \text{(输入门)} \\
\tilde{C}_t &= \tanh(W_C \cdot [h_{t-1}, x_t] + b_C) & \text{(候选细胞)} \\
C_t &= f_t \odot C_{t-1} + i_t \odot \tilde{C}_t & \text{(细胞状态更新)} \\
o_t &= \sigma(W_o \cdot [h_{t-1}, x_t] + b_o) & \text{(输出门)} \\
h_t &= o_t \odot \tanh(C_t) & \text{(隐藏状态输出)}
\end{aligned}
$$

输入维度：$x_t \in \mathbb{R}^d$，隐藏状态：$h_t \in \mathbb{R}^{d_h}$，细胞状态：$C_t \in \mathbb{R}^{d_h}$。

**参数数量**：LSTM 有 4 组权重矩阵（$W_f, W_i, W_C, W_o$）+ 4 组偏置，每组大小为 $W \in \mathbb{R}^{d_h \times (d_h + d)}$，$b \in \mathbb{R}^{d_h}$。

$$ \text{参数量} = 4 \times \left[ d_h \times (d_h + d) + d_h \right] $$

---

## 3. GRU (Gated Recurrent Unit)

GRU 由 Cho et al. 于 2014 年提出，是 LSTM 的简化变体。

### 3.1 GRU 的设计动机

LSTM 有三个门和一个独立的细胞状态。GRU 观察到：
- 遗忘门和输入门常常是互补的（忘记旧信息 = 留出空间给新信息）
- 细胞状态 $C_t$ 和隐藏状态 $h_t$ 可以合并

于是 GRU 将门减少到两个，合并了细胞状态和隐藏状态。

### 3.2 GRU 公式推导

**重置门 (Reset Gate) $r_t$**：控制忽略过去隐藏状态的程度。

$$ r_t = \sigma(W_r \cdot [h_{t-1}, x_t] + b_r) $$

**更新门 (Update Gate) $z_t$**：控制从过去的隐藏状态中保留多少信息，类似于 LSTM 中遗忘门和输入门的组合。

$$ z_t = \sigma(W_z \cdot [h_{t-1}, x_t] + b_z) $$

**候选隐藏状态**：使用重置门来"重置"旧状态。

$$ \tilde{h}_t = \tanh(W_h \cdot [r_t \odot h_{t-1}, x_t] + b_h) $$

注意这里 $r_t \odot h_{t-1}$ — 当 $r_t$ 接近 0 时，GRU 忽略过去的隐藏状态，就像从头开始。

**最终隐藏状态**：更新门 $z_t$ 在新旧之间做插值。

$$ h_t = (1 - z_t) \odot h_{t-1} + z_t \odot \tilde{h}_t $$

> **直观理解**：这是**可学习的加权平均**。$z_t$ 接近 0 时保留更多旧信息（类似遗忘门 = 1），接近 1 时接受更多新信息（类似遗忘门 = 0，输入门 = 1）。

### 3.3 LSTM vs GRU

| 特性 | LSTM | GRU |
|:---|:---|:---|
| 门数量 | 3 (f, i, o) | 2 (r, z) |
| 内部状态 | 细胞状态 $C_t$ + 隐藏状态 $h_t$ | 只有隐藏状态 $h_t$ |
| 参数量 | $4(d_h(d_h + d) + d_h)$ | $3(d_h(d_h + d) + d_h)$ |
| 表达能力 | 理论上更灵活（独立控制遗忘/写入/输出） | 更简洁，参数量少约 25% |
| 实际表现 | 长序列任务稍优 | 许多任务上与 LSTM 持平 |
| 训练速度 | 稍慢 | 稍快 |

**经验法则**：如果数据量很大，LSTM 的额外参数可能带来精度提升；如果计算资源受限或追求快速迭代，GRU 是不错的选择。

---

## 4. 编码器-解码器架构 (Encoder-Decoder Architecture)

### 4.1 固定维度的上下文向量

编码器-解码器（Encoder-Decoder）架构由 Cho et al. 和 Sutskever et al. 在 2014 年独立提出。也称为 **Seq2Seq (Sequence-to-Sequence)**。

**基本结构**：

```
    编码器 (Encoder)             解码器 (Decoder)

    x_1 → [RNN]                  y_1 → [RNN] → y_1_pred
    x_2 → [RNN]                  y_2 → [RNN] → y_2_pred
    ...          ↘            ↗  ...
    x_T → [RNN] → [context] → [RNN] → y_T_pred
                    ↓
              固定维度向量
           (通常取 h_T 或某种聚合)
```

**流程**：

1. **编码**：将输入序列 $\{x_1, x_2, ..., x_T\}$ 依次送入 RNN 编码器，最终得到上下文向量 $c$：

$$ h_t^{\text{enc}} = \text{RNN}_{\text{enc}}(h_{t-1}^{\text{enc}}, x_t) \quad, \quad c = h_T^{\text{enc}} $$

2. **解码**：基于上下文向量 $c$ 和已生成的输出，逐个时间步生成目标序列 $\{y_1, y_2, ..., y_{T'}\}$：

$$ h_t^{\text{dec}} = \text{RNN}_{\text{dec}}(h_{t-1}^{\text{dec}}, [y_{t-1}, c]) $$

$$ y_t^{\text{pred}} = \text{softmax}(W_y h_t^{\text{dec}} + b_y) $$

### 4.2 编码器-解码器的信息瓶颈

**核心问题**：无论输入序列多长，编码器必须将全部信息压缩到一个**固定维度的向量 $c$** 中。

这个 $c$ 的维度 $d_h$ 通常远小于输入序列包含的信息量（比如 $d_h = 256$ 却要编码包含几十个词的句子）。这造成了**严重的信息瓶颈**：

- 对于短句（如 "Hello world"），256 维向量可能够用
- 对于长句（如 "The man who gave a speech about... yesterday finally..."），256 维向量几乎不可能保留所有细节
- 解码器在每个时间步都**看到同一个 $c$**，没有机制去"关注"输入序列特定位置的信息

**直觉类比**：这就像你闭着眼睛听别人复述整篇论文的内容摘要，然后要求你逐字写出全文——摘要中丢失的细节无法被恢复。

---

## 5. 为什么需要 Attention？

### 5.1 从瓶颈到查阅

Attention 机制的核心思想非常直观：

> **在解码的每一步，不依赖单一的上下文向量，而是"查阅"编码器的所有隐藏状态，动态选择相关信息。**

### 5.2 Attention 的直觉

让我们用类比来理解（不涉及 Attention 的具体计算——那将在 Vol 5 第 1 章展开）：

**无 Attention（RNN Encoder-Decoder）**: 

> 你参观一座博物馆，在入口处被迫写下一段描述整座博物馆的文字，然后进入各个展厅时只能依靠这段文字来回忆展品。显然，你不可能在入口描述所有细节。

**有 Attention**:

> 在每一个展厅，你直接看向当前展品，并翻阅之前写下的笔记，找到与当前展品最相关的记录。你本质上是在**有选择地查阅**所有信息源。

**核心列表对比：**

| 特性 | RNN (无 Attention) | Transformer (有 Attention) |
|:---|:---|:---|
| 信息传递 | 通过固定向量 $c$ 传递整个序列 | 动态选择相关位置的信息 |
| 长程依赖 | 困难（梯度消失） | 直连（任意两个位置步长 = 1） |
| 并行化 | 必须串行（后一步依赖前一步的 $h_t$） | 可以完全并行 |
| 瓶颈 | 上下文向量维度固定 | 无信息瓶颈 |

**Attention 的完整公式将在《第 6 卷 Transformer》第 1 章中给出。** 本章的 core 结论是：**RNN 的循环结构（串行、乘性梯度路径、固定上下文向量）是其所有固有局限的根源，而 Attention 正是针对这些局限的直接回应。**

---

## 6. 小结 (Summary)

1. **RNN** 通过隐藏状态 $h_t = \tanh(W_{hh} h_{t-1} + W_{xh} x_t + b_h)$ 实现序列建模，但 BPTT 的连乘梯度路径导致梯度消失/爆炸。

2. **LSTM** 引入细胞状态 $C_t$ 和三个门（遗忘、输入、输出），通过**加法梯度路径**使梯度能无损传播到远处，有效缓解了梯度消失。

3. **GRU** 是 LSTM 的简化变体，将门减为 2 个（更新门、重置门），合并了细胞状态和隐藏状态，参数量减少约 25%。

4. **编码器-解码器**架构将变长序列压缩到固定维度的上下文向量，存在严重的信息瓶颈。

5. **RNN 的局限**（串行计算、梯度消失、信息瓶颈）是通往 **Attention 机制**的直接动机——Attention 将在 Transformer 架构中彻底替代循环结构。

---

**进一步阅读 (Further Reading):**
- Hochreiter & Schmidhuber (1997). "Long Short-Term Memory." *Neural Computation*. — LSTM 原始论文
- Cho et al. (2014). "Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation." — GRU 与 Seq2Seq
- Sutskever, Vinyals & Le (2014). "Sequence to Sequence Learning with Neural Networks." — Seq2Seq 经典
- Bengio, Simard & Frasconi (1994). "Learning long-term dependencies with gradient descent is difficult." — 梯度消失的理论分析
- Olah (2015). "Understanding LSTM Networks." — 可视化 LSTM 的优秀博文

## 参考文献 (References)

1. **Hochreiter, S. & Schmidhuber, J.** (1997). Long Short-Term Memory. *Neural Computation*, 9(8), 1735–1780.
2. **Cho, K. et al.** (2014). Learning phrase representations using RNN encoder-decoder. *EMNLP*.
3. **Sutskever, I., Vinyals, O. & Le, Q. V.** (2014). Sequence to sequence learning with neural networks. *NeurIPS*.
