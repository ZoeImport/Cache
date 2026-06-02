"""
Python ML Ecosystem Overview — Quick Tour
Python ML 生态系统纵览 — 快速演示

This script demonstrates key frameworks across the Python ML ecosystem:
- HuggingFace Transformers (model loading, pipeline inference)
- Weights & Biases (experiment tracking)
- LangChain (LLM chain)
- Version comparison of all major packages

Each section gracefully handles missing dependencies.
"""

import sys
import importlib

SEPARATOR = "=" * 64


def print_header(title: str) -> None:
    print(f"\n{SEPARATOR}")
    print(f"  {title}")
    print(SEPARATOR)


def get_version(pkg_name: str, import_name: str | None = None) -> str:
    """Safely get package version, return 'not installed' if missing."""
    try:
        mod = importlib.import_module(import_name or pkg_name)
        return getattr(mod, "__version__", "unknown")
    except (ImportError, ModuleNotFoundError):
        return "✗ not installed"


# ---------------------------------------------------------------------------
# 1. Version Overview
# ---------------------------------------------------------------------------
print_header("1. Package Version Overview  /  包版本概览")

packages = [
    ("torch", "torch"),
    ("transformers", "transformers"),
    ("datasets", "datasets"),
    ("accelerate", "accelerate"),
    ("peft", "peft"),
    ("pytorch_lightning", "pytorch_lightning"),
    ("lightning_fabric", "lightning_fabric"),
    ("wandb", "wandb"),
    ("mlflow", "mlflow"),
    ("langchain", "langchain"),
    ("llama_index", "llama_index"),
    ("vllm", "vllm"),
]

for pkg_name, import_name in packages:
    ver = get_version(pkg_name, import_name)
    print(f"  {pkg_name:<20s} {ver}")


# ---------------------------------------------------------------------------
# 2. HuggingFace Pipeline Demo
# ---------------------------------------------------------------------------
print_header("2. HuggingFace Pipeline Demo  /  Transformers 管道演示")

try:
    from transformers import pipeline

    classifier = pipeline(
        "text-classification",
        model="distilbert-base-uncased-finetuned-sst-2-english",
    )
    texts = [
        "The Python ML ecosystem is incredibly rich.",
        "This code is not very useful by itself.",
    ]
    for text in texts:
        result = classifier(text)[0]
        print(f"  input : {text}")
        print(f"  output: label={result['label']}, score={result['score']:.4f}\n")

except ImportError:
    print("  [SKIP] transformers not installed")
except Exception as e:
    print(f"  [ERROR] pipeline failed: {e}")


# ---------------------------------------------------------------------------
# 3. HuggingFace Datasets Quick Look
# ---------------------------------------------------------------------------
print_header("3. Datasets Streaming Demo  /  Datasets 流式加载")

try:
    from datasets import load_dataset

    dataset = load_dataset("stanfordnlp/imdb", split="train", streaming=True)
    print(f"  Dataset size: ~{dataset.n_samples if hasattr(dataset, 'n_samples') else 'unknown'} samples")
    for i, example in enumerate(dataset):
        if i >= 2:
            break
        text_preview = example["text"][:100].replace("\n", " ")
        print(f"  sample {i}: {text_preview}...")
        print(f"  label : {example['label']} ({'pos' if example['label'] else 'neg'})")
except ImportError:
    print("  [SKIP] datasets not installed")
except Exception as e:
    print(f"  [ERROR] datasets demo failed: {e}")


# ---------------------------------------------------------------------------
# 4. Weights & Biases Demo (disabled by default)
# ---------------------------------------------------------------------------
print_header("4. Weights & Biases Experiment Tracking  /  WandB 实验跟踪")

try:
    import wandb

    # Use anonymous mode for demo purposes
    # In real usage: wandb.init(project="my-project")
    with wandb.init(project="ecosystem-demo", mode="disabled") as run:
        run.config.update({"learning_rate": 1e-3, "epochs": 5})
        for epoch in range(3):
            loss = 1.0 / (epoch + 1)  # fake loss
            acc = min(1.0, 0.2 * (epoch + 1))
            wandb.log({"epoch": epoch, "loss": loss, "accuracy": acc})
            print(f"  epoch {epoch}: loss={loss:.4f}, acc={acc:.4f} [logged to wandb]")
        print("  WandB run completed (disabled mode, no cloud sync)")

except ImportError:
    print("  [SKIP] wandb not installed")


# ---------------------------------------------------------------------------
# 5. LangChain Demo
# ---------------------------------------------------------------------------
print_header("5. LangChain Chain Demo  /  LangChain 链演示")

try:
    from langchain.chains import LLMChain
    from langchain.prompts import PromptTemplate
    from langchain.llms import HuggingFacePipeline

    # Use a local HuggingFace model as the LLM backend
    hf_pipeline = pipeline(
        "text-generation",
        model="distilgpt2",
        max_new_tokens=30,
        pad_token_id=50256,
    )
    llm = HuggingFacePipeline(pipeline=hf_pipeline)

    prompt = PromptTemplate(
        input_variables=["topic"],
        template="Write a short sentence about {topic}:\n",
    )
    chain = LLMChain(llm=llm, prompt=prompt)

    result = chain.run("machine learning tools")
    print(f"  Generated text: {result.strip()}")
    print(f"  (Note: distilgpt2 is very small; output quality is limited)")

except ImportError:
    print("  [SKIP] langchain not installed")
except Exception as e:
    print(f"  [ERROR] langchain demo failed: {e}")


# ---------------------------------------------------------------------------
# 6. Summary — When to Use Each Tool
# ---------------------------------------------------------------------------
print_header("6. Quick Decision Guide  /  快速选型指南")

guide = """
  Framework       When to use
  ─────────────────────────────────────────────────────────────
  Transformers    Any model loading & inference task
  Datasets        Large-scale data loading (streaming)
  PEFT            Fine-tuning LLMs on limited hardware
  Lightning       Full training pipeline with minimal boilerplate
  Fabric          Flexible training without Trainer lock-in
  Accelerate      Distributed training for Transformers users
  WandB           Experiment tracking & team collaboration
  MLflow          Open-source experiment management (self-hosted)
  LangChain       LLM application orchestration (agents, chains)
  LlamaIndex      RAG systems & document retrieval
  vLLM            High-throughput LLM serving in production
  Ollama          Local LLM for dev / personal use
  llama.cpp       CPU-first inference on edge devices
"""
print(guide)


def main():
    print("\n✅ Ecosystem overview complete.  /  生态概览完成。\n")


if __name__ == "__main__":
    main()
