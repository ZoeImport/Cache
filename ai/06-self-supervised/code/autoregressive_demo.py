"""
autoregressive_demo.py -- Autoregressive Language Modeling & Scaling Laws Demo

Demonstrates:
- Next-token prediction using GPT-2 (via transformers library)
- Comparison of decoding strategies: greedy vs. sampling vs. top-k
- Perplexity measurement
- Visualizing how autoregressive models build text step by step

Usage:
    python code/autoregressive_demo.py

Requires:
    pip install torch transformers
"""

import torch
import torch.nn.functional as F
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import numpy as np
import warnings
from typing import List, Optional

warnings.filterwarnings("ignore")

# -- Configuration ------------------------------------------------------------

MODEL_NAME: str = "gpt2"  # Can also use "gpt2-medium", "gpt2-large", "gpt2-xl"
DEVICE: torch.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MAX_LENGTH: int = 100  # Maximum generation length
TOP_K_VALUES: List[int] = [1, 10, 50]  # Top-k values for comparison
TEMPERATURE: float = 0.8  # Sampling temperature
SEED: int = 42

# Prompts for demonstration
PROMPTS: List[str] = [
    "The future of artificial intelligence is",
    "To solve this problem, we first need to",
    "In the beginning, the universe was",
    "The key insight of the Transformer architecture is",
]

# A few sentences for perplexity evaluation
PPL_SENTENCES: List[str] = [
    "The cat sat on the mat.",
    "The quick brown fox jumps over the lazy dog.",
    "Natural language processing is a subfield of artificial intelligence.",
    "Colorless green ideas sleep furiously.",  # Chomsky's famous grammatical but nonsensical sentence
]

torch.manual_seed(SEED)


# -- Model Loading ------------------------------------------------------------

def load_model() -> tuple[GPT2LMHeadModel, GPT2Tokenizer]:
    """Load pretrained GPT-2 model and tokenizer."""
    print(f"Loading {MODEL_NAME}...")
    tokenizer = GPT2Tokenizer.from_pretrained(MODEL_NAME)
    tokenizer.pad_token = tokenizer.eos_token  # GPT-2 has no pad token by default
    model = GPT2LMHeadModel.from_pretrained(MODEL_NAME).to(DEVICE)
    model.eval()
    print(f"Model loaded: {MODEL_NAME}, Parameters: {model.num_parameters():,}")
    print(f"Vocabulary size: {tokenizer.vocab_size}")
    print(f"Device: {DEVICE}")
    return model, tokenizer


# -- Core: Next-Token Prediction ---------------------------------------------

def predict_next_token(
    model: GPT2LMHeadModel,
    tokenizer: GPT2Tokenizer,
    text: str,
) -> tuple[str, float]:
    """
    Predict the single most likely next token given a prefix.

    Returns (next_token_str, probability).
    """
    inputs = tokenizer(text, return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits[:, -1, :]  # Take the last position's logits

    probs = F.softmax(logits, dim=-1)
    top_prob, top_idx = probs.topk(1, dim=-1)
    next_token = tokenizer.decode(top_idx[0].item())

    return next_token, top_prob[0].item()


def step_by_step_generation(
    model: GPT2LMHeadModel,
    tokenizer: GPT2Tokenizer,
    prompt: str,
    n_tokens: int = 10,
) -> None:
    """
    Show step-by-step autoregressive generation by revealing one token at a time.
    """
    print(f"\n{'='*70}")
    print(f"Step-by-step autoregressive generation")
    print(f"Prompt: '{prompt}'")
    print(f"{'='*70}")

    generated = prompt
    for step in range(n_tokens):
        next_token, prob = predict_next_token(model, tokenizer, generated)
        print(f"  Step {step+1:2d}: P('{next_token}' | ...'{generated[-40:]}') = {prob:.4f}")
        generated += next_token

    print(f"\nFinal generated text:")
    print(f"  {generated}")


# -- Decoding Strategies ------------------------------------------------------

def generate_greedy(
    model: GPT2LMHeadModel,
    tokenizer: GPT2Tokenizer,
    prompt: str,
    max_new_tokens: int = MAX_LENGTH,
) -> str:
    """Greedy decoding: at each step, pick the token with highest probability."""
    inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,  # Greedy
            pad_token_id=tokenizer.eos_token_id,
        )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


def generate_sampling(
    model: GPT2LMHeadModel,
    tokenizer: GPT2Tokenizer,
    prompt: str,
    temperature: float = TEMPERATURE,
    max_new_tokens: int = MAX_LENGTH,
) -> str:
    """Random sampling: sample from the full probability distribution."""
    inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=temperature,
            pad_token_id=tokenizer.eos_token_id,
        )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


def generate_topk(
    model: GPT2LMHeadModel,
    tokenizer: GPT2Tokenizer,
    prompt: str,
    top_k: int = 50,
    temperature: float = TEMPERATURE,
    max_new_tokens: int = MAX_LENGTH,
) -> str:
    """Top-k sampling: sample from the top-k most likely tokens only."""
    inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            top_k=top_k,
            temperature=temperature,
            pad_token_id=tokenizer.eos_token_id,
        )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


def generate_topk_with_seed(
    model: GPT2LMHeadModel,
    tokenizer: GPT2Tokenizer,
    prompt: str,
    top_k: int = 50,
    temperature: float = TEMPERATURE,
    seed: int = 42,
    max_new_tokens: int = MAX_LENGTH,
) -> str:
    """Top-k sampling with a fixed seed for reproducibility."""
    torch.manual_seed(seed)
    return generate_topk(model, tokenizer, prompt, top_k, temperature, max_new_tokens)


def compare_decoding_strategies(
    model: GPT2LMHeadModel,
    tokenizer: GPT2Tokenizer,
    prompt: str,
) -> None:
    """Compare greedy, sampling, and top-k decoding on the same prompt."""
    print(f"\n{'='*70}")
    print(f"Decoding strategy comparison")
    print(f"Prompt: '{prompt}'")
    print(f"{'='*70}")

    # Greedy (deterministic)
    result_greedy = generate_greedy(model, tokenizer, prompt)
    print(f"\n[Greedy] (deterministic, always picks highest prob token):")
    print(f"  {result_greedy}")

    # Random sampling (stochastic)
    result_sample = generate_sampling(model, tokenizer, prompt)
    print(f"\n[Sampling] (t={TEMPERATURE}, stochastic):")
    print(f"  {result_sample}")

    # Top-k sampling
    for k in TOP_K_VALUES:
        result = generate_topk_with_seed(model, tokenizer, prompt, top_k=k)
        print(f"\n[Top-{k}] (seed={SEED}):")
        print(f"  {result}")

    print()


# -- Perplexity ----------------------------------------------------------------

def compute_perplexity(
    model: GPT2LMHeadModel,
    tokenizer: GPT2Tokenizer,
    sentence: str,
) -> float:
    """
    Compute perplexity of a sentence under the model.

    Perplexity = exp( cross_entropy_loss )
    Lower perplexity = the model finds the sentence more "likely".
    """
    inputs = tokenizer(sentence, return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        outputs = model(**inputs, labels=inputs["input_ids"])
        loss = outputs.loss
    return float(torch.exp(loss).cpu().numpy())


def analyze_perplexity(
    model: GPT2LMHeadModel,
    tokenizer: GPT2Tokenizer,
    sentences: List[str],
) -> None:
    """Compute and report perplexity for a list of sentences."""
    print(f"\n{'='*70}")
    print(f"Perplexity analysis (lower = more likely under the model)")
    print(f"{'='*70}")

    results = []
    for sent in sentences:
        ppl = compute_perplexity(model, tokenizer, sent)
        results.append((sent, ppl))
        print(f"  PPL = {ppl:8.2f} | {sent}")

    # Rank by perplexity
    results.sort(key=lambda x: x[1])
    print(f"\n  Ranked (lowest to highest perplexity):")
    for i, (sent, ppl) in enumerate(results, 1):
        print(f"  {i}. PPL = {ppl:8.2f} | {sent}")


# -- Autoregressive Visualization ---------------------------------------------

def visualize_token_probabilities(
    model: GPT2LMHeadModel,
    tokenizer: GPT2Tokenizer,
    prefix: str,
    top_k: int = 10,
) -> None:
    """
    Visualize the probability distribution over the next token.
    Shows the top-k most likely tokens and their probabilities.
    """
    print(f"\n{'='*70}")
    print(f"Next-token probability distribution")
    print(f"Prefix: '{prefix}'")
    print(f"{'='*70}")

    inputs = tokenizer(prefix, return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits[:, -1, :]

    probs = F.softmax(logits, dim=-1).squeeze(0)
    top_probs, top_indices = probs.topk(top_k)

    print(f"  Top-{top_k} most likely next tokens:")
    for i in range(top_k):
        token_str = tokenizer.decode([top_indices[i].item()])
        print(f"  {i+1:2d}. '{token_str:10s}'  p = {top_probs[i].item():.4f}")

    # Show how probability mass is distributed
    total_top = top_probs.sum().item()
    print(f"\n  Probability mass in top-{top_k}: {total_top:.3f} ({total_top*100:.1f}%)")


# -- Main ----------------------------------------------------------------------

def main() -> None:
    """Run all demonstrations."""
    model, tokenizer = load_model()

    # 1. Step-by-step autoregressive generation
    print(f"\n{'#'*70}")
    print(f"# 1. Step-by-step autoregressive generation")
    print(f"{'#'*70}")
    step_by_step_generation(model, tokenizer, PROMPTS[0], n_tokens=8)

    # 2. Compare decoding strategies
    print(f"\n{'#'*70}")
    print(f"# 2. Decoding strategy comparison")
    print(f"{'#'*70}")
    compare_decoding_strategies(model, tokenizer, PROMPTS[1])

    # 3. Next-token probability visualization
    print(f"\n{'#'*70}")
    print(f"# 3. Next-token probability distribution visualization")
    print(f"{'#'*70}")
    visualize_token_probabilities(model, tokenizer, "The meaning of life is", top_k=10)

    # 4. Perplexity analysis
    print(f"\n{'#'*70}")
    print(f"# 4. Perplexity analysis")
    print(f"{'#'*70}")
    analyze_perplexity(model, tokenizer, PPL_SENTENCES)

    # 5. Compare all prompts with greedy/sampling strategies
    print(f"\n{'#'*70}")
    print(f"# 5. Quick generation across multiple prompts")
    print(f"{'#'*70}")
    for prompt in PROMPTS:
        gen = generate_greedy(model, tokenizer, prompt, max_new_tokens=30)
        print(f"\nPrompt: '{prompt}'")
        print(f"Greedy: {gen}")

    print(f"\n{'='*70}")
    print(f"Demo complete!")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
