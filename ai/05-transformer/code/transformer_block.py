"""
transformer_block.py -- One Transformer Encoder Block from Scratch
===================================================================

Implements a complete Transformer Encoder block in PyTorch:
  1. Multi-Head Self-Attention (MHA)
  2. Residual Connection + Layer Norm (Pre-Norm style)
  3. Position-wise Feed-Forward Network (FFN) with ReLU
  4. Full forward pass on dummy data with shape trace
  5. Attention mask verification (padding mask)

Dependencies: torch, numpy (for verification)

Usage:
    python transformer_block.py

Expected output: console trace of every component's input/output shape
    + attention_heatmap.png showing the 8x8 attention weight matrix.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(precision=4, suppress=True)
torch.manual_seed(42)


# =========================================================================
# 1. Multi-Head Self-Attention
# =========================================================================
class MultiHeadAttention(nn.Module):
    """Multi-Head Self-Attention with scaled dot-product attention.

    Splits Q, K, V into h heads, computes attention in parallel,
    concatenates, then linearly projects.
    """

    def __init__(self, d_model: int, n_head: int):
        super().__init__()
        assert d_model % n_head == 0, "d_model must be divisible by n_head"

        self.d_model = d_model
        self.n_head = n_head
        self.d_k = d_model // n_head  # dimension per head

        # Single large matrices for all heads (efficient)
        self.W_Q = nn.Linear(d_model, d_model, bias=False)
        self.W_K = nn.Linear(d_model, d_model, bias=False)
        self.W_V = nn.Linear(d_model, d_model, bias=False)
        self.W_O = nn.Linear(d_model, d_model, bias=False)

    def forward(self, x: torch.Tensor, mask: torch.Tensor = None):
        # x shape: (batch, n_tokens, d_model)
        batch, n_tokens, _ = x.shape

        # Step 1: Project Q, K, V
        Q = self.W_Q(x)  # (batch, n_tokens, d_model)
        K = self.W_K(x)
        V = self.W_V(x)

        # Step 2: Reshape to (batch, n_head, n_tokens, d_k)
        Q = Q.view(batch, n_tokens, self.n_head, self.d_k).transpose(1, 2)
        K = K.view(batch, n_tokens, self.n_head, self.d_k).transpose(1, 2)
        V = V.view(batch, n_tokens, self.n_head, self.d_k).transpose(1, 2)

        # Step 3: Scaled dot-product attention
        # S = Q @ K^T / sqrt(d_k)  ->  (batch, n_head, n_tokens, n_tokens)
        scale = torch.sqrt(torch.tensor(self.d_k, dtype=torch.float32))
        S = (Q @ K.transpose(-2, -1)) / scale

        # Step 4: Apply mask (if provided)
        if mask is not None:
            # mask shape: (batch, 1, 1, n_tokens) -- broadcastable
            S = S.masked_fill(mask == 0, float("-inf"))

        # Step 5: Softmax over keys (last dim)
        A = F.softmax(S, dim=-1)  # attention weights

        # Step 6: Weighted sum of values
        Z = A @ V  # (batch, n_head, n_tokens, d_k)

        # Step 7: Concatenate heads -> (batch, n_tokens, d_model)
        Z = Z.transpose(1, 2).contiguous().view(batch, n_tokens, self.d_model)
        # Step 8: Final linear projection
        Z = self.W_O(Z)

        return Z, A  # return weights for inspection


# =========================================================================
# 2. Position-wise Feed-Forward Network
# =========================================================================
class FeedForward(nn.Module):
    """Two-layer FFN with ReLU activation.

    FFN(x) = W2 * ReLU(W1 * x + b1) + b2
    Hidden dimension is 4x the model dimension.
    """

    def __init__(self, d_model: int, d_ff: int = None):
        super().__init__()
        d_ff = d_ff or 4 * d_model
        self.W_1 = nn.Linear(d_model, d_ff)
        self.W_2 = nn.Linear(d_ff, d_model)

    def forward(self, x: torch.Tensor):
        return self.W_2(F.relu(self.W_1(x)))


# =========================================================================
# 3. Transformer Encoder Block
# =========================================================================
class TransformerEncoderBlock(nn.Module):
    """One Transformer Encoder block: MHA -> Add&Norm -> FFN -> Add&Norm.

    Uses Pre-Norm (LayerNorm before each sublayer) for training stability.
    """

    def __init__(self, d_model: int, n_head: int,
                 d_ff: int = None, dropout: float = 0.1):
        super().__init__()
        self.attention = MultiHeadAttention(d_model, n_head)
        self.ffn = FeedForward(d_model, d_ff)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x: torch.Tensor, mask: torch.Tensor = None):
        # Sublayer 1: Multi-Head Self-Attention + Add & Norm
        attn_out, attn_weights = self.attention(self.norm1(x), mask)
        x = x + self.dropout(attn_out)  # residual connection

        # Sublayer 2: FFN + Add & Norm
        ffn_out = self.ffn(self.norm2(x))
        x = x + self.dropout(ffn_out)  # residual connection

        return x, attn_weights


# =========================================================================
# 4. Demonstration: Forward Pass with Shape Trace
# =========================================================================
def run_demo():
    print("=" * 70)
    print("Transformer Encoder Block -- Forward Pass Demo")
    print("=" * 70)

    # Hyperparameters (small for clarity)
    batch_size = 2
    n_tokens = 8
    d_model = 16
    n_head = 4
    d_k = d_model // n_head  # 4
    d_ff = 4 * d_model  # 64

    print(f"\nHyperparameters:")
    print(f"  batch_size = {batch_size}  (number of sequences)")
    print(f"  n_tokens   = {n_tokens}    (sequence length)")
    print(f"  d_model    = {d_model}     (embedding dimension)")
    print(f"  n_head     = {n_head}      (attention heads)")
    print(f"  d_k        = {d_k}         (dimension per head)")
    print(f"  d_ff       = {d_ff}        (FFN hidden dimension)")

    # Create dummy data: random embeddings
    x = torch.randn(batch_size, n_tokens, d_model)

    print(f"\n{'=' * 70}")
    print(f"Input: x shape = {tuple(x.shape)}")
    print(f"{'=' * 70}")
    print(f"  batch={batch_size}, tokens={n_tokens}, d_model={d_model}")
    print(f"  Each token is a {d_model}-dim vector.")

    # Create padding mask: pretend the last 2 tokens in sequence 1 are padding
    mask = torch.ones(batch_size, 1, 1, n_tokens)
    mask[1, :, :, -2:] = 0  # sequence 1: last 2 tokens are padding

    print(f"\n{'=' * 70}")
    print(f"Padding Mask (1 = attend, 0 = ignore):")
    print(f"{'=' * 70}")
    print(f"  Sequence 0: all {n_tokens} tokens active")
    print(f"  Sequence 1: last 2 tokens masked out (padding)")
    print(f"\n  Mask shape: {tuple(mask.shape)}")
    print(f"  Mask[0,0,0,:] = {mask[0, 0, 0, :].numpy()}")
    print(f"  Mask[1,0,0,:] = {mask[1, 0, 0, :].numpy()}")

    # Instantiate the block
    block = TransformerEncoderBlock(d_model=d_model, n_head=n_head, dropout=0.0)
    block.eval()  # disable dropout for deterministic output

    # Forward pass
    with torch.no_grad():
        output, attn_weights = block(x, mask)

    # =====================================================================
    # 5. Shape Verification at Every Stage
    # =====================================================================
    print(f"\n{'=' * 70}")
    print("Shape Trace Through the Encoder Block")
    print("=" * 70)

    # Simulate the internal forward pass to get intermediate shapes
    with torch.no_grad():
        # Pre-Norm
        x_normed = block.norm1(x)
        # MHA internal
        Q = block.attention.W_Q(x_normed)
        K = block.attention.W_K(x_normed)
        V = block.attention.W_V(x_normed)
        # Reshape to heads
        Q_h = Q.view(batch_size, n_tokens, n_head, d_k).transpose(1, 2)
        K_h = K.view(batch_size, n_tokens, n_head, d_k).transpose(1, 2)
        V_h = V.view(batch_size, n_tokens, n_head, d_k).transpose(1, 2)
        # Scores
        scale = torch.sqrt(torch.tensor(d_k, dtype=torch.float32))
        S = (Q_h @ K_h.transpose(-2, -1)) / scale
        # After softmax
        A_internal = F.softmax(S, dim=-1)
        # After value aggregation
        Z_internal = A_internal @ V_h
        # Concatenate
        Z_concat = Z_internal.transpose(1, 2).contiguous().view(
            batch_size, n_tokens, d_model)
        # Final projection
        Z_final = block.attention.W_O(Z_concat)
        # Residual
        x_after_mha = x + Z_final
        # FFN path
        x_normed2 = block.norm2(x_after_mha)
        ffn_hidden = F.relu(block.ffn.W_1(x_normed2))
        ffn_out = block.ffn.W_2(ffn_hidden)

    trace = [
        ("Input", x.shape, "Raw token embeddings"),
        ("LayerNorm1(x)", x_normed.shape, "Pre-Norm before MHA"),
        ("Q = W_Q(x_normed)", Q.shape, "Query projection"),
        ("K = W_K(x_normed)", K.shape, "Key projection"),
        ("V = W_V(x_normed)", V.shape, "Value projection"),
        ("Reshape Q -> (B,H,T,d_k)", Q_h.shape,
         f"{n_head} heads x {d_k}-dim each"),
        ("Reshape K -> (B,H,T,d_k)", K_h.shape, ""),
        ("Reshape V -> (B,H,T,d_k)", V_h.shape, ""),
        ("S = Q@K^T / sqrt(d_k)", S.shape,
         f"Attention scores: each head has {n_tokens}x{n_tokens}"),
        ("A = softmax(S, dim=-1)", A_internal.shape,
         "Weights: each row sums to 1"),
        ("Z_head = A@V", Z_internal.shape, "Weighted sum per head"),
        ("Concat heads", Z_concat.shape, f"Back to {d_model}-dim"),
        ("W_O(Z_concat)", Z_final.shape, "Final MHA output"),
        ("x + MHA(x) [Residual]", x_after_mha.shape,
         "First residual connection"),
        ("LayerNorm2(x)", x_normed2.shape, "Pre-Norm before FFN"),
        ("ReLU(W_1(x))", ffn_hidden.shape,
         f"FFN hidden: d_ff={ffn_hidden.shape[-1]}"),
        ("W_2(hidden)", ffn_out.shape, "FFN output"),
        ("Output = x + FFN(x)", output.shape,
         "Final output (same shape as input)"),
    ]

    for name, shape, note in trace:
        note_str = f"  # {note}" if note else ""
        print(f"  {name:<35s} -> {str(shape):<20s}{note_str}")

    # =====================================================================
    # 6. Verification: Mask Effect on Attention Weights
    # =====================================================================
    print(f"\n{'=' * 70}")
    print("Mask Verification: Sequence 1 (last 2 tokens masked)")
    print("=" * 70)

    # attn_weights shape: (batch, n_head, n_tokens, n_tokens)
    # Look at head 0, query token 0 of sequence 1
    seq_idx = 1
    head_idx = 0
    query_idx = 0
    weights_seq1 = attn_weights[seq_idx, head_idx, query_idx, :].numpy()

    print(f"\n  Attention weights for Seq {seq_idx}, "
          f"Head {head_idx}, Query {query_idx}:")
    for k in range(n_tokens):
        is_masked = mask[seq_idx, 0, 0, k] == 0
        status = "MASKED" if is_masked else "attend"
        print(f"    -> Key {k}: weight = {weights_seq1[k]:.6f}  ({status})")

    # The sum should be exactly 1.0 across all positions
    sum_all = weights_seq1.sum()
    sum_active = weights_seq1[mask[seq_idx, 0, 0, :].numpy() == 1].sum()
    print(f"\n  Sum over all positions:        {sum_all:.6f}  "
          f"(should be ~1.0)")
    print(f"  Sum over non-masked positions: {sum_active:.6f}  "
          f"(should be ~1.0 -- redistributed from masked)")
    assert abs(sum_all - 1.0) < 1e-5, "Attention weights must sum to 1!"
    print(f"  OK: Attention weights sum to 1 -- "
          f"mask correctly redistributes weight.")

    # Verify that masked positions get zero weight
    for k in range(n_tokens):
        if mask[seq_idx, 0, 0, k] == 0:
            assert weights_seq1[k] == 0.0, \
                f"Masked key {k} should have weight 0!"
    print(f"  OK: All masked positions have exactly zero attention weight.")

    # =====================================================================
    # 7. Verify: Per-Query Top-3 Attention (Head 0)
    # =====================================================================
    print(f"\n{'=' * 70}")
    print("Per-Query Attention Distribution (Head 0)")
    print("=" * 70)
    for si in range(batch_size):
        print(f"\n  Sequence {si}:")
        for q in range(min(4, n_tokens)):  # show first 4 queries
            w = attn_weights[si, 0, q, :].numpy()
            top_k = np.argsort(w)[-3:][::-1]  # top-3 attended keys
            top_str = ", ".join([f"K{k} ({w[k]:.2f})" for k in top_k])
            print(f"    Query {q}: top-3 keys = [{top_str}]")

    # =====================================================================
    # 8. Visualization: Attention Heatmap
    # =====================================================================
    fig, axes = plt.subplots(2, 2, figsize=(10, 9))

    labels = [f"T{i}" for i in range(n_tokens)]

    for si in range(batch_size):
        for hi in range(2):  # show first 2 heads
            ax = axes[si, hi]
            A_plot = attn_weights[si, hi].numpy()
            im = ax.imshow(A_plot, cmap="YlOrRd", vmin=0, vmax=1)
            ax.set_xticks(range(n_tokens))
            ax.set_yticks(range(n_tokens))
            ax.set_xticklabels(labels, fontsize=8)
            ax.set_yticklabels(labels, fontsize=8)
            ax.set_xlabel("Key")
            ax.set_ylabel("Query")
            status = "masked (last 2)" if si == 1 else "full"
            ax.set_title(f"Seq {si} ({status}), Head {hi}", fontsize=10)

            # Annotate cells
            for i in range(n_tokens):
                for j in range(n_tokens):
                    val = A_plot[i, j]
                    color = "white" if val > 0.5 else "black"
                    ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                            fontsize=7, color=color)

            fig.colorbar(im, ax=ax, fraction=0.046)

    plt.suptitle("Attention Weights: Full vs Masked Sequence",
                 fontsize=13, y=1.01)
    plt.tight_layout()
    plt.savefig("ai/05-transformer/code/transformer_attention.png", dpi=150,
                bbox_inches="tight")
    print(f"\n[SAVED] transformer_attention.png")

    # =====================================================================
    # 9. Summary
    # =====================================================================
    print(f"\n{'=' * 70}")
    print("SUMMARY: Transformer Encoder Block Anatomy")
    print("=" * 70)
    print(f"""
  Input:  (batch, n_tokens, d_model) = ({batch_size}, {n_tokens}, {d_model})
  Output: (batch, n_tokens, d_model) = ({batch_size}, {n_tokens}, {d_model})

  +- Input -----------------------------+
  |                                     |
  |  LayerNorm    -- Pre-Norm           |
  |  Multi-Head Attention               |
  |    +-- Split into {n_head} heads (each {d_k}-dim)  |
  |    +-- Scaled dot-product: QK^T/sqrt({d_k})  |
  |    +-- Mask: -inf for padding       |
  |    +-- Softmax -> weights           |
  |    +-- Weighted sum -> concat-> W_O |
  |  + Residual Connection              |
  |                                     |
  |  LayerNorm    -- Pre-Norm           |
  |  Feed-Forward Network               |
  |    +-- W_1: Linear({d_model} -> {d_ff})     |
  |    +-- ReLU activation              |
  |    +-- W_2: Linear({d_ff} -> {d_model})    |
  |  + Residual Connection              |
  |                                     |
  +- Output ---------------------------+
""")
    print("[DONE] Transformer Encoder Block forward pass complete.")
    print(f"  Output shape: {output.shape} -- "
          f"same as input (residual design).")
    print(f"  Attention weights shape: {attn_weights.shape} -- "
          f"inspectable for debugging.")


if __name__ == "__main__":
    run_demo()
