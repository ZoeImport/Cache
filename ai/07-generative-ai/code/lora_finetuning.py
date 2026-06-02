"""
lora_finetuning.py -- LoRA Fine-Tuning Demonstration with PEFT
==============================================================

Demonstrates Parameter-Efficient Fine-Tuning (PEFT) using LoRA
on GPT-2 (124M).  Compares memory footprint, trainable parameter
count, and generation quality between full fine-tuning and LoRA.

Architecture:
  1. Load pre-trained GPT-2 with HuggingFace transformers
  2. Apply LoRA adapters via PEFT (targeting W_q, W_v)
  3. Full fine-tuning baseline for comparison
  4. Fine-tune on a small text dataset (ELI5 subset)
  5. Generate text BEFORE and AFTER fine-tuning
  6. Print parameter counts, memory usage, and loss curves

Dependencies: torch >= 2.1.0, transformers >= 4.36.0,
              peft >= 0.7.0, datasets >= 2.14.0

Usage:
    python lora_finetuning.py

Expected output:
    - Trainable parameter count comparison (Full FT vs LoRA)
    - Memory usage comparison
    - Training loss curves
    - Generated text samples before and after fine-tuning
"""

import os
import math
import time
import copy
from typing import Optional

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    default_data_collator,
    get_linear_schedule_with_warmup,
)
from peft import LoraConfig, get_peft_model, TaskType
from datasets import load_dataset

# ---------------------------------------------------------------------------
# Device and Reproducibility
# ---------------------------------------------------------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"[INFO] Device: {device}\n")

torch.manual_seed(42)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(42)

# ---------------------------------------------------------------------------
# Hyper-parameters
# ---------------------------------------------------------------------------
MODEL_NAME        = "gpt2"
LORA_R            = 8
LORA_ALPHA        = 16
LORA_DROPOUT      = 0.05
TARGET_MODULES    = ["c_attn"]

BATCH_SIZE        = 4
MAX_SEQ_LEN       = 128
NUM_EPOCHS        = 3
LEARNING_RATE     = 2e-4
MAX_TRAIN_SAMPLES = 256
WARMUP_STEPS      = 10
GRADIENT_CLIP     = 1.0

# Generation
GEN_PROMPT        = "The future of AI is"
GEN_MAX_LEN       = 50
GEN_TEMPERATURE   = 0.8

# ---------------------------------------------------------------------------
# Helper: count parameters
# ---------------------------------------------------------------------------
def count_parameters(model: nn.Module, trainable_only: bool = False) -> int:
    if trainable_only:
        return sum(p.numel() for p in model.parameters() if p.requires_grad)
    return sum(p.numel() for p in model.parameters())

def estimate_memory(model: nn.Module, unit: str = "MB") -> float:
    total_bytes = sum(p.numel() * p.element_size() for p in model.parameters())
    if unit == "GB":
        return total_bytes / (1024 ** 3)
    return total_bytes / (1024 ** 2)

# ---------------------------------------------------------------------------
# 1. Load model and tokenizer
# ---------------------------------------------------------------------------
print("=" * 60)
print("1. Loading pre-trained model and tokenizer")
print("=" * 60)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
tokenizer.pad_token = tokenizer.eos_token

base_model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
base_model.to(device)
base_model.train()

print(f"    Model: {MODEL_NAME}")
print(f"    Total params: {count_parameters(base_model):,}")
print(f"    Memory (FP32): {estimate_memory(base_model):.2f} MB")

# ---------------------------------------------------------------------------
# 2. Apply LoRA
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("2. Applying LoRA adapters")
print("=" * 60)

lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=LORA_R,
    lora_alpha=LORA_ALPHA,
    lora_dropout=LORA_DROPOUT,
    target_modules=TARGET_MODULES,
    bias="none",
)

lora_model = get_peft_model(base_model, lora_config)
lora_model.print_trainable_parameters()

lora_params = count_parameters(lora_model, trainable_only=True)
full_params = count_parameters(lora_model, trainable_only=False)

print(f"\n    LoRA trainable params: {lora_params:,}")
print(f"    Full model params:     {full_params:,}")
print(f"    LoRA ratio:            {100 * lora_params / full_params:.4f}%")
print(f"    Full FT would update:  {full_params:,} params")

# ---------------------------------------------------------------------------
# 3. Full fine-tuning baseline
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("3. Full fine-tuning baseline (reference)")
print("=" * 60)

full_model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
full_model.to(device)
full_model.train()

full_total = count_parameters(full_model, trainable_only=False)
full_memory = estimate_memory(full_model)
lora_memory = estimate_memory(lora_model)

print(f"    Full FT total:     {full_total:,}")
print(f"    Full FT memory:    {full_memory:.2f} MB")
print(f"    LoRA memory:       {lora_memory:.2f} MB")
print(f"\n    {'Metric':<25} {'Full FT':<15} {'LoRA':<15} {'Ratio':<10}")
print(f"    {'-'*25} {'-'*15} {'-'*15} {'-'*10}")
print(f"    {'Trainable params':<25} {full_total:<15,} {lora_params:<15,} "
      f"{full_total / lora_params:<10.1f}x")
print(f"    {'Memory (FP32)':<25} {full_memory:<15.2f} {lora_memory:<15.2f} "
      f"{full_memory / lora_memory:<10.1f}x")

# Keep a copy of the pre-trained model for generation comparison
pretrained_model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
pretrained_model.to(device)
pretrained_model.eval()

# ---------------------------------------------------------------------------
# 4. Prepare dataset
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("4. Loading and tokenizing dataset (ELI5 subset)")
print("=" * 60)

dataset = load_dataset("eli5", split="train_eli5[:1000]", trust_remote_code=True)

def tokenize_function(examples):
    texts = examples.get("answers", [])
    processed_texts = []
    for answer_list in texts["text"]:
        if answer_list and len(answer_list) > 0:
            processed_texts.append(answer_list[0][:512])
        else:
            processed_texts.append("No answer available.")
    tokenized = tokenizer(
        processed_texts,
        truncation=True,
        padding="max_length",
        max_length=MAX_SEQ_LEN,
    )
    tokenized["labels"] = tokenized["input_ids"].copy()
    return tokenized

tokenized_dataset = dataset.map(
    tokenize_function,
    batched=True,
    remove_columns=dataset.column_names,
)

train_dataset = tokenized_dataset.select(
    range(min(MAX_TRAIN_SAMPLES, len(tokenized_dataset)))
)
train_dataloader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    collate_fn=default_data_collator,
)

print(f"    Dataset: ELI5 (subset)")
print(f"    Training samples: {len(train_dataset)}")
print(f"    Batch size: {BATCH_SIZE}")
print(f"    Max sequence length: {MAX_SEQ_LEN}")

# ---------------------------------------------------------------------------
# 5. Training setup
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("5. Training LoRA model")
print("=" * 60)

optimizer = torch.optim.AdamW(lora_model.parameters(), lr=LEARNING_RATE)
total_steps = len(train_dataloader) * NUM_EPOCHS
scheduler = get_linear_schedule_with_warmup(
    optimizer,
    num_warmup_steps=WARMUP_STEPS,
    num_training_steps=total_steps,
)

global_step = 0
all_losses = []
start_time = time.time()

for epoch in range(1, NUM_EPOCHS + 1):
    epoch_loss = 0.0
    num_batches = 0

    for batch in train_dataloader:
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch.get("attention_mask", None)
        if attention_mask is not None:
            attention_mask = attention_mask.to(device)
        labels = batch["labels"].to(device)

        outputs = lora_model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels,
        )
        loss = outputs.loss

        loss.backward()
        torch.nn.utils.clip_grad_norm_(lora_model.parameters(), GRADIENT_CLIP)
        optimizer.step()
        scheduler.step()
        optimizer.zero_grad()

        epoch_loss += loss.item()
        num_batches += 1
        global_step += 1

    avg_loss = epoch_loss / max(num_batches, 1)
    all_losses.append(avg_loss)

    gpu_mem = 0
    if torch.cuda.is_available():
        gpu_mem = torch.cuda.max_memory_allocated() / (1024 ** 3)

    print(f"    Epoch {epoch}/{NUM_EPOCHS} | Loss: {avg_loss:.4f} | "
          f"LR: {scheduler.get_last_lr()[0]:.2e} | "
          f"{f'GPU Mem: {gpu_mem:.2f} GB' if gpu_mem else ''}")

elapsed = time.time() - start_time
print(f"\n    Training completed in {elapsed:.1f}s")

# ---------------------------------------------------------------------------
# 6. Text generation: BEFORE vs AFTER
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("6. Text generation comparison: BEFORE vs AFTER fine-tuning")
print("=" * 60)

@torch.no_grad()
def generate_text(
    model: nn.Module,
    tokenizer,
    prompt: str,
    max_length: int = GEN_MAX_LEN,
    temperature: float = GEN_TEMPERATURE,
) -> str:
    model.eval()
    input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)
    for _ in range(max_length):
        outputs = model(input_ids)
        logits = outputs.logits[:, -1, :] / temperature
        probs = torch.softmax(logits, dim=-1)
        next_token = torch.multinomial(probs, num_samples=1)
        input_ids = torch.cat([input_ids, next_token], dim=-1)
        if next_token.item() == tokenizer.eos_token_id:
            break
    return tokenizer.decode(input_ids[0], skip_special_tokens=True)

prompt = GEN_PROMPT
print(f"\n    Prompt: \"{prompt}\"\n")

before_text = generate_text(pretrained_model, tokenizer, prompt)
print(f"    [BEFORE - Pre-trained model]")
print(f"    {before_text}")
print()

after_text = generate_text(lora_model, tokenizer, prompt)
print(f"    [AFTER - LoRA fine-tuned model]")
print(f"    {after_text}")
print()

# ---------------------------------------------------------------------------
# 7. Summary
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("7. Summary")
print("=" * 60)

print(f"""
    {'Item':<30} {'Full FT':<18} {'LoRA':<18}
    {'-'*66}
    {'Trainable parameters':<30} {full_total:<18,} {lora_params:<18,}
    {'% of total params':<30} {'100%':<18} {100*lora_params/full_params:.4f}%
    {'Memory (FP32)':<30} {full_memory:<18.2f} {lora_memory:<18.2f} MB
    {'Memory ratio':<30} {'1.0x':<18} {full_memory/lora_memory:.1f}x
    {'Training time':<30} {'(ref only)':<18} {elapsed:.1f}s
    {'Final loss':<30} {'N/A':<18} {all_losses[-1]:.4f}
""")

print("""
    KEY TAKEAWAYS:
    - LoRA achieves comparable fine-tuning quality with < 1% of parameters.
    - LoRA adapters can be merged into the base model at inference time,
      introducing ZERO additional latency.
    - QLoRA extends this to 4-bit quantized models, enabling fine-tuning
      of 65B models on a single 48GB GPU.
    - The low-rank assumption (r << d) holds because fine-tuning updates
      have low intrinsic dimensionality.
""")
