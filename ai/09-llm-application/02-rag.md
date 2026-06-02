# 第2章 RAG — 检索增强生成
# Chapter 2: Retrieval-Augmented Generation

> **RAG (Retrieval-Augmented Generation) is a paradigm that equips LLMs with external knowledge by combining a retrieval system with a generative model.** Instead of relying solely on parametric memory, RAG fetches relevant documents from a knowledge base at inference time and conditions the generation on them. This chapter covers the standard RAG pipeline, text chunking strategies, vector databases, and advanced variants like HyDE, RAPTOR, and Self-RAG.
>
> **RAG（检索增强生成）是一种通过将检索系统与生成模型相结合，为 LLM 配备外部知识的范式。** RAG 不依赖纯参数化记忆，而是在推理时从知识库中检索相关文档，并基于这些文档进行生成。本章涵盖标准 RAG 流程、文本分割策略、向量数据库以及 HyDE、RAPTOR、Self-RAG 等高级变体。

**前置知识 (Prerequisites):** 了解 Transformer 和 LLM 基本原理
**依赖库 (Dependencies):** `langchain`, `chromadb`, `sentence-transformers`, `faiss-cpu` (code)
**配套代码 (Code):** 本章无独立代码文件

---

## 目录 (Table of Contents)

1. [为什么需要 RAG (Why RAG)](#1-为什么需要-rag-why-rag)
2. [RAG 三件套 (The RAG Triad)](#2-rag-三件套-the-rag-triad)
3. [文本分割 (Text Chunking)](#3-文本分割-text-chunking)
4. [向量数据库 (Vector Databases)](#4-向量数据库-vector-databases)
5. [高级 RAG 技术 (Advanced RAG Techniques)](#5-高级-rag-技术-advanced-rag-techniques)

---

## 1. 为什么需要 RAG (Why RAG)

### 1.1 LLM 的固有局限 (Inherent Limitations of LLMs)

大语言模型虽强大，但存在三个根本性缺陷：

| 缺陷 (Limitation) | 表现 (Manifestation) | 后果 (Consequence) |
|---|---|---|
| **知识截止 (Knowledge Cutoff)** | 模型只记住训练截止前的知识 | 无法回答最新事件、新产品、新法规 |
| **幻觉 (Hallucination)** | 模型编造看似合理但错误的信息 | 降低可信度，在生产环境中不可接受 |
| **私有数据 (Private Data)** | 模型未见过企业内部数据 | 无法处理公司文档、用户个性化数据 |

### 1.2 RAG 的解决思路 (The RAG Solution)

RAG 的核心思想是：**不让模型凭记忆回答，而是先查资料，再作答。**

```
Query ──► Retriever ──► [Doc₁, Doc₂, ..., Docₖ]
                              │
                              ▼
                     ┌──────────────────┐
                     │  Augmented Prompt │
                     │                   │
                     │  Context: Doc₁... │
                     │  Question: Query  │
                     └──────────────────┘
                              │
                              ▼
                        Generator (LLM)
                              │
                              ▼
                          Answer
```

**LLM 负责"阅读理解"而非"记忆回忆"** — 这一思路将外部知识库与生成模型解耦，使两者可以独立更新。

---

## 2. RAG 三件套 (The RAG Triad)

标准 RAG 管道由三个核心组件构成：**索引 (Index) → 检索 (Retrieve) → 生成 (Generate)**。

### 2.1 索引 (Indexing)

将原始文档转化为可检索的向量索引：

```
Raw Documents
      ↓  Split (Chunking)
Text Chunks
      ↓  Embed (Text → Vector)
Vector Embeddings
      ↓  Store
Vector Database
```

**核心公式 (Core Formula):** 嵌入函数 $f: \text{text} \rightarrow \mathbb{R}^d$ 将文本映射到 $d$ 维向量空间。每个文档块 $c_i$ 被映射为向量 $\mathbf{v}_i = f(c_i)$。

### 2.2 检索 (Retrieval)

给定查询 $q$，同样计算其嵌入 $\mathbf{v}_q = f(q)$，然后在向量空间中搜索最近邻：

$$
\text{Retrieve}(q) = \text{top-}k \text{ argmin}_{c_i} \| \mathbf{v}_q - \mathbf{v}_i \|_2
$$

或使用余弦相似度 (cosine similarity)：

$$
\text{sim}(q, c_i) = \frac{\mathbf{v}_q \cdot \mathbf{v}_i}{\|\mathbf{v}_q\| \|\mathbf{v}_i\|}
$$

| 相似度度量 (Similarity) | 公式 (Formula) | 特点 |
|---|---|---|
| 余弦相似度 | $\frac{\mathbf{a} \cdot \mathbf{b}}{\|\mathbf{a}\| \|\mathbf{b}\|}$ | 对向量长度不敏感，最常用 |
| 欧氏距离 | $\|\mathbf{a} - \mathbf{b}\|_2$ | 对向量长度敏感 |
| 内积 | $\mathbf{a} \cdot \mathbf{b}$ | 需要归一化后使用 |

**Top-k 的选择 (Choice of k):** $k$ 通常在 3–10 之间。$k$ 过小可能遗漏相关信息，$k$ 过大则引入噪声并消耗更多 LLM 上下文窗口。

### 2.3 生成 (Generation)

将检索到的文档块拼接到 prompt 中，让 LLM 基于上下文生成：

```
System: Answer the question based solely on the provided context.
If the context does not contain the answer, say "I don't know."

Context:
[1] {doc_1}
[2] {doc_2}
...
[k] {doc_k}

Question: {user_query}
Answer:
```

**增强 prompt 的数学描述 (Augmented Prompt Formally):**

$$
P(\text{answer} | q, D) = \prod_{t} P_{\text{LLM}}(y_t | y_{<t}, \text{concat}([C], q))
$$

其中 $C = \text{concat}(c_1, c_2, \ldots, c_k)$ 为检索到的上下文，$q$ 为原始查询。

---

## 3. 文本分割 (Text Chunking)

文本分割是将原始文档切分为适合检索的块。这是 RAG 系统中**最容易被忽视但影响最大的超参数**。

### 3.1 固定大小分割 (Fixed-Size Chunking)

最简单的策略：按固定字符数切分，通常加一定重叠 (overlap) 避免切在关键位置。

```
Text: "RAG is a powerful technique for ..."
                      ↓  chunk_size=50, overlap=10
Chunk 1: "RAG is a powerful technique for [10 chars overlap]"
Chunk 2: "[10 chars overlap] improving LLM accuracy and ..."
```

**超参数影响 (Hyperparameter Impact):**

| 参数 (Parameter) | 过小 (Too Small) | 过大 (Too Large) |
|---|---|---|
| **chunk_size** | 上下文碎片化，丢失语义 | 检索精度下降，浪费 LLM 上下文 |
| **overlap** | 切分点附近的语义断裂 | 重复内容增多，边际收益递减 |

### 3.2 递归分割 (Recursive Chunking)

按语义边界（段落 → 句子 → 短语）逐步切割，比固定大小更尊重文本结构。

```
Document
    ↓  Split by "\n\n" (paragraph boundaries)
Paragraphs
    ↓  If too long, split by "\n" (line breaks)
Line groups
    ↓  If still too long, split by ". " (sentence boundaries)
Sentences
    ↓  If still too long, split by ", " (clause boundaries)
Clauses
```

**LangChain 的 `RecursiveCharacterTextSplitter` 是这一方法的典型实现。**

### 3.3 语义分割 (Semantic Chunking)

利用嵌入向量的相似度变化来检测语义边界。当两个连续句子之间的嵌入距离超过阈值时，认为存在语义断层。

```
Sentence 1: Embed → v₁
Sentence 2: Embed → v₂
              │
              ▼
        cos(v₁, v₂) < θ ?
              │
        ┌─────┴─────┐
       Yes          No
        │            │
    New chunk    Continue chunk
```

**优点 (Advantages):** 块边界与语义边界对齐，检索质量最高。
**缺点 (Disadvantages):** 需要额外嵌入计算，延迟与成本更高。

### 3.4 经验准则 (Empirical Guidelines)

| 数据类型 (Data Type) | 推荐策略 (Strategy) | 典型大小 (Typical Size) |
|---|---|---|
| 新闻文章 | 递归分割 (段落) | 256–512 tokens |
| PDF 论文 | 按章节分割 | 512–1024 tokens |
| 代码文件 | 按函数/类分割 | 200–500 tokens |
| 对话记录 | 按轮次分割 | 128–256 tokens |
| 技术文档 | 按标题结构分割 | 256–512 tokens |

---

## 4. 向量数据库 (Vector Databases)

向量数据库专门处理高维向量的存储和近似最近邻 (ANN) 搜索。

### 4.1 核心能力 (Core Capabilities)

1. **向量索引** — 构建 ANN 索引结构（HNSW, IVF, PQ）
2. **相似度搜索** — 支持余弦、欧氏、内积等度量
3. **元数据过滤** — 结合结构化查询（如 `WHERE date > 2024-01-01`）
4. **混合搜索** — 向量相似度 + 关键词 BM25 加权

### 4.2 主流产品对比 (Comparison)

| 特性 (Feature) | Chroma | Pinecone | Qdrant | Weaviate |
|---|---|---|---|---|
| **部署方式** | 嵌入式 / 本地 | 云托管 | 自托管 / 云 | 自托管 / 云 |
| **开源** | ✅ Apache 2.0 | ❌ 闭源 | ✅ Apache 2.0 | ✅ BSD-3 |
| **索引算法** | HNSW | HNSW | HNSW + IQR | HNSW |
| **元数据过滤** | 有限 | ✅ 丰富 | ✅ 丰富 | ✅ 丰富 |
| **混合搜索** | ❌ | ✅ | ✅ | ✅ |
| **多租户** | ❌ | ✅ | ✅ | ✅ |
| **适用场景** | 个人/小项目 | 生产级免运维 | 高性能生产 | 企业级方案 |

**选择建议 (Selection Guide):**

- **快速原型** → Chroma（零配置，pip install 即用）
- **托管生产** → Pinecone（零运维，SLA 保证）
- **自建高性能** → Qdrant（Rust 实现，低延迟）
- **企业全栈** → Weaviate（内置 GraphQL 和推理）

### 4.3 近似最近邻搜索 (ANN Search)

暴力搜索 $O(n \cdot d)$ 在大规模数据上不可行。ANN 通过牺牲少量精度换取数量级的速度提升。

**HNSW (Hierarchical Navigable Small World)** 是当前最主流的 ANN 算法：

```
Layer 3: sparse graph (long-range connections)
Layer 2: medium graph
Layer 1: dense graph (short-range connections)

Search starts at top layer, descends greedily.
```

| 算法 (Algorithm) | 搜索速度 | 索引构建 | 内存占用 | 精度 |
|---|---|---|---|---|
| HNSW | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| IVF (倒排文件) | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| PQ (乘积量化) | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐ |
| DiskANN | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |

---

## 5. 高级 RAG 技术 (Advanced RAG Techniques)

标准 RAG 在简单场景下效果不错，但在复杂查询、多跳推理、噪声鲁棒性等方面存在不足。以下三种技术从不同角度解决了这些问题。

### 5.1 HyDE (Hypothetical Document Embeddings)

**核心思想 (Core Idea):** 查询有时与文档不在同一语义空间。HyDE 先生成一个"假设文档"（即理想的答案），然后用这个假设文档去检索真实文档。

```
Query: "How to treat migraine?"
         │
         ▼
  LLM generates hypothetical answer:
  "Migraine treatment includes NSAIDs, triptans, and lifestyle changes..."
         │
         ▼
  Embed(hypothetical_answer) → search vectorDB
         │
         ▼
  Retrieve real documents about migraine treatments
```

**优势 (Advantage):** 查询 → 假设文档的转换弥合了查询与文档之间的语义鸿沟 (semantic gap)。

**局限性 (Limitation):** 假设文档如果偏离真实答案，反而会引入噪声。

### 5.2 RAPTOR (Recursive Abstractive Processing for Tree-Organized Retrieval)

**核心思想 (Core Idea):** 将文档集构建为**多层树结构**，在检索时根据查询的粒度选择不同层级的节点。

```
                    ┌─────────────────┐
                    │  Root Summary    │  ← Level 3 (highest abstraction)
                    │  "Overall theme" │
                    └────────┬────────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
     ┌────────┴──────┐ ┌───┴───────┐ ┌───┴────────┐
     │ Cluster 1     │ │ Cluster 2 │ │ Cluster 3  │  ← Level 2
     │ "Subtopic A"  │ │ "Subtopic B"││ "Subtopic C"│
     └────────┬──────┘ └───┬───────┘ └───┬────────┘
              │            │             │
     ┌────────┴─┐  ┌──────┴───┐  ┌──────┴───┐
     │ Doc₁ Doc₂│  │ Doc₃ Doc₄│  │ Doc₅ Doc₆│  ← Level 1 (raw chunks)
     └──────────┘  └──────────┘  └──────────┘
```

**对比标准 RAG (vs. Standard RAG):**

| 维度 | 标准 RAG | RAPTOR |
|---|---|---|
| 检索粒度 | 固定大小的块 | 多层抽象，自适应选择 |
| 跨文档推理 | 弱 | 强（通过摘要节点） |
| 计算成本 | 低 | 较高（需多级摘要） |
| 适用场景 | 事实型问答 | 综述型、分析型问答 |

**RAPTOR 的数学直觉 (Mathematical Intuition):**

给定文档集 $\mathcal{D}$，RAPTOR 递归地进行聚类和摘要：

$$
\begin{aligned}
L_1 &= \{c_1, c_2, \ldots, c_n\} \quad \text{(原始块)} \\
L_2 &= \text{Summarize}(\text{Cluster}(L_1)) \\
L_3 &= \text{Summarize}(\text{Cluster}(L_2)) \\
&\vdots
\end{aligned}
$$

检索时，在树的所有层级进行搜索，并将相关性得分最高的节点返回给 LLM。

### 5.3 Self-RAG

**核心思想 (Core Idea):** 让 LLM 自主决定"是否需要检索"以及"检索结果是否可信"，引入反思 (reflection) 机制。

```
Query
  │
  ├── Step 1: Should I retrieve? (IS_RETRIEVE)
  │        │
  │     Yes/No
  │        │
  ├── Step 2: If Yes → retrieve chunks
  │        │
  │        ▼
  │   For each chunk, check: IS_RELEVANT?
  │        │
  │        ▼
  ├── Step 3: Generate response from relevant chunks
  │        │
  │        ▼
  └── Step 4: Verify response (IS_SUPPORTED?)
```

**Self-RAG 的特殊 Token (Special Tokens):**

| Token | 功能 (Function) | 取值 |
|---|---|---|
| `IS_RETRIEVE` | 判断是否需要检索 | `{Continue, NoRetrieve}` |
| `IS_RELEVANT` | 判断块是否相关 | `{Relevant, Irrelevant}` |
| `IS_SUPPORTED` | 判断生成是否被支持 | `{Fully, Partially, NoSupport}` |

**为什么 Self-RAG 重要？** 标准 RAG 的检索是"盲目的"——即使模型已经知道答案，仍然会触发检索，增加延迟和成本。Self-RAG 让模型学会了"知道何时知道，知道何时不知道"。

### 5.4 三种技术的对比与选择 (Comparison)

| 技术 (Technique) | 解决的问题 | 代价 |
|---|---|---|
| **HyDE** | 查询-文档语义鸿沟 | 多一次 LLM 调用 |
| **RAPTOR** | 跨文档、多跳推理 | 建树成本高 |
| **Self-RAG** | 盲目检索、不信任检索结果 | 需微调特殊 token |

**组合使用 (Combination):** 这三种技术不是互斥的。实际系统中常将多个技术组合使用，例如"HyDE 做检索增强 + RAPTOR 做多层级索引 + Self-RAG 做反思验证"。

---

## 总结 (Summary)

| 组件 (Component) | 关键技术 (Key Techniques) |
|---|---|
| **Indexing** | 递归块分割、语义块分割 |
| **Embedding** | `sentence-transformers`, `text-embedding-3-small` |
| **Vector DB** | Chroma (快速原型), Pinecone/Qdrant (生产) |
| **Retrieval** | ANN 搜索 (HNSW), 混合搜索 (向量 + BM25) |
| **Generation** | 上下文增强 prompt |
| **Advanced** | HyDE, RAPTOR, Self-RAG |

**核心原则 (Core Principles):**
1. **垃圾进垃圾出** — 文档质量 > 检索算法 > 生成模型
2. **块大小是关键超参数** — 根据文档类型和任务调整
3. **检索不是越多越好** — top-k 的 $k$ 和 LLM 上下文窗口需要平衡
4. **监控检索质量** — 低检索精度会直接"毒化"生成结果

---

**参考资源 (References):**
- Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (NeurIPS 2020)
- Gao et al., "Precise Zero-Shot Dense Retrieval without Relevance Labels" (HyDE, ACL 2023)
- Sarthi et al., "RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval" (2024)
- Asai et al., "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection" (ICLR 2024)
- Malkov & Yashunin, "Efficient and Robust Approximate Nearest Neighbor Search using Hierarchical Navigable Small World Graphs" (TPAMI 2020)
