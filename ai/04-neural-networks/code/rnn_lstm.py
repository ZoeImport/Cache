"""
rnn_lstm.py — LSTM Character-Level Text Generation
====================================================

Demonstrates:
  1. LSTM module definition in PyTorch
  2. Character-level language modeling (predict next character)
  3. Training loop with cross-entropy loss
  4. Text generation (sampling) at regular intervals
  5. Visual evidence of the model learning sequence patterns

Dependencies: torch >= 2.1.0, numpy

Usage:
    python rnn_lstm.py

Expected output: loss values decreasing over epochs followed by
generated character sequences that improve in quality.
"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# Device configuration
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"[INFO] Using device: {device}\n")

# ---------------------------------------------------------------------------
# 1. Data preparation: character-level encoding
# ---------------------------------------------------------------------------
# Use a short training text with repeated patterns so the LSTM can learn
# character-level dependencies.
TRAINING_TEXT = (
    "hello world "
    "this is a character level LSTM model "
    "it learns to predict the next character "
    "given a sequence of previous characters "
    "the model uses lstm gates to remember long term patterns "
    "vanishing gradients are no longer a problem "
)

train_text = TRAINING_TEXT.lower()

# Build character vocabulary
chars = sorted(list(set(train_text)))
vocab_size = len(chars)
char_to_idx = {ch: i for i, ch in enumerate(chars)}
idx_to_char = {i: ch for i, ch in enumerate(chars)}

print(f"[DATA] Training text length: {len(train_text)} characters")
print(f"[DATA] Vocabulary ({vocab_size} chars): {repr(''.join(chars))}")

# Encode entire text as integer indices
indices = [char_to_idx[ch] for ch in train_text]

# Sequence length for the LSTM ("look back window")
SEQ_LEN = 12

# Build (X, y) pairs: X is SEQ_LEN characters, y is the next character
X_data, y_data = [], []
for i in range(len(indices) - SEQ_LEN):
    X_data.append(indices[i : i + SEQ_LEN])
    y_data.append(indices[i + SEQ_LEN])

X_tensor = torch.tensor(X_data, dtype=torch.long, device=device)
y_tensor = torch.tensor(y_data, dtype=torch.long, device=device)

num_samples = len(X_data)
print(f"[DATA] {num_samples} training samples (seq_len={SEQ_LEN})")
print(f"[DATA] Sample: X='{train_text[:SEQ_LEN]}' -> y='{train_text[SEQ_LEN]}'\n")


# ---------------------------------------------------------------------------
# 2. LSTM Model definition
# ---------------------------------------------------------------------------
class CharLSTM(nn.Module):
    """
    Character-level language model using LSTM.

    Architecture:
        Embedding(vocab_size -> embed_dim)
            -> LSTM(embed_dim -> hidden_dim, num_layers)
            -> Linear(hidden_dim -> vocab_size)
    """

    def __init__(
        self,
        vocab_size: int,
        embed_dim: int = 32,
        hidden_dim: int = 64,
        num_layers: int = 2,
        dropout: float = 0.2,
    ):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers

        # Embedding: maps character indices to dense vectors
        self.embedding = nn.Embedding(vocab_size, embed_dim)

        # LSTM layer(s): the core recurrent component
        self.lstm = nn.LSTM(
            input_size=embed_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            dropout=dropout if num_layers > 1 else 0.0,
            batch_first=True,
        )

        # Output projection: LSTM output -> vocabulary logits
        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(
        self, x: torch.Tensor, hidden: tuple | None = None
    ) -> tuple[torch.Tensor, tuple[torch.Tensor, torch.Tensor]]:
        """
        Args:
            x: (batch, seq_len) — character indices
            hidden: optional (h0, c0) for the LSTM

        Returns:
            logits: (batch, vocab_size) — predictions for last time step
            hidden: (hn, cn) — final hidden states
        """
        emb = self.embedding(x)                     # (B, S) -> (B, S, E)
        lstm_out, hidden = self.lstm(emb, hidden)   # (B, S, E) -> (B, S, H)
        last_out = lstm_out[:, -1, :]               # take last time step
        logits = self.fc(last_out)                  # (B, H) -> (B, V)
        return logits, hidden

    def init_hidden(self, batch_size: int = 1) -> tuple[torch.Tensor, torch.Tensor]:
        h0 = torch.zeros(self.num_layers, batch_size, self.hidden_dim, device=device)
        c0 = torch.zeros(self.num_layers, batch_size, self.hidden_dim, device=device)
        return (h0, c0)


model = CharLSTM(
    vocab_size=vocab_size,
    embed_dim=32,
    hidden_dim=64,
    num_layers=2,
    dropout=0.2,
).to(device)

total_params = sum(p.numel() for p in model.parameters())
print(f"[MODEL] {model.__class__.__name__}")
print(f"[MODEL] Total parameters: {total_params:,}")
print(f"[MODEL] Architecture:\n{model}\n")


# ---------------------------------------------------------------------------
# 3. Text generation function
# ---------------------------------------------------------------------------
def generate_text(
    model: nn.Module,
    seed_str: str,
    gen_len: int = 80,
    temperature: float = 1.0,
) -> str:
    """
    Generate text by feeding the model's own predictions back as input.
    """
    model.eval()
    with torch.no_grad():
        seed = seed_str.lower()
        seed_indices = [char_to_idx.get(ch, 0) for ch in seed]
        input_seq = torch.tensor(seed_indices, dtype=torch.long, device=device).unsqueeze(0)

        generated = list(seed)
        hidden = model.init_hidden(batch_size=1)

        # Warm up hidden state with the seed
        _, hidden = model(input_seq, hidden)

        # Last seed character as first generation input
        current_input = torch.tensor(
            [[input_seq[0, -1].item()]], dtype=torch.long, device=device
        )

        for _ in range(gen_len):
            logits, hidden = model(current_input, hidden)
            scaled_logits = logits / temperature
            probs = torch.softmax(scaled_logits, dim=-1).squeeze(0)
            next_idx = torch.multinomial(probs, num_samples=1).item()
            generated.append(idx_to_char[next_idx])
            current_input = torch.tensor([[next_idx]], dtype=torch.long, device=device)

    return "".join(generated)


# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.005)

NUM_EPOCHS = 120
BATCH_SIZE = 32
PRINT_EVERY = 20
SAMPLE_EVERY = 30

print(f"[TRAIN] Starting training for {NUM_EPOCHS} epochs...\n")

# ---------------------------------------------------------------------------
# 4. Training loop
# ---------------------------------------------------------------------------
for epoch in range(1, NUM_EPOCHS + 1):
    model.train()
    epoch_loss = 0.0
    num_batches = 0

    perm = torch.randperm(num_samples, device=device)
    for start in range(0, num_samples, BATCH_SIZE):
        batch_idx = perm[start : start + BATCH_SIZE]
        batch_X = X_tensor[batch_idx]
        batch_y = y_tensor[batch_idx]

        logits, _ = model(batch_X)
        loss = criterion(logits, batch_y)

        optimizer.zero_grad()
        loss.backward()
        # Gradient clipping prevents exploding gradients
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=5.0)
        optimizer.step()

        epoch_loss += loss.item()
        num_batches += 1

    avg_loss = epoch_loss / num_batches

    if epoch % PRINT_EVERY == 0 or epoch == 1:
        print(f"  Epoch [{epoch:3d}/{NUM_EPOCHS}] — Loss: {avg_loss:.4f}")

    if epoch % SAMPLE_EVERY == 0 or epoch == 1:
        seed_str = "hello "
        gen = generate_text(model, seed_str, gen_len=60, temperature=0.8)
        print(f"  |-- Generated: \"{gen}\"")
        gen2 = generate_text(model, seed_str, gen_len=60, temperature=0.4)
        print(f"  +-- Generated (T=0.4): \"{gen2}\"")
        print()

print(f"[TRAIN] Training complete.\n")

# ---------------------------------------------------------------------------
# 5. Final evaluation: multiple samples across seeds and temperatures
# ---------------------------------------------------------------------------
print("=" * 65)
print("FINAL GENERATED TEXT SAMPLES")
print("=" * 65)

seed_texts = ["hello ", "this ", "the model "]
for seed in seed_texts:
    print(f"\n  Seed: \"{seed}\"")
    for temp in [0.3, 0.7, 1.2]:
        gen = generate_text(model, seed, gen_len=70, temperature=temp)
        print(f"    T={temp:.1f}: \"{gen}\"")

print("\n[DONE] LSTM character-level generation complete.")
