"""
04-implement-transformer.py -- nanoGPT-Style Transformer from Scratch
=====================================================================

A from-scratch implementation of a decoder-only Transformer (GPT-style)
using PyTorch.  Trains on a tiny slice of Shakespeare and generates text.

Architecture (see 04-implement-transformer.md for the full concept map):

  1. TokenEmbedding + PositionalEncoding
  2. TransformerBlock x N  (Self-Attention -> FFN -> Add&Norm)
  3. LayerNorm -> Linear -> softmax
  4. Training loop on tiny Shakespeare (character-level)
  5. Autoregressive text generation with temperature sampling

Dependencies: torch >= 2.1.0, numpy

Usage:
    python 04-implement-transformer.py

Expected output: decreasing loss + generated Shakespeare-like text.
"""

import os
import sys
import math
import urllib.request

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.utils import clip_grad_norm_

# ---------------------------------------------------------------------------
# Device
# ---------------------------------------------------------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"[INFO] Device: {device}\n")

# ---------------------------------------------------------------------------
# 0. Hyper-parameters  (tiny GPT = nanoGPT)
# ---------------------------------------------------------------------------
BATCH_SIZE      = 32
CONTEXT_LENGTH  = 64       # T -- max sequence length the model sees
EMBED_DIM       = 64       # d_model -- token + position embedding size
N_HEAD          = 4        # number of attention heads
N_LAYER         = 2        # number of Transformer blocks stacked
FFN_HIDDEN      = 256      # hidden dimension of the feed-forward network
DROPOUT         = 0.1
LR              = 3e-3
NUM_EPOCHS      = 200
EVAL_EVERY      = 50       # generate text & print loss every N epochs
GEN_LEN         = 200      # number of characters to generate during sampling

# ---------------------------------------------------------------------------
# 1. Data: download tiny Shakespeare, character-level tokenisation
# ---------------------------------------------------------------------------
DATA_URL = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)
DATA_PATH = os.path.join(DATA_DIR, "tinyshakespeare.txt")

if not os.path.exists(DATA_PATH):
    print("[DATA] Downloading tiny Shakespeare ...")
    urllib.request.urlretrieve(DATA_URL, DATA_PATH)

with open(DATA_PATH, "r", encoding="utf-8") as f:
    full_text = f.read()

# Use only the first ~100 000 characters so training stays fast
train_text = full_text[:100_000]
print(f"[DATA] Using {len(train_text):,} characters from Shakespeare\n")

# Build character-level vocabulary
chars = sorted(list(set(train_text)))
vocab_size = len(chars)
char_to_idx = {ch: i for i, ch in enumerate(chars)}
idx_to_char = {i: ch for i, ch in enumerate(chars)}

print(f"[DATA] Vocabulary size: {vocab_size}")
print(f"[DATA] chars: {repr(''.join(chars))}\n")

# Encode the whole text
data = torch.tensor([char_to_idx[ch] for ch in train_text], dtype=torch.long)

# Train / validation split (90/10)
n = int(0.9 * len(data))
train_data = data[:n]
val_data   = data[n:]


def get_batch(split: str) -> tuple:
    """Sample a random mini-batch of (inputs, targets)."""
    src = train_data if split == "train" else val_data
    ix = torch.randint(len(src) - CONTEXT_LENGTH, (BATCH_SIZE,))
    x = torch.stack([src[i : i + CONTEXT_LENGTH] for i in ix])
    y = torch.stack([src[i + 1 : i + CONTEXT_LENGTH + 1] for i in ix])
    return x.to(device), y.to(device)


# ============================================================================
# 2. Transformer building blocks
# ============================================================================

class TokenEmbedding(nn.Module):
    """Map token indices to dense vectors.
    -------------------------------------------------
    Transformer Ch.1: Token Embedding -- each discrete token is projected
    into a continuous d_model-dimensional space.
    """
    def __init__(self):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, EMBED_DIM)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (B, T)  ->  out: (B, T, d_model)
        return self.embed(x)


class PositionalEncoding(nn.Module):
    """Sinusoidal positional encoding (non-learnable).
    -------------------------------------------------
    Transformer Ch.1: Positional Encoding -- injects sequence-order
    information via fixed sin/cos functions of different frequencies.

    PE(pos, 2i)   = sin(pos / 10000^{2i / d_model})
    PE(pos, 2i+1) = cos(pos / 10000^{2i / d_model})
    """
    def __init__(self):
        super().__init__()
        pe = torch.zeros(CONTEXT_LENGTH, EMBED_DIM)          # (T, d_model)
        position = torch.arange(0, CONTEXT_LENGTH, dtype=torch.float).unsqueeze(1)  # (T, 1)
        div_term = torch.exp(
            torch.arange(0, EMBED_DIM, 2).float() *
            (-math.log(10000.0) / EMBED_DIM)
        )                                                     # (d_model/2,)
        pe[:, 0::2] = torch.sin(position * div_term)         # even indices
        pe[:, 1::2] = torch.cos(position * div_term)         # odd  indices
        pe = pe.unsqueeze(0)                                  # (1, T, d_model)
        self.register_buffer("pe", pe)                        # not a parameter

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (B, T, d_model)
        return x + self.pe[:, : x.size(1), :]


class MultiHeadSelfAttention(nn.Module):
    """Scaled dot-product multi-head self-attention.
    -------------------------------------------------
    Transformer Ch.2: Multi-Head Attention.

    Q, K, V are all derived from the *same* input (hence "self"-attention).
    """
    def __init__(self):
        super().__init__()
        assert EMBED_DIM % N_HEAD == 0, "d_model must be divisible by n_head"
        self.head_dim = EMBED_DIM // N_HEAD  # d_k

        # Single fused projection for Q, K, V (efficient)
        self.qkv = nn.Linear(EMBED_DIM, 3 * EMBED_DIM, bias=False)
        self.proj = nn.Linear(EMBED_DIM, EMBED_DIM, bias=False)
        self.dropout = nn.Dropout(DROPOUT)

        # Causal mask (prevents attending to future positions)
        mask = torch.tril(torch.ones(CONTEXT_LENGTH, CONTEXT_LENGTH)).view(
            1, 1, CONTEXT_LENGTH, CONTEXT_LENGTH
        )
        self.register_buffer("mask", mask)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        B, T, C = x.shape  # batch, seq_len, d_model

        # 1. Project to Q, K, V  (B, T, 3*d_model) -> split -> 3x(B, T, d_model)
        qkv = self.qkv(x)
        q, k, v = qkv.chunk(3, dim=-1)

        # 2. Reshape for multi-head: (B, T, d_model) -> (B, n_head, T, d_k)
        q = q.view(B, T, N_HEAD, self.head_dim).transpose(1, 2)
        k = k.view(B, T, N_HEAD, self.head_dim).transpose(1, 2)
        v = v.view(B, T, N_HEAD, self.head_dim).transpose(1, 2)

        # 3. Scaled dot-product attention  (Eq.1 in Transformer paper)
        #    Attention(Q,K,V) = softmax(Q K^T / sqrt(d_k)) V
        attn = (q @ k.transpose(-2, -1)) * (1.0 / math.sqrt(self.head_dim))
        # Apply causal mask: positions with mask == 0 get -inf before softmax
        attn = attn.masked_fill(self.mask[:, :, :T, :T] == 0, float("-inf"))
        attn = F.softmax(attn, dim=-1)
        attn = self.dropout(attn)

        # 4. Weighted sum of values
        out = attn @ v                                       # (B, n_head, T, d_k)

        # 5. Concatenate heads and project back to d_model
        out = out.transpose(1, 2).contiguous().view(B, T, C)
        out = self.proj(out)
        return out


class FeedForward(nn.Module):
    """Position-wise Feed-Forward Network (FFN).
    -------------------------------------------------
    Transformer Ch.2: FFN -- two linear layers with a GELU activation.

    FFN(x) = GELU(x W_1 + b_1) W_2 + b_2
    """
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(EMBED_DIM, FFN_HIDDEN),
            nn.GELU(),                         # GELU ~ smooth ReLU
            nn.Linear(FFN_HIDDEN, EMBED_DIM),
            nn.Dropout(DROPOUT),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


class TransformerBlock(nn.Module):
    """One Transformer block: Self-Attention -> Add&Norm -> FFN -> Add&Norm.
    -------------------------------------------------
    Transformer Ch.2: The complete block architecture.

    Every sub-layer (attention, FFN) is wrapped with:
        output = LayerNorm(x + sublayer(x))
    """
    def __init__(self):
        super().__init__()
        self.attn  = MultiHeadSelfAttention()
        self.ffn   = FeedForward()
        self.ln1   = nn.LayerNorm(EMBED_DIM)
        self.ln2   = nn.LayerNorm(EMBED_DIM)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Pre-LayerNorm variant (more stable for training)
        x = x + self.attn(self.ln1(x))   # Self-Attention -> residual
        x = x + self.ffn(self.ln2(x))    # FFN -> residual
        return x


# ============================================================================
# 3. Full Transformer Model  (decoder-only, GPT-style)
# ============================================================================

class TransformerLM(nn.Module):
    """Decoder-only Transformer language model.

    Architecture (from bottom to top):
        TokenEmbedding -> PositionalEncoding
        -> TransformerBlock x N_LAYER
        -> LayerNorm -> Linear(vocab_size) -> softmax

    This is a **causal** (autoregressive) language model: each position
    can only attend to itself and previous positions via the causal mask.
    """
    def __init__(self):
        super().__init__()
        self.token_embed  = TokenEmbedding()
        self.pos_embed    = PositionalEncoding()
        self.blocks       = nn.ModuleList([
            TransformerBlock() for _ in range(N_LAYER)
        ])
        self.ln_final     = nn.LayerNorm(EMBED_DIM)
        self.lm_head      = nn.Linear(EMBED_DIM, vocab_size, bias=False)

        # Tie the embedding and the output projection weights (weight tying)
        # This is a common trick in language models (Press & Wolf 2017)
        self.token_embed.embed.weight = self.lm_head.weight

        # Initialise parameters
        self.apply(self._init_weights)

    @staticmethod
    def _init_weights(module: nn.Module):
        if isinstance(module, nn.Linear):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.bias is not None:
                torch.nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)

    def forward(self, idx: torch.Tensor) -> torch.Tensor:
        """
        Args:
            idx: (B, T) -- token indices
        Returns:
            logits: (B, T, vocab_size)
        """
        x = self.token_embed(idx)       # (B, T, d_model)
        x = self.pos_embed(x)           # (B, T, d_model)
        for block in self.blocks:
            x = block(x)
        x = self.ln_final(x)            # (B, T, d_model)
        logits = self.lm_head(x)        # (B, T, vocab_size)
        return logits

    @torch.no_grad()
    def generate(self, idx: torch.Tensor, max_new_tokens: int,
                 temperature: float = 1.0) -> torch.Tensor:
        """Autoregressive generation.

        At each step, feed the model its own prediction as the next input.
        This is the "greedy / sampling" loop described in Transformer Ch.4.
        """
        self.eval()
        for _ in range(max_new_tokens):
            # Crop to CONTEXT_LENGTH (model's max context window)
            idx_cond = idx[:, -CONTEXT_LENGTH:]
            logits = self(idx_cond)                     # (B, T, vocab_size)
            logits = logits[:, -1, :] / temperature      # last time-step only
            probs  = F.softmax(logits, dim=-1)           # (B, vocab_size)
            next_idx = torch.multinomial(probs, num_samples=1)  # (B, 1)
            idx = torch.cat((idx, next_idx), dim=1)
        return idx


# ============================================================================
# 4. Instantiate model, loss, optimiser
# ============================================================================
model = TransformerLM().to(device)
total_params = sum(p.numel() for p in model.parameters())
print(f"[MODEL] TransformerLM -- {total_params:,} parameters")
print(f"[MODEL] {N_LAYER} blocks, {N_HEAD} heads, d_model={EMBED_DIM}\n")

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.AdamW(model.parameters(), lr=LR)

# ---------------------------------------------------------------------------
# 5. Text generation utility
# ---------------------------------------------------------------------------
@torch.no_grad()
def sample_text(model: nn.Module, seed: str, length: int = GEN_LEN,
                temperature: float = 0.8) -> str:
    """Generate text starting from a seed string."""
    model.eval()
    # Encode seed
    seed_indices = [char_to_idx.get(ch, 0) for ch in seed]
    context = torch.tensor(seed_indices, dtype=torch.long, device=device).unsqueeze(0)
    out = model.generate(context, length, temperature=temperature)
    generated = out[0].tolist()
    return "".join(idx_to_char[i] for i in generated)


# ============================================================================
# 6. Training loop
# ============================================================================
print("=" * 60)
print("TRAINING STARTED")
print("=" * 60)

for epoch in range(1, NUM_EPOCHS + 1):
    model.train()
    total_loss = 0.0
    num_batches = 0

    # Each "epoch" = a fixed number of batches (fast)
    for _ in range(50):  # 50 batches per "epoch" =~ 1600 tokens seen
        x, y = get_batch("train")
        logits = model(x)                             # (B, T, vocab_size)
        loss = criterion(logits.view(-1, vocab_size), y.view(-1))

        optimizer.zero_grad()
        loss.backward()
        clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()

        total_loss += loss.item()
        num_batches += 1

    avg_loss = total_loss / num_batches

    # Print training loss and generate samples at checkpoints
    if epoch == 1 or epoch % EVAL_EVERY == 0 or epoch == NUM_EPOCHS:
        # Validation loss
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for _ in range(20):
                x, y = get_batch("val")
                logits = model(x)
                loss = criterion(logits.view(-1, vocab_size), y.view(-1))
                val_loss += loss.item()
        val_loss /= 20

        print(f"\n[Epoch {epoch:3d}/{NUM_EPOCHS}]  "
              f"train loss: {avg_loss:.4f}  val loss: {val_loss:.4f}  "
              f"perplexity: {math.exp(avg_loss):.1f}")

        # Generate samples at different temperatures
        seed = "ROMEO:\n"
        for temp, label in [(0.5, "conservative"), (0.8, "balanced"), (1.2, "creative")]:
            gen_text = sample_text(model, seed, length=GEN_LEN, temperature=temp)
            # Show only the generated part (after seed)
            new_part = gen_text[len(seed):]
            print(f"  T={temp:.1f} ({label}): {new_part[:120]}...")
        print()


print("\n" + "=" * 60)
print("TRAINING COMPLETE")
print("=" * 60)

# ---------------------------------------------------------------------------
# 7. Final demonstration: longer generated samples
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("FINAL TEXT SAMPLES")
print("=" * 60)

seeds = [
    "ROMEO:\n",
    "JULIET:\n",
    "KING:\n",
    "But, soft! what light",
]

for seed in seeds:
    print(f"\n-- Seed: {repr(seed)} --")
    for temp in [0.6, 1.0]:
        gen_text = sample_text(model, seed, length=250, temperature=temp)
        full = gen_text
        print(f"\n  [T={temp:.1f}]")
        # Print with line breaks for readability
        words = full.split()
        line = ""
        for w in words:
            if len(line) + len(w) > 72:
                print(f"    {line}")
                line = w
            else:
                line = f"{line} {w}" if line else w
        if line:
            print(f"    {line}")

print("\n[DONE] Transformer implementation complete.")
