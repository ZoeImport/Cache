#!/usr/bin/env python3
"""
Pretrain-Finetune Workflow 预训练-微调工作流
============================================
Load a pre-trained model → finetune on custom dataset → evaluate → inference.
加载预训练模型 → 在自定义数据集上微调 → 评估 → 推理预测.

Concepts covered:
  - Transfer learning / 迁移学习
  - Task adaptation / 任务适配
  - Catastrophic forgetting (briefly) / 灾难性遗忘
  - Evaluation metrics / 评估指标

Requires: torch, transformers, datasets, accelerate, numpy
"""

import os
import sys
import json
import logging
import numpy as np
from pathlib import Path
from typing import Optional, Tuple

import torch
from torch.utils.data import DataLoader

# ── HuggingFace ecosystem ──────────────────────────────────────────────
import datasets
from datasets import load_dataset, Dataset, DatasetDict
import transformers
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback,
    pipeline,
    set_seed,
)
from transformers.trainer_utils import EvalPrediction

# ── Metrics ────────────────────────────────────────────────────────────
try:
    import evaluate as hf_evaluate

    _HAS_EVALUATE = True
except ImportError:
    _HAS_EVALUATE = False

# ── Logging ────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
    stream=sys.stdout,
)
log = logging.getLogger(__name__)

# ── Configuration ──────────────────────────────────────────────────────
HF_CACHE_DIR = os.environ.get("HF_HOME", None)

# Model / 模型
MODEL_NAME = "distilbert-base-uncased"  # 66M params, runs on CPU
MAX_LENGTH = 256                         # token truncation length

# Data / 数据
DATASET_NAME = "stanfordnlp/imdb"        # binary sentiment classification
DATASET_CONFIG = "plain_text"            # config name for imdb
NUM_TRAIN_SAMPLES = 200                  # small subset for quick demo
NUM_TEST_SAMPLES = 50

# Training / 训练
OUTPUT_DIR = "./finetune-output"
BATCH_SIZE = 8
LEARNING_RATE = 2e-5
NUM_EPOCHS = 1
WEIGHT_DECAY = 0.01
WARMUP_RATIO = 0.1
LOGGING_STEPS = 10
SAVE_STRATEGY = "steps"
SAVE_STEPS = 50
EVAL_STRATEGY = "steps"
EVAL_STEPS = 50
SEED = 42

# Device / 设备
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
log.info("Using device: %s", DEVICE)
log.info("PyTorch %s | Transformers %s | Datasets %s",
         torch.__version__, transformers.__version__, datasets.__version__)

set_seed(SEED)
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ══════════════════════════════════════════════════════════════════════
# Step 1: Load Dataset  加载数据集
# ══════════════════════════════════════════════════════════════════════
def load_imdb_subset(
    num_train: int = NUM_TRAIN_SAMPLES,
    num_test: int = NUM_TEST_SAMPLES,
) -> DatasetDict:
    """
    Load a small balanced subset of IMDB for quick experimentation.
    加载 IMDB 的小型平衡子集用于快速实验。

    IMDB has 25k train / 25k test, balanced (50% pos, 50% neg).
    We take num_train/2 from each class for train, num_test/2 for test.
    """
    log.info("Loading IMDB dataset (full) ...")
    full: DatasetDict = load_dataset(DATASET_NAME, DATASET_CONFIG, cache_dir=HF_CACHE_DIR)  # type: ignore

    def _balanced_subset(split: str, n: int) -> Dataset:
        ds = full[split]
        # Keep only n/2 positive and n/2 negative examples
        pos = ds.filter(lambda x: x["label"] == 1).select(range(max(1, n // 2)))
        neg = ds.filter(lambda x: x["label"] == 0).select(range(max(1, n // 2)))
        import itertools
        combined = Dataset.from_list(list(itertools.chain(pos, neg)))
        return combined.shuffle(seed=SEED)

    train_sub = _balanced_subset("train", num_train)
    test_sub = _balanced_subset("test", num_test)

    log.info("Train samples: %d (pos=%d, neg=%d)",
             len(train_sub),
             sum(train_sub["label"]),
             len(train_sub) - sum(train_sub["label"]))
    log.info("Test samples: %d (pos=%d, neg=%d)",
             len(test_sub),
             sum(test_sub["label"]),
             len(test_sub) - sum(test_sub["label"]))

    return DatasetDict({"train": train_sub, "test": test_sub})


# ══════════════════════════════════════════════════════════════════════
# Step 2: Tokenize  分词 / 编码
# ══════════════════════════════════════════════════════════════════════
def tokenize_dataset(
    raw: DatasetDict,
    model_name: str = MODEL_NAME,
    max_length: int = MAX_LENGTH,
) -> DatasetDict:
    """
    Tokenize text using the model's matching tokenizer.
    使用与模型匹配的 tokenizer 对文本进行编码。
    """
    log.info("Loading tokenizer: %s", model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=HF_CACHE_DIR)

    def _tokenize_fn(examples):
        return tokenizer(
            examples["text"],
            truncation=True,
            padding="max_length",
            max_length=max_length,
        )

    log.info("Tokenizing datasets ...")
    tokenized = raw.map(_tokenize_fn, batched=True)
    # Remove original text column — Trainer expects only input_ids, attention_mask, label
    tokenized = tokenized.remove_columns(["text"])
    # Rename 'label' column name (it's already 'label' in IMDB)
    tokenized.set_format("torch", columns=["input_ids", "attention_mask", "label"])
    return tokenized  # type: ignore


# ══════════════════════════════════════════════════════════════════════
# Step 3: Metrics  评估指标
# ══════════════════════════════════════════════════════════════════════
def compute_metrics(eval_pred: EvalPrediction) -> dict:
    """
    Compute accuracy & F1 from model predictions.
    从模型预测中计算准确率和 F1 分数。
    """
    predictions, labels = eval_pred
    preds = np.argmax(predictions, axis=-1)

    accuracy = (preds == labels).mean().item()

    # Manual F1 (binary)
    tp = ((preds == 1) & (labels == 1)).sum().item()
    fp = ((preds == 1) & (labels == 0)).sum().item()
    fn = ((preds == 0) & (labels == 1)).sum().item()
    precision = tp / (tp + fp + 1e-10)
    recall = tp / (tp + fn + 1e-10)
    f1 = 2 * precision * recall / (precision + recall + 1e-10)

    return {"accuracy": round(accuracy, 4), "f1": round(f1, 4),
            "precision": round(precision, 4), "recall": round(recall, 4)}


# ══════════════════════════════════════════════════════════════════════
# Step 4: Model Loading  加载预训练模型
# ══════════════════════════════════════════════════════════════════════
def load_pretrained_model(
    model_name: str = MODEL_NAME,
    num_labels: int = 2,
) -> Tuple[AutoModelForSequenceClassification, AutoTokenizer]:
    """
    Load a pre-trained transformer with a randomly initialized classification head.
    加载预训练 transformer 并附加随机初始化的分类头。

    The pre-trained body (distilBERT) keeps its learned representations;
    only the classification head (last layer) needs to learn the new task.
    预训练 body 保留已学表示，仅分类头需要学习新任务。
    """
    log.info("Loading pre-trained model: %s (num_labels=%d)", model_name, num_labels)
    tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=HF_CACHE_DIR)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        num_labels=num_labels,
        cache_dir=HF_CACHE_DIR,
    )
    model.to(DEVICE)

    # Count trainable parameters / 可训练参数统计
    total = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    log.info("Total params: %d | Trainable: %d (%.2f%%)",
             total, trainable, 100.0 * trainable / total)

    return model, tokenizer


# ══════════════════════════════════════════════════════════════════════
# Step 5: Training  训练
# ══════════════════════════════════════════════════════════════════════
def train_model(
    model: AutoModelForSequenceClassification,
    tokenized_data: DatasetDict,
    output_dir: str = OUTPUT_DIR,
) -> Trainer:
    """
    Set up HuggingFace Trainer and run finetuning.
    设置 HuggingFace Trainer 并执行微调。
    """
    log.info("Setting up TrainingArguments ...")
    args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=NUM_EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        per_device_eval_batch_size=BATCH_SIZE * 2,
        learning_rate=LEARNING_RATE,
        weight_decay=WEIGHT_DECAY,
        warmup_ratio=WARMUP_RATIO,
        logging_steps=LOGGING_STEPS,
        save_strategy=SAVE_STRATEGY,
        save_steps=SAVE_STEPS,
        save_total_limit=2,
        eval_strategy=EVAL_STRATEGY,
        eval_steps=EVAL_STEPS,
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        greater_is_better=True,
        report_to="none",           # disable wandb / tensorboard for demo
        seed=SEED,
        fp16=False,                 # CPU or no-CUDA safe
        dataloader_pin_memory=False,
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=tokenized_data["train"],
        eval_dataset=tokenized_data["test"],
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=3)],
    )

    # ── Train ──────────────────────────────────────────────────────
    log.info("=" * 60)
    log.info("Starting finetuning ... 开始微调 ...")
    log.info("=" * 60)
    train_result = trainer.train()

    # Save the final model / 保存最终模型
    trainer.save_model(output_dir)
    log.info("Model saved to: %s", output_dir)

    # Save training metrics / 保存训练指标
    with open(os.path.join(output_dir, "train_metrics.json"), "w") as f:
        json.dump(train_result.metrics, f, indent=2)

    # ── Log training loss curve summary ────────────────────────────
    log_history = trainer.state.log_history
    loss_steps = [h for h in log_history if "loss" in h]
    if loss_steps:
        losses = [h["loss"] for h in loss_steps]
        log.info("Training loss: start=%.4f, end=%.4f, min=%.4f",
                 losses[0], losses[-1], min(losses))

    return trainer


# ══════════════════════════════════════════════════════════════════════
# Step 6: Evaluation  评估
# ══════════════════════════════════════════════════════════════════════
def evaluate_model(trainer: Trainer, tokenized_data: DatasetDict) -> dict:
    """
    Run evaluation on the test set and print metrics.
    在测试集上运行评估并打印指标。
    """
    log.info("Evaluating on test set ... 在测试集上评估 ...")
    metrics = trainer.evaluate(tokenized_data["test"])
    log.info("Evaluation results / 评估结果:")
    for key, val in metrics.items():
        log.info("  %s = %.4f", key, val)

    # Save evaluation metrics / 保存评估指标
    with open(os.path.join(OUTPUT_DIR, "eval_metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)

    return metrics


# ══════════════════════════════════════════════════════════════════════
# Step 7: Inference  推理
# ══════════════════════════════════════════════════════════════════════
def run_inference(
    model: AutoModelForSequenceClassification,
    tokenizer: AutoTokenizer,
    examples: list,
) -> None:
    """
    Run inference on raw text examples using the finetuned model.
    使用微调后的模型对原始文本进行推理。
    """
    log.info("Running inference on sample texts ... 推理示例文本 ...")

    classifier = pipeline(
        "text-classification",
        model=model,
        tokenizer=tokenizer,
        device=0 if DEVICE == "cuda" else -1,
        top_k=None,  # return all labels
    )

    results = classifier(examples)
    for text, out in zip(examples, results):
        # out is a list of dicts like [{'label':'LABEL_1','score':0.98}, ...]
        label_map = {"LABEL_0": "NEGATIVE 😠", "LABEL_1": "POSITIVE 😊"}
        best = max(out, key=lambda x: x["score"])
        sentiment = label_map.get(best["label"], best["label"])
        log.info("  Text 文本: %s", text[:80] + ("..." if len(text) > 80 else ""))
        log.info("  → %s (confidence: %.4f)", sentiment, best["score"])


# ══════════════════════════════════════════════════════════════════════
# Main Pipeline  主流程
# ══════════════════════════════════════════════════════════════════════
def main():
    log.info("")
    log.info("╔═══════════════════════════════════════════════════╗")
    log.info("║  Pretrain-Finetune Workflow  预训练-微调工作流   ║")
    log.info("╚═══════════════════════════════════════════════════╝")
    log.info("")

    # ── Step 1: Load data ──────────────────────────────────────────
    log.info("─── Step 1 [1/7]: Loading dataset  加载数据集 ───")
    raw_data = load_imdb_subset(NUM_TRAIN_SAMPLES, NUM_TEST_SAMPLES)

    # ── Step 2: Tokenize ───────────────────────────────────────────
    log.info("─── Step 2 [2/7]: Tokenizing  分词编码 ───")
    tokenized_data = tokenize_dataset(raw_data)

    # ── Step 3: Load pre-trained model ─────────────────────────────
    log.info("─── Step 3 [3/7]: Loading pre-trained model  加载预训练模型 ───")
    model, tokenizer = load_pretrained_model()

    # ── Step 4: Train (finetune) ───────────────────────────────────
    log.info("─── Step 4 [4/7]: Finetuning  微调 ───")
    trainer = train_model(model, tokenized_data)

    # ── Step 5: Evaluate ───────────────────────────────────────────
    log.info("─── Step 5 [5/7]: Evaluation  评估 ───")
    eval_metrics = evaluate_model(trainer, tokenized_data)

    # ── Step 6: Inference ──────────────────────────────────────────
    log.info("─── Step 6 [6/7]: Inference  推理 ───")
    sample_texts = [
        "This movie was absolutely fantastic! The acting was superb and the story kept me on the edge of my seat.",
        "What a waste of time. The plot made no sense and the characters were completely unbelievable.",
        "It was okay, nothing special but not terrible either. Some parts were entertaining.",
        "A masterpiece of modern cinema. Brilliant direction and stunning cinematography.",
        "I fell asleep halfway through. Extremely boring and predictable.",
    ]
    run_inference(model, tokenizer, sample_texts)

    # ── Step 7: Summary ────────────────────────────────────────────
    log.info("─── Step 7 [7/7]: Summary  总结 ───")
    log.info("")
    log.info("═══════════════════════════════════════════════════")
    log.info("Finetuning complete!  微调完成！")
    log.info("Best accuracy: %.4f", eval_metrics.get("eval_accuracy", 0))
    log.info("Best F1:       %.4f", eval_metrics.get("eval_f1", 0))
    log.info("Model saved at: %s", os.path.abspath(OUTPUT_DIR))
    log.info("═══════════════════════════════════════════════════")

    # ── Cleanup: remove output dir for demo repeatability ──────────
    # Uncomment the next line to keep the model:
    # log.info("Model kept at %s", os.path.abspath(OUTPUT_DIR))
    import shutil
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
        log.info("Temporary output cleaned up. 临时输出已清理。")


if __name__ == "__main__":
    main()
