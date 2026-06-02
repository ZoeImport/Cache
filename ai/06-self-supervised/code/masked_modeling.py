"""
Masked Modeling Demo: Mini BERT MLM
====================================
Demonstrates Masked Language Model (MLM) pre-training with a tiny BERT.
Shows masking strategy, training loop, loss curve, and token predictions.

Concepts covered:
  - BERT-style masking (80% [MASK], 10% random, 10% unchanged)
  - MLM training with cross-entropy loss on masked positions only
  - Visual comparison of MLM vs Autoregressive (GPT-style) prediction
"""

import math
import os
import warnings
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset

warnings.filterwarnings("ignore")

# Save outputs in the same directory as this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ──────────────────────────────────────────────
# Device
# ──────────────────────────────────────────────
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}\n")

# ──────────────────────────────────────────────
# 1. Tiny Vocabulary & Toy Corpus
# ──────────────────────────────────────────────
VOCAB = [
    "[PAD]", "[CLS]", "[SEP]", "[MASK]", "[UNK]",
    "the", "cat", "dog", "sat", "ran", "on", "mat",
    "is", "in", "garden", "sun", "shines", "brightly",
    "sky", "a", "bird", "flies", "fish", "swims",
    "apple", "eats", "big", "small", "red", "blue",
]
VOCAB_SIZE = len(VOCAB)
PAD_IDX = VOCAB.index("[PAD]")
CLS_IDX = VOCAB.index("[CLS]")
SEP_IDX = VOCAB.index("[SEP]")
MASK_IDX = VOCAB.index("[MASK]")

word2idx = {w: i for i, w in enumerate(VOCAB)}
idx2word = {i: w for w, i in word2idx.items()}

# Toy corpus: 6 short sentences
CORPUS = [
    "the cat sat on the mat",
    "the dog ran in the garden",
    "the sun shines brightly in the sky",
    "a bird flies in the sky",
    "a fish swims in the water",
    "the cat eats a big red apple",
]


SPECIAL_TOKENS_SET = {"[CLS]", "[SEP]", "[MASK]", "[PAD]", "[UNK]"}


def tokenize(sentence: str) -> list[int]:
    """Convert a sentence to token indices with [CLS] and [SEP].
    Special tokens like [MASK] are kept as-is (not lowercased)."""
    raw_tokens = sentence.split()
    tokens = []
    for t in raw_tokens:
        if t in SPECIAL_TOKENS_SET:
            tokens.append(t)
        else:
            tokens.append(t.lower())
    ids = [CLS_IDX] + [word2idx.get(t, word2idx["[UNK]"]) for t in tokens] + [SEP_IDX]
    return ids


MAX_LEN = 16  # fixed sequence length (pad/truncate)


class TinyTextDataset(Dataset):
    """Simple dataset from toy corpus, tokenized and padded."""

    def __init__(self, corpus: list[str], max_len: int = MAX_LEN):
        self.data = []
        self.max_len = max_len
        for sent in corpus:
            ids = tokenize(sent)
            if len(ids) > max_len:
                ids = ids[:max_len - 1] + [SEP_IDX]  # ensure [SEP] at end
            pad_len = max_len - len(ids)
            ids = ids + [PAD_IDX] * pad_len
            self.data.append(torch.tensor(ids, dtype=torch.long))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]


dataset = TinyTextDataset(CORPUS, MAX_LEN)
dataloader = DataLoader(dataset, batch_size=2, shuffle=True)

# ──────────────────────────────────────────────
# 2. BERT-style Masking Function
# ──────────────────────────────────────────────

def apply_mlm_mask(input_ids: torch.Tensor, mask_prob: float = 0.15,
                   vocab_size: int = VOCAB_SIZE,
                   mask_idx: int = MASK_IDX,
                   pad_idx: int = PAD_IDX,
                   special_tokens: set = None) -> tuple[torch.Tensor, torch.Tensor]:
    """
    Apply BERT-style masking:
      - 15% of tokens selected for masking
      - Among selected: 80% -> [MASK], 10% -> random, 10% -> unchanged
    Returns (masked_ids, labels) where labels=-100 for non-masked positions.
    """
    if special_tokens is None:
        special_tokens = {CLS_IDX, SEP_IDX, pad_idx}

    labels = input_ids.clone()
    masked = input_ids.clone()
    batch_size, seq_len = input_ids.shape

    # Create mask: select positions (excluding special tokens)
    prob = torch.full((batch_size, seq_len), mask_prob, device=input_ids.device)
    for st in special_tokens:
        prob[input_ids == st] = 0.0

    # Sample which positions to mask
    selected_mask = torch.bernoulli(prob).bool()
    labels[~selected_mask] = -100  # -100 is ignored by CrossEntropyLoss

    # Among selected:
    # 80% -> [MASK]
    mask_rand = torch.rand_like(input_ids, dtype=torch.float)
    mask_mask = (mask_rand < 0.8) & selected_mask
    masked[mask_mask] = mask_idx

    # 10% -> random token
    random_mask = (mask_rand >= 0.8) & (mask_rand < 0.9) & selected_mask
    random_tokens = torch.randint(vocab_size, input_ids.shape, device=input_ids.device)
    masked[random_mask] = random_tokens[random_mask]

    # 10% -> unchanged (already in `masked` from input_ids)

    return masked, labels


# ──────────────────────────────────────────────
# 3. Tiny BERT Model
# ──────────────────────────────────────────────

class TinyBertMLM(nn.Module):
    """A minimal BERT-style model for MLM demonstration."""

    def __init__(self, vocab_size: int, d_model: int = 128, nhead: int = 4,
                 num_layers: int = 4, dim_feedforward: int = 256, max_len: int = 64):
        super().__init__()
        self.d_model = d_model
        self.token_embedding = nn.Embedding(vocab_size, d_model, padding_idx=PAD_IDX)
        self.pos_embedding = nn.Embedding(max_len, d_model)

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model, nhead=nhead, dim_feedforward=dim_feedforward,
            dropout=0.1, activation="gelu", batch_first=True, norm_first=True,
        )
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.ln_head = nn.LayerNorm(d_model)
        self.head = nn.Linear(d_model, vocab_size)

        self._init_weights()

    def _init_weights(self):
        for p in self.parameters():
            if p.dim() > 1:
                nn.init.xavier_uniform_(p)

    def forward(self, input_ids: torch.Tensor) -> torch.Tensor:
        B, S = input_ids.shape
        positions = torch.arange(S, device=input_ids.device).unsqueeze(0)
        x = self.token_embedding(input_ids) * math.sqrt(self.d_model)
        x = x + self.pos_embedding(positions)
        x = self.encoder(x)
        x = self.ln_head(x)
        logits = self.head(x)
        return logits


# ──────────────────────────────────────────────
# 4. Visualization Tools
# ──────────────────────────────────────────────

def show_mask_demo(sentence: str, model: TinyBertMLM = None):
    """Visualize masking: show original, masked, and predicted tokens."""
    ids = tokenize(sentence)
    orig_len = len(ids)
    if orig_len < MAX_LEN:
        ids = ids + [PAD_IDX] * (MAX_LEN - orig_len)
    input_tensor = torch.tensor([ids], dtype=torch.long, device=device)
    masked_tensor, labels = apply_mlm_mask(input_tensor)

    masked_words = [idx2word.get(int(mt), "?") for mt in masked_tensor[0]]
    orig_words = [idx2word.get(int(it), "?") for it in input_tensor[0]]

    print("=" * 70)
    print("Masking Strategy Visualization")
    print("=" * 70)
    print(f"Original : {' '.join(orig_words)}")
    print(f"Masked   : {' '.join(masked_words)}")

    if model is not None:
        model.eval()
        with torch.no_grad():
            logits = model(masked_tensor)
            probs = F.softmax(logits, dim=-1)
            preds = probs.argmax(dim=-1)
        print("Predicted: ", end="")
        pred_words = []
        for i, (mp, pred_idx) in enumerate(zip(masked_words, preds[0])):
            if mp == "[MASK]":
                p = float(probs[0, i, pred_idx])
                pred_words.append(f"{idx2word.get(int(pred_idx), '?')}({p:.2f})")
            else:
                pred_words.append(mp)
        print(" ".join(pred_words))

    mask_positions = (labels[0] != -100).nonzero(as_tuple=True)[0].tolist()
    print(f"Masked positions: {mask_positions}")
    print()


def visualize_attention_pattern():
    """Show the key difference between MLM (bidirectional) and autoregressive."""
    print("=" * 70)
    print("MLM vs Autoregressive: Attention Pattern Comparison")
    print("=" * 70)

    seq = ["The", "cat", "[MASK]", "on", "the", "mat"]
    n = len(seq)

    # MLM (bidirectional): each token attends to ALL tokens
    mlm_mask = np.ones((n, n))

    # Autoregressive (causal): each token attends only to itself + left tokens
    causal_mask = np.tril(np.ones((n, n)), k=0)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

    ax1.imshow(mlm_mask, cmap="Blues", vmin=0, vmax=1)
    ax1.set_title("MLM (BERT) - Bidirectional", fontsize=13, fontweight="bold")
    ax1.set_xticks(range(n))
    ax1.set_yticks(range(n))
    ax1.set_xticklabels(seq, fontsize=9)
    ax1.set_yticklabels(seq, fontsize=9)
    ax1.set_xlabel("Attends to (Keys)", fontsize=10)
    ax1.set_ylabel("Query position", fontsize=10)
    for i in range(n):
        for j in range(n):
            ax1.text(j, i, chr(10003), ha="center", va="center", fontsize=8,
                     color="white" if mlm_mask[i, j] else "black")

    ax2.imshow(causal_mask, cmap="Blues", vmin=0, vmax=1)
    ax2.set_title("Autoregressive (GPT) - Causal", fontsize=13, fontweight="bold")
    ax2.set_xticks(range(n))
    ax2.set_yticks(range(n))
    ax2.set_xticklabels(seq, fontsize=9)
    ax2.set_yticklabels(seq, fontsize=9)
    ax2.set_xlabel("Attends to (Keys)", fontsize=10)
    ax2.set_ylabel("Query position", fontsize=10)
    for i in range(n):
        for j in range(n):
            mark = chr(10003) if causal_mask[i, j] else chr(10007)
            ax2.text(j, i, mark, ha="center", va="center", fontsize=8,
                     color="white" if causal_mask[i, j] else "red")

    plt.tight_layout()
    save_path = os.path.join(SCRIPT_DIR, "attention_pattern_comparison.png")
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved attention pattern comparison to {save_path}\n")


# ──────────────────────────────────────────────
# 5. Training Loop
# ──────────────────────────────────────────────

def train_mlm(model: TinyBertMLM, dataloader: DataLoader,
              num_epochs: int = 100, lr: float = 3e-4):
    """Train the tiny BERT model on MLM task."""
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.01)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=num_epochs)
    losses = []

    print("=" * 70)
    print("MLM Training Loop")
    print("=" * 70)

    for epoch in range(1, num_epochs + 1):
        model.train()
        epoch_loss = 0.0
        num_batches = 0

        for batch in dataloader:
            batch = batch.to(device)
            masked_batch, labels = apply_mlm_mask(batch)

            logits = model(masked_batch)
            loss = F.cross_entropy(
                logits.view(-1, VOCAB_SIZE),
                labels.view(-1),
                ignore_index=-100,
            )

            # Skip if loss is NaN (protect against numerical instability)
            if torch.isnan(loss) or torch.isinf(loss):
                optimizer.zero_grad()
                continue

            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()

            epoch_loss += loss.item()
            num_batches += 1

        scheduler.step()
        avg_loss = epoch_loss / max(num_batches, 1) if num_batches > 0 else float("nan")
        losses.append(avg_loss)

        if epoch == 1 or epoch % 20 == 0 or epoch == num_epochs:
            print(f"  Epoch {epoch:3d}/{num_epochs} | Loss: {avg_loss:.4f}")

    # Plot loss curve
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(range(1, num_epochs + 1), losses, color="#4C72B0", linewidth=1.5)
    ax.set_xlabel("Epoch", fontsize=12)
    ax.set_ylabel("MLM Loss", fontsize=12)
    ax.set_title("MLM Training Loss Curve", fontsize=14, fontweight="bold")
    ax.grid(alpha=0.3)
    plt.tight_layout()
    save_path = os.path.join(SCRIPT_DIR, "mlm_loss_curve.png")
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"\nSaved loss curve to {save_path}")
    print(f"Final loss: {losses[-1]:.4f}\n")

    return losses


# ──────────────────────────────────────────────
# 6. Prediction Demonstration
# ──────────────────────────────────────────────

def show_predictions(model: TinyBertMLM, sentences: list[str]):
    """Show MLM predictions on masked sentences."""
    model.eval()
    print("=" * 70)
    print("MLM Prediction Demo")
    print("=" * 70)

    for sentence in sentences:
        ids = tokenize(sentence)
        if len(ids) < MAX_LEN:
            ids = ids + [PAD_IDX] * (MAX_LEN - len(ids))
        input_tensor = torch.tensor([ids], dtype=torch.long, device=device)
        masked_tensor, labels = apply_mlm_mask(input_tensor)

        with torch.no_grad():
            logits = model(masked_tensor)
            probs = F.softmax(logits, dim=-1)

        masked_words = [idx2word.get(int(mt), "?") for mt in masked_tensor[0]]
        orig_words = [idx2word.get(int(it), "?") for it in input_tensor[0]]

        print(f"\nInput : {' '.join(orig_words)}")
        print(f"Masked: {' '.join(masked_words)}")
        print("Output: ", end="")

        output_tokens = []
        for i in range(len(masked_words)):
            if masked_words[i] == "[MASK]":
                p = probs[0, i]
                top5 = p.topk(5)
                pred_word = idx2word[int(top5.indices[0])]
                output_tokens.append(f"{pred_word}({float(top5.values[0]):.2f})")

                # Show top-5 candidates for first mask
                first_visible = next(
                    (j for j, w in enumerate(masked_words) if w == "[MASK]"), -1
                )
                if i == first_visible:
                    candidates = [
                        f"{idx2word[int(top5.indices[k])]}({float(top5.values[k]):.3f})"
                        for k in range(5)
                    ]
                    has_only_masks = all(
                        w == "[MASK]" or w in ("[PAD]", "[CLS]", "[SEP]")
                        for w in masked_words
                    )
                    output_tokens[-1] += f"  [{', '.join(candidates)}]"
            else:
                if masked_words[i] not in ("[PAD]", "[CLS]", "[SEP]"):
                    output_tokens.append(masked_words[i])
                else:
                    output_tokens.append(masked_words[i])
        print(" ".join(output_tokens))
    print()


# ──────────────────────────────────────────────
# 7. Main
# ──────────────────────────────────────────────

def main():
    print("=" * 70)
    print("Masked Modeling (MLM) Demonstration")
    print("=" * 70)

    # Instantiate model
    model = TinyBertMLM(
        vocab_size=VOCAB_SIZE,
        d_model=64,       # tiny dimension
        nhead=4,
        num_layers=3,     # 3 transformer layers
        dim_feedforward=128,
        max_len=MAX_LEN,
    ).to(device)

    total_params = sum(p.numel() for p in model.parameters())
    print(f"\nModel parameters: {total_params:,} ({total_params/1e6:.2f}M)")
    print(f"Vocabulary size: {VOCAB_SIZE}")

    # Step 1: Visualize masking strategy
    show_mask_demo("the cat sat on the mat", model=None)

    # Step 2: Visualize attention pattern (MLM vs Autoregressive)
    visualize_attention_pattern()

    # Step 3: Initial predictions (before training)
    print("Before training:")
    pred_sentences = [
        "the [MASK] sat on the mat",
        "the sun [MASK] brightly",
        "a bird [MASK] in the sky",
    ]
    show_predictions(model, pred_sentences)

    # Step 4: Train
    _ = train_mlm(model, dataloader, num_epochs=80, lr=5e-4)

    # Step 5: Predictions after training
    print("After training:")
    show_predictions(model, pred_sentences)

    # Step 6: Show final masked prediction with top-5 confidence
    print("=" * 70)
    print("Final MLM Predictions with Top-5 Candidates")
    print("=" * 70)
    for sent in pred_sentences:
        ids = tokenize(sent)
        if len(ids) < MAX_LEN:
            ids = ids + [PAD_IDX] * (MAX_LEN - len(ids))
        input_tensor = torch.tensor([ids], dtype=torch.long, device=device)
        masked_tensor, labels = apply_mlm_mask(input_tensor)

        model.eval()
        with torch.no_grad():
            logits = model(masked_tensor)
            probs = F.softmax(logits, dim=-1)

        print(f"\nInput: {sent}")
        masked_positions = (labels[0] != -100).nonzero(as_tuple=True)[0]
        for pos in masked_positions:
            p = probs[0, pos]
            top5_vals, top5_idxs = p.topk(5)
            candidates = [
                f"{idx2word[int(top5_idxs[k])]}({float(top5_vals[k]):.4f})"
                for k in range(5)
            ]
            print(f"  Position {int(pos)}: {', '.join(candidates)}")
    print("\nDone!")


if __name__ == "__main__":
    main()
