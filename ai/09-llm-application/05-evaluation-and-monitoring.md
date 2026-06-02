# 9.5 评估与监控 — LLM 效果衡量与持续改进
# 9.5 Evaluation & Monitoring — Measuring LLM Quality & Continuous Improvement

> **"You can't improve what you don't measure." If you deploy an LLM without evaluation, you are flying blind.**
>
> **「无法衡量就无法改进。」如果未经评估就部署 LLM，等于在盲飞。**

---

**前置知识 (Prerequisites):** 第 9.1-9.4 节, 基础 NLP 知识 (BLEU, ROUGE, BERTScore 概念)
**依赖库 (Dependencies):** `transformers`, `numpy`, `nltk`
**配套代码 (Code):** `code/evaluation_pipeline.py`

---

## 目录 (Table of Contents)

1. [评估指标 (Evaluation Metrics)](#1-评估指标-evaluation-metrics)
2. [评估数据集 (Evaluation Datasets)](#2-评估数据集-evaluation-datasets)
3. [LLM-as-Judge ⭐](#3-llm-as-judge)
4. [LangSmith / LangFuse 监控 (Monitoring)](#4-langsmith--langfuse-监控-monitoring)

---

## 1. 评估指标 (Evaluation Metrics)

LLM 评估需要从多个维度衡量输出质量，没有一个指标能覆盖所有场景。

| 维度 (Dimension) | 指标 (Metric) | 衡量什么 (What it measures) | 适用场景 (Use case) |
|---|---|---|---|
| **Accuracy** | Exact Match, F1 | 输出与参考答案的精确匹配程度 | QA, 分类, 信息抽取 |
| **Relevance** | BERTScore, ROUGE | 输出内容与输入的语义相关性 | 摘要, 对话, 翻译 |
| **Safety** | Toxicity, Bias | 输出是否包含有害/偏见内容 | 任何面向用户的场景 |
| **Hallucination** | Factual Consistency | 输出是否与已知事实一致 | RAG, 知识问答 |
| **Task-specific** | BLEU, CodeBLEU, PASS@K | 领域特定质量 | 翻译, 代码生成 |

### 1.1 准确性指标 (Accuracy Metrics)

**Exact Match (EM):** 输出与参考答案完全一致的比例。严格但过于苛刻。

$$
\text{EM} = \frac{\text{完全匹配的样本数}}{\text{总样本数}}
$$

**F1 Score:** 基于 token 级别计算精确率与召回率的调和平均，比 EM 更宽容。

$$
F1 = 2 \times \frac{Precision \times Recall}{Precision + Recall}
$$

其中 Precision = 预测正确的 token 数 / 预测总 token 数，Recall = 预测正确的 token 数 / 参考答案总 token 数。

### 1.2 相关性指标 (Relevance Metrics)

**ROUGE (Recall-Oriented Understudy for Gisting Evaluation):** 衡量生成文本与参考文本的 n-gram 重叠。常用于摘要评估。

| 变体 (Variant) | 含义 (Meaning) | 说明 (Note) |
|---|---|---|
| ROUGE-1 | unigram 召回率 | 单词重叠 |
| ROUGE-2 | bigram 召回率 | 词组重叠 |
| ROUGE-L | 最长公共子序列 | 结构相似度 |

**BERTScore:** 利用 BERT 语义嵌入计算生成文本与参考文本的余弦相似度，比 n-gram 方法更好地捕捉语义相似性。

```
BERTScore(P_i, R_j) = cosine(BERT(P_i), BERT(R_j))
```

> BERTScore 与人类判断的相关性 (约 0.85) 显著高于 ROUGE (约 0.65)。

### 1.3 安全指标 (Safety Metrics)

**Toxicity Scoring:** 使用预训练的毒性检测模型 (如 Detoxify) 评估输出毒性等级。

**Bias Detection:** 检测输出中是否存在性别、种族、地域等偏见。

**Perturbation Robustness:** 对输入进行微小扰动（同义词替换、错别字），观察输出稳定性。

### 1.4 幻觉检测 (Hallucination Detection)

**Factual Consistency:** 使用 NLI (自然语言推理) 模型判断输出是否被上下文"蕴涵"。

```
如果 上下文 ⊨ 输出 → 一致 (faithful)
如果 上下文 ⊭ 输出 → 幻觉 (hallucination)
```

**SelfCheckGPT** 是一种不需要参考答案的幻觉检测方法：对同一输入采样多个输出，通过一致性判断幻觉。

---

## 2. 评估数据集 (Evaluation Datasets)

### 2.1 Golden Dataset 黄金数据集

黄金数据集是人工标注的高质量测试集，包含 `(input, expected_output)` 对。

```
{
  "qa_pair": {
    "input": "What is the capital of France?",
    "expected_output": "Paris",
    "difficulty": "easy",
    "category": "geography"
  },
  "summarization": {
    "input": "长篇文档内容...",
    "expected_output": "简洁摘要...",
    "difficulty": "hard",
    "category": "news"
  }
}
```

### 2.2 数据集设计原则 (Design Principles)

| 原则 (Principle) | 说明 (Description) |
|---|---|
| **Coverage** | 覆盖所有关键场景 (正常、边界、异常) |
| **Adversarial** | 包含对抗性测试用例 (误导性输入、越狱尝试) |
| **Balance** | 各类别样本数量均衡 |
| **Size** | 100-500 样本通常足以获得可靠指标 |
| **Freshness** | 定期更新防止过拟合 |

### 2.3 数据来源 (Data Sources)

| 来源 (Source) | 优点 (Pros) | 缺点 (Cons) |
|---|---|---|
| **Human-annotated** | 质量最高 | 成本高, 速度慢 |
| **LLM-generated** | 成本低, 速度快 | 可能出现错误, 需要验证 |
| **User feedback** | 真实分布 | 噪音大, 隐私问题 |
| **Synthetic** | 可定制, 覆盖边界 | 可能偏离真实分布 |

> **最佳实践:** 先用 LLM 生成候选数据集，再由人工抽检和修正。Human-in-the-loop 是质量保障的关键。

---

## 3. LLM-as-Judge ⭐

### 3.1 核心思想 (Core Idea)

**用强 LLM (如 GPT-4, Claude) 评估弱 LLM 的输出。** 研究表明，LLM-as-Judge 与人类评估者的相关性可达 0.8 左右。

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Student LLM │────▶│   Response   │────▶│  Judge LLM  │
│  (被评估者)  │     │   (输出)     │     │  (评估者)   │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                 │
                    ┌────────────────────────────┘
                    ▼
          ┌─────────────────────┐
          │  Score + Explanation │
          │  评分 + 详细理由     │
          └─────────────────────┘
```

### 3.2 评估 Prompt (Evaluation Prompt)

```
System: You are an expert evaluator. Rate the following answer on a scale of 1-5
        for each dimension. Provide a brief explanation for each score.

Dimensions:
- Accuracy (1-5): Is the answer factually correct?
- Relevance (1-5): Does the answer address the question?
- Completeness (1-5): Does the answer cover all aspects?
- Clarity (1-5): Is the answer clear and well-structured?

User Question: {input}
Model Answer: {output}

Output JSON format:
{
  "accuracy": {"score": 5, "reason": "..."},
  "relevance": {"score": 4, "reason": "..."},
  ...
}
```

### 3.3 评估协议的几种变体 (Variants)

| 方法 (Method) | 描述 (Description) | 适用场景 |
|---|---|---|
| **Single-judge** | 一个 LLM 评估所有维度 | 快速评估, 内部迭代 |
| **Multi-judge** | 多个 LLM 分别评估取平均 | 减少偏差, 提高稳健性 |
| **Pairwise comparison** | 比较两个 LLM 的输出哪个更好 | 模型选型 A/B 测试 |
| **Rubric-based** | 按评分规则逐项打分 | 需要结构化反馈 |
| **Reference-based** | 与参考答案对比评分 | 有黄金数据集时 |

### 3.4 局限性 (Limitations)

- **Position bias:** LLM 倾向于选择列表中的第一个或最后一个回答
- **Self-enhancement bias:** LLM 偏好自己的输出风格
- **Verbosity bias:** 更长的输出往往获得更高评分
- **Calibration:** LLM 的评分绝对值可能不可靠，但相对排序往往有效

> **缓解策略:** 交换选项顺序取平均、使用多 judge 投票、校准到人类评分。

---

## 4. LangSmith / LangFuse 监控 (Monitoring)

### 4.1 为什么需要监控平台 (Why Monitoring?)

| 生产环境需求 (Production Need) | LangSmith / LangFuse 提供的功能 |
|---|---|
| 追踪每次 LLM 调用链路 | **Tracing** — 完整调用链可视化 |
| 比较不同实验版本 | **Comparison** — Run 级别对比 |
| 管理评估数据集 | **Dataset Management** — 版本化数据集 |
| 线上实时监控告警 | **Monitoring** — 延迟/Token/错误率看板 |
| Prompt 版本管理 | **Prompt Management** — 版本化/回滚 |

### 4.2 LangSmith

由 LangChain 团队开发的 LLM 应用可观测性平台。

**核心功能:**

```
┌─────────────────────────────────────────────┐
│                LangSmith                      │
│                                               │
│  ┌─────────┐  ┌─────────┐  ┌──────────────┐  │
│  │ Tracing │  │  Hub    │  │  Evaluation   │  │
│  │ (追踪)  │  │ (Prompt │  │  (评估)      │  │
│  │         │  │  仓库)  │  │              │  │
│  └─────────┘  └─────────┘  └──────────────┘  │
│                                               │
│  ┌─────────┐  ┌─────────┐  ┌──────────────┐  │
│  │ Datasets│  │ Monitor │  │  Annotation   │  │
│  │ (数据集)│  │ (监控)  │  │  (标注)      │  │
│  └─────────┘  └─────────┘  └──────────────┘  │
└─────────────────────────────────────────────┘
```

**典型集成代码:**

```python
from langsmith import Client
from langsmith.run_helpers import traceable

client = Client()

@traceable(project_name="my-llm-app")
def my_llm_call(input_text: str) -> str:
    # 你的 LLM 调用
    return response

# 记录评估结果
client.create_feedback(
    run_id=run_id,
    key="accuracy",
    score=0.95,
)
```

### 4.3 LangFuse

开源 LLM 可观测性平台，是 LangSmith 的自托管替代方案。

**核心功能对比:**

| 特性 (Feature) | LangSmith | LangFuse |
|---|---|---|
| 开源 | ❌ 闭源 SaaS | ✅ 开源 (MIT) |
| 自托管 | ❌ | ✅ |
| Prompt 管理 | ✅ LangSmith Hub | ✅ |
| 数据集管理 | ✅ | ✅ |
| 在线评估 | ✅ | ✅ |
| 成本控制 | ✅ Token 用量统计 | ✅ |
| Python SDK | ✅ | ✅ `langfuse` |

**典型集成代码:**

```python
from langfuse import Langfuse

langfuse = Langfuse(
    secret_key="sk-lf-...",
    public_key="pk-lf-..."
)

# 创建追踪
trace = langfuse.trace(name="my-llm-app")

# 记录 LLM 调用
span = trace.span(
    name="llm-call",
    input={"question": user_input},
    output={"response": llm_response},
    metadata={"model": "gpt-4", "temperature": 0.7}
)

# 记录评估分数
langfuse.score(
    trace_id=trace.id,
    name="accuracy",
    value=0.95
)
```

### 4.4 关键监控指标 (Key Monitoring Metrics)

| 指标 (Metric) | 含义 (Meaning) | 告警阈值 (Alert Threshold) |
|---|---|---|
| **Latency P95** | 95% 请求在 X 毫秒内完成 | > 5000ms |
| **Token Usage** | 输入/输出 token 数统计 | 异常突增 200% |
| **Error Rate** | LLM 调用失败率 | > 5% |
| **Cost per Call** | 每次调用的 API 成本 | 超预算 |
| **User Feedback** | 用户点赞/点踩率 | 点赞率 < 80% |
| **Drift Detection** | 输出分布变化检测 | 分布显著偏移 |

### 4.5 评估与监控工作流 (Workflow)

```
开发阶段 (Development)             生产阶段 (Production)
┌─────────────────┐               ┌─────────────────────┐
│  Golden Dataset  │               │   Online Tracing     │
│  黄金数据集      │               │   在线追踪          │
└────────┬────────┘               └──────────┬──────────┘
         │                                     │
         ▼                                     ▼
┌─────────────────┐               ┌─────────────────────┐
│  Offline Eval   │               │   Feedback Loop     │
│  离线评估        │──────────────▶│   反馈闭环          │
│  (Pre-deploy)   │               │   (User Feedback)   │
└────────┬────────┘               └──────────┬──────────┘
         │                                     │
         ▼                                     ▼
┌─────────────────┐               ┌─────────────────────┐
│  Regression     │               │   Alert & Retrain   │
│  回归测试        │               │   告警与重训练      │
└─────────────────┘               └─────────────────────┘
```

> **一句话总结:** 离线评估保下限，在线监控保上线，反馈闭环促改进。

---

## 总结 (Summary)

| 概念 (Concept) | 关键要点 (Key Takeaway) |
|---|---|
| **评估指标** | 多维度衡量：Accuracy + Relevance + Safety + Hallucination |
| **评估数据集** | 黄金数据集 100-500 样本，Human + LLM 联合构建 |
| **LLM-as-Judge** | 强 LLM 评估弱 LLM，相关性 ~0.8，注意 Position Bias |
| **监控平台** | LangSmith (SaaS) vs LangFuse (开源)，Tracing + Eval + Monitor 三位一体 |
| **最佳实践** | 离线评估 + 在线监控 + 反馈闭环 = 持续改进 |

> **记住:** 评估是 LLM 工程中最容易被忽视但最重要的环节。没有评估的部署是对用户的不负责任。
>
> **Remember:** Evaluation is the most overlooked yet most critical part of LLM engineering. Deploying without evaluation is irresponsible to your users.
