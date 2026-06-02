"""
llm_inference.py -- Large Language Model Inference Demonstration
================================================================

Demonstrates core LLM inference concepts using GPT-2 (124M):

  1. Text generation with different decoding strategies
     - Temperature sampling
     - Top-k sampling
     - Top-p (nucleus) sampling
  2. KV cache analysis (with vs. without cache)
  3. Prompt formatting for instruction-tuned models
  4. Simplified RLHF simulation (reward model + PPO surrogate loss)

Dependencies: torch >= 2.1.0, transformers >= 4.36.0, numpy >= 1.24.0

Usage:
    python llm_inference.py

Expected output:
    - Generated text samples under different settings
    - Inference speed comparison (with/without KV cache)
    - Prompt-formatted outputs
    - Reward scores from simulated RLHF
"""

import math
import time
from typing import Optional

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    AutoConfig,
)

# ---------------------------------------------------------------------------
# Device and reproducibility
# ---------------------------------------------------------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"[INFO] Device: {device}")
print(f"[INFO] PyTorch version: {torch.__version__}")
print()

torch.manual_seed(42)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(42)

MODEL_NAME = "gpt2"

# ===================================================================
# 1. GENERATION WITH DIFFERENT DECODING STRATEGIES
# ===================================================================
print("=" * 65)
print("1. TEXT GENERATION -- Decoding Strategies")
print("=" * 65)

print(f"\n  Loading model: {MODEL_NAME}")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(MODEL_NAME).to(device)
model.eval()
print(f"  Model parameters: {sum(p.numel() for p in model.parameters()):,}")


@torch.no_grad()
def generate(
    prompt: str,
    max_new_tokens: int = 30,
    temperature: float = 1.0,
    top_k: Optional[int] = None,
    top_p: Optional[float] = None,
    use_cache: bool = True,
) -> tuple[str, float, list[float]]:
    """Generate text from a prompt with specified decoding strategy."""
    model.eval()
    input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)
    prompt_len = input_ids.shape[1]
    all_logprobs = []
    start = time.perf_counter()
    past_key_values = None

    for _ in range(max_new_tokens):
        if past_key_values is None:
            outputs = model(input_ids, use_cache=use_cache)
        else:
            outputs = model(
                input_ids[:, -1:], past_key_values=past_key_values, use_cache=use_cache
            )

        logits = outputs.logits[:, -1, :]
        scaled_logits = logits / temperature

        # Top-k filtering
        if top_k is not None and top_k > 0:
            values, _ = torch.topk(scaled_logits, top_k, dim=-1)
            threshold = values[:, -1].unsqueeze(-1)
            scaled_logits[scaled_logits < threshold] = -float("Inf")

        # Top-p (nucleus) filtering
        if top_p is not None and top_p < 1.0:
            sorted_logits, sorted_indices = torch.sort(
                scaled_logits, descending=True, dim=-1
            )
            cum_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)
            sorted_mask = cum_probs - F.softmax(sorted_logits, dim=-1) >= top_p
            sorted_logits[sorted_mask] = -float("Inf")
            scaled_logits = sorted_logits.scatter(1, sorted_indices, sorted_logits)

        probs = F.softmax(scaled_logits, dim=-1)
        next_token = torch.multinomial(probs, num_samples=1)

        log_probs = F.log_softmax(logits, dim=-1)
        all_logprobs.append(log_probs[0, next_token[0, 0]].item())

        input_ids = torch.cat([input_ids, next_token], dim=-1)
        past_key_values = outputs.past_key_values

        if next_token.item() == tokenizer.eos_token_id:
            break

    elapsed = time.perf_counter() - start
    new_tokens = input_ids.shape[1] - prompt_len
    tokens_per_sec = new_tokens / elapsed if elapsed > 0 else 0.0
    generated = tokenizer.decode(input_ids[0], skip_special_tokens=True)
    return generated, tokens_per_sec, all_logprobs


# --- 1a. Greedy (temperature -> 0) ---
print("\n  --- 1a. Greedy Decoding (T->0) ---")
text, speed, _ = generate("The future of AI is", temperature=0.1, max_new_tokens=30)
print(f"  Speed: {speed:.1f} tok/s")
print(f"  Output: {text}")

# --- 1b. Temperature sampling ---
print("\n  --- 1b. Temperature Sampling (T=0.8) ---")
text, speed, _ = generate("The future of AI is", temperature=0.8, max_new_tokens=30)
print(f"  Speed: {speed:.1f} tok/s")
print(f"  Output: {text}")

# --- 1c. High temperature ---
print("\n  --- 1c. High Temperature (T=1.5) ---")
text, speed, _ = generate("The future of AI is", temperature=1.5, max_new_tokens=30)
print(f"  Speed: {speed:.1f} tok/s")
print(f"  Output: {text}")

# --- 1d. Top-k sampling ---
print("\n  --- 1d. Top-k Sampling (k=40, T=0.9) ---")
text, speed, _ = generate("The future of AI is", temperature=0.9, top_k=40, max_new_tokens=30)
print(f"  Speed: {speed:.1f} tok/s")
print(f"  Output: {text}")

# --- 1e. Top-p (nucleus) sampling ---
print("\n  --- 1e. Top-p Sampling (p=0.9, T=0.9) ---")
text, speed, _ = generate("The future of AI is", temperature=0.9, top_p=0.9, max_new_tokens=30)
print(f"  Speed: {speed:.1f} tok/s")
print(f"  Output: {text}")

# --- 1f. Combined top-k + top-p ---
print("\n  --- 1f. Top-k (50) + Top-p (0.95) ---")
text, speed, _ = generate("The future of AI is", temperature=0.8, top_k=50, top_p=0.95, max_new_tokens=30)
print(f"  Speed: {speed:.1f} tok/s")
print(f"  Output: {text}")


# ===================================================================
# 2. KV CACHE ANALYSIS
# ===================================================================
print("\n" + "=" * 65)
print("2. KV CACHE ANALYSIS -- With vs. Without Cache")
print("=" * 65)

PROMPT = "In the beginning, the universe was"
NEW_TOKENS = 50

def generate_no_cache(prompt: str, max_new_tokens: int = NEW_TOKENS) -> tuple[float, int]:
    """Generate tokens one-by-one, recomputing full attention each time."""
    model.eval()
    input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)
    prompt_len = input_ids.shape[1]
    start = time.perf_counter()
    for _ in range(max_new_tokens):
        outputs = model(input_ids, use_cache=False)
        logits = outputs.logits[:, -1, :]
        probs = F.softmax(logits / 0.9, dim=-1)
        next_token = torch.multinomial(probs, num_samples=1)
        input_ids = torch.cat([input_ids, next_token], dim=-1)
        if next_token.item() == tokenizer.eos_token_id:
            break
    elapsed = time.perf_counter() - start
    return elapsed, input_ids.shape[1] - prompt_len

def generate_with_cache(prompt: str, max_new_tokens: int = NEW_TOKENS) -> tuple[float, int]:
    """Generate using KV cache -- O(n) per step instead of O(n^2)."""
    model.eval()
    input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)
    prompt_len = input_ids.shape[1]
    past_key_values = None
    start = time.perf_counter()
    for _ in range(max_new_tokens):
        if past_key_values is None:
            outputs = model(input_ids, use_cache=True)
        else:
            outputs = model(
                input_ids[:, -1:], past_key_values=past_key_values, use_cache=True
            )
        logits = outputs.logits[:, -1, :]
        probs = F.softmax(logits / 0.9, dim=-1)
        next_token = torch.multinomial(probs, num_samples=1)
        input_ids = torch.cat([input_ids, next_token], dim=-1)
        past_key_values = outputs.past_key_values
        if next_token.item() == tokenizer.eos_token_id:
            break
    elapsed = time.perf_counter() - start
    return elapsed, input_ids.shape[1] - prompt_len

print(f"\n  Prompt: \"{PROMPT}\"")
print(f"  Target new tokens: ~{NEW_TOKENS}")

# Run multiple trials
trials = 3
times_no_cache, times_with_cache = [], []
tokens_no_cache, tokens_with_cache = [], []

for _ in range(trials):
    t_no, n_no = generate_no_cache(PROMPT)
    times_no_cache.append(t_no)
    tokens_no_cache.append(n_no)
    t_wc, n_wc = generate_with_cache(PROMPT)
    times_with_cache.append(t_wc)
    tokens_with_cache.append(n_wc)

avg_no_cache = np.mean(times_no_cache)
avg_with_cache = np.mean(times_with_cache)
avg_tokens_no = np.mean(tokens_no_cache)
avg_tokens_wc = np.mean(tokens_with_cache)

print(f"\n  {'Method':<20} {'Avg Time':<12} {'Avg Tokens':<12} {'Tok/s':<10}")
print(f"  {'-'*20} {'-'*12} {'-'*12} {'-'*10}")
print(f"  {'No KV Cache':<20} {avg_no_cache:<12.3f}s {avg_tokens_no:<12.0f} {avg_tokens_no/avg_no_cache:<10.1f}")
print(f"  {'With KV Cache':<20} {avg_with_cache:<12.3f}s {avg_tokens_wc:<12.0f} {avg_tokens_wc/avg_with_cache:<10.1f}")
speedup = avg_no_cache / avg_with_cache
print(f"\n  Speedup from KV cache: {speedup:.1f}x")

print(f"\n  --- Complexity Analysis ---")
print(f"  Without cache: O(n^2 * d_h) per step (full attention recomputed)")
print(f"  With cache:    O(n * d_h) per step   (only new token's attention)")
print(f"  Theoretical speedup for n={NEW_TOKENS}: ~{NEW_TOKENS//2}x per layer")


# ===================================================================
# 3. PROMPT FORMATTING
# ===================================================================
print("\n" + "=" * 65)
print("3. PROMPT FORMATTING -- Instruction-Tuned Style")
print("=" * 65)

def format_prompt_chat(instruction: str) -> str:
    """Format a prompt in ChatML style."""
    return (
        f"<|im_start|>system\nYou are a helpful assistant.<|im_end|>\n"
        f"<|im_start|>user\n{instruction}<|im_end|>\n"
        f"<|im_start|>assistant\n"
    )

def format_prompt_llama2(instruction: str) -> str:
    """Format prompt in LLaMA-2 chat style."""
    return f"<s>[INST] {instruction} [/INST] "

prompts = [
    "Explain what a neural network is in one sentence.",
    "Write a haiku about artificial intelligence.",
    "What is the capital of France?",
]

print(f"\n  --- ChatML-style formatting ---")
for i, inst in enumerate(prompts):
    fmt = format_prompt_chat(inst)
    display = fmt[:100] + "..." if len(fmt) > 100 else fmt
    print(f"\n  Prompt {i+1}: \"{inst}\"")
    print(f"  Formatted: {repr(display)}")
    out, speed, _ = generate(inst, temperature=0.7, top_p=0.9, max_new_tokens=40)
    print(f"  Response: {out[len(inst):].strip()}")
    print(f"  Speed: {speed:.1f} tok/s")

print(f"\n  --- LLaMA-2-style formatting ---")
for i, inst in enumerate(prompts):
    fmt = format_prompt_llama2(inst)
    display = fmt[:100] + "..." if len(fmt) > 100 else fmt
    print(f"\n  Prompt {i+1}: \"{inst}\"")
    print(f"  Formatted: {repr(display)}")


# ===================================================================
# 4. SIMPLIFIED RLHF SIMULATION
# ===================================================================
print("\n" + "=" * 65)
print("4. SIMPLIFIED RLHF SIMULATION")
print("=" * 65)

print("\n  --- Step 1: SFT (simulated with one epoch) ---")
sft_data = [
    ("The capital of France is", " Paris."),
    ("Water freezes at", " 0 degrees Celsius."),
    ("The square root of 144 is", " 12."),
    ("Python is a", " programming language."),
    ("The Earth orbits the", " Sun."),
]
print(f"  SFT dataset: {len(sft_data)} (prompt, completion) pairs")

model.train()
optimizer_sft = torch.optim.AdamW(model.parameters(), lr=5e-5)
sft_loss_total = 0.0

for prompt_text, target_text in sft_data:
    full_text = prompt_text + target_text
    input_ids = tokenizer.encode(full_text, return_tensors="pt").to(device)
    labels = input_ids.clone()
    prompt_len = len(tokenizer.encode(prompt_text))
    labels[:, :prompt_len] = -100  # ignore prompt in loss
    outputs = model(input_ids, labels=labels)
    loss = outputs.loss
    sft_loss_total += loss.item()
    optimizer_sft.zero_grad()
    loss.backward()
    optimizer_sft.step()

avg_sft_loss = sft_loss_total / len(sft_data)
print(f"  SFT loss (after 1 epoch): {avg_sft_loss:.4f}")


print("\n  --- Step 2: Reward Model ---")

class RewardModel(nn.Module):
    """GPT-2 backbone + linear head for scalar reward."""
    def __init__(self):
        super().__init__()
        config = AutoConfig.from_pretrained(MODEL_NAME)
        self.backbone = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
        hidden_size = config.n_embd
        self.reward_head = nn.Linear(hidden_size, 1)

    def forward(self, input_ids: torch.Tensor) -> torch.Tensor:
        outputs = self.backbone(input_ids, output_hidden_states=True)
        last_hidden = outputs.hidden_states[-1][:, -1, :]
        reward = self.reward_head(last_hidden)
        return reward.squeeze(-1)

reward_model = RewardModel().to(device)
reward_model.eval()
print(f"  Reward model params: {sum(p.numel() for p in reward_model.parameters()):,}")

# For demonstration, define a heuristic reward function
POSITIVE_KEYWORDS = ["good", "correct", "Paris", "Python", "sun", "programming"]
NEGATIVE_KEYWORDS = ["wrong", "bad", "incorrect", "error", "never"]

def heuristic_reward(text: str) -> float:
    """Heuristic reward simulating what a trained reward model would output."""
    text_lower = text.lower()
    reward = 0.0
    for kw in POSITIVE_KEYWORDS:
        if kw.lower() in text_lower:
            reward += 0.5
    for kw in NEGATIVE_KEYWORDS:
        if kw.lower() in text_lower:
            reward -= 0.5
    words = text.split()
    reward -= max(0, len(words) - 20) * 0.1
    return reward

test_prompts = [
    "The best programming language is",
    "The meaning of life is",
    "Machine learning is",
]

print(f"\n  Scoring generated responses with heuristic reward:")
for p in test_prompts:
    gen_text, _, _ = generate(p, temperature=0.8, top_p=0.9, max_new_tokens=20)
    response = gen_text[len(p):].strip()
    reward = heuristic_reward(response)

    # Also get reward model score (random init, but shows the API)
    input_ids = tokenizer.encode(gen_text, return_tensors="pt").to(device)
    with torch.no_grad():
        rm_score = reward_model(input_ids).item()

    print(f"\n  Prompt: \"{p}\"")
    print(f"  Response: \"{response[:60]}...\"")
    print(f"  Heuristic Reward: {reward:+.2f}")
    print(f"  Reward Model Score: {rm_score:+.4f}")


print("\n  --- Step 3: PPO (Proximal Policy Optimization, one update) ---")
print(f"\n  Performing one PPO update step...")

# Reference policy (copy of original model)
ref_model = AutoModelForCausalLM.from_pretrained(MODEL_NAME).to(device)
ref_model.eval()

# Policy model = current model (after SFT)
policy_model = model
policy_model.train()

PPO_EPS = 0.2        # clipping epsilon
PPO_LR = 1e-5
KL_PENALTY = 0.01    # KL divergence coefficient

ppo_optimizer = torch.optim.AdamW(policy_model.parameters(), lr=PPO_LR)
ppo_prompt = "Q: What is 2+2? A:"
input_ids = tokenizer.encode(ppo_prompt, return_tensors="pt").to(device)

# Generate response with current policy (no grad for generation step)
with torch.no_grad():
    gen_ids = input_ids.clone()
    past = None
    for _ in range(10):
        if past is None:
            out = policy_model(gen_ids, use_cache=True)
        else:
            out = policy_model(
                gen_ids[:, -1:], past_key_values=past, use_cache=True
            )
        logits = out.logits[:, -1, :]
        probs = F.softmax(logits / 1.0, dim=-1)
        next_tok = torch.multinomial(probs, 1)
        gen_ids = torch.cat([gen_ids, next_tok], dim=-1)
        past = out.past_key_values

response = tokenizer.decode(gen_ids[0], skip_special_tokens=True)
print(f"  Prompt: {ppo_prompt}")
print(f"  Response: {response}")

# Compute reference log-probs (no grad needed)
def get_log_probs(model: nn.Module, input_ids: torch.Tensor, requires_grad: bool = False) -> torch.Tensor:
    """Get per-token log-probabilities."""
    if not requires_grad:
        with torch.no_grad():
            outputs = model(input_ids)
            logits = outputs.logits[:, :-1, :]
            target_ids = input_ids[:, 1:]
            log_probs = F.log_softmax(logits, dim=-1)
            token_log_probs = log_probs.gather(-1, target_ids.unsqueeze(-1)).squeeze(-1)
        return token_log_probs
    else:
        outputs = model(input_ids)
        logits = outputs.logits[:, :-1, :]
        target_ids = input_ids[:, 1:]
        log_probs = F.log_softmax(logits, dim=-1)
        token_log_probs = log_probs.gather(-1, target_ids.unsqueeze(-1)).squeeze(-1)
        return token_log_probs

with torch.no_grad():
    ref_lp = get_log_probs(ref_model, gen_ids)

# Policy log-probs with gradients enabled
policy_lp = get_log_probs(policy_model, gen_ids, requires_grad=True)

full_text = tokenizer.decode(gen_ids[0], skip_special_tokens=True)
reward_val = heuristic_reward(full_text)
# Use reward as advantage (no value baseline in this simplified demo)
advantage = torch.tensor([[reward_val]], device=device)

# PPO clipped surrogate objective:
# L^{CLIP}(theta) = E[ min(r_t(theta) * A_t, clip(r_t(theta), 1-eps, 1+eps) * A_t) ]
ratio = torch.exp(policy_lp - ref_lp)
surr1 = ratio * advantage
surr2 = torch.clamp(ratio, 1.0 - PPO_EPS, 1.0 + PPO_EPS) * advantage
clip_loss = -torch.min(surr1, surr2).mean()

# KL penalty to keep policy close to reference
kl_div = (policy_lp - ref_lp).mean()
ppo_loss = clip_loss + KL_PENALTY * kl_div

print(f"  Reward: {reward_val:+.2f}")
print(f"  Probability ratio (mean): {ratio.mean().item():.4f}")
print(f"  KL divergence: {kl_div.item():.4f}")
print(f"  PPO loss: {ppo_loss.item():.4f}")

# Gradient-based update
ppo_optimizer.zero_grad()
ppo_loss.backward()
torch.nn.utils.clip_grad_norm_(policy_model.parameters(), 1.0)
ppo_optimizer.step()
print(f"  PPO update complete.")


# ===================================================================
# SUMMARY
# ===================================================================
print("\n" + "=" * 65)
print("SUMMARY")
print("=" * 65)
print("""
  Demonstrated concepts:
    1. Decoding strategies - temperature, top-k, top-p sampling
    2. KV cache - O(n) vs O(n^2) per-step complexity
    3. Prompt formatting - ChatML and LLaMA-2 style templates
    4. RLHF pipeline - SFT, Reward Model, PPO update

  Key takeaways:
    - Temperature controls randomness: low=greedy, high=diverse
    - Top-k filters to the k most probable tokens
    - Top-p (nucleus) adaptively selects a variable-size candidate set
    - KV cache reduces per-step complexity from O(n^2) to O(n)
    - RLHF aligns LLMs via: SFT, Reward Model, PPO clipped surrogate
""")
print(f"[INFO] All demonstrations completed successfully.")
