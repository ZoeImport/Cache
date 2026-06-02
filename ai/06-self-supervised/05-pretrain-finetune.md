# 05 — Pretrain-Finetune Workflow 预训练-微调工作流

> **Code**: `code/05-pretrain-finetune.py`

## Overview 概述

**Transfer learning via pretrain-finetune** is the dominant paradigm in modern NLP/CV:
> **预训练-微调范式**是现代 NLP 和计算机视觉的主流方法。

```
┌──────────────────────────────────────────────────────────┐
│                 Pretrain-Finetune Pipeline                │
├──────────────────────────────────────────────────────────┤
│  ① Pretrained Model (distilBERT)                         │
│     ├── Self-supervised on massive corpus (Wikipedia)    │
│     └── General language understanding                    │
│                                                          │
│  ② Add Task-Specific Head                                │
│     ├── Classification head (random init)                │
│     └── Replaces the original pretraining head           │
│                                                          │
│  ③ Finetune on Downstream Task                           │
│     ├── IMDB sentiment (or your custom data)             │
│     ├── Small learning rate (2e-5)                       │
│     └── Few epochs (1-5)                                 │
│                                                          │
│  ④ Evaluate & Deploy                                     │
│     ├── Accuracy, F1, Precision, Recall                  │
│     └── Inference pipeline                               │
└──────────────────────────────────────────────────────────┘
```

### Why It Works 为什么有效

| Concept 概念 | Explanation 解释 |
|---|---|
| **Transfer Learning 迁移学习** | Knowledge from pretraining transfers to the new task 预训练学到的通用知识迁移到新任务 |
| **Task Adaptation 任务适配** | Only the head needs to learn task-specific patterns 仅分类头需要学习任务特定模式 |
| **Catastrophic Forgetting 灾难性遗忘** | Low LR + few epochs preserve pretrained knowledge 小学习率+少epoch保留预训练知识 |

---

## Step-by-Step Code Walkthrough 代码逐行讲解

### Step 1: Load Dataset 加载数据集

```python
from datasets import load_dataset

dataset = load_dataset("stanfordnlp/imdb", "plain_text")
```

- Loads 25k train + 25k test IMDB reviews (balanced binary sentiment)
- We take a small subset (200 train, 50 test) for quick demo
- 加载 25000 训练 + 25000 测试样本，取子集用于快速演示

Each sample: `{"text": "This movie was...", "label": 0 or 1}`

### Step 2: Tokenize 分词编码

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

def tokenize_fn(examples):
    return tokenizer(examples["text"], truncation=True,
                     padding="max_length", max_length=256)
```

- **tokenizer**: converts text → `input_ids` + `attention_mask`
- `[CLS] wonderful film [SEP]` → `[101, 2910, 2616, 102, 0, ..., 0]`
- Padding/truncation to uniform length (256 tokens) for batch processing
- 将文本转为模型可理解的 token ID 序列

### Step 3: Load Pretrained Model 加载预训练模型

```python
model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased", num_labels=2
)
```

**Key insight 关键理解**: The original pretraining head (`DistilBertForMaskedLM`) is replaced with a randomly initialized classification head.

```
Pretrained Body (distilBERT)   → frozen-ish (low LR keeps it close)
    └── 6 transformer layers, 66M params  ← general language knowledge
    
New Head (Classifier)           → actively learning
    └── pre_classifier + classifier
    └── 2 output neurons (positive / negative)
```

**Load report 加载报告**:

| Key 参数 | Status 状态 | Meaning 含义 |
|---|---|---|
| `classifier.weight` | MISSING | Randomly initialized for new task 为新任务随机初始化 |
| `vocab_transform.weight` | UNEXPECTED | From MLM head, discarded 来自 MLM 头部，已丢弃 |

### Step 4: TrainingArguments & Trainer 训练配置

```python
from transformers import TrainingArguments, Trainer

args = TrainingArguments(
    output_dir="./finetune-output",
    num_train_epochs=1,
    per_device_train_batch_size=8,
    learning_rate=2e-5,
    weight_decay=0.01,
    warmup_ratio=0.1,
    eval_strategy="steps",
    eval_steps=50,
    save_strategy="steps",
    save_steps=50,
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
)
```

**Why these values? 为什么这些参数？**

| Parameter 参数 | Reason 原因 |
|---|---|
| `lr=2e-5` | Small — prevents catastrophic forgetting of pretrained weights 小学习率防止灾难性遗忘 |
| `weight_decay=0.01` | L2 regularization to prevent overfitting on small data 防止小数据过拟合 |
| `warmup_ratio=0.1` | Gradually increase LR for stable training 逐步增加学习率使训练稳定 |
| `batch_size=8` | Small enough for CPU training 适合 CPU 训练 |

### Step 5: Metrics 评估指标

```python
def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    preds = np.argmax(predictions, axis=-1)
    accuracy = (preds == labels).mean()
    # F1 = 2 * precision * recall / (precision + recall)
    return {"accuracy": accuracy, "f1": f1, ...}
```

- **Accuracy 准确率**: overall correctness
- **F1 Score**: harmonic mean of precision & recall (better for imbalanced data)
- **Precision 精确率**: TP / (TP + FP) — how many predicted positives are real
- **Recall 召回率**: TP / (TP + FN) — how many real positives are caught

### Step 6-7: Evaluate & Inference 评估与推理

```python
classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)
result = classifier("This movie was fantastic!")
```

The trainer evaluates after every `eval_steps` and saves the best checkpoint. After training, we load the saved model and run predictions on new text.

---

## Actual Console Output 实际运行输出

```text
09:23:39 | INFO | Starting finetuning ... 开始微调 ...
09:23:39 | INFO | ============================================================
  0%|          | 0/25 [00:00<?, ?it/s]
  4%|▍         | 1/25 [00:03<01:12,  3.02s/it]
  ...
100%|██████████| 25/25 [01:05<00:00,  3.09s/it]

{'loss': '0.6907', 'grad_norm': '1.56', 'learning_rate': '1.455e-05', 'epoch': '0.4'}
{'loss': '0.6928', 'grad_norm': '1.67', 'learning_rate': '5.455e-06', 'epoch': '0.8'}

Training completed. Training metrics:
  train_runtime           = 74.46 seconds
  train_samples_per_second= 2.686
  train_loss              = 0.6918

Evaluation results / 评估结果:
  eval_loss        = 0.6904
  eval_accuracy    = 0.5200
  eval_f1          = 0.6757
  eval_precision   = 0.5102
  eval_recall      = 1.0000

Inference / 推理:
  Text: This movie was absolutely fantastic! The acting was superb...
  → POSITIVE 😊 (confidence: 0.5474)

  Text: What a waste of time. The plot made no sense...
  → POSITIVE 😊 (confidence: 0.5251)

  Text: A masterpiece of modern cinema. Brilliant direction...
  → POSITIVE 😊 (confidence: 0.5242)
```

**Why the low accuracy? 为什么准确率低？**
- Only 200 training samples (vs 25k full IMDB) — severely undersampled
- Only 1 epoch — needs 3-5 for convergence
- CPU training — limited batch size and speed
- The demo is designed for **speed**, not SOTA accuracy

With full IMDB (25k) + 3 epochs, expect ~90%+ accuracy.

---

## How to Customize 如何自定义

### Change Dataset 更换数据集

```python
# Custom CSV
from datasets import load_dataset
dataset = load_dataset("csv", data_files={"train": "my_train.csv"})
# Must have 'text' and 'label' columns

# HuggingFace dataset
dataset = load_dataset("rotten_tomatoes")  # another sentiment dataset
```

### Change Model 更换模型

```python
MODEL_NAME = "bert-base-uncased"       # 110M params, better accuracy
MODEL_NAME = "roberta-base"            # 125M params, optimized
MODEL_NAME = "albert-base-v2"          # 12M params, faster
MODEL_NAME = "google/bert_uncased_L-2_H-128_A-2"  # tiny BERT, 4M params
```

### Key Training Configuration 关键训练配置

| Config 配置 | Change 修改建议 |
|---|---|
| `num_train_epochs` | 3-5 for convergence, 1 for quick demo |
| `learning_rate` | 2e-5 (BERT), 3e-5 (RoBERTa), 5e-5 (DistilBERT) |
| `per_device_train_batch_size` | Max that fits in memory (CPU: 8-16, GPU: 32-64) |
| `max_length` | 128 (faster), 256 (balanced), 512 (full context) |
| `weight_decay` | 0.01 (default), increase to 0.1 for overfitting |

### Train on GPU 在 GPU 上训练

```bash
CUDA_VISIBLE_DEVICES=0 python 05-pretrain-finetune.py
```

Set `BATCH_SIZE = 32`, `NUM_EPOCHS = 3` for production-quality results.

---

## Mapping to Course Concepts 联系课程概念

| Chapter Concept 章节概念 | Code Implementation 代码实现 |
|---|---|
| **Self-Supervised Pretraining 自监督预训练** | `distilbert-base-uncased` — pretrained on masked language modeling |
| **Transfer Learning 迁移学习** | Reuse pretrained body, finetune only the head |
| **Task-Specific Head 任务头** | `num_labels=2` classification head |
| **Evaluation 评估** | `compute_metrics()` with accuracy & F1 |
| **Inference 推理** | `pipeline("text-classification")` |

---

## Further Reading 延伸阅读

- [HuggingFace TrainingArguments docs](https://huggingface.co/docs/transformers/main_classes/trainer)
- [HuggingFace Trainer docs](https://huggingface.co/docs/transformers/main/en/main_classes/trainer)
- [How to finetune a model](https://huggingface.co/docs/transformers/training)
- [DistilBERT paper (Sanh et al., 2019)](https://arxiv.org/abs/1910.01108)
